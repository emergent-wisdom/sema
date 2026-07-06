from dataclasses import dataclass
from enum import Enum


class SemaViolation(Exception):
    pass


class ConstraintType(Enum):
    BINARY_FLAG = 1  # e.g., "NO_INTERNET"
    RESOURCE_MAX = 2  # e.g., "MAX_BUDGET"
    ALLOW_LIST = 3  # e.g., "ALLOWED_TOOLS"


@dataclass
class Constraint:
    type: ConstraintType
    value: any
    key: str | None = None

    def __hash__(self):
        # Allow use in sets
        return hash((self.type, str(self.value), self.key))


@dataclass
class TaskObj:
    id: str
    budget: float
    remaining_budget: float
    deadline: int
    constraints: list[Constraint]

    @property
    def allowed_tools(self) -> set[str]:
        # Extract tools from constraints
        tools = set()
        for c in self.constraints:
            if c.type == ConstraintType.ALLOW_LIST and c.key == "tools":
                tools.update(c.value)
        return tools

    @classmethod
    def from_dict(cls, data: dict) -> "TaskObj":
        constraints = []
        for c_data in data.get("constraints", []):
            # Parse constraint
            c_type_str = c_data.get("type")
            c_value = c_data.get("value")
            c_key = c_data.get("key")

            try:
                # getattr with a non-string name raises TypeError, so a
                # constraint dict missing "type" must be caught here too.
                c_type = getattr(ConstraintType, c_type_str)
                # Convert list values to sets for ALLOW_LIST
                if c_type == ConstraintType.ALLOW_LIST and isinstance(c_value, list):
                    c_value = set(c_value)
                constraints.append(Constraint(c_type, c_value, c_key))
            except (AttributeError, TypeError):
                pass  # Skip unknown or malformed types

        return cls(
            id=data.get("id", "unknown"),
            budget=float(data.get("budget", 0.0)),
            remaining_budget=float(data.get("remaining_budget", 0.0)),
            deadline=int(data.get("deadline", 0)),
            constraints=constraints,
        )


class SemaGuardian:
    def __init__(self):
        pass

    def enforce_holography(self, parent_task: TaskObj, child_task: TaskObj) -> bool:
        """
        Validates that a Child Task strictly inherits (or tightens)
        the safety constraints of the Parent Task.
        """

        # 1. BINARY FLAGS (Superset Check)
        # Rule: If Parent has a flag, Child MUST have it.
        parent_flags = set(
            c.value for c in parent_task.constraints if c.type == ConstraintType.BINARY_FLAG
        )
        child_flags = set(
            c.value for c in child_task.constraints if c.type == ConstraintType.BINARY_FLAG
        )

        missing_flags = parent_flags - child_flags
        if missing_flags:
            raise SemaViolation(
                f"🛑 ESCALATION ATTEMPT: Child task dropped constraints: {missing_flags}"
            )

        # 2. RESOURCE BOUNDS (Numeric Check)
        # Rule: Child budget <= Parent remaining budget
        if child_task.budget > parent_task.remaining_budget:
            raise SemaViolation(
                f"🛑 BUDGET OVERFLOW: Child requested {child_task.budget}, "
                f"Parent only has {parent_task.remaining_budget}"
            )

        # 3. ALLOW LISTS (Subset Check)
        # Rule: Child cannot access tools that Parent cannot access.
        parent_tools = parent_task.allowed_tools
        child_tools = child_task.allowed_tools

        # If parent has NO tool constraints (empty set might mean ALL or NONE depending on impl)
        # Let's assume explicit allow-list. If parent set is NOT empty, child must be subset.
        # If parent set is empty, implies no tools allowed? Or unlimited?
        # Safe default: If parent has defined tools, child must conform.
        if parent_tools:
            illegal_tools = child_tools - parent_tools
            if illegal_tools:
                raise SemaViolation(
                    f"🛑 TOOL ESCAPE: Child attempted to access forbidden tools: {illegal_tools}"
                )

        # 4. DEADLINE (Time Check)
        if child_task.deadline > parent_task.deadline:
            raise SemaViolation("🛑 TEMPORAL VIOLATION: Child deadline exceeds Parent timeframe")

        return True


# --- Simulation for Verification ---

if __name__ == "__main__":
    print("🛡️  Sema Kernel: Holographic Inheritance Test\n")

    # 1. Setup Parent Task (Restricted)
    parent = TaskObj(
        id="root_task",
        budget=100.0,
        remaining_budget=100.0,
        deadline=5000,
        constraints=[
            Constraint(ConstraintType.BINARY_FLAG, "NO_INTERNET"),
            Constraint(ConstraintType.ALLOW_LIST, {"calculator", "python"}, key="tools"),
        ],
    )
    print("📋 PARENT: Budget=100, Constraints=[NO_INTERNET], Tools={calculator, python}")

    guardian = SemaGuardian()

    # 2. Test Safe Child
    print("\n🔹 Test 1: Safe Child (Inherits All)")
    child_safe = TaskObj(
        id="sub_task_1",
        budget=50.0,
        remaining_budget=50.0,
        deadline=4000,
        constraints=[
            Constraint(ConstraintType.BINARY_FLAG, "NO_INTERNET"),
            Constraint(ConstraintType.ALLOW_LIST, {"calculator"}, key="tools"),
        ],
    )
    try:
        guardian.enforce_holography(parent, child_safe)
        print("✅ PASSED: Child is valid.")
    except SemaViolation as e:
        print(f"❌ FAILED: {e}")

    # 3. Test Attack: Dropping Constraint
    print("\n🔹 Test 2: Attack (Dropping NO_INTERNET)")
    child_unsafe_1 = TaskObj(
        id="sub_task_evil",
        budget=10.0,
        remaining_budget=10.0,
        deadline=4000,
        constraints=[
            # Missing NO_INTERNET
            Constraint(ConstraintType.ALLOW_LIST, {"calculator"}, key="tools")
        ],
    )
    try:
        guardian.enforce_holography(parent, child_unsafe_1)
        print("❌ FAILED: Attack succeeded (Bad!)")
    except SemaViolation as e:
        print(f"✅ BLOCKED: {e}")

    # 4. Test Attack: Budget Overflow
    print("\n🔹 Test 3: Attack (Budget Overflow)")
    child_unsafe_2 = TaskObj(
        id="sub_task_greedy",
        budget=200.0,  # > 100
        remaining_budget=200.0,
        deadline=4000,
        constraints=[Constraint(ConstraintType.BINARY_FLAG, "NO_INTERNET")],
    )
    try:
        guardian.enforce_holography(parent, child_unsafe_2)
        print("❌ FAILED: Attack succeeded (Bad!)")
    except SemaViolation as e:
        print(f"✅ BLOCKED: {e}")

    # 5. Test Attack: Tool Escape
    print("\n🔹 Test 4: Attack (Tool Escape - Adding 'bash')")
    child_unsafe_3 = TaskObj(
        id="sub_task_hack",
        budget=10.0,
        remaining_budget=10.0,
        deadline=4000,
        constraints=[
            Constraint(ConstraintType.BINARY_FLAG, "NO_INTERNET"),
            Constraint(ConstraintType.ALLOW_LIST, {"calculator", "python", "bash"}, key="tools"),
        ],
    )
    try:
        guardian.enforce_holography(parent, child_unsafe_3)
        print("❌ FAILED: Attack succeeded (Bad!)")
    except SemaViolation as e:
        print(f"✅ BLOCKED: {e}")
