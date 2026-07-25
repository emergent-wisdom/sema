"""
Sema Dependency Resolution and Topological Sorting.
Extracts dependency graph from patterns and enforces acyclic ordering.
"""

from collections import defaultdict, deque

from .validator import clean_handle

# Layer ordering: lower index = more fundamental (Rule 7.6)
# Dependencies should flow from higher to lower (specific -> general)
# Infrastructure underpins everything (data structures, constraints, resources)
LAYER_ORDER = {
    "Infrastructure": 0,  # Most fundamental - data structures, constraints
    "Physics": 1,  # State, events, physical laws
    "Mind": 2,  # Cognition, reasoning
    "Society": 3,  # Most abstract - coordination, governance
}


def get_layer(pattern: dict) -> str | None:
    """Extract layer from pattern _meta. Layer is path[0] in the path-based
    schema; falls back to legacy `_meta.layer` for pre-migration patterns."""
    meta = pattern.get("_meta") or {}
    path = meta.get("path")
    if path and isinstance(path, list) and path:
        return path[0]
    return meta.get("layer")


def get_dependencies_handles(p: dict) -> set[str]:
    """
    Return set of Handles that this pattern depends on.
    """
    deps = set()
    d = p.get("dependencies", {})

    # Categorized
    for cat in ["accepts", "yields", "composes_with", "references"]:
        if cat in d and isinstance(d[cat], dict):
            for val in d[cat].values():
                h = clean_handle(val)
                if h:
                    deps.add(h)

    return deps


# Buckets subject to layer-direction checking (Rule 7.6).
# The paper (§5.2) treats layer direction as a style guide for the full
# dependency set, but enforces it as a hard constraint on structural deps.
# Cross-layer soft links belong in references or _meta.related (Soft-Linking).
# - accepts: inputs the pattern reads — must be at or below its layer.
# - composes_with: subroutines invoked — must be at or below its layer.
# Excluded:
# - yields: outputs produced. Emergence goes upward (Mind yields Society artifacts).
# - references: soft citations/comparisons, not structural dependencies.
_LAYER_CHECKED_BUCKETS = ("accepts", "composes_with")


def get_layer_checked_handles(p: dict) -> set[str]:
    """
    Return handles from buckets subject to layer-direction checking.

    Layer direction applies to consumption (accepts, composes_with), not
    production (yields) or citation (references).
    """
    deps = set()
    d = p.get("dependencies", {})
    for cat in _LAYER_CHECKED_BUCKETS:
        if cat in d and isinstance(d[cat], dict):
            for val in d[cat].values():
                h = clean_handle(val)
                if h:
                    deps.add(h)
    return deps


def find_cycle_path(adj: dict[str, set[str]], nodes: set[str]) -> list[str] | None:
    """
    Find one cycle path in the dependency graph restricted to 'nodes'.
    adj: {dependent: {dependencies}}
    Returns list [A, B, C, A] where A depends on B, B depends on C, C depends on A.
    """
    # Filter adj to only include nodes in the cycle set
    subgraph = {u: [v for v in deps if v in nodes] for u, deps in adj.items() if u in nodes}

    visited = set()
    recursion_stack = set()
    path_stack = []

    def visit(u):
        visited.add(u)
        recursion_stack.add(u)
        path_stack.append(u)

        for v in subgraph.get(u, []):
            if v in recursion_stack:
                # Cycle found!
                # Extract cycle from path_stack
                cycle_start_index = path_stack.index(v)
                return path_stack[cycle_start_index:] + [v]
            if v not in visited:
                res = visit(v)
                if res:
                    return res

        recursion_stack.remove(u)
        path_stack.pop()
        return None

    for node in nodes:
        if node not in visited:
            res = visit(node)
            if res:
                return res
    return None


def build_dependency_adjacency(
    patterns_dict: dict[str, dict], existing_patterns: dict[str, dict] | None = None
) -> dict[str, set[str]]:
    """
    Return {dependent: {dependencies}} over the merged corpus.

    Patterns in patterns_dict win over same-handle entries in existing_patterns,
    because an add replaces the committed version. Edges to handles outside the
    merged corpus are dropped — they cannot participate in a cycle here.
    """
    merged = dict(existing_patterns or {})
    merged.update(patterns_dict)

    adj: dict[str, set[str]] = defaultdict(set)
    for handle, p in merged.items():
        for dep in get_dependencies_handles(p):
            if dep in merged and dep != handle:
                adj[handle].add(dep)
    return adj


def find_cycle_through(adj: dict[str, set[str]], start: str) -> list[str] | None:
    """
    Return a cycle path [start, ..., start] if `start` lies on one, else None.

    Breadth-first from start's dependencies, so each node is visited once and the
    walk is linear in the graph. A depth-first enumeration of paths would be
    exponential on a dense corpus.
    """
    parent: dict[str, str] = {}
    queue = deque()
    for v in sorted(adj.get(start, ())):
        parent[v] = start
        queue.append(v)

    while queue:
        u = queue.popleft()
        for v in sorted(adj.get(u, ())):
            if v == start:
                chain = [u]
                while chain[-1] != start:
                    chain.append(parent[chain[-1]])
                chain.reverse()
                return chain + [start]
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return None


def validate_acyclic(
    patterns_dict: dict[str, dict], existing_patterns: dict[str, dict] | None = None
) -> None:
    """
    Raise ValueError if any pattern being added lies on a dependency cycle.

    `topological_sort` sees only the batch, so its `dep in patterns_dict` filter
    silently drops every edge to a committed pattern. A mutual `references` pair
    between a staged pattern and a committed one is therefore invisible to it,
    and `sema apply --check` passed exactly that case — the full rebuild then
    rejected it, after having already replaced the database.

    Only cycles containing a pattern from the batch are reported. A cycle wholly
    inside the committed corpus is a pre-existing condition and must not block an
    unrelated change.

    Args:
        patterns_dict: New patterns being added {handle: pattern_data}
        existing_patterns: Already-committed patterns. Dependencies are stored as
            graph edges rather than on the node, so a caller reading from a
            GraphStore must supply {handle: {"dependencies": <edge deps>}}.

    Raises:
        ValueError: If a cycle through one of the added patterns is found.
    """
    adj = build_dependency_adjacency(patterns_dict, existing_patterns)

    for handle in sorted(patterns_dict):
        cycle = find_cycle_through(adj, handle)
        if cycle:
            raise ValueError(
                "Cycle detected in dependencies.\n"
                f"Cycle Path: {' --> '.join(cycle)}\n"
                "A dependency in one direction and a reference back is still a cycle. "
                "Where the reverse edge already exists, the relationship is in the graph "
                "from the side that does not cycle — name the other pattern in prose."
            )


def topological_sort(patterns_dict: dict[str, dict]) -> list[str]:
    """
    Returns a list of handles in dependency order (Leaf -> Root).
    patterns_dict: {handle: pattern_data}

    Raises:
        ValueError: If a cycle is detected (provides cycle details in message).
    """
    adj = defaultdict(set)
    for handle, p in patterns_dict.items():
        # Only depend on patterns that are IN this batch
        raw_deps = get_dependencies_handles(p)
        for dep in raw_deps:
            if dep in patterns_dict and dep != handle:
                adj[handle].add(dep)

    # Kahn's Algorithm
    in_degree = {h: 0 for h in patterns_dict}

    # Build graph: Dependency -> Dependent
    graph = defaultdict(list)
    for dependent, dependencies in adj.items():
        for dependency in dependencies:
            graph[dependency].append(dependent)
            in_degree[dependent] += 1

    queue = [h for h in patterns_dict if in_degree[h] == 0]
    order = []

    while queue:
        u = queue.pop(0)
        order.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(order) < len(patterns_dict):
        # Report the cycle
        remaining = set(patterns_dict.keys()) - set(order)
        cycle_path = find_cycle_path(adj, remaining)

        msg = f"Cycle detected in dependencies. Unsorted nodes: {len(remaining)}."
        if cycle_path:
            path_str = " --> ".join(cycle_path)
            msg += f"\nCycle Path: {path_str}"

        raise ValueError(msg)

    return order


def check_layer_direction(
    patterns_dict: dict[str, dict], existing_patterns: dict[str, dict] | None = None
) -> list[tuple[str, str, str, str]]:
    """
    Check for layer direction violations (Rule 7.6).

    A lower layer (e.g., Physics) should not depend on a higher layer (e.g., Society).
    Dependencies should flow from higher layers to lower (specific -> general).

    Args:
        patterns_dict: New patterns being added {handle: pattern_data}
        existing_patterns: Already-committed patterns for reference lookup

    Returns:
        List of violations as (pattern_handle, pattern_layer, dep_handle, dep_layer)
    """
    all_patterns = {**(existing_patterns or {}), **patterns_dict}
    violations = []

    for handle, pattern in patterns_dict.items():
        pattern_layer = get_layer(pattern)
        if pattern_layer is None or pattern_layer not in LAYER_ORDER:
            continue

        pattern_level = LAYER_ORDER[pattern_layer]
        deps = get_layer_checked_handles(pattern)

        for dep_handle in deps:
            if dep_handle not in all_patterns:
                continue  # Unknown dependency, skip

            dep_layer = get_layer(all_patterns[dep_handle])
            if dep_layer is None or dep_layer not in LAYER_ORDER:
                continue

            dep_level = LAYER_ORDER[dep_layer]

            # Violation: depending on a HIGHER layer (more abstract)
            if dep_level > pattern_level:
                violations.append((handle, pattern_layer, dep_handle, dep_layer))

    return violations


def validate_layer_direction(
    patterns_dict: dict[str, dict], existing_patterns: dict[str, dict] | None = None
) -> None:
    """
    Validate layer direction and raise ValueError if violations found (Rule 7.6).

    Args:
        patterns_dict: New patterns being added
        existing_patterns: Already-committed patterns

    Raises:
        ValueError: If any layer direction violations are found
    """
    violations = check_layer_direction(patterns_dict, existing_patterns)

    if violations:
        msg_parts = ["Layer direction violation (Rule 7.6):"]
        for handle, p_layer, dep_handle, d_layer in violations:
            msg_parts.append(
                f"  '{handle}' ({p_layer}) cannot depend on '{dep_handle}' ({d_layer}) - "
                f"lower layers cannot depend on higher layers"
            )
        raise ValueError("\n".join(msg_parts))
