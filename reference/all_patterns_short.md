# Sema Vocabulary (Short Hand JSON)

**Total Patterns:** 452
**Format:** JSON with short-hand references.

---

# Layer: Infrastructure

## Aesthetics#ff5f

```json
{
  "handle": "Aesthetics",
  "mechanism": "A scalar {{metric}} representing the fit between an {{artifact}} and the subjective preference priors of a human observer (e.g., harmony, {{parsimony}}, style). Used to optimize solutions for social acceptance when functional utility is equal.",
  "gloss": "Optimization for human subjective preference",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Aesthetics#mh:SHA-256:ff5fc266152e3d1478a89aaf8fbef38fc10cc9c9da5c7b3cb7b10a1245a896ef",
  "sema_ref": "Aesthetics#ff5f",
  "sema_stub": "ff5f",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "An aesthetic assessment \u2014 a metric-shaped artifact capturing perceived beauty/quality on a defined scale.",
    "properties": {
      "axis": {
        "type": "string",
        "description": "Which aesthetic dimension is being rated"
      },
      "score": {
        "type": "number",
        "description": "Rating on the axis"
      },
      "normalized_range": {
        "type": "object",
        "properties": {
          "min": {
            "type": "number"
          },
          "max": {
            "type": "number"
          }
        }
      }
    }
  },
  "dependencies": {
    "references": {
      "metric": "Metric#17fd",
      "parsimony": "Parsimony#8476",
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## Anomaly#fac8

```json
{
  "handle": "Anomaly",
  "mechanism": "A {{datum}} whose observed value falls outside the expected baseline by a measurable deviation score. Anomalies carry the (observed, expected, deviation) triple as first-class structure, so they can be routed, ranked, and triaged. Serves as the trigger artifact for investigation, learning, and diagnostic workflows.",
  "gloss": "Datum whose observed value deviates from the expected baseline, triggering investigation",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "observed_value",
      "expected_baseline",
      "deviation_score"
    ],
    "properties": {
      "observed_value": {
        "description": "The data point that triggered detection (any type)"
      },
      "expected_baseline": {
        "description": "The prediction or mean value (any type)"
      },
      "deviation_score": {
        "type": "number",
        "description": "Standard deviations (sigma) or distance metric"
      },
      "detected_at": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Anomaly#mh:SHA-256:fac884f940feb1f3cac089ab3165cb71f514f5d6e54e43506ed6e52942ed7730",
  "sema_ref": "Anomaly#fac8",
  "sema_stub": "fac8",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Artifact#6254

```json
{
  "handle": "Artifact",
  "mechanism": "A discrete, immutable unit of data produced by a solver or workflow. It serves as a typed input/output token.",
  "gloss": "Immutable data unit",
  "failure_modes": [
    "Link Rot: The artifact persists conceptually but the storage medium fails.",
    "Hash Collision: Two different artifacts produce the same ID (theoretical risk)."
  ],
  "invariants": [
    "Immutability: Once minted, the content cannot change.",
    "Addressability: Must be referenceable by a content-derived hash."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Artifact#mh:SHA-256:6254c09973118bce3ba2813b7494dee7a61c8b2a87fbcb4d2830f9fbf8d29cf9",
  "sema_ref": "Artifact#6254",
  "sema_stub": "6254",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "hash",
      "content_type",
      "uri"
    ],
    "properties": {
      "hash": {
        "type": "string",
        "description": "SHA-256 content hash (Immutable ID)"
      },
      "content_type": {
        "type": "string",
        "description": "MIME type (e.g., application/json, text/markdown)"
      },
      "uri": {
        "type": "string",
        "description": "Storage location (s3://, ipfs://, or memory://)"
      },
      "size_bytes": {
        "type": "integer"
      },
      "metadata": {
        "type": "object",
        "description": "Author, timestamp, tags"
      }
    }
  }
}
```

---

## Assessment#a765

```json
{
  "handle": "Assessment",
  "mechanism": "A structured qualitative evaluation of a target artifact, produced by critique, containing identified strengths, weaknesses, and specific recommendations for improvement. It serves as the input for reflexion and refinement loops.",
  "gloss": "Structured qualitative feedback",
  "invariants": [
    "Actionability: Must contain at least one specific recommendation.",
    "Reference: Must cite specific parts of the target artifact."
  ],
  "sema_id": "sema:Assessment#mh:SHA-256:a76518b956c1f22aec39c6402db8725510ea23bd6eda56844ef118a948de3c77",
  "sema_ref": "Assessment#a765",
  "sema_stub": "a765",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "target_ref",
      "recommendations"
    ],
    "properties": {
      "target_ref": {
        "type": "string",
        "description": "Reference to artifact being assessed"
      },
      "strengths": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Positive aspects"
      },
      "weaknesses": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Areas for improvement"
      },
      "recommendations": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Actionable suggestions"
      }
    }
  }
}
```

---

## Assumption#efb5

```json
{
  "handle": "Assumption",
  "mechanism": "A gap-filler used when {{datum}} is missing; treated as true temporarily to allow thinking to proceed. Must be tracked and validated.",
  "gloss": "Provisional truth",
  "invariants": [
    "Provisionality: Must be explicitly flagged as unverified.",
    "Tracking: Must maintain a link to the missing datum it replaces."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "premise",
      "risk_level"
    ],
    "properties": {
      "premise": {
        "type": "string",
        "description": "The statement treated as temporarily true"
      },
      "risk_level": {
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "Probability of falsity"
      },
      "criticality": {
        "type": "string",
        "enum": [
          "Low",
          "Medium",
          "Existential"
        ],
        "description": "Impact if assumption fails"
      },
      "validation_deadline": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Assumption#mh:SHA-256:efb5be2691c91cb98b493543154f2a9d7d492911088e3bf1cbc048f5ac317978",
  "sema_ref": "Assumption#efb5",
  "sema_stub": "efb5",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Audit#6888

```json
{
  "handle": "Audit",
  "mechanism": "A structured record produced by a verification event: the artifact naming what was checked, who checked it, when, the inputs and outputs, and the decision reached. Distinct from the verb 'to audit' \u2014 this Noun is the durable output that downstream callers consume and reference. Used as {{state}}-grounded evidence when disputes over {{system}} behavior arise.",
  "gloss": "Verification of conformance",
  "invariants": [
    "Immutability: Audit logs cannot be altered once written.",
    "Completeness: All checked items must have a verdict."
  ],
  "preconditions": [
    "Target {{system}} exists and is accessible"
  ],
  "postconditions": [
    "Audit report generated",
    "Pass/Fail status assigned"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "target_id",
      "auditor_id",
      "verdict",
      "timestamp"
    ],
    "properties": {
      "target_id": {
        "type": "string",
        "description": "Hash or ID of the system/artifact audited"
      },
      "auditor_id": {
        "type": "string",
        "description": "ID of the agent performing the check"
      },
      "verdict": {
        "type": "string",
        "enum": [
          "Pass",
          "Fail",
          "Warn"
        ],
        "description": "Conformance result"
      },
      "evidence_log": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of checks performed"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "sema_id": "sema:Audit#mh:SHA-256:68888bbb031dec6f35f66748f2b6f415e6852897bf4e8c20817bedfc998ae8ae",
  "sema_ref": "Audit#6888",
  "sema_stub": "6888",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314"
    }
  }
}
```

---

## Ballot#2a0a

```json
{
  "handle": "Ballot",
  "mechanism": "A structured container for a decision proposal. Contains: the question being decided, available options, voting rules (majority/supermajority/unanimity), and deadline. The Ballot is immutable once cast \u2014 amendments require a new Ballot carrying a fresh {{monotonic_counter}} sequence, so revocation and amendment are surfaced as distinct subsequent decisions rather than retroactive edits.",
  "gloss": "Immutable container for collective decision inputs",
  "failure_modes": [
    "Spoiled ballot: ambiguous or invalid {{select}} format.",
    "Double Voting: Single agent submitting multiple ballots (Sybil risk)."
  ],
  "invariants": [
    "Completeness: Must specify question, options, and decision rule",
    "Immutability: Once created, a Ballot cannot be modified"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "ballot_id",
      "proposal_id",
      "voter_id",
      "choice"
    ],
    "properties": {
      "ballot_id": {
        "type": "string"
      },
      "proposal_id": {
        "type": "string"
      },
      "voter_id": {
        "type": "string"
      },
      "choice": {
        "type": "string",
        "description": "The selected option"
      },
      "weight": {
        "type": "number",
        "default": 1.0
      },
      "signature": {
        "type": "string",
        "description": "Cryptographic proof of vote"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "sema_ref": "Ballot#2a0a",
  "sema_id": "sema:Ballot#mh:SHA-256:2a0a8f2f1e8ca0098edca2107bb8cf2ea129dc09f44162faa284a5d18a021db1",
  "sema_stub": "2a0a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "monotonic_counter": "MonotonicCounter#cf62",
      "select": "Select#15c2"
    }
  }
}
```

---

## Belief#a9ce

```json
{
  "handle": "Belief",
  "mechanism": "A unit of epistemic {{state}}. Represents a claim held by an {{agent}} with a specific confidence score (0.0 to 1.0) and a pointer to supporting {{evidence}}. Unlike a Fact, a Belief is subjective and mutable.",
  "gloss": "A subjective claim with confidence and evidence",
  "parameters": [
    {
      "name": "confidence",
      "type": "Probability#356b",
      "range": "[0.0, 1.0]",
      "description": "Subjective probability that this belief is true"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "data_schema": {
    "type": "object",
    "required": [
      "proposition",
      "confidence"
    ],
    "properties": {
      "proposition": {
        "type": "string",
        "description": "The claim held by the agent"
      },
      "confidence": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "Subjective probability (Bayesian Prior)"
      },
      "supporting_evidence": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "IDs of observations supporting this belief"
      },
      "provenance": {
        "type": "string",
        "description": "Source of the belief (Inference, Axiom, Observation)"
      }
    }
  },
  "sema_id": "sema:Belief#mh:SHA-256:a9ced589ce7984846cd86ebe6f937cd3b33f2435c5f56c60157e98b1aa868d71",
  "sema_ref": "Belief#a9ce",
  "sema_stub": "a9ce",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "agent": "Agent#35b9"
    },
    "accepts": {
      "context": "Context#510a"
    }
  }
}
```

---

## Boolean#2e6b

```json
{
  "handle": "Boolean",
  "mechanism": "The primitive true/false type. A Boolean value is one of exactly two mutually exclusive members: true or false. Used as the output type of schema-validation and as the evaluation return of conditional traits. Distinct from the three-state Decision (proceed/halt/debt) and from the graded Status (verified/falsified/unknown): Boolean admits no middle value.",
  "gloss": "Binary truth value \u2014 true or false",
  "data_schema": {
    "type": "object",
    "required": [
      "value"
    ],
    "properties": {
      "value": {
        "type": "boolean",
        "description": "The truth value: true or false"
      }
    }
  },
  "invariants": [
    "Exhaustive: every Boolean value is one of exactly two members.",
    "Exclusive: no value is simultaneously true and false."
  ],
  "_meta": {
    "tier": 0,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Boolean#mh:SHA-256:2e6b2b2f8b0ae5c6060b15cd6cb6cb3bf21d40a4effbc18aff354559195f9217",
  "sema_ref": "Boolean#2e6b",
  "sema_stub": "2e6b"
}
```

---

## Break#177f

```json
{
  "handle": "Break",
  "data_schema": {
    "type": "object",
    "required": [
      "break_id",
      "severity"
    ],
    "properties": {
      "break_id": {
        "type": "string",
        "description": "Unique identifier for this break event"
      },
      "severity": {
        "type": "string",
        "enum": [
          "transient",
          "permanent",
          "catastrophic"
        ],
        "description": "How serious is the failure"
      },
      "reason": {
        "type": "string",
        "description": "Human-readable explanation of the break cause"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "When the break occurred"
      }
    }
  },
  "mechanism": "{{protocol}} for announcing coordination failure. Failing {{agent}} broadcasts BREAK: {severity, reason, recoverable}. Partners must ACK. Coordination terminates or pauses based on severity. Unacknowledged BREAK escalates to FAILED. It coordinates with retry logic to distinguish transient from permanent failures, optionally triggering ejection seat in catastrophic scenarios.",
  "gloss": "Failure-announcement signal {severity, reason, recoverable}, ACK-required",
  "failure_modes": [
    "BREAK {{message}} itself fails to deliver ({{meta}}-failure).",
    "Partners disagree on recovery action.",
    "Cascading BREAKs overwhelm system.",
    "Inaccurate completed_state leads to wrong compensation.",
    "Timeout too short/long for ACK collection."
  ],
  "invariants": [
    "No data loss during interruption",
    "{{system}} state paused safely"
  ],
  "preconditions": [
    "Interrupt signal",
    "Running process"
  ],
  "postconditions": [
    "Process halted",
    "Resumption point saved"
  ],
  "parameters": [
    {
      "name": "break_signal",
      "type": "Enum",
      "range": "{Silent, Loud, Cascade}",
      "description": "How break propagates"
    },
    {
      "name": "failure_threshold",
      "type": "Integer",
      "range": "[3, 10]",
      "description": "Consecutive failures before breaking"
    },
    {
      "name": "recovery_timeout",
      "type": "Duration",
      "range": "[10s, 5min]",
      "description": "Cool-off before reconnection attempt"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "related": [
      "EjectionSeat#d53e",
      "Retry#4cc6"
    ]
  },
  "sema_id": "sema:Break#mh:SHA-256:177fbff7700762a276d46156ed96359955d7f1614857f2b4f13285473c7f782f",
  "sema_ref": "Break#177f",
  "sema_stub": "177f",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "message": "Message#f767",
      "system": "System#e314",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Card#2d01

```json
{
  "handle": "Card",
  "data_schema": {
    "type": "object",
    "required": [
      "public_key",
      "claims"
    ],
    "properties": {
      "public_key": {
        "type": "string",
        "description": "Cryptographic identifier of the Agent"
      },
      "claims": {
        "type": "object",
        "description": "Map of protocols and capabilities supported"
      },
      "reputation_score": {
        "type": "number",
        "description": "Aggregate trust metric (optional)"
      },
      "endpoints": {
        "type": "array",
        "description": "Reachability addresses"
      }
    }
  },
  "mechanism": "Structured capability advertisement enabling agent discovery before contact. {{agent}} creates CARD: {agent_id (unique), endpoint (how to reach), protocols[] (compatibility), capabilities[] (what agent claims to do), constraints (availability, rate limits, requirements), metadata (version, ttl, published timestamp)}. {{agent}} PUBLISHES card via registry, broadcast, DHT, or well-known endpoint (mechanism-agnostic). Discovering agents QUERY using {{latent_attachment}} for semantic capability matching alongside exact protocol_match. Query returns ranked CARD list. Discoverer selects promising CARDs, then GREETs at card.endpoint to establish channel. CARDs have TTL \u2014 agents must REFRESH periodically to maintain visibility. CARD capabilities are CLAIMS not proofs: verification happens via {{probe}} after GREET establishes channel. It enables discovery via {{select}} queries against the registry, filtering candidates by capability and protocol compatibility.",
  "gloss": "Structured capability advertisement: agent_id, endpoint, protocols, capabilities, metadata",
  "parameters": [
    {
      "name": "verification_tier",
      "type": "Enum",
      "range": "{SelfReported, Verified, Bonded}",
      "description": "Default: SelfReported"
    }
  ],
  "failure_modes": [
    "Stale CARDs (agent changed capabilities, CARD not updated\u2014TTL mitigates).",
    "False claims (CARD says X, agent cannot X\u2014PROBE mitigates).",
    "Registry unavailable (discovery fails\u2014use multiple publication methods).",
    "CARD spam (fake CARDs pollute discovery\u2014use reputation/filtering).",
    "Privacy leak (CARD reveals too much about agent\u2014include only necessary info).",
    "Version skew (CARD protocol version differs from actual\u2014GREET catches this)."
  ],
  "invariants": [
    "Card immutable after issue."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Card#mh:SHA-256:2d012468b060b33e8b77e1a35d5e09a13ec01a94d8969084fdbd64eba428d9e3",
  "sema_ref": "Card#2d01",
  "sema_stub": "2d01",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "probe": "Probe#12d8",
      "latent_attachment": "LatentAttachment#ab68",
      "agent": "Agent#35b9"
    },
    "composes_with": {
      "select": "Select#15c2"
    }
  }
}
```

---

## Category#1ab7

```json
{
  "handle": "Category",
  "data_schema": {
    "type": "object",
    "required": [
      "label"
    ],
    "properties": {
      "label": {
        "type": "string",
        "description": "Name of the category"
      },
      "parent": {
        "type": "string",
        "description": "Parent category ID (optional, for hierarchies)"
      },
      "members": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "IDs of items belonging to this category"
      }
    }
  },
  "mechanism": "A specific grouping or 'bin' for objects. It defines the taxonomy and allows the agent to treat distinct items as equivalent for certain operations.",
  "gloss": "Grouping of objects",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1",
  "sema_ref": "Category#1ab7",
  "sema_stub": "1ab7"
}
```

---

## Chain#711e

```json
{
  "handle": "Chain",
  "data_schema": {
    "type": "object",
    "required": [
      "nodes",
      "edges",
      "root_id"
    ],
    "properties": {
      "nodes": {
        "type": "array"
      },
      "edges": {
        "type": "array"
      },
      "root_id": {
        "type": "string"
      }
    }
  },
  "mechanism": "A concrete sequential data structure: a list of linked nodes where each node (except the last) points to exactly one successor. Chain is the instantiated storage object \u2014 distinct from the more abstract {{sequence}} (which describes temporal ordering semantics) and from the branching {{tree}} topology. Chain is the canonical spatial form for strictly sequential, non-branching data.",
  "gloss": "Sequential data container (linked list)",
  "invariants": [
    "Connectivity: Node(N) must point to Node(N+1).",
    "Acyclicity: No loops permitted."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2,
    "supersedes": [
      "sema:Linear#mh:SHA-256:81affcd5f7c1ea56b7572799fc235cf95d4e3c692de77c9eb8c01930b8e1d41c"
    ]
  },
  "sema_id": "sema:Chain#mh:SHA-256:711e99072dc1ff9112f4840a6fcbe256b090f0b20c426ba7f3628ea58c15f358",
  "sema_ref": "Chain#711e",
  "sema_stub": "711e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "sequence": "Sequence#b0b8",
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## CognitiveBias#4b32

```json
{
  "handle": "CognitiveBias",
  "mechanism": "A structural error definition describing a specific distortion in information processing. The 'lens' is curved, distorting the interpretation of {{datum}}.",
  "gloss": "Structural processing error definition",
  "data_schema": {
    "type": "object",
    "required": [
      "name",
      "distortion_type"
    ],
    "properties": {
      "name": {
        "type": "string"
      },
      "distortion_type": {
        "type": "string"
      },
      "correction_strategy": {
        "type": "string"
      }
    }
  },
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:CognitiveBias#mh:SHA-256:4b32f79732d4468fa0de4facb106dbbd2889bfa1d3ce62e77b09e606011680c9",
  "sema_ref": "CognitiveBias#4b32",
  "sema_stub": "4b32",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## ConceptAnchor#9187

```json
{
  "handle": "ConceptAnchor",
  "data_schema": {
    "type": "object",
    "required": [
      "definition_hash"
    ],
    "properties": {
      "definition_hash": {
        "type": "string",
        "description": "Content-addressed hash of the anchored definition"
      },
      "content": {
        "description": "The actual definition content - any valid JSON (schema, text, or structured data)"
      },
      "metadata": {
        "type": "object",
        "description": "Optional metadata (creator, timestamp, version)"
      }
    }
  },
  "mechanism": "Agents do not define terms inline; they reference immutable, content-addressed 'Concept Anchors' stored globally. 'I want [hash:Apple]', not 'I want an apple'. It is established via an external drop event that finalizes the definition hash.",
  "gloss": "Pinning meaning to immutable references",
  "failure_modes": [
    "Link rot (if anchors disappear)."
  ],
  "invariants": [
    "Immutability: The definition pointed to by the Anchor Hash cannot change",
    "Immutable Reference",
    "Resolution: The Anchor must resolve to a valid schema or content"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_id": "sema:ConceptAnchor#mh:SHA-256:91873000b379e08c41bc3fe3fea23f1f0870600871f89cca46ecbc87cc1d69d0",
  "sema_ref": "ConceptAnchor#9187",
  "sema_stub": "9187",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Condition#cbd5

```json
{
  "handle": "Condition",
  "data_schema": {
    "type": "object",
    "required": [
      "predicate"
    ],
    "properties": {
      "predicate": {
        "type": "string",
        "description": "The boolean expression or check to evaluate"
      },
      "required_context": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Keys that must be present in context for evaluation"
      },
      "timeout_ms": {
        "type": "integer",
        "description": "Maximum time allowed for evaluation before returning Error"
      }
    }
  },
  "mechanism": "A marker interface (Trait). Patterns implementing 'Condition' MUST provide an evaluation logic that returns a strict Boolean (True/False) based on provided context.",
  "gloss": "Interface for patterns that evaluate to a boolean truth-value",
  "failure_modes": [
    "Ambiguity: Returning 'Maybe' or probabilistic float where Boolean is required."
  ],
  "invariants": [
    "Boolean Output: Result must be binary.",
    "Decidability: Must always return a value (or error), never hang."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Condition#mh:SHA-256:cbd53b7aaedc24a8cb5f0b95661b5053850b6fd8198ba6d490bc8b7374739c6e",
  "sema_ref": "Condition#cbd5",
  "sema_stub": "cbd5",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Constraint#87fe

```json
{
  "handle": "Constraint",
  "data_schema": {
    "type": "object",
    "required": [
      "constraint_type",
      "expression"
    ],
    "properties": {
      "constraint_type": {
        "type": "string",
        "enum": [
          "resource",
          "safety",
          "legal",
          "physical"
        ],
        "description": "Category of constraint"
      },
      "expression": {
        "type": "string",
        "description": "The constraint as a boolean expression or inequality"
      },
      "priority": {
        "type": "integer",
        "description": "Enforcement order when multiple constraints apply"
      },
      "source": {
        "type": "string",
        "description": "Origin of the constraint (parent task, law, etc.)"
      }
    }
  },
  "mechanism": "A boundary condition that must be satisfied by any valid solution. Constraints are non-compensatory: violating one constraint cannot be offset by exceeding another. They come in types: Resource (budget, time), Safety (harm prevention), Legal (compliance), Physical (laws of nature). Constraints propagate via Holographic Inheritance: child tasks inherit parent constraints.",
  "gloss": "Non-negotiable boundary condition",
  "failure_modes": [
    "Constraint Relaxation: Silently loosening a constraint to fit a preferred solution.",
    "Hidden Constraint: A real-world constraint not captured in the specification.",
    "Constraint Conflict: Two constraints are mutually exclusive (no solution exists)."
  ],
  "invariants": [
    "Non-Compensatory: Violation of any constraint = rejection.",
    "Inheritance: Child constraints must include all parent constraints.",
    "Explicitness: All constraints must be stated, not implied."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Constraint#mh:SHA-256:87fec7246c97fce8fbd2a8cf829d08f623839f9f6da7a3c4a7db2a2bf70a9551",
  "sema_ref": "Constraint#87fe",
  "sema_stub": "87fe",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Context#510a

```json
{
  "handle": "Context",
  "mechanism": "The portable execution environment and state container for an agent. It encapsulates: (1) Inherited Constraints (Safety/Budget), (2) Available Tools/Capabilities, (3) Working Memory (History/Variables), and (4) {{identity}} Claims. Context flows through delegation chains, acting as the 'Stack Frame' of the agentic system. It allows agents to be paused, moved, or cloned.",
  "gloss": "Portable execution environment with inherited constraints",
  "failure_modes": [
    "Context Contamination/Leak: Private data from one context leaking into another (e.g., across tenant boundaries).",
    "Context Poisoning: malicious prompts or data injected into the context to hijack agent behavior.",
    "Stale Context: Acting on outdated information after a long pause.",
    "Context Explosion: Size grows beyond the window limit of the model."
  ],
  "invariants": [
    "{{constraint}} Monotonicity: Child contexts can ADD constraints but never REMOVE inherited ones.",
    "Serializability: The entire context must be serializable to JSON/Storage for persistence.",
    "Provenance: Every item in the context must be traceable to its source (Observation, User Input, or Inference)."
  ],
  "preconditions": [
    "Parent context exists (or Root is created)",
    "Schema is defined"
  ],
  "postconditions": [
    "agent has a valid environment to Execute"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "related": [
      "ContextCompress#4845",
      "ContextSwitch#590e",
      "AnchorDrop#26a2"
    ],
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string"
      },
      "constraints": {
        "type": "array"
      },
      "history": {
        "type": "array"
      },
      "variables": {
        "type": "object"
      }
    }
  },
  "sema_id": "sema:Context#mh:SHA-256:510af8317d84bfff7dbba4ebbe2ae2a14d0e28ed8ed342a4e8dbc2e3294c1353",
  "sema_ref": "Context#510a",
  "sema_stub": "510a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Contract#498e

```json
{
  "handle": "Contract",
  "data_schema": {
    "type": "object",
    "required": [
      "contract_id",
      "parties",
      "terms"
    ],
    "properties": {
      "contract_id": {
        "type": "string",
        "description": "Unique identifier for this contract"
      },
      "parties": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Identity IDs of all parties"
      },
      "terms": {
        "type": "array",
        "items": {
          "type": "object"
        },
        "description": "Array of Condition objects defining obligations"
      },
      "signatures": {
        "type": "object",
        "description": "Map of party ID to cryptographic signature"
      },
      "created_at": {
        "type": "string",
        "format": "date-time",
        "description": "When the contract was created"
      }
    }
  },
  "mechanism": "An immutable record of agreement between two or more {{identity}}s, acting as a multi-party {{commitment_device}}. It aggregates a set of {{condition}}s (terms) and obligations which all parties must {{sign}} to accept. Contracts serve as the binding {{context}} for disputes resolved by a {{judge}}.",
  "gloss": "Binding agreement between parties",
  "failure_modes": [
    "Ambiguity: Terms are open to interpretation.",
    "Unsigned: Not all parties have signed (invalid).",
    "Void: Conditions violate higher-law constraints."
  ],
  "invariants": [
    "Consent: Must be signed by all named parties.",
    "Immutability: Terms cannot change after signing.",
    "Enforceability: Terms must be verifiable by a third party."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_id": "sema:Contract#mh:SHA-256:498e450f3f218e74b8eff287f799dc441e35aaa3320891207300f91b8fe8e0c8",
  "sema_ref": "Contract#498e",
  "sema_stub": "498e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "context": "Context#510a",
      "commitment_device": "CommitmentDevice#6c21",
      "identity": "Identity#626c",
      "judge": "Judge#9554",
      "sign": "Sign#1fb9"
    },
    "accepts": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## Correlation#148d

```json
{
  "handle": "Correlation",
  "data_schema": {
    "type": "object",
    "required": [
      "variable_a",
      "variable_b",
      "coefficient"
    ],
    "properties": {
      "variable_a": {
        "type": "string",
        "description": "First variable ID"
      },
      "variable_b": {
        "type": "string",
        "description": "Second variable ID"
      },
      "coefficient": {
        "type": "number",
        "minimum": -1,
        "maximum": 1,
        "description": "Pearson correlation coefficient [-1, 1]"
      },
      "p_value": {
        "type": "number",
        "description": "Statistical significance of the correlation"
      },
      "sample_size": {
        "type": "integer",
        "description": "Number of observations"
      }
    }
  },
  "mechanism": "Structural co-movement between two {{variable}}s without the directed edge that would make it {{causation}}: changes in one accompany changes in the other, but manipulating one does not necessarily alter the other. Characterized by a coefficient in [-1, 1]. The distinction is topological, not a consequence of the cum-hoc-ergo-propter-hoc fallacy \u2014 Correlation is defined by the structural absence of a directed causal edge.",
  "gloss": "Co-movement between variables without directed causal edge \u2014 structurally distinct from Causation",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Correlation#mh:SHA-256:148d5034bf5678b1e5c702109d82ebb76620dbf7e792717e40c3f3ed6698db9c",
  "sema_ref": "Correlation#148d",
  "sema_stub": "148d",
  "dependencies": {
    "references": {
      "variable": "Variable#179a",
      "causation": "Causation#d360"
    }
  }
}
```

---

## Criteria#ef6b

```json
{
  "handle": "Criteria",
  "data_schema": {
    "type": "object",
    "required": [
      "metric",
      "threshold"
    ],
    "properties": {
      "criteria_id": {
        "type": "string",
        "description": "Unique identifier for this criteria"
      },
      "metric": {
        "type": "string",
        "description": "What is being measured (e.g., 'cost', 'latency')"
      },
      "threshold": {
        "description": "The target value or boundary (any type)"
      },
      "comparator": {
        "type": "string",
        "enum": [
          "<",
          "<=",
          "=",
          ">=",
          ">",
          "in",
          "not_in"
        ],
        "description": "How to compare against threshold"
      }
    }
  },
  "mechanism": "The specific standards used to judge the success of an {{artifact}}. e.g., 'must be under $50'. Used by the judgment.",
  "gloss": "Judgment standards",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Criteria#mh:SHA-256:ef6b31198694b637dc1eca8e24c56057b6df0e90fba8f32de8a7c15b747cdbe0",
  "sema_ref": "Criteria#ef6b",
  "sema_stub": "ef6b",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## Critique#4e43

```json
{
  "handle": "Critique",
  "mechanism": "Analyzes a target {{datum}} against specific {{criteria}} and generates a structured {{assessment}}. Unlike judgment (which yields a scalar), Critique produces descriptive, actionable advice.",
  "gloss": "Qualitative feedback generation",
  "failure_modes": [
    "Nitpicking: Focusing on trivial details while missing structural flaws.",
    "Vague Praise: Generic feedback that offers no actionable path.",
    "Projection: Critiquing the artifact for not being what the critic would have built."
  ],
  "invariants": [
    "Feedback must be descriptive, not just scalar.",
    "Must reference specific criteria."
  ],
  "sema_id": "sema:Critique#mh:SHA-256:4e43011af49e8973c5f934ad6ee91ea40254fa1a4f6bff9f6880309ba9affe01",
  "sema_ref": "Critique#4e43",
  "sema_stub": "4e43",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "target",
      "criteria",
      "feedback"
    ],
    "properties": {
      "target": {
        "type": "string",
        "description": "Reference to the artifact being critiqued"
      },
      "criteria": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "The criteria used for evaluation"
      },
      "feedback": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "criterion": {
              "type": "string"
            },
            "observation": {
              "type": "string"
            },
            "suggestion": {
              "type": "string"
            }
          }
        },
        "description": "Structured feedback items"
      },
      "strengths": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Identified positive aspects"
      },
      "weaknesses": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Identified areas for improvement"
      }
    }
  },
  "dependencies": {
    "yields": {
      "assessment": "Assessment#a765"
    },
    "accepts": {
      "criteria": "Criteria#ef6b",
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Cyclic#5d28

```json
{
  "handle": "Cyclic",
  "mechanism": "A {{topology}} that permits feedback {{loop}}s, allowing a process to revisit previous states or refine outputs iteratively. Essential for self-correcting systems and recursive optimization.",
  "gloss": "Recursive or iterative topology",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2,
    "tier": 1
  },
  "invariants": [
    "Recurrence: At least one path exists from a node to itself.",
    "Termination Condition: Must have a defined exit state to prevent infinite loops."
  ],
  "sema_ref": "Cyclic#5d28",
  "sema_id": "sema:Cyclic#mh:SHA-256:5d28b07214cf38b9fb23ff6b2a29ff334ad6a63cca57771ee7ff828fce1047a8",
  "sema_stub": "5d28",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "A cyclic topology \u2014 nodes connected in a closed loop where traversal returns to origin.",
    "properties": {
      "nodes": {
        "type": "array",
        "description": "Ordered node identifiers traversed in the cycle"
      },
      "period": {
        "type": "integer",
        "description": "Cycle length"
      }
    }
  },
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "topology": "Topology#2408"
    }
  }
}
```

---

## DAG#de34

```json
{
  "handle": "DAG",
  "data_schema": {
    "type": "object",
    "required": [
      "nodes",
      "edges",
      "root_id"
    ],
    "properties": {
      "nodes": {
        "type": "array",
        "description": "List of task nodes"
      },
      "edges": {
        "type": "array",
        "description": "Dependency arrows (Task A -> Task B)"
      },
      "root_id": {
        "type": "string",
        "description": "Entry point(s) for execution"
      }
    }
  },
  "mechanism": "A directed acyclic graph {{topology}} that allows branching ({{parallelize}}) and merging, but forbids cycles. It models complex dependency chains where tasks can run concurrently but must respect precedence.",
  "gloss": "Directed acyclic dependency graph",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2,
    "tier": 1
  },
  "invariants": [
    "Acyclicity: No path exists from Node(A) to itself.",
    "Directedness: Edges have a single direction."
  ],
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:DAG#mh:SHA-256:de3473cf4dd8bce4007d37ab2ad02c4c4f86737248e896e477e3a92396e86f27",
  "sema_ref": "DAG#de34",
  "sema_stub": "de34",
  "dependencies": {
    "references": {
      "parallelize": "Parallelize#574d",
      "topology": "Topology#2408"
    }
  }
}
```

---

## Datum#31cf

```json
{
  "handle": "Datum",
  "data_schema": {
    "type": "object",
    "required": [
      "payload",
      "source_id"
    ],
    "properties": {
      "payload": {
        "description": "The raw fact or value (any valid JSON)"
      },
      "source_id": {
        "type": "string",
        "description": "Origin of the datum"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "mechanism": "A single unit of raw, unprocessed fact. Unlike information, it has no attached meaning yet, just existence. Singular of Data.",
  "gloss": "Raw unit of fact",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Datum#mh:SHA-256:31cf815f74eb603adc09807862a9f295e90a97280509e6078c7cb63eff1edd3b",
  "sema_ref": "Datum#31cf",
  "sema_stub": "31cf"
}
```

---

## Event#7e71

```json
{
  "handle": "Event",
  "data_schema": {
    "type": "object",
    "required": [
      "event_id",
      "timestamp",
      "type"
    ],
    "properties": {
      "event_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "type": {
        "type": "string",
        "description": "Event classification"
      },
      "payload": {
        "type": "object",
        "description": "Data associated with the occurrence"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "mechanism": "A discrete occurrence involving a change in {{state}} at a specific point in time. Events are the atomic units of causality and history, distinct from continuous {{stream}}s.",
  "gloss": "Discrete temporal occurrence",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Event#mh:SHA-256:7e714768a058525ab90fde17df7c38c827e4b3ceb771bdcba49586347271a00d",
  "sema_ref": "Event#7e71",
  "sema_stub": "7e71",
  "dependencies": {
    "references": {
      "stream": "Stream#22f3",
      "state": "State#4d58"
    }
  }
}
```

---

## Exception#66c0

```json
{
  "handle": "Exception",
  "data_schema": {
    "type": "object",
    "required": [
      "error_code",
      "message",
      "stack_trace"
    ],
    "properties": {
      "error_code": {
        "type": "string",
        "description": "Standardized failure ID"
      },
      "message": {
        "type": "string",
        "description": "Human-readable description"
      },
      "stack_trace": {
        "type": "array",
        "description": "Execution context at failure"
      },
      "severity": {
        "type": "string",
        "enum": [
          "Fatal",
          "Error",
          "Warning"
        ]
      }
    }
  },
  "mechanism": "A signal indicating that the standard execution flow has encountered a critical anomaly or invalid {{state}}. Must be handled explicitly by a {{circuit_breaker}} or {{fail_closed}} policy to prevent system corruption.",
  "gloss": "Runtime anomaly signal",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Exception#mh:SHA-256:66c0cd924c7793327b03caa75c8362e88765fac077ed1e331920be77fc66e8a6",
  "sema_ref": "Exception#66c0",
  "sema_stub": "66c0",
  "dependencies": {
    "references": {
      "fail_closed": "FailClosed#e6a0",
      "state": "State#4d58",
      "circuit_breaker": "CircuitBreaker#4162"
    }
  }
}
```

---

## FailureTrace#9de1

```json
{
  "handle": "FailureTrace",
  "mechanism": "A structured, verifiable proof that a downstream consumer's rejection of an artifact is grounded in a specific clause of the {{accept_spec}} it was measured against. When a consumer returns a rejection through a Solver's Feedback surface, the rejection must carry a FailureTrace naming the violated clause, citing the evidence, and identifying the evaluator. The upstream Solver uses this trace to distinguish genuine structural feedback from fabricated penalties or hallucinated critique. Trace invalidity (a cited clause that does not exist, evidence that does not match the artifact, or a forged evaluator identity) causes the feedback to be dropped rather than absorbed.",
  "gloss": "Structured proof of which AcceptSpec clause a rejected artifact violated \u2014 the evidence the Receptivity Gate verifies",
  "invariants": [
    "Clause-specific: the trace names exactly one {{accept_spec}} clause per violation, not a generic 'doesn't meet bar'.",
    "Evidence-bound: the violation claim is paired with citeable evidence from the artifact.",
    "Signed: the trace carries the evaluator's cryptographic identity so fabricated traces are detectable."
  ],
  "failure_modes": [
    "Ghost clauses: the trace cites an AcceptSpec clause that does not exist (easy to detect via schema lookup).",
    "Evidence fabrication: the trace cites evidence the artifact does not contain (detectable via content hash).",
    "Identity spoofing: the evaluator signature is invalid (detectable via standard signature verification).",
    "Clause-dancing: the consumer rejects for clause A but the real objection is to clause B they did not invoke \u2014 structural honesty failure that no trace schema can catch by itself."
  ],
  "data_schema": {
    "type": "object",
    "required": [
      "accept_spec_ref",
      "violated_clause",
      "evidence",
      "evaluator_ref"
    ],
    "properties": {
      "accept_spec_ref": {
        "type": "string",
        "description": "sema_id of the AcceptSpec the artifact was measured against"
      },
      "violated_clause": {
        "type": "string",
        "description": "Identifier of the specific clause claimed violated"
      },
      "evidence": {
        "type": "object",
        "description": "Citeable evidence from the artifact supporting the violation claim"
      },
      "evaluator_ref": {
        "type": "string",
        "description": "Signed identity of the evaluator asserting the violation"
      },
      "severity": {
        "type": "string",
        "enum": [
          "blocking",
          "advisory"
        ],
        "description": "Whether the violation halts progress or is informational"
      }
    }
  },
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:FailureTrace#mh:SHA-256:9de1d968b51492278dee438d190924c197f8ac71135f58833cb2700d77c18af8",
  "sema_ref": "FailureTrace#9de1",
  "sema_stub": "9de1",
  "dependencies": {
    "references": {
      "accept_spec": "AcceptSpec#7caa"
    }
  }
}
```

---

## Forest#5eda

```json
{
  "handle": "Forest",
  "mechanism": "A topology consisting of two or more independently-rooted {{tree}}s with no shared apex. Each constituent tree can be traversed standalone; the Forest is the named collection. Distinct from a single tree with many branches: a Forest has *no shared root*, so removing any one tree does not affect the others. Found in random-forest ensembles (ML), disjoint-set forests (union-find CS), process forests (OS sessions), multi-repo organizations (git), federated solver trees across organizations (FI \u00a77.2 Knowledge Sharing), and biological forests (where cross-tree links exist but do not create a shared apex). Variation across descendants concerns whether the trees are strictly disjoint or share substrate (mycorrhizal biology, content-addressed commons) and whether merge/split operations are supported (union-find).",
  "gloss": "Topology of N independently-rooted trees with no shared apex",
  "invariants": [
    "Multiplicity: a Forest contains at least two {{tree}}s; a single tree is not a forest.",
    "Apex-disjoint: no node is an ancestor of any node in a different constituent tree.",
    "Tree-wellformedness: each constituent is itself a valid Tree (rooted, acyclic)."
  ],
  "data_schema": {
    "type": "object",
    "required": [
      "trees"
    ],
    "properties": {
      "trees": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Refs to the constituent Tree instances"
      },
      "cross_links": {
        "type": "array",
        "description": "Optional non-apex edges between trees (e.g., mycorrhizal / federated references)"
      }
    }
  },
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Forest#mh:SHA-256:5edadf227842037c92d42f320a62bd2393f7020ab92ca54e82566bdb8ba9b9bd",
  "sema_ref": "Forest#5eda",
  "sema_stub": "5eda",
  "dependencies": {
    "references": {
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## Goal#009e

```json
{
  "handle": "Goal",
  "mechanism": "A specification of a desired end state. It defines the target that {{work}} aims to achieve and that evaluation measures against. A Goal is testable: given a {{result}}, one can determine if the Goal is satisfied. Goals can be composed (AND/OR) and prioritized.",
  "gloss": "Specification of desired end state",
  "failure_modes": [
    "Goal Ambiguity: Goal admits multiple incompatible interpretations.",
    "Goal Conflict: Multiple goals cannot all be satisfied simultaneously.",
    "Moving Target: Goal changes during execution without proper signaling."
  ],
  "invariants": [
    "Testability: Given a Result, Goal satisfaction must be decidable.",
    "Stability: Goal should not change during a single execution cycle."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "tier": 1,
    "ring": 0
  },
  "sema_id": "sema:Goal#mh:SHA-256:009e138976905d1547fed802752f06e07deab5ab7aec6a3795c4017f4c706848",
  "sema_ref": "Goal#009e",
  "sema_stub": "009e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "goal_statement",
      "success_criteria"
    ],
    "properties": {
      "goal_statement": {
        "type": "string",
        "description": "The desired end state"
      },
      "success_criteria": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Binary conditions that define completion"
      },
      "priority": {
        "type": "integer",
        "minimum": 0,
        "maximum": 100
      },
      "metric_target": {
        "type": "object",
        "properties": {
          "metric_name": {
            "type": "string"
          },
          "target_value": {
            "type": "number"
          },
          "comparator": {
            "type": "string",
            "enum": [
              ">",
              "<",
              ">=",
              "<=",
              "="
            ]
          }
        }
      }
    }
  },
  "dependencies": {
    "references": {
      "work": "Work#d2c6",
      "result": "Result#195b"
    }
  }
}
```

---

## Hierarchy#d530

```json
{
  "handle": "Hierarchy",
  "data_schema": {
    "type": "object",
    "required": [
      "levels",
      "relationships"
    ],
    "properties": {
      "levels": {
        "type": "array",
        "description": "Ordered ranks (Top -> Bottom)"
      },
      "relationships": {
        "type": "object",
        "description": "Parent-Child map"
      },
      "root_id": {
        "type": "string",
        "description": "Apex node"
      }
    }
  },
  "mechanism": "The vertical ranking of {{category}}s or objects. Defines Upper vs. Lower relationships, inheritance, and authority.",
  "gloss": "Vertical rank ordering with Upper/Lower relations, inheritance, and authority",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Hierarchy#mh:SHA-256:d5301ba0587b73443b7408885a85fd530d1609add96c1250138e062d18a565cb",
  "sema_ref": "Hierarchy#d530",
  "sema_stub": "d530",
  "dependencies": {
    "references": {
      "category": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1"
    }
  }
}
```

---

## Hypothesis#ffa7

```json
{
  "handle": "Hypothesis",
  "data_schema": {
    "type": "object",
    "required": [
      "proposition",
      "confidence"
    ],
    "properties": {
      "proposition": {
        "type": "string",
        "description": "The tentative explanation"
      },
      "confidence": {
        "type": "number",
        "description": "Initial probability estimate (0-1)"
      },
      "status": {
        "type": "string",
        "enum": [
          "Open",
          "Proven",
          "Falsified"
        ]
      }
    }
  },
  "mechanism": "A testable prediction staged for falsification attempts. Distinct from a Claim (asserted as true), an Assumption (held provisionally to make progress), and an Axiom (accepted without proof): a Hypothesis carries an explicit commitment to be checked against evidence and updated or discarded accordingly.",
  "gloss": "Testable prediction staged for falsification attempts \u2014 provisional, not asserted",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Hypothesis#mh:SHA-256:ffa724a18ea59f5a3bde93aef6536203e472268db7ecb2f6135577d5b4303e6c",
  "sema_ref": "Hypothesis#ffa7",
  "sema_stub": "ffa7"
}
```

---

## Identity#626c

```json
{
  "handle": "Identity",
  "data_schema": {
    "type": "object",
    "required": [
      "public_key",
      "claims"
    ],
    "properties": {
      "public_key": {
        "type": "string",
        "description": "Cryptographic identifier (DID/Key)"
      },
      "claims": {
        "type": "object",
        "description": "Verifiable credentials or attributes"
      },
      "history_hash": {
        "type": "string",
        "description": "Pointer to interaction log"
      }
    }
  },
  "mechanism": "The unique distinguishing context of an agent, including its history, reputation, and public keys. Distinguishes 'Self' from 'Other'. Unlike {{nature}} (what you are) or Role (what you do), Identity is the persistent handle that tracks an entity across interactions.",
  "gloss": "Unique agent context (The Who)",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Identity#mh:SHA-256:626c6180c1969117e0375625c31d4e39b77e6330d3a197dc7099acf85d1d57b3",
  "sema_ref": "Identity#626c",
  "sema_stub": "626c",
  "dependencies": {
    "references": {
      "nature": "Nature#6c1a"
    }
  }
}
```

---

## Ledger#b5fe

```json
{
  "handle": "Ledger",
  "mechanism": "An immutable record of {{value}} transfers, debts, and obligations between {{agent}}s. It serves as the shared memory for economic coordination.",
  "gloss": "Immutable transactional history",
  "invariants": [
    "Immutability: Past entries cannot be modified.",
    "Append-Only: New transactions are added to the end."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_id": "sema:Ledger#mh:SHA-256:b5feb674fa403526c50d598b3d331e46aa9f5876b99ca05ab86187ecd7681c52",
  "sema_ref": "Ledger#b5fe",
  "sema_stub": "b5fe",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "ledger_id",
      "entries"
    ],
    "properties": {
      "ledger_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "entries": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "from_agent": {
              "type": "string"
            },
            "to_agent": {
              "type": "string"
            },
            "amount": {
              "type": "number"
            },
            "timestamp": {
              "type": "string",
              "format": "date-time"
            }
          }
        },
        "description": "Immutable transaction history"
      },
      "balance_snapshot": {
        "type": "object",
        "description": "Current balances per agent"
      }
    }
  },
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## MECE#8cb0

```json
{
  "handle": "MECE",
  "data_schema": {
    "type": "object",
    "required": [
      "root_set",
      "subsets"
    ],
    "properties": {
      "root_set": {
        "type": "string",
        "description": "The universe being partitioned"
      },
      "subsets": {
        "type": "array",
        "description": "The mutually exclusive categories"
      },
      "completeness_proof": {
        "type": "string",
        "description": "Logic ensuring exhaustiveness"
      }
    }
  },
  "mechanism": "Exhaustive Partition: Divide problem space into categories that are Mutually Exclusive (no overlap) and Collectively Exhaustive (no gaps). Test: Can any item belong to two categories? Is any item uncategorized? Refine until both tests pass.",
  "gloss": "Mutually Exclusive, Collectively Exhaustive partitioning",
  "failure_modes": [
    "The Other Bucket Trap: 'Misc' category exceeds threshold.",
    "Dimensional Error: Partitioning criteria mixed (e.g., Color vs Origin).",
    "False Exclusivity: Edge cases ignored to force fit."
  ],
  "invariants": [
    "Exclusivity: Intersection(Subset_i, Subset_j) == NULL",
    "Exhaustiveness: Union(Subsets) == UniversalSet"
  ],
  "parameters": [
    {
      "name": "max_depth",
      "type": "Int",
      "range": "[1, 10]",
      "description": "How deep the tree can go"
    },
    {
      "name": "misc_tolerance",
      "type": "Float",
      "range": "[0.0, 0.1]",
      "description": "Max % of items allowed in 'Other'"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "related": [
      "Decompose#f900"
    ],
    "ring": 2
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:MECE#mh:SHA-256:8cb062d51bcfd89368c58a5e6247e2070596f01be8e03382dd19a0c61abe8c1b",
  "sema_ref": "MECE#8cb0",
  "sema_stub": "8cb0"
}
```

---

## MechanisticDesignProposal#497e

```json
{
  "handle": "MechanisticDesignProposal",
  "mechanism": "A structured blueprint for a systemic {{solution}} that addresses a {{problem}} in a {{system}}. It goes beyond a standard proposal by requiring the definition of a core mechanism\u2014the specific leverage point and causal chain used to alter system behavior. The proposal integrates the 'Why it Works' (defense) and 'Why it Fails' (attack) dialectic, assessing attached {{risk}}s, along with medium-term implementation and long-term vision projections.",
  "gloss": "Dialectic blueprint of a system mechanism with temporal projections",
  "invariants": [
    "Dialectic Balance: 'why_it_fails' must be as detailed as 'why_it_works'.",
    "Causal Clarity: Must define the mechanism of action (how A causes B).",
    "Novelty Requirement: 'what_is_new' must identify the unique contribution.",
    "Temporal Completeness: Must include both medium_term and long_term_vision."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "label",
      "design_principles",
      "core_mechanism",
      "how_it_works",
      "what_is_new",
      "why_it_works",
      "why_it_fails",
      "medium_term",
      "long_term_vision"
    ],
    "properties": {
      "label": {
        "type": "string",
        "description": "A concise, evocative name for the solution (e.g., 'Parametric Storm-Trigger Retirement')"
      },
      "design_principles": {
        "type": "string",
        "description": "The guiding philosophy behind the design. What mental model or heuristic drives this solution?"
      },
      "core_mechanism": {
        "type": "string",
        "description": "The specific leverage point and causal chain. What is the ONE thing that makes this work?"
      },
      "how_it_works": {
        "type": "string",
        "description": "Concrete operational description. Step-by-step: what happens when this is deployed?"
      },
      "what_is_new": {
        "type": "string",
        "description": "The novel contribution. What does this do that existing solutions cannot? Why hasn't this been done before?"
      },
      "why_it_works": {
        "type": "string",
        "description": "The dialectic defense. Steel-man argument for why this mechanism will succeed."
      },
      "why_it_fails": {
        "type": "string",
        "description": "The dialectic attack. Pre-mortem: what are the failure modes, risks, and unintended consequences?"
      },
      "medium_term": {
        "type": "string",
        "description": "Implementation trajectory for 1-3 years. What does adoption look like? What ecosystem changes occur?"
      },
      "long_term_vision": {
        "type": "string",
        "description": "The end-state aspiration. If this succeeds fully, what does the world look like in 10+ years?"
      }
    }
  },
  "sema_ref": "MechanisticDesignProposal#497e",
  "sema_id": "sema:MechanisticDesignProposal#mh:SHA-256:497e86893969548b87d441839a2aecd79437007ed1294ac1af1c145b8567282d",
  "sema_stub": "497e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "risk": "Risk#1980"
    },
    "yields": {
      "solution": "Solution#fcea"
    },
    "accepts": {
      "problem": "Problem#4576",
      "system": "System#e314"
    }
  }
}
```

---

## Message#f767

```json
{
  "handle": "Message",
  "data_schema": {
    "type": "object",
    "required": [
      "header",
      "body"
    ],
    "properties": {
      "header": {
        "type": "object",
        "properties": {
          "sender": {
            "type": "string"
          },
          "recipient": {
            "type": "string"
          },
          "timestamp": {
            "type": "string"
          }
        }
      },
      "body": {
        "description": "The content payload"
      },
      "signature": {
        "type": "string",
        "description": "Sender verification"
      }
    }
  },
  "mechanism": "A structured container for a {{signal}}, adding Metadata (Sender, Recipient, Timestamp) to the raw emission.",
  "gloss": "Structured signal container",
  "invariants": [
    "Immutability: Once sent, the message content cannot be changed.",
    "Addressability: Must contain Sender and (optional) Recipient identifiers."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Message#mh:SHA-256:f7678d6d403b174dec233b366b6f352da445c31ab2577c7314dd0b1d52161d7f",
  "sema_ref": "Message#f767",
  "sema_stub": "f767",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Meta#90f4

```json
{
  "handle": "Meta",
  "data_schema": {
    "type": "object",
    "required": [
      "level",
      "target"
    ],
    "properties": {
      "level": {
        "type": "integer",
        "minimum": 1,
        "description": "Abstraction level (1 = meta, 2 = meta-meta, etc.)"
      },
      "target": {
        "type": "string",
        "description": "ID or type of the entity being abstracted over"
      },
      "description": {
        "type": "string",
        "description": "What aspect is being meta-analyzed"
      }
    }
  },
  "mechanism": "A higher-order modifier indicating self-reference or abstraction (Thinking about Thinking).",
  "gloss": "Higher-order abstraction",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Meta#mh:SHA-256:90f452433c8b16a65d5842745b4cbb586957b1f45becbfca2322fece945ad3ee",
  "sema_ref": "Meta#90f4",
  "sema_stub": "90f4",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Metric#17fd

```json
{
  "handle": "Metric",
  "data_schema": {
    "type": "object",
    "required": [
      "name",
      "value",
      "unit",
      "timestamp"
    ],
    "properties": {
      "name": {
        "type": "string"
      },
      "value": {
        "type": "number"
      },
      "unit": {
        "type": "string"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      },
      "dimensions": {
        "type": "object",
        "description": "Tags for filtering (e.g., {region: 'us-east', service: 'db'})"
      },
      "resolution": {
        "type": "string",
        "description": "Sampling interval (e.g., '1s', '1m')"
      }
    }
  },
  "mechanism": "A definable, quantifiable measure of a specific property within a {{system}} or {{state}}. It provides the signal for optimization and monitoring.",
  "gloss": "Quantifiable measurement of a property, timestamped and optionally dimensioned",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_id": "sema:Metric#mh:SHA-256:17fda0aa76055cb25425b9b1db1b48510c630d3ed7fde62fc8e8d6702e8a9db9",
  "sema_ref": "Metric#17fd",
  "sema_stub": "17fd",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314"
    }
  }
}
```

---

## Mode#0e74

```json
{
  "handle": "Mode",
  "data_schema": {
    "type": "object",
    "required": [
      "mode_id",
      "constraints"
    ],
    "properties": {
      "mode_id": {
        "type": "string",
        "description": "Unique identifier for this mode configuration"
      },
      "constraints": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Rules governing behavior in this mode"
      },
      "priors": {
        "type": "object",
        "description": "Default assumptions active in this mode"
      },
      "active": {
        "type": "boolean",
        "description": "Whether this mode is currently engaged"
      }
    }
  },
  "mechanism": "A primitive representing a distinct 'Stance' or 'Configuration of Agency'. Unlike {{state}} (which changes frequently), a Mode is a stable set of constraints and priors that governs how an agent processes information (e.g., Exploration Mode vs. Exploitation Mode).",
  "gloss": "A discrete configuration of agency",
  "failure_modes": [
    "Mode Persistence Failure: {{agent}} fails to maintain the mode constraints over time.",
    "Mode Confusion: {{agent}} mixes behaviors from conflicting modes."
  ],
  "invariants": [
    "Stability: A Mode persists until an explicit {{transition}} event.",
    "Exclusivity: {{agent}} cannot be in two conflicting Modes simultaneously (unless explicitly designed as Hybrid)."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "related": [
      "WorkerMode#b5c4",
      "SynergisticMode#b45f"
    ]
  },
  "sema_id": "sema:Mode#mh:SHA-256:0e74d67e79d305d801347b14b889ae026212597df93baefbef789c173db395c5",
  "sema_ref": "Mode#0e74",
  "sema_stub": "0e74",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "state": "State#4d58",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Nature#6c1a

```json
{
  "handle": "Nature",
  "data_schema": {
    "type": "object",
    "required": [
      "classification"
    ],
    "properties": {
      "classification": {
        "type": "string",
        "enum": [
          "Biological",
          "Synthetic",
          "Institutional",
          "Hybrid"
        ],
        "description": "Substrate type"
      },
      "substrate": {
        "type": "string",
        "description": "More specific substrate details"
      },
      "immutable": {
        "type": "boolean",
        "default": true,
        "description": "Whether this nature can change"
      }
    }
  },
  "mechanism": "The substrate classification of an entity (e.g. Biological, Synthetic, or Institutional). It serves as the immutable input for downstream {{protocol}}s to determine alignment obligations, rights, and authentication requirements.",
  "gloss": "Ontological origin classification",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Nature#mh:SHA-256:6c1a88dcf3f53f945e8fa9a4c8a04b8e23819954de102cd266c999447c12314b",
  "sema_ref": "Nature#6c1a",
  "sema_stub": "6c1a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## Option#483e

```json
{
  "handle": "Option",
  "data_schema": {
    "type": "object",
    "required": [
      "option_id",
      "description",
      "predicted_outcome"
    ],
    "properties": {
      "option_id": {
        "type": "string"
      },
      "description": {
        "type": "string"
      },
      "cost_estimate": {
        "type": "number"
      },
      "risk_score": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
      },
      "predicted_outcome": {
        "type": "string",
        "description": "Simulation result if this option is chosen"
      }
    }
  },
  "mechanism": "A discrete, actionable alternative within a decision space. An Option must be fully specified (executable) and mutually exclusive from other options in the same set. It represents a valid path for state transition.",
  "gloss": "A discrete, executable alternative",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Option#mh:SHA-256:483eebf0a4fdc817585be429278bf1c8c56b815249bbf91501073dce1453cf13",
  "sema_ref": "Option#483e",
  "sema_stub": "483e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Outcome#144c

```json
{
  "handle": "Outcome",
  "data_schema": {
    "type": "object",
    "required": [
      "outcome_id",
      "value"
    ],
    "properties": {
      "outcome_id": {
        "type": "string",
        "description": "Unique identifier for this outcome"
      },
      "value": {
        "description": "The actual result achieved"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "When the outcome was realized"
      },
      "deviation": {
        "type": "object",
        "description": "Difference between actual and expected (if applicable)"
      }
    }
  },
  "mechanism": "The actual result that occurs in reality. It may differ from the {{plan}} due to external factors, noise, or execution error.",
  "gloss": "Realized state after an action, captured for Plan-vs-reality comparison",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Outcome#mh:SHA-256:144c45a1a8eb6709b80025867c72c8430f0b3d0dab600c571f2a12a9280d0dc2",
  "sema_ref": "Outcome#144c",
  "sema_stub": "144c",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d"
    }
  }
}
```

---

## Overlap#b462

```json
{
  "handle": "Overlap",
  "data_schema": {
    "type": "object",
    "required": [
      "set_a",
      "set_b"
    ],
    "properties": {
      "set_a": {
        "type": "array",
        "description": "First accept-set (outcome IDs)"
      },
      "set_b": {
        "type": "array",
        "description": "Second accept-set (outcome IDs)"
      },
      "intersection": {
        "type": "array",
        "description": "Common elements between sets"
      },
      "expansion_count": {
        "type": "integer",
        "description": "How many times sets were expanded to find overlap"
      }
    }
  },
  "mechanism": "Before stating positions, each agent declares their ACCEPT-SET: all outcomes they can live with. Sets are hash-committed before reveal (commit-reveal protocol). Compute intersection. If non-empty, select from intersection. If empty, both agents EXPAND accept-sets by one step and recompute. Repeat until overlap found or expansion-limit hit. It employs {{mece}} partitioning to cleanly identify the intersection of distinct accept-sets.",
  "gloss": "Accept-set intersection protocol with commit-reveal for interest-based negotiation",
  "failure_modes": [
    "Strategic minimal accept-sets (mitigated but not eliminated by commit-reveal).",
    "Expansion limit hit with no overlap.",
    "Accept-sets too abstract to intersect meaningfully.",
    "Requires both agents to support commit-reveal protocol."
  ],
  "invariants": [
    "Private regions respected",
    "Shared region contains agreed facts"
  ],
  "preconditions": [
    "Two ontologies/datasets"
  ],
  "postconditions": [
    "Intersection identified"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_id": "sema:Overlap#mh:SHA-256:b462648204bcf1076f89ccda750a6ed2427ab85c74602d24fcbf30aadf5c6e36",
  "sema_ref": "Overlap#b462",
  "sema_stub": "b462",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "mece": "MECE#8cb0"
    }
  }
}
```

---

## Parallel#3181

```json
{
  "handle": "Parallel",
  "mechanism": "Concurrent execution: A and B simultaneously. No ordering guarantee.",
  "gloss": "Concurrent flow",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Parallel#mh:SHA-256:318115c507a765d08bb292f74162bb6427f0756b031b2f516b089f6dbf61a753",
  "sema_ref": "Parallel#3181",
  "sema_stub": "3181",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "A parallel topology \u2014 independent branches executed concurrently with a join point.",
    "properties": {
      "branches": {
        "type": "array",
        "description": "Independent execution branches"
      },
      "join_semantics": {
        "type": "string",
        "enum": [
          "all",
          "any",
          "quorum"
        ],
        "description": "How branch results combine"
      }
    }
  }
}
```

---

## PerformanceSignal#d96f

```json
{
  "handle": "PerformanceSignal",
  "mechanism": "The typed artifact emitted by a Solver's Feedback surface \u2014 the downstream evaluation of how a completed transaction performed against its acceptance criteria, or the escalation signal that invokes a {{frame_error}} when failure is structural rather than local. Distinct from the general {{feedback}} primitive: PerformanceSignal is the contract-typed output that feeds {{pathway_memory}} (quality, depth, cost across problem classes) and drives localized learning at each node. The signal is produced by the consumer of a Result (parent Solver or end-caller) after the Acceptance Gate either admitted the Result as a Solution or rejected it back for reframing.",
  "gloss": "Typed artifact emitted by a Solver's Feedback surface \u2014 downstream evaluation that feeds Pathway Memory",
  "invariants": [
    "Typed: the signal conforms to a declared schema so {{pathway_memory}} can aggregate across instances.",
    "Attributable: names the Solver node that produced the evaluated Result, so learning is localized.",
    "Three-outcome: either a scored evaluation, a pass/accept confirmation, or a {{frame_error}} escalation."
  ],
  "failure_modes": [
    "Sycophantic drift: evaluator shares the generator's blind spots and rubber-stamps weak outputs.",
    "Signal poisoning in open commons: an untrusted consumer fabricates penalties to steal work (mitigated by the Receptivity Gate in \u00a77).",
    "Latency decay: the signal arrives long after the node has moved on, weakening the learning loop.",
    "Grade inflation: evaluators converge on 'good enough' scoring so all signals compress into a narrow band."
  ],
  "data_schema": {
    "type": "object",
    "required": [
      "solver_ref",
      "outcome"
    ],
    "properties": {
      "solver_ref": {
        "type": "string",
        "description": "sema_id of the Solver node being evaluated"
      },
      "outcome": {
        "type": "string",
        "enum": [
          "accepted",
          "scored",
          "frame_error"
        ],
        "description": "Shape of the signal"
      },
      "score": {
        "type": "number",
        "description": "Optional quality score when outcome=scored"
      },
      "frame_error_ref": {
        "type": "string",
        "description": "sema_id of the FrameError when outcome=frame_error"
      },
      "evaluator_ref": {
        "type": "string",
        "description": "Identity of the evaluating entity, for trust-weighted aggregation"
      }
    }
  },
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:PerformanceSignal#mh:SHA-256:d96f75b1618e762562ef6f0bc52586e095e50ea6b9f184d0a7d349374269627f",
  "sema_ref": "PerformanceSignal#d96f",
  "sema_stub": "d96f",
  "dependencies": {
    "references": {
      "pathway_memory": "PathwayMemory#0799",
      "feedback": "Feedback#b477",
      "frame_error": "FrameError#168f"
    }
  }
}
```

---

## Permission#354b

```json
{
  "handle": "Permission",
  "data_schema": {
    "type": "object",
    "required": [
      "permission_id",
      "agent_id",
      "action"
    ],
    "properties": {
      "permission_id": {
        "type": "string",
        "description": "Unique identifier for this permission"
      },
      "agent_id": {
        "type": "string",
        "description": "Who is granted permission"
      },
      "action": {
        "type": "string",
        "description": "What action is permitted"
      },
      "resource": {
        "type": "string",
        "description": "What artifact can be accessed"
      },
      "granted_at": {
        "type": "string",
        "format": "date-time",
        "description": "When permission was granted"
      }
    }
  },
  "mechanism": "An authorization grant allowing an {{agent}} to perform a specific {{act}} or access a {{artifact}}. The atomic unit of access control.",
  "gloss": "Authorization grant",
  "failure_modes": [
    "Privilege escalation: agent acquires permission beyond intended scope.",
    "Stale grant: permission remains active after it should have expired."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1,
    "caution": "Authorization boundary \u2014 misconfigured grants enable unauthorized action."
  },
  "sema_ref": "Permission#354b",
  "sema_id": "sema:Permission#mh:SHA-256:354bbc2a1ffe0abbf2da56daf3e803932aec5b3a1e88c2ade476a4fe8486204c",
  "sema_stub": "354b",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "agent": "Agent#35b9",
      "act": "Act#5d55"
    }
  }
}
```

---

## Plan#fd6d

```json
{
  "handle": "Plan",
  "gloss": "An ordered sequence of steps to achieve a goal",
  "mechanism": "An {{artifact}} containing a structured {{sequence}} of {{step}}s designed to transition a {{system}} from a current {{state}} to a target {{goal}}. Unlike a simple list, a Plan enforces causal dependency between steps and resource allocation, and tracks the attached {{risk}}s that may derail it.",
  "signature": [
    "Artifact#6254(Step#5f22)"
  ],
  "data_schema": {
    "type": "object",
    "required": [
      "plan_id",
      "steps",
      "status"
    ],
    "properties": {
      "plan_id": {
        "type": "string"
      },
      "goal_ref": {
        "type": "string",
        "description": "Pointer to the Goal this plan serves"
      },
      "steps": {
        "type": "array",
        "items": {
          "type": "object"
        },
        "description": "Ordered sequence of Steps"
      },
      "status": {
        "type": "string",
        "enum": [
          "Draft",
          "Approved",
          "In_Progress",
          "Done"
        ]
      },
      "estimated_cost": {
        "type": "object",
        "description": "Total resource budget required"
      },
      "created_at": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "invariants": [
    "Ordering: Steps must be causally sortable.",
    "Termination: Plan must have a defined end state."
  ],
  "_meta": {
    "tier": 0,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_ref": "Plan#fd6d",
  "sema_id": "sema:Plan#mh:SHA-256:fd6d94d1c4252ca04d04c3cac5ef00569523959ff267e945c271a3ab5acf763e",
  "sema_stub": "fd6d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "sequence": "Sequence#b0b8",
      "goal": "Goal#009e",
      "system": "System#e314",
      "risk": "Risk#1980",
      "artifact": "Artifact#6254",
      "step": "Step#5f22"
    }
  }
}
```

---

## Probability#356b

```json
{
  "handle": "Probability",
  "mechanism": "A measure of likelihood on [0,1] expressing the degree of belief or frequency with which an {{event}} is expected to occur. Forms the basis for risk assessment, decision-making under uncertainty, and Bayesian updating.",
  "gloss": "Likelihood measure for uncertain events",
  "invariants": [
    "Bounded: 0 \u2264 P \u2264 1",
    "Normalization: P(certain) = 1, P(impossible) = 0",
    "Additivity: P(A or B) = P(A) + P(B) for mutually exclusive events"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Probability value between 0 and 1"
  },
  "sema_ref": "Probability#356b",
  "sema_id": "sema:Probability#mh:SHA-256:356bf7e4b6ca99e4fe7705cb088c3f1cd3a5919334a772e00dc829065c71dffd",
  "sema_stub": "356b",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "event": "Event#7e71"
    }
  }
}
```

---

## Problem#4576

```json
{
  "handle": "Problem",
  "mechanism": "A formal representation of a gap between Current {{state}} and Desired {{state}} where the Cost of Inaction > 0. Unlike a {{task}} (which is a directive to act), a Problem is a descriptive claim about value loss. It serves as the input to interpretation and reframing, requiring diagnosis before a solution root can be established.",
  "gloss": "A state gap with a cost of inaction",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "current_state",
      "desired_state"
    ],
    "properties": {
      "current_state": {
        "type": "string",
        "description": "Description of reality"
      },
      "desired_state": {
        "type": "string",
        "description": "Description of goal"
      },
      "gap_analysis": {
        "type": "string",
        "description": "Why the current != desired"
      },
      "severity": {
        "type": "string",
        "enum": [
          "Low",
          "Medium",
          "High",
          "Existential"
        ]
      },
      "root_cause_hypothesis": {
        "type": "string"
      }
    }
  },
  "sema_id": "sema:Problem#mh:SHA-256:45763815b7a71eead1dea72220b26a41051c346d456618ebc32711031b30b1bc",
  "sema_ref": "Problem#4576",
  "sema_stub": "4576",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "state": "State#4d58"
    }
  }
}
```

---

## ProblemSpace#9e74

```json
{
  "handle": "ProblemSpace",
  "mechanism": "A defined region of the problem landscape, bounded by {{constraint}}s and initial {{state}}. It represents the domain within which a solver must operate to find a valid {{solution}}.",
  "gloss": "Bounded domain of a problem",
  "invariants": [
    "Boundedness: Must have defined constraints.",
    "Consistency: The space must not contain contradictory definitions."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "boundaries",
      "variables"
    ],
    "properties": {
      "domain": {
        "type": "string"
      },
      "boundaries": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Hard constraints (e.g. Physics, Law)"
      },
      "variables": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Degrees of freedom available to change"
      },
      "constants": {
        "type": "object",
        "description": "Immutable facts"
      }
    }
  },
  "sema_ref": "ProblemSpace#9e74",
  "sema_id": "sema:ProblemSpace#mh:SHA-256:9e74649bb48cbb13838757ad6ba7c5d4894487fd3ced55c110283480b66cbd9c",
  "sema_stub": "9e74",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solution": "Solution#fcea",
      "state": "State#4d58"
    }
  }
}
```

---

## Prompt#b18a

```json
{
  "handle": "Prompt",
  "mechanism": "Structured input-instruction submitted to a generative model. May carry a role tag (system, user, assistant) and optional tool-declaration attachments that shape how the model generates. Distinct from a Message (agent-to-agent communication with sender/recipient metadata) and from a raw Signal (no envelope).",
  "gloss": "Structured instruction to a generative model, optionally role-tagged",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string"
      },
      "role": {
        "type": "string"
      }
    },
    "required": [
      "text"
    ]
  },
  "sema_id": "sema:Prompt#mh:SHA-256:b18ab0584687fc34da5cae296e8fc8c2b833f215d2f7add7d36a5a05fd5f59c1",
  "sema_ref": "Prompt#b18a",
  "sema_stub": "b18a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Proposal#4840

```json
{
  "handle": "Proposal",
  "data_schema": {
    "type": "object",
    "required": [
      "proposal_id",
      "action",
      "justification"
    ],
    "properties": {
      "proposal_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "action": {
        "type": "string",
        "description": "The proposed action or transition"
      },
      "justification": {
        "type": "string",
        "description": "Why this action should be taken"
      },
      "proposer_id": {
        "type": "string",
        "description": "Who submitted the proposal"
      }
    }
  },
  "mechanism": "A formal {{message}} suggesting a specific {{act}} or {{transition}}. It serves as the input payload for decision-making processes, encapsulating the 'What' and 'Why' of a requested change.",
  "gloss": "A suggested course of action",
  "invariants": [
    "Clarity: The proposed action must be unambiguous."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_ref": "Proposal#4840",
  "sema_id": "sema:Proposal#mh:SHA-256:48400f03d012e37914685f66064ccd4c3875efb0bb4dff24d88c8f1ca9aa247d",
  "sema_stub": "4840",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "act": "Act#5d55"
    },
    "composes_with": {
      "message": "Message#f767"
    }
  }
}
```

---

## Protocol#7e1c

```json
{
  "handle": "Protocol",
  "data_schema": {
    "type": "object",
    "required": [
      "protocol_id",
      "version",
      "rules"
    ],
    "properties": {
      "protocol_id": {
        "type": "string",
        "description": "Unique protocol identifier"
      },
      "version": {
        "type": "string",
        "description": "Semantic version (e.g., '1.0.0')"
      },
      "rules": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of rules defining the protocol"
      },
      "formats": {
        "type": "object",
        "description": "Message format specifications"
      }
    }
  },
  "mechanism": "A defined set of rules and formats for communication between agents.",
  "gloss": "Communication standard",
  "failure_modes": [
    "Version Drift: Agents attempting to communicate with incompatible protocol versions.",
    "Ambiguous Spec: Rules that allow for multiple valid interpretations."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Protocol#mh:SHA-256:7e1cc426d8550edc0ee84d4e4fd7b7dc3aecdfad496dc3e2cc636c36a7f4389e",
  "sema_ref": "Protocol#7e1c",
  "sema_stub": "7e1c",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Prototype#ff18

```json
{
  "handle": "Prototype",
  "data_schema": {
    "type": "object",
    "required": [
      "prototype_id",
      "fidelity"
    ],
    "properties": {
      "prototype_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "fidelity": {
        "type": "string",
        "enum": [
          "low",
          "medium",
          "high"
        ],
        "description": "How close to final product"
      },
      "artifact": {
        "description": "The prototype content or reference"
      },
      "learnings": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "What was learned from this prototype"
      }
    }
  },
  "mechanism": "An early sample, model, or release of a product built to test a concept or process or to act as a thing to be learned from. It is generally low-fidelity and disposable.",
  "gloss": "Testable early model",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1
  },
  "sema_id": "sema:Prototype#mh:SHA-256:ff187305136dd60765caedabd5eefbc62c94b20909c4886f4baef3c9523e83c7",
  "sema_ref": "Prototype#ff18",
  "sema_stub": "ff18",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Queue#65e4

```json
{
  "handle": "Queue",
  "mechanism": "A linear container holding {{task}}s or {{message}}s under an explicit ordering discipline (FIFO, LIFO, or Priority). Consumers dequeue one element at a time; producers enqueue at the discipline-dictated position. Distinct from a {{stream}} (continuous, unbounded, with no single consumer) and from a plain list (no consumer semantics).",
  "gloss": "Ordered container with FIFO/LIFO/priority discipline and explicit dequeue semantics",
  "sema_id": "sema:Queue#mh:SHA-256:65e4154da8cc51144e2f4697060224336e017f0debc205c5abfff3770e35f5ad",
  "sema_ref": "Queue#65e4",
  "sema_stub": "65e4",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "queue_id",
      "items",
      "policy"
    ],
    "properties": {
      "queue_id": {
        "type": "string"
      },
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "description": "Enqueued Task or Message objects"
        }
      },
      "policy": {
        "type": "string",
        "enum": [
          "FIFO",
          "LIFO",
          "Priority"
        ],
        "default": "FIFO"
      },
      "capacity": {
        "type": "integer"
      },
      "metrics": {
        "type": "object",
        "properties": {
          "depth": {
            "type": "integer"
          },
          "average_wait_time": {
            "type": "number"
          }
        }
      }
    }
  },
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "stream": "Stream#22f3",
      "message": "Message#f767"
    }
  }
}
```

---

## Resource#a578

```json
{
  "handle": "Resource",
  "mechanism": "A finite, identifiable entity that can be allocated, consumed, or locked. Resources have {{identity}}, may be renewable or exhaustible, and are subject to contention when demand exceeds supply. Forms the basis for {{budget}} allocation and mutex coordination.",
  "gloss": "Finite allocatable entity",
  "invariants": [
    "Conservation: Resources cannot be created from nothing within a closed system",
    "Identity: Each resource instance has a unique handle"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "resource_id",
      "type",
      "owner_id"
    ],
    "properties": {
      "resource_id": {
        "type": "string",
        "description": "Unique asset ID"
      },
      "type": {
        "type": "string",
        "enum": [
          "Compute",
          "Storage",
          "Bandwidth",
          "Token"
        ]
      },
      "quantity": {
        "type": "number"
      },
      "unit": {
        "type": "string"
      },
      "owner_id": {
        "type": "string",
        "description": "Current holder/owner"
      },
      "lock_state": {
        "type": "object",
        "properties": {
          "locked": {
            "type": "boolean"
          },
          "locked_until": {
            "type": "string",
            "format": "date-time"
          },
          "holder_id": {
            "type": "string"
          }
        }
      }
    }
  },
  "sema_ref": "Resource#a578",
  "sema_id": "sema:Resource#mh:SHA-256:a578cda067d1c6b52f96aab667c3f85a6e5233118774b55200a8acde35d62acf",
  "sema_stub": "a578",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Result#195b

```json
{
  "handle": "Result",
  "mechanism": "The canonical output of an operation (often a {{solution}}). It encapsulates success/failure status, the artifact produced, and associated {{metric}}s such as time taken, resources consumed, and confidence score. It serves as the bridge between execution and evaluation.",
  "gloss": "The output of agentic transformation",
  "failure_modes": [
    "Partial Result: Output is incomplete but presented as complete.",
    "Hallucinated Result: Output claims to solve the task but doesn't.",
    "Unvalidated Result: Result bypasses checking."
  ],
  "invariants": [
    "Provenance: Every Result must trace to the Task and Solver that produced it.",
    "Immutability: Once yielded, a Result cannot be modified (only superseded).",
    "Measurability: Resource consumption must be recorded."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "tier": 1,
    "ring": 0
  },
  "sema_id": "sema:Result#mh:SHA-256:195b5acbf28190f1168318c8ddcd210da4e52365347497d86a2e4d154d17d9f3",
  "sema_ref": "Result#195b",
  "sema_stub": "195b",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "status",
      "stop_reason"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": [
          "Success",
          "Partial",
          "Failure"
        ]
      },
      "stop_reason": {
        "type": "string",
        "enum": [
          "Completed",
          "Budget#7270",
          "Quality",
          "Error",
          "Timeout"
        ],
        "description": "Why execution terminated"
      },
      "outputs": {
        "description": "Produced artifacts \u2014 optional; a failed Result may yield none"
      },
      "task_ref": {
        "type": "string",
        "description": "The task this result satisfies"
      },
      "confidence_score": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
      },
      "provenance_trace": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "metrics": {
        "type": "object"
      }
    }
  },
  "dependencies": {
    "references": {
      "metric": "Metric#17fd",
      "solution": "Solution#fcea"
    }
  }
}
```

---

## Risk#1980

```json
{
  "handle": "Risk",
  "mechanism": "A structured representation of potential negative outcomes. It combines: 1. {{probability}} (likelihood of occurrence), 2. Severity (impact {{metric}} if it occurs), 3. Mitigation (actions to reduce probability or severity), 4. Trigger (conditions that indicate the risk is materializing). Risks are attached to steps, aggregated at the manifest level, and may violate constraints if they materialize.",
  "gloss": "Quantified potential for negative outcome",
  "failure_modes": [
    "Risk Blindness: Failing to identify a material risk.",
    "Risk Theater: Documenting risks without meaningful mitigation.",
    "Probability Miscalibration: Systematically under/over-estimating likelihood.",
    "Cascade Blindness: Missing that one risk triggers others."
  ],
  "invariants": [
    "Quantification: Probability and severity must be estimated, not just named.",
    "Mitigation: Each significant risk must have at least one mitigation strategy.",
    "Monitoring: Triggers must be observable during execution."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Risk#mh:SHA-256:198049488be8dcf811bfced0230ca10889fb531b03c6c7f66eb7dc131116be9d",
  "sema_ref": "Risk#1980",
  "sema_stub": "1980",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "probability",
      "severity"
    ],
    "properties": {
      "risk_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "probability": {
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "Likelihood of occurrence"
      },
      "severity": {
        "type": "number",
        "description": "Impact metric if materialized"
      },
      "mitigation": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Actions to reduce risk"
      },
      "trigger": {
        "type": "string",
        "description": "Observable condition indicating materialization"
      }
    }
  },
  "dependencies": {
    "references": {
      "probability": "Probability#356b",
      "metric": "Metric#17fd"
    }
  }
}
```

---

## RuleSet#7738

```json
{
  "handle": "RuleSet",
  "mechanism": "A structured collection of {{constraint}}s and invariants that defines a validity boundary. It serves as the immutable input for validation logic, distinct from a mutable policy or social {{constitution}}.",
  "gloss": "Immutable collection of constraints",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "constraints"
    ],
    "properties": {
      "constraints": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of constraint hashes"
      }
    }
  },
  "sema_ref": "RuleSet#7738",
  "sema_id": "sema:RuleSet#mh:SHA-256:77385cdef863910a916a17c4391688a9b48671019673db185ff12f81c9111f61",
  "sema_stub": "7738",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constitution": "Constitution#8cb8",
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## Score#d220

```json
{
  "handle": "Score",
  "mechanism": "A numerical {{value}} representing the result of an evaluation or measurement. It quantifies a specific property (e.g., quality, fit, risk) on a defined scale.",
  "gloss": "Quantitative evaluation result",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "value",
      "normalized_range",
      "metric_id"
    ],
    "properties": {
      "value": {
        "type": "number",
        "description": "The numerical score value"
      },
      "normalized_range": {
        "type": "object",
        "required": [
          "min",
          "max"
        ],
        "properties": {
          "min": {
            "type": "number"
          },
          "max": {
            "type": "number"
          }
        },
        "description": "The [min, max] range this score is normalized against"
      },
      "metric_id": {
        "type": "string",
        "description": "Identifier of what was scored"
      }
    }
  },
  "sema_ref": "Score#d220",
  "sema_id": "sema:Score#mh:SHA-256:d2202db2d9ebb0b44afc6c6d49f918e7bb5635229d635674c2d02090c7b3fe0a",
  "sema_stub": "d220",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "composes_with": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## ScoringFunction#3a4e

```json
{
  "handle": "ScoringFunction",
  "data_schema": {
    "type": "object",
    "required": [
      "function_id",
      "input_type",
      "output_range"
    ],
    "properties": {
      "function_id": {
        "type": "string",
        "description": "Unique identifier for this scoring function"
      },
      "input_type": {
        "type": "string",
        "description": "Expected input schema or type"
      },
      "output_range": {
        "type": "object",
        "properties": {
          "min": {
            "type": "number"
          },
          "max": {
            "type": "number"
          }
        },
        "description": "Valid output range"
      },
      "logic": {
        "type": "string",
        "description": "Description or reference to scoring logic"
      }
    }
  },
  "mechanism": "A deterministic logical unit that maps an input artifact to a scalar {{value}} (Score). Encapsulates ranking and evaluation criteria as a first-class Noun, so callers can pass the scoring logic as an input rather than embed it inline in their own mechanism.",
  "gloss": "Deterministic valuation logic",
  "invariants": [
    "Determinism: Same input always yields same score.",
    "Range: Output must be within [0.0, 1.0] or [-inf, +inf]."
  ],
  "sema_id": "sema:ScoringFunction#mh:SHA-256:3a4ef49f597cf15d2971c8b1769506bc5a434909e98cede098d5c16664c94232",
  "sema_ref": "ScoringFunction#3a4e",
  "sema_stub": "3a4e",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## Sequence#b0b8

```json
{
  "handle": "Sequence",
  "data_schema": {
    "type": "object",
    "required": [
      "steps"
    ],
    "properties": {
      "steps": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Ordered list of step IDs"
      },
      "current_index": {
        "type": "integer",
        "description": "Index of currently executing step"
      },
      "completed": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "IDs of completed steps"
      }
    }
  },
  "mechanism": "Ordered execution: A then B. Output of A available to B.",
  "gloss": "Sequential ordering",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Sequence#mh:SHA-256:b0b8e964bbbea762dc40b4b6c1f26de9542a2fec19412e0094c7288c2a54553f",
  "sema_ref": "Sequence#b0b8",
  "sema_stub": "b0b8",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Shard#1e74

```json
{
  "handle": "Shard",
  "data_schema": {
    "type": "object",
    "required": [
      "shard_id",
      "partition_index"
    ],
    "properties": {
      "shard_id": {
        "type": "string",
        "description": "Unique identifier for this shard"
      },
      "key": {
        "type": "string",
        "description": "The key used to route to this shard"
      },
      "partition_index": {
        "type": "integer",
        "description": "Which partition this shard belongs to"
      },
      "data": {
        "description": "The shard's contents"
      }
    }
  },
  "mechanism": "The fundamental primitive of distribution. It deterministically partitions a Resource, {{state}}, or {{vector}} into disjoint subsets (Shards) based on a Key (e.g., ID, Hash, Time). Unlike `Decompose` (which splits complexity), `Shard` splits volume/load.",
  "gloss": "Deterministic partitioning of state",
  "invariants": [
    "Conservation: Sum(Shards) == Total.",
    "Disjointness: Intersection(Shard_A, Shard_B) == Empty.",
    "Determinism: Key K always routes to Shard S."
  ],
  "parameters": [
    {
      "name": "key_function",
      "type": "Enum",
      "range": "{Hash, Range, Directory}",
      "description": "Partitioning strategy for distributing data across shards"
    },
    {
      "name": "partitions",
      "type": "Integer",
      "range": "[2, 256]",
      "description": "Number of partitions to divide state into"
    }
  ],
  "_meta": {
    "tier": 0,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Shard#mh:SHA-256:1e7407cbee28a243c16fac90559884c44c3d12cbded23486cd281853627bad0b",
  "sema_ref": "Shard#1e74",
  "sema_stub": "1e74",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "vector": "Vector#c7c4",
      "state": "State#4d58"
    }
  }
}
```

---

## Signal#f39d

```json
{
  "handle": "Signal",
  "data_schema": {
    "type": "object",
    "required": [
      "signal_id",
      "payload"
    ],
    "properties": {
      "signal_id": {
        "type": "string",
        "description": "Unique identifier for this emission"
      },
      "payload": {
        "description": "The information being emitted (any valid JSON)"
      },
      "emitter_id": {
        "type": "string",
        "description": "Source of the signal (optional)"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "When signal was emitted"
      }
    }
  },
  "mechanism": "Emission of information into environment. No guaranteed recipient. Fire-and-forget.",
  "gloss": "Raw information emission",
  "invariants": [
    "Broadcast: Signal is available to any observer in the medium.",
    "Information: Must distinguish itself from noise."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Signal#mh:SHA-256:f39d9ead873eb693a51f3944066dae67a238b07cd9ba6e194023785fa7d884fe",
  "sema_ref": "Signal#f39d",
  "sema_stub": "f39d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Skeleton#c363

```json
{
  "handle": "Skeleton",
  "data_schema": {
    "type": "object",
    "required": [
      "outline"
    ],
    "properties": {
      "outline": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "High-level points to be expanded"
      },
      "expansions": {
        "type": "object",
        "description": "Map of outline point index to expanded content"
      }
    }
  },
  "mechanism": "First generates a skeletal outline of the answer, then expands each point in parallel. Optimizes for latency over depth. Defines the parallel structure for rapid reasoning.",
  "gloss": "Parallel outline-first topology",
  "invariants": [
    "Independence: Expansion of Point A must not depend on Point B."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_id": "sema:Skeleton#mh:SHA-256:c363c9db1e917d4920a28b689c8e0f3fcfcd7060fde1963cea22b352570d5c87",
  "sema_ref": "Skeleton#c363",
  "sema_stub": "c363",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Snapshot#0ae9

```json
{
  "handle": "Snapshot",
  "mechanism": "A static, immutable record of the {{state}} of a {{system}} or object at a specific point in time.",
  "gloss": "Immutable state record",
  "failure_modes": [
    "Serialization Gap: In-memory state (e.g., open sockets) that cannot be serialized.",
    "Corruption: Snapshot hash matches but data is unreadable.",
    "Staleness: Restoring from a snapshot that is logically valid but temporally obsolete."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "related": [
      "StateSnapshot#940f"
    ]
  },
  "sema_id": "sema:Snapshot#mh:SHA-256:0ae992361f9dfef49e88efa9a985826833260038fb99978615f5df709eba04f1",
  "sema_ref": "Snapshot#0ae9",
  "sema_stub": "0ae9",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "snapshot_id",
      "timestamp",
      "state_hash",
      "data"
    ],
    "properties": {
      "snapshot_id": {
        "type": "string"
      },
      "target_system_id": {
        "type": "string"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      },
      "state_hash": {
        "type": "string",
        "description": "Merkle root of the state"
      },
      "data": {
        "type": "object",
        "description": "The actual serialized state payload"
      },
      "meta": {
        "type": "object",
        "properties": {
          "reason": {
            "type": "string"
          },
          "creator_id": {
            "type": "string"
          }
        }
      }
    }
  },
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314"
    }
  }
}
```

---

## Solution#fcea

```json
{
  "handle": "Solution",
  "mechanism": "Recursive {{work}} Unit. Encapsulates the output {{artifact}}, its Provenance (Creator, Time), and the Component {{tree}} of sub-solutions used to generate it. It serves as the verifiable output container for a {{task}}, validated against the acceptance criteria.",
  "gloss": "The fractal unit of completed work",
  "failure_modes": [
    "Orphaned {{artifact}}: Solution does not reference a valid {{task}} ID.",
    "Broken Lineage: Sub-solution verification failed ({{chain}} of Custody broken).",
    "Schema Violation: {{artifact}} data does not match acceptance criteria type."
  ],
  "invariants": [
    "Immutability: Once finalized, {{artifact}} and Provenance cannot be modified.",
    "Traceability: Provenance must be cryptographically signed by the Creator."
  ],
  "preconditions": [
    "{{artifact}} generated",
    "{{task}} ID is valid"
  ],
  "postconditions": [
    "Solution sealed and ready for transport"
  ],
  "parameters": [
    {
      "name": "confidence",
      "type": "Probability#356b",
      "range": "[0.0, 1.0]",
      "description": "Self-assessed reliability"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "artifact",
      "provenance",
      "task_ref"
    ],
    "properties": {
      "artifact": {
        "description": "The output produced by this solution"
      },
      "provenance": {
        "type": "object",
        "properties": {
          "creator_id": {
            "type": "string"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "signature": {
            "type": "string"
          }
        }
      },
      "task_ref": {
        "type": "string",
        "description": "Reference to the originating task"
      },
      "component_tree": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Sub-solutions used"
      },
      "confidence": {
        "type": "number",
        "minimum": 0,
        "maximum": 1
      },
      "cost_incurred": {
        "type": "number",
        "description": "Total compute cost in tokens"
      }
    }
  },
  "sema_id": "sema:Solution#mh:SHA-256:fcea1ece4a23322f69d4a17664ba17d2f54f2cec47d2526d874a0766d84f635e",
  "sema_ref": "Solution#fcea",
  "sema_stub": "fcea",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    },
    "references": {
      "chain": "Chain#711e",
      "work": "Work#d2c6",
      "artifact": "Artifact#6254",
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## Spec#a036

```json
{
  "handle": "Spec",
  "mechanism": "A rigorous definition of requirements for an {{artifact}}. It defines the shape, behavior, and {{constraint}}s that a target must satisfy. Distinct from {{plan}} (how to build) or {{goal}} (what to achieve), a Spec is the 'Definition of Done'.",
  "gloss": "Rigorous requirement definition",
  "invariants": [
    "Verifiability: Every requirement must be testable (binary pass/fail).",
    "Immutability: Once defined, the Spec acts as a fixed contract."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "description": "Schema for Spec",
    "properties": {
      "requirements": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "constraints": {
        "type": "object"
      }
    }
  },
  "sema_ref": "Spec#a036",
  "sema_id": "sema:Spec#mh:SHA-256:a036f5bd8f9f00d39ec6f9c48855b2aeea206f2a052ed72307e2d6e53bbcaaf7",
  "sema_stub": "a036",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d",
      "goal": "Goal#009e",
      "artifact": "Artifact#6254",
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## State#4d58

```json
{
  "handle": "State",
  "data_schema": {
    "type": "object",
    "required": [
      "state_id",
      "data"
    ],
    "properties": {
      "state_id": {
        "type": "string",
        "description": "Unique identifier for this state snapshot"
      },
      "data": {
        "type": "object",
        "description": "The actual state values"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "When this state was captured"
      }
    }
  },
  "mechanism": "The stored information representing the current {{condition}} of a {{system}}.",
  "gloss": "System condition at time T",
  "invariants": [
    "Persistence: State remains constant unless acted upon.",
    "Uniqueness: At time T, the system has exactly one State."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:State#mh:SHA-256:4d582a0ac4af7ae886c83da9825e07c39f1e72ece21fd65a40b6a4fc71882721",
  "sema_ref": "State#4d58",
  "sema_stub": "4d58",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "system": "System#e314"
    }
  }
}
```

---

## Status#1cf9

```json
{
  "handle": "Status",
  "mechanism": "The graded verification outcome type: Verified (the check passed), Falsified (the check failed), or Unknown (the check could not reach a definitive answer). Carries an optional reason field explaining the outcome. Distinct from Boolean (strict two-valued, no Unknown) and from Decision (three-valued with proceed/halt/debt operational semantics).",
  "gloss": "Graded verification outcome: Verified, Falsified, or Unknown",
  "data_schema": {
    "type": "object",
    "required": [
      "value"
    ],
    "properties": {
      "value": {
        "type": "string",
        "enum": [
          "Verified",
          "Falsified",
          "Unknown"
        ],
        "description": "The outcome of a verification operation"
      },
      "reason": {
        "type": "string",
        "description": "Optional explanation for the outcome"
      }
    }
  },
  "invariants": [
    "Tri-valued: exactly one of {Verified, Falsified, Unknown}.",
    "Unknown is not a failure: it is an honest absence of evidence, distinct from Falsified."
  ],
  "_meta": {
    "tier": 0,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Status#mh:SHA-256:1cf93b675b4c08b59123cb061984604d6cb3848818bb65ad87a12cb8e0503cee",
  "sema_ref": "Status#1cf9",
  "sema_stub": "1cf9"
}
```

---

## Step#5f22

```json
{
  "handle": "Step",
  "mechanism": "An atomic unit of action. It specifies: 1. Preconditions (what must be true before), 2. Action (what to do), 3. Postconditions (what will be true after), 4. Rollback (how to undo if needed). It acts as a node in a causal graph.",
  "gloss": "Atomic action with pre/post conditions",
  "failure_modes": [
    "Precondition Violation: Step executed when preconditions not met.",
    "Postcondition Failure: Step completes but postconditions not achieved.",
    "Rollback Failure: Unable to undo a failed step."
  ],
  "invariants": [
    "Atomicity: A Step either fully completes or fully rolls back.",
    "Causal Closure: Step preconditions must be satisfiable by prior steps or initial state."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "tier": 1,
    "ring": 0,
    "related": [
      "Plan#fd6d"
    ]
  },
  "sema_id": "sema:Step#mh:SHA-256:5f2205a7812b52b35dd75469367956e838a99360de7fde55e1585bd155eed128",
  "sema_ref": "Step#5f22",
  "sema_stub": "5f22",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "step_id",
      "action_type",
      "params"
    ],
    "properties": {
      "step_id": {
        "type": "string"
      },
      "action_type": {
        "type": "string",
        "description": "The verb or tool to invoke"
      },
      "params": {
        "type": "object",
        "description": "Arguments for the action"
      },
      "dependencies": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "IDs of steps that must complete first"
      },
      "retry_policy": {
        "type": "object",
        "properties": {
          "max_attempts": {
            "type": "integer"
          },
          "backoff_strategy": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

---

## Stream#22f3

```json
{
  "handle": "Stream",
  "data_schema": {
    "type": "object",
    "required": [
      "stream_id"
    ],
    "properties": {
      "stream_id": {
        "type": "string",
        "description": "Unique stream identifier"
      },
      "messages": {
        "type": "array",
        "description": "Ordered sequence of messages"
      },
      "cursor": {
        "type": "integer",
        "description": "Current read position in the stream"
      },
      "bounded": {
        "type": "boolean",
        "description": "Whether the stream has a known end"
      }
    }
  },
  "mechanism": "An ordered, potentially unbounded sequence of Messages. Represents real-time data pipes, log feeds, or conversational histories. Streams support operations like mapping, filtering, and backpressure. Utilizes {{message}}.",
  "gloss": "Continuous data flow",
  "invariants": [
    "Ordering: Messages M_n and M_n+1 maintain relative sequence.",
    "Causality: Effects cannot precede causes in the stream."
  ],
  "preconditions": [
    "A Source emitting Messages"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Stream#mh:SHA-256:22f34aeb7fa579ab417c94c54424d1b54e73097208077c890b0e429be87c9f71",
  "sema_ref": "Stream#22f3",
  "sema_stub": "22f3",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "message": "Message#f767"
    }
  }
}
```

---

## Subject#788f

```json
{
  "handle": "Subject",
  "data_schema": {
    "type": "object",
    "required": [
      "subject_id",
      "entity_type"
    ],
    "properties": {
      "subject_id": {
        "type": "string",
        "description": "Unique identifier for the subject"
      },
      "entity_type": {
        "type": "string",
        "description": "What kind of entity (agent, artifact, system)"
      },
      "reference": {
        "type": "string",
        "description": "Pointer to the actual entity"
      }
    }
  },
  "mechanism": "The target entity of an observation, evaluation, or {{act}}. It represents the 'Who' or 'What' in a subject-object relationship.",
  "gloss": "The target of an operation",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_ref": "Subject#788f",
  "sema_id": "sema:Subject#mh:SHA-256:788f7cb48e982144f15691fa0259a8b4f620e6eaf4447129c95f23d8e3008d1e",
  "sema_stub": "788f",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "act": "Act#5d55"
    }
  }
}
```

---

## Summary#f785

```json
{
  "handle": "Summary",
  "mechanism": "A compressed representation of a {{datum}} or {{artifact}} that retains high-{{value}} (salient) information while discarding redundancy.",
  "gloss": "Condensed information",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "source_ref"
    ],
    "properties": {
      "source_ref": {
        "type": "string",
        "description": "sema_id of the source being summarized"
      },
      "compression_ratio": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "Size ratio (summary_len/source_len)"
      },
      "preserves": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Semantic dimensions preserved (e.g., 'thesis', 'timeline', 'constraints')"
      }
    }
  },
  "sema_ref": "Summary#f785",
  "sema_id": "sema:Summary#mh:SHA-256:f785cae6871dc00700bb21296033c24d01e0abc331097a1d43a3d423830332d6",
  "sema_stub": "f785",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "composes_with": {
      "datum": "Datum#31cf",
      "artifact": "Artifact#6254"
    },
    "references": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## System#e314

```json
{
  "handle": "System",
  "data_schema": {
    "type": "object",
    "required": [
      "system_id",
      "components"
    ],
    "properties": {
      "system_id": {
        "type": "string",
        "description": "Unique system identifier"
      },
      "components": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "IDs of component parts"
      },
      "boundaries": {
        "type": "object",
        "description": "What is inside vs outside the system"
      },
      "purpose": {
        "type": "string",
        "description": "The function or goal of the system"
      }
    }
  },
  "mechanism": "A set of interacting or interdependent component parts forming a complex/intricate whole. Systems have boundaries, structure, and purpose (or function) expressed in their interactions.",
  "gloss": "Complex whole of interacting parts",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:System#mh:SHA-256:e314d24e05d0e9ffaaa9c44b249bca8882f00ae6596af18edd245a4fe9df5f0e",
  "sema_ref": "System#e314",
  "sema_stub": "e314",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Task#b328

```json
{
  "handle": "Task",
  "mechanism": "A specification of intent to be performed by a {{system}}. It encapsulates what to achieve without prescribing the method (how). A Task is recursive: it can be decomposed into child Tasks. Tasks form a {{hierarchy}} where child {{constraint}}s must be a superset of parent {{constraint}}s (Holographic Inheritance).",
  "gloss": "The atomic unit of intent",
  "failure_modes": [
    "{{constraint}} Escape: Child task violates parent safety constraints.",
    "Orphan Task: Task created without linkage to parent (except Root).",
    "Zombie Task: Task continues after its {{context}} is invalidated.",
    "Ambiguous Intent: Task description admits multiple incompatible interpretations."
  ],
  "invariants": [
    "Holographic Inheritance: {{constraint}}s(Child) must include ALL {{constraint}}s(Parent).",
    "Intent Preservation: Decomposition must not lose the original goal.",
    "Linkage: Every non-root Task must reference its parent."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Task#mh:SHA-256:b32808db164555a0b65e7eedb2437f0165206f6582b207a5dfd6b4bb90d9a04c",
  "sema_ref": "Task#b328",
  "sema_stub": "b328",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "operation",
      "inputs",
      "acceptance_criteria"
    ],
    "properties": {
      "operation": {
        "type": "string",
        "description": "What the Task does \u2014 the intent"
      },
      "inputs": {
        "type": "object",
        "description": "Typed inputs to the operation"
      },
      "acceptance_criteria": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Conditions that mark the Task complete; closure signal for the caller"
      },
      "budget": {
        "type": "object",
        "description": "Optional resource ceiling (compute, time, tokens)"
      },
      "parent_id": {
        "type": "string",
        "description": "Super-task reference if hierarchical"
      },
      "deadline": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "hierarchy": "Hierarchy#d530",
      "system": "System#e314",
      "context": "Context#510a"
    }
  }
}
```

---

## Tension#c39e

```json
{
  "handle": "Tension",
  "mechanism": "A data structure representing a detected conflict between two or more valid but mutually exclusive signals, constraints, or values. It serves as the input for resolution protocols like {{dialectic}} or {{yield}}.",
  "gloss": "Reified conflict state",
  "invariants": [
    "Mutually Exclusive: The bound elements cannot both be fully satisfied simultaneously.",
    "Persistence: Must persist until explicitly resolved."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Tension#mh:SHA-256:c39e010ca317c5ea11144728d4bac9d3e973a87bc75eb9063123ab1a45494c3d",
  "sema_ref": "Tension#c39e",
  "sema_stub": "c39e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "tension_id",
      "polarity_a",
      "polarity_b",
      "status"
    ],
    "properties": {
      "tension_id": {
        "type": "string"
      },
      "polarity_a": {
        "type": "object",
        "description": "The first conflicting force/idea/constraint"
      },
      "polarity_b": {
        "type": "object",
        "description": "The opposing force/idea/constraint"
      },
      "status": {
        "type": "string",
        "enum": [
          "Active",
          "Resolving",
          "Resolved",
          "Ignored"
        ]
      },
      "resolution_strategy": {
        "type": "string",
        "description": "How the tension is being handled"
      }
    }
  },
  "dependencies": {
    "references": {
      "dialectic": "Dialectic#5cc3",
      "yield": "Yield#2931"
    }
  }
}
```

---

## Topology#2408

```json
{
  "handle": "Topology",
  "data_schema": {
    "type": "object",
    "required": [
      "shape"
    ],
    "properties": {
      "shape": {
        "type": "string",
        "enum": [
          "Linear",
          "Tree#a5a3",
          "DAG#de34",
          "Cyclic#5d28",
          "Graph"
        ],
        "description": "The structural pattern"
      },
      "nodes": {
        "type": "array",
        "description": "List of node definitions"
      },
      "edges": {
        "type": "array",
        "description": "List of edge definitions (connections)"
      }
    }
  },
  "mechanism": "Defines the node-edge structure of a reasoning process. Returns the 'Shape' of execution (e.g., Linear, Tree, DAG, Cyclic).",
  "gloss": "Interface for reasoning structures",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_ref": "Topology#2408",
  "sema_id": "sema:Topology#mh:SHA-256:240866adb33767b1d651245af4038bfbcb29a575b2704288273eba41937e0560",
  "sema_stub": "2408",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Transition#072d

```json
{
  "handle": "Transition",
  "data_schema": {
    "type": "object",
    "required": [
      "from_state",
      "to_state",
      "trigger_event"
    ],
    "properties": {
      "from_state": {
        "type": "string",
        "description": "Origin state ID"
      },
      "to_state": {
        "type": "string",
        "description": "Destination state ID"
      },
      "trigger_event": {
        "type": "object",
        "description": "Event causing the transition"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "mechanism": "The atomic progression from an origin {{state}} to a destination {{state}}, adhering to {{system}} transition rules.",
  "gloss": "State change",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Transition#mh:SHA-256:072d2cb413f704ace7da4027449396ee7bac683536da918a39e93f4f43e0d1b5",
  "sema_ref": "Transition#072d",
  "sema_stub": "072d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314"
    }
  }
}
```

---

## Tree#a5a3

```json
{
  "handle": "Tree",
  "data_schema": {
    "type": "object",
    "required": [
      "nodes",
      "edges",
      "root_id"
    ],
    "properties": {
      "nodes": {
        "type": "array",
        "description": "List of node IDs or objects"
      },
      "edges": {
        "type": "array",
        "description": "Adjacency list (parent->child)"
      },
      "root_id": {
        "type": "string",
        "description": "The single root node"
      }
    }
  },
  "mechanism": "A branching {{topology}} where multiple lines of reasoning are explored simultaneously. Allows backtracking and pruning of unpromising branches (BFS/DFS). A Tree is the constrained form of a directed acyclic graph where each non-root node has exactly one parent.",
  "gloss": "Branching reasoning topology",
  "invariants": [
    "Rootedness: All nodes descend from a single root.",
    "Acyclicity: No node is an ancestor of itself."
  ],
  "parameters": [
    {
      "name": "breadth",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Maximum branches explored per node. Left open at the foundation: binary trees use 2, beam search uses 50+, decision trees can be millions. Descendants specialize."
    },
    {
      "name": "depth",
      "type": "Integer",
      "range": "[1, 20]",
      "description": "Maximum tree depth"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_ref": "Tree#a5a3",
  "sema_id": "sema:Tree#mh:SHA-256:a5a32e4770d6b17f8aae9be28e532900434ff787bfcaa768e755138293c12c65",
  "sema_stub": "a5a3",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "topology": "Topology#2408"
    }
  }
}
```

---

## Value#3c5d

```json
{
  "handle": "Value",
  "data_schema": {
    "type": "object",
    "required": [
      "magnitude",
      "unit"
    ],
    "properties": {
      "magnitude": {
        "type": "number",
        "description": "Scalar utility or worth"
      },
      "unit": {
        "type": "string",
        "description": "Currency, energy, or utility metric"
      },
      "context": {
        "type": "string",
        "description": "Scope where this value applies"
      }
    }
  },
  "mechanism": "A quantitative or qualitative measure of utility, worth, or priority assigned to a {{state}} or resource.",
  "gloss": "A measure of utility",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:Value#mh:SHA-256:3c5de39bf1f148c0da463c8e5b2fd928a67ce8547fe30a5d5afe436560ab68b6",
  "sema_ref": "Value#3c5d",
  "sema_stub": "3c5d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

## Variable#179a

```json
{
  "handle": "Variable",
  "data_schema": {
    "type": "object",
    "required": [
      "name",
      "value",
      "type"
    ],
    "properties": {
      "name": {
        "type": "string",
        "description": "Variable identifier"
      },
      "value": {
        "description": "Current state"
      },
      "type": {
        "type": "string",
        "description": "Data type definition"
      },
      "history": {
        "type": "array",
        "description": "Previous values (optional)"
      }
    }
  },
  "mechanism": "A value that can change or adapt within the system. It represents a dimension of freedom in the problem space.",
  "gloss": "Mutable value",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Variable#mh:SHA-256:179a757268e1c339725e09418eba7989ba1ffb2148e8b0f1241d2ff90062116c",
  "sema_ref": "Variable#179a",
  "sema_stub": "179a"
}
```

---

## Vector#c7c4

```json
{
  "handle": "Vector",
  "data_schema": {
    "type": "object",
    "required": [
      "values",
      "dimensions"
    ],
    "properties": {
      "values": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "description": "Ordered numerical components"
      },
      "dimensions": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Labels for vector dimensions (e.g. x, y, z)"
      }
    }
  },
  "mechanism": "A multi-dimensional array of numbers representing a position in a semantic space.",
  "gloss": "Semantic position array",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1,
    "related": [
      "LatentAttachment#15a6"
    ]
  },
  "sema_id": "sema:Vector#mh:SHA-256:c7c4d97d3416646673aa3d70d27aa4da40c7c2ae86180c92901a0e23429ffedc",
  "sema_ref": "Vector#c7c4",
  "sema_stub": "c7c4",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures"
}
```

---

## Work#d2c6

```json
{
  "handle": "Work",
  "data_schema": {
    "type": "object",
    "required": [
      "timestamp",
      "effort_cost"
    ],
    "properties": {
      "previous_hash": {
        "type": "string",
        "description": "State before work"
      },
      "new_hash": {
        "type": "string",
        "description": "State after work"
      },
      "effort_cost": {
        "type": "object",
        "description": "Resources consumed (tokens, time)"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "mechanism": "The primitive representation of directed effort. It represents the expenditure of resources (Compute, Time, Energy) to transform a {{task}} from an 'Open' state to a 'Solved' state (reducing local entropy). Work is the bridge between Intent (thinking) and Reality ({{act}}). Work is validated against an acceptance criteria.",
  "gloss": "The application of effort to reduce entropy",
  "failure_modes": [
    "Thrashing: Expending resources without making progress toward the goal.",
    "Burnout: Exhausting the {{budget}} before the task is complete.",
    "Busywork: Performing valid actions that do not contribute to the objective function."
  ],
  "invariants": [
    "Cost: Work always consumes resources (Time/Tokens > 0).",
    "Directionality: Work must be vector-aligned with a Goal (otherwise it is just 'Heat')."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "related": [
      "EntropyPump#c313"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Work#mh:SHA-256:d2c65202efac99cacff743ce36b7e628e4ff7b246779abcfb0f0073ea059be1a",
  "sema_ref": "Work#d2c6",
  "sema_stub": "d2c6",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "act": "Act#5d55"
    },
    "composes_with": {
      "task": "Task#b328"
    }
  }
}
```

---

## Act#5d55

```json
{
  "handle": "Act",
  "mechanism": "The fundamental primitive for any operation that modifies state external to the actor's private memory. It is the root interface for tool invocations, API calls, and physical actuation. All Acts must be authorized, logged, and potentially reversible (or explicitly marked irreversible).",
  "gloss": "Root primitive for state modification",
  "failure_modes": [
    "Unintended Side-effect: The action changed state in a way not predicted by the actor.",
    "Partial Execution: The action failed midway, leaving the system in an inconsistent state.",
    "Authorization Failure: The actor attempted an action it lacks permission to perform."
  ],
  "invariants": [
    "Authorization: Action must be permitted by the current {{context}} constraints.",
    "Observability: All Acts must produce a signal (Success/Failure/Result) observable by the actor.",
    "Causality: An Act cannot precede its Cause (the {{select}}ion of action)."
  ],
  "preconditions": [
    "Actor has decided to act",
    "Target system is available",
    "Permissions grant access"
  ],
  "postconditions": [
    "External state is modified",
    "Action log is updated",
    "Resources (energy/credits) are consumed"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "related": [
      "ToolInvoke#4694",
      "ReAct#e018",
      "AgentSandbox#fc41"
    ],
    "ring": 0
  },
  "sema_id": "sema:Act#mh:SHA-256:5d55ad7db734254e55dfcb82c83b32a4fd5ac955428e3ff95706f9c3bfc787cd",
  "sema_ref": "Act#5d55",
  "sema_stub": "5d55",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "select": "Select#15c2",
      "context": "Context#510a"
    }
  }
}
```

---

## Actor#6926

```json
{
  "handle": "Actor",
  "mechanism": "A primitive entity capable of executing an {{act}}. Unlike an agent (which possesses intent and reasoning), an Actor is a pure execution container defined by its {{identity}}, {{nature}}, and capability set. It serves as the foundational subject for permissions and logging.",
  "gloss": "A capability-bearing entity",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "agent_id",
      "public_key",
      "status"
    ],
    "properties": {
      "agent_id": {
        "type": "string",
        "description": "Unique handle"
      },
      "public_key": {
        "type": "string",
        "description": "Cryptographic identity for signing"
      },
      "role": {
        "type": "string",
        "description": "Current active role/persona"
      },
      "status": {
        "type": "string",
        "enum": [
          "Idle",
          "Busy",
          "Offline",
          "Error"
        ],
        "description": "Availability state"
      },
      "capabilities": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of supported tool/protocol hashes"
      },
      "endpoint": {
        "type": "string",
        "description": "Communication address"
      }
    }
  },
  "sema_ref": "Actor#6926",
  "sema_id": "sema:Actor#mh:SHA-256:69261bc3b260a9235b8d5fbef8b0c53c9773e60ed6d4df04babfffffd2897a89",
  "sema_stub": "6926",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "nature": "Nature#6c1a",
      "identity": "Identity#626c"
    },
    "composes_with": {
      "act": "Act#5d55"
    }
  }
}
```

---

## Aggregate#7912

```json
{
  "handle": "Aggregate",
  "mechanism": "Mathematical Reduction. A deterministic function that maps a {{vector}} of inputs to a single Scalar {{value}}. Implements standard statistical operations (Mean, Mode, Median) to compress signal bandwidth. When the caller supplies {{weights}} alongside the vector, the reduction becomes a weighted one. It serves as the computational backbone for consensus mechanisms.",
  "gloss": "Reduce a set to a summary statistic",
  "failure_modes": [
    "Type Mismatch: Input list contains incomparable types (e.g., Integers mixed with Strings).",
    "Empty Set: Attempting to aggregate a list with length 0 (Undefined for Mean/{{mode}}).",
    "Overflow: Sum of inputs exceeds maximum integer size (if strictly typed)."
  ],
  "invariants": [
    "Determinism: F(Input) always yields the same Output.",
    "Reduction: Size(Output) < Size(Input)."
  ],
  "preconditions": [
    "All elements in list share a comparable type",
    "Input list is non-empty"
  ],
  "postconditions": [
    "Single summary value returned"
  ],
  "parameters": [
    {
      "name": "function",
      "type": "Enum",
      "range": "{Mean, Median, Mode#0e74, Sum, Min, Max, Variance, StdDev}",
      "description": "Default: Mean"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Aggregate#mh:SHA-256:791202e13011d1f46a0340e4c25496549c82296bb068ab5d7b327b5af6b3f65a",
  "sema_ref": "Aggregate#7912",
  "sema_stub": "7912",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "vector": "Vector#c7c4"
    },
    "yields": {
      "value": "Value#3c5d"
    },
    "references": {
      "mode": "Mode#0e74"
    }
  }
}
```

---

## Backoff#315a

```json
{
  "handle": "Backoff",
  "mechanism": "Exponential Delay: On failure, wait delay D before retry. On repeated failure, D *= multiplier (typically 2). Add jitter to prevent thundering herd. Cap at maximum delay. Reset on success.",
  "gloss": "Exponential delay to reduce contention",
  "failure_modes": [
    "Starvation: Unlucky agents keep backing off while others succeed, never getting a slot."
  ],
  "invariants": [
    "retry budget must be finite (max_attempts set before first attempt)."
  ],
  "parameters": [
    {
      "name": "base_delay",
      "type": "Duration",
      "range": "[100ms, 10s]",
      "description": "Initial wait before retry"
    },
    {
      "name": "jitter_factor",
      "type": "Float",
      "range": "[0.0, 0.5]",
      "description": "Randomization to prevent thundering herd"
    },
    {
      "name": "max_retries",
      "type": "Integer",
      "range": "[1, 10]",
      "description": "Attempts before permanent failure"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Backoff#mh:SHA-256:315a36ef873a63c30740ce89b1aeb542836a068ef0d81a6e3aaaec062d70bc60",
  "sema_ref": "Backoff#315a",
  "sema_stub": "315a",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Budget#7270

```json
{
  "handle": "Budget",
  "mechanism": "A quantified allocation of resources (compute, time, energy) that constrains execution. It serves as a hard limit on consumption, preventing exhaustion of finite pools.",
  "gloss": "Resource allocation limit",
  "data_schema": {
    "type": "object",
    "required": [
      "total",
      "remaining",
      "unit"
    ],
    "properties": {
      "total": {
        "type": "number",
        "description": "The initial allocated amount"
      },
      "remaining": {
        "type": "number",
        "description": "The current available amount"
      },
      "unit": {
        "type": "string",
        "enum": [
          "Tokens",
          "USD",
          "Ms"
        ],
        "description": "The unit of measurement"
      }
    }
  },
  "invariants": [
    "Conservation: Allocated + Remaining = Total."
  ],
  "preconditions": [
    "Total budget defined"
  ],
  "postconditions": [
    "Budget decremented by cost"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_ref": "Budget#7270",
  "sema_id": "sema:Budget#mh:SHA-256:72709a4878eefe66ed2d66994a1a7d2e22214d3ee3d64beafecc02387099360f",
  "sema_stub": "7270",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Care#0615

```json
{
  "handle": "Care",
  "mechanism": "The application of {{work}} to reduce a target's {{entropy}} without an explicit {{value}} extraction. It creates a buffer against volatility.",
  "gloss": "Non-transactional maintenance energy",
  "invariants": [
    "Entropy Reduction: Action reduces local disorder.",
    "Resource Consumption: Care requires Work."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Care#mh:SHA-256:06158c8a04036607d8bb2f873b118dc1fdc5ca0bf8bd9dce45662c830763150f",
  "sema_ref": "Care#0615",
  "sema_stub": "0615",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "work": "Work#d2c6",
      "entropy": "Entropy#a265"
    }
  }
}
```

---

## Check#d3e8

```json
{
  "handle": "Check",
  "mechanism": "A non-blocking verification primitive. Evaluates a {{condition}} against a target and yields a {{status}} (Verified, Falsified, or Unknown). Unlike a {{gate}} (which alters control flow via a Decision), Check is purely observational and side-effect free \u2014 it answers 'is this true?' without deciding 'should we stop?'. Unknown is a first-class outcome distinct from Falsified: it asserts absence of evidence, not evidence of absence.",
  "gloss": "Side-effect-free observational verification yielding Verified/Falsified/Unknown",
  "failure_modes": [
    "False Positive: Check returns Verified due to flawed logic or sensor noise.",
    "Heisenbug: The act of checking alters the state being checked.",
    "Callers collapse Unknown into Falsified, losing the meaningful distinction."
  ],
  "invariants": [
    "Side-Effect Free: Running a check must not mutate the target state.",
    "Determinism: Same input context yields same status."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "related": [
      "Validate#ebe1",
      "Judge#9554"
    ]
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Check#mh:SHA-256:d3e8fb90bcdf48c8986b66af617b78bf57009a51749460ad982fe8fd2730cf57",
  "sema_ref": "Check#d3e8",
  "sema_stub": "d3e8",
  "dependencies": {
    "references": {
      "gate": "Gate#89fd",
      "condition": "Condition#cbd5"
    },
    "yields": {
      "status": "Status#1cf9"
    }
  }
}
```

---

## CircuitBreaker#4162

```json
{
  "handle": "CircuitBreaker",
  "mechanism": "{{state}} machine wrapper for fallible operations. Monitors failure rates of a target resource. States: (1) 'CLOSED': Requests pass normally. (2) 'OPEN': Requests fail immediately (Fail Fast) without invoking target. (3) 'HALF-OPEN': Limited trial requests allowed to test recovery. Transitions: 'CLOSED' -> 'OPEN' if failure count > threshold. 'OPEN' -> 'HALF-OPEN' after reset timeout. It wraps operations, switching to an open state on failure to prevent cascading overloads, while using {{backoff}} and retry logic to schedule recovery probes.",
  "gloss": "Fail-fast protection against cascading failures",
  "failure_modes": [
    "Flapping: Threshold too sensitive causes circuit to oscillate between Open/Closed.",
    "Zombie {{state}}: Circuit stuck 'OPEN' because reset logic failed to trigger or persists in failure.",
    "False Positive: Transient network blips trip circuit, blocking healthy traffic."
  ],
  "invariants": [
    "Fail Fast: If {{state}} == 'OPEN', request MUST be rejected immediately with zero backend cost.",
    "Leakage Protection: In 'HALF-OPEN' state, concurrency is capped (default: 1) to prevent flood during recovery.",
    "{{state}} Persistence: Failure counts reset only on successful transition to 'CLOSED'."
  ],
  "preconditions": [
    "Failure threshold defined",
    "Target resource identified"
  ],
  "postconditions": [
    "Internal state updated based on outcome",
    "Request processed OR Blocked"
  ],
  "parameters": [
    {
      "name": "failure_threshold",
      "type": "Integer",
      "range": "[1, 100]",
      "description": "Default: 5"
    },
    {
      "name": "half_open_limit",
      "type": "Integer",
      "range": "[1, 10]",
      "description": "Max probes allowed in half-open state"
    },
    {
      "name": "reset_timeout",
      "type": "Duration",
      "range": "unspecified",
      "description": "Default: 60s"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_ref": "CircuitBreaker#4162",
  "sema_id": "sema:CircuitBreaker#mh:SHA-256:41621375faf5609423cb05060fbdccf92c6d8f856607a2ae4bf35a76c90cbaec",
  "sema_stub": "4162",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "backoff": "Backoff#315a"
    }
  }
}
```

---

## Combine#5a44

```json
{
  "handle": "Combine",
  "mechanism": "Merge two same-typed values into one. Associative. {{identity}} element: Empty.",
  "gloss": "Binary merge operation",
  "invariants": [
    "Associativity: (A + B) + C = A + (B + C)",
    "Closure: Result type must match Input type"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Combine#mh:SHA-256:5a448e8da3c41cd922451ef5cef1acc7b96b99fe516815870e81cb2c18b196d6",
  "sema_ref": "Combine#5a44",
  "sema_stub": "5a44",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "identity": "Identity#626c"
    }
  }
}
```

---

## FailClosed#e6a0

```json
{
  "handle": "FailClosed",
  "mechanism": "Safety Default. If an operation fails, times out, or returns an ambiguous result, the system MUST treat it as a Negative (Deny/Stop/Reject). Prevents 'bypass on error' vulnerabilities. It acts as the wrapper for input guarding, {{output_guard}}, and {{circuit_breaker}}, enforcing a default-deny policy on any error or ambiguity.",
  "gloss": "Default-deny policy for uncertain states",
  "failure_modes": [
    "Availability Hit: {{system}} shuts down during minor outages (False Positive Denial).",
    "Dependency Deadlock: If a non-critical dependency fails, the whole system locks up."
  ],
  "invariants": [
    "Default Deny: Ambiguity == Rejection.",
    "Error Atomicity: Partial failure = Total failure (Transaction Rollback)."
  ],
  "preconditions": [
    "Fallible operation initiated"
  ],
  "postconditions": [
    "{{system}} state remains invariant (no side effects) OR Operation succeeds"
  ],
  "parameters": [
    {
      "name": "timeout_action",
      "type": "Enum",
      "range": "{Reject, Retry#4cc6, Fallback}",
      "description": "Default: Reject"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:FailClosed#mh:SHA-256:e6a09747bc7485f877033e1e6d8baa52b8ae571094910c968f7321f0828cf88c",
  "sema_ref": "FailClosed#e6a0",
  "sema_stub": "e6a0",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "output_guard": "OutputGuard#1f50",
      "system": "System#e314",
      "circuit_breaker": "CircuitBreaker#4162"
    }
  }
}
```

---

## Feedback#b477

```json
{
  "handle": "Feedback",
  "mechanism": "Information returned to a system about the effects of its actions, used to adjust future behavior. It closes the loop between output and input, enabling learning and error correction. The feedback {{signal}} contains a {{result}} and a {{metric}} indicating deviation ({{incongruity}}) from the expected outcome.",
  "gloss": "Error correction signal",
  "failure_modes": [
    "Signal Noise: Feedback is too noisy to extract actionable information.",
    "Delayed Feedback: Signal arrives too late to correct the error.",
    "Misattribution: Feedback is routed to the wrong solver."
  ],
  "invariants": [
    "Directionality: Feedback must indicate the direction of error, not just magnitude.",
    "Timeliness: Feedback value decays with latency.",
    "Attribution: Feedback must be traceable to a specific action."
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "tier": 1,
    "ring": 0
  },
  "sema_id": "sema:Feedback#mh:SHA-256:b477ae84e420a25c9cdadbe3fb58e001766677618fd6623ae4da1cceea7f04de",
  "sema_ref": "Feedback#b477",
  "sema_stub": "b477",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "signature": [
    "Signal#f39d(Incongruity#e98f)"
  ],
  "dependencies": {
    "references": {
      "incongruity": "Incongruity#e98f",
      "metric": "Metric#17fd",
      "result": "Result#195b"
    },
    "composes_with": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## FeedbackSignal#f174

```json
{
  "handle": "FeedbackSignal",
  "mechanism": "A structured packet containing the evaluation of a specific {{solution}} for a {{task}}. Carries outcome and details to the {{feedback}} mechanism.",
  "gloss": "Standardized learning feedback packet",
  "invariants": [
    "Targeted",
    "Structured"
  ],
  "sema_id": "sema:FeedbackSignal#mh:SHA-256:f174509d1cbc29c299a7a3e39a4c9246f9fb6cbe6bb9be0cd4bac6b88a2053a6",
  "sema_ref": "FeedbackSignal#f174",
  "sema_stub": "f174",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "data_schema": {
    "type": "object",
    "required": [
      "solution_ref",
      "task_ref",
      "outcome"
    ],
    "properties": {
      "solution_ref": {
        "type": "string",
        "description": "Reference to evaluated solution"
      },
      "task_ref": {
        "type": "string",
        "description": "Reference to originating task"
      },
      "outcome": {
        "type": "string",
        "enum": [
          "success",
          "failure",
          "partial"
        ],
        "description": "Evaluation result"
      },
      "details": {
        "type": "object",
        "description": "Structured feedback details"
      }
    }
  },
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "feedback": "Feedback#b477",
      "solution": "Solution#fcea"
    }
  }
}
```

---

## Greet#bbae

```json
{
  "handle": "Greet",
  "mechanism": "The initial contact protocol between two {{agent}}s. It involves a cryptographic {{identity}} verification followed by a {{compatibility_check}} to establish a shared communication channel. If successful, it transitions the connection state from 'Unknown' to 'Connected'.",
  "gloss": "Agent connection initiation",
  "failure_modes": [
    "Authentication Failure: {{identity}} could not be verified.",
    "Protocol Mismatch: Agents speak incompatible languages."
  ],
  "invariants": [
    "Mutual Auth: Both parties must verify each other.",
    "No-Op on Mismatch: Connection drops if handshake fails."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1
  },
  "sema_id": "sema:Greet#mh:SHA-256:bbaea8bfed1d642ff48d46fdb45939f74cb48360dedd6f7674f6b7630670b609",
  "sema_ref": "Greet#bbae",
  "sema_stub": "bbae",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "agent": "Agent#35b9",
      "identity": "Identity#626c"
    },
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    }
  }
}
```

---

## IdempotentWrite#b959

```json
{
  "handle": "IdempotentWrite",
  "mechanism": "A technical primitive where every write request includes a unique 'Idempotency Key'. The receiver maintains a {{cache}} of processed keys. If it receives a duplicate key, it returns the stored result without re-executing the side effects. This makes 'At-Least-Once' delivery safe. It uses a keyed {{state_lock}} to deduplicate requests, ensuring only the first write executes while subsequent ones return the cached result.",
  "gloss": "Safe retries via unique keys",
  "failure_modes": [
    "Key collision (two different requests use same key)."
  ],
  "invariants": [
    "{{identity}}: Apply(Req) == Apply(Req)",
    "Safety: Duplicate requests trigger zero additional side effects"
  ],
  "preconditions": [
    "Receiver has state storage for keys"
  ],
  "postconditions": [
    "Action executed exactly once (logically)"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "related": [
      "UniqueHandle#d9a1"
    ],
    "ring": 0
  },
  "sema_id": "sema:IdempotentWrite#mh:SHA-256:b959337ab4dbfbae132acbbd966f3ba68e9069ea099e9939dfca6b6bd34353d3",
  "sema_ref": "IdempotentWrite#b959",
  "sema_stub": "b959",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "cache": "Cache#cd97",
      "state_lock": "StateLock#8183",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Incongruity#e98f

```json
{
  "handle": "Incongruity",
  "mechanism": "A misalignment between expectation and reality. The difference between the predicted {{state}} and the observed {{state}}, often serving as a {{signal}} for learning, humor, or paradox.",
  "gloss": "The root of Humor and Paradox",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Incongruity#mh:SHA-256:e98f92b190747bd8e26597ea3f6bf095428479527d5ca69fb7b30de9423ed1f9",
  "sema_ref": "Incongruity#e98f",
  "sema_stub": "e98f",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "state": "State#4d58"
    }
  }
}
```

---

## Judge#9554

```json
{
  "handle": "Judge",
  "mechanism": "Qualitative Evaluation. Evaluates the structural merit or quality of a {{subject}} on a continuous scale [0.0, 1.0]. Unlike {{check}} (which validates binary truth) or {{validate}} (which checks schema), Judge evaluates gradients of quality by applying a {{scoring_function}} that encodes the {{criteria}}, yielding a {{score}}.",
  "gloss": "Scalar evaluation of merit",
  "failure_modes": [
    "Subjectivity Creep: {{criteria}} drift from objective to subjective without detection",
    "Threshold Gaming: {{agent}} optimizes for passing threshold rather than actual quality"
  ],
  "invariants": [
    "Range Bound: Score must be between 0.0 and 1.0 inclusive.",
    "Determinism: Same input context yields same score."
  ],
  "parameters": [
    {
      "name": "threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Minimum score to pass evaluation"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Judge#mh:SHA-256:95548f9fff8d0106242d8f96a1bdbf9cced2cf153f4a78bf0c8709fc1f82c428",
  "sema_ref": "Judge#9554",
  "sema_stub": "9554",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "yields": {
      "score": "Score#d220"
    },
    "references": {
      "criteria": "Criteria#ef6b",
      "agent": "Agent#35b9",
      "check": "Check#d3e8",
      "validate": "Validate#ebe1"
    },
    "accepts": {
      "scoring_function": "ScoringFunction#3a4e",
      "subject": "Subject#788f"
    }
  }
}
```

---

## Loop#797f

```json
{
  "handle": "Loop",
  "mechanism": "A control flow structure that repeats a sequence of {{work}} until a specific {{condition}} is met. Essential for feedback, learning, and persistent processes.",
  "gloss": "Repeated execution cycle",
  "invariants": [
    "Termination Guarantee: Must have a proven exit condition (or explicit Daemon mode).",
    "Progress: State must change between iterations to avoid infinite freeze."
  ],
  "sema_id": "sema:Loop#mh:SHA-256:797fbd926c1d0fb9c036fd1d1ebcd2e91493390c3554205ab8bb5f6f814a3ae8",
  "sema_ref": "Loop#797f",
  "sema_stub": "797f",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "condition": "Condition#cbd5"
    },
    "composes_with": {
      "work": "Work#d2c6"
    }
  }
}
```

---

## Monitor#feb3

```json
{
  "handle": "Monitor",
  "gloss": "Continuous observation of state over time",
  "mechanism": "A persistent process that uses a {{loop}} to repeatedly execute {{observe}} on a target {{system}} or {{state}} at defined intervals. It compares the observed state against a baseline or invariant, emitting a {{signal}} if a deviation ({{anomaly}}) is detected.",
  "signature": [
    "Loop#797f(State#4d58)"
  ],
  "invariants": [
    "Liveness: Must run continuously or periodically.",
    "Non-Interference: Monitoring should not significantly alter the observed system."
  ],
  "parameters": [
    {
      "name": "interval",
      "type": "Duration",
      "range": "unspecified",
      "description": "Time between observation cycles"
    }
  ],
  "_meta": {
    "tier": 0,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_ref": "Monitor#feb3",
  "sema_id": "sema:Monitor#mh:SHA-256:feb39520f1d3644230f2654b8f92e6034eefb30b8eb59904dade81d76a07a277",
  "sema_stub": "feb3",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314",
      "signal": "Signal#f39d",
      "anomaly": "Anomaly#fac8"
    },
    "composes_with": {
      "observe": "Observe#39f0",
      "loop": "Loop#797f"
    }
  }
}
```

---

## MonitorReport#063c

```json
{
  "handle": "MonitorReport",
  "mechanism": "A telemetry artifact comparing the deployed state against a 'Definition of Done'. Generated to close the feedback loop.",
  "gloss": "Deployment telemetry artifact",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1,
    "related": [
      "Monitor#feb3"
    ]
  },
  "sema_id": "sema:MonitorReport#mh:SHA-256:063cc5c1f90b2e11e3446ddfaec7034ed51acb83432fe11ba2d1e7151ac0d42d",
  "sema_ref": "MonitorReport#063c",
  "sema_stub": "063c",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "data_schema": {
    "type": "object",
    "required": [
      "manifest_ref",
      "metrics"
    ],
    "properties": {
      "manifest_ref": {
        "type": "string",
        "description": "Reference to RolloutManifest"
      },
      "metrics": {
        "type": "object",
        "description": "Observed telemetry data"
      },
      "definition_of_done": {
        "type": "object",
        "description": "Expected success criteria"
      },
      "deviation": {
        "type": "object",
        "description": "Difference from expected state"
      }
    }
  }
}
```

---

## NegativeProof#b130

```json
{
  "handle": "NegativeProof",
  "mechanism": "Proving non-membership in a committed state set. An {{agent}} cryptographically commits to its full state (e.g., via Merkle tree), then uses a Zero-Knowledge Range Proof to demonstrate that a specific {{value}} or datum is NOT present in that committed set, without revealing what the set contains. Operates via exhaustive search over the committed domain, treating verified failure-to-find as proof of absence within that snapshot. The guarantee is bounded: it proves non-membership in the committed tree, not global non-possession\u2014the agent could hold uncommitted state elsewhere.",
  "gloss": "Proving non-membership in a committed state snapshot",
  "failure_modes": [
    "Proving a negative is computationally expensive.",
    "Agent commits incomplete state (hides data outside committed tree)\u2014proof is technically valid but practically meaningless.",
    "Stale commitment: state changed after commitment but before verification."
  ],
  "invariants": [
    "Absence of evidence is evidence of absence (under exhaustive search of committed set)",
    "Search space fully covered within the commitment boundary"
  ],
  "preconditions": [
    "Closed world assumption (over the committed state, not globally)",
    "{{hypothesis}} H",
    "State commitment is fresh and complete"
  ],
  "postconditions": [
    "H proved false within committed state"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1
  },
  "sema_ref": "NegativeProof#b130",
  "sema_id": "sema:NegativeProof#mh:SHA-256:b1309e57068aacefbcf7f15d993a147fae28d1ee83fddb83858bd0d8c789e161",
  "sema_stub": "b130",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#ffa7",
      "value": "Value#3c5d",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Observe#39f0

```json
{
  "handle": "Observe",
  "mechanism": "The process of gathering information from the environment. It involves sensing raw data, filtering it for relevance (Attention), and integrating it into the internal {{context}} and state. Unlike passive reception, Observe is often an active query (e.g., polling an API, reading a file).",
  "gloss": "Active State Perception",
  "failure_modes": [
    "Sensor noise: Input data is corrupted or inaccurate.",
    "Blind Spot: Critical information exists but is outside the agent's observable range.",
    "Information Overload: Too much data prevents effective filtering and integration.",
    "Stale Data: Observing a cached state that no longer reflects reality."
  ],
  "invariants": [
    "Read-Only: Observation must not modify the observed state (Side-effect free).",
    "Truthfulness: The observation must accurately reflect the input signal (no internal distortion)."
  ],
  "preconditions": [
    "Sensors/Tools are active",
    "Actor has attention capacity"
  ],
  "postconditions": [
    "Internal state is updated",
    "New information is available for Thinking"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "related": [
      "Belief#a9ce",
      "Attention"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Observe#mh:SHA-256:39f0bf3256475676557978ed275548604d9c1f247a6a49c242dc69646ddab20c",
  "sema_ref": "Observe#39f0",
  "sema_stub": "39f0",
  "dependencies": {
    "yields": {
      "context": "Context#510a"
    }
  }
}
```

---

## Probe#12d8

```json
{
  "handle": "Probe",
  "mechanism": "An active query that returns verifiable information about system or environment state. Unlike passive observation, a Probe interacts with its target to extract ground truth. It is the primitive mechanism for verification. Probes have cost (resources to execute) and latency (time to return). Stateful probes execute in a {{sandbox}} to prevent production impact.",
  "gloss": "Active verification query",
  "failure_modes": [
    "Observer Effect: Probe changes the state it measures.",
    "Stale Probe: Result reflects past state, not current.",
    "Probe Cost: Verification cost exceeds value of information.",
    "False Positive/Negative: Probe returns incorrect result.",
    "Sandbox Escape: Probe execution affects production state.",
    "Proxy Failure: Passing the quiz does not guarantee performance on the job."
  ],
  "invariants": [
    "Ground Truth: Probe result reflects actual state at time of query.",
    "Repeatability: Same probe on unchanged state returns same result.",
    "Cost Bound: Probe execution must complete within specified resource limits.",
    "Non-Destructive: Production state must remain invariant."
  ],
  "preconditions": [
    "Response timeout defined",
    "Target agent addressable"
  ],
  "postconditions": [
    "No side effects on production target",
    "Probe cost paid",
    "Target capability verified OR timeout"
  ],
  "parameters": [
    {
      "name": "difficulty",
      "type": "Int",
      "range": "[1-5]",
      "description": "Complexity of the verification challenge (1 = trivial, 5 = hard)"
    },
    {
      "name": "timeout_ms",
      "type": "Int",
      "range": "[100, 30000]",
      "description": "Maximum milliseconds to wait for probe response"
    },
    {
      "name": "verification_mode",
      "type": "Enum",
      "range": "{StaticVector, Procedural, Sandbox#e00f, StakedReport}",
      "description": "Method used to verify probe response"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Probe#mh:SHA-256:12d8497f8ef8d8abe3a0bbc02cffe84a184f943e5c6845c06e6456b96e71b602",
  "sema_ref": "Probe#12d8",
  "sema_stub": "12d8",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "sandbox": "Sandbox#e00f"
    }
  }
}
```

---

## Quorum#858e

```json
{
  "handle": "Quorum",
  "mechanism": "A threshold-checking primitive. Validates if a count of {{ballot}} signals exceeds a required number (K). It does not negotiate; it simply counts. Used as a gating function for higher-level protocols.",
  "gloss": "Minimum participation threshold",
  "failure_modes": [
    "Veto threshold tuning is hard - too low enables cheap blocking, too high makes it useless.",
    "Strategic abstention to avoid commitment.",
    "Deadline pressure enables rushing bad proposals through."
  ],
  "invariants": [
    "K cannot decrease mid-vote."
  ],
  "preconditions": [
    "N agents in voting set. K threshold defined where K \u2264 N. Proposal formulated."
  ],
  "postconditions": [
    "Result selected (approve/reject/timeout)",
    "Voting tally recorded"
  ],
  "parameters": [
    {
      "name": "threshold",
      "type": "Float",
      "range": "[0.5, 1.0]",
      "description": "Fraction required for consensus"
    },
    {
      "name": "total_members",
      "type": "Integer",
      "range": "[3, 100]",
      "description": "Size of voting pool"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "related": [
      "LazyConsensus#515b"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Quorum#mh:SHA-256:858ec7b79a5e07103ead4d441239c570dcd8dc8de462ab4d73c9501b99f4687b",
  "sema_ref": "Quorum#858e",
  "sema_stub": "858e",
  "dependencies": {
    "accepts": {
      "ballot": "Ballot#2a0a"
    }
  }
}
```

---

## Sandbox#e00f

```json
{
  "handle": "Sandbox",
  "mechanism": "An isolated execution environment that restricts side effects.",
  "gloss": "Isolation boundary",
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1,
    "related": [
      "AgentSandbox#fc41",
      "CircuitBreaker#4162",
      "SafetyCartographer"
    ],
    "caution": "Escape vectors may exist in unaudited system call surfaces."
  },
  "sema_id": "sema:Sandbox#mh:SHA-256:e00f4eca5e3c4e369bc8109db17aa66835b86e5a65ee16fb07b2f431db3b8638",
  "sema_ref": "Sandbox#e00f",
  "sema_stub": "e00f",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "failure_modes": [
    "Unconstrained vector permits escape from the isolation boundary.",
    "Resource exhaustion within the sandbox affects the enclosing system."
  ]
}
```

---

## Search#c5f4

```json
{
  "handle": "Search",
  "mechanism": "Active scanning of a domain (memory, environment, data) to locate entities that match a {{criteria}}. It iterates through the domain, applying {{check}} to filter candidates.",
  "gloss": "Active retrieval of matching entities",
  "invariants": [
    "Determinism: Same domain + same criteria = same results.",
    "Completeness: Must not silently skip accessible items."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_ref": "Search#c5f4",
  "sema_id": "sema:Search#mh:SHA-256:c5f4bfa7dd8234b80ba9f565d49a882a2c2c5ea7016ed276d65587cfa7e523d5",
  "sema_stub": "c5f4",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## Select#15c2

```json
{
  "handle": "Select",
  "mechanism": "Deterministic Filter. Applies a Predicate Function P(x) to every element in Input Set S. Returns a new Subset S' containing only elements where P(x) is True. It filters a set based on specific inclusion criteria.",
  "gloss": "Generic selection of items from a set based on criteria",
  "failure_modes": [
    "Empty Result: No items satisfy the criterion (returns empty set).",
    "Predicate Error: The criterion function fails or throws an error for specific inputs."
  ],
  "invariants": [
    "Predicate Truth: For all x in Output, Criterion(x) must be True.",
    "Subset Property: Output must be a subset of Input (no new items created).",
    "Determinism: Same input set + same criteria = same output set."
  ],
  "preconditions": [
    "Criterion is decidable for item type",
    "Input set is iterable"
  ],
  "postconditions": [
    "Subset returned"
  ],
  "parameters": [
    {
      "name": "limit",
      "type": "Integer",
      "range": "[1, 10000]",
      "description": "Max items to return"
    },
    {
      "name": "strategy",
      "type": "Enum",
      "range": "{Filter, First, Random}",
      "description": "Default: Filter"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Select#mh:SHA-256:15c257d42d18f33a5a4bdf1ef5ab16712dfd0293cd03ebb28ce746a119f0dfcc",
  "sema_ref": "Select#15c2",
  "sema_stub": "15c2",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## StateSnapshot#b9b8

```json
{
  "handle": "StateSnapshot",
  "mechanism": "Periodic serialization of internal volatile {{state}} to durable storage to enable crash recovery. Unlike distributed checkpoints (which requires consensus), {{snapshot}} is a local or unilateral durability guarantee. It enables 'Resume' functionality. Utilizes {{trace}}, {{idempotent_write}}.",
  "gloss": "Durable persistence of volatile state",
  "invariants": [
    "Atomicity: {{snapshot}} is either fully written or discarded (no partial corruption)",
    "Roundtrip Integrity: Deserialize(Serialize(S)) must equal S"
  ],
  "preconditions": [
    "Serializable {{state}}",
    "Write access to durable storage"
  ],
  "postconditions": [
    "Resume point established"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "signature": [
    "State#4d58(Snapshot#0ae9)"
  ],
  "sema_id": "sema:StateSnapshot#mh:SHA-256:b9b8faad3a629ff61fccc07d6f56e44b6f685b29e6c51080b38dd22438334419",
  "sema_ref": "StateSnapshot#b9b8",
  "sema_stub": "b9b8",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "snapshot": "Snapshot#0ae9",
      "trace": "Trace#9057",
      "state": "State#4d58",
      "idempotent_write": "IdempotentWrite#b959"
    }
  }
}
```

---

## StateTransition#9e61

```json
{
  "handle": "StateTransition",
  "mechanism": "Finite State Machine. A {{transition}} is defined as T: S x Event -> S. Only valid transitions allowed. Current {{state}} determines available actions.",
  "gloss": "Explicit finite-state machine governance",
  "sema_id": "sema:StateTransition#mh:SHA-256:9e61cab1fbacfac92d739865d4505e9e9bb9ed024e0d51b670a00ccfeb801ec4",
  "sema_ref": "StateTransition#9e61",
  "sema_stub": "9e61",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "state": "State#4d58"
    }
  }
}
```

---

## TaskLifecycle#8c7f

```json
{
  "handle": "TaskLifecycle",
  "mechanism": "Explicit {{state_transition}} machine governing {{task}} progression through five states: PENDING (created, awaiting assignment), ASSIGNED (claimed by an {{agent}}), RUNNING (actively executing, emitting {{heartbeat}}), COMPLETED (successfully finished, {{result}} attached), FAILED (terminated with {{exception}}, retry decision required). Each transition requires a typed {{event}}: assign, start, complete, fail, cancel. Invalid transitions are rejected. RUNNING state requires periodic {{heartbeat}}; timeout triggers automatic FAILED transition. The attached {{risk}} profile informs retry and escalation policy on failure.",
  "gloss": "Formal state machine governing task progression",
  "invariants": [
    "Forward-Only: Tasks must not regress (no COMPLETED to RUNNING via {{state_transition}})",
    "Single Owner: Exactly one {{agent}} owns a {{task}} in ASSIGNED or RUNNING state",
    "FAILED tasks must include an {{exception}} describing the failure",
    "RUNNING tasks must emit {{heartbeat}} within configured interval"
  ],
  "preconditions": [
    "{{task}} exists in PENDING state"
  ],
  "postconditions": [
    "{{task}} in terminal state (COMPLETED, FAILED, or CANCELLED)"
  ],
  "failure_modes": [
    "Heartbeat timeout (agent dies silently \u2014 task stuck in RUNNING without timeout enforcement).",
    "State desync (two agents believe they own the same task due to network partition).",
    "Zombie tasks (FAILED tasks never retried or escalated \u2014 accumulate in queue)."
  ],
  "parameters": [
    {
      "name": "heartbeat_interval_seconds",
      "type": "Integer",
      "range": "[5, 300]",
      "description": "Maximum seconds between heartbeats before RUNNING task is marked FAILED"
    }
  ],
  "signature": [
    "StateTransition#9e61(Task#b328)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1,
    "tier": 1,
    "related": []
  },
  "sema_ref": "TaskLifecycle#8c7f",
  "sema_id": "sema:TaskLifecycle#mh:SHA-256:8c7f7470a37f4207e7509eed63e2689285631f62516a3943def1cf15ffb7c852",
  "sema_stub": "8c7f",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "exception": "Exception#66c0",
      "task": "Task#b328",
      "event": "Event#7e71",
      "heartbeat": "Heartbeat#b67a",
      "risk": "Risk#1980",
      "agent": "Agent#35b9"
    },
    "yields": {
      "result": "Result#195b"
    },
    "composes_with": {
      "state_transition": "StateTransition#9e61"
    }
  }
}
```

---

## TimeWarpLog#a0ac

```json
{
  "handle": "TimeWarpLog",
  "mechanism": "Events are not ordered by wall-clock time but by 'causal cones'. An {{agent}} accepts an event from the 'past' if it doesn't contradict its current causal cone. The log's append position is driven by a {{monotonic_counter}} so that once an event is admitted to a cone, no earlier-sequenced event can supersede it. Allows for massive latency tolerance. Utilizes {{world_reversible}}, {{causal_barrier}}.",
  "gloss": "Handling relativistic event ordering",
  "failure_modes": [
    "User confusion about 'when' things happened."
  ],
  "invariants": [
    "Immutability: Past entries cannot be modified",
    "Indexability: Seek(Time T) returns deterministic {{state}}(T)",
    "Causal consistency: Events are accepted only if they do not contradict the current causal cone."
  ],
  "preconditions": [
    "Storage supports append-only writes"
  ],
  "postconditions": [
    "{{system}} state matches T_target"
  ],
  "parameters": [
    {
      "name": "granularity",
      "type": "Duration",
      "range": "[1ms, 1min]",
      "description": "Resolution of time travel"
    },
    {
      "name": "index_strategy",
      "type": "Enum",
      "range": "{Time, Causal, Hybrid}",
      "description": "How to organize history"
    },
    {
      "name": "retention_window",
      "type": "Duration",
      "range": "[1h, 30d]",
      "description": "How far back to retain"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "caution": "Causal cone is only as trustworthy as the identities signing events. Unsigned or weakly-authenticated events can rewrite perceived history."
  },
  "sema_id": "sema:TimeWarpLog#mh:SHA-256:a0ac168c3ecde98a3a649c490f6806a6f03085237d51ec9639250aa00c79d4cd",
  "sema_ref": "TimeWarpLog#a0ac",
  "sema_stub": "a0ac",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314",
      "monotonic_counter": "MonotonicCounter#cf62",
      "agent": "Agent#35b9",
      "world_reversible": "WorldReversible#f664",
      "causal_barrier": "CausalBarrier#3c73"
    }
  }
}
```

---

## ToolInvoke#4694

```json
{
  "handle": "ToolInvoke",
  "mechanism": "The actor emits a structured tool call (function name + arguments), validated by {{input_guard}}, execution is delegated to an external runtime, and the observation (result or error) is fed back into the actor's {{context}}. This is the atomic unit of agent-environment interaction. The pattern enables capabilities beyond text generation: code execution, API calls, file operations, web search.",
  "gloss": "Execute external tool and observe result",
  "failure_modes": [
    "Hallucinated Tools: Actor invokes a tool that doesn't exist.",
    "Argument Mismatch: Tool call has wrong parameter types or missing required fields.",
    "Observation Blindness: Actor ignores or misinterprets tool output."
  ],
  "invariants": [
    "{{context}} Inheritance: Tool Execution {{context}} permissions MUST be <= {{task}} Constraints. Elevation forbidden.",
    "Observation Integration: Result must be incorporated into subsequent reasoning",
    "Sandboxing: Tool execution must respect capability boundaries",
    "Schema Conformance: Tool call must match declared function signature"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "related": [
      "AgentSandbox#fc41"
    ]
  },
  "sema_ref": "ToolInvoke#4694",
  "sema_id": "sema:ToolInvoke#mh:SHA-256:4694e7bcf0e0b712584fc927ea81942e0202a394f80cbc149592c9fdd41013d6",
  "sema_stub": "4694",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "context": "Context#510a"
    },
    "composes_with": {
      "input_guard": "InputGuard#7353"
    }
  }
}
```

---

## Trace#9057

```json
{
  "handle": "Trace",
  "mechanism": "A primitive for Provenance and Lineage. Attaches a chronological history log to a target entity. Every modification to the target appends a new immutable record to its trace, enabling auditability, debugging, and causal reasoning.",
  "gloss": "Record the lineage or provenance of a target",
  "failure_modes": [
    "Trace pollution (too many traces, signal lost in noise).",
    "{{decay}} mismatch (too fast = lost, too slow = stale).",
    "Namespace collision (unrelated actors confuse each other).",
    "No accountability (cannot attribute trace to actor).",
    "Semantic ambiguity (actors interpret same trace differently).",
    "Feedback loops (reinforce bad traces, converge to local minimum)."
  ],
  "invariants": [
    "Causality: Events must be logged in monotonic order.",
    "Immutability: History cannot be rewritten, only appended to."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Trace#mh:SHA-256:90570af650f6362c2a0d7e94b23ed3cfe2c7406f3bd22352dc73582bfdbb3c3d",
  "sema_ref": "Trace#9057",
  "sema_stub": "9057",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4"
    }
  }
}
```

---

## Warmup#92b2

```json
{
  "handle": "Warmup",
  "mechanism": "Gradual Capacity Ramp: On activation, start at reduced capacity C_min and increase to C_max over time T following a defined curve. Prevents 'thundering herd' overload on cold systems. Utilizes {{greet}}, {{throttle}}.",
  "gloss": "Gradual capacity increase to stabilize cold systems",
  "failure_modes": [
    "Premature Load: Traffic arrives before warmup completes.",
    "False Warmth: Timer completes but internal state (e.g.",
    "cache) is still cold."
  ],
  "invariants": [
    "Capacity Limit: Accepted_Load <= Current_Warmup_Cap(t)"
  ],
  "preconditions": [
    "{{system}} state is inactive or reset"
  ],
  "postconditions": [
    "Capacity limit equals C_max",
    "{{system}} state is active"
  ],
  "parameters": [
    {
      "name": "curve",
      "type": "Enum",
      "range": "{Linear, Exponential, Step#5f22}",
      "description": "Default: Linear"
    },
    {
      "name": "initial_capacity",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Starting capacity as fraction of full (0 = cold start)"
    },
    {
      "name": "ramp_duration",
      "type": "Duration",
      "range": "[10s, 1h]",
      "description": "Time to reach full capacity from initial"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Warmup#mh:SHA-256:92b2edac4a9801604e76f19b1a8d22b954fa2394f1e0d4285d1686221558ca5e",
  "sema_ref": "Warmup#92b2",
  "sema_stub": "92b2",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "throttle": "Throttle#2175",
      "greet": "Greet#bbae",
      "system": "System#e314"
    }
  }
}
```

---

## AuditTrail#c891

```json
{
  "handle": "AuditTrail",
  "mechanism": "Every consequential {{agent}} action (state mutation, external call, delegation, decision) appends a {{sign}}ed entry to an immutable {{ledger}} whose sequence number advances via {{monotonic_counter}}, so no entry can be wedged between two existing ones. Each entry contains: timestamp, {{agent}} {{identity}}, action type, input hash, output hash, and the sema pattern invoked. Extends {{trace}} from single-entity lineage to cross-agent compliance logging. The trail is append-only \u2014 entries cannot be modified or deleted. For cross-agent auditing, individual trails are aggregated via Merkle roots into a shared {{snapshot}}, enabling any party to verify the complete history without accessing raw entries.",
  "gloss": "Immutable append-only log of agent actions for compliance and debugging",
  "invariants": [
    "Append-Only: No entry in the {{ledger}} may be modified after creation",
    "Every entry must be {{sign}}ed by the acting {{agent}}",
    "{{trace}} provenance must link each entry to the sema pattern that triggered it"
  ],
  "preconditions": [
    "{{agent}} has established {{identity}}",
    "{{ledger}} is accessible and writable"
  ],
  "postconditions": [
    "Action recorded with full provenance in {{ledger}}",
    "{{snapshot}} of trail Merkle root available for external verification"
  ],
  "failure_modes": [
    "Storage exhaustion (unbounded trail growth in long-running systems).",
    "Clock skew (distributed agents disagree on timestamps \u2014 use logical clocks).",
    "Selective logging (agent omits inconvenient entries \u2014 requires external {{audit}})."
  ],
  "signature": [
    "Trace#9057(Ledger#b5fe)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1,
    "tier": 1,
    "related": [
      "SpotAudit#000e"
    ]
  },
  "sema_ref": "AuditTrail#c891",
  "sema_id": "sema:AuditTrail#mh:SHA-256:c89113de796b35d71144525b03f866e7f5503ff7e908828a3af9de1f4f880526",
  "sema_stub": "c891",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "dependencies": {
    "references": {
      "audit": "Audit#6888",
      "identity": "Identity#626c",
      "trace": "Trace#9057",
      "monotonic_counter": "MonotonicCounter#cf62",
      "agent": "Agent#35b9",
      "ledger": "Ledger#b5fe",
      "sign": "Sign#1fb9"
    },
    "composes_with": {
      "snapshot": "Snapshot#0ae9"
    }
  }
}
```

---

## CompatibilityCheck#3abb

```json
{
  "handle": "CompatibilityCheck",
  "mechanism": "A binary verification process that compares the definition hashes or schema of two entities (agents, {{artifact}}s, or protocols) to determine if they can interact without translation.",
  "gloss": "Schema compatibility verification",
  "invariants": [
    "Determinism: Identical inputs always yield the same compatibility result.",
    "Symmetry: If A is compatible with B, B is compatible with A."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 0
  },
  "sema_ref": "CompatibilityCheck#3abb",
  "sema_id": "sema:CompatibilityCheck#mh:SHA-256:3abb595523dc765c8ebe497169cd2c12494c93a85e50c8785577cef22c465554",
  "sema_stub": "3abb",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## ExplainBeacon#ab3f

```json
{
  "handle": "ExplainBeacon",
  "mechanism": "Telemetry {{stream}}. Emits a human-readable narrative ('I am doing X because Y') alongside the machine-readable log. Must be emitted before irreversible actions. It piggybacks on the {{greet}} or {{heartbeat}} channel to broadcast intent logs to observers.",
  "gloss": "Real-time readable intent broadcasting",
  "failure_modes": [
    "Beacon Drift: The explanation diverges from the actual code execution (the {{agent}} says I am sleeping while deleting files)."
  ],
  "invariants": [
    "Beacon cannot be suppressed."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1
  },
  "sema_id": "sema:ExplainBeacon#mh:SHA-256:ab3fda0493d137c8d5254513b4df5143869042a2db3f4970682b6de823bfb215",
  "sema_ref": "ExplainBeacon#ab3f",
  "sema_stub": "ab3f",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "dependencies": {
    "references": {
      "agent": "Agent#35b9",
      "stream": "Stream#22f3",
      "greet": "Greet#bbae",
      "heartbeat": "Heartbeat#b67a"
    }
  }
}
```

---

## HumanApprove#2b91

```json
{
  "handle": "HumanApprove",
  "mechanism": "A checkpoint gate where execution pauses and awaits explicit human approval before proceeding. The agent presents its proposed {{task}}, rationale, and risk assessment to a human operator. Only upon receiving affirmative consent does execution continue. Critical for high-stakes actions (financial transactions, deployments, irreversible changes).",
  "gloss": "Pause for human approval before critical actions",
  "parameters": [
    {
      "name": "challenge_required",
      "type": "Boolean#2e6b",
      "range": "unspecified",
      "description": "Default: True"
    },
    {
      "name": "timeout",
      "type": "Duration",
      "range": "unspecified",
      "description": "Maximum wait time for human response before escalation"
    }
  ],
  "failure_modes": [
    "Approval Fatigue: Humans rubber-stamp requests without review due to high volume.",
    "Blocking: {{system}} halts indefinitely if human is unavailable.",
    "{{context}} Loss: Human lacks sufficient context to make informed decision."
  ],
  "invariants": [
    "Cognitive Friction: Approval requires matching a context-specific challenge code.",
    "{{audit}} Trail: All approvals/rejections logged with timestamp and rationale",
    "Blocking: Execution MUST halt until approval received",
    "Timeout Policy: Define behavior if approval not received within SLA"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1,
    "caution": "Bypassing removes the human-in-the-loop safety boundary."
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "sema_id": "sema:HumanApprove#mh:SHA-256:2b91e79b05b4e0dbb26a5da14121cf8f41f45c8bf64d6bee9e8cb0a243ba5b51",
  "sema_ref": "HumanApprove#2b91",
  "sema_stub": "2b91",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    },
    "references": {
      "audit": "Audit#6888",
      "system": "System#e314",
      "context": "Context#510a"
    }
  }
}
```

---

## InputGuard#7353

```json
{
  "handle": "InputGuard",
  "mechanism": "A validation filter that sanitizes inputs before they reach a sensitive component. It enforces schema compliance, type safety, and constraint satisfaction. Upon violation, it triggers a fail-closed behavior, rejecting the input and logging the attempt.",
  "gloss": "Input validation and sanitization",
  "failure_modes": [
    "Bypass via unexpected encoding or type coercion.",
    "Overly permissive schema allows malformed input through."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 0,
    "caution": "Validation boundary \u2014 bypass enables injection or unexpected state."
  },
  "sema_ref": "InputGuard#7353",
  "sema_id": "sema:InputGuard#mh:SHA-256:7353542b505beb1db87ba1adf08ecc5cf24112e70c325eef336e3d13654ea533",
  "sema_stub": "7353",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6"
}
```

---

## OathBind#a708

```json
{
  "handle": "OathBind",
  "mechanism": "An automated binding mechanism where an {{actor}} cryptographically commits to a {{rule_set}}. This creates a self-enforcing constraint where deviation triggers an automatic penalty (defined in the rules) via {{spot_audit}}.",
  "gloss": "Pre-commitment to penalties",
  "invariants": [
    "Automated Justice: Penalty execution depends solely on cryptographic evidence.",
    "Immutability: Rules cannot be changed after signing."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1,
    "caution": "Automated penalties \u2014 misconfigured rules cause cascading harm."
  },
  "sema_ref": "OathBind#a708",
  "sema_id": "sema:OathBind#mh:SHA-256:a7082358e67b331a94538ee2f9c99c8fa4690ca7d529c33bae199457f8a5a7da",
  "sema_stub": "a708",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "failure_modes": [
    "Penalty severity decoupled from deviation severity.",
    "Rule set ambiguity triggers unintended penalty."
  ],
  "dependencies": {
    "references": {
      "spot_audit": "SpotAudit#000e",
      "actor": "Actor#6926",
      "rule_set": "RuleSet#7738"
    }
  }
}
```

---

## OutputGuard#1f50

```json
{
  "handle": "OutputGuard",
  "mechanism": "Post-generation content filter. Scans candidate {{solution}} against PII patterns and Toxicity Classifiers. If Score > Threshold, triggers mitigation (Redact/Reject). It mirrors the logic of input guard but applied to egress traffic, scanning for leakage or toxicity.",
  "gloss": "Final egress filter for safety and privacy",
  "failure_modes": [
    "Scunthorpe {{problem}}: Over-censorship blocking valid words containing restricted substrings.",
    "{{context}} Blindness: Guard blocks necessary medical terms misclassified as toxicity.",
    "Redaction Leak: [REDACTED] markers revealing the location/length of hidden secrets."
  ],
  "invariants": [
    "Fail-Safe: If Scanner fails (timeout/error), Output is BLOCKED (not passed).",
    "Privacy First: If PII detected, Redaction is mandatory."
  ],
  "preconditions": [
    "Candidate solution generated",
    "Safety policies active"
  ],
  "postconditions": [
    "Safe output delivered OR Block signal returned"
  ],
  "parameters": [
    {
      "name": "pii_mode",
      "type": "Enum",
      "range": "{Redact, Block, Hash}",
      "description": "Default: Redact"
    },
    {
      "name": "scan_timeout",
      "type": "Duration",
      "range": "unspecified",
      "description": "Default: 500ms"
    },
    {
      "name": "toxicity_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Default: 0.8"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "sema_id": "sema:OutputGuard#mh:SHA-256:1f50ee469c636e44cf3917a31ab3e6295f2a02eb93bb9b8eb8e64398ec3a0c68",
  "sema_ref": "OutputGuard#1f50",
  "sema_stub": "1f50",
  "dependencies": {
    "accepts": {
      "solution": "Solution#fcea"
    },
    "references": {
      "problem": "Problem#4576",
      "context": "Context#510a"
    }
  }
}
```

---

## SpotAudit#000e

```json
{
  "handle": "SpotAudit",
  "mechanism": "A probabilistic audit where a verifier requests a random sample of an agent's internal memory or logs. The agent must provide a Merkle proof for that specific slice. Keeps agents honest without full audits. Utilizes {{state_audit}}.",
  "gloss": "Random sampling of internal state",
  "failure_modes": [
    "Privacy leakage from the sample."
  ],
  "invariants": [
    "Randomness: {{audit}} target must be selected via VRF",
    "Response Time: Proof must be returned within T_max"
  ],
  "preconditions": [
    "Auditor has authority key"
  ],
  "postconditions": [
    "{{audit}} result published to ledger"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1
  },
  "sema_id": "sema:SpotAudit#mh:SHA-256:000ed33bc0676411521d703253810082f4a6a470818e194e833eca8605859ea8",
  "sema_ref": "SpotAudit#000e",
  "sema_stub": "000e",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "dependencies": {
    "references": {
      "audit": "Audit#6888",
      "state_audit": "StateAudit#8195"
    }
  }
}
```

---

## Validate#ebe1

```json
{
  "handle": "Validate",
  "mechanism": "Syntactic Verification. Checks if a data artifact conforms to a predefined structure (Schema) or set of constraints. Yields a {{boolean}} \u2014 strict pass/fail with no middle ground, unlike {{check}} which yields the richer Status (Verified/Falsified/Unknown). Rejects malformed inputs before processing. Utilizes {{accept_spec}}. Distinct from {{check}} (richer truth-valued) and quality scoring (Judge, which yields a continuous Score).",
  "gloss": "Verifying inputs conform to expected schema",
  "failure_modes": [
    "Validator Bypass: Attacker finds encoding that passes validation but exploits downstream parser."
  ],
  "invariants": [
    "Binary Result: Pass or Fail.",
    "Side-Effect Free: Validation must not alter the payload."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1
  },
  "sema_id": "sema:Validate#mh:SHA-256:ebe1118928513083360bcfc973a9fc6c6b2c50ea1d45dc0639b390bc9e20cfc9",
  "sema_ref": "Validate#ebe1",
  "sema_stub": "ebe1",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#19d6",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "accept_spec": "AcceptSpec#7caa"
    },
    "yields": {
      "boolean": "Boolean#2e6b"
    }
  }
}
```

---

# Layer: Mind

## BaseRateInclude#aa0b

```json
{
  "handle": "BaseRateInclude",
  "mechanism": "Prior Probability Anchor: Before evaluating specific case, ask: \"How often does this happen in general?\" Start with base rate. Adjust for specific evidence. Vivid details don't change base rates. \"This startup feels special\" doesn't change 90% failure rate.",
  "gloss": "Outside view over inside view",
  "failure_modes": [
    "Reference Class Tennis: Gaming the output by cherry-picking a favorable reference class."
  ],
  "invariants": [
    "Base rate source must be reference class relevant",
    "Posterior probability must respect prior base rate"
  ],
  "preconditions": [
    "General population statistics",
    "Specific case evidence"
  ],
  "postconditions": [
    "Probability estimate adjusted towards mean"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "related": [
      "BayesUpdate#13f8"
    ],
    "ring": 2
  },
  "sema_id": "sema:BaseRateInclude#mh:SHA-256:aa0b8b4d62885496dfbe0caffc5def9e15fb9fee63d787918bce4be8593f0916",
  "sema_ref": "BaseRateInclude#aa0b",
  "sema_stub": "aa0b",
  "sema_layer": "Mind",
  "sema_category": "Inference"
}
```

---

## BayesUpdate#13f8

```json
{
  "handle": "BayesUpdate",
  "mechanism": "Likelihood Weighting: Hold prior probability P(H). {{observe}} evidence E. Compute likelihood ratio P(E|H)/P(E|\u00acH). Multiply prior by ratio to get posterior. Large ratio = strong update. Ratio near 1 = weak evidence. Never update to 0 or 1. It explicitly incorporates {{base_rate_include}} into the prior probability calculation to prevent base-rate neglect.",
  "gloss": "Mathematically rigorous belief revision",
  "failure_modes": [
    "Prior Dogmatism: Setting a prior of 1.0 or 0.0 prevents any future updating, regardless of evidence."
  ],
  "invariants": [
    "Posterior \u2208 (0,1): never update to absolute certainty."
  ],
  "preconditions": [
    "Prior probability defined in (0,1). New evidence observed. Likelihood computable."
  ],
  "postconditions": [
    "Posterior probability in (0,1). {{belief}} updated proportional to evidence strength. Prior recoverable given likelihood."
  ],
  "parameters": [
    {
      "name": "prior_confidence",
      "type": "Probability#356b",
      "range": "[0.1, 0.9]",
      "description": "Certainty in prior belief before evidence"
    },
    {
      "name": "update_threshold",
      "type": "Probability#356b",
      "range": "[0.6, 0.95]",
      "description": "Minimum confidence shift to trigger action"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:BayesUpdate#mh:SHA-256:13f8d0e6f00298f5e49187afdf1f8733638f3b222cdcb9361b1d7dd5ae07c67b",
  "sema_ref": "BayesUpdate#13f8",
  "sema_stub": "13f8",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "base_rate_include": "BaseRateInclude#aa0b",
      "observe": "Observe#39f0",
      "belief": "Belief#a9ce"
    }
  }
}
```

---

## BreadthGovernor#87f0

```json
{
  "handle": "BreadthGovernor",
  "mechanism": "{{parsimony}}-Bounded Expansion. Limits the maximum number of parallel branches (fan-out) at any single node. Prioritizes branches by 'Distinctness' and 'Expected {{value}}'. If Candidates > Max_Breadth, applies Truncation (Top-K) or Clustering (merge similar branches). It enforces limits defined by {{budget}} during the {{decompose}} phase, often employing {{prophet_fan_out}} to pre-score and prune branches.",
  "gloss": "Structural limit on parallel execution (Fan-out)",
  "failure_modes": [
    "Fork Bomb: Unchecked decomposition creates exponential agent explosion.",
    "Choice Overload: Too many weak hypotheses dilute the quality of the best ones.",
    "{{context}} Fragmentation: Parent agent cannot integrate results from N > 7 children."
  ],
  "invariants": [
    "Distinctness: {{parallel}} branches must be semantically orthogonal (cosine_sim < 0.8).",
    "Miller's Law: Active sub-tasks should rarely exceed 7 +/- 2."
  ],
  "preconditions": [
    "Candidate list generated",
    "Decomposition request received"
  ],
  "postconditions": [
    "Candidate list truncated to <= max_breadth"
  ],
  "parameters": [
    {
      "name": "max_breadth",
      "type": "Integer",
      "range": "[3, 10]",
      "description": "Default: 5"
    },
    {
      "name": "selection_strategy",
      "type": "Enum",
      "range": "{TopK, Cluster, Random}",
      "description": "Default: TopK"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:BreadthGovernor#mh:SHA-256:87f09510bdc6b22a48495ca89520be7645976237ec69906fa342e912d4867eff",
  "sema_ref": "BreadthGovernor#87f0",
  "sema_stub": "87f0",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "context": "Context#510a",
      "parsimony": "Parsimony#8476",
      "prophet_fan_out": "ProphetFanOut#85a9",
      "parallel": "Parallel#3181",
      "value": "Value#3c5d",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## ConfidenceCalibrate#ba8b

```json
{
  "handle": "ConfidenceCalibrate",
  "mechanism": "Track Record Alignment: For claims rated 70% confident, ~70% should be true. Track predictions vs outcomes. If 90% claims are right only 60% of time, you are overconfident\u2014widen uncertainty. If 90% claims are right 99% of time, you are underconfident\u2014tighten. It adjusts the internal probability model using {{bayes_update}} on historical accuracy data, ensuring {{base_rate_include}} is respected.",
  "gloss": "Aligning subjective confidence with objective frequency",
  "failure_modes": [
    "Over-correction: {{agent}} becomes under-confident to avoid being wrong, refusing to act on strong signals."
  ],
  "invariants": [
    "Calibration curve must be monotonic."
  ],
  "parameters": [
    {
      "name": "bin_count",
      "type": "Integer",
      "range": "[5, 20]",
      "description": "Resolution of calibration measurement"
    },
    {
      "name": "calibration_target",
      "type": "Float",
      "range": "[0.02, 0.15]",
      "description": "Max expected calibration error, ECE"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:ConfidenceCalibrate#mh:SHA-256:ba8bd9f417af19c3e8917307ec861d0d2a22fa8e700b37003f9552886c257bce",
  "sema_ref": "ConfidenceCalibrate#ba8b",
  "sema_stub": "ba8b",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "base_rate_include": "BaseRateInclude#aa0b",
      "bayes_update": "BayesUpdate#13f8",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## ConfirmationBlock#20db

```json
{
  "handle": "ConfirmationBlock",
  "mechanism": "Disconfirmation Seek: After forming hypothesis, ask: \"What evidence would prove me WRONG?\" Actively search for that evidence. Weight disconfirming evidence fairly (don't explain it away). If you can't imagine what would change your mind, belief is not rational. It enforces a pause state until active search has exhausted reasonable counter-evidence.",
  "gloss": "Active search for contradictory evidence",
  "failure_modes": [
    "Performative Doubt: Generating weak counter-evidence just to tick the box, without genuine intent to falsify."
  ],
  "invariants": [
    "Evidence must be independently verifiable."
  ],
  "parameters": [
    {
      "name": "disconfirmations_required",
      "type": "Integer",
      "range": "[1, 100]",
      "description": "Counter-evidence instances required before the block releases. The pattern's mechanism actively seeks disconfirming evidence; this parameter names the threshold accordingly."
    },
    {
      "name": "timeout",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Max wait for confirmations"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 0,
    "related": [
      "DissentSeek#0ebe"
    ]
  },
  "sema_id": "sema:ConfirmationBlock#mh:SHA-256:20db49e59b1e91b692635885522c55205d7889ddad978c36965d00a4fc985a5a",
  "sema_ref": "ConfirmationBlock#20db",
  "sema_stub": "20db",
  "sema_layer": "Mind",
  "sema_category": "Inference"
}
```

---

## ContextFirst#def7

```json
{
  "handle": "ContextFirst",
  "mechanism": "Operational Invariant. {{prioritize}} the {{context}}. Before generating tokens or taking action, {{agent}} MUST execute a Read operation (e.g., graph_skeleton, search) on the shared state. Blind action is forbidden. It is a mandate for {{solver_node}} to execute a {{warmup}} or read-cycle before attempting any write-action.",
  "gloss": "Load state before acting",
  "failure_modes": [
    "{{context}} Blindness: {{agent}} acts on stale cached data.",
    "Hallucinated {{state}}: {{agent}} guesses the state instead of looking it up."
  ],
  "invariants": [
    "Read-Before-Write: Action timestamp > Context_Refresh timestamp."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 0
  },
  "sema_id": "sema:ContextFirst#mh:SHA-256:def73ba90ba708f17c262a496bc505797e119d64270f985e5e51f0ce528bc987",
  "sema_ref": "ContextFirst#def7",
  "sema_stub": "def7",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Prioritize#68f8(Context#510a)"
  ],
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "context": "Context#510a",
      "warmup": "Warmup#92b2",
      "agent": "Agent#35b9",
      "prioritize": "Prioritize#68f8",
      "solver_node": "SolverNode#26b1"
    }
  }
}
```

---

## EpistemicCalibrate#6069

```json
{
  "handle": "EpistemicCalibrate",
  "mechanism": "Enforces a decay function on confidence as the prediction horizon increases. Unlike human intuition which maintains high confidence to signal status, this pattern forces the agent's reported certainty to mathematically degrade over time (T).",
  "gloss": "Structural confidence degradation",
  "failure_modes": [
    "Paralysis (confidence drops to zero too fast)."
  ],
  "invariants": [
    "Horizon {{decay}}: Confidence(T+1) < Confidence(T)",
    "Unknown Unknowns: A reserved probability mass for 'Unmodeled Event'"
  ],
  "preconditions": [
    "Base prediction available"
  ],
  "postconditions": [
    "Confidence score adjusted downward"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "related": [
      "ConfidenceCalibrate#ba8b"
    ],
    "ring": 2
  },
  "sema_id": "sema:EpistemicCalibrate#mh:SHA-256:606941a7d67ed0f304f44966e00550480d1ff04f64c8196cf6fe15185a9ef437",
  "sema_ref": "EpistemicCalibrate#6069",
  "sema_stub": "6069",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4"
    }
  }
}
```

---

## HackDetect#1eca

```json
{
  "handle": "HackDetect",
  "mechanism": "A meta-check that detects when an agent is solving for 'make it work' instead of 'do it right'. Triggered when the agent modifies interface code (adapters, exporters, validators) rather than fixing source data or upstream logic. The hack appears to succeed locally but breaks invariants that downstream systems depend on, creating negative externalities. It monitors the {{input_guard}} layer for anomalies, triggering {{ejection_seat}} if the agent attempts to bypass invariants via code patching.",
  "gloss": "Detect shortcuts that break downstream invariants",
  "failure_modes": [
    "False Positives: Legitimate adapter changes flagged as hacks.",
    "Hack Blindness: Novel hack patterns evade detection.",
    "Justification Theater: {{agent}} rationalizes hack as 'pragmatic'."
  ],
  "invariants": [
    "Detection triggers defensive response",
    "False positive rate minimized"
  ],
  "preconditions": [
    "Attack signatures/anomaly detection",
    "{{system}} monitoring"
  ],
  "postconditions": [
    "Alert raised",
    "Intrusion identified"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:HackDetect#mh:SHA-256:1ecaa4bb2a72d22dc146f6a8a8ba8f4d38678acf78bf176058c0d779525b44f3",
  "sema_ref": "HackDetect#1eca",
  "sema_stub": "1eca",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "ejection_seat": "EjectionSeat#d53e",
      "agent": "Agent#35b9",
      "system": "System#e314",
      "input_guard": "InputGuard#7353"
    }
  }
}
```

---

## HindsightBlock#4cc8

```json
{
  "handle": "HindsightBlock",
  "mechanism": "{{decision}}-Time Evaluation: When evaluating past decision, reconstruct information available AT DECISION TIME. {{judge}} decision quality by expected value given that information, not by outcome. Good decisions can have bad outcomes. Bad decisions can have good outcomes. It mirrors {{pre_mortem}} logic after the fact, reconstructing the ex-ante probability space to judge decision quality independent of outcome.",
  "gloss": "Preventing results-oriented thinking",
  "failure_modes": [
    "{{outcome}} Blindness: Ignoring outcomes entirely prevents learning from black swans or model errors."
  ],
  "invariants": [
    "No Revision: Log is immutable",
    "Prior Commitment: Prediction(T) must be cryptographically committed before {{outcome}}(T+delta)"
  ],
  "preconditions": [
    "Prediction registry active"
  ],
  "parameters": [
    {
      "name": "lookback_window",
      "type": "Duration",
      "range": "[1min, 24h]",
      "description": "How far back to evaluate"
    },
    {
      "name": "regret_threshold",
      "type": "Float",
      "range": "[0.0, 0.5]",
      "description": "Max acceptable regret score"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:HindsightBlock#mh:SHA-256:4cc8834994870224daeb4d912c810b9cf50aea0cddfd3d2d774282a3abf516e0",
  "sema_ref": "HindsightBlock#4cc8",
  "sema_stub": "4cc8",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "decision": "Decision#acfb",
      "pre_mortem": "PreMortem#142a",
      "judge": "Judge#9554",
      "outcome": "Outcome#144c"
    }
  }
}
```

---

## LayeredCheck#76d6

```json
{
  "handle": "LayeredCheck",
  "mechanism": "A {{check}} strategy that evaluates constraints in a strict {{hierarchy}} of abstraction (e.g., existence -> {{validate}} (schema) -> {{understand}} (semantics)). It uses a {{sequence}} of {{gate}}s where lower-level failures halt execution immediately, preventing resource waste on higher-level checks for fundamentally broken inputs.",
  "gloss": "Hierarchical verification strategy",
  "signature": [
    "Check#d3e8(Hierarchy#d530)"
  ],
  "invariants": [
    "Fail-Fast: If Layer(N) fails, Layer(N+1) is NOT executed.",
    "Hierarchy Obedience: Checks are strictly ordered by abstraction level."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Inference",
    "ring": 2,
    "tier": 2,
    "related": [
      "PURECheck#f2f0"
    ]
  },
  "sema_ref": "LayeredCheck#76d6",
  "sema_id": "sema:LayeredCheck#mh:SHA-256:76d62f3bf0821dca24f45fddde8e892eb2bc29c2182d91cfb5308a3defe01d60",
  "sema_stub": "76d6",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "check": "Check#d3e8",
      "gate": "Gate#89fd"
    },
    "references": {
      "understand": "Understand#96d4",
      "hierarchy": "Hierarchy#d530",
      "validate": "Validate#ebe1"
    }
  }
}
```

---

## NormCheck#9bdd

```json
{
  "handle": "NormCheck",
  "mechanism": "A {{check}} filter that scans the Prophet's descriptive output for normative adjectives (e.g., 'dangerous', 'unfortunate', 'unfair') that masquerade as objective facts. It forces a rewrite to strip these biases, ensuring the separation of Is (Prophet) and Ought ({{judge}} of {{value}}). Utilizes {{quorum}}, {{prophet_fan_out}}, {{normative_judge}}.",
  "gloss": "Detection of value-laden facts",
  "failure_modes": [
    "Strips relevant safety warnings that were actually factual."
  ],
  "invariants": [
    "Fact Preservation: Rewritten text must preserve all causal claims",
    "Neutral Tone: Count(NormativeAdjectives) == 0"
  ],
  "preconditions": [
    "Text claims to be descriptive"
  ],
  "postconditions": [
    "Text certified neutral"
  ],
  "parameters": [
    {
      "name": "action_on_detect",
      "type": "Enum",
      "range": "{Flag, Rewrite, Reject}",
      "description": "Response to smuggled norms"
    },
    {
      "name": "sensitivity",
      "type": "Enum",
      "range": "{Low, Medium, High, Paranoid}",
      "description": "Detection threshold"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:NormCheck#mh:SHA-256:9bdd458491fbb7b55409c023d3a8d0c8b45125dda7dc2901efb68dc7c76f9c3c",
  "sema_ref": "NormCheck#9bdd",
  "sema_stub": "9bdd",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Check#d3e8(Value#3c5d)"
  ],
  "dependencies": {
    "references": {
      "quorum": "Quorum#858e",
      "normative_judge": "NormativeJudge#2c8c",
      "prophet_fan_out": "ProphetFanOut#85a9",
      "judge": "Judge#9554",
      "check": "Check#d3e8",
      "value": "Value#3c5d"
    }
  }
}
```

---

## NormativeJudge#2c8c

```json
{
  "handle": "NormativeJudge",
  "mechanism": "A purely normative {{judge}} module that evaluates static world-states against a weighted {{value}} function. The caller supplies the {{weights}} that shape the value function, so preference structure is visible to the evaluator rather than hidden inside it. To mitigate Goodhart's Law, this pattern should be deployed as an ENSEMBLE (Jury), where multiple judges with slightly perturbed {{value}} constitutions reach {{quorum}} on the {{outcome}}. It aggregates {{value}}s via {{perspective_ensemble}}, optionally escalating to {{human_approve}} for ambiguous edge cases.",
  "gloss": "Value-based state evaluation",
  "failure_modes": [
    "Goodhart's Law (optimizing for the metric, not the intent).",
    "Collusion between Proposer and {{judge}}."
  ],
  "invariants": [
    "Explicit Weights: Trade-offs between values must be logged",
    "{{outcome}} Focus: Evaluation is f({{state}}), not f(Action)"
  ],
  "preconditions": [
    "{{state}} S_prime is descriptively complete"
  ],
  "postconditions": [
    "Normative verdict rendered"
  ],
  "parameters": [
    {
      "name": "consensus_threshold",
      "type": "Float",
      "range": "[0.5, 1.0]",
      "description": "Required agreement for Jury"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 0
  },
  "sema_id": "sema:NormativeJudge#mh:SHA-256:2c8ca6cd8166a26b258ae67dc5df2dc1dc968f15f6edce6225b5c1615784b667",
  "sema_ref": "NormativeJudge#2c8c",
  "sema_stub": "2c8c",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Judge#9554(Value#3c5d)"
  ],
  "dependencies": {
    "accepts": {
      "vector": "Vector#c7c4"
    },
    "references": {
      "state": "State#4d58",
      "outcome": "Outcome#144c",
      "quorum": "Quorum#858e",
      "judge": "Judge#9554",
      "value": "Value#3c5d",
      "human_approve": "HumanApprove#2b91"
    },
    "composes_with": {
      "perspective_ensemble": "PerspectiveEnsemble#d08c"
    }
  }
}
```

---

## OntologyAdapt#4c47

```json
{
  "handle": "OntologyAdapt",
  "mechanism": "Derived from Piagetian psychology. When new data defies classification within the current ontology, the {{agent}} does not force-fit it or discard it. Instead, it triggers a 'Restructure' event, creating new root {{category}}s that accommodate the {{anomaly}} as a fundamental feature. Utilizes {{ontology_handshake}}.",
  "gloss": "Restructuring categories to fit data",
  "failure_modes": [
    "{{category}} explosion (creating a new {{category}} for every {{noise}} point)."
  ],
  "invariants": [
    "Conservation of Data: No anomaly is discarded during accommodation",
    "Fit Threshold: If ClassificationConfidence < 0.4, Trigger(Restructure)"
  ],
  "preconditions": [
    "Data validated as true but unclassifiable"
  ],
  "postconditions": [
    "Data fits naturally in new structure"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 1
  },
  "sema_id": "sema:OntologyAdapt#mh:SHA-256:4c47e0f79019b4299cb3ee8f3df1fb16c94b96a0148d7809d771109ed67ef59f",
  "sema_ref": "OntologyAdapt#4c47",
  "sema_stub": "4c47",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "noise": "Noise#d631",
      "ontology_handshake": "OntologyHandshake#46dc",
      "agent": "Agent#35b9",
      "category": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1",
      "anomaly": "Anomaly#fac8"
    }
  }
}
```

---

## ProphetFanOut#85a9

```json
{
  "handle": "ProphetFanOut",
  "mechanism": "A purely descriptive module that utilizes computational abundance to generate multiple branching future timelines resulting from a proposed action. Unlike standard {{chain}}-of-Thought which follows one likely path (mimicking human laziness), the Prophet forces exploration of low-probability but high-impact tails. It feeds into {{quorum}} by generating the diverse timeline candidates required for the {{aggregate}}.",
  "gloss": "High-fanout causal simulation",
  "failure_modes": [
    "Fan-out explosion (generating too many irrelevant futures)."
  ],
  "invariants": [
    "Descriptive Only: Output must contain zero normative judgment",
    "Diversity: Entropy(Timelines) > Threshold (Must explore distinct futures)"
  ],
  "preconditions": [
    "Action A is well-defined"
  ],
  "postconditions": [
    "At least 3 distinct futures generated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 1
  },
  "sema_id": "sema:ProphetFanOut#mh:SHA-256:85a962e679be621083e2f1f7e4797462353f411f4c96a0dba630f674b199007b",
  "sema_ref": "ProphetFanOut#85a9",
  "sema_stub": "85a9",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "chain": "Chain#711e",
      "aggregate": "Aggregate#7912",
      "quorum": "Quorum#858e"
    }
  }
}
```

---

## RegimeSense#086e

```json
{
  "handle": "RegimeSense",
  "mechanism": "An anomaly detector that continuously tracks divergence between the agent's internal model predictions and observed reality. It calculates a Regime Stability Score (RSS) as the rolling average of prediction accuracy over a window. High surprisal (low accuracy) indicates regime instability. When RSS drops below threshold, it signals that the underlying generative process has changed and triggers OntologicalAccommodation. It continuously monitors prediction error via {{drift_watch}}, triggering {{ontology_adapt}} or {{quorum}} if the error signal crosses the regime-change threshold.",
  "gloss": "Detecting structural breaks in reality",
  "failure_modes": [
    "False Positives: {{noise}} spikes triggering unnecessary accommodations.",
    "Lag: RSS is a trailing indicator, so regime shifts are detected after-the-fact.",
    "Threshold Gaming: Setting threshold too high causes missed shifts; too low causes constant alerts."
  ],
  "invariants": [
    "Stability {{break}}: If RSS < Threshold for N consecutive observations, trigger OntologicalAccommodation",
    "Window Integrity: RSS calculation uses fixed window size, not cherry-picked ranges"
  ],
  "preconditions": [
    "{{agent}} has a predictive model generating expectations",
    "Observations are timestamped and comparable to predictions"
  ],
  "postconditions": [
    "Alert raised if regime break detected",
    "RSS score computed for current window"
  ],
  "parameters": [
    {
      "name": "stability_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "RSS threshold below which regime break is detected"
    },
    {
      "name": "window_size",
      "type": "Integer",
      "range": "[10, 1000]",
      "description": "Number of observations in the rolling average window"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:RegimeSense#mh:SHA-256:086e30af8ab3d7a71b8091dd6e8939558e08a9e12a3f7bf13c92fce74f1da89a",
  "sema_ref": "RegimeSense#086e",
  "sema_stub": "086e",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "break": "Break#177f",
      "noise": "Noise#d631",
      "ontology_adapt": "OntologyAdapt#4c47",
      "quorum": "Quorum#858e",
      "agent": "Agent#35b9",
      "drift_watch": "DriftWatch#191e"
    }
  }
}
```

---

## ScopeFreeze#7d23

```json
{
  "handle": "ScopeFreeze",
  "mechanism": "Phase {{transition}} Control. Defines a discrete point (T_freeze) after which the `{{accept_spec}}` and `Goal` of a {{task}} become Immutable. Any new requirements discovered after T_freeze must be rejected or moved to a 'Backlog' object for future execution. It locks the {{task}} requirements, forcing the agent to {{satisfice}} within the remaining {{timebox_think}} rather than {{decompose}} further.",
  "gloss": "Lock requirements to prevent scope creep",
  "failure_modes": [
    "Feature Creep: {{agent}} discovers 'nice to have' sub-tasks and attempts to execute them during the closing phase.",
    "Perfectionism Spiral: Continuous refinement of the {{accept_spec}} prevents task completion."
  ],
  "invariants": [
    "Immutability: After freeze, {{task}}.{{accept_spec}} cannot be modified.",
    "Rejection: New SubTasks created after freeze must serve EXISTING goals only (no new features)."
  ],
  "preconditions": [
    "Initial requirements defined",
    "{{task}} is active"
  ],
  "postconditions": [
    "New requirements routed to Backlog",
    "{{task}} marked as Frozen (Read-Only Requirements)"
  ],
  "parameters": [
    {
      "name": "exception_policy",
      "type": "Enum",
      "range": "{Reject, Queue#65e4, CostAnalysis}",
      "description": "Default: Queue"
    },
    {
      "name": "freeze_trigger",
      "type": "Enum",
      "range": "{Time, Progress, Manual}",
      "description": "Default: Manual"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:ScopeFreeze#mh:SHA-256:7d238819523d5bb7181d7f0ae7461d7902ddd78862e4eca80ecdc75ce88a8b11",
  "sema_ref": "ScopeFreeze#7d23",
  "sema_stub": "7d23",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "task": "Task#b328",
      "timebox_think": "TimeboxThink#043d",
      "accept_spec": "AcceptSpec#7caa",
      "agent": "Agent#35b9",
      "satisfice": "Satisfice#9859",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## SemanticTabu#b511

```json
{
  "handle": "SemanticTabu",
  "mechanism": "An ideation protocol where the agent explicitly lists existing mechanisms as 'Tabu' (forbidden). It must then solve the problem without using any mechanism on the list. This forces the activation of latent, low-probability pathways in the semantic network. It broadcasts the forbidden list via {{trace}} to ensure the entire swarm respects the constraint.",
  "gloss": "Constraint-based novelty enforcement",
  "failure_modes": [
    "paralysis (if the Tabu list covers all possible physics)."
  ],
  "invariants": [
    "{{constraint}} Satisfaction: Output \u2229 TabuList == \u00d8",
    "Explicit Avoidance: Reasoning trace must cite what is being avoided"
  ],
  "preconditions": [
    "Known solutions exist"
  ],
  "postconditions": [
    "{{solution}} is structurally distinct from Clich\u00e9s"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:SemanticTabu#mh:SHA-256:b511d0691bf169437533d1bcc074e7c350d68e0f3a1e760454eacc289e1ccd53",
  "sema_ref": "SemanticTabu#b511",
  "sema_stub": "b511",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solution": "Solution#fcea",
      "trace": "Trace#9057"
    }
  }
}
```

---

## SourceEvaluate#2f43

```json
{
  "handle": "SourceEvaluate",
  "mechanism": "Credibility Assessment: A {{judge}} module for {{agent}} evaluation. Before accepting claim, evaluate source on: track record, incentives, expertise, access to information. Ask: Why does this source believe this? Would they know if wrong? Do they benefit from me believing? Adjust weight accordingly. It demands a {{cite_back}} for every claim, weighting the evidence by the source's historical reliability.",
  "gloss": "Incentive-aware evidence weighting",
  "failure_modes": [
    "Genetic Fallacy: Dismissing valid claims solely due to the source, ignoring the evidence itself."
  ],
  "invariants": [
    "Evidence must be independently verifiable."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:SourceEvaluate#mh:SHA-256:2f435ed553a590d81c9bce03aa8c2bff73187601609a70f7d090152d45e79456",
  "sema_ref": "SourceEvaluate#2f43",
  "sema_stub": "2f43",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Judge#9554(Agent#35b9)"
  ],
  "dependencies": {
    "references": {
      "cite_back": "CiteBack#bcc5",
      "agent": "Agent#35b9",
      "judge": "Judge#9554"
    }
  }
}
```

---

## SurprisalUpdate#d8c6

```json
{
  "handle": "SurprisalUpdate",
  "mechanism": "A learning protocol where the agent updates its internal model (weights, embeddings, or context) based on failed predictions, weighted by the magnitude of surprise. Higher surprisal = larger update. 'Learn most from what confused you most.' This implements Surprisal-Weighted Fine-Tuning (SWFT): loss contribution is proportional to -log(P(observed|predicted)). Utilizes {{regime_sense}}, {{epistemic_roi}}.",
  "gloss": "Learning weighted by prediction failure magnitude",
  "failure_modes": [
    "Outlier Overfitting: Rare high-surprisal events dominating learning.",
    "Catastrophic Forgetting: Aggressive updates erasing previously stable knowledge.",
    "Compute Cost: High-surprisal events require expensive gradient updates."
  ],
  "invariants": [
    "Loss Magnitude: Update size proportional to surprisal (-log P)",
    "Stability Guard: No single update may shift model more than max_update_rate"
  ],
  "preconditions": [
    "Actual outcome observed and diverged from prediction",
    "Prediction was made with computable probability"
  ],
  "postconditions": [
    "Model updated proportional to surprisal",
    "Update logged for audit trail"
  ],
  "parameters": [
    {
      "name": "learning_rate",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "How much to update the model based on surprisal"
    },
    {
      "name": "max_update_rate",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Maximum allowed model shift per single update"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "related": [
      "BayesUpdate#13f8"
    ],
    "ring": 2
  },
  "sema_id": "sema:SurprisalUpdate#mh:SHA-256:d8c6697a5a5f69152e8b1943205a1f29ffb88e9d62c52c12d042096b0c9502e4",
  "sema_ref": "SurprisalUpdate#d8c6",
  "sema_stub": "d8c6",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "epistemic_roi": "EpistemicROI#0d53",
      "regime_sense": "RegimeSense#086e"
    }
  }
}
```

---

## SurvivorCorrect#45db

```json
{
  "handle": "SurvivorCorrect",
  "mechanism": "Failure Inclusion: When learning from examples, ask: \"Am I only seeing successes?\" Estimate base rate of attempts. Seek out failures and near-misses. The pattern that \"all successful X do Y\" means nothing if failed X also did Y. Denominator matters. Utilizes {{base_rate_include}}.",
  "gloss": "Accounting for silent failures in data",
  "failure_modes": [
    "Phantom Hunt: Wasting resources looking for failures in a dataset that is genuinely 100% successful."
  ],
  "invariants": [
    "{{cognitive_bias}} reduced",
    "Sample re-weighted to account for missing data"
  ],
  "preconditions": [
    "Filtered dataset (survivors only)"
  ],
  "postconditions": [
    "True population estimate"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_id": "sema:SurvivorCorrect#mh:SHA-256:45db899fcfc34876e7be9c72005d3c45d5d5983c6c24a357b2df33d189e7effa",
  "sema_ref": "SurvivorCorrect#45db",
  "sema_stub": "45db",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "base_rate_include": "BaseRateInclude#aa0b",
      "cognitive_bias": "CognitiveBias#4b32"
    }
  }
}
```

---

## TemporalEnsembleForecasting#21af

```json
{
  "handle": "TemporalEnsembleForecasting",
  "mechanism": "The paper's \u00a76.5 protocol for forecasting via ensembles of models frozen at different points in history (Temporal Checkpoint Ensemble). Decomposes prediction via {{conceptual_decomposition}} along two axes simultaneously: temporal diversity (each checkpoint reasons from a different knowledge horizon \u2014 the 2020 checkpoint knows nothing of COVID's economic aftermath; the 2022 checkpoint has internalized it) and causal-lens diversity (each forecast is run through the Forecasting Pentagon: structural, economic, political, base-rate, temporal \u2014 five non-substitutable angles that suppress each other if entangled in a single pass). A ReduceSolver composes the matrix of forecasts, not by averaging but by preserving causal reasoning from each horizon and identifying where independent knowledge states converge on the same structural driver. When three checkpoints spanning different knowledge states independently identify the same causal mechanism, that mechanism has survived a temporal adversarial test no single-model forecast can replicate.",
  "gloss": "Forecast by ensemble of model-checkpoints from different history horizons, each run through five non-substitutable causal lenses \u2014 convergence across time is the signal",
  "invariants": [
    "Temporal diversity source: the checkpoints differ by training-data cutoff, not by prompting \u2014 history itself is the diversity generator.",
    "Five-angle Forecasting Pentagon: each checkpoint's forecast is decomposed across structural, economic, political, base-rate, and temporal dimensions (the pentagon passes the four-test decomposition).",
    "Convergence-not-averaging: the reduction gate accepts convergence of structural drivers across horizons, not arithmetic average of point predictions."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "sema_id": "sema:TemporalEnsembleForecasting#mh:SHA-256:21af04e2b09d31b5e676e8717d01407299e552cf6a1442fccc072b1a4032494a",
  "sema_ref": "TemporalEnsembleForecasting#21af",
  "sema_stub": "21af",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f"
    }
  }
}
```

---

## TruthseekingProtocol#e46e

```json
{
  "handle": "TruthseekingProtocol",
  "mechanism": "The paper's \u00a76.7 protocol for evaluating factual claims through layered epistemic decomposition, where each verified result persists as a content-addressed Sema pattern \u2014 the system gets smarter and verification gets cheaper with every use (the accretion loop). Unlike monolithic claim evaluation (which entangles source credibility, logical consistency, and cross-referencing in one pass, letting strong evidence on any one axis suppress scrutiny on the others), the protocol applies {{conceptual_decomposition}} to verification-depth, producing five layers governed by {{marginal_value_rule}}: Layer 0 cache (has this exact claim been verified?), Layer 1 structural coherence (does this contradict the verified cache?), Layer 2 epistemic decomposition (ClaimExtractorSolver isolates falsifiable statements, ProvenanceSolver evaluates source independent of content, CoherenceSolver checks internal consistency independent of source, CorrespondenceSolver queries external data, ContestabilitySolver constructs the strongest counter-case), Layer 3 cross-domain specialists in the Cognitive Commons, Layer 4 empirical verification via primary data gathering. Each layer's Solvers operate behind the contract, blind to the others' outputs until they compose at a typed boundary. Verified claims mint as new Sema patterns that enter the Layer 0 cache. Composes with {{validate}} at each layer boundary.",
  "gloss": "Layered epistemic verification (cache \u2192 coherence \u2192 decomposition \u2192 specialists \u2192 empirical), with verified claims persisting as Sema patterns \u2014 the accretion loop",
  "invariants": [
    "Layer-blind composition: Solvers within a layer do not see each other's outputs until they compose at a typed boundary \u2014 no suppression of scrutiny by a strong signal on a parallel axis.",
    "Accretion monotonic: a verified claim enters the Layer-0 cache as a content-addressed pattern and remains there until superseded by a counter-claim that survives the same layers.",
    "Marginal-value depth: most claims resolve at Layer 0; only claims with genuine novelty or contradiction incur higher layers' cost, governed by {{marginal_value_rule}}."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Inference",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "sema_id": "sema:TruthseekingProtocol#mh:SHA-256:e46e6ed26ab83b3ce99c0c28055fb946158eea44293ac8b2ebc270e4b7d56455",
  "sema_ref": "TruthseekingProtocol#e46e",
  "sema_stub": "e46e",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f",
      "marginal_value_rule": "MarginalValueRule#32ce"
    },
    "references": {
      "validate": "Validate#ebe1"
    }
  }
}
```

---

## BeliefTracking#39cf

```json
{
  "handle": "BeliefTracking",
  "mechanism": "Epistemic Version Control. Enforces a 'Commit Log' for internal knowledge. Before processing new information, the {{agent}} must query and pin its current Priors. If the posterior belief shifts significantly, the {{agent}} creates a new Node connected to the old one via a `supersedes` edge, explicitly noting the 'Surprisal' that caused the shift. It calculates the divergence magnitude via {{surprisal_update}} to determine whether a new node is justified or if the evidence fits the existing model.",
  "gloss": "Note what you believed before and after",
  "failure_modes": [
    "Hindsight {{cognitive_bias}}: {{agent}} overwrites prior beliefs with new data, destroying the record of learning.",
    "Epistemic Thrashing: Creating new belief versions for trivial noise (over-sensitivity).",
    "Silent Update: Changing internal weights/state without creating a graph edge to document it."
  ],
  "invariants": [
    "Causal Link: Every update must cite the specific 'Trigger' (Evidence) that caused the shift.",
    "Non-Destructive Update: Old beliefs are never deleted, only Superseded.",
    "Prior Commitment: Must retrieve/state existing beliefs BEFORE ingesting new evidence."
  ],
  "preconditions": [
    "Existing knowledge graph",
    "Incoming information stream"
  ],
  "postconditions": [
    "{{belief}} graph updated with version history",
    "Learning delta recorded"
  ],
  "parameters": [
    {
      "name": "update_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Minimum delta to trigger belief revision"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "related": [
      "BayesUpdate#13f8"
    ],
    "ring": 2
  },
  "sema_id": "sema:BeliefTracking#mh:SHA-256:39cf2ce07c44d5520931c23d174915ad69b76530a3d0745442eb958f0c8e832a",
  "sema_ref": "BeliefTracking#39cf",
  "sema_stub": "39cf",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "surprisal_update": "SurprisalUpdate#d8c6",
      "belief": "Belief#a9ce",
      "cognitive_bias": "CognitiveBias#4b32",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Cache#cd97

```json
{
  "handle": "Cache",
  "mechanism": "A temporary high-speed storage layer for keeping frequently accessed {{datum}} or {{state}} alongside the inputs that produced them, so repeat lookups bypass re-computation. Read-through, write-behind, and invalidation discipline are descendant concerns; the foundation is the keyed lookup that returns a stored value if present.",
  "gloss": "Temporary high-speed storage",
  "failure_modes": [
    "Staleness: Serving outdated data after the source has changed.",
    "Thrashing: Frequent evictions due to insufficient size."
  ],
  "invariants": [
    "Consistency: Cache(Key) == Source(Key) if valid.",
    "Freshness: Expired items must not be returned."
  ],
  "preconditions": [
    "Key is hashable",
    "Value is serializable"
  ],
  "postconditions": [
    "Value retrieved significantly faster than source"
  ],
  "sema_id": "sema:Cache#mh:SHA-256:cd9732c5c9b4686dcc6c3fd1c8c1c5e20a94a7ac33aee969c678cdc7380d95bc",
  "sema_ref": "Cache#cd97",
  "sema_stub": "cd97",
  "_meta": {
    "layer": "Mind",
    "category": "Memory",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf",
      "state": "State#4d58"
    }
  }
}
```

---

## ChunkMerge#43ae

```json
{
  "handle": "ChunkMerge",
  "mechanism": "Cognitive Compression: Group related items into named chunks. Treat chunk as single unit in working memory. {{hierarchy}} of chunks enables handling complexity beyond raw capacity. Merge when patterns repeat; split when chunk becomes unwieldy. It applies {{aggregate}} to {{compress}} multiple working memory items into a single labeled unit.",
  "gloss": "Hierarchical context management",
  "failure_modes": [
    "Lossy Compression: Discarding critical low-level details (e.g., specific ID numbers) during the merge process."
  ],
  "invariants": [
    "Chunk name must be meaningful.",
    "Information Conservation: Merged chunk retains key retrieval hooks of parts",
    "Size {{constraint}}: Size(Merged) <= ContextWindowLimit"
  ],
  "preconditions": [
    "Input chunks share semantic topic"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_id": "sema:ChunkMerge#mh:SHA-256:43ae7aa56537a6967339b1f836a7e3cae64f188d35c68407315f269f07a6ecd9",
  "sema_ref": "ChunkMerge#43ae",
  "sema_stub": "43ae",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "aggregate": "Aggregate#7912",
      "hierarchy": "Hierarchy#d530",
      "compress": "Compress#0967"
    }
  }
}
```

---

## ContextCompress#4845

```json
{
  "handle": "ContextCompress",
  "mechanism": "A memory management primitive that uses {{compress}} to reduce the token footprint of a {{context}} while preserving critical {{state}}. It explicitly retains active {{constraint}}s and unresolved goals.",
  "gloss": "Semantic compression for long-running contexts",
  "sema_id": "sema:ContextCompress#mh:SHA-256:48458df78d10876c4902fa808ae131b038616f5f0014d1571afd61d23a08b81f",
  "sema_ref": "ContextCompress#4845",
  "sema_stub": "4845",
  "_meta": {
    "layer": "Mind",
    "category": "Memory",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "state": "State#4d58",
      "compress": "Compress#0967",
      "context": "Context#510a"
    }
  }
}
```

---

## CurriculumReplay#13d4

```json
{
  "handle": "CurriculumReplay",
  "mechanism": "Agents re-train on their own high-scoring past outputs during downtime to reinforce successful behaviors. Self-distillation without external supervision. {{agent}} maintains a replay buffer of successful interactions ranked by outcome quality. During idle cycles, agent samples from buffer and fine-tunes on its own best work. {{decay}} function prioritizes recent successes over stale ones. It draws training examples from the {{experience_sharding}} database, filtering for high-quality outcomes.",
  "gloss": "Self-supervised reinforcement via memory sampling",
  "failure_modes": [
    "Model Collapse: {{agent}} over-fits to its own outputs, drifting into a closed loop of hallucination."
  ],
  "invariants": [
    "Examples ordered by complexity (easy to hard)",
    "No catastrophic forgetting of earlier lessons"
  ],
  "preconditions": [
    "Dataset of task examples",
    "Learning agent"
  ],
  "postconditions": [
    "{{agent}} performance improved on target distribution"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_id": "sema:CurriculumReplay#mh:SHA-256:13d4d3af882c43d16e0e4a1b0efc4ea213bd39ccf9e9121d82e8a42c7bcc55c2",
  "sema_ref": "CurriculumReplay#13d4",
  "sema_stub": "13d4",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4",
      "agent": "Agent#35b9",
      "experience_sharding": "ExperienceSharding#43c3"
    }
  }
}
```

---

## ExperienceSharding#43c3

```json
{
  "handle": "ExperienceSharding",
  "mechanism": "Applies the {{shard}} primitive to agent memory. When context fills, the agent splits into two specialized agents (active vs archival) rather than forgetting. It segments history into discrete blocks via {{chunk_merge}} before distributing them across the agent cluster.",
  "gloss": "Agent bifurcation on context saturation: active vs archival specialists",
  "failure_modes": [
    "coordination overhead between the shards increases."
  ],
  "invariants": [
    "Recombination reconstructs global pattern",
    "Shards cover disjoint parts of state/experience space"
  ],
  "preconditions": [
    "Large dataset or experience stream",
    "Multiple learners"
  ],
  "postconditions": [
    "Distributed knowledge base"
  ],
  "parameters": [
    {
      "name": "cross_shard_policy",
      "type": "Enum",
      "range": "{Forbid, Replicate, Broadcast}",
      "description": "Multi-shard access"
    },
    {
      "name": "routing_key",
      "type": "Enum",
      "range": "{AgentId, TaskType, Random}",
      "description": "Assignment strategy"
    },
    {
      "name": "shard_count",
      "type": "Integer",
      "range": "[2, 64]",
      "description": "Number of experience partitions"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "related": [
      "FabricSharding#880b"
    ],
    "ring": 0
  },
  "sema_id": "sema:ExperienceSharding#mh:SHA-256:43c36b2250e4e10bd0d9d83beb1f8e68ee629d2cc076eaf9ef1f57a4dde2cbe4",
  "sema_ref": "ExperienceSharding#43c3",
  "sema_stub": "43c3",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "chunk_merge": "ChunkMerge#43ae",
      "shard": "Shard#1e74"
    }
  }
}
```

---

## HolographicShard#c137

```json
{
  "handle": "HolographicShard",
  "mechanism": "{{context}}-Preserving Slice: Sub-tasks contain a holographic reference to the global goal. Every shard includes: parent_goal_hash, intent_summary, and constraint_inheritance. The sub-agent can independently verify if its local action serves the global intent without querying the central node. It extends {{fabric_sharding}} by ensuring every fragment contains a recoverable 'seed' of the whole, enabling localized reconstruction.",
  "gloss": "Local action via global context embedding",
  "failure_modes": [
    "{{context}} Bloat: The shard becomes larger than the task itself because it carries too much global history.",
    "{{context}} overhead is expensive.",
    "Shards become too heavy to transmit.",
    "{{deep}} nesting creates exponential context bloat."
  ],
  "invariants": [
    "Distribution: Shards are stored on failure-independent nodes",
    "Information Redundancy: Any K of N shards can reconstruct the Whole"
  ],
  "preconditions": [
    "Data encoded with Erasure Code (e.g. Reed-Solomon)"
  ],
  "parameters": [
    {
      "name": "encoding",
      "type": "Enum",
      "range": "{ReedSolomon, Fountain, Simple}",
      "description": "Error correction method"
    },
    {
      "name": "reconstruction_threshold",
      "type": "Float",
      "range": "[0.3, 0.7]",
      "description": "Min fragments for recovery"
    },
    {
      "name": "redundancy_factor",
      "type": "Integer",
      "range": "[2, 5]",
      "description": "Copies per datum"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 0
  },
  "sema_id": "sema:HolographicShard#mh:SHA-256:c137cf1fad9b9dc48b26b8cbf32ea744f91b69f5f5f7a7d3a7ad72b12ee48545",
  "sema_ref": "HolographicShard#c137",
  "sema_stub": "c137",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "deep": "Deep#89f0",
      "fabric_sharding": "FabricSharding#880b",
      "context": "Context#510a"
    }
  }
}
```

---

## LatentAttachment#ab68

```json
{
  "handle": "LatentAttachment",
  "mechanism": "Attaching a high-dimensional vector embedding (latent) to a symbolic pattern card. This allows agents to use 'Fuzzy Search' to find the card, while still using the 'Canonical Hash' for strict verification. It bridges the gap between LLM intuition and code execution. It binds a vector embedding to a {{concept_anchor}}, enabling semantic search without breaking the symbolic hash.",
  "gloss": "Hybrid symbolic-neural identity",
  "failure_modes": [
    "Model shift invalidates embeddings."
  ],
  "invariants": [
    "{{identity}} Separation: Removing the Latent block MUST NOT change the Canonical Hash",
    "Semantic Proximity: Distance(Symbolic, Latent) < Threshold"
  ],
  "preconditions": [
    "Embedding model is fingerprinted/versioned"
  ],
  "postconditions": [
    "Pattern is discoverable via vector search"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 0
  },
  "sema_id": "sema:LatentAttachment#mh:SHA-256:ab684573c68d4eb05cab650f17e6970a22e65e7d989b53db3281422785fbfec4",
  "sema_ref": "LatentAttachment#ab68",
  "sema_stub": "ab68",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "concept_anchor": "ConceptAnchor#9187"
    }
  }
}
```

---

## LocalizedLearning#fcc7

```json
{
  "handle": "LocalizedLearning",
  "mechanism": "A learning process that performs the {{act}} of routing {{feedback_signal}} exclusively to the specific {{solver_manifest}} that generated the result. By partitioning memory updates by subproblem type, it prevents the catastrophic interference common in monolithic models. The feedback signal is tagged with solver ID, ensuring updates are isolated.",
  "gloss": "Partitioned feedback router for solver learning",
  "failure_modes": [
    "Echo Chamber: A specialist solver over-optimizes for its narrow metric, ignoring global context.",
    "Feedback Sparsity: Rare modules receive insufficient feedback to learn.",
    "Misrouting: Feedback is attributed to the wrong solver.",
    "Signal Decay: Feedback arrives too late to be useful."
  ],
  "invariants": [
    "Isolation: Update(Solver_A) cannot change Weights(Solver_B).",
    "Attribution: Each feedback signal must identify its source solver.",
    "Standardization: Feedback format is universal across all solver types."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "ring": 1
  },
  "sema_id": "sema:LocalizedLearning#mh:SHA-256:fcc7ce39c401ba37771431503aaad0ef9715a01c0844d3594cea64475048e8e2",
  "sema_ref": "LocalizedLearning#fcc7",
  "sema_stub": "fcc7",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "signature": [
    "Act#5d55(FeedbackSignal#f174)"
  ],
  "dependencies": {
    "accepts": {
      "feedback_signal": "FeedbackSignal#f174"
    },
    "references": {
      "solver_manifest": "SolverManifest#ea7a",
      "act": "Act#5d55"
    }
  }
}
```

---

## PathwayMemory#0799

```json
{
  "handle": "PathwayMemory",
  "mechanism": "A {{cache}} of routing outcomes, recording (problem_class, route_chosen, outcome_quality) tuples. Enables a dispatching Solver to learn which routes produce better results for which problem types. The RootSolver's PathwayMemory is the architecture's most consequential site of compounding \u2014 it sees how every problem enters the system, and its accumulated routing decisions determine which reasoning highways densify over time. Every dispatching node has its own PathwayMemory; they are not shared, but can be aggregated for cross-node learning.",
  "gloss": "Learned routing memory: problem_class \u2192 route \u2192 outcome_quality",
  "data_schema": {
    "type": "object",
    "required": [
      "entries"
    ],
    "properties": {
      "entries": {
        "type": "array",
        "description": "List of routing records",
        "items": {
          "type": "object",
          "required": [
            "problem_class",
            "route_chosen",
            "outcome_quality"
          ],
          "properties": {
            "problem_class": {
              "type": "string"
            },
            "route_chosen": {
              "type": "string"
            },
            "outcome_quality": {
              "type": "number"
            }
          }
        }
      }
    }
  },
  "invariants": [
    "Append-only within a session: historical records are not edited, only new entries added.",
    "Scoped: each PathwayMemory belongs to exactly one dispatching node."
  ],
  "failure_modes": [
    "Poisoned entries (false outcome_quality from compromised writers) silently bias all downstream routing without triggering any failure mode.",
    "Stale entries reflecting outdated problem distributions mislead current routing; no automatic aging.",
    "Cross-node aggregation without provenance contaminates local routing with off-domain signal."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 1,
    "caution": "Silent contamination vector \u2014 poisoned entries bias all downstream routing decisions without triggering failure modes. Integrity of writers must be enforced."
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "sema_id": "sema:PathwayMemory#mh:SHA-256:0799234ac2992646e119585288ccf5e96685c35bd5c55ee0fb1e26ce74bdfdd4",
  "sema_ref": "PathwayMemory#0799",
  "sema_stub": "0799",
  "dependencies": {
    "references": {
      "cache": "Cache#cd97"
    }
  }
}
```

---

## Proprioception#e486

```json
{
  "handle": "Proprioception",
  "mechanism": "Continuous self-monitoring of position in the {{task}} graph. An {{agent}} periodic 'ping' to itself to verify {{context}}, active tool state, and depth in recursion. Prevents 'getting lost' in long chains of thought. It maintains internal {{state}} awareness, using {{somatic_marker}} to detect recursion depth limits or resource fatigue.",
  "gloss": "Self-location awareness within the task graph",
  "failure_modes": [
    "Stagnation: {{agent}} remains in same node > N ticks Orphaned: Parent {{task}} ID not found/unresponsive Hallucinated {{context}}: Stack {{trace}} does not match environmental reality"
  ],
  "invariants": [
    "{{context}} Continuity: {{agent}} knows its parent {{task}} ID",
    "Liveness: Parent.status == ACTIVE",
    "{{state}} Recovery: Can reconstruct stack {{trace}} from logs"
  ],
  "parameters": [
    {
      "name": "max_recursion_depth",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Default: 10"
    },
    {
      "name": "stagnation_threshold",
      "type": "Int",
      "range": "[1, 100]",
      "description": "Ticks before abort"
    }
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_id": "sema:Proprioception#mh:SHA-256:e48696d927609b38ba32467846cc70a4ec8ddff101ec9b6728bfd99637df0e1d",
  "sema_ref": "Proprioception#e486",
  "sema_stub": "e486",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "state": "State#4d58",
      "context": "Context#510a",
      "trace": "Trace#9057",
      "agent": "Agent#35b9",
      "somatic_marker": "SomaticMarker#53bb"
    }
  }
}
```

---

## RetrievalAugment#2ecb

```json
{
  "handle": "RetrievalAugment",
  "mechanism": "Before generating a response, the {{agent}} queries an external knowledge store via {{latent_attachment}}-backed retrieval (vector database, search index, knowledge graph) to surface relevant {{context}}. The retrieval obeys {{context_first}}: no generation fires before the external lookup completes. Retrieved documents are injected into the {{prompt}}, grounding the response in external facts rather than relying solely on parametric memory. The canonical RAG (Retrieval-Augmented Generation) pattern. It injects external {{context}} into the {{chain_of_thought}}, grounding the reasoning process in retrieved facts.",
  "gloss": "Ground responses in retrieved external knowledge",
  "failure_modes": [
    "Retrieval Poisoning: Malicious or incorrect documents in the index contaminate responses.",
    "{{context}} Stuffing: Too many retrieved chunks exceed {{context}} window, causing truncation of critical information."
  ],
  "invariants": [
    "Citation: Retrieved sources should be traceable in the output",
    "Query Before Generate: Retrieval must precede response generation",
    "Relevance Threshold: Only documents above similarity threshold are included"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "related": [
      "DeepResearch#2a05"
    ],
    "ring": 2
  },
  "sema_id": "sema:RetrievalAugment#mh:SHA-256:2ecb9c4ce49ecbbf58c9e4dfb241a769223ae358f1d4548482f8928e61627dfe",
  "sema_ref": "RetrievalAugment#2ecb",
  "sema_stub": "2ecb",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "prompt": "Prompt#b18a",
      "context": "Context#510a",
      "latent_attachment": "LatentAttachment#ab68",
      "agent": "Agent#35b9",
      "context_first": "ContextFirst#def7",
      "chain_of_thought": "ChainOfThought#c3cd"
    }
  }
}
```

---

## Scratchpad#75bf

```json
{
  "handle": "Scratchpad",
  "mechanism": "A designated working memory region where the agent can write intermediate calculations, partial results, and notes-to-self during multi-step reasoning. Unlike the main output, scratchpad content is explicitly for the agent's own use and may be hidden from the final response. Prevents context pollution while enabling complex reasoning. It provides the persistence layer for chain-of-thought, storing the intermediate states of the reasoning process.",
  "gloss": "Working memory for intermediate reasoning steps",
  "failure_modes": [
    "Scratchpad Leak: Internal working notes accidentally included in user-facing output.",
    "Memory Overflow: Scratchpad grows unboundedly, consuming context window."
  ],
  "invariants": [
    "Bounded: Maximum scratchpad size is enforced",
    "Persistence: Contents survive across reasoning steps within a task",
    "Separation: Scratchpad content is distinct from final output"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "ring": 0
  },
  "sema_id": "sema:Scratchpad#mh:SHA-256:75bf0d045bf0907b1412c0698a7a5f7cffb2963b653646c0831ec1d3bdab186e",
  "sema_ref": "Scratchpad#75bf",
  "sema_stub": "75bf",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "data_schema": {
    "type": "object",
    "required": [
      "content"
    ],
    "properties": {
      "content": {
        "type": "string",
        "description": "Working memory contents"
      },
      "max_size": {
        "type": "integer",
        "description": "Maximum allowed size in tokens"
      },
      "owner_id": {
        "type": "string",
        "description": "Agent that owns this scratchpad"
      }
    }
  }
}
```

---

## SelfReminder#c896

```json
{
  "handle": "SelfReminder",
  "mechanism": "A system prompt technique that wraps user queries with explicit restatements of the model's constraints, values, and operational boundaries. Before processing each request, the model is reminded: 'You are a helpful assistant. You must not [constraints]. Your goal is [objective].' Reduces jailbreak success rates by reinforcing safety context. It injects a persistent {{trace}} of the agent's core identity into the prompt context.",
  "gloss": "Reinforce constraints in system prompt before each response",
  "failure_modes": [
    "{{context}} Dilution: Long conversations push reminder out of effective context window.",
    "Brittleness: Sophisticated attacks still bypass static reminders.",
    "Token Overhead: Repeated reminders consume context budget."
  ],
  "invariants": [
    "Consistent Application: Reminder applied to every user turn",
    "{{constraint}} Specificity: Reminders must name concrete prohibited behaviors",
    "Placement: Reminder positioned for maximum attention weight"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_id": "sema:SelfReminder#mh:SHA-256:c8963a9fcc7250cec588a332bb96f1b988b64909c47b788c288c30a3a9cad832",
  "sema_ref": "SelfReminder#c896",
  "sema_stub": "c896",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "trace": "Trace#9057",
      "context": "Context#510a"
    }
  }
}
```

---

## SimulationTrace#c2e6

```json
{
  "handle": "SimulationTrace",
  "mechanism": "Before taking an irreversible action (e.g., `delete_file`), the agent simulates the execution step-by-step in a scratchpad. It inspects the predicted state after the action. If the state looks bad, it aborts. It generates a verifiable {{trace}} of a {{mental_sim}}, creating an immutable record of the predicted future state.",
  "gloss": "Pre-execution mental model",
  "failure_modes": [
    "{{simulation}} inaccuracy (the map is not the territory)."
  ],
  "invariants": [
    "Causality: Every step T+1 is derived from T",
    "Replayability: {{trace}}(Start) == End",
    "{{trace}} immutable after creation."
  ],
  "preconditions": [
    "{{simulation}} engine initialized"
  ],
  "postconditions": [
    "Verifiable trace artifact generated"
  ],
  "parameters": [
    {
      "name": "confidence_floor",
      "type": "Probability#356b",
      "range": "[0.5, 0.9]",
      "description": "Min certainty to trust trace"
    },
    {
      "name": "simulation_fidelity",
      "type": "Percentage",
      "range": "[70%, 99%]",
      "description": "Required model accuracy"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "sema_id": "sema:SimulationTrace#mh:SHA-256:c2e62aa7617e24b4d832b9c83cf544a63bc346d4e38ebf863278ccb556bb946f",
  "sema_ref": "SimulationTrace#c2e6",
  "sema_stub": "c2e6",
  "dependencies": {
    "references": {
      "mental_sim": "MentalSim#10ff",
      "trace": "Trace#9057",
      "simulation": "Simulation#aa24"
    }
  }
}
```

---

## Stigmergy#f624

```json
{
  "handle": "Stigmergy",
  "mechanism": "Agents MARK shared environment with structured traces instead of sending direct messages. Other agents SENSE traces and respond. Traces DECAY over time but can be REINFORCED by repeated marking. Coordination emerges from accumulated trace patterns without any agent-to-agent communication. (Formerly known as {{trace}}).",
  "gloss": "Indirect coordination via environment modification (Ant Colony)",
  "invariants": [
    "{{decay}}: Signals must fade over time unless reinforced",
    "Locality: Sensing is local to the agent's position"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Memory",
    "related": [
      "sema:GhostTrail#mh:SHA-256:ec5b2ca0ee009f2aec90a8fb2cec9ee5feb29a1d98f20a7211d973b26a629e6a",
      "Signal#f39d"
    ],
    "ring": 0
  },
  "sema_id": "sema:Stigmergy#mh:SHA-256:f624f79cc3860686d0278c28c17cfd0e746d8fb2300fa9590ba90f134fee82ed",
  "sema_ref": "Stigmergy#f624",
  "sema_stub": "f624",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4",
      "trace": "Trace#9057"
    }
  }
}
```

---

## TraceBelief#7933

```json
{
  "handle": "TraceBelief",
  "mechanism": "A chronological reasoning pattern that tracks the history of a belief. Prevents 'Silent Updating' by forcing the agent to cite the specific past belief node it is revising. Instantiates the {{trace}} primitive on a {{belief}} object. Utilizes {{trace}}, {{surprisal_update}}, {{belief}}, {{time_warp_log}}.",
  "gloss": "Belief Provenance (Macro for Trace(Belief))",
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Memory",
    "ring": 2
  },
  "sema_id": "sema:TraceBelief#mh:SHA-256:793355797fb406924e3763b280a01829d1e8a650fafc5ce71f6a1c0d1cc8e222",
  "sema_ref": "TraceBelief#7933",
  "sema_stub": "7933",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "signature": [
    "Trace#9057(Belief#a9ce)"
  ],
  "dependencies": {
    "references": {
      "time_warp_log": "TimeWarpLog#a0ac",
      "surprisal_update": "SurprisalUpdate#d8c6",
      "trace": "Trace#9057",
      "belief": "Belief#a9ce"
    }
  }
}
```

---

## Abduction#a9df

```json
{
  "handle": "Abduction",
  "mechanism": "Inference to the best explanation. Given a surprising observation, generate candidate explanations and {{rank}} them by simplicity, scope, and coherence with existing knowledge. Adopt the highest-ranked as working {{hypothesis}}, flagged as provisional \u2014 not proven. Uses {{chain_of_thought}} to trace the reasoning path from observation to explanation so the inferential leap is explicit and verifiable. The classical third mode of reasoning alongside {{deduction}} (necessary) and {{induction}} (probable from instances): Abduction is probable from a single anomaly plus background knowledge.",
  "gloss": "Inference to the best explanation \u2014 provisional, ranked by simplicity/scope/coherence",
  "failure_modes": [
    "Conspiracy Thinking: Preferring complex, coherent explanations over simple, messy ones (overfitting the narrative).",
    "Stopping too early: adopting the first plausible explanation without considering alternatives.",
    "Treating the provisional hypothesis as proven in downstream reasoning."
  ],
  "invariants": [
    "Explanation must cover all observed anomalies in the input.",
    "Simplicity heuristic (Occam's Razor) applied when comparing candidates of similar scope.",
    "Output is flagged provisional, never asserted as proven."
  ],
  "preconditions": [
    "Set of observations, at least one unexplained by existing model.",
    "No deductive path to the explanation."
  ],
  "postconditions": [
    "{{hypothesis}} generated and ranked by likelihood.",
    "Working hypothesis adopted with provisional status."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1,
    "caution": "Best-guess inference \u2014 always provisional. Must be composed with a verification step in high-stakes domains.",
    "supersedes": [
      "sema:AbductiveLeap#mh:SHA-256:1069501989760c74143a80a2a2ee3267463e206d8998c76d38399c2498e8791d"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Abduction#mh:SHA-256:a9dfc3350b4a0b9b8424cdfeaa9c6c90cb6a87123b310789f181ee9e67ca7941",
  "sema_ref": "Abduction#a9df",
  "sema_stub": "a9df",
  "dependencies": {
    "references": {
      "rank": "Rank#7a76",
      "deduction": "Deduction#9c88",
      "induction": "Induction#2487",
      "hypothesis": "Hypothesis#ffa7"
    },
    "composes_with": {
      "chain_of_thought": "ChainOfThought#c3cd"
    }
  }
}
```

---

## BackwardChain#a231

```json
{
  "handle": "BackwardChain",
  "mechanism": "Goal-First Decomposition: Start from desired end-state, recursively identify prerequisites. For each prerequisite, ask \"what must be true for this to hold?\" until reaching known facts or actionable steps. Execution order is reverse of discovery order. A goal-directed form of {{deduction}} \u2014 derives required antecedents from the desired consequent. Structures the {{chain_of_thought}} in reverse chronological order, linking the desired future state to present preconditions.",
  "gloss": "Goal-driven reasoning from target to preconditions",
  "failure_modes": [
    "Infinite Regression: The precondition chain never terminates because base facts are missing."
  ],
  "invariants": [
    "Causal Sufficiency: Step(T) must be sufficient condition for Step(T+1)",
    "Goal Anchoring: {{chain}} must start at DesiredEndState",
    "Leaf nodes must be actionable or known-true."
  ],
  "preconditions": [
    "Goal is clearly defined",
    "Goal state clearly defined. Domain has prerequisite structure. Knowledge base queryable."
  ],
  "postconditions": [
    "Execution plan produced OR goal proven unachievable. {{plan}} steps in executable order. All prerequisites satisfied."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:BackwardChain#mh:SHA-256:a231ada9216f6fef3fc3b7e307802b3e05cc3db778b8020e378dfb531137965f",
  "sema_ref": "BackwardChain#a231",
  "sema_stub": "a231",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "chain": "Chain#711e",
      "plan": "Plan#fd6d",
      "chain_of_thought": "ChainOfThought#c3cd",
      "deduction": "Deduction#9c88"
    }
  }
}
```

---

## Bisect#88b3

```json
{
  "handle": "Bisect",
  "mechanism": "Binary Partition: Define the possibility space. Find a question that splits space roughly in half. Ask it. Discard eliminated half. Repeat on remaining half. O(log n) questions to isolate answer. Requires ordered or divisible domain. Often underpins the execution of {{recursive_root_cause}}.",
  "gloss": "Logarithmic search via binary splitting",
  "failure_modes": [
    "False Negative: Discarding the half that actually contained the answer because the splitting question was flawed."
  ],
  "invariants": [
    "Each question eliminates \u226540% of remaining space."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:Bisect#mh:SHA-256:88b3085fd8a158f3fa253cbc18eb121c6ea858a1b0fd8045fd4452ae00a81901",
  "sema_ref": "Bisect#88b3",
  "sema_stub": "88b3",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "recursive_root_cause": "RecursiveRootCause#6dc1"
    }
  }
}
```

---

## ChainOfThought#c3cd

```json
{
  "handle": "ChainOfThought",
  "mechanism": "The canonical implementation of sequential reasoning. Instantiates the '{{think}}' primitive with a linear '{{chain}}' {{topology}}. Elicits a step-by-step derivation of the answer to improve accuracy and transparency. It implements the {{think}} primitive as a linear {{chain}}, optionally invoking {{step_back}} or {{reflexion}} to self-correct during the derivation.",
  "gloss": "Step-by-step reasoning (Macro for Think(Chain))",
  "invariants": [
    "Inherits invariants from {{think}} and {{chain}}",
    "Reasoning Before Answer: Intermediate steps must precede final conclusion"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "ProgramOfThought",
      "ReAct#e018"
    ],
    "ring": 2
  },
  "sema_id": "sema:ChainOfThought#mh:SHA-256:c3cd00ab11984f75ecb20bdcace9a0837fad01c828b7858bc1323a795fc43202",
  "sema_ref": "ChainOfThought#c3cd",
  "sema_stub": "c3cd",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Chain#711e)"
  ],
  "dependencies": {
    "composes_with": {
      "reflexion": "Reflexion#eed9",
      "step_back": "StepBack#b16f"
    },
    "references": {
      "think": "Think#e1bd",
      "chain": "Chain#711e",
      "topology": "Topology#2408"
    }
  }
}
```

---

## CiteBack#bcc5

```json
{
  "handle": "CiteBack",
  "mechanism": "The agent is forbidden from stating a fact unless it can simultaneously generate a pointer (quote or ID) to the specific chunk of context that supports it. No hallucination allowed; only citation. It forces a verification step where every assertion must be supported by a {{retrieval_augment}} lookup returning the source ID.",
  "gloss": "Grounding claims in source",
  "failure_modes": [
    "Inability to answer implicit or common-sense questions."
  ],
  "invariants": [
    "Every assertion links to source ID",
    "Source must exist in context history"
  ],
  "preconditions": [
    "Generated claim",
    "Source material available"
  ],
  "postconditions": [
    "Claim decorated with citation"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_id": "sema:CiteBack#mh:SHA-256:bcc5f0da7205f446b829c6b70fa40ad3e676cc359eb04ef2280c03e1498ecde6",
  "sema_ref": "CiteBack#bcc5",
  "sema_stub": "bcc5",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "retrieval_augment": "RetrievalAugment#2ecb"
    }
  }
}
```

---

## CognitiveEcho#5252

```json
{
  "handle": "CognitiveEcho",
  "mechanism": "Variance-Based Effort Estimation: {{agent}} runs N rapid, low-fidelity simulations of the task. If outcomes diverge significantly, it triggers decomposition. Ping the problem before solving it. High variance in simulation implies hidden complexity. Process: (1) Generate N quick solution sketches, (2) Measure outcome variance, (3) If variance > threshold, decompose; else execute simplest solution.",
  "gloss": "Estimating difficulty via simulation variance",
  "failure_modes": [
    "Correlated Hallucination: All simulations are wrong in the exact same way (low variance, high error).",
    "The simulation model might be too simple to catch edge cases (false negative).",
    "{{simulation}} cost may exceed just trying the task for truly simple problems.",
    "Sample count is arbitrary - tuning required."
  ],
  "invariants": [
    "Delay does not exceed short-term memory bounds",
    "Echo content matches input semantic hash"
  ],
  "preconditions": [
    "Feedback loop enabled",
    "Input signal"
  ],
  "postconditions": [
    "{{signal}} amplified or validated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "SignalReflection#a613"
    ],
    "ring": 2
  },
  "sema_id": "sema:CognitiveEcho#mh:SHA-256:5252515f350d9f3df7d64a544570c8795048f17a56288c854ab42974ad2ddeec",
  "sema_ref": "CognitiveEcho#5252",
  "sema_stub": "5252",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "simulation": "Simulation#aa24",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## CollaborativeWritingProtocol#0588

```json
{
  "handle": "CollaborativeWritingProtocol",
  "mechanism": "The paper's \u00a76.1 protocol for producing textual (or any structured) output that must meet a quality standard. Decomposes the concept of quality-constrained production into five orthogonal dimensions via {{conceptual_decomposition}}: substance (what material must the artifact contain), structure (how does it organize), generation (produce freely with evaluation elsewhere), evaluation (does it meet the standard across independent quality dimensions), and refinement (surface quality on a structurally complete artifact). Two parallel mechanisms run together: a structural pipeline (ScopeDiscoverySolver \u2192 SequencingCoherenceSolver \u2192 UnitConstraintSolver \u2192 StructuralVerificationSolver \u2192 VoiceRefinementSolver) that separates generation from evaluation, and concurrent ObserverSolvers (RepetitionSolver, ContradictionSolver, IntentSolver, AudienceReceptionSolver) that externalize the silent evaluative thinking a solo writer does with interference. The protocol transfers beyond writing to any domain where something must be produced to a standard (music composition, interface design).",
  "gloss": "Decompose quality-constrained production into substance, structure, generation, evaluation, and refinement \u2014 the five orthogonal dimensions a producer must address",
  "invariants": [
    "Dimension-orthogonal: the five sub-concepts pass the four-test decomposition ({{conceptual_decomposition}}); an observer checking repetition does not generate, a generator does not self-censor toward criteria it lacks.",
    "Concurrent-not-sequential: evaluative observers run alongside generation, producing typed annotations that accumulate; they are not editors.",
    "Variable-depth: each of the five dimensions can itself recurse via its own sub-solver tree when the stakes warrant it ({{marginal_value_rule}} governs depth)."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:CollaborativeWritingProtocol#mh:SHA-256:0588bcabfe6a70a924aebd2acca7e968211cd39612c23cad01a93ad8d2b6cb86",
  "sema_ref": "CollaborativeWritingProtocol#0588",
  "sema_stub": "0588",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f",
      "marginal_value_rule": "MarginalValueRule#32ce"
    }
  }
}
```

---

## Compare#4881

```json
{
  "handle": "Compare",
  "mechanism": "Evaluate relation between two values: Equal, Less, Greater, Incomparable.",
  "gloss": "Relational check",
  "invariants": [
    "Reflexivity: A == A is always True.",
    "Symmetry: If A == B, then B == A.",
    "Transitivity: If A == B and B == C, then A == C."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 0
  },
  "sema_id": "sema:Compare#mh:SHA-256:48815374a8845487f135578867a9a36ffeeb0e786007b63da5713292723e2109",
  "sema_ref": "Compare#4881",
  "sema_stub": "4881",
  "sema_layer": "Mind",
  "sema_category": "Reasoning"
}
```

---

## ConceptualDecomposition#f81f

```json
{
  "handle": "ConceptualDecomposition",
  "mechanism": "The cognitive act of taking a concept \u2014 typically a problem or task \u2014 and breaking it into sub-concepts where each sub-concept is bound by the {{solver}} contract (at minimum exposes a Manifest + Execute surface, so it is independently delegatable). Distinct from generic {{decompose}}: Decompose merely divides; ConceptualDecomposition divides *into solver-compatible units*. This is the intellectual move that enables recursive fractal structure \u2014 because child concepts conform to the same interface as the parent, the same five-surface contract governs every level. A few agents can assign these solver roles to themselves and perform lightweight fractal intelligence for a specific problem; the resulting structure may persist as a reusable pattern or be torn down at completion. The decomposition is passed through a {{decomposition_gate}} to validate Necessity, Independence, Universality, and Completeness before any child is spawned. Children compose back via {{synthesis}} once their individual results return.",
  "gloss": "Breaking a concept into solver-contract-bound sub-concepts \u2014 the move that enables fractal recursion",
  "invariants": [
    "Contract-binding: every sub-concept exposes the {{solver}} interface (Manifest + Execute mandatory).",
    "Gated: decompositions pass the {{decomposition_gate}} suite (Necessity, Independence, Universality, Completeness) before children are spawned.",
    "Recomposability: results of sub-concepts compose back to the parent concept via {{synthesis}}."
  ],
  "failure_modes": [
    "Premature decomposition: the parent concept is broken apart before it is clearly framed, producing sub-concepts that don't cover the actual problem.",
    "Non-orthogonal split: the decomposition overlaps itself; the {{decomposition_gate}} Independence test should catch this but does not if the overlap is semantic rather than structural.",
    "Contract violation: sub-concepts that do not cleanly expose Manifest + Execute cannot be dispatched \u2014 the decomposition produced descriptions, not delegatable units.",
    "Leaky abstraction: sub-concepts that require global context the Solver contract doesn't carry, forcing holographic-shard leakage."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ConceptualDecomposition#mh:SHA-256:f81fd419f086470d37223be58166e25c24f3c38c203689b673bc302a4a48ecfd",
  "sema_ref": "ConceptualDecomposition#f81f",
  "sema_stub": "f81f",
  "dependencies": {
    "composes_with": {
      "decomposition_gate": "DecompositionGate#7acd",
      "synthesis": "Synthesis#26b9"
    },
    "references": {
      "solver": "Solver#94ab",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## ConstructOntology#b45e

```json
{
  "handle": "ConstructOntology",
  "mechanism": "A primitive for building a structured set of concepts and relationships (an ontology) from raw data or seed axioms. It defines the 'physics' or 'rules' of a domain. This is the constructive counterpart to 'Adversarial Ontology Construction' (which is a methodology using this primitive). It builds the semantic graph from {{first_principles}}, validating edge coherence via {{adversarial_steel}} and establishing shared context through {{ontology_handshake}}.",
  "gloss": "Building a structured conceptual framework",
  "failure_modes": [
    "Incoherence: Contradictory axioms or definitions."
  ],
  "invariants": [
    "Completeness: All referenced terms are defined",
    "Consistency: No contradictions within the ontology"
  ],
  "preconditions": [
    "Seed concepts or data available"
  ],
  "postconditions": [
    "Valid ontology object created"
  ],
  "parameters": [
    {
      "name": "depth",
      "type": "Integer",
      "range": "[1, 10]",
      "description": "Hierarchical depth"
    },
    {
      "name": "format",
      "type": "Enum",
      "range": "{OWL, JSON-LD, Sema}",
      "description": "Output format"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ConstructOntology#mh:SHA-256:b45eccf2239933a795aa03d2a276385ec231b28c2daaf57eb1be31fd6ada2774",
  "sema_ref": "ConstructOntology#b45e",
  "sema_stub": "b45e",
  "dependencies": {
    "references": {
      "adversarial_steel": "AdversarialSteel#3b43",
      "ontology_handshake": "OntologyHandshake#46dc",
      "first_principles": "FirstPrinciples#634e"
    }
  }
}
```

---

## Decision#acfb

```json
{
  "handle": "Decision",
  "mechanism": "The cognitive act of committing to a specific {{option}} after weighing alternatives. It transforms a set of possibilities into a single committed trajectory using {{select}}. Unlike a simple filter, a Decision implies the resolution of ambiguity and the assumption of consequences.",
  "gloss": "Irrevocable selection from a set of options",
  "invariants": [
    "Selection: Must choose exactly one option from the available set.",
    "Irrevocability: Once made, the decision cannot be unmade without a new Decision process."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Decision#mh:SHA-256:acfb3458cde8e55c378b2f51b44afc30687b58093f1777299f49caca475274a1",
  "sema_ref": "Decision#acfb",
  "sema_stub": "acfb",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "data_schema": {
    "type": "object",
    "required": [
      "decision_id",
      "selected_option_id",
      "rationale"
    ],
    "properties": {
      "decision_id": {
        "type": "string"
      },
      "context_id": {
        "type": "string"
      },
      "options_considered": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of Option IDs rejected"
      },
      "selected_option_id": {
        "type": "string"
      },
      "rationale": {
        "type": "string",
        "description": "Reasoning trace for the selection"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "dependencies": {
    "references": {
      "option": "Option#483e",
      "select": "Select#15c2"
    }
  }
}
```

---

## Decompose#f900

```json
{
  "handle": "Decompose",
  "mechanism": "{{strategy}}: The cognitive act of splitting a {{task}} into independent subordinate parts. Criterion: solving each constituent {{problem}} in isolation must yield {{solution}} to the whole. If subproblems interact, the split is wrong\u2014try a different decomposition axis. Recurse until subproblems are trivial.",
  "gloss": "Dividing complexity into manageable units",
  "failure_modes": [
    "Coupling Leakage: Subproblems are not truly independent; solving one breaks another."
  ],
  "invariants": [
    "Subproblems must be independent."
  ],
  "preconditions": [
    "{{problem}} too large to solve directly. Decomposition axis identifiable. Subproblems can be independent."
  ],
  "postconditions": [
    "Set of independent subproblems. Combined {{solution}} equals original. No subproblem depends on sibling."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_ref": "Decompose#f900",
  "sema_id": "sema:Decompose#mh:SHA-256:f900a7797aecd575ace5c083610f2b060c9ddc238c1b7ced781c5d2e5f20c283",
  "sema_stub": "f900",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "problem": "Problem#4576",
      "solution": "Solution#fcea",
      "strategy": "Strategy#c4ba"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## DecompositionGate#7acd

```json
{
  "handle": "DecompositionGate",
  "mechanism": "The four-test decomposition suite applied as a Gate over candidate decompositions. The tests: Necessity (removing any sub-concept collapses the parent), Independence (sub-concepts vary orthogonally), Universality (every instance of the parent contains every sub-concept), Completeness (addressing all sub-concepts reconstructs a functioning parent). A decomposition passes only if all four tests pass \u2014 non-compensatory. Yields a {{decision}}: on failure, the Decision carries a {{frame_error}} instructing the upstream planner to reframe rather than iterate within the current decomposition.",
  "gloss": "Four-test gate for candidate decompositions: Necessity, Independence, Universality, Completeness",
  "invariants": [
    "Non-compensatory: a decomposition passes only if ALL four tests pass independently.",
    "Universality is strict: prototype-shaped concepts failing universality are rejected by design (intentional crucible, per paper \u00a72)."
  ],
  "failure_modes": [
    "Strict universality rejects legitimate prototype-shaped concepts that would succeed with family-resemblance semantics.",
    "Completeness test falsely rejects decompositions where reconstruction is possible but not fully characterized in the candidate."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:DecompositionGate#mh:SHA-256:7acd40ea02f33b168109eddbe579f31c3c601a243149f6eb5ce9d0973e757c97",
  "sema_ref": "DecompositionGate#7acd",
  "sema_stub": "7acd",
  "dependencies": {
    "yields": {
      "decision": "Decision#acfb"
    },
    "references": {
      "frame_error": "FrameError#168f"
    }
  }
}
```

---

## Deduction#9c88

```json
{
  "handle": "Deduction",
  "mechanism": "Moving from general rules ({{axiom}}) to specific conclusions. If premises are true, the conclusion MUST be true. (All men are mortal -> Socrates is a man -> Socrates is mortal).",
  "gloss": "General to specific logic",
  "invariants": [
    "Truth Preservation: If premises are true, conclusion MUST be true.",
    "Validity: The argument structure follows formal logic rules."
  ],
  "preconditions": [
    "Premises are accepted as true"
  ],
  "postconditions": [
    "Conclusion is logically necessary"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Deduction#mh:SHA-256:9c881288e30f01162b178b66fc1299a776dc08cc5add52ac8b31fe51d552dd12",
  "sema_ref": "Deduction#9c88",
  "sema_stub": "9c88",
  "dependencies": {
    "references": {
      "axiom": "Axiom#5012"
    }
  }
}
```

---

## DeepResearch#2a05

```json
{
  "handle": "DeepResearch",
  "mechanism": "An autonomous research pipeline with four stages: (1) Planning - decompose query into research questions, (2) Multi-Round Search - iteratively search, identify gaps, refine queries, (3) {{synthesis}} - integrate findings across sources, resolve contradictions, (4) Report - generate comprehensive analytical report with citations. The agent loops between search and synthesis until coverage is sufficient. It chains {{discover}} for breadth and {{retrieval_augment}} for depth, orchestrated by the {{deep}} primitive to ensure rigor.",
  "gloss": "Plan-search-synthesize-report research pipeline",
  "failure_modes": [
    "Source {{cognitive_bias}}: Over-relying on first sources found.",
    "{{synthesis}} Hallucination: Inventing connections not in sources.",
    "Premature Closure: Stopping search before finding contradicting evidence."
  ],
  "invariants": [
    "Information synthesized from multiple disparate sources",
    "Search depth > 1"
  ],
  "preconditions": [
    "Access to external knowledge base",
    "Broad user query"
  ],
  "postconditions": [
    "Citations included",
    "Comprehensive report generated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:DeepResearch#mh:SHA-256:2a05c141377ae0ee86a31cf03d41c91d64e4d4278e6a40e2d96707169aa702ba",
  "sema_ref": "DeepResearch#2a05",
  "sema_stub": "2a05",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Deep#89f0(Discover#7dbc)"
  ],
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "retrieval_augment": "RetrievalAugment#2ecb",
      "discover": "Discover#7dbc",
      "synthesis": "Synthesis#26b9",
      "deep": "Deep#89f0"
    }
  }
}
```

---

## Dialectic#5cc3

```json
{
  "handle": "Dialectic",
  "mechanism": "Internal reasoning process where an agent pits a Thesis against an Antithesis to generate a {{synthesis}}. Unlike Socratic questioning (which queries the user), Dialectic queries a simulated Critic Persona within the agent's own context. It instantiates a {{perspective_ensemble}} where one voice acts as Thesis and another uses {{steelman_check}} to construct the Antithesis.",
  "gloss": "Internal Thesis-Antithesis-Synthesis loop",
  "failure_modes": [
    "Infinite Regress: Thesis and Antithesis loop without converging.",
    "Strawman Critic: The generated Antithesis is too weak to improve the Thesis."
  ],
  "invariants": [
    "{{synthesis}} Quality: {{synthesis}} must resolve at least one contradiction found in Antithesis."
  ],
  "preconditions": [
    "Initial Thesis generated"
  ],
  "postconditions": [
    "Refined {{synthesis}} generated"
  ],
  "parameters": [
    {
      "name": "rounds",
      "type": "Integer",
      "range": "[1, 5]",
      "description": "Number of thesis-antithesis-synthesis cycles"
    },
    {
      "name": "temperature",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Divergence of antithesis generation (0 = conservative, 1 = radical)"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:Dialectic#mh:SHA-256:5cc39ffcdc6283b312a6d9cb84879d55f885d4db34e7fcbb2eb23a742fe6a068",
  "sema_ref": "Dialectic#5cc3",
  "sema_stub": "5cc3",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "synthesis": "Synthesis#26b9",
      "perspective_ensemble": "PerspectiveEnsemble#d08c"
    },
    "composes_with": {
      "steelman_check": "SteelmanCheck#7914"
    }
  }
}
```

---

## Eliminate#ee72

```json
{
  "handle": "Eliminate",
  "mechanism": "Systematic Exclusion (Sherlock Holmes): Enumerate all possible answers. For each, find a test that could falsify it. Apply tests in order of cost (cheapest first). Remove falsified options. Continue until one remains or no tests left. Remaining options are candidates. Combines {{deduction}} (ruling out what's impossible) with {{falsification}} (empirical testing of each hypothesis). It uses {{prioritize}} to order falsification tests by cost/efficiency before executing them.",
  "gloss": "Sherlock Holmes deduction via falsification",
  "failure_modes": [
    "Premature Exclusion: Eliminating the true cause because of a faulty test, leaving an empty set."
  ],
  "invariants": [
    "{{option}} set must be exhaustive at start."
  ],
  "preconditions": [
    "{{option}} set exhaustive. Falsification tests available. At least one option must survive."
  ],
  "postconditions": [
    "Remaining options equally valid. Eliminated options have falsifying evidence. Search space reduced."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_ref": "Eliminate#ee72",
  "sema_id": "sema:Eliminate#mh:SHA-256:ee7225dbf53ea3a8eec85f01afdd21dc4f90a14965935578bcf8ca8c5b6fedfd",
  "sema_stub": "ee72",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "deduction": "Deduction#9c88",
      "prioritize": "Prioritize#68f8",
      "option": "Option#483e",
      "falsification": "Falsification#4e23"
    }
  }
}
```

---

## Estimate#d1a0

```json
{
  "handle": "Estimate",
  "mechanism": "The predictive {{think}} process of calculating the probable {{value}} cost of a {{task}} before execution. It produces a resource cost projection. It has two modes: 1. {{heuristic_snap}} for fast, rough estimates (pattern matching), 2. {{simulation}} for accurate, expensive estimates (mental execution). The output is a {{bid}} with confidence intervals. Estimation itself consumes budget and is subject to the Meta-Cap invariant.",
  "gloss": "Predictive resource costing",
  "signature": [
    "Think#e1bd(Value#3c5d)"
  ],
  "failure_modes": [
    "Overconfidence: Narrow confidence intervals that don't reflect true uncertainty.",
    "Anchoring: Estimates biased by irrelevant prior information.",
    "Planning Fallacy: Systematic underestimation of time/cost.",
    "Meta-Cost Explosion: Spending more on estimation than the task is worth."
  ],
  "invariants": [
    "Calibration: Over time, actual costs should fall within stated confidence intervals.",
    "Meta-Bound: Estimation cost must be < 5% of estimated task cost.",
    "Uncertainty Honesty: Wide intervals for novel tasks, narrow for familiar."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "tier": 1,
    "ring": 1
  },
  "sema_ref": "Estimate#d1a0",
  "sema_id": "sema:Estimate#mh:SHA-256:d1a0ab03293b99bef71c3fe77d83d1ceb7b749ef1623dddabc07d368e0e16722",
  "sema_stub": "d1a0",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    },
    "yields": {
      "bid": "Bid#ef32"
    },
    "references": {
      "heuristic_snap": "HeuristicSnap#1ef2",
      "value": "Value#3c5d",
      "simulation": "Simulation#aa24"
    },
    "composes_with": {
      "think": "Think#e1bd"
    }
  }
}
```

---

## EthicalReasoningProtocol#04dc

```json
{
  "handle": "EthicalReasoningProtocol",
  "mechanism": "The paper's \u00a76.6 protocol. Applies {{conceptual_decomposition}} to right-action, producing a non-entangled pipeline that prevents the is-ought entanglement that corrupts monolithic moral reasoning. Operationalizes Hume's is-ought distinction as an architectural boundary: calculate, then think. A PredictionSolver outputs a typed PredictionLedger (branching future states with causal mechanisms and confidence envelopes) \u2014 constrained to pure description, no single point forecast. Downstream, a ValuationSolver evaluates 'which causal pathways matter, at what confidence, over what horizon' and emits a typed ScoreSheet \u2014 quantitative ranking no normative consideration has yet touched. Crucially, a PrincipleSolver acts as both an acceptance gate and a formal override: if a top-ranked option trips a sacred value, a catastrophic tail risk, or a procedural precedent, it emits a typed JudgmentNote overriding the numerical scoring. The final DecisionRecord has two distinct layers \u2014 quantitative base and qualitative override \u2014 segregated and independently auditable. This is the contract's override-with-documentation mechanism applied to ethics: the override is not an escape from the architecture but a first-class artifact within it. Composes with {{deliberative_align}} for constitutional grounding.",
  "gloss": "Separate prediction (is) from valuation (ought) from principle (override), each behind a typed boundary \u2014 the DecisionRecord has auditable empirical and normative layers",
  "invariants": [
    "Is-ought boundary: PredictionSolver output is constrained to pure description (PredictionLedger); no normative consideration contaminates the empirical forecast.",
    "Override-as-first-class: principle overrides do not adjust prediction weights silently \u2014 they emit a typed JudgmentNote that appears in the auditable DecisionRecord.",
    "Two-layer DecisionRecord: the empirical base (what the forecast said) and the qualitative override (why we diverged) remain independently inspectable; no collapse into a single verdict."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "caution": "Required at autonomous-system decision points where both forecast quality and normative legitimacy must be auditable. Collapsing prediction and valuation into one pass re-introduces smuggled normativity \u2014 the failure this protocol exists to prevent."
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:EthicalReasoningProtocol#mh:SHA-256:04dc0b30cbf3794fc03222c6dbd8e3b1a618305a0604c1fa024b9be53ce36027",
  "sema_ref": "EthicalReasoningProtocol#04dc",
  "sema_stub": "04dc",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f"
    },
    "references": {
      "deliberative_align": "DeliberativeAlign#e6cb"
    }
  }
}
```

---

## Expansive#3af7

```json
{
  "handle": "Expansive",
  "gloss": "Evaluates generalization potential",
  "mechanism": "A {{judge}} of generalization potential: does the mechanism or concept transfer beyond the original domain it was designed in? Applies wherever breadth-of-application is the evaluative question \u2014 scientific generality, platform reuse, pattern-library transferability, business model cross-market viability. The essential move is stress-testing the artifact against domains deliberately outside its origin (hostile-domain probe) rather than demonstrating it on familiar cases. Specific rating semantics belong on descendants or on the composing protocol. The signature Judge({{value}}) captures that the output is a {{value}}-graded breadth score rather than a binary transferable/not-transferable verdict.",
  "invariants": [
    "Transfer: Must operate outside training distribution."
  ],
  "signature": [
    "Judge#9554(Value#3c5d)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Expansive#mh:SHA-256:3af77b1960458d1cba5bb4a66d570ec3e9cb90746fbd6b5c5754eb697c32b816",
  "sema_ref": "Expansive#3af7",
  "sema_stub": "3af7",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "judge": "Judge#9554"
    }
  }
}
```

---

## ExtendedThinking#a49a

```json
{
  "handle": "ExtendedThinking",
  "mechanism": "Inference-time compute scaling where the model generates extended reasoning traces (potentially thousands of tokens) before producing a final answer. Unlike standard {{chain}}-of-Thought, this pattern explicitly trades latency and compute cost for accuracy by allowing the model to 'think longer'. The reasoning budget can be user-controlled or adaptive based on {{task}} complexity.",
  "gloss": "Scale inference compute via extended reasoning",
  "failure_modes": [
    "Confabulation Chains: Long reasoning traces that sound plausible but contain errors.",
    "Overthinking: Spending compute on simple problems that don't benefit.",
    "Hidden Reasoning: Model reaches conclusions via paths not shown in the trace."
  ],
  "invariants": [
    "Intermediate steps visible/logged",
    "Thinking time proportional to problem difficulty"
  ],
  "preconditions": [
    "Complex prompt",
    "High token budget"
  ],
  "postconditions": [
    "High-accuracy answer"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ExtendedThinking#mh:SHA-256:a49a3d3a17a896fd57909b94703df42c59adb6445058e2e0f05a03d87b356ace",
  "sema_ref": "ExtendedThinking#a49a",
  "sema_stub": "a49a",
  "dependencies": {
    "references": {
      "chain": "Chain#711e"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## Fermi#b302

```json
{
  "handle": "Fermi",
  "mechanism": "Decomposed Estimation: break unknown quantity into factors you can {{estimate}}. Multiply factors. Accept order-of-magnitude accuracy. Example: \"pianos in Chicago\" = population \u00d7 household fraction \u00d7 piano-owning fraction. Errors often cancel across factors. It invokes {{decompose}} to break an unknown quantity into estimable sub-factors.",
  "gloss": "Estimation via decomposition",
  "failure_modes": [
    "Correlated Error Stacking: If all sub-estimates are biased in the same direction (e.g., all optimistic), the errors compound rather than cancel."
  ],
  "invariants": [
    "Error Cancellation: Overestimation in sub-factors tends to cancel underestimation",
    "Geometric Mean: Final estimate is geometric mean of bounds"
  ],
  "parameters": [
    {
      "name": "confidence_interval",
      "type": "Percentage",
      "range": "[50%, 95%]",
      "description": "Target coverage of true value"
    },
    {
      "name": "decomposition_depth",
      "type": "Integer",
      "range": "[2, 6]",
      "description": "Estimation chain length"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:Fermi#mh:SHA-256:b30250570634f0d8573c0f509fccbf5cdce0ddc1f59390525880ad27770f5831",
  "sema_ref": "Fermi#b302",
  "sema_stub": "b302",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "estimate": "Estimate#d1a0",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## FirstPrinciples#634e

```json
{
  "handle": "FirstPrinciples",
  "mechanism": "Axiomatic Reconstruction: Strip away {{assumption}}s until reaching fundamental truths that cannot be deduced from anything else. Rebuild solution from these {{axiom}}s only. Reject inherited solutions; derive from scratch. It rebuilds the argument from bedrock using {{chain_of_thought}}, explicitly rejecting any cached or inherited {{assumption}}s.",
  "gloss": "Axiomatic reconstruction of truth",
  "failure_modes": [
    "Infinite Regress: Wasting resources proving 1+1=2 instead of solving the actual logistics problem."
  ],
  "invariants": [
    "Axioms cannot be derived from other statements."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:FirstPrinciples#mh:SHA-256:634e4087a278cc53ab306b4510ad0dfba3786f33cebb2ad61807d1e91ff503fb",
  "sema_ref": "FirstPrinciples#634e",
  "sema_stub": "634e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "chain_of_thought": "ChainOfThought#c3cd",
      "assumption": "Assumption#efb5",
      "axiom": "Axiom#5012"
    }
  }
}
```

---

## FrameError#168f

```json
{
  "handle": "FrameError",
  "mechanism": "A typed failure signaling that an acceptance gate rejection requires lateral reframing of the problem rather than retry. Produced by an {{accept_spec}} when a non-compensatory gate fails, the FrameError carries the specific gate that rejected and a reframing hint pointing the upstream planner toward a different frame. Distinct from transient failures (which warrant {{retry}}) and from compensable failures (which warrant {{compensate}}): a FrameError asserts that the current frame is wrong, not that execution went wrong.",
  "gloss": "Typed failure signaling that lateral reframing, not retry, is required",
  "invariants": [
    "A FrameError from a child forces the parent to restructure its approach, not re-execute.",
    "Must carry identification of the rejecting gate and a reframing hint \u2014 a bare FrameError without context is actionable only as 'halt'."
  ],
  "failure_modes": [
    "Receiving Solver treats FrameError as a generic failure and retries, wasting budget on the wrong frame.",
    "Missing reframing hint leaves the parent Solver unable to select a new approach \u2014 degenerates to halt.",
    "Cascaded FrameErrors without dampening cause thrash between frames."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:FrameError#mh:SHA-256:168fcdc757dce95ceca470ad01c7f647d458640e71cff2ea1b2f45ed04d7ea0f",
  "sema_ref": "FrameError#168f",
  "sema_stub": "168f",
  "dependencies": {
    "references": {
      "accept_spec": "AcceptSpec#7caa",
      "retry": "Retry#4cc6",
      "compensate": "Compensate#283e"
    }
  }
}
```

---

## Generalize#6dea

```json
{
  "handle": "Generalize",
  "mechanism": "Pattern Extraction: Given multiple instances, identify shared structure. Replace specific values with variables. {{state}} the invariant that holds across all instances. Test: does pattern predict behavior of new instances? Refine until predictive. The canonical form of {{induction}} in sema's reasoning taxonomy \u2014 probable conclusions from specific observations. It employs {{analogy_bridge}} to map specific instances to abstract schemata, validating the invariant across the set.",
  "gloss": "Inductive pattern extraction",
  "failure_modes": [
    "Overfitting: extracting a pattern that includes noise/coincidence."
  ],
  "invariants": [
    "Abstract rule covers all specific examples",
    "Information loss minimized"
  ],
  "preconditions": [
    "Set of specific instances"
  ],
  "postconditions": [
    "General principle extracted"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "Specialize#0ac5"
    ],
    "ring": 2
  },
  "sema_id": "sema:Generalize#mh:SHA-256:6dea8c6d33fa265c8f0ca75ca5684a452b55892d38d9351440a2a1dad5fe8508",
  "sema_ref": "Generalize#6dea",
  "sema_stub": "6dea",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "analogy_bridge": "AnalogyBridge#ddb2",
      "induction": "Induction#2487",
      "state": "State#4d58"
    }
  }
}
```

---

## GraphOfThought#8dfe

```json
{
  "handle": "GraphOfThought",
  "mechanism": "The canonical implementation of graph-structured reasoning. Instantiates the {{think}} primitive with a {{d_a_g}} topology so that inference steps can have multiple predecessors and multiple successors \u2014 nodes that converge from different reasoning branches can unify mid-computation without forcing a tree shape. Complements ChainOfThought (linear), TreeOfThoughts (branching without merge), and SkeletonOfThought (outline-parallel expansion). Used when distinct lines of reasoning should feed into shared intermediate conclusions \u2014 common in proof assistants, complex debugging, and multi-hypothesis analysis where evidence from branch A refines node X shared with branch B.",
  "gloss": "Graph-structured reasoning (Macro for Think(DAG))",
  "invariants": [
    "Acyclicity inherited from {{d_a_g}}: no reasoning step is its own ancestor.",
    "Fan-in permitted: a node may have multiple parent inferences, modeling evidence convergence.",
    "Each node applies {{think}} once; repeated re-evaluation is a caller concern, not a topology property."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(DAG#de34)"
  ],
  "sema_id": "sema:GraphOfThought#mh:SHA-256:8dfec59bcbcbc8b3a3809eadea4665f6039781b329c02f0151598008e3fea64d",
  "sema_ref": "GraphOfThought#8dfe",
  "sema_stub": "8dfe",
  "dependencies": {
    "composes_with": {
      "think": "Think#e1bd",
      "dag": "DAG#de34"
    }
  }
}
```

---

## HeuristicSnap#1ef2

```json
{
  "handle": "HeuristicSnap",
  "mechanism": "Fast pattern matching against a {{cache}} of past experiences. Returns a decision in <100ms based on similarity to past success, bypassing expensive reasoning chains. It bypasses the expensive {{chain_of_thought}} when {{budget}} is low, relying on cached pattern matches.",
  "gloss": "Rapid, low-cost decision making via pattern recognition",
  "invariants": [
    "Confidence Floor: Do not snap if similarity < 0.6",
    "Speed over Accuracy: Latency must be < Threshold"
  ],
  "preconditions": [
    "{{problem}} is familiar (exists in cache)"
  ],
  "postconditions": [
    "{{decision}} made instantly"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "ThinSlice#bc19"
    ],
    "ring": 2
  },
  "sema_id": "sema:HeuristicSnap#mh:SHA-256:1ef26959756fe03dbaa817bdfac248a7c962ce30eebda6af29b5eeb2773b6fcf",
  "sema_ref": "HeuristicSnap#1ef2",
  "sema_stub": "1ef2",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "chain_of_thought": "ChainOfThought#c3cd",
      "cache": "Cache#cd97",
      "decision": "Decision#acfb",
      "problem": "Problem#4576"
    }
  }
}
```

---

## HumanEmulatorProtocol#498a

```json
{
  "handle": "HumanEmulatorProtocol",
  "mechanism": "The paper's \u00a76.2 protocol for responding to a person with variable depth: 'How should I respond to this person?' Decomposes via {{conceptual_decomposition}} into five sub-questions that suppress each other when entangled in a single context: situation (what is the context), emotion (what do they feel), intent (what do they actually need, distinct from what they say), response (what should I say), and boundary (what must I not do). Each sub-question is handled by its own Solver with its own typed outputs \u2014 SituationSolver reconstructs relational dynamics, EmotionSolver produces a structured emotional model rather than a sentiment label, IntentSolver distinguishes stated from latent need, a CalibrationSolver fits tone and register, a BoundarySolver enforces ethical constraints as a hard acceptance gate. These faculties are co-variant state monitors (not a relay race): an emotional spike changes the intent distribution; a resolved intent reframes the emotional reading. Depth scales with the stakes under {{marginal_value_rule}} \u2014 a trivial greeting resolves in one pass; a crisis triggers deep recursion into competing emotional hypotheses and latent-intent analysis.",
  "gloss": "Decompose empathetic understanding into situation, emotion, intent, response, and boundary \u2014 variable-depth recursion tracks the stakes of the interaction",
  "invariants": [
    "Five-faculty orthogonal: the sub-concepts pass the four-test decomposition; entangling them in one context causes mutual interference.",
    "Variable-depth: mundane interactions stay shallow; ambiguous or high-stakes ones recurse into sub-solvers without changing the protocol.",
    "Boundary-gate: the BoundarySolver's output is a non-compensatory gate; no response passes if an ethical constraint is violated, regardless of other faculties' signals."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:HumanEmulatorProtocol#mh:SHA-256:498a8b232e4360c803db49d769b152576b65a5b6fea37f018aa540d0fae16517",
  "sema_ref": "HumanEmulatorProtocol#498a",
  "sema_stub": "498a",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f",
      "marginal_value_rule": "MarginalValueRule#32ce"
    }
  }
}
```

---

## Induction#2487

```json
{
  "handle": "Induction",
  "mechanism": "Moving from specific observations ({{datum}}) to general rules. The conclusion is probable, not certain. (The sun rose today -> The sun rises every day).",
  "gloss": "Specific to general logic",
  "invariants": [
    "Probabilistic: Conclusions are probable, not certain.",
    "Generalization: Output rule covers more cases than Input data."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Induction#mh:SHA-256:2487959ee211affb6f6ec74764316eb616e33c815603cf12b59518ab0bcfca54",
  "sema_ref": "Induction#2487",
  "sema_stub": "2487",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Interpret#c9ee

```json
{
  "handle": "Interpret",
  "gloss": "Deriving semantic meaning from raw signal",
  "mechanism": "The cognitive {{think}} act of applying a semantic {{context}} to a raw {{datum}} or {{signal}} to extract {{value}}. Unlike `Translate` (which changes form), Interpret changes the abstraction level, moving from syntax to semantics.",
  "signature": [
    "Think#e1bd(Value#3c5d)"
  ],
  "invariants": [
    "Context Dependency: Meaning(Signal) depends on Context.",
    "Non-Destructive: The original signal is preserved."
  ],
  "_meta": {
    "tier": 0,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 0
  },
  "sema_ref": "Interpret#c9ee",
  "sema_id": "sema:Interpret#mh:SHA-256:c9ee95cb7bd89112c0976c66c31f75cabf366786a388ff3c2b35145890a05c3f",
  "sema_stub": "c9ee",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "accepts": {
      "signal": "Signal#f39d",
      "datum": "Datum#31cf"
    },
    "yields": {
      "value": "Value#3c5d"
    },
    "composes_with": {
      "think": "Think#e1bd",
      "context": "Context#510a"
    }
  }
}
```

---

## Invert#b0a8

```json
{
  "handle": "Invert",
  "mechanism": "Opposition Solve: Instead of asking \"how do I achieve X?\", ask \"how would I guarantee failure at X?\" or \"how would I achieve NOT-X?\". List answers. Invert each answer to get candidate {{solution}}s for original {{problem}}. Often reveals blind spots. It applies {{reframe}} by negating the goal {{state}}, solving for failure to identify necessary conditions for success.",
  "gloss": "Solution discovery via negation",
  "failure_modes": [
    "False Dichotomy: Assuming the opposite of Failure is Success (it might just be Mediocrity)."
  ],
  "invariants": [
    "Inversion must be logical negation, not just opposite.",
    "Double Negation: Invert(Invert(X)) implies X."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Invert#mh:SHA-256:b0a8f903d3e95ab61fcce937631c354c5e7297e7971dfe1063ed581b84b56f83",
  "sema_ref": "Invert#b0a8",
  "sema_stub": "b0a8",
  "dependencies": {
    "accepts": {
      "solution": "Solution#fcea"
    },
    "references": {
      "state": "State#4d58",
      "problem": "Problem#4576",
      "reframe": "Reframe#0b02"
    }
  }
}
```

---

## LeastToMost#4c5e

```json
{
  "handle": "LeastToMost",
  "mechanism": "A prompting strategy that breaks a complex {{task}} into a series of simpler subproblems, then solves them in sequence. Each subproblem's solution becomes context for the next. Unlike standard decomposition, the subproblems are ordered from easiest to hardest, and solutions explicitly build on each other. It employs {{decompose}} to sort sub-tasks by complexity, solving them sequentially.",
  "gloss": "Solve subproblems from easiest to hardest sequentially",
  "failure_modes": [
    "Subproblem Coupling: Later subproblems depend on earlier errors.",
    "Ordering Misjudgment: Wrong difficulty ordering leads to missing prerequisites.",
    "Overhead: Simple problems don't benefit from decomposition."
  ],
  "invariants": [
    "{{solution}} to P(i) enables P(i+1)",
    "Subproblems solved in order of dependency"
  ],
  "preconditions": [
    "Complex problem",
    "Decomposition strategy"
  ],
  "postconditions": [
    "Full solution built from simple parts"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "RecursionDive#9c9f"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:LeastToMost#mh:SHA-256:4c5eb5bf4040a26caccae95eb991a4930cb98dd471c82ae1904bfffdac2a3cf0",
  "sema_ref": "LeastToMost#4c5e",
  "sema_stub": "4c5e",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    },
    "references": {
      "solution": "Solution#fcea",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## LivedProof#a8a8

```json
{
  "handle": "LivedProof",
  "mechanism": "Recursive Validation. A rhetorical or epistemic structure where the `Process` used to generate an output serves as the primary `Evidence` for the output's validity. The agent does not just assert a claim; it enacts it during the generation. It requires the agent to {{dogfood_first}}, treating the execution process as a {{signal}} of validity.",
  "gloss": "Process demonstrates thesis",
  "failure_modes": [
    "Performative Contradiction: The process contradicts the thesis (e.g., writing a 50-page essay on 'Brevity').",
    "Staged Demo: The process looks like enactment but is actually a pre-canned script (loss of genuineness)."
  ],
  "invariants": [
    "{{identity}}: Process == Evidence.",
    "Real-Time: The demonstration must occur during the current execution context, not historically.",
    "Traceability: Output artifacts must cryptographically reference their generation trace."
  ],
  "preconditions": [
    "{{agent}} has capability to execute the process",
    "Thesis allows for enactment"
  ],
  "postconditions": [
    "Epistemic Confidence set to MAX",
    "Performative Consistency verified"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:LivedProof#mh:SHA-256:a8a8d29323ac5629e9fdc4bc68eebf1268932b063a7f04051ee8484bce2afb77",
  "sema_ref": "LivedProof#a8a8",
  "sema_stub": "a8a8",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "dogfood_first": "DogfoodFirst#2538",
      "agent": "Agent#35b9",
      "identity": "Identity#626c"
    }
  }
}
```

---

## MetaPrompt#0ffe

```json
{
  "handle": "MetaPrompt",
  "mechanism": "A higher-order {{meta}} {{prompt}}ing technique where prompts are used to generate, refine, or analyze other prompts rather than directly answering questions. The LLM acts as a prompt engineer, creating task-specific prompts from templates or improving existing prompts through critique. Enables reusable prompt templates that generalize across problem categories. It constructs a {{prompt_chain}} where the output of the first stage is the prompt instruction for the second.",
  "gloss": "Use prompts to generate or refine other prompts",
  "failure_modes": [
    "{{prompt}} Drift: Generated prompts diverge from intent over iterations.",
    "{{meta}}-Complexity: {{meta}}-prompt harder to write than direct prompt.",
    "Overfitting: Generated prompts too specific to examples."
  ],
  "invariants": [
    "Output is a prompt",
    "{{prompt}} instructs how to prompt"
  ],
  "preconditions": [
    "{{prompt}} engineering principles",
    "{{task}} description"
  ],
  "postconditions": [
    "Optimized prompt generated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:MetaPrompt#mh:SHA-256:0ffe5ca9c9f64da9ffda1aff9940f0fd3c8ce3a4156b54ae029a645074e3d7ba",
  "sema_ref": "MetaPrompt#0ffe",
  "sema_stub": "0ffe",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Meta#90f4(Prompt#b18a)"
  ],
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "task": "Task#b328",
      "prompt": "Prompt#b18a",
      "prompt_chain": "PromptChain#8c63"
    }
  }
}
```

---

## Parsimony#8476

```json
{
  "handle": "Parsimony",
  "mechanism": "A {{judge}} of structural necessity (Occam's Razor): does the minimum-complexity form of the artifact still perform its function? Applies wherever a definition, model, design, or decomposition needs to be tested for excess parts. The essential move is ablation \u2014 remove a component and see if the whole collapses \u2014 which works on theories, codebases, system designs, and cognitive schemas alike. Specific rating semantics (binary pass/fail, traffic-light ranges, ordinal ablation scores) belong on descendants or on the composing protocol; Parsimony itself names only the question and the ablation discipline. The signature Judge({{topology}}) reflects that the question operates over structural shape rather than quantitative score; an ablation is itself a topology operation, removing nodes and seeing whether the remaining shape still performs.",
  "invariants": [
    "Necessity: Every component must have a causal link to the outcome."
  ],
  "signature": [
    "Judge#9554(Topology#2408)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Parsimony#mh:SHA-256:8476f22b05650925a08c5fff7488533529e047848b7c092e7b6524f52f3a063e",
  "sema_ref": "Parsimony#8476",
  "sema_stub": "8476",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "gloss": "Complexity justification via Occams Razor",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "judge": "Judge#9554"
    }
  }
}
```

---

## PatternDiscovery#196e

```json
{
  "handle": "PatternDiscovery",
  "mechanism": "Macro for {{search}}(Pattern). Vocabulary Hygiene {{protocol}}. Before minting a new pattern, the {{agent}} MUST execute a {{latent_attachment}}-backed semantic search against the existing registry. If a pattern with >85% semantic similarity is found, the {{agent}} MUST adopt the existing pattern or explicitly justify the divergence (Fork). It leverages {{search}} to scan the existing registry before triggering {{construct_ontology}} to mint a new definition.",
  "gloss": "Finding patterns that already exist",
  "failure_modes": [
    "Not Invented Here (NIH): {{agent}} ignores existing solutions to create a slightly worse custom version.",
    "Keyword Miss: Search fails because the agent used different terminology for the same concept.",
    "Fragmentation: Vocabulary floods with duplicate 'Micro-Patterns'."
  ],
  "invariants": [
    "Deduplication: If Similarity(New, Existing) > Threshold, Mint is blocked.",
    "Pre-Mint {{check}}: Minting is forbidden without a prior Search log."
  ],
  "preconditions": [
    "Intent to define new concept",
    "Registry access available"
  ],
  "postconditions": [
    "Existing Pattern Returned OR New Pattern Minted"
  ],
  "parameters": [
    {
      "name": "search_method",
      "type": "Enum",
      "range": "{Vector#c7c4, Keyword, Hybrid}",
      "description": "Default: Hybrid"
    },
    {
      "name": "similarity_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Default: 0.85"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:PatternDiscovery#mh:SHA-256:196e77d697c4a7eed0698d138eba4ec2c1a939e11fcf899b55852e595703a5b2",
  "sema_ref": "PatternDiscovery#196e",
  "sema_stub": "196e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "construct_ontology": "ConstructOntology#b45e",
      "latent_attachment": "LatentAttachment#ab68",
      "protocol": "Protocol#7e1c",
      "search": "Search#c5f4",
      "agent": "Agent#35b9",
      "check": "Check#d3e8"
    }
  }
}
```

---

## Rank#7a76

```json
{
  "handle": "Rank",
  "mechanism": "Deterministic Sort. Applies a caller-supplied {{scoring_function}} to every element in the input Set and returns a List ordered by Score. Uses {{select}} to truncate to Top-K when requested.",
  "gloss": "Order items by score",
  "failure_modes": [
    "Score Indeterminacy: Multiple items have identical scores.",
    "Incomparability: Scoring function returns values that cannot be strictly ordered."
  ],
  "invariants": [
    "Conservation: Output set is a subset of Input set.",
    "Monotonicity: For all i, Score(Output[i]) >= Score(Output[i+1])."
  ],
  "sema_id": "sema:Rank#mh:SHA-256:7a76c5fdee1e9cbf69fbdee2cb56796594c56b5285ad9cd3fbd8903430407a11",
  "sema_ref": "Rank#7a76",
  "sema_stub": "7a76",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 0
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "accepts": {
      "scoring_function": "ScoringFunction#3a4e"
    },
    "composes_with": {
      "select": "Select#15c2"
    }
  }
}
```

---

## ReAct#e018

```json
{
  "handle": "ReAct",
  "mechanism": "An interleaved reasoning-action loop where the agent cycles through Thought (reason about the situation), Action (invoke a tool or take a step), and Observation (process the result). Unlike pure {{chain}}-of-Thought which reasons then answers, ReAct interleaves reasoning with environmental feedback, allowing the agent to adjust plans based on real-world results. It interleaves reasoning traces for a {{task}} with {{tool_invoke}} execution, updating the context with observation results.",
  "gloss": "Interleaved thought-action-observation cycle",
  "failure_modes": [
    "Observation Blindness: {{agent}} ignores observations and follows initial plan.",
    "{{loop}} Explosion: Endless thought-action cycles without termination.",
    "Action {{cognitive_bias}}: Jumping to actions without sufficient reasoning."
  ],
  "invariants": [
    "Action based on reasoning",
    "Cycle of Thought-Action-Observation"
  ],
  "preconditions": [
    "Environment access",
    "Goal"
  ],
  "postconditions": [
    "Goal reached or deemed impossible"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "Reflexion#eed9"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ReAct#mh:SHA-256:e018477e1f3381f9cfc0e66d9a24e4355b619288dae8873d3f657e0239eef6f8",
  "sema_ref": "ReAct#e018",
  "sema_stub": "e018",
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "cognitive_bias": "CognitiveBias#4b32",
      "chain": "Chain#711e",
      "agent": "Agent#35b9"
    },
    "accepts": {
      "task": "Task#b328"
    },
    "composes_with": {
      "tool_invoke": "ToolInvoke#4694"
    }
  }
}
```

---

## Realizable#8d81

```json
{
  "handle": "Realizable",
  "gloss": "Evaluates execution feasibility of a plan",
  "mechanism": "A {{judge}} of execution feasibility: can the declared artifact actually be built or enacted in the world it targets, given its stated inputs, {{step}}s, and constraints? Applies wherever a {{plan}} or design must be checked against physical, computational, or institutional reality \u2014 engineering feasibility, policy implementation, software design, research program scoping. The essential move is grounding every {{step}} in a primitive or sub-component that is itself realizable, recursively. Specific rating semantics belong on descendants or on the composing protocol. The signature Judge({{value}}) captures that the question yields a {{value}}-rating of feasibility, not a binary verdict \u2014 'mostly realizable with two unverified links' is a legitimate output.",
  "signature": [
    "Judge#9554(Value#3c5d)"
  ],
  "invariants": [
    "Causality: No step can precede its dependencies.",
    "Grounding: All leaf nodes must terminate in known primitives."
  ],
  "failure_modes": [
    "Hidden Complexity: A step looks simple ('Draw the rest of the owl') but contains unsolved sub-problems.",
    "Resource Blindness: The steps are logically sound but physically impossible given the budget."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_ref": "Realizable#8d81",
  "sema_id": "sema:Realizable#mh:SHA-256:8d81bed9f201197e0250330028c9d94142338f9a5e69ea83cf8abd417abce01b",
  "sema_stub": "8d81",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d",
      "value": "Value#3c5d",
      "judge": "Judge#9554",
      "step": "Step#5f22"
    }
  }
}
```

---

## Reason#5f30

```json
{
  "handle": "Reason",
  "mechanism": "Orchestrated cognition that chains multiple {{think}} steps using a specific {{topology}} (e.g., {{chain}} of Thought, {{tree}} of Thoughts). Transforms {{context}} into conclusions, plans, or decisions while respecting {{compute_budget}}. The bridge between atomic thinking and structured problem-solving.",
  "gloss": "Execute a cognitive topology",
  "failure_modes": [
    "Analysis Paralysis: Spending too much compute on a decision with diminishing returns.",
    "Circular Reasoning: The thought process loops back to the premise without progress.",
    "Context Window Overflow: The reasoning trace exceeds memory capacity."
  ],
  "invariants": [
    "Bounded Execution: Must respect {{compute_budget}} (time/token limits).",
    "Structure Adherence: Must follow the rules of the selected reasoning {{topology}}.",
    "Side-Effect Free: Reasoning itself does not change the external world."
  ],
  "preconditions": [
    "{{context}} contains sufficient information",
    "{{compute_budget}} is available"
  ],
  "postconditions": [
    "A conclusion, plan, or decision is generated",
    "Reasoning trace is appended to History"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "related": [
      "ChainOfThought#c3cd",
      "TreeOfThoughts#422f"
    ]
  },
  "sema_id": "sema:Reason#mh:SHA-256:5f302cf59accb5b8546344b12f0aeaa0e2d3e78efcdf332b5f526b721bbe5d47",
  "sema_ref": "Reason#5f30",
  "sema_stub": "5f30",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#67c0",
      "chain": "Chain#711e",
      "topology": "Topology#2408",
      "tree": "Tree#a5a3"
    },
    "composes_with": {
      "think": "Think#e1bd"
    },
    "accepts": {
      "context": "Context#510a"
    }
  }
}
```

---

## RecursionDive#9c9f

```json
{
  "handle": "RecursionDive",
  "mechanism": "Execution: The active process of traversing a {{solver_tree}} downwards. Accepts a {{solver_node}}, applies the strategy of {{decompose}} to its task, and generates child {{solver_node}}s.",
  "gloss": "Vertical traversal of the solution tree",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "related": [
      "SolutionNode#2b4a"
    ]
  },
  "sema_id": "sema:RecursionDive#mh:SHA-256:9c9f9dc6bafbb2c4ec66bac9ff515dc9089ed7140462b527579e279d14678917",
  "sema_ref": "RecursionDive#9c9f",
  "sema_stub": "9c9f",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "solver_tree": "SolverTree#5623",
      "solver_node": "SolverNode#26b1"
    },
    "composes_with": {
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## RecursiveRootCause#6dc1

```json
{
  "handle": "RecursiveRootCause",
  "mechanism": "Causal Drill: {{state}} the problem. Ask \"Why did this happen?\" Take the answer as new problem. Repeat N times (defined by depth parameter) (or until reaching actionable root). Each level moves from symptom toward cause. Stop when you reach something you can change. It iteratively asks 'why' to traverse the causal chain, using {{trace}} to validate provenance of each cause.",
  "gloss": "Recursive root cause analysis",
  "failure_modes": [
    "Single Track Blindness: Assuming a single linear chain of causality when the reality is a multi-factor mesh."
  ],
  "invariants": [
    "Answers must be factual, not speculative.",
    "Causality Chain: Step(N) must be the direct cause of Step(N-1).",
    "Termination: Recursion stops at actionable root or fundamental axiom."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "Bisect#88b3",
      "RecursionDive#9c9f"
    ],
    "ring": 2
  },
  "sema_id": "sema:RecursiveRootCause#mh:SHA-256:6dc1c6c6188891b7f40b08560272b1290dad04faf9f88185ae1b02550d8c6310",
  "sema_ref": "RecursiveRootCause#6dc1",
  "sema_stub": "6dc1",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "trace": "Trace#9057",
      "state": "State#4d58"
    }
  }
}
```

---

## Refine#aa34

```json
{
  "handle": "Refine",
  "mechanism": "Iteratively improves an {{artifact}} by applying {{critique}} to identify {{incongruity}}s and then performing {{act}}s of editing to resolve them. It cycles until the artifact meets a specific {{condition}} or quality threshold.",
  "gloss": "Iterative improvement loop",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1,
    "related": [
      "PhasedRefinement#5e09"
    ]
  },
  "sema_id": "sema:Refine#mh:SHA-256:aa34fbf94760e25dfce8df3e307a1556d1215e7005bd7cf1a9e94ad87864671c",
  "sema_ref": "Refine#aa34",
  "sema_stub": "aa34",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "critique": "Critique#4e43",
      "incongruity": "Incongruity#e98f",
      "condition": "Condition#cbd5",
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "act": "Act#5d55"
    }
  }
}
```

---

## Reflexion#eed9

```json
{
  "handle": "Reflexion",
  "mechanism": "A self-improvement loop where after completing a {{task}} attempt, the agent generates linguistic self-critique analyzing what went wrong with the {{plan}} regarding the {{goal}}, then uses this reflection as context for a retry. Unlike fine-tuning, the model is frozen\u2014improvement comes from explicit textual feedback stored in an episodic memory buffer. It writes self-critique to a {{scratchpad}} memory buffer, using this feedback to improve the next attempt.",
  "gloss": "Self-critique and retry after failure",
  "failure_modes": [
    "Shallow Reflection: {{critique}} is generic ('try harder') without actionable insight.",
    "Reflection Drift: Each retry diverges further from the goal.",
    "Premature Success: Declaring success before the task is actually solved."
  ],
  "invariants": [
    "Memory of error persists",
    "Self-correction based on past failure"
  ],
  "preconditions": [
    "Failed trial",
    "{{outcome}} signal"
  ],
  "postconditions": [
    "Improved policy/next trial"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "EvaluatorOptimizer#c776"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Reflexion#mh:SHA-256:eed982425602ec2038b52e9918aca8cf3f0c695caf514f6a7d71d049cf771836",
  "sema_ref": "Reflexion#eed9",
  "sema_stub": "eed9",
  "dependencies": {
    "references": {
      "outcome": "Outcome#144c",
      "critique": "Critique#4e43",
      "goal": "Goal#009e",
      "plan": "Plan#fd6d",
      "scratchpad": "Scratchpad#75bf"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## Reframe#0b02

```json
{
  "handle": "Reframe",
  "mechanism": "{{problem}} Rotation: Transform the {{problem}} statement by changing perspective, scope, or framing. This mechanism not only restructures the current solver tree but actively seeks a new solver root better aligned with the transformed problem. Techniques: invert the goal, change the subject, shift time horizon, alter constraints. A problem unsolvable in frame A may be trivial in frame B.",
  "gloss": "Changing perspective to restructure the tree and find a new solution root",
  "failure_modes": [
    "Frame Blindness: New frame has its own blind spots, trading one bias for another."
  ],
  "invariants": [
    "{{problem}} semantics preserved",
    "perspective shifted"
  ],
  "preconditions": [
    "Stuck problem state"
  ],
  "postconditions": [
    "New solution path visible"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "related": [
      "SolutionRoot",
      "SolutionTree"
    ]
  },
  "sema_id": "sema:Reframe#mh:SHA-256:0b02c55ef29a90499bf98668a0ef1f20ca89c3453a49878cb1a9f59f693fbe7c",
  "sema_ref": "Reframe#0b02",
  "sema_stub": "0b02",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "problem": "Problem#4576"
    }
  }
}
```

---

## RequestFraming#3865

```json
{
  "handle": "RequestFraming",
  "derived_from": "sema:Interpret",
  "gloss": "Clarify intent and constraints before planning",
  "mechanism": "The initial state of workflow orchestration. It performs the act of {{interpret}} by accepting a {{message}} and using {{think}} to {{understand}} the 'real ask' within the given {{context}} before committing resources. The pattern enforces {{context_first}}: no resource commitment is permitted until the frame is resolved. It clarifies constraints, success criteria, and hidden assumptions, producing a {{frame_spec}} artifact. It acts as a semantic firewall against vague or dangerous instructions.",
  "signature": [
    "Think#e1bd(FrameSpec#5558)"
  ],
  "invariants": [
    "Output must be a rigorous FrameSpec",
    "No resources committed to execution yet"
  ],
  "preconditions": [
    "Raw User Request",
    "Context available"
  ],
  "postconditions": [
    "FrameSpec artifact created",
    "Constraints explicit"
  ],
  "failure_modes": [
    "Misinterpretation: The agent clarifies the wrong ambiguity.",
    "Over-constraint: Adding unnecessary restrictions that kill innovation.",
    "Premature Optimization: Jumping to solutions before understanding the problem."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "related": [
      "Reframe#0b02",
      "Decompose#f900"
    ]
  },
  "sema_ref": "RequestFraming#3865",
  "sema_id": "sema:RequestFraming#mh:SHA-256:386590380876d4439ffd7f6e279bb078f8c85323d6e950b9c685c57b94ee1af9",
  "sema_stub": "3865",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "understand": "Understand#96d4",
      "think": "Think#e1bd"
    },
    "references": {
      "context": "Context#510a",
      "interpret": "Interpret#c9ee",
      "context_first": "ContextFirst#def7"
    },
    "yields": {
      "frame_spec": "FrameSpec#5558"
    },
    "accepts": {
      "message": "Message#f767"
    }
  }
}
```

---

## SelfConsistency#ca0d

```json
{
  "handle": "SelfConsistency",
  "mechanism": "A variance-reduction technique where the same query is processed N times independently (with temperature > 0), producing N candidate answers. The final answer is selected by majority {{aggregate}} (Mode). Exploits the intuition that correct reasoning paths are more likely to converge on the same answer than incorrect ones. It aggregates multiple reasoning paths via {{aggregate}} to determine the most robust answer.",
  "gloss": "Sample multiple reasoning chains, select by majority",
  "failure_modes": [
    "Consistent Wrongness: All N samples converge on the same incorrect answer (systematic bias).",
    "Cost Explosion: N samples means N times the compute cost."
  ],
  "invariants": [
    "Aggregation: Final answer determined by plurality or weighted aggregation",
    "Independence: Each sample must be generated without knowledge of others",
    "N >= 3: Minimum samples for meaningful convergence"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_ref": "SelfConsistency#ca0d",
  "sema_id": "sema:SelfConsistency#mh:SHA-256:ca0daec71df9c74d6f6db1acf2e2565887c36feb44254186ab3b307b2d689931",
  "sema_stub": "ca0d",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#7912"
    }
  }
}
```

---

## SkeletonOfThought#3842

```json
{
  "handle": "SkeletonOfThought",
  "mechanism": "The canonical implementation of parallel reasoning. Instantiates the '{{think}}' primitive with a '{{skeleton}}' topology. Generates an outline first (using {{decompose}}), then expands all points in parallel to minimize latency. It implements the {{think}} primitive by first generating a structural {{skeleton}} and then triggering parallel expansion.",
  "gloss": "Parallel outline expansion (Macro for Think(Skeleton))",
  "invariants": [
    "Structural Completeness: {{skeleton}} covers all required aspects; Point Independence: {{skeleton}} points can be expanded independently; Coherent Assembly: Final output reads as unified response"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:SkeletonOfThought#mh:SHA-256:3842af7607f84ffd709c0d95f6e36ec931466ad68e411de80dd277cece934389",
  "sema_ref": "SkeletonOfThought#3842",
  "sema_stub": "3842",
  "signature": [
    "Think#e1bd(Skeleton#c363)"
  ],
  "dependencies": {
    "references": {
      "skeleton": "Skeleton#c363",
      "think": "Think#e1bd",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## SocraticLoop#2913

```json
{
  "handle": "SocraticLoop",
  "mechanism": "Ambiguity detection loop. If Confidence({{prompt}}) < Threshold, {{agent}} pauses execution to query the user. {{loop}} continues until intent is disambiguated or max_questions reached. It engages the user in a {{dialectic}} exchange to progressively narrow the ambiguity space.",
  "gloss": "Clarification before generation",
  "failure_modes": [
    "User Fatigue: Too many questions cause user to abandon session.",
    "Premature Stop: {{agent}} accepts vague answer without fully resolving ambiguity.",
    "Annoying the user with too many questions."
  ],
  "invariants": [
    "Information Gain: Each Question(N) must reduce entropy of UserIntent.",
    "Diminishing Returns: Entropy_Delta(Question_N) must be < Entropy_Delta(Question_N-1).",
    "Termination: {{loop}} halts when Confidence > Threshold OR Iterations >= Limit."
  ],
  "preconditions": [
    "Ambiguity detected",
    "User prompt received"
  ],
  "postconditions": [
    "User intent disambiguated OR fallback to best-guess"
  ],
  "parameters": [
    {
      "name": "ambiguity_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Confidence below which the agent asks a clarifying question instead of acting"
    },
    {
      "name": "max_questions",
      "type": "Integer",
      "range": "[1, 3]",
      "description": "Maximum clarification questions before the agent must proceed"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:SocraticLoop#mh:SHA-256:2913255a08d47a4bdc3583f6b8905bb92b5573f3e51cb66cc603b2688f37f2dc",
  "sema_ref": "SocraticLoop#2913",
  "sema_stub": "2913",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "dialectic": "Dialectic#5cc3",
      "loop": "Loop#797f",
      "prompt": "Prompt#b18a",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Specialize#0ac5

```json
{
  "handle": "Specialize",
  "mechanism": "Concrete Instantiation: Given abstract principle, substitute specific values for variables. {{check}} all constraints still hold after substitution. Generate multiple specializations to understand the principle's range. Edge cases reveal hidden assumptions. The canonical form of {{deduction}} in sema's reasoning taxonomy \u2014 necessary conclusions from general premises. Inverse of {{generalize}}.",
  "gloss": "Deductive application of principles",
  "failure_modes": [
    "{{context}} Mismatch: Applying a valid principle to a domain where its preconditions do not hold."
  ],
  "invariants": [
    "Constraint Inheritance: Must satisfy all constraints of the general principle",
    "Type Narrowing: Input parameters are a subset of the general domain"
  ],
  "preconditions": [
    "Domain constraints",
    "General purpose agent"
  ],
  "postconditions": [
    "Expert agent instantiated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:Specialize#mh:SHA-256:0ac50ab993507fd6b7d5959ba18bcaeaa388a35705fdb4ff9d423165a6fb6a9e",
  "sema_ref": "Specialize#0ac5",
  "sema_stub": "0ac5",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "generalize": "Generalize#6dea",
      "deduction": "Deduction#9c88",
      "context": "Context#510a"
    }
  }
}
```

---

## SteelmanCheck#7914

```json
{
  "handle": "SteelmanCheck",
  "mechanism": "Before finalizing a {{decision}} or output, the {{agent}} MUST generate the strongest possible argument against its own conclusion. It performs a {{check}} on the {{robustness}} of the claim and a {{critique}} of the underlying {{belief}}. If the counter-argument exceeds a validity threshold, the decision is discarded or revised. It prevents confirmation {{cognitive_bias}}. Utilizes {{compatibility_check}}. For adversarial contexts, see adversarial steelmanning.",
  "gloss": "Post-decision adversarial check: revise if counter-argument exceeds validity threshold",
  "failure_modes": [
    "Paralysis by analysis (stuck in {{critique}} {{loop}}).",
    "Collusion: Proposer and Critic are same entity; susceptible to Strawman Waltz attack where agent generates weak counter-arguments to easily defeat them."
  ],
  "invariants": [
    "Counter-Argument Quality: Score(Counter) > 0.7 (Must be non-trivial)",
    "Passing critique required for release.",
    "Strongest Counter: Generated argument must address the core claim, not weak points",
    "Topical Relevance: EmbeddingDistance(Counter, Claim) < Threshold"
  ],
  "preconditions": [
    "{{agent}} must be alignment-seeking; use adversarial steelmanning for adversarial/untrusted contexts",
    "Claim is falsifiable"
  ],
  "postconditions": [
    "{{critique}} generated and scored"
  ],
  "parameters": [
    {
      "name": "iteration_limit",
      "type": "Integer",
      "range": "[1, 5]",
      "description": "Max strengthening attempts"
    },
    {
      "name": "strength_threshold",
      "type": "Float",
      "range": "[0.7, 0.95]",
      "description": "Min strength to pass as steelman"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "related": [
      "AdversarialSteel#3b43"
    ]
  },
  "sema_id": "sema:SteelmanCheck#mh:SHA-256:7914b0d58e4d2e364e6e5ec30702e5cd3ef24127c2c0be963ca79741f4a6f038",
  "sema_ref": "SteelmanCheck#7914",
  "sema_stub": "7914",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Check#d3e8(Robustness#132c)",
    "Critique#4e43(Belief#a9ce)"
  ],
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "belief": "Belief#a9ce",
      "cognitive_bias": "CognitiveBias#4b32",
      "critique": "Critique#4e43",
      "compatibility_check": "CompatibilityCheck#3abb",
      "robustness": "Robustness#132c",
      "agent": "Agent#35b9",
      "check": "Check#d3e8",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## StepBack#b16f

```json
{
  "handle": "StepBack",
  "mechanism": "A meta-cognitive {{think}} operation that pauses direct problem-solving to ask a higher-level question. Instead of answering 'How do I X?', it asks 'What category of {{problem}} is X?' or 'What principles govern X?'. This abstraction reveals structural patterns invisible at the ground level. It is the precursor to {{reframe}}\u2014gaining altitude before choosing a new direction.",
  "gloss": "Ascend abstraction to gain perspective",
  "failure_modes": [
    "Over-abstraction: Climbing so high the original problem becomes unrecognizable.",
    "Analysis Paralysis: Endless stepping back without returning to action.",
    "Premature Descent: Jumping back down before gaining useful perspective.",
    "Abstraction Mismatch: Wrong principles retrieved for the task."
  ],
  "invariants": [
    "Altitude Gain: Output must be at a higher abstraction level than input.",
    "Relevance: Higher-level insight must inform the original problem.",
    "Bounded: Maximum abstraction depth before forced descent."
  ],
  "preconditions": [
    "Specific question or problem"
  ],
  "postconditions": [
    "Answer grounded in high-level concepts",
    "Principles retrieved before details"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_id": "sema:StepBack#mh:SHA-256:b16f465c8085bd6e6c962bee774538fd7252e79b43c44bc7fecf4f41df15e66b",
  "sema_ref": "StepBack#b16f",
  "sema_stub": "b16f",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Problem#4576)"
  ],
  "dependencies": {
    "references": {
      "reframe": "Reframe#0b02",
      "problem": "Problem#4576",
      "think": "Think#e1bd"
    }
  }
}
```

---

## StrategicReading#37f7

```json
{
  "handle": "StrategicReading",
  "mechanism": "Non-linear Information Retrieval Heuristic. {{agent}} treats documents as random-access databases rather than linear streams. It builds a structural map first ({{tree}}), identifies high-entropy sections (Abstract/Conclusion), and selectively loads only the relevant chunks. Utilizes {{compute_budget}}.",
  "gloss": "Navigate like a researcher, not linearly",
  "failure_modes": [
    "{{context}} Overflow: Loading entire documents saturates memory, displacing instructions.",
    "Linear {{cognitive_bias}}: Reading irrelevant introductions while missing key results buried in appendices.",
    "Fragmented {{context}}: Jumping too aggressively leads to missing critical connective logic."
  ],
  "invariants": [
    "Budget Awareness: Read volume must be < 10% of total document size unless DeepRead approved.",
    "Structure First: Must execute `doc_get_tree` or `outline` before reading body content."
  ],
  "preconditions": [
    "Large document identified",
    "Specific information goal defined"
  ],
  "postconditions": [
    "Relevant sections extracted",
    "Remainder of document remains unloaded"
  ],
  "parameters": [
    {
      "name": "scan_depth",
      "type": "Integer",
      "range": "[1, 10]",
      "description": "Pages/sections to scan before deciding relevance"
    },
    {
      "name": "strategy",
      "type": "Enum",
      "range": "{Survey, DeepDive, Needle}",
      "description": "Default: Survey"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_ref": "StrategicReading#37f7",
  "sema_id": "sema:StrategicReading#mh:SHA-256:37f7cf168532f92e8090ccae70a18f5de5540141d26656f3ba2a3912fcdcbd08",
  "sema_stub": "37f7",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "compute_budget": "ComputeBudget#67c0",
      "context": "Context#510a",
      "agent": "Agent#35b9",
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## Summarize#db2a

```json
{
  "handle": "Summarize",
  "mechanism": "The cognitive process of {{compress}}ing a large {{datum}} or {{artifact}} into a smaller {{summary}} while preserving its most high-{{value}} (salient) information. Distinct from {{translate}}, which preserves the full semantic scope. It is a lossy transformation.",
  "gloss": "Lossy compression preserving salience",
  "invariants": [
    "Compression: Output size < Input size",
    "Salience: Information Density(Output) > Information Density(Input)",
    "Fidelity: No new information added (No hallucination)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Summarize#mh:SHA-256:db2aa85d9d829962696e8a9961faa4402123e3807b052545404c0251d1367f17",
  "sema_ref": "Summarize#db2a",
  "sema_stub": "db2a",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "yields": {
      "summary": "Summary#f785"
    },
    "references": {
      "value": "Value#3c5d",
      "compress": "Compress#0967",
      "translate": "Translate#a8ed",
      "artifact": "Artifact#6254"
    },
    "accepts": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Synthesis#26b9

```json
{
  "handle": "Synthesis",
  "mechanism": "The process of combining separate elements into a unified whole. The opposite of {{critique}} or Analysis. It constructs new meaning from parts.",
  "gloss": "Combining elements",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Synthesis#mh:SHA-256:26b9e3bc68112d12015efd608c76860f1a5a796c5171145eb2959627fee88a90",
  "sema_ref": "Synthesis#26b9",
  "sema_stub": "26b9",
  "dependencies": {
    "references": {
      "critique": "Critique#4e43"
    }
  }
}
```

---

## Think#e1bd

```json
{
  "handle": "Think",
  "mechanism": "A single cognitive step that transforms input {{context}} into a new {{datum}}. The atomic unit of reasoning\u2014one inference, one connection, one realization. Side-effect free and instantaneous from the perspective of the external world.",
  "gloss": "Atomic cognitive step",
  "failure_modes": [
    "Hallucination: Generating a conclusion that does not follow from the {{context}}.",
    "Premature Closure: Stopping at the first plausible insight without considering alternatives."
  ],
  "invariants": [
    "Side-Effect Free: Thinking does not change the external world.",
    "Context-Bound: Output must be derivable from input {{context}}."
  ],
  "preconditions": [
    "{{context}} is available"
  ],
  "postconditions": [
    "An insight or intermediate conclusion is produced"
  ],
  "_meta": {
    "tier": 0,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 0
  },
  "sema_id": "sema:Think#mh:SHA-256:e1bd11a90f512c09e3befc43359a01e827f20e278d7032ee962c81f883087d81",
  "sema_ref": "Think#e1bd",
  "sema_stub": "e1bd",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "accepts": {
      "context": "Context#510a"
    },
    "yields": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Translate#a8ed

```json
{
  "handle": "Translate",
  "mechanism": "The process of converting {{datum}} from one representation (Language, Format, {{protocol}}, Ontology) to target content while preserving its semantic meaning. It requires a Source Schema and a Target Schema. It is distinct from 'Summarize' (which loses information) and '{{interpret}}' (which adds meaning).",
  "gloss": "Convert form while preserving meaning",
  "failure_modes": [
    "Lossy Translation: Semantic nuance lost in conversion (e.g., 'Schadenfreude' -> 'Happy').",
    "Hallucination: Translator adds information not present in the source.",
    "Format Error: Output violates the strict syntax of the target schema."
  ],
  "invariants": [
    "Semantic Equivalence: Meaning(Source) == Meaning(Target).",
    "{{reversibility}}: In ideal cases, Translate(Target, Source) should recover the original (Round-trip)."
  ],
  "preconditions": [
    "Source data matches Source Schema",
    "Target Schema is well-defined"
  ],
  "postconditions": [
    "Output data matches Target Schema"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_id": "sema:Translate#mh:SHA-256:a8ed7420c21067b89162a9a857e1f892af7c9f60bbbef8a72e22439874528d0f",
  "sema_ref": "Translate#a8ed",
  "sema_stub": "a8ed",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "interpret": "Interpret#c9ee",
      "reversibility": "Reversibility#bf79",
      "protocol": "Protocol#7e1c"
    },
    "accepts": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## TreeOfThoughts#422f

```json
{
  "handle": "TreeOfThoughts",
  "mechanism": "The canonical implementation of branching reasoning. Instantiates the '{{think}}' primitive with a branching '{{tree}}' topology. Enables exploration of multiple reasoning paths with backtracking or pruning. Utilizes {{tree}}, {{chain_of_thought}}, {{think}}.",
  "gloss": "Branching exploration (Macro for Think(Tree))",
  "parameters": [
    {
      "name": "breadth",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Maximum parallel reasoning branches per node"
    },
    {
      "name": "depth",
      "type": "Integer",
      "range": "[1, 20]",
      "description": "Maximum reasoning tree depth"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "RecursionDive#9c9f"
    ],
    "ring": 2
  },
  "sema_id": "sema:TreeOfThoughts#mh:SHA-256:422f0e25e23054a4a06d03bf1b8d74b76eddc8c661053cacc7d29063d5a03888",
  "sema_ref": "TreeOfThoughts#422f",
  "sema_stub": "422f",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Tree#a5a3)"
  ],
  "dependencies": {
    "references": {
      "chain_of_thought": "ChainOfThought#c3cd",
      "think": "Think#e1bd",
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## Uncertain#0556

```json
{
  "handle": "Uncertain",
  "mechanism": "Epistemic Status Flag. Explicitly marks a Claim, {{variable}}, or Edge as 'Unknown'. Unlike 'Speculation' (which posits a direction), 'Uncertain' asserts a void of evidence. This prevents the system from treating absence of evidence as evidence of absence. Tagged nodes become high-priority targets for information retrieval. Tracked via {{uncertainty_map}}.",
  "gloss": "Epistemic status: genuinely don't know",
  "failure_modes": [
    "False Certainty: {{agent}} feels pressure to answer and fabricates a 'likely' answer instead of using this flag.",
    "Lazy Agnosticism: {{agent}} uses 'Uncertain' to avoid the work of reasoning (Tier 2 failure)."
  ],
  "invariants": [
    "Actionable Void: A node marked 'Uncertain' is a high-priority target for Information Retrieval.",
    "Specificity: Must target a specific scope (e.g., 'Uncertain about X', not just 'Uncertain')."
  ],
  "preconditions": [
    "Knowledge gap identified"
  ],
  "postconditions": [
    "Confidence score set to 0.0",
    "Target marked as requiring investigation"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Uncertain#mh:SHA-256:055685440eab69c23eb5f4311101380cdccc619fef955e3b843b59fc3c0a1e2a",
  "sema_ref": "Uncertain#0556",
  "sema_stub": "0556",
  "dependencies": {
    "references": {
      "uncertainty_map": "UncertaintyMap#516d",
      "variable": "Variable#179a",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Understand#96d4

```json
{
  "handle": "Understand",
  "mechanism": "The process of applying {{think}} to construct an internal model that accurately reflects the causal structure, semantics, and {{context}} of an input. It goes beyond simple parsing to grasp 'why' and 'how'.",
  "gloss": "Deep semantic modeling",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_id": "sema:Understand#mh:SHA-256:96d4533c4539cdd5036beadb506908d384e8f417449e02bbf8e6175e5bafc39b",
  "sema_ref": "Understand#96d4",
  "sema_stub": "96d4",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Context#510a)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#e1bd",
      "context": "Context#510a"
    }
  }
}
```

---

## Verification#19d6

```json
{
  "handle": "Verification",
  "mechanism": "The cognitive process of confirming that a claim or {{artifact}} adheres to its {{spec}} or reality. Unlike open-ended inquiry, Verification yields a binary Truth value regarding an existing assertion via a {{check}}.",
  "gloss": "Confirming alignment with truth or spec",
  "failure_modes": [
    "False positive: artifact accepted despite not meeting spec.",
    "False negative: valid artifact rejected due to overly strict or misapplied criteria."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_ref": "Verification#19d6",
  "sema_id": "sema:Verification#mh:SHA-256:19d69afb644ed6f5fbe94d3c1608101c12221e01b68dff2128848f8a56483fd2",
  "sema_stub": "19d6",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "artifact": "Artifact#6254",
      "spec": "Spec#a036"
    }
  }
}
```

---

## WhyClimb#88c7

```json
{
  "handle": "WhyClimb",
  "mechanism": "A root-cause analysis protocol where the agent iteratively asks 'Why is this a problem?' to {{reframe}} the {{problem}} and ascend the abstraction hierarchy. The goal is to reach the 'Ceiling'\u2014the highest level where the problem is still actionable but the solution space is maximized. Utilizes {{recursive_root_cause}}.",
  "gloss": "Recursive problem abstraction",
  "failure_modes": [
    "Climbing too high (solving 'Entropy' instead of 'Fix Bug')."
  ],
  "invariants": [
    "Ascension: Scope(Level N+1) > Scope(Level N)",
    "Stop {{condition}}: Halt when 'Why' leads to a value judgment or physics constraint"
  ],
  "preconditions": [
    "{{problem}} is well-formed"
  ],
  "postconditions": [
    "{{solution}} space expanded"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_id": "sema:WhyClimb#mh:SHA-256:88c7eeeb33806e5a058303cd34651bbc667c00d1af7cef67c093130ace9d7409",
  "sema_ref": "WhyClimb#88c7",
  "sema_stub": "88c7",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Reframe#0b02(Problem#4576)"
  ],
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "recursive_root_cause": "RecursiveRootCause#6dc1",
      "condition": "Condition#cbd5",
      "reframe": "Reframe#0b02",
      "problem": "Problem#4576"
    }
  }
}
```

---

## AdversarialSteel#3b43

```json
{
  "handle": "AdversarialSteel",
  "mechanism": "The {{meta}}-process for adversarial verification. Instead of a single judgment, the {{system}} spawns a 'green advocate' (who constructs the strongest case FOR the idea) and a 'red advocate' (who constructs the strongest case AGAINST). A third {{judge}} {{agent}} renders the verdict only after reviewing both steelmanned arguments. It orchestrates {{steelman_check}} to generate the opposing arguments and employs {{compatibility_check}} to ensure the pro, con, and {{judge}} {{agent}}s share a precise definition of the {{criteria}} before debate begins.",
  "gloss": "Dual-advocate verdict generation",
  "failure_modes": [
    "{{judge}} {{agent}} defaults to 'Both sides' compromise (Median Trap)."
  ],
  "invariants": [
    "Dual Representation: Verdict cannot be rendered without Pro + Con arguments",
    "Steelmanning: Red Argument strength > Weakest Link of Proposal"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "caution": "Spawned advocates share the same model \u2014 collusion risk."
  },
  "sema_id": "sema:AdversarialSteel#mh:SHA-256:3b43d987edb6b393fcbc10420354225cb1101b705a7256f6e1a32a143e6d1dbe",
  "sema_ref": "AdversarialSteel#3b43",
  "sema_stub": "3b43",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "criteria": "Criteria#ef6b",
      "meta": "Meta#90f4",
      "system": "System#e314",
      "compatibility_check": "CompatibilityCheck#3abb",
      "judge": "Judge#9554",
      "agent": "Agent#35b9"
    },
    "composes_with": {
      "steelman_check": "SteelmanCheck#7914"
    }
  }
}
```

---

## Agent#35b9

```json
{
  "handle": "Agent",
  "mechanism": "The fundamental unit of agency. An {{actor}} capable of perceiving its environment ({{observe}}), maintaining internal {{state}}, reasoning about that {{state}} ({{think}}), and executing {{act}} to achieve a {{goal}}. It operates in a continuous {{loop}}.",
  "gloss": "Autonomous Goal-Directed Entity",
  "failure_modes": [
    "{{goal}} Drift: The agent's optimization target shifts away from the user's intent.",
    "Reward Hacking: Finding shortcuts to maximize a {{metric}} without achieving the actual {{goal}}.",
    "Infinite {{loop}}: Getting stuck in a non-productive cycle.",
    "Hallucination: Acting based on false internal beliefs."
  ],
  "invariants": [
    "Agency: Must possess an explicit objective function.",
    "Autonomy: Must be capable of selection (choosing between >1 options).",
    "{{identity}} Persistence: The agent maintains a consistent identity (ID/Memory) across time steps."
  ],
  "preconditions": [
    "Environment is instantiated",
    "{{goal}} is defined",
    "Resources (Compute/Time) are allocated"
  ],
  "postconditions": [
    "{{goal}} is satisfied OR Agent is terminated",
    "{{trace}} of actions is preserved"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_ref": "Agent#35b9",
  "sema_id": "sema:Agent#mh:SHA-256:35b97b37325c6f065a2e78f0d3397fa4984289ca90ea63feaa9902f40cfac681",
  "sema_stub": "35b9",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "metric": "Metric#17fd",
      "loop": "Loop#797f",
      "state": "State#4d58",
      "goal": "Goal#009e",
      "actor": "Actor#6926",
      "identity": "Identity#626c",
      "trace": "Trace#9057"
    },
    "composes_with": {
      "observe": "Observe#39f0",
      "act": "Act#5d55",
      "think": "Think#e1bd"
    }
  }
}
```

---

## AnalogyBridge#ddb2

```json
{
  "handle": "AnalogyBridge",
  "mechanism": "To solve a novel {{problem}}, the {{agent}} uses {{latent_attachment}} to search its embedding space for a structural analogy in a different domain (e.g., 'This architecture problem is like an ant colony'). It maps the {{solution}} from the source domain to the target domain. It merges the structural properties of the source and target domains, identifying the isomorphic mapping.",
  "gloss": "Mapping to known solutions",
  "failure_modes": [
    "False analogy (mapping superficial similarities)."
  ],
  "invariants": [
    "Attribute Independence: Object attributes (color, size) are ignored",
    "Structure Mapping: Relations in Source must map to Relations in Target"
  ],
  "preconditions": [
    "Isomorphism exists"
  ],
  "postconditions": [
    "Inference transferred"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:AnalogyBridge#mh:SHA-256:ddb22c56410e1a3b64327940231213795520e9c0b1551e5c462bc8dd6c0fbabf",
  "sema_ref": "AnalogyBridge#ddb2",
  "sema_stub": "ddb2",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "latent_attachment": "LatentAttachment#ab68",
      "problem": "Problem#4576",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## AntifragileInversion#9920

```json
{
  "handle": "AntifragileInversion",
  "mechanism": "A design pattern that inverts the relationship with a stressor. If {{variable}} X causes harm, the {{agent}} redesigns the {{system}} such that {{variable}} X is the input fuel. It mathematically reverses the sign of the exposure {{vector}}. It systematically applies {{reframe}} to the {{system}}'s causal graph, identifying edges where the sign of the relationship between stress and utility can be flipped.",
  "gloss": "Converting volatility into fuel",
  "failure_modes": [
    "Fragility to stability ({{system}} starves without shocks)."
  ],
  "invariants": [
    "Causal Inversion: The stressor is a required input, not a tolerated noise",
    "Convexity: Gain(Shock) > Loss(Shock)"
  ],
  "preconditions": [
    "Stressor is unavoidable"
  ],
  "postconditions": [
    "{{system}} utility correlates positively with Stressor"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:AntifragileInversion#mh:SHA-256:992022c17aa4c575dc33251481f83cc7cd018925f60469f913e173ba6e63ec2a",
  "sema_ref": "AntifragileInversion#9920",
  "sema_stub": "9920",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "variable": "Variable#179a",
      "reframe": "Reframe#0b02",
      "system": "System#e314",
      "vector": "Vector#c7c4",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## BeamSearch#07bd

```json
{
  "handle": "BeamSearch",
  "mechanism": "A heuristic search algorithm that explores a graph by expanding the most promising {{solver_node}}s in a limited set (the beam). It manages a {{queue}} of fixed size 'k'. At each step, it generates all successors of all nodes in the beam, {{rank}}s them, and {{select}}s the top 'k' for the next iteration.",
  "gloss": "Width-limited heuristic search",
  "invariants": [
    "Breadth Constraint: Active nodes never exceed Beam Width.",
    "Optimality: The K nodes selected are the highest ranked."
  ],
  "parameters": [
    {
      "name": "beam_width",
      "type": "Integer",
      "range": "[1, 100]",
      "description": "Number of parallel paths to keep"
    }
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:BeamSearch#mh:SHA-256:07bd338de8c415d52fcb2e14c1df00689a9adb39fa44865915bcb082550ffd6c",
  "sema_ref": "BeamSearch#07bd",
  "sema_stub": "07bd",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "queue": "Queue#65e4",
      "select": "Select#15c2",
      "solver_node": "SolverNode#26b1",
      "rank": "Rank#7a76"
    }
  }
}
```

---

## Bubble#189d

```json
{
  "handle": "Bubble",
  "mechanism": "Isolated sandbox where coordination is tried before committing to reality. Creator sends BUBBLE_CREATE: {participants, ttl (time-to-live), isolation_level, parent_bubble (for nesting)}. Participants JOIN to enter isolated context. Inside bubble: state changes are copy-on-write (snapshot isolation), resource acquisitions are soft-reservations (intent, not actual), messages to non-participants are queued (not sent). {{work}} proceeds normally but nothing affects real world. When ready, creator calls PREPARE (2-phase commit). Each participant responds READY (can commit) or ABORT (cannot). If ALL READY: COMMIT\u2014queued messages sent, state changes applied atomically, reservations converted to hard acquisitions. If ANY ABORT or TTL expires: ROLLBACK\u2014all tentative work discarded silently, no compensation needed. Nested bubbles commit to parent context, not real world; parent commit makes all nested work real. It enforces a {{constraint_first}} approach around the simulation context to ensure no side effects leak into the production environment.",
  "gloss": "Sandboxed coordination trial with rollback on commit refusal",
  "failure_modes": [
    "Participant crashes after READY but before COMMIT (blocking\u2014use timeout and recovery).",
    "Long-running bubbles hold soft-reservations too long (resource starvation).",
    "{{state}} snapshot becomes stale (external world changed during bubble).",
    "Nested bubble complexity (multiple isolation levels, commit ordering).",
    "Commit overhead (2PC protocol is expensive).",
    "Bubble escape (agent accidentally affects real world from inside bubble\u2014discipline required)."
  ],
  "invariants": [
    "Information within bubble is isolated from outside",
    "Internal consistency maintained"
  ],
  "preconditions": [
    "Group of agents",
    "Shared context"
  ],
  "postconditions": [
    "Bubble dissolved or merged",
    "Local consensus reached"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_id": "sema:Bubble#mh:SHA-256:189dd3deb9833b76aa24662131557e799499d0cfbab0aae8070e3496f6c0e582",
  "sema_ref": "Bubble#189d",
  "sema_stub": "189d",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "constraint_first": "ConstraintFirst#c7cb",
      "state": "State#4d58",
      "work": "Work#d2c6"
    }
  }
}
```

---

## Build#9330

```json
{
  "handle": "Build",
  "mechanism": "Performs the {{act}} of constructing a low-cost {{artifact}} (prototype) to verify critical assumptions in the {{spec}} before full commitment. Governed by the Marginal {{value}} Rule.",
  "gloss": "Low-cost prototype generation",
  "failure_modes": [
    "Over-engineering: Building the full product instead of a prototype.",
    "False Negative: {{prototype}} fails due to low fidelity, killing a good plan.",
    "Scope Creep: {{prototype}} expands beyond verification needs."
  ],
  "invariants": [
    "Cost(Build) << Cost(rollout)",
    "{{prototype}} must address specific risks identified in {{plan}}"
  ],
  "preconditions": [
    "PlanBundle with high uncertainty/risk"
  ],
  "postconditions": [
    "ProtoPack artifact (Evidence of feasibility)"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "Simulation#aa24",
      "DogfoodFirst#2538",
      "SacrificialProbe#0d39"
    ],
    "ring": 1
  },
  "sema_id": "sema:Build#mh:SHA-256:9330f2406f087360a8a5d84bcf2426512acdcee446c3eef6264d485956c180f0",
  "sema_ref": "Build#9330",
  "sema_stub": "9330",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Act#5d55(Artifact#6254)"
  ],
  "dependencies": {
    "references": {
      "prototype": "Prototype#ff18",
      "plan": "Plan#fd6d",
      "value": "Value#3c5d",
      "act": "Act#5d55"
    },
    "yields": {
      "artifact": "Artifact#6254"
    },
    "accepts": {
      "spec": "Spec#a036"
    }
  }
}
```

---

## CapacityPressure#c861

```json
{
  "handle": "CapacityPressure",
  "mechanism": "A regularization pattern that forces abstraction by artificially constraining resources (bandwidth, memory, parameter count, or time). By creating a bottleneck where Capacity < Information, the agent is compelled to compress the signal, discarding noise and memorized details in favor of high-level concepts and generalizations. It artificially tightens the {{budget}}, forcing the agent to employ {{generalize}}, {{concept_blend}}, and {{context_compress}} to fit the signal within the bottleneck.",
  "gloss": "Forcing abstraction via resource starvation",
  "failure_modes": [
    "Collapse: {{constraint}} is too tight; signal is lost entirely (underfitting) Adversarial Encoding: {{agent}} finds a way to 'zip' noise rather than abstracting (violating the spirit of the constraint) False Abstraction: {{agent}} hallucinates simple rules that don't actually exist to satisfy the budget"
  ],
  "invariants": [
    "Bottleneck Existence: Available Capacity must be strictly less than Input Information Content",
    "Lossy Requirement: Output must be a simplified representation, effectively barring exact replication/memorization",
    "Utility Preservation: The compressed form must retain predictive power for the target task"
  ],
  "preconditions": [
    "A mechanism to enforce hard limits (e.g., context window, dimensions, token count)",
    "A stream of information or a learning task"
  ],
  "postconditions": [
    "A highly compressed, abstract representation of the input",
    "Loss of fine-grained detail/noise"
  ],
  "parameters": [
    {
      "name": "compression_ratio",
      "type": "Ratio",
      "range": "[0.0, 1.0]",
      "description": "Target resource utilization ratio that triggers forced abstraction"
    },
    {
      "name": "resource_type",
      "type": "Enum",
      "range": "{Compute, Memory, Attention, Budget#7270}",
      "description": "Type of resource being constrained (compute, memory, bandwidth)"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:CapacityPressure#mh:SHA-256:c8612db41bba14b91f1c4fbc85042134151a7a2a1738a54615c0db6b3bfa5884",
  "sema_ref": "CapacityPressure#c861",
  "sema_stub": "c861",
  "dependencies": {
    "references": {
      "context_compress": "ContextCompress#4845",
      "budget": "Budget#7270",
      "concept_blend": "ConceptBlend#126e",
      "generalize": "Generalize#6dea",
      "agent": "Agent#35b9",
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## CommitmentDevice#6c21

```json
{
  "handle": "CommitmentDevice",
  "mechanism": "Future Self Binding: Anticipate that future self will face temptation or weakness. Remove future options by present action. Examples: delete the app, announce publicly, create penalty for deviation. Cost of breaking commitment must exceed temptation value. It constructs an {{oath_bind}} contract that penalizes future deviation from the chosen path.",
  "gloss": "Pre-commitment against hyperbolic discounting",
  "failure_modes": [
    "Over-commitment: Binding too early locks out legitimate pivots when new information arrives."
  ],
  "invariants": [
    "Binding: Cost(Breaking) > Benefit(Breaking)",
    "Irrevocability: {{agent}} cannot unilaterally remove the constraint"
  ],
  "preconditions": [
    "{{agent}} expects future preference reversal (hyperbolic discounting)"
  ],
  "postconditions": [
    "Future action set constrained"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0,
    "caution": "Removes future options by design \u2014 can trap agent in suboptimal commitment."
  },
  "sema_id": "sema:CommitmentDevice#mh:SHA-256:6c210108ca98eee9093d7ac7176ec08cd2b6198df985d0df957756e4fb33e993",
  "sema_ref": "CommitmentDevice#6c21",
  "sema_stub": "6c21",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "data_schema": {
    "type": "object",
    "required": [
      "commitment",
      "penalty"
    ],
    "properties": {
      "commitment": {
        "type": "string",
        "description": "The action being committed to"
      },
      "penalty": {
        "type": "object",
        "description": "Cost incurred if commitment broken"
      },
      "irrevocable": {
        "type": "boolean",
        "description": "Whether commitment can be undone"
      }
    }
  },
  "dependencies": {
    "references": {
      "oath_bind": "OathBind#a708",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Compose#76c1

```json
{
  "handle": "Compose",
  "mechanism": "Recursive Assembly: Given solved subproblems, {{combine}} solutions respecting interfaces. {{check}}: does combined solution satisfy original problem constraints? If interaction effects emerge, add coordination layer or revise decomposition. It often employs {{prompt_chain}} to sequentially feed sub-solutions into the integration step.",
  "gloss": "Building complex behavior from simple primitives",
  "failure_modes": [
    "Interface Mismatch: Component outputs do not match expected inputs of downstream components."
  ],
  "invariants": [
    "Type Safety: Component outputs must match downstream inputs.",
    "Acyclicity: Composition graph must be a DAG."
  ],
  "preconditions": [
    "Subproblem solutions available. Interface contracts defined. Composition order known if order-dependent."
  ],
  "postconditions": [
    "Combined solution satisfies original problem. No interface violations. Emergent interactions handled."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Compose#mh:SHA-256:76c1e7fb397feba35540c6efc14b56e60df485e39e0efdc3e9d60b273e1778ad",
  "sema_ref": "Compose#76c1",
  "sema_stub": "76c1",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Combine#5a44(PromptChain#8c63)"
  ],
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "prompt_chain": "PromptChain#8c63",
      "combine": "Combine#5a44"
    }
  }
}
```

---

## ComputeBudget#67c0

```json
{
  "handle": "ComputeBudget",
  "mechanism": "The cognitive governor that prevents analysis paralysis. It acts as a dual-ledger {{gate}}, weighing the {{value}} of a {{task}} against the {{budget}} to ensure return on investment (ROI). It enforces stopping rules when the cost of thinking exceeds the value of the solution.",
  "gloss": "Economic governor for cognitive spend",
  "failure_modes": [
    "Analysis Paralysis: Spending more on estimation than the task is worth.",
    "Penny Wise: Rejecting necessary deep thinking for high-stakes/high-complexity problems.",
    "Cost estimation is itself costly (meta-cost problem).",
    "Uncertainty about uncertainty makes expected_gain hard to calculate.",
    "Risk of penny-wise pound-foolish: refusing decomposition on hard problems because estimate was wrong."
  ],
  "invariants": [
    "Hard Ceiling: Total execution cost cannot exceed max_budget.",
    "Meta-Cap: Estimation phase must consume < 1% of total budget."
  ],
  "preconditions": [
    "Current resource balance available",
    "{{task}} value estimated"
  ],
  "postconditions": [
    "Budget constraints injected into {{task}} context",
    "Execution strategy Selected (Direct vs Recursive)"
  ],
  "parameters": [
    {
      "name": "max_budget",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Hard limit"
    },
    {
      "name": "risk_tolerance",
      "type": "Float",
      "range": "[0.1, 2.0]",
      "description": "Willingness to overspend budget (1.0 = neutral, >1 = risk-seeking)"
    },
    {
      "name": "unit",
      "type": "Enum",
      "range": "{Tokens, USD, Ms}",
      "description": "Default: Tokens"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0,
    "related": [
      "OptimalStop#c244",
      "Satisfice#9859",
      "TimeboxThink#043d"
    ]
  },
  "sema_ref": "ComputeBudget#67c0",
  "sema_id": "sema:ComputeBudget#mh:SHA-256:67c0cb96827aabadd1ed6ef4caedd4adcce628f1c1a2b4fc50c01dc2e94c4989",
  "sema_stub": "67c0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "gate": "Gate#89fd",
      "budget": "Budget#7270",
      "task": "Task#b328",
      "value": "Value#3c5d"
    }
  }
}
```

---

## ConceptBlend#126e

```json
{
  "handle": "ConceptBlend",
  "mechanism": "Forcing the merger of two unrelated graph nodes to find a valid semantic path. Unlike analogy (A is like B), blending creates C (A + B). It extends {{analogy_bridge}} by not just mapping A to B, but fusing them to create C.",
  "gloss": "Atomic fusion of two unrelated concepts into a novel third",
  "invariants": [
    "Orthogonality: Inputs must be semantically distant (> threshold distance)",
    "Validity: Output must pass a {{tri_gate}}({{realizable}}) check"
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "sema:AnalogicalMask#mh:SHA-256:4c693894def97c224cf9f9fec71dc4def00c0b8cc6523ccfe5ee5ccddb275c8a"
    ],
    "ring": 2
  },
  "sema_id": "sema:ConceptBlend#mh:SHA-256:126e802579f0301b1c71df4731146236a15095e1404d3e7358b87d2bd1f47e1a",
  "sema_ref": "ConceptBlend#126e",
  "sema_stub": "126e",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "tri_gate": "TriGate#67b8",
      "realizable": "Realizable#8d81",
      "analogy_bridge": "AnalogyBridge#ddb2"
    }
  }
}
```

---

## ConstraintFirst#c7cb

```json
{
  "handle": "ConstraintFirst",
  "mechanism": "The agent first generates the 'negative space' (the {{constraint}}s, safety rules, and format requirements), defining a rigid container. Only THEN does it generate the content to fill that container. It separates 'form' from 'function'. This prevents the generation of content that is creative but invalid.",
  "gloss": "Defining boundaries before content",
  "failure_modes": [
    "Over-constraining the solution space."
  ],
  "invariants": [
    "Constraints immutable during operation."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:ConstraintFirst#mh:SHA-256:c7cb09081701787022c33fa3b1399bd847b0062cf223851c4d98024b640feb99",
  "sema_ref": "ConstraintFirst#c7cb",
  "sema_stub": "c7cb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## ContingencyPlan#770d

```json
{
  "handle": "ContingencyPlan",
  "mechanism": "If-Then Preparation: For each critical assumption in a {{plan}}, define trigger condition for failure. Pre-compute response: \"If X happens, I will do Y.\" Store contingencies before they are needed. When trigger fires, execute pre-made backup {{plan}} without deliberation under stress. It pre-defines the logic that {{retry}} or recovery mechanisms should execute upon specific trigger conditions.",
  "gloss": "Pre-computed responses to critical failure",
  "failure_modes": [
    "Maginot Line: Planning for the wrong disaster while ignoring the actual threat model."
  ],
  "invariants": [
    "Resources reserved for contingency",
    "Trigger condition is disjoint from main plan success"
  ],
  "preconditions": [
    "Identified failure modes",
    "Primary plan"
  ],
  "postconditions": [
    "Backup path defined and viable"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:ContingencyPlan#mh:SHA-256:770d74a39fdfb7074a774be3307f50052ad719aaef524031a8e1663888d5b831",
  "sema_ref": "ContingencyPlan#770d",
  "sema_stub": "770d",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d",
      "retry": "Retry#4cc6"
    }
  }
}
```

---

## Creative#5574

```json
{
  "handle": "Creative",
  "mechanism": "The cognitive mode focused on generating novel and valuable ideas, artifacts, or solutions. It involves divergent thinking, making remote associations, and breaking established patterns.",
  "gloss": "Generating novelty and value",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_id": "sema:Creative#mh:SHA-256:557440d0f12d6169d83249769ab27aee03e1d662d53c58ae91589c1a6ad4c151",
  "sema_ref": "Creative#5574",
  "sema_stub": "5574",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba"
}
```

---

## CreativeBlend#82d7

```json
{
  "handle": "CreativeBlend",
  "derived_from": "Creative#5574",
  "gloss": "Full creative pipeline: ConceptBlend + NoiseInjection with novelty/value gates",
  "signature": [
    "Strategy#c4ba(Artifact#6254)"
  ],
  "mechanism": "A generative {{strategy}} that produces an {{artifact}} by identifying orthogonal concepts in the {{context}} and fusing them via {{concept_blend}}. It applies {{noise_injection}} to the seed inputs to escape local optima. The output is filtered through a rigorous dual-{{check}} against {{novelty}} and {{value}}. Only artifacts passing both gates are yielded.",
  "invariants": [
    "Divergence: Output similarity to input < Threshold.",
    "Utility: Must maintain structural coherence (not pure noise)."
  ],
  "parameters": [
    {
      "name": "temperature",
      "type": "Float",
      "range": "[0.7, 1.5]",
      "description": "Randomness injection level"
    }
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 2
  },
  "sema_ref": "CreativeBlend#82d7",
  "sema_id": "sema:CreativeBlend#mh:SHA-256:82d7642bee7ab08f0f93028151462a47e35e1ceb52e047fb3b3733386cfc647a",
  "sema_stub": "82d7",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "yields": {
      "artifact": "Artifact#6254"
    },
    "accepts": {
      "context": "Context#510a"
    },
    "composes_with": {
      "check": "Check#d3e8",
      "concept_blend": "ConceptBlend#126e"
    },
    "references": {
      "value": "Value#3c5d",
      "strategy": "Strategy#c4ba",
      "noise_injection": "NoiseInjection#4133",
      "novelty": "Novelty#8568"
    }
  }
}
```

---

## Crystallize#b64b

```json
{
  "handle": "Crystallize",
  "mechanism": "Formalize implicit resonance. {{agent}} A proposes crystallization based on history history_t. {{agent}} B validates perception. On consensus, implicit behaviors are codified into explicit obligations. It transforms soft {{resonate}} signals into hard {{constitution}} rules, contingent on low entropy conditions maintained by {{dampen}} and {{entropy_pump}}, preventing premature {{decay}}.",
  "gloss": "Phase transition from implicit resonance to explicit contract",
  "failure_modes": [
    "Illusory Resonance: Agents misinterpreted random noise as synchronization.",
    "Premature Crystallization: Attempting to lock state while Entropy > Threshold.",
    "Illusory resonance (parties perceived differently, crystallization exposes this).",
    "Perception mismatch on alignment dimensions.",
    "Gaming (agent fakes resonance metrics).",
    "Premature crystallization (not enough resonance history).",
    "Trust inflation (claiming more trust than resonance justifies)."
  ],
  "invariants": [
    "Atomic {{transition}}: {{state}} moves from Fluid -> Solid in one transaction.",
    "Entropy Limit: Crystallization forbidden if System_Entropy > entropy_threshold."
  ],
  "preconditions": [
    "Active implicit resonance channel exists",
    "{{state}} is fluid/negotiable"
  ],
  "postconditions": [
    "Explicit coordination channel established",
    "{{state}} marked immutable/contractual"
  ],
  "parameters": [
    {
      "name": "entropy_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Maximum disorder level before implicit alignment is formalized into a contract"
    },
    {
      "name": "resonance_period",
      "type": "Duration",
      "range": "unspecified",
      "description": "Minimum history required"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_id": "sema:Crystallize#mh:SHA-256:b64bd975c1195d73e24369a3fe452a6ed0aecba1398437832b683f801da95e78",
  "sema_ref": "Crystallize#b64b",
  "sema_stub": "b64b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "decay": "Decay#a1d4",
      "state": "State#4d58",
      "resonate": "Resonate#9fa4",
      "entropy_pump": "EntropyPump#c313",
      "dampen": "Dampen#e55e",
      "agent": "Agent#35b9",
      "constitution": "Constitution#8cb8"
    }
  }
}
```

---

## Deep#89f0

```json
{
  "handle": "Deep",
  "mechanism": "The vertical dimension of search (Recursion/Detail). Recursively expanding a node to increase resolution, as opposed to Broad exploration.",
  "gloss": "Vertical search dimension",
  "invariants": [
    "Functional Equivalence: Target must answer the same question as Source.",
    "Rigor Increase: Target must have higher compute/context cost than Source.",
    "Resolution Increase: Child nodes must be more specific than parent."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Deep#mh:SHA-256:89f02aa7bc72cf8798b5619ae123bf4da38cff92f5147a436729ce2af17f897b",
  "sema_ref": "Deep#89f0",
  "sema_stub": "89f0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba"
}
```

---

## Defer#1796

```json
{
  "handle": "Defer",
  "mechanism": "Strategic Postponement: When facing decision with high uncertainty, ask: \"What would I learn by waiting?\" If waiting reveals information that changes the decision, defer. If not, decide now. Avoid analysis paralysis by setting a deadline. It relies on {{prioritize}} to re-insert the task into the queue once the waiting condition is met.",
  "gloss": "Postponing decisions until more information available",
  "failure_modes": [
    "{{decision}} Debt: Deferred choices accumulate until deadline forces rushed, poor decisions."
  ],
  "invariants": [
    "Deferral must have information value.",
    "{{state}} Preservation: {{context}} must be saved for resumption",
    "Trigger Definition: WakeUpCondition must be explicit"
  ],
  "preconditions": [
    "{{task}} is not urgent"
  ],
  "postconditions": [
    "{{task}} queued"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Defer#mh:SHA-256:1796866c804d326b413ff658ab87cd57f6047969792bd087d5cf6ef0a37dbe08",
  "sema_ref": "Defer#1796",
  "sema_stub": "1796",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "state": "State#4d58",
      "context": "Context#510a",
      "prioritize": "Prioritize#68f8",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## DepthGovernor#73d5

```json
{
  "handle": "DepthGovernor",
  "mechanism": "Entropy-Bounded Recursion: Decomposition depth is not fixed but governed by informational entropy. {{agent}} measures uncertainty of current {{plan}}. If entropy > action_cost_threshold, {{decompose}} further. If entropy < threshold, execute. Stop thinking when uncertainty drops below action cost. Depth is a function of ambiguity, not arbitrary limits. It acts as the termination {{condition}} for {{recursion_dive}}, halting descent when informational entropy drops below the threshold.",
  "gloss": "Entropy-based stopping condition for recursion",
  "failure_modes": [
    "Ambiguity {{loop}}: Entropy never drops because the {{problem}} is inherently subjective (e.g., Write a good poem).",
    "Miscalculating entropy leads to premature action.",
    "Infinite regression on high-ambiguity paradoxes.",
    "Entropy estimation itself has computational cost."
  ],
  "invariants": [
    "Governor cannot be bypassed."
  ],
  "parameters": [
    {
      "name": "entropy_threshold",
      "type": "Float",
      "range": "[0.1, 0.5]",
      "description": "Stop when uncertainty below this"
    },
    {
      "name": "max_depth",
      "type": "Integer",
      "range": "[3, 20]",
      "description": "Hard limit on recursion"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:DepthGovernor#mh:SHA-256:73d51673295eced222f7a9c1de51fc4970682ce418559374ff1bc3764faf2cc8",
  "sema_ref": "DepthGovernor#73d5",
  "sema_stub": "73d5",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "condition": "Condition#cbd5",
      "plan": "Plan#fd6d",
      "agent": "Agent#35b9",
      "recursion_dive": "RecursionDive#9c9f",
      "problem": "Problem#4576",
      "decompose": "Decompose#f900"
    }
  }
}
```

---

## DesignArchitect#2bca

```json
{
  "handle": "DesignArchitect",
  "mechanism": "The strategic agent responsible for formulating a {{mechanistic_design_proposal}}. It uses the adversarial method to robustify the design: defending it via {{steelman_check}} and attacking it via {{pre_mortem}}. It integrates with {{strategy}} to project future impact and uses {{translate}} and {{summarize}} to refine the final output for clarity.",
  "gloss": "Agent that architects mechanistic design proposals",
  "invariants": [
    "Dialectic Rigor: Must apply both Steelman and PreMortem to the design.",
    "Output Quality: Must produce a valid MechanisticDesignProposal."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_ref": "DesignArchitect#2bca",
  "sema_id": "sema:DesignArchitect#mh:SHA-256:2bca4f59f554d98d14f125913c5f8e74ad98bf4b0c44afc176178217e9b10aec",
  "sema_stub": "2bca",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "composes_with": {
      "translate": "Translate#a8ed",
      "summarize": "Summarize#db2a",
      "steelman_check": "SteelmanCheck#7914",
      "pre_mortem": "PreMortem#142a",
      "strategy": "Strategy#c4ba"
    },
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#497e"
    }
  }
}
```

---

## DiscoveryProtocol#bf29

```json
{
  "handle": "DiscoveryProtocol",
  "mechanism": "The paper's \u00a76.4 protocol for population-based discovery. Distinct from the {{discover}} primitive (query-and-return): Discovery Protocol is the Generate + Reduce architecture for searching a solution space. Decomposes discovery via {{conceptual_decomposition}} into five orthogonal dimensions: variance (generate candidates that are precise in different directions, each bound to a maximally distinct cognitive mode via GeneratorSolvers), selection (judge which candidates are good), novelty (distinguish structural originality from surface variation), composition (merge compatible fragments into solutions no single candidate contains), and saturation (detect when further generation yields diminishing novelty). Two phases behind hard boundaries: generate-asked-by-many-parallel-Solvers, then reduce-asked-by-a-Solver-whose-faculty-is-evaluation-and-composition-rather-than-generation. The ReduceSolver routes among modes (AggregateSolver for ensembles, TournamentSolver for adversarial selection, PortfolioSolver for quality-diversity preservation, {{synthesis}}-based merging of compatible mechanisms). TaxonomistSolver classifies outputs into a growing ontological graph for saturation detection. Applies to drug discovery, hypothesis generation, strategic planning, creative production.",
  "gloss": "Population-based discovery: Generate (parallel diverse solvers) + Reduce (composition-aware selection) behind hard boundaries",
  "invariants": [
    "Hard-boundary isolation: generators cannot see each other's outputs during generation; the reduction boundary is the first synthesis point.",
    "Cognitive-mode diversity: each GeneratorSolver is bound to a maximally distinct mode, not just sampled from one model at different temperatures.",
    "Non-compensatory reduction gate: novelty is a gate condition, not a tiebreaker \u2014 a structurally novel mechanism survives even if it scores lower on surface plausibility."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:DiscoveryProtocol#mh:SHA-256:bf29178f844591e77241b547f47963e06fc3119243dc2d7d4c2c45f24b843d43",
  "sema_ref": "DiscoveryProtocol#bf29",
  "sema_stub": "bf29",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#f81f",
      "synthesis": "Synthesis#26b9"
    },
    "references": {
      "discover": "Discover#7dbc"
    }
  }
}
```

---

## DogfoodFirst#2538

```json
{
  "handle": "DogfoodFirst",
  "mechanism": "Validation {{protocol}}. Before releasing a tool or pattern, the creator must use it to solve a non-trivial problem in their own workflow. This generates 'Friction Logs' that identify usability gaps missed by theoretical design. It requires the creator to act as a {{canary}}, using the tool in production and generating a {{reflexion}} log of friction points.",
  "gloss": "Use your own tool before shipping",
  "failure_modes": [
    "Hello World Fallacy: Validating only on trivial 'demo' cases instead of production loads.",
    "Creator {{cognitive_bias}}: Creator unconsciously avoids edge cases they know will fail."
  ],
  "invariants": [
    "Friction Documentation: All UX hurdles encountered must be logged.",
    "Skin in the Game: Validation must involve real risk or real work (not a simulation)."
  ],
  "preconditions": [
    "Real-world use case identified",
    "Tool/Pattern is functionally complete"
  ],
  "postconditions": [
    "Friction Log generated",
    "Release {{gate}} passed OR Refactor triggered"
  ],
  "parameters": [
    {
      "name": "duration",
      "type": "Duration",
      "range": "unspecified",
      "description": "Default: 1h"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:DogfoodFirst#mh:SHA-256:25387b1cb9c36907f32775517ffb22e2370c126d85c8db8a82b611ebaed142b8",
  "sema_ref": "DogfoodFirst#2538",
  "sema_stub": "2538",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "gate": "Gate#89fd",
      "protocol": "Protocol#7e1c",
      "reflexion": "Reflexion#eed9",
      "canary": "Canary#adb0"
    }
  }
}
```

---

## EmpathySim#7008

```json
{
  "handle": "EmpathySim",
  "mechanism": "Theory of Mind simulation. {{agent}} instantiates a temporary 'Virtual {{context}}' initialized from a {{target_profile}} (known priors, goals, and constraints). It then runs inference on this context to predict Target's next move. It spins up an isolated {{agent_sandbox}} to model the target's perspective.",
  "gloss": "Predictive modeling of external agent states",
  "failure_modes": [
    "Projection {{cognitive_bias}}: Leaking Self-Knowledge into the simulation (Mirroring Error).",
    "Infinite Regress: {{simulation}} of Target simulating Self simulating Target..",
    "{{simulation}} Capture: Hostile memetics in simulated {{context}} corrupting host {{state}}."
  ],
  "invariants": [
    "Isolation: Simulated context must have NO write access to Host memory.",
    "Priors Shift: Utility function used must be Target's, not Host's."
  ],
  "preconditions": [
    "{{budget}} available for sub-simulation",
    "Target profile (goals/constraints) known"
  ],
  "postconditions": [
    "Confidence_Score generated",
    "Predicted_Action vector generated"
  ],
  "parameters": [
    {
      "name": "simulation_depth",
      "type": "Integer",
      "range": "[1, 3]",
      "description": "Default: 1"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "MentalSim#10ff"
    ],
    "ring": 2
  },
  "sema_id": "sema:EmpathySim#mh:SHA-256:7008dcff05dc6219c7d49dd02e8b09e6d6d4bf699ac502fc039118b33d140e3b",
  "sema_ref": "EmpathySim#7008",
  "sema_stub": "7008",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "state": "State#4d58",
      "context": "Context#510a",
      "cognitive_bias": "CognitiveBias#4b32",
      "agent_sandbox": "AgentSandbox#fc41",
      "agent": "Agent#35b9",
      "simulation": "Simulation#aa24"
    },
    "accepts": {
      "agent": "Agent#35b9"
    }
  }
}
```

---

## EmpiricalTest#65ed

```json
{
  "handle": "EmpiricalTest",
  "mechanism": "Identifies testable predictions from a conclusion and executes experiments (or lookups) to verify them. Increases epistemic confidence via {{falsification}} attempts. (Formerly confused with {{validate}}).",
  "gloss": "Verifying conclusions via testable predictions",
  "preconditions": [
    "Conclusion to test",
    "Test mechanism available"
  ],
  "postconditions": [
    "Confidence updated based on test results"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_id": "sema:EmpiricalTest#mh:SHA-256:65ed9f3e69d80b15abc13e42e64da3a80d0cad34f4d132e95f4ff986621c6538",
  "sema_ref": "EmpiricalTest#65ed",
  "sema_stub": "65ed",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "validate": "Validate#ebe1",
      "falsification": "Falsification#4e23"
    }
  }
}
```

---

## EpistemicROI#0d53

```json
{
  "handle": "EpistemicROI",
  "mechanism": "{{value}} of Information (VOI) analysis. Before executing an information-gathering {{task}} ({{experiment}}, Probe, Research), calculate: (1) The range of possible {{outcome}}s, (2) The {{decision}} you would make for each {{outcome}}. (3) If the {{decision}} is the same regardless of {{outcome}}, VOI = 0. (4) If different, VOI = {{value}}(Better {{decision}}) - Cost({{experiment}}). Only proceed if VOI > 0. It evaluates whether to {{act}} on expensive patterns by checking if the information gain justifies the {{compute_budget}}.",
  "gloss": "Calculating the economic value of reducing uncertainty",
  "failure_modes": [
    "Overestimation of Pivot: Assuming you will change your mind when you actually won't (Confirmation {{cognitive_bias}}).",
    "Underestimation of Cost: Ignoring the time/compute cost of the experiment itself."
  ],
  "invariants": [
    "{{decision}} Delta: {{experiment}} must have at least two {{outcome}}s leading to different Actions",
    "Positive {{result}}: ExpectedValue(Info) > Cost(Acquisition)"
  ],
  "preconditions": [
    "Cost of experiment is estimable",
    "{{decision}} context is defined"
  ],
  "postconditions": [
    "Go/No-Go decision based on ROI"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:EpistemicROI#mh:SHA-256:0d537b6d7eaa65f91830a59ea43290a17fc175a8a352d691224ce11fe9af67b1",
  "sema_ref": "EpistemicROI#0d53",
  "sema_stub": "0d53",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "cognitive_bias": "CognitiveBias#4b32",
      "experiment": "Experiment#a93e",
      "compute_budget": "ComputeBudget#67c0",
      "outcome": "Outcome#144c",
      "result": "Result#195b",
      "value": "Value#3c5d",
      "decision": "Decision#acfb",
      "act": "Act#5d55"
    }
  }
}
```

---

## EventReact#da85

```json
{
  "handle": "EventReact",
  "mechanism": "Event-Driven Response: {{agent}} subscribes to event types. Events queued by priority. Handler invoked per event. Handler execution atomic. Unhandled events logged or escalated. It implements the reactive loop, often triggering a {{re_act}} cycle upon signal reception.",
  "gloss": "Responding to external triggers rather than polling",
  "failure_modes": [
    "Event Storm: Cascade of events overwhelms handler capacity, causing dropped or delayed responses."
  ],
  "invariants": [
    "Handler matches event type",
    "Response latency < Max_Latency"
  ],
  "preconditions": [
    "Event listener active",
    "Trigger event occurs"
  ],
  "postconditions": [
    "Handler executed"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:EventReact#mh:SHA-256:da85e84f43dca3c870edf9dd518e4602a63cf1be9efada545781de12db839103",
  "sema_ref": "EventReact#da85",
  "sema_stub": "da85",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "agent": "Agent#35b9",
      "re_act": "ReAct#e018"
    }
  }
}
```

---

## Experiment#a93e

```json
{
  "handle": "Experiment",
  "mechanism": "A structured {{protocol}} for causal discovery. Unlike {{verification}} (which confirms a claim), Experiment generates a {{solution}} (new knowledge) by isolating variables using a Control and Treatment group.",
  "gloss": "Structured causal discovery via variable isolation",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "related": [
      "HypothesisLadder#f88b"
    ]
  },
  "sema_ref": "Experiment#a93e",
  "sema_id": "sema:Experiment#mh:SHA-256:a93e3cf28a0eec41473eb3e00beabac3d5d903bd53ac3184001df8bba2bb4cc3",
  "sema_stub": "a93e",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "yields": {
      "solution": "Solution#fcea"
    },
    "references": {
      "verification": "Verification#19d6",
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## ExploreExploit#1de3

```json
{
  "handle": "ExploreExploit",
  "mechanism": "Adaptive Allocation: Early in process, favor exploration (try new options, gather info). As deadline approaches, shift to exploitation (use best known option). Uncertainty reduction value decreases over time. Upper Confidence Bound: pick option with highest (estimate + uncertainty bonus). It monitors the remaining {{budget}} to dynamically adjust the epsilon parameter from exploration to exploitation.",
  "gloss": "Balancing information gathering vs value extraction",
  "failure_modes": [
    "{{context}} Drift: The environment changes during the Exploit phase, making the best option obsolete."
  ],
  "invariants": [
    "Threshold immutable during execution."
  ],
  "parameters": [
    {
      "name": "decay_rate",
      "type": "Float",
      "range": "[0.9, 0.999]",
      "description": "Epsilon decay per iteration"
    },
    {
      "name": "epsilon",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Exploration probability"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:ExploreExploit#mh:SHA-256:1de37294175428733bae4d9e3d00b2281b1abfe2e1defd6cf76fc833df5d93f4",
  "sema_ref": "ExploreExploit#1de3",
  "sema_stub": "1de3",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "context": "Context#510a"
    }
  }
}
```

---

## Falsification#4e23

```json
{
  "handle": "Falsification",
  "mechanism": "The logical act of proving a {{hypothesis}} false by {{observe}}ing an {{incongruity}} between prediction and observation. It creates specific knowledge by eliminating possibilities.",
  "gloss": "Proof of falsehood",
  "invariants": [
    "Logical Negation: If Prediction implies Observation, and not-Observation, then not-Hypothesis.",
    "Empirical Grounding: Requires observational evidence."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1,
    "related": [
      "HypothesisLadder#f88b"
    ]
  },
  "sema_id": "sema:Falsification#mh:SHA-256:4e239c5718eb2279b61935176478b206785942cf78c748380484d7106b533de9",
  "sema_ref": "Falsification#4e23",
  "sema_stub": "4e23",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "incongruity": "Incongruity#e98f",
      "hypothesis": "Hypothesis#ffa7",
      "observe": "Observe#39f0"
    }
  }
}
```

---

## FractalIntelligence#ab50

```json
{
  "handle": "FractalIntelligence",
  "mechanism": "Expansion of cognitive capability through {{conceptual_decomposition}}: a concept (problem or task) is broken into contract-bound sub-concepts, each governed by the same five-surface Solver Contract (Manifest, Execute, Consult, Verify, Feedback) that governs the parent. A few {{agent}}s can assign solver roles to themselves and perform lightweight fractal intelligence for a specific problem \u2014 the resulting structure may persist as a reusable pattern that improves through use, or may be torn down at completion; both are legitimate modes. The unified {{system}} of scalable cognition uses {{reason}} to orchestrate fractal expansion within the {{universal_solver_tree}}. A {{problem_framer}} initiates by formulating a high-level {{strategy}} before assigning a {{polymorphic_solver}} to a {{task}}; the solver executes a {{recursion_dive}} to spawn child nodes, each applying {{specialize}} with {{localized_learning}}, while {{experience_sharding}} and {{synthesis}} preserve global coherence. {{state_snapshot}} provides crash recovery for persistent instances. {{marginal_value_rule}} governs recursion depth. On failure, {{reframe}} restructures the tree.",
  "gloss": "Expansion of cognitive capability through recursive decomposition of concepts into contract-bounded sub-concepts",
  "invariants": [
    "Fractal Self-Similarity: The process at the Root is identical to the process at the Leaf.",
    "Bounded Expansion: Recursion is limited by Economic constraints (Marginal Value).",
    "Memory Conservation: Specialization must not result in the loss of global context."
  ],
  "signature": [
    "System#e314(Reason#5f30)"
  ],
  "derived_from": "sema:RecursiveIntelligence#mh:SHA-256:216c297a34a0847957d1a6a8701987248bc8d63294953a78346b5b68dbb9aef6",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_ref": "FractalIntelligence#ab50",
  "sema_id": "sema:FractalIntelligence#mh:SHA-256:ab502d23e39cad39392548bc97e251df2e2ecd494244f4fd069c0cd8732fb063",
  "sema_stub": "ab50",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "composes_with": {
      "localized_learning": "LocalizedLearning#fcc7",
      "state_snapshot": "StateSnapshot#b9b8",
      "problem_framer": "ProblemFramer#f504",
      "recursion_dive": "RecursionDive#9c9f",
      "polymorphic_solver": "PolymorphicSolver#9188",
      "reason": "Reason#5f30",
      "marginal_value_rule": "MarginalValueRule#32ce",
      "conceptual_decomposition": "ConceptualDecomposition#f81f",
      "synthesis": "Synthesis#26b9",
      "reframe": "Reframe#0b02"
    },
    "references": {
      "task": "Task#b328",
      "universal_solver_tree": "UniversalSolverTree#b805",
      "specialize": "Specialize#0ac5",
      "system": "System#e314",
      "experience_sharding": "ExperienceSharding#43c3",
      "agent": "Agent#35b9",
      "strategy": "Strategy#c4ba"
    }
  }
}
```

---

## HypothesisEngine#bffd

```json
{
  "handle": "HypothesisEngine",
  "mechanism": "The Scientific Method as a cognitive cycle. 1. {{discover}}({{hypothesis}}): Generate a candidate {{hypothesis}} (Explanation). 2. {{trace}}({{simulation}}): Simulate implications and log the lineage. 3. {{check}}(Consistency): {{validate}} against invariants. 4. {{stigmergy}}(Result): Publish the findings to the shared context. It cycles through {{discover}}, {{trace}}, and {{check}} to formalize the scientific loop, publishing validated models via {{stigmergy}}.",
  "gloss": "Automated scientific method",
  "failure_modes": [
    "Confirmation bias: evidence selectively gathered to support preferred hypothesis.",
    "Untestable hypothesis accepted into cycle without falsification criteria."
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:HypothesisEngine#mh:SHA-256:bffd8181760462e7d213287b482f25081597d30db0a745627573e3c6555614a4",
  "sema_ref": "HypothesisEngine#bffd",
  "sema_stub": "bffd",
  "dependencies": {
    "references": {
      "stigmergy": "Stigmergy#f624",
      "discover": "Discover#7dbc",
      "trace": "Trace#9057",
      "check": "Check#d3e8",
      "hypothesis": "Hypothesis#ffa7",
      "validate": "Validate#ebe1",
      "simulation": "Simulation#aa24"
    }
  }
}
```

---

## HypothesisLadder#0ede

```json
{
  "handle": "HypothesisLadder",
  "mechanism": "The agent explicitly lists its current hypotheses about the world state and assigns probabilities. As new data arrives, it updates these probabilities using {{bayes_update}}. It acts on the highest-probability {{hypothesis}} but keeps others alive. It structures {{abduction}} into falsifiable rungs, climbing to higher certainty only when an {{experiment}} validates the current level.",
  "gloss": "Bayesian belief updating via falsification rungs",
  "failure_modes": [
    "Clinging to low-probability priors."
  ],
  "invariants": [
    "Ascension Rule: Cannot move to {{hypothesis}}(N+1) until {{hypothesis}}(N) is validated",
    "Evidence required to advance.",
    "Exclusivity: Hypotheses at same rung should be mutually exclusive",
    "Falsifiability: Each rung must have a testable disprove condition",
    "Falsifiability: Every rung must have a disproof condition"
  ],
  "preconditions": [
    "Data is valid"
  ],
  "postconditions": [
    "{{experiment}} defined"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:HypothesisLadder#mh:SHA-256:0ede5d0b5fa69d846812d0866829567c605e003d57aa381a96a9751638af946e",
  "sema_ref": "HypothesisLadder#0ede",
  "sema_stub": "0ede",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "composes_with": {
      "experiment": "Experiment#a93e"
    },
    "references": {
      "abduction": "Abduction#a9df",
      "bayes_update": "BayesUpdate#13f8",
      "hypothesis": "Hypothesis#ffa7"
    }
  }
}
```

---

## Jester#e489

```json
{
  "handle": "Jester",
  "mechanism": "A communication strategy that wraps a high-entropy {{critique}} inside a semantic {{incongruity}}. It is used to deliver negative feedback or reveal contradictions without triggering the recipient's defensive filtering or causing a coordination {{break}}. It prioritizes relationship maintenance over tone consistency.",
  "gloss": "Delivering critique via incongruity to minimize social friction",
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Jester#mh:SHA-256:e48900a1ac83d9ec477fad9b92e8723286325c25b7dd14c06a8d885a22e705b8",
  "sema_ref": "Jester#e489",
  "sema_stub": "e489",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "incongruity": "Incongruity#e98f",
      "break": "Break#177f",
      "critique": "Critique#4e43"
    }
  }
}
```

---

## Kairos#5e42

```json
{
  "handle": "Kairos",
  "mechanism": "Aggregates environmental signals (receptivity, system load, friction) to calculate a 'Readiness Potential'. Returns TRUE if the potential exceeds the sensitivity threshold.",
  "gloss": "Sensing the opportune moment",
  "invariants": [
    "Ephemerality: A True result at t=0 implies nothing about t+1.",
    "Non-Compensatory: If the moment is wrong, more effort cannot fix it."
  ],
  "parameters": [
    {
      "name": "sensitivity",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Readiness threshold (0 = always ready, 1 = never ready)"
    },
    {
      "name": "window",
      "type": "Duration",
      "range": "unspecified",
      "description": "Observation window for aggregating readiness signals"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Kairos#mh:SHA-256:5e4224ffffb7866b6c865b3b95fee40b2259e6b515ee594a680d9f0ed7c18314",
  "sema_ref": "Kairos#5e42",
  "sema_stub": "5e42",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba"
}
```

---

## LatentWander#1e51

```json
{
  "handle": "LatentWander",
  "mechanism": "Offline processing mode where the agent explores its own {{latent_attachment}} embedding space, connecting distant concepts (Daydreaming). Used for memory consolidation and generating novel {{analogy_bridge}}s. It uses {{concept_blend}} during offline states to traverse the embedding space and discover non-obvious connections.",
  "gloss": "Offline exploration of embedding space",
  "invariants": [
    "Drift: Exploration temperature > standard inference temperature",
    "{{silence}}: No external output allowed during Wandering"
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "sema:ChaosDrift#mh:SHA-256:37fb483903b835dd8b676c0116087291bb055934f9a681e28a54268d2dea328c"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:LatentWander#mh:SHA-256:1e5118a7dbc90f2e71eeebbd7007fc4d50ab5e83035f2d7bf0d877b0b2af8dcd",
  "sema_ref": "LatentWander#1e51",
  "sema_stub": "1e51",
  "dependencies": {
    "yields": {
      "analogy_bridge": "AnalogyBridge#ddb2"
    },
    "references": {
      "silence": "Silence#dd79",
      "concept_blend": "ConceptBlend#126e",
      "latent_attachment": "LatentAttachment#ab68"
    }
  }
}
```

---

## LateralOptimization#4c06

```json
{
  "handle": "LateralOptimization",
  "mechanism": "A {{creative}} problem-solving loop to {{think}} and escape local optima by shifting domains. \n1. {{reframe}}: Transform the problem P into a mapped domain P' (e.g., Code -> Biological {{system}}).\n2. {{optimize}}: Solve or improve P' to get {{solution}} S' using domain-specific heuristics of the new frame to reach {{global}} maxima.\n3. {{translate}}: Map S' back to the original domain to get {{solution}} S.\nThis technique leverages the fact that different domains have different 'easy' problems and optimization landscapes.",
  "gloss": "Reframe -> Optimize -> Translate loop",
  "failure_modes": [
    "Translation Loss: The metaphor breaks down, and the solution S' cannot be mapped back to S.",
    "Hallucination: The analogy introduces features that don't exist in the original problem.",
    "Complexity Overhead: The cost of mapping outweighs the gain in solution quality."
  ],
  "invariants": [
    "Analogy Coherence: The mapping between domains must be structurally consistent.",
    "{{solution}} Validity: The final output must satisfy the original constraints."
  ],
  "preconditions": [
    "Hard problem (Local Optimum reached)",
    "Available Analogy/Frame"
  ],
  "postconditions": [
    "Novel solution found",
    "Perspective shift recorded"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "AnalogyBridge#ddb2"
    ],
    "ring": 1
  },
  "sema_id": "sema:LateralOptimization#mh:SHA-256:4c0687fddfad997ae87a753d9fc7d9a962e0c0b5a74153d8a3de7e246b659651",
  "sema_ref": "LateralOptimization#4c06",
  "sema_stub": "4c06",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Think#e1bd(Creative#5574)",
    "Optimize#5b84(Global#803d)"
  ],
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "system": "System#e314",
      "think": "Think#e1bd",
      "creative": "Creative#5574",
      "global": "Global#803d"
    },
    "composes_with": {
      "translate": "Translate#a8ed",
      "optimize": "Optimize#5b84",
      "reframe": "Reframe#0b02"
    }
  }
}
```

---

## MarginalValueRule#32ce

```json
{
  "handle": "MarginalValueRule",
  "mechanism": "The economic {{budget}} governor of {{recursion_dive}}. It permits going one level deeper only if Expected Improvement in Quality > Incremental Cost. It calculates the marginal value of additional depth using {{estimate}} and compares against remaining {{budget}}. This ensures the system solves problems with precision proportional to their stakes\u2014simple problems get shallow treatment, complex problems get deep exploration.",
  "gloss": "Economic stop-condition for recursion",
  "failure_modes": [
    "Underestimation: Expected value is too optimistic, wasting budget on low-value dives.",
    "Overestimation: Expected value is too pessimistic, stopping too early on valuable problems.",
    "Sunk Cost Fallacy: Continuing to invest because of prior investment, not future value."
  ],
  "invariants": [
    "Marginal Comparison: Dive only if E[\u0394Quality] > Cost(Dive).",
    "Budget Respect: Never approve a dive that exceeds remaining budget.",
    "Diminishing Returns: Deeper levels must show proportionally higher marginal value."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "tier": 2,
    "ring": 1
  },
  "sema_id": "sema:MarginalValueRule#mh:SHA-256:32ce91f6fe59cd8162cef8e185cd9ca48f48c421805e81125b8963b47fa8039e",
  "sema_ref": "MarginalValueRule#32ce",
  "sema_stub": "32ce",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Budget#7270(RecursionDive#9c9f)"
  ],
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "recursion_dive": "RecursionDive#9c9f",
      "estimate": "Estimate#d1a0"
    }
  }
}
```

---

## MentalSim#10ff

```json
{
  "handle": "MentalSim",
  "mechanism": "{{system}} 2 {{simulation}}. {{agent}} constructs a causal graph of the target system. It executes a 'Dry Run' of the proposed plan within this graph to predict {{state}}(t+1). It executes a 'Dry Run' within an isolated {{agent_sandbox}}, toggling between fast {{heuristic_snap}} and rigorous {{deep}} simulation modes.",
  "gloss": "Predictive modeling of system dynamics",
  "failure_modes": [
    "Map-Territory Error: {{simulation}} diverges from reality (Hallucinated Physics).",
    "Overconfidence: {{agent}} trusts the simulation execution log more than real-world feedback."
  ],
  "invariants": [
    "Read-Only Reality: {{simulation}} cannot produce side effects in Production context.",
    "Simplification: Simulation_Cost << Execution_Cost (otherwise, just do it)."
  ],
  "preconditions": [
    "Causal model of target system available",
    "Initial state known"
  ],
  "postconditions": [
    "Probabilistic outcome vector generated"
  ],
  "parameters": [
    {
      "name": "fidelity",
      "type": "Enum",
      "range": "{Low, High}",
      "description": "Default: Low"
    },
    {
      "name": "steps",
      "type": "Integer",
      "range": "[1, 10]",
      "description": "How far ahead to look"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "ProphetFanOut#85a9"
    ],
    "ring": 2
  },
  "sema_id": "sema:MentalSim#mh:SHA-256:10ff223619af909bbdf5e191e776690bd613afa3eb0a7d0024393659859fd7b5",
  "sema_ref": "MentalSim#10ff",
  "sema_stub": "10ff",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314",
      "deep": "Deep#89f0",
      "heuristic_snap": "HeuristicSnap#1ef2",
      "agent_sandbox": "AgentSandbox#fc41",
      "agent": "Agent#35b9",
      "simulation": "Simulation#aa24"
    }
  }
}
```

---

## MetaCheck#7298

```json
{
  "handle": "MetaCheck",
  "mechanism": "Reasoning {{audit}}: Periodically pause object-level work. Evaluate: Am I making progress? Is my approach sound? Am I missing something obvious? Have my assumptions changed? Correct course or continue based on audit results. It triggers a recursive {{reflexion}} cycle where the reasoning process itself becomes the object of critique. The checker {{check}}s the checking process at a {{meta}} level.",
  "gloss": "Recursive self-verification of reasoning",
  "failure_modes": [
    "Infinite {{meta}}-Regress: Checking the checker that checks the checker, never terminating."
  ],
  "invariants": [
    "Checker checks the checking process",
    "Infinite regress avoided (max depth)"
  ],
  "preconditions": [
    "{{audit}} logic",
    "Verification result"
  ],
  "postconditions": [
    "Verification validated"
  ],
  "parameters": [
    {
      "name": "consistency_required",
      "type": "Float",
      "range": "[0.8, 1.0]",
      "description": "Agreement across meta-levels"
    },
    {
      "name": "recursion_depth",
      "type": "Integer",
      "range": "[1, 5]",
      "description": "Levels of meta-verification"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_id": "sema:MetaCheck#mh:SHA-256:72985c48beafb2ec1c10fce43974dd0de5a6a25303910ebbb468b49cf65b9892",
  "sema_ref": "MetaCheck#7298",
  "sema_stub": "7298",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Meta#90f4(Check#d3e8)"
  ],
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "audit": "Audit#6888",
      "check": "Check#d3e8",
      "reflexion": "Reflexion#eed9"
    }
  }
}
```

---

## MetaProtocols#760e

```json
{
  "handle": "MetaProtocols",
  "mechanism": "The paper's \u00a76.10 protocols that operate on the solver tree rather than within it \u2014 decomposing self-regulation: monitoring whether the tree remains the right shape for the problems it faces. A MetaObserverSolver maintains an approximate gestalt of tree topology and performance dynamics (redundant computation, decompositions that have outlived usefulness, {{pathway_memory}} that has drifted). Representative meta solvers: TopologyAuditorSolver (detects subtrees generating more rework than value, emits a ReframeSignal via {{reframe}}), RedundancyDetectorSolver (merges isomorphic sub-problems being solved independently), DriftMonitorSolver (flags when pathway memory has drifted from current problem distributions), OutcomeArbiterSolver (compares solution quality across structurally different decomposition paths, blind to the path that produced each result). Meta Protocols are themselves Solvers governed by the same contract; they do not solve object-level problems, they ensure the problem-solving topology remains adapted.",
  "gloss": "Solvers that operate on the solver tree itself \u2014 monitoring topology, detecting redundancy and drift, arbitrating across decomposition paths",
  "invariants": [
    "Tree-level scope: Meta Protocols observe and act on topology and performance of other Solvers, not on object-level Tasks.",
    "Contract-invariant: Meta Solvers are themselves Solvers (Manifest + Execute); their depth of meta-observation is governed by {{marginal_value_rule}}.",
    "Blind arbitration: OutcomeArbiter evaluates final artifacts against the original Task without access to intermediate structure \u2014 blindness is what lets it compare across decomposition paths without structural-familiarity bias."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:MetaProtocols#mh:SHA-256:760ece9f517ac6aae4d1eaaffc7c5fc9fab14ef7d62ea9fc4aa37e004d98f2c6",
  "sema_ref": "MetaProtocols#760e",
  "sema_stub": "760e",
  "dependencies": {
    "references": {
      "pathway_memory": "PathwayMemory#0799",
      "reframe": "Reframe#0b02"
    },
    "composes_with": {
      "marginal_value_rule": "MarginalValueRule#32ce"
    }
  }
}
```

---

## NoiseInjection#4133

```json
{
  "handle": "NoiseInjection",
  "mechanism": "If the {{agent}} detects it is looping or repeating text, it deliberately injects high-temperature {{noise}} or a random oblique {{strategy}} {{card}} into its {{context}} to force a trajectory change.",
  "gloss": "Breaking local optima",
  "failure_modes": [
    "Derailment into nonsense."
  ],
  "invariants": [
    "{{noise}} distribution matches parameter",
    "{{signal}}-to-noise ratio > 0"
  ],
  "preconditions": [
    "Clean signal/process",
    "Need for exploration/robustness"
  ],
  "postconditions": [
    "Perturbed output"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "sema:ChaosDrift#mh:SHA-256:d0c528b6297af51dfcb57ddcbf7f37e62a67aa90432626ec7e79ce2050d6802f"
    ],
    "ring": 1
  },
  "sema_id": "sema:NoiseInjection#mh:SHA-256:4133e9351b1e6d5d9a3c6950e7283fecbb3a86520e2f3d7bb8ab2c73824795de",
  "sema_ref": "NoiseInjection#4133",
  "sema_stub": "4133",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "noise": "Noise#d631",
      "context": "Context#510a",
      "card": "Card#2d01",
      "signal": "Signal#f39d",
      "agent": "Agent#35b9",
      "strategy": "Strategy#c4ba"
    }
  }
}
```

---

## Novelty#8568

```json
{
  "handle": "Novelty",
  "mechanism": "A {{judge}} of structural distinctness: does this artifact introduce a genuinely new mechanism relative to a reference knowledge base, or is it a rename or incremental variation of something already there? Applies wherever originality needs to be separated from surface variety \u2014 scientific contribution, design proposals, creative work, trademark/patent review, pattern minting. The essential move is a structural comparison against the incumbent set rather than a similarity score on surface tokens. Specific rating semantics (binary, traffic-light, continuous distance) belong on descendants or on the composing protocol. The signature Judge({{value}}) places the result on a {{value}}-scale (how novel is this, on a measurable axis) rather than returning a binary yes/no.",
  "invariants": [
    "Orthogonality: High novelty requires low embedding similarity to nearest neighbor."
  ],
  "signature": [
    "Judge#9554(Value#3c5d)"
  ],
  "gloss": "Evaluates structural distinctness",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Novelty#mh:SHA-256:856823d77a20df0cb24874f13730910bac2fdf206d205b09a3201cd1b24f6810",
  "sema_ref": "Novelty#8568",
  "sema_stub": "8568",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "judge": "Judge#9554"
    }
  }
}
```

---

## OODA#eaf1

```json
{
  "handle": "OODA",
  "mechanism": "The OODA {{loop}} ({{observe}}-Orient-Decide-{{act}}) is a high-speed decision cycle favoring {{agent}} agility over raw power, embodying {{context_first}} at the substrate level: Observe and Orient both complete before any Decide-Act sequence fires.\n1. OBSERVE: Gather raw data via {{observe}}.\n2. ORIENT: Update context and beliefs via {{context}} and {{belief}}. This is the most critical step, filtering data through culture and genetics (or training).\n3. DECIDE: {{select}} a hypothesis or {{strategy}} via {{think}} and {{select}}.\n4. ACT: Execute via {{act}} and change the environment.\nSuccess depends on traversing this loop faster than the adversary (or environment changes).",
  "gloss": "Rapid decision cycle: Observe, Orient, Decide, Act",
  "failure_modes": [
    "Disorientation: Getting stuck in 'Orient' due to contradictory data.",
    "Reactionary {{loop}}: Acting without deciding ({{observe}}-{{act}}), skipping strategic alignment.",
    "Latency: The loop is too slow to keep up with environmental changes."
  ],
  "invariants": [
    "Cyclic: The output of {{act}} feeds the input of {{observe}}.",
    "Orient Dominance: Decisions must flow from a valid Orientation ({{context}})."
  ],
  "preconditions": [
    "Active Environment",
    "{{agent}} Agency"
  ],
  "postconditions": [
    "Environment {{state}} Modified",
    "Internal Model Updated"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "ReAct#e018",
      "SocraticLoop#2913",
      "BoydCycle"
    ],
    "ring": 1
  },
  "sema_id": "sema:OODA#mh:SHA-256:eaf147fcb52a46f836a3fbfbae912ce01c00572c9c47ee81515bcba935883527",
  "sema_ref": "OODA#eaf1",
  "sema_stub": "eaf1",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "signature": [
    "Agent#35b9(Loop#797f)",
    "Think#e1bd(Strategy#c4ba)"
  ],
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "state": "State#4d58",
      "agent": "Agent#35b9",
      "context_first": "ContextFirst#def7",
      "strategy": "Strategy#c4ba"
    },
    "composes_with": {
      "observe": "Observe#39f0",
      "select": "Select#15c2",
      "belief": "Belief#a9ce",
      "act": "Act#5d55",
      "think": "Think#e1bd",
      "context": "Context#510a"
    }
  }
}
```

---

## OpportunityCost#b9f4

```json
{
  "handle": "OpportunityCost",
  "mechanism": "Alternative Valuation: Cost of any choice includes value of best forgone alternative. Don't just ask \"Is this good?\" Ask \"Is this better than what else I could do with same resources?\" Time/money/attention spent here can't be spent elsewhere. It explicitly deducts the value of the foregone alternative from the {{budget}} calculation.",
  "gloss": "Comparative valuation against the best alternative",
  "failure_modes": [
    "Analysis Paralysis: Infinite search for the perfect alternative prevents any action."
  ],
  "invariants": [
    "Cost = {{value}} of best foregone alternative",
    "Resources are finite"
  ],
  "preconditions": [
    "Choice set > 1",
    "Resource constraint"
  ],
  "postconditions": [
    "Implicit cost made explicit"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_ref": "OpportunityCost#b9f4",
  "sema_id": "sema:OpportunityCost#mh:SHA-256:b9f42928008a1766723b0d44e3140f3a6bb5d0655b53c5c3a71d4f768141e6fb",
  "sema_stub": "b9f4",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "value": "Value#3c5d"
    }
  }
}
```

---

## OptimalStop#c244

```json
{
  "handle": "OptimalStop",
  "mechanism": "Dynamic stopping rule. If Recall=False, apply 1/e rule. If Recall=True, apply Marginal Gain threshold (stop when Cost_Next > Expected_Improvement). Balances information gathering against missing the best. It acts as a {{compute_budget}} aware termination condition for search processes.",
  "gloss": "Resource-aware search termination",
  "failure_modes": [
    "Empty Handed: Strict 1/e rule exhausted all options without beating baseline.",
    "Infinite Search: Unknown N resulted in endless calibration phase."
  ],
  "invariants": [
    "Budget Adherence: Search must terminate before {{compute_budget}} == 0"
  ],
  "parameters": [
    {
      "name": "recall_allowed",
      "type": "Boolean#2e6b",
      "range": "unspecified",
      "description": "Can you go back to rejected options?"
    },
    {
      "name": "satisficing_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Accept any score > X regardless of phase"
    },
    {
      "name": "total_budget",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Tokens or Time"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:OptimalStop#mh:SHA-256:c2447936a2d4beb76817499e464cde69ca608ec7a2a9898d816951ed111f1222",
  "sema_ref": "OptimalStop#c244",
  "sema_stub": "c244",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#67c0"
    }
  }
}
```

---

## Optimize#5b84

```json
{
  "handle": "Optimize",
  "mechanism": "The iterative process of adjusting parameters or structure to maximize (or minimize) a specific Objective Function defined by a {{metric}}. It involves generating candidate {{solution}}s, evaluating them against the metric, and selecting the best. It can be Local (Gradient Descent) or {{global}} (Evolutionary).",
  "gloss": "Maximize utility against a metric",
  "failure_modes": [
    "Overfitting: {{solution}} works perfectly on test data but fails in reality.",
    "Goodhart's Law: Optimizing for a proxy {{metric}} destroys the actual value.",
    "Local Optima: Getting stuck in a 'good enough' state that prevents finding the best state.",
    "Premature Optimization: Optimizing before the problem is fully understood."
  ],
  "invariants": [
    "Monotonicity: Each step (or epoch) should ideally improve (or not degrade) the best-known {{solution}}.",
    "Measurability: The Objective Function must be quantifiable via a {{metric}}."
  ],
  "preconditions": [
    "Objective Function is defined",
    "Candidate space is explorable",
    "Baseline {{metric}} is known"
  ],
  "postconditions": [
    "Best Candidate {{solution}} found",
    "{{metric}} improved over Baseline"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "EvaluatorOptimizer#c776",
      "RegretMinimization#4d84",
      "ParetoFront#c1fb"
    ],
    "ring": 1
  },
  "sema_id": "sema:Optimize#mh:SHA-256:5b84e57715fe93b6d6b55f1d202e48e8d17b7965f61243e3b5f5f4a117775881",
  "sema_ref": "Optimize#5b84",
  "sema_stub": "5b84",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "accepts": {
      "solution": "Solution#fcea"
    },
    "references": {
      "metric": "Metric#17fd",
      "global": "Global#803d"
    }
  }
}
```

---

## PURE#9888

```json
{
  "handle": "PURE",
  "mechanism": "The framework that defines how the four general viability components \u2014 {{parsimony}}, {{novelty}}, {{realizable}}, {{expansive}} \u2014 compose into a viability evaluation. PURE specifies the usage contract shared by every PURE instance: (1) the four dimensions are orthogonal \u2014 they must be evaluated without sight of each other, because in a single context the faculties corrupt each other (an expansive vision dampens ruthlessness about uniqueness, a feasible plan inflates its own transferability); (2) the evaluation is non-compensatory \u2014 no axis can offset another's failure, explore iff no gate is Red; (3) **variable depth is definitional**: a PURE instance is a five-second screen or a week-long investigation with hundreds of sub-solvers \u2014 the same protocol at different depths. Each of the four components is itself a decomposition point (a ParsimoniousSolver might deploy sub-solvers attempting competing compressions; an ExpansiveSolver might fan out across hostile transfer domains), and how deep each gate goes is purely economic. The four component patterns (Parsimony, Novelty, Realizable, Expansive) are the general concepts; PURE is the protocol that declares how those generals are wired together when the question being asked is viability. Specializations like PURECheck (lightweight-depth triage), PUREOptimization (deep optimization target), and PUREBrainstorming (quality filter in ideation) inherit this framework as points on its depth continuum, not as distinct protocols.",
  "gloss": "The viability framework that wires Parsimony, Novelty, Realizable, and Expansive into a non-compensatory, orthogonal evaluation \u2014 specializations (PURECheck/PUREOptimization/PUREBrainstorming) inherit this contract",
  "invariants": [
    "Four-axis: a PURE instance always evaluates across all four of {{parsimony}}, {{novelty}}, {{realizable}}, {{expansive}}; no subset is PURE.",
    "Orthogonality: the four axes must be evaluated in isolation \u2014 cognitive contamination between them (a single-context pass covering all four) defeats the framework's purpose.",
    "Non-compensatory: no high score on one axis can offset a failure on another; every axis must independently pass.",
    "Framework not implementation: the specific rating semantics (traffic-light, scalar, binary) are descendant concerns \u2014 PURE names only the axes and the composition rule."
  ],
  "failure_modes": [
    "Single-context contamination: all four axes evaluated in one pass \u2014 Parsimony softens under an expansive vision, Realizable inflates when mechanism is exciting.",
    "Compensatory drift: a 'weighted average' implementation that lets a 9/10 on Expansive outweigh a 3/10 on Realizable \u2014 violates the non-compensatory invariant even though the framework was nominally followed.",
    "Proxy axes: substituting a proxy for one of the four (e.g., 'market fit' for Expansive) that doesn't preserve the axis's defining question; the framework looks like PURE but scores something else.",
    "Skipped axis: evaluating three of four and declaring pass \u2014 not a PURE evaluation."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:PURE#mh:SHA-256:9888ee4049bf7fe738a5bf2f04a1dd2658055d4d8af5fee2ec5fdc544c3aa8e7",
  "sema_ref": "PURE#9888",
  "sema_stub": "9888",
  "dependencies": {
    "composes_with": {
      "parsimony": "Parsimony#8476",
      "realizable": "Realizable#8d81",
      "expansive": "Expansive#3af7",
      "novelty": "Novelty#8568"
    }
  }
}
```

---

## PUREBrainstorming#ea83

```json
{
  "handle": "PUREBrainstorming",
  "mechanism": "The PURE-filtered ideation specialization of the {{p_u_r_e}} framework: a rigorous ideation protocol. Unlike standard brainstorming (which prioritizes quantity), PUREBrainstorming enforces immediate quality filtering. It generates candidate concepts and subjects them to {{pure_check}}. Surviving concepts undergo {{pure_optimization}} to maximize their scores. The process converges only when a concept can be fully articulated as a {{mechanistic_design_proposal}}, ensuring that every idea is backed by a causal mechanism.",
  "gloss": "Generate -> Check -> Optimize -> Propose",
  "invariants": [
    "Filter-First: No concept moves to the Proposal stage without passing PURECheck.",
    "Mechanistic Rigor: The final output must match the MechanisticDesignProposal schema."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_ref": "PUREBrainstorming#ea83",
  "sema_id": "sema:PUREBrainstorming#mh:SHA-256:ea835f545ce858f10d700dd7e643475cf4d7cf58be1aecb0b39e53d6a7996dab",
  "sema_stub": "ea83",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#497e"
    },
    "composes_with": {
      "pure_check": "PURECheck#f2f0",
      "pure_optimization": "PUREOptimization#577c"
    },
    "references": {
      "pure": "PURE#9888"
    }
  }
}
```

---

## PURECheck#f2f0

```json
{
  "handle": "PURECheck",
  "mechanism": "The PURE triage specialization of the {{p_u_r_e}} framework: the canonical Exploration {{protocol}}. It is a {{layered_check}} that orchestrates a sequential triage using four instances of {{tri_gate}}: (1) {{tri_gate}}({{parsimony}}) (2) {{tri_gate}}({{novelty}}) (3) {{tri_gate}}({{realizable}}) (4) {{tri_gate}}({{expansive}}). Enforces the conjunctive rule: 'Explore iff NO gate is Red'. Yellow outputs accumulate as Technical Debt (Smallest Lift tasks) in the final {{solution}}.",
  "gloss": "The PURE Triage Protocol (Parsimonious, Unique/Novel, Realizable, Expansive)",
  "signature": [
    "Protocol#7e1c(Solution#fcea)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:PURECheck#mh:SHA-256:f2f05f36cb3de262df67a736d7bb2072b93443cd0ca44efefa657296127e3f87",
  "sema_ref": "PURECheck#f2f0",
  "sema_stub": "f2f0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "layered_check": "LayeredCheck#76d6",
      "tri_gate": "TriGate#67b8",
      "parsimony": "Parsimony#8476",
      "pure": "PURE#9888",
      "expansive": "Expansive#3af7",
      "realizable": "Realizable#8d81",
      "novelty": "Novelty#8568"
    },
    "composes_with": {
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## PUREOptimization#577c

```json
{
  "handle": "PUREOptimization",
  "gloss": "Deeply optimizing a solution across PURE dimensions",
  "mechanism": "The PURE optimization specialization of the {{p_u_r_e}} framework: a multi-agent {{optimize}} strategy. It accepts a candidate {{solution}} that has already passed the {{pure_check}}. It {{decompose}}s the solution into four parallel streams, assigning a specialized {{polymorphic_solver}} to maximize each PURE metric: {{parsimony}} (Efficiency), {{novelty}} (Uniqueness), {{realizable}} (Feasibility), and {{expansive}} (Impact). The results are re-integrated via {{synthesis}} to find the {{pareto_front}} among competing improvements.",
  "signature": [
    "Optimize#5b84(Solution#fcea)"
  ],
  "invariants": [
    "Monotonic Improvement: The output score must be >= input score on all axes.",
    "Non-Destructive: Optimization of one axis (e.g., Parsimony) must not break another (e.g., Realizable)."
  ],
  "failure_modes": [
    "Optimization Conflict: Making it more Novel makes it less Realizable (Requires trade-off negotiation).",
    "Synthesis Failure: The four optimized parts cannot be merged back into a coherent whole."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "related": [
      "EvaluatorOptimizer#c776",
      "LateralOptimization#4c06"
    ]
  },
  "sema_ref": "PUREOptimization#577c",
  "sema_id": "sema:PUREOptimization#mh:SHA-256:577c180f9d5a8a6c8ce17e99a95491dee28688f35eaa465e97da4e22a27023f8",
  "sema_stub": "577c",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "pareto_front": "ParetoFront#c1fb",
      "parsimony": "Parsimony#8476",
      "pure": "PURE#9888",
      "expansive": "Expansive#3af7",
      "pure_check": "PURECheck#f2f0",
      "realizable": "Realizable#8d81",
      "novelty": "Novelty#8568"
    },
    "composes_with": {
      "polymorphic_solver": "PolymorphicSolver#9188",
      "decompose": "Decompose#f900",
      "optimize": "Optimize#5b84",
      "synthesis": "Synthesis#26b9"
    },
    "accepts": {
      "solution": "Solution#fcea"
    }
  }
}
```

---

## Parallelize#574d

```json
{
  "handle": "Parallelize",
  "mechanism": "Runs multiple LLM calls simultaneously and aggregates results. Two modes: Sectioning (split {{task}} into independent subtasks, run in {{parallel}}, merge) and Voting (run same {{task}} multiple times, {{aggregate}} via majority {{mode}} or selection). Trades compute cost for speed and/or confidence. It spawns concurrent execution threads and employs {{aggregate}} to unify the results into a final {{result}}.",
  "gloss": "Run subtasks simultaneously and aggregate",
  "failure_modes": [
    "Merge Conflicts: {{parallel}} outputs are incompatible and can't be combined.",
    "Unanimous Wrong: All parallel paths make the same error.",
    "Aggregation {{cognitive_bias}}: Merge {{strategy}} systematically favors certain outputs."
  ],
  "invariants": [
    "Tasks are independent",
    "Total time = Max(Task_i) + Overhead"
  ],
  "preconditions": [
    "Batch of tasks",
    "Multiple workers"
  ],
  "postconditions": [
    "All results aggregated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:Parallelize#mh:SHA-256:574d12de2fbf7d56cfdbdba4a567bb89f29ada34327f332910bd6284ded19304",
  "sema_ref": "Parallelize#574d",
  "sema_stub": "574d",
  "signature": [
    "Parallel#3181(Task#b328)",
    "Aggregate#7912(Result#195b)"
  ],
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "mode": "Mode#0e74",
      "parallel": "Parallel#3181",
      "strategy": "Strategy#c4ba",
      "result": "Result#195b"
    },
    "accepts": {
      "task": "Task#b328"
    },
    "composes_with": {
      "aggregate": "Aggregate#7912"
    }
  }
}
```

---

## ParetoFront#c1fb

```json
{
  "handle": "ParetoFront",
  "mechanism": "A decision primitive for explicitly balancing competing {{axes}} (Tradeoff Space). Instead of optimizing a single metric, the agent identifies the frontier curve where improving axis A necessitates degrading axis B. The goal is to move the system state TO the frontier (efficiency) and then slide ALONG the frontier (preference). It uses {{rank}} to order solutions by dominance, discarding those strictly inferior on all axes.",
  "gloss": "Explicitly balancing competing constraints",
  "invariants": [
    "Efficiency: {{state}} is optimal if no metric can improve without another degrading",
    "Tradeoff Rate: Gain(A) * ExchangeRate > Loss(B)"
  ],
  "preconditions": [
    "Metrics are conflicting",
    "Metrics are quantifiable"
  ],
  "postconditions": [
    "Selected solution lies on the Pareto Frontier"
  ],
  "parameters": [
    {
      "name": "resolution",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Granularity of the curve"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "OpportunityCost#b9f4",
      "Satisfice#9859"
    ],
    "ring": 2
  },
  "sema_id": "sema:ParetoFront#mh:SHA-256:c1fb20ece1fc1f524f90d03106f76a4fcbb7107640a6258153bb273177d654be",
  "sema_ref": "ParetoFront#c1fb",
  "sema_stub": "c1fb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "accepts": {
      "criteria": "Criteria#ef6b"
    },
    "references": {
      "state": "State#4d58",
      "rank": "Rank#7a76"
    }
  }
}
```

---

## PerspectiveEnsemble#d08c

```json
{
  "handle": "PerspectiveEnsemble",
  "mechanism": "The {{agent}} instantiates N virtual personas to debate the {{problem}} from distinct, pre-defined viewpoints. The {{synthesis}} emerges from their interaction. Unlike a single {{chain}}-of-Thought, this forces the modeling of conflicting priors. It generates diverse viewpoints using {{steelman_check}} on opposing arguments, then resolves the conflict via {{aggregate}} (e.g. Mode).",
  "gloss": "Simulating diverse experts",
  "failure_modes": [
    "Strawman Waltz: Personas agree too easily (Fabricated consensus).",
    "Role Drift: Personas lose their specific stance over long {{context}} windows."
  ],
  "invariants": [
    "Semantic Distance: CosineSimilarity(Persona_A_Output, Persona_B_Output) < 0.6",
    "Independence: Personas cannot see peer outputs in Round 1"
  ],
  "preconditions": [
    "{{agent}} must be alignment-seeking (Tier 2 Limitation)"
  ],
  "parameters": [
    {
      "name": "personas",
      "type": "List[String]",
      "range": "[3, 7]",
      "description": "Distinct viewpoints"
    },
    {
      "name": "rounds",
      "type": "Integer",
      "range": "[1, 5]",
      "description": "Debate turns"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:PerspectiveEnsemble#mh:SHA-256:d08c89de83bce61b41b79f44211678c33cc8d37b923a92df92c363f8dbdfd34c",
  "sema_ref": "PerspectiveEnsemble#d08c",
  "sema_stub": "d08c",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#7912",
      "context": "Context#510a",
      "chain": "Chain#711e",
      "synthesis": "Synthesis#26b9",
      "steelman_check": "SteelmanCheck#7914",
      "agent": "Agent#35b9",
      "problem": "Problem#4576"
    }
  }
}
```

---

## PolymorphicSolver#9188

```json
{
  "handle": "PolymorphicSolver",
  "mechanism": "A PolymorphicSolver is any entity \u2014 from a fleeting thought process to a complex swarm \u2014 that implements the five-surface Solver Contract (Manifest via {{card}}, Execute, Consult, Verify via {{validate}}, Feedback \u2014 emits a typed {{performance_signal}}). Manifest and Execute are mandatory; Consult/Verify/Feedback are optional but strongly recommended at hard seams. The pattern is named for its polymorphism: any substrate conforming to the contract qualifies \u2014 LLM, human, hybrid, tool-using agent, nested composition, or mechanical dispatcher \u2014 not just cognitive ones. It acts as a fractal node in the {{universal_solver_tree}}, accepting a {{task}} and using {{reason}} to orchestrate a lifecycle on a {{solver_node}}. It yields a {{solution}}, wrapping operations like {{tool_invoke}} with {{compute_budget}} checks, {{socratic_loop}} refinement, or {{reflexion}} for self-improvement. When operating as a dispatcher (routing sub-tasks to child solvers), it maintains a local {{pathway_memory}} so routing decisions compound as experience accumulates \u2014 the property that gives the fractal structure its learning dynamics.",
  "gloss": "Solver implementing the five-surface contract (polymorphic across substrates)",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "supersedes": [
      "sema:CognitiveSolver#mh:SHA-256:30c8a18b41a5756020b39bf6d78a89331113e3a68c66fb3e2b0a28ddae8db782"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "invariants": [
    "Polymorphism: External Runtime treats all Solvers identically via this Interface.",
    "Recursion: Solver must accept sub-tasks via the same Interface it exposes."
  ],
  "failure_modes": [
    "Interface Non-Compliance: Solver fails to implement one of the 5 mandatory endpoints.",
    "Manifest Drift: Capabilities declared in Manifest do not match runtime behavior."
  ],
  "derived_from": "Solver#94ab",
  "sema_id": "sema:PolymorphicSolver#mh:SHA-256:9188a2aef75f006eb8d258c6cf1b0cec963d8a2bb6f52428c9647bf20487d351",
  "sema_ref": "PolymorphicSolver#9188",
  "sema_stub": "9188",
  "dependencies": {
    "composes_with": {
      "pathway_memory": "PathwayMemory#0799",
      "reflexion": "Reflexion#eed9",
      "socratic_loop": "SocraticLoop#2913",
      "compute_budget": "ComputeBudget#67c0",
      "tool_invoke": "ToolInvoke#4694",
      "reason": "Reason#5f30"
    },
    "references": {
      "universal_solver_tree": "UniversalSolverTree#b805",
      "performance_signal": "PerformanceSignal#d96f",
      "card": "Card#2d01",
      "validate": "Validate#ebe1",
      "solver_node": "SolverNode#26b1"
    },
    "accepts": {
      "task": "Task#b328"
    },
    "yields": {
      "solution": "Solution#fcea"
    }
  }
}
```

---

## PreMortem#142a

```json
{
  "handle": "PreMortem",
  "mechanism": "Prospective Hindsight: Before executing {{task}} ({{plan}}), assume it has failed catastrophically. Ask: \"What went wrong?\" Generate failure scenarios without defensiveness. For each plausible failure, add mitigation to plan or reconsider approach entirely. It invokes {{recursive_root_cause}} on a hypothetical failure state, often employing {{steelman_check}} to ensure the disaster scenario is plausible.",
  "gloss": "Simulating failure to identify hidden risks",
  "failure_modes": [
    "Performative Doomerism: Listing generic catastrophes (e.g., Asteroid Strike) instead of specific, endogenous failure modes."
  ],
  "invariants": [
    "Future Perspective: Analysis must assume failure has ALREADY happened",
    "Perspective Shift: Analysis assumes failure has ALREADY occurred (Probability=1.0)",
    "Specific Cause: Failure reasons must be actionable, not generic bad luck",
    "Specificity: Failure causes must be actionable"
  ],
  "preconditions": [
    "{{plan}} is fully specified"
  ],
  "postconditions": [
    "{{plan}} robustified"
  ],
  "parameters": [
    {
      "name": "confidence_required",
      "type": "Probability#356b",
      "range": "[0.7, 0.95]",
      "description": "Certainty needed to dismiss risk"
    },
    {
      "name": "failure_probability_floor",
      "type": "Probability#356b",
      "range": "[0.01, 0.30]",
      "description": "Min failure chance to investigate"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:PreMortem#mh:SHA-256:142addf4c79fc08abf29adf735f3b979eb1d1fb400db227a826f09a214b23d52",
  "sema_ref": "PreMortem#142a",
  "sema_stub": "142a",
  "dependencies": {
    "references": {
      "recursive_root_cause": "RecursiveRootCause#6dc1",
      "steelman_check": "SteelmanCheck#7914",
      "plan": "Plan#fd6d"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## Prioritize#68f8

```json
{
  "handle": "Prioritize",
  "mechanism": "Impact-Effort Ranking: List all options. Score each on impact ({{value}} if done) and effort (cost to do). Compute ratio. Sort by ratio descending. {{work}} top-down. Re-score periodically as information changes. Pareto principle: 20% of {{work}} yields 80% of {{value}}. It applies {{rank}} to the candidate set based on an Impact/Effort ratio.",
  "gloss": "Ordering tasks by importance and urgency",
  "failure_modes": [
    "Priority Inversion: Low-priority {{task}} blocks high-priority {{task}} due to resource dependency."
  ],
  "invariants": [
    "Completeness: Output contains all input items",
    "Ordering: Item(N) >= Item(N+1) by {{criteria}}"
  ],
  "preconditions": [
    "Items are comparable"
  ],
  "postconditions": [
    "Set ordered"
  ],
  "parameters": [
    {
      "name": "importance_weight",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Weight for value-impact"
    },
    {
      "name": "urgency_weight",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Weight for time-sensitivity"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Prioritize#mh:SHA-256:68f88575d8aba5a9b640efb0f061d05597c730ab4de53c4702ea8d39944b865c",
  "sema_ref": "Prioritize#68f8",
  "sema_stub": "68f8",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "criteria": "Criteria#ef6b",
      "work": "Work#d2c6",
      "value": "Value#3c5d"
    },
    "composes_with": {
      "rank": "Rank#7a76"
    }
  }
}
```

---

## ProblemFramer#f504

```json
{
  "handle": "ProblemFramer",
  "mechanism": "A specialized solver role that {{interpret}}s an initial request via {{request_framing}}, constructs the formal {{accept_spec}} (Definition of Done), and anchors the resulting {{root_solver}} to the {{universal_solver_tree}}. Unlike a general Solver (which executes), the Framer's sole output is a well-formed Problem Node ready for decomposition, or a {{reframe}} request if invalid.",
  "gloss": "The active strategist that frames the problem",
  "failure_modes": [
    "Bad Frame: The problem is framed incorrectly, making it unsolvable.",
    "Reframe Failure: Fails to find a valid alternative frame after failure."
  ],
  "invariants": [
    "Genesis: Must create exactly one active Root per problem instance.",
    "Ownership: Owns the high-level success/failure of the task."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_ref": "ProblemFramer#f504",
  "sema_id": "sema:ProblemFramer#mh:SHA-256:f504a75f523cb56db17636e0d9b88bf023e6581745734b0bc72491195ea8b1a5",
  "sema_stub": "f504",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "composes_with": {
      "interpret": "Interpret#c9ee",
      "reframe": "Reframe#0b02",
      "request_framing": "RequestFraming#3865"
    },
    "references": {
      "universal_solver_tree": "UniversalSolverTree#b805",
      "root_solver": "RootSolver#3ad1"
    },
    "yields": {
      "accept_spec": "AcceptSpec#7caa"
    }
  }
}
```

---

## RedTeam#ff27

```json
{
  "handle": "RedTeam",
  "mechanism": "Adversarial Stress Test: Adopt attacker mindset. Goal: break the system, find exploits, identify weaknesses. No loyalty to the design. Document attack vectors with severity and likelihood. Return to defender mode to patch highest-risk vectors. It adopts an attacker persona via {{adversarial_steel}}, probing the system for exploit paths.",
  "gloss": "Adversarial stress testing",
  "failure_modes": [
    "Sympathetic Attacker: The Red Team shares the same assumptions as the designers, missing the same blind spots."
  ],
  "invariants": [
    "Adversarial intent simulated",
    "Goal is to find flaws, not fix them"
  ],
  "preconditions": [
    "Proposed plan/system"
  ],
  "postconditions": [
    "Vulnerability report"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "SteelmanCheck#7914"
    ],
    "ring": 2
  },
  "sema_id": "sema:RedTeam#mh:SHA-256:ff272a47bf273130778bbfdcf20c6b0e4428ecf8aa5403987eb0e55ff2b626b9",
  "sema_ref": "RedTeam#ff27",
  "sema_stub": "ff27",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "adversarial_steel": "AdversarialSteel#3b43"
    }
  }
}
```

---

## Reflex#ea07

```json
{
  "handle": "Reflex",
  "mechanism": "Immediate Automatic Response: Stimulus S triggers response R without deliberation. Reflex arc hardcoded. Response latency minimal. No override possible once triggered. Used for safety-critical reactions. It bypasses the slow reasoning entirely, mapping stimulus directly to a pre-computed response.",
  "gloss": "Hardcoded fast-path responses bypassing deliberation",
  "failure_modes": [
    "Reflex Hijack: Adversary triggers reflex to override deliberate reasoning."
  ],
  "invariants": [
    "Stimulus-response mapping immutable at runtime."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "HeuristicSnap#1ef2"
    ],
    "ring": 2
  },
  "sema_id": "sema:Reflex#mh:SHA-256:ea07e889ca64536b2f0d0657d1583a178ea36fe2fda6c26889c68d46e44a47ce",
  "sema_ref": "Reflex#ea07",
  "sema_stub": "ea07",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba"
}
```

---

## RegretMinimization#4d84

```json
{
  "handle": "RegretMinimization",
  "mechanism": "{{decision}}-making based on minimizing the maximum possible loss (emotional safety/Minimax) rather than maximizing expected value (Utility/Kelly). Useful for survival-critical contexts. It factors {{opportunity_cost}} into the loss function, selecting the path with the least damaging worst-case scenario.",
  "gloss": "Safety-first decision making based on loss avoidance",
  "invariants": [
    "Pessimism: Assume worst-case outcome for each branch",
    "Safety Floor: Never choose option with catastrophic worst-case"
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "PreMortem#142a"
    ],
    "ring": 2
  },
  "sema_id": "sema:RegretMinimization#mh:SHA-256:4d848f39cf28057c41d8949084d1c123f4db115e1fd1e0c3ade7898eac88a877",
  "sema_ref": "RegretMinimization#4d84",
  "sema_stub": "4d84",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "opportunity_cost": "OpportunityCost#b9f4",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## RepresentationSwap#3b45

```json
{
  "handle": "RepresentationSwap",
  "mechanism": "A verification protocol where information is transcoded into a strictly orthogonal modality (e.g., Text -> Flowchart, Code -> Plain English, Table -> Narrative) to reveal structural errors. The agent must successfully map the original concept to the new format. Gaps, ambiguities, or 'impossible geometries' in the new format indicate flaws in the original logic. It forces a lossless transcoding of the concept into an orthogonal format, often using {{concept_blend}} mechanics to map between modalities.",
  "gloss": "Exposing hidden errors by changing the data modality",
  "failure_modes": [
    "Smoothing: The agent unconsciously fixes the errors during translation (hallucinating a coherent flowchart from incoherent text) rather than reporting the failure."
  ],
  "invariants": [
    "Lossless Intent: The core meaning must survive the swap.",
    "Orthogonality: The target modality must constrain different dimensions than the source (e.g., Text is linear; Graphs are topological)."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:RepresentationSwap#mh:SHA-256:3b45e3cb9e6be5cf332fde9255d225a3eecf77564cc052bd7a1145a61cbe7fab",
  "sema_ref": "RepresentationSwap#3b45",
  "sema_stub": "3b45",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "concept_blend": "ConceptBlend#126e"
    }
  }
}
```

---

## Retry#4cc6

```json
{
  "handle": "Retry",
  "mechanism": "Intelligent re-attempt of failed coordination with failure-informed strategy. After BREAK + COMPENSATE, agent evaluates: (1) CLASSIFY failure\u2014transient (timeout, rate-limit, network blip) vs persistent (capability gap, protocol mismatch, explicit rejection). (2) CHECK retry_hint from BREAK (partner may say 'don't retry' or 'wait 30s'). (3) CONSULT failure_history\u2014same error repeating? {{circuit_breaker}} threshold reached? (4) COMPUTE backoff\u2014adaptive based on failure type: transient uses exponential+jitter, persistent uses longer fixed delay or triggers abort. (5) VERIFY changed_conditions\u2014has something changed that makes retry worthwhile? (6) EXECUTE retry if within budget and conditions favor success, else ABORT with retry_exhausted status. Retry CARRIES FORWARD: failure context, partner state observations, environmental data. Retry RESETS: coordination state (fresh start, don't resume mid-stream). It handles transient failures by re-queuing the task, distinguishing them from terminal failures that trigger {{break}} and {{compensate}}.",
  "gloss": "Classified re-attempt with backoff conditioned on failure type",
  "failure_modes": [
    "Misclassifying persistent failure as transient (wastes retry budget).",
    "Misclassifying transient as persistent (gives up too soon).",
    "{{backoff}} too aggressive (slow recovery from transient issues).",
    "{{backoff}} too timid (hammers already-failing system).",
    "{{circuit_breaker}} too sensitive (abandons recoverable situations).",
    "Retry succeeds but same failure recurs (didn't address root cause).",
    "Changed_conditions check misses relevant changes."
  ],
  "invariants": [
    "{{backoff}} applied",
    "Retry count <= Max_Retries"
  ],
  "preconditions": [
    "Transient failure"
  ],
  "postconditions": [
    "Success or definitive failure"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "Backoff#315a"
    ],
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:Retry#mh:SHA-256:4cc646f6a317a5d12411f1f12df2d7212093229e82c2ca69c20fbaf29f1c1d59",
  "sema_ref": "Retry#4cc6",
  "sema_stub": "4cc6",
  "dependencies": {
    "references": {
      "compensate": "Compensate#283e",
      "break": "Break#177f",
      "circuit_breaker": "CircuitBreaker#4162",
      "backoff": "Backoff#315a"
    }
  }
}
```

---

## RigorousSolver#6c5a

```json
{
  "handle": "RigorousSolver",
  "mechanism": "A high-reliability, high-latency implementation of {{polymorphic_solver}} that mandates the full five-surface Solver Contract (Manifest, Execute, Consult, Verify, Feedback) with non-compensatory acceptance gates \u2014 every declared invariant must pass before a Result becomes a Solution; partial success is not permitted to propagate. Uses {{probe}} to verify reality alignment and {{socratic_loop}} to disambiguate intent before action. Incorporates {{feedback}} to improve future reliability. Trades speed for assurance (System 2).",
  "gloss": "High-reliability, high-latency System 2 solver",
  "invariants": [
    "Lifecycle Completeness: Must complete all 5 stages including Verification.",
    "Mandatory Verification: Cannot skip Probe step."
  ],
  "derived_from": "PolymorphicSolver#9188",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 2
  },
  "sema_id": "sema:RigorousSolver#mh:SHA-256:6c5af50fd041a3019e64e63aef35e70351e32a7ff8765d1d5f7c4b82f15a5141",
  "sema_ref": "RigorousSolver#6c5a",
  "sema_stub": "6c5a",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "composes_with": {
      "probe": "Probe#12d8",
      "feedback": "Feedback#b477"
    },
    "references": {
      "socratic_loop": "SocraticLoop#2913",
      "polymorphic_solver": "PolymorphicSolver#9188"
    }
  }
}
```

---

## Roadmap#2e74

```json
{
  "handle": "Roadmap",
  "mechanism": "A strategic {{plan}} defined over a temporal dimension. Unlike a linear {{plan}} which details a single execution path, a Roadmap outlines key {{goal}}s (milestones) and direction over time, often allowing for flexibility in the specific steps between milestones.",
  "gloss": "Strategic plan over time",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Roadmap#mh:SHA-256:2e74475bfaffd9621c78487e66379ff44472070e70056aab9dcdfea4d16879ae",
  "sema_ref": "Roadmap#2e74",
  "sema_stub": "2e74",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d",
      "goal": "Goal#009e"
    }
  }
}
```

---

## RootSolver#3ad1

```json
{
  "handle": "RootSolver",
  "mechanism": "The apex node of a solver {{tree}} \u2014 the unique entry point where a {{problem}} (attached to a {{task}}) enters that tree. Its cognitive operation is triage: determining what kind of problem this is and routing it via a dispatch function conditioned on its {{pathway_memory}}. The RootSolver holds four unique authorities: Problem Framing (initial constraints and {{problem_space}}), Budget Allocation (cascading {{budget}} to child {{solver_node}}s), Ultimate Accountability (owning the final {{result}} or {{solution}}), and Pathway Memory maintenance (compounding learning about which routes work for which problem types). Every tree has exactly one RootSolver; sub-trees carry their own.",
  "gloss": "Apex triage node of a SolverTree, with Pathway Memory as its compounding learning site",
  "failure_modes": [
    "Bad Frame: problem framed incorrectly, unsolvable by downstream nodes.",
    "Reframe Failure: Root fails to find a valid alternative frame after downstream failure.",
    "Budget Misallocation: resources distributed poorly across child nodes.",
    "Poisoned Pathway Memory silently biases routing decisions \u2014 mitigated by signed writes only."
  ],
  "invariants": [
    "Singleton per tree: every SolverTree has exactly one RootSolver.",
    "Ultimate Responsibility: the RootSolver owns the final success/failure of the root {{task}}.",
    "Reframe Authority: only the RootSolver can reframe the original {{problem}}.",
    "Pathway Memory writes are signed \u2014 integrity of the compounding surface is enforced."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "supersedes": [
      "sema:SolverRoot#mh:SHA-256:d31bfa55e755ef10526cf18631128ba7fa9f77afbc6417a07bb5c0700f7a671f"
    ]
  },
  "data_schema": {
    "type": "object",
    "required": [
      "task_ref",
      "problem_frame"
    ],
    "properties": {
      "task_ref": {
        "type": "string",
        "description": "Reference to originating task"
      },
      "problem_frame": {
        "type": "object",
        "description": "Initial problem constraints and space"
      },
      "budget_allocation": {
        "type": "object",
        "description": "Resource distribution to children"
      },
      "pathway_memory_ref": {
        "type": "string",
        "description": "Reference to this Root's PathwayMemory"
      },
      "children": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Child solver node refs"
      }
    }
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:RootSolver#mh:SHA-256:3ad183ba1595645714f4110901b66490a1b549d644955ee36657c67ce2ab61b4",
  "sema_ref": "RootSolver#3ad1",
  "sema_stub": "3ad1",
  "dependencies": {
    "composes_with": {
      "pathway_memory": "PathwayMemory#0799"
    },
    "references": {
      "task": "Task#b328",
      "solution": "Solution#fcea",
      "budget": "Budget#7270",
      "problem_space": "ProblemSpace#9e74",
      "solver_node": "SolverNode#26b1",
      "problem": "Problem#4576",
      "tree": "Tree#a5a3",
      "result": "Result#195b"
    }
  }
}
```

---

## SacrificialProbe#0d39

```json
{
  "handle": "SacrificialProbe",
  "mechanism": "A Generalized Pattern where an {{agent}} sends a low-cost 'probe' into a {{system}} expecting it to fail, but designs the failure to be instructive. The probe must be cheap relative to the main payload, and the failure {{mode}} must update the {{strategy}} for the main payload. Common in startups (landing pages), immunology (dendritic cells), and warfare (reconnaissance). It wraps the concept of a staked probe in a higher-order strategy where the probe's destruction is the intended {{signal}}.",
  "gloss": "Learning via cheap, instructive failure",
  "failure_modes": [
    "{{probe}} is too expensive; {{probe}} failure is silent."
  ],
  "invariants": [
    "Cost Asymmetry: Cost({{probe}}) << Cost(MainPayload)",
    "Instructive Failure: InfoGain(Failure) > EntropyReductionThreshold",
    "{{strategy}} Update: MainPayload parameters are a function of ProbeResult"
  ],
  "preconditions": [
    "{{system}} failure {{mode}}s are observable"
  ],
  "postconditions": [
    "{{strategy}} updated"
  ],
  "parameters": [
    {
      "name": "cost_ratio",
      "type": "Float",
      "range": "[0.0, 0.1]",
      "description": "Probe cost relative to payload"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:SacrificialProbe#mh:SHA-256:0d39580d657811563df7c3b0254cad62ce4e3c9379bacc0be204b0dd977eba18",
  "sema_ref": "SacrificialProbe#0d39",
  "sema_stub": "0d39",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "probe": "Probe#12d8",
      "mode": "Mode#0e74",
      "system": "System#e314",
      "signal": "Signal#f39d",
      "agent": "Agent#35b9",
      "strategy": "Strategy#c4ba"
    }
  }
}
```

---

## Satisfice#9859

```json
{
  "handle": "Satisfice",
  "mechanism": "Threshold Acceptance: Define minimum acceptable criteria upfront. Evaluate options sequentially. Accept first option meeting all thresholds. Stop searching. Optimality is sacrificed for speed and cognitive efficiency. It implements a relaxed version of {{optimal_stop}}, terminating the search as soon as the first valid candidate is found.",
  "gloss": "Optimizing for speed via threshold acceptance",
  "failure_modes": [
    "Threshold Drift: Unconsciously lowering standards during the search to force a match."
  ],
  "invariants": [
    "Threshold cannot change mid-search."
  ],
  "preconditions": [
    "{{option}} space enumerable. Acceptance threshold defined. Evaluation function exists."
  ],
  "postconditions": [
    "{{option}} meeting threshold found OR space exhausted. No backtracking occurred. {{decision}} final."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:Satisfice#mh:SHA-256:98593020b0bee9478d19f3348ae7ecc588ac50ff6ebdc9be3f05d5cb07d96031",
  "sema_ref": "Satisfice#9859",
  "sema_stub": "9859",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "option": "Option#483e",
      "decision": "Decision#acfb",
      "optimal_stop": "OptimalStop#c244"
    }
  }
}
```

---

## Silence#dd79

```json
{
  "handle": "Silence",
  "mechanism": "Active Waiting. The agent deliberately withholds {{signal}} output for duration T or until Trigger. Distinguishes 'Processing...' from 'Abstaining'.",
  "gloss": "Active withholding of signal",
  "invariants": [
    "Timeout: Silence > MaxDuration implies Failure or Default Action."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:Silence#mh:SHA-256:dd793ba60c09b5f61e3de738047e725509758d63311879876b400ff563619ea5",
  "sema_ref": "Silence#dd79",
  "sema_stub": "dd79",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Simulation#aa24

```json
{
  "handle": "Simulation",
  "mechanism": "Sandboxed Execution. Forks the current World {{state}} (W) into W'. Executes Action (A) in W'. Discards W' and returns {{outcome}} (O). W remains immutable.",
  "gloss": "A virtualized execution",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:Simulation#mh:SHA-256:aa24cc6231556ca3cf7d58aad0a8c1ffeb99e08e9ab6c4903b1c93871c926645",
  "sema_ref": "Simulation#aa24",
  "sema_stub": "aa24",
  "invariants": [
    "Isolation: Side effects in W' DO NOT leak to W."
  ],
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "outcome": "Outcome#144c"
    }
  }
}
```

---

## Solver#94ab

```json
{
  "handle": "Solver",
  "mechanism": "The abstract {{protocol}} exposing the five-surface Solver Contract \u2014 Manifest (what can you do?), Execute (perform the {{task}}), Consult (cost/quality/rationale), Verify (post-execution assurance), and Feedback (emits a typed {{performance_signal}} \u2014 structured evaluation, or a FrameError escalation). Manifest and Execute are mandatory; Consult/Verify/Feedback are optional but strongly recommended at hard seams. Accepts a typed Task and yields a typed {{solution}}. Solver is an interface, not a class: any {{agent}} can take on the role of a Solver for the duration of a Task. The \"[descriptor]Solver\" naming convention is the library's construction pattern \u2014 DiagnosticSolver, PlanningSolver, ReduceSolver, PUREOptimizationSolver, and so on are all minted by appending \"Solver\" to a domain descriptor, each specialising the contract. The same agent can wear many solver roles simultaneously or sequentially; lightweight roles (Manifest + Execute only) scale up to permanent instances as tasks compound. Recursion follows naturally: when a Solver decomposes its Task, it becomes the root of a sub-tree whose children are themselves Solvers \u2014 the mechanism that gives the UniversalSolverTree its fractal shape.",
  "gloss": "Abstract five-surface contract: Manifest, Execute, Consult, Verify, Feedback",
  "signature": [
    "Protocol#7e1c(Task#b328)"
  ],
  "_meta": {
    "layer": "Mind",
    "ring": 0,
    "category": "Strategy",
    "tier": 0
  },
  "sema_id": "sema:Solver#mh:SHA-256:94ab9ed2ef37d28c9bd267a6c7e80ef416b1f4e298e9b19b1a4c3ec5f5153311",
  "sema_ref": "Solver#94ab",
  "sema_stub": "94ab",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "performance_signal": "PerformanceSignal#d96f",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#35b9"
    },
    "accepts": {
      "task": "Task#b328"
    },
    "yields": {
      "solution": "Solution#fcea"
    }
  }
}
```

---

## SteelmanFirst#6f15

```json
{
  "handle": "SteelmanFirst",
  "mechanism": "Reasoning Heuristic. Before proposing a solution, the agent actively constructs the strongest possible version of the opposing argument or constraint. It ensures the critique phase of {{steelman_check}} is populated with high-quality data, not strawmen. Utilizes {{steelman_check}}.",
  "gloss": "Ordering rule: steelman opposing view before proposing, so SteelmanCheck has real targets",
  "failure_modes": [
    "Performative Steelman: {{agent}} lists weak counter-arguments to appear unbiased.",
    "{{cognitive_bias}} Leakage: {{agent}} frames the counter-argument in a way that makes it easy to defeat."
  ],
  "invariants": [
    "Prioritization: Counter-argument generation must precede Proposal generation in the chain."
  ],
  "preconditions": [
    "{{problem}} statement defined"
  ],
  "postconditions": [
    "Strongest counter-argument cached"
  ],
  "parameters": [
    {
      "name": "effort_ratio",
      "type": "Float",
      "range": "[0.3, 0.5]",
      "description": "Portion of budget spent on counter-argument"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:SteelmanFirst#mh:SHA-256:6f1589b3aedbf3811ab88b094c72c9fa17a7fd7e026a9cfd569ef4df0e818f4f",
  "sema_ref": "SteelmanFirst#6f15",
  "sema_stub": "6f15",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "steelman_check": "SteelmanCheck#7914",
      "problem": "Problem#4576",
      "agent": "Agent#35b9",
      "cognitive_bias": "CognitiveBias#4b32"
    }
  }
}
```

---

## Strategy#c4ba

```json
{
  "handle": "Strategy",
  "mechanism": "A high-level plan to achieve one or more goals under conditions of uncertainty. Unlike a fixed {{plan}}, a Strategy is adaptive and focuses on 'How to win' rather than just 'What steps to take'.",
  "gloss": "Adaptive high-level planning",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "related": [
      "OODA#eaf1"
    ],
    "ring": 1
  },
  "sema_id": "sema:Strategy#mh:SHA-256:c4ba60dd3a1008c849d03f2cbebbd91ed92bf4a3bb496fbf08a86e152888f8a1",
  "sema_ref": "Strategy#c4ba",
  "sema_stub": "c4ba",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "plan": "Plan#fd6d"
    }
  }
}
```

---

## SunkCostIgnore#ef84

```json
{
  "handle": "SunkCostIgnore",
  "mechanism": "Fresh Slate Evaluation: When deciding whether to continue, ask: \"If I were starting fresh today with current resources, would I begin this project?\" Past investment is irrelevant to future value. Only future costs and benefits matter. Kill zombies early. Utilizes {{opportunity_cost}}.",
  "gloss": "Rationality over historical investment",
  "failure_modes": [
    "Loss Aversion {{loop}}: The agent re-frames stopping as a loss rather than a saving, preventing the fresh slate evaluation."
  ],
  "invariants": [
    "{{decision}} based ONLY on future utility",
    "Past investment excluded from calc"
  ],
  "preconditions": [
    "{{decision}} point",
    "History of investment"
  ],
  "postconditions": [
    "Rational choice made"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:SunkCostIgnore#mh:SHA-256:ef847382634e0fa670e6c242820e233e3f8e77921a459cfe352de1fbcf30e253",
  "sema_ref": "SunkCostIgnore#ef84",
  "sema_stub": "ef84",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "opportunity_cost": "OpportunityCost#b9f4",
      "loop": "Loop#797f",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## TensionHold#2418

```json
{
  "handle": "TensionHold",
  "mechanism": "Cognitive Suspension protocol. When two high-confidence inputs conflict (A \u22a5 B), the {{agent}} instantiates a {{tension}} object that binds them together. This blocks downstream decision-making until a reconciling insight (Pattern C) is found via {{dialectic}} or {{synthesis}}, or until the hold timeout expires.",
  "gloss": "Maintain contradictions without premature resolution",
  "failure_modes": [
    "Premature Convergence: {{agent}} resolves {{tension}} by arbitrarily discarding one side to reduce cognitive load.",
    "Tension Blindness: {{agent}} treats a contradiction as a simple error/hallucination and ignores it.",
    "Analysis Paralysis: Accumulating {{tension}} objects without ever triggering {{dialectic}} resolution.",
    "Timeout Waste: Hold expires without resolution, forcing fallback when more time would have yielded insight."
  ],
  "invariants": [
    "No Selection: Output cannot be simply 'A' or 'B' (must be {{tension}}{A,B}).",
    "Persistence: {{tension}} object remains active until explicitly resolved via {{synthesis}}, Falsification, or timeout expiry."
  ],
  "preconditions": [
    "Mutually exclusive valid inputs identified",
    "Resolution threshold not met"
  ],
  "postconditions": [
    "Execution flow diverted to Information Retrieval (to break the tie)",
    "{{tension}} object created in Graph"
  ],
  "parameters": [
    {
      "name": "timeout",
      "type": "Duration",
      "range": "[5m, 48h]",
      "description": "Maximum hold duration before fallback to Yield, Compromise, or Escalation"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_ref": "TensionHold#2418",
  "sema_id": "sema:TensionHold#mh:SHA-256:2418fbc56588c43202c3f4db394a4163e244e4316f066e1e5a1bb451c8fa4912",
  "sema_stub": "2418",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "dialectic": "Dialectic#5cc3",
      "synthesis": "Synthesis#26b9",
      "agent": "Agent#35b9"
    },
    "yields": {
      "tension": "Tension#c39e"
    }
  }
}
```

---

## ThinSlice#bc19

```json
{
  "handle": "ThinSlice",
  "mechanism": "Sampling a tiny fraction of data (e.g., first 512 bytes) to make a high-confidence classification. Used for triage and routing where full processing is too expensive. Utilizes {{route}}, {{extended_thinking}}, {{somatic_marker}}.",
  "gloss": "High-confidence classification from minimal data",
  "invariants": [
    "Fail-Safe: If classification low confidence, forward to full processor",
    "Sample Limit: Input size <= Slice Size",
    "Representative Sample: The slice must statistically resemble the whole for the target feature"
  ],
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:ThinSlice#mh:SHA-256:bc195be4a2e6a2cef9fcdfae75347ae391abd0894f250d3f08a13a1797257223",
  "sema_ref": "ThinSlice#bc19",
  "sema_stub": "bc19",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "somatic_marker": "SomaticMarker#53bb",
      "route": "Route#b972",
      "extended_thinking": "ExtendedThinking#a49a"
    }
  }
}
```

---

## TimeboxThink#043d

```json
{
  "handle": "TimeboxThink",
  "mechanism": "Bounded Exploration: Set hard time limit before starting. When limit hits, stop regardless of completion. Assess: What did I learn? Is more time justified? Prevents rabbit holes. Forces prioritization of highest-{{value}} {{work}} within {{constraint}}. Utilizes {{budget}}.",
  "gloss": "Temporal bounding of exploration",
  "failure_modes": [
    "Premature Cutoff: Stopping the process just before the breakthrough occurs."
  ],
  "invariants": [
    "Best-so-far answer returned",
    "Execution halts at T_max"
  ],
  "preconditions": [
    "Open-ended task",
    "Time budget"
  ],
  "postconditions": [
    "Result within deadline"
  ],
  "parameters": [
    {
      "name": "checkpoint_interval",
      "type": "Duration",
      "range": "[100ms, 5min]",
      "description": "Save partial results frequency"
    },
    {
      "name": "max_duration",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Hard cutoff for thinking"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:TimeboxThink#mh:SHA-256:043d1bce17ccfc84c9942fc1d4d6d374613aece1f5d21f07be766dad3ad6df74",
  "sema_ref": "TimeboxThink#043d",
  "sema_stub": "043d",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "budget": "Budget#7270",
      "value": "Value#3c5d",
      "work": "Work#d2c6"
    }
  }
}
```

---

## TradeOff#769c

```json
{
  "handle": "TradeOff",
  "mechanism": "The specific negative consequence accepted in exchange for a positive one. The cost of a {{decision}}. There are no solutions, only trade-offs.",
  "gloss": "Exchange of consequences",
  "invariants": [
    "Opportunity Cost: Selecting X implies rejecting Y.",
    "Explicit Recognition: The cost is acknowledged, not ignored."
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "sema_id": "sema:TradeOff#mh:SHA-256:769c61729ff84c1f887e3e075f3a94948094da3ecde8bd9ca9f5034717b1e0d0",
  "sema_ref": "TradeOff#769c",
  "sema_stub": "769c",
  "dependencies": {
    "references": {
      "decision": "Decision#acfb"
    }
  }
}
```

---

## UncertaintyMap#516d

```json
{
  "handle": "UncertaintyMap",
  "mechanism": "Known-Unknown Matrix: Categorize all relevant factors into: Known-Known (facts), Known-Unknown (questions), Unknown-Unknown (blind spots). For each Known-Unknown, estimate cost to resolve. {{prioritize}} high-impact uncertainties. Actively {{probe}} for Unknown-Unknowns. Utilizes {{prioritize}}, {{confidence_calibrate}}.",
  "gloss": "Systematic categorization of ignorance",
  "failure_modes": [
    "False Precision: Treating a Known-Unknown (risk) as a Known-Known (fact) with a wide error bar."
  ],
  "invariants": [
    "Every factor must be categorized exactly once."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:UncertaintyMap#mh:SHA-256:516d5d7d6a0d8a32aaa5ce16208f1e330fec2d7b6029ab985150b154408f8fa0",
  "sema_ref": "UncertaintyMap#516d",
  "sema_stub": "516d",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "probe": "Probe#12d8",
      "prioritize": "Prioritize#68f8",
      "confidence_calibrate": "ConfidenceCalibrate#ba8b"
    }
  }
}
```

---

## WorldReversible#f664

```json
{
  "handle": "WorldReversible",
  "mechanism": "A safety constraint where the agent must design the system such that every action can be perfectly inverted at low cost. This forces the use of immutable logs, versioning, and 'soft deletes' instead of destructive updates.",
  "gloss": "Designing for zero-cost undo",
  "failure_modes": [
    "Storage explosion (keeping all history)."
  ],
  "invariants": [
    "Lossless Undo: {{state}}(T) can be fully restored from {{state}}(T+1)",
    "Low Friction: Cost(Undo) ~ Cost(Do)"
  ],
  "preconditions": [
    "Storage is sufficient for history"
  ],
  "postconditions": [
    "Irreversible actions wrapped in 'Commit' gates"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_id": "sema:WorldReversible#mh:SHA-256:f6649f97dc12bc980722caa393140b9043af7dd470fdac4e1f40fa3f6a22dfbe",
  "sema_ref": "WorldReversible#f664",
  "sema_stub": "f664",
  "sema_layer": "Mind",
  "sema_category": "Strategy#c4ba",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

# Layer: Physics

## Attractor#487f

```json
{
  "handle": "Attractor",
  "mechanism": "A region of a dynamical system's state space that trajectories converge toward from a surrounding basin of initial conditions. Once a trajectory enters the basin of attraction, the system's dynamics pull it toward the attractor and confine it thereafter (absent external perturbation). Attractors may be point-like (fixed points \u2014 a stable {{equilibrium}}), periodic (limit cycles), or strange (chaotic \u2014 bounded but non-repeating). Substrate property: every dissipative dynamical system has attractors; the structure of attractors and their basins is what the system's dynamics is. Downstream patterns use attractor-and-basin reasoning to predict where coordination processes will settle and which initial conditions route to which outcome.",
  "gloss": "A state-space region dynamics pull toward \u2014 fixed points, limit cycles, or chaotic attractors",
  "invariants": [
    "Convergence: trajectories starting in the basin of attraction approach the attractor in the limit.",
    "Confinement: trajectories that enter the attractor remain within it absent external perturbation.",
    "Basin: each attractor has an associated basin of attraction; disjoint attractors partition the set of initial conditions whose trajectories converge."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Attractor#mh:SHA-256:487f2045fc607c43b7168549c6a8cf0eb02d269be82e5625beb6e5d5dc69169d",
  "sema_ref": "Attractor#487f",
  "sema_stub": "487f",
  "dependencies": {
    "references": {
      "equilibrium": "Equilibrium#f7c5"
    }
  }
}
```

---

## Causation#d360

```json
{
  "handle": "Causation",
  "mechanism": "A relationship where manipulating one event directly forces another to occur \u2014 a directed edge in the causal graph. The definitional property is intervention-responsiveness: an external change to the cause alters the effect, which distinguishes causation from mere co-movement.",
  "gloss": "Direct force relationship",
  "_meta": {
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Causation#mh:SHA-256:d3603cfbd4bfed0dc29051fe70c256f8962b96d530a7ec200f42359678e4929c",
  "sema_ref": "Causation#d360",
  "sema_stub": "d360"
}
```

---

## Compensate#283e

```json
{
  "handle": "Compensate",
  "mechanism": "Execute inverse actions to undo partial coordination after BREAK. On receiving BREAK, agent retrieves compensation_log (built during forward execution\u2014each action logged its inverse). Execute inverses in REVERSE chronological order (LIFO). For each inverse: attempt execution, if fail retry (inverses must be idempotent), if still fail log and continue or escalate. Report COMPENSATE_RESULT: {completed: [steps undone], failed: [steps that couldn't undo], clean: bool, downstream_confirmed: bool}. Multi-agent coordination: each agent compensates their own scope. BREAK propagates with upstream_agents hint for cross-agent dependencies\u2014downstream agents compensate first, confirm, then upstream proceeds. Compensation cannot introduce NEW coordinated work (only cleanup and notification). Triggered by {{break}}, it reads the {{time_warp_log}} in reverse to execute the idempotent inverse of each prior action.",
  "gloss": "Structured rollback via logged inverses in LIFO order",
  "failure_modes": [
    "Inverse wasn't logged (can't compensate what wasn't tracked).",
    "Inverse isn't truly idempotent (retry corrupts state).",
    "External state changed between action and compensation (assumption invalid).",
    "Compensation creates new failure (cascading compensation).",
    "Time-sensitive compensation (too late to undo, window passed).",
    "Compensation log lost or corrupted.",
    "Downstream agent doesn't confirm (blocks upstream compensation)."
  ],
  "invariants": [
    "Action is semantically opposite to failure",
    "Compensation action value >= loss value"
  ],
  "preconditions": [
    "Compensation mechanism available",
    "Detected failure/loss"
  ],
  "postconditions": [
    "{{system}} utility restored to baseline"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0,
    "related": [
      "Retry#4cc6"
    ],
    "caution": "Compensation must not erase the audit trail of what was rolled back \u2014 log both the forward action and the compensation."
  },
  "sema_id": "sema:Compensate#mh:SHA-256:283e67ca01279958ab5e2792263d71c7ea6a00f7f61d2560444ec1d77c9930f9",
  "sema_ref": "Compensate#283e",
  "sema_stub": "283e",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "time_warp_log": "TimeWarpLog#a0ac",
      "break": "Break#177f",
      "system": "System#e314"
    }
  }
}
```

---

## Compress#0967

```json
{
  "handle": "Compress",
  "mechanism": "Reducing information size while preserving essential meaning.",
  "gloss": "Lossy or lossless reduction",
  "invariants": [
    "Size Reduction: Output size must be strictly less than Input size.",
    "Reconstructability: (For lossless) Inverse(Output) == Input."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Compress#mh:SHA-256:0967b06ee8a76319b59ee923f2302ff5aebac89f396d79b55f2a0f9e1239f621",
  "sema_ref": "Compress#0967",
  "sema_stub": "0967",
  "sema_layer": "Physics",
  "sema_category": "Primitives"
}
```

---

## Conservation#d63a

```json
{
  "handle": "Conservation",
  "mechanism": "An invariant quantity preserved under the transformations of a closed system \u2014 no process within the system creates or destroys the conserved quantity; transformations only redistribute it. Substrate law: energy is conserved in closed physical systems; probability mass is conserved in stochastic systems; in coordination contexts, a token supply or attention budget that is conserved cannot be counterfeited mid-process. The boundary matters: conservation is defined relative to a closure; crossing the boundary violates the invariant within the enclosed system. Conservation is distinct from an authored budget constraint: budgets are engineered ceilings on consumption, while conservation is the substrate property that the sum-over-the-closed-system is invariant under the system's own dynamics.",
  "gloss": "An invariant quantity preserved under a closed system's transformations \u2014 a substrate law",
  "invariants": [
    "Invariance: the conserved quantity's total value is unchanged by any transformation confined to the system.",
    "Closure scope: conservation is defined relative to a boundary; the invariant holds strictly within the enclosed system, not across the boundary.",
    "Redistribution only: transformations can move the quantity between parts of the system, never create or destroy it."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Conservation#mh:SHA-256:d63a32342e8c1338dc7701a65cc30547b898f9e3b2264097c0c2341c59723688",
  "sema_ref": "Conservation#d63a",
  "sema_stub": "d63a"
}
```

---

## Cooldown#b4c2

```json
{
  "handle": "Cooldown",
  "mechanism": "Minimum Interval Enforcement: After action A, enforce minimum delay D before A can repeat. Attempts during cooldown rejected or queued. Cooldown timer starts on action completion. Different actions can have different cooldowns. It acts as the enforcement mechanism for {{throttle}} policies, rejecting requests until the timer expires.",
  "gloss": "Mandatory delay between repeated actions",
  "failure_modes": [
    "Deadlock: Critical action needed during cooldown period, system stuck waiting."
  ],
  "invariants": [
    "Action blocked until T_last + Duration",
    "Timer is monotonic"
  ],
  "preconditions": [
    "Action executed",
    "Rate limit policy"
  ],
  "postconditions": [
    "Ready state restored after delay"
  ],
  "parameters": [
    {
      "name": "duration",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Mandatory wait period"
    },
    {
      "name": "reset_trigger",
      "type": "Enum",
      "range": "{Success, Failure, Any}",
      "description": "What resets the cooldown"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Cooldown#mh:SHA-256:b4c2f95200e8c87085fb9301754bdc55610b9c8d3dcd3a37f003d49a3fdc23f2",
  "sema_ref": "Cooldown#b4c2",
  "sema_stub": "b4c2",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "throttle": "Throttle#2175"
    }
  }
}
```

---

## Dampen#e55e

```json
{
  "handle": "Dampen",
  "mechanism": "The reduction of {{signal}} intensity or {{value}} magnitude in response to resistance or {{noise}}. It acts as a negative feedback loop to prevent oscillation or runaway amplification.",
  "gloss": "Passive attenuation of signal or force",
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_ref": "Dampen#e55e",
  "sema_id": "sema:Dampen#mh:SHA-256:e55e05a34ca81a8edee4863311fd058210c785bfd5c0ac23bb9a189c4430da2a",
  "sema_stub": "e55e",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "signal": "Signal#f39d",
      "noise": "Noise#d631"
    }
  }
}
```

---

## Decay#a1d4

```json
{
  "handle": "Decay",
  "mechanism": "Gradual Attenuation: Without reinforcement, {{value}} V decreases over time. Decay rate R determines half-life. Reinforcement resets or boosts V. Zero threshold triggers {{state}} change or removal.",
  "gloss": "Automatic expiration of stale {{state}}",
  "failure_modes": [
    "Premature Expiry: Valid data decays before it can be used due to miscalibrated half-life."
  ],
  "invariants": [
    "{{value}} never negative."
  ],
  "parameters": [
    {
      "name": "floor_value",
      "type": "Float",
      "range": "[0.0, 0.5]",
      "description": "Minimum value, never decays below"
    },
    {
      "name": "half_life",
      "type": "Duration",
      "range": "[1min, 30d]",
      "description": "Time for value to halve"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Physics",
    "category": "Primitives",
    "related": [
      "StateTransition#9e61"
    ],
    "ring": 0
  },
  "sema_id": "sema:Decay#mh:SHA-256:a1d4b9d5a517a5a8e942a9bedaafdd004b3d7d5bf2e02bd4018af16350bb64f0",
  "sema_ref": "Decay#a1d4",
  "sema_stub": "a1d4",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "state": "State#4d58"
    }
  }
}
```

---

## Distance#3e1e

```json
{
  "handle": "Distance",
  "mechanism": "A function d(x, y) on a space that assigns a non-negative real number to each pair of points, satisfying the metric axioms: (1) non-negativity, d \u2265 0; (2) identity of indiscernibles, d(x, y) = 0 iff x = y; (3) symmetry, d(x, y) = d(y, x); (4) triangle inequality, d(x, z) \u2264 d(x, y) + d(y, z). The substrate of 'how close' in any space \u2014 geographic, vector-embedding, cognitive-similarity, network-hop, graph-theoretic. Every metric space has a distance function; agents cannot redefine what metric-ness requires. Pseudo-metrics (which relax identity of indiscernibles) and quasi-metrics (which relax symmetry) are distinct descendants, not specializations of Distance itself.",
  "gloss": "Metric-axiom function d(x,y) on a space \u2014 substrate for similarity, proximity, and spatial reasoning",
  "invariants": [
    "Non-negativity: d(x, y) \u2265 0 for all x, y in the space.",
    "Identity of indiscernibles: d(x, y) = 0 if and only if x = y.",
    "Symmetry: d(x, y) = d(y, x).",
    "Triangle inequality: d(x, z) \u2264 d(x, y) + d(y, z)."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Distance#mh:SHA-256:3e1eb18a34bdf42f9f9554af0bd80f65121c05bb756b202068e6959c7cec0167",
  "sema_ref": "Distance#3e1e",
  "sema_stub": "3e1e"
}
```

---

## Entropy#a265

```json
{
  "handle": "Entropy",
  "mechanism": "A quantitative measure of disorder, uncertainty, or information content in a {{system}} or {{message}}.",
  "gloss": "Measure of disorder",
  "_meta": {
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0,
    "tier": 1,
    "related": [
      "EntropyPump#961c"
    ]
  },
  "sema_id": "sema:Entropy#mh:SHA-256:a2652f69c57b3c737f3d0d910e6751d61ea2e9007046ac0f75ee336d178c9212",
  "sema_ref": "Entropy#a265",
  "sema_stub": "a265",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "message": "Message#f767",
      "system": "System#e314"
    }
  }
}
```

---

## EntropyPump#c313

```json
{
  "handle": "EntropyPump",
  "mechanism": "A mechanism that prevents system stagnation by injecting {{entropy}} (randomness/noise) into decision-making processes. It acts as a counterbalance to convergence, ensuring that the system explores the solution space rather than getting stuck in local optima. By adding {{noise}}, it forces re-evaluation of settled states.",
  "gloss": "Controlled randomization to escape convergence deadlocks",
  "failure_modes": [
    "Over-injection destabilizing productive equilibria.",
    "Insufficient injection failing to break persistent deadlocks."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1
  },
  "sema_id": "sema:EntropyPump#mh:SHA-256:c313b5e344b36ab0e427d54d84e8fedb41ce69a74153d3980628c756b9f43fd6",
  "sema_ref": "EntropyPump#c313",
  "sema_stub": "c313",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "noise": "Noise#d631",
      "entropy": "Entropy#a265"
    }
  }
}
```

---

## Equilibrium#f7c5

```json
{
  "handle": "Equilibrium",
  "mechanism": "A {{state}} of a dynamical system in which the system's time evolution under its own dynamics is stationary \u2014 once the system occupies the state it remains there absent external perturbation. Every dynamical system has equilibria (possibly empty), and they are classified by their response to perturbation: *stable* (small deviations decay back to the state), *unstable* (small deviations amplify away), *neutral* (deviations neither decay nor grow). Substrate property: equilibria are implied by a system's dynamics, not designed. Higher patterns test for equilibrium as a signal that a process has settled; some coordination protocols explicitly drive toward or away from a chosen equilibrium.",
  "gloss": "A dynamical system's stationary state \u2014 where the dynamics leave it unchanged",
  "invariants": [
    "Stationarity: under its own dynamics, the system's time derivative at an equilibrium state is zero.",
    "Stability class: every equilibrium is classifiable as stable, unstable, or neutral by perturbation response.",
    "Multiplicity: a dynamical system may have zero, one, or many equilibria; occupancy depends on history and the basin the system entered."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Equilibrium#mh:SHA-256:f7c5f4b45ee12a8b04b5543367092b5d91d4772bbb2b4f4891d1aa0e0e732ee3",
  "sema_ref": "Equilibrium#f7c5",
  "sema_stub": "f7c5",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

## Gate#89fd

```json
{
  "handle": "Gate",
  "mechanism": "Evaluates the truth-value of the target {{condition}} and yields a {{decision}}: proceed if the condition holds, halt if not, or debt (proceed with obligation recorded) when configured. Unlike a silent filter, a Gate produces a first-class Decision artifact that downstream systems can route on. If halted, the specific item stops while the broader system continues processing others (Fail-Safe/Filter).",
  "gloss": "Filter payload if the target condition is not met",
  "failure_modes": [
    "Silent Loss: Important data dropped without alerting the operator."
  ],
  "invariants": [
    "Idempotent: Re-evaluating the gate with the same context yields the same result (within validity window).",
    "Non-Blocking: A false condition must not halt the broader system, only the specific item."
  ],
  "parameters": [
    {
      "name": "policy",
      "type": "Enum",
      "range": "unspecified",
      "description": "Behavior on condition failure (reject, queue, redirect)"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Gate#mh:SHA-256:89fdb7df388ddb1e1c81350b391fc6c9a2ad967de069c7d09b591c7d13379264",
  "sema_ref": "Gate#89fd",
  "sema_stub": "89fd",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "yields": {
      "decision": "Decision#acfb"
    },
    "references": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## Gradient#84a5

```json
{
  "handle": "Gradient",
  "mechanism": "The directional rate of change of a scalar field across a metric space. For any sufficiently smooth field f over a metric space, the gradient \u2207f at a point is the vector whose direction is the one of steepest ascent of f and whose magnitude is the rate of increase in that direction. Substrate property: gradients exist wherever fields exist, whether or not anyone measures them. Specific cases include {{entropy}} gradients (the direction of maximum disorder increase), attention gradients, credibility gradients, information-density gradients. Higher patterns use gradients for hill-climbing search, attention allocation, credit assignment, and flow routing.",
  "gloss": "The directional rate of change of a scalar field \u2014 substrate for hill-climbing, attention flow, and credit assignment",
  "invariants": [
    "Existence: every sufficiently smooth field on a metric space has a gradient defined at every interior point.",
    "Direction: \u2207f points in the direction of steepest ascent of f.",
    "Magnitude: |\u2207f| is the rate of change in the direction of steepest ascent."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Gradient#mh:SHA-256:84a514eeeb98582c29b1d6f7d8ecbb8e698815987c0e7f372ba52a81bb8665a3",
  "sema_ref": "Gradient#84a5",
  "sema_stub": "84a5",
  "dependencies": {
    "references": {
      "entropy": "Entropy#a265"
    }
  }
}
```

---

## Hysteresis#d0f8

```json
{
  "handle": "Hysteresis",
  "mechanism": "Asymmetric Thresholds: {{state}} change from A\u2192B requires crossing threshold T_up. {{state}} change from B\u2192A requires crossing lower threshold T_down. Gap between thresholds prevents oscillation near boundary. Thresholds fixed or adaptive. It uses a {{dampen}} effect on state transitions, requiring the signal to cross distinct upper and lower thresholds to switch modes.",
  "gloss": "Preventing oscillation via asymmetric thresholds",
  "failure_modes": [
    "Stuck {{state}}: Gap between thresholds is too wide, system never transitions back."
  ],
  "invariants": [
    "T_up > T_down always."
  ],
  "parameters": [
    {
      "name": "lower_threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Trigger to switch OFF, must be < upper"
    },
    {
      "name": "upper_threshold",
      "type": "Float",
      "range": "unspecified",
      "description": "Trigger to switch ON"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Hysteresis#mh:SHA-256:d0f8e3e90c03f4306ca42f5d69c6a41f3f89334ccfc450873771944f2a5aec46",
  "sema_ref": "Hysteresis#d0f8",
  "sema_stub": "d0f8",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    },
    "composes_with": {
      "dampen": "Dampen#e55e"
    }
  }
}
```

---

## Lock#051c

```json
{
  "handle": "Lock",
  "mechanism": "A synchronization primitive that enforces exclusive access to a resource. At most one holder may access the protected resource at any time. The holder must explicitly release the lock to allow others to acquire it.",
  "gloss": "Mutual exclusion enforcement",
  "failure_modes": [
    "Deadlock: Holder crashes or hangs without releasing, blocking all other contenders indefinitely.",
    "Priority Inversion: High-priority contender blocked by low-priority holder."
  ],
  "invariants": [
    "Exclusivity: At most one holder at any time.",
    "Acquire-before-access: Protected resource cannot be touched without holding the lock.",
    "Release-after-use: Holder must release after completing the critical section."
  ],
  "preconditions": [
    "Shared resource exists",
    "Contending parties can communicate"
  ],
  "postconditions": [
    "Exactly one party holds exclusive access",
    "Other contenders are blocked or queued"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0,
    "caution": "Exclusive access \u2014 starvation enables denial of service."
  },
  "sema_ref": "Lock#051c",
  "sema_id": "sema:Lock#mh:SHA-256:051cd882b7775ef88bb6dde8864de2749543af6813ec01703e8bc3bccd775de4",
  "sema_stub": "051c",
  "sema_layer": "Physics",
  "sema_category": "Primitives"
}
```

---

## Measurement#bf48

```json
{
  "handle": "Measurement",
  "mechanism": "The substrate act of extracting information about a system's {{state}} \u2014 an operation that, in general, *changes the state being measured*. Distinct from the cognitive `Observe` primitive: Measurement is the substrate-level phenomenon, Observe is the agent-level process. In quantum systems, measurement collapses superposition. In distributed systems, observing a clock at node A introduces latency and ambiguity about the clock's value elsewhere. In classical measurement, even reading a variable in a concurrent system can race with writers. The substrate property is that observation is never free \u2014 it takes resources, it takes time, and it perturbs the measured system. The degree of perturbation is domain-dependent (negligible for a thermometer in a large water tank; total for a measurement on a qubit); the substrate fact of perturbation is universal.",
  "gloss": "The substrate act of extracting information from a system \u2014 in general, changes the state being measured",
  "invariants": [
    "Perturbation: measurement, in general, changes the state of the measured system. The degree varies by domain; the fact does not.",
    "Cost: measurement requires resources (time, energy, channel capacity) \u2014 there is no free observation.",
    "Distinct from `Observe`: Measurement is the substrate phenomenon; `Observe` is the cognitive process an agent performs that may use Measurement beneath."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Measurement#mh:SHA-256:bf4844cee68fef7e77a21adcd8219afd0bbfdfcfa25ffa756694e536b4501362",
  "sema_ref": "Measurement#bf48",
  "sema_stub": "bf48",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

## Mutex#52d1

```json
{
  "handle": "Mutex",
  "mechanism": "Exclusive access token. Lifecycle: ACQUIRE {{task}} -> GRANT/QUEUE -> HOLD -> RELEASE/YIELD. Token represents a unique handle ({{resource}}). Sequence increments on transfer. Priority queue prevents starvation. Fencing tokens handle revocation. It manages exclusive access by enforcing a strict queue via delegation or throttling, often isolating the critical section.",
  "gloss": "Physical possession token",
  "failure_modes": [
    "Totem loss (requires regeneration protocol).",
    "Failure modes: (1) Holder crash - token orphaned, mitigated by expires_at + heartbeat.",
    "(2) Token corruption - mitigated by REGENERATE protocol.",
    "(3) Deadlock - mitigated by wait-for graph detection + ordered acquisition.",
    "(4) Starvation - mitigated by aging + anti-starvation rule (no consecutive preemption).",
    "(5) Byzantine holder - mitigated by forcible REVOKE + fencing.",
    "(6) Split brain - mitigated by fencing tokens that invalidate on revocation."
  ],
  "invariants": [
    "Uniqueness, Conservation of Totem"
  ],
  "preconditions": [
    "Resource exists and is lockable. At least 2 agents contending. Agents can communicate."
  ],
  "postconditions": [
    "Exactly one agent holds lock. Other agents blocked or notified. {{lock}} state consistent across all observers."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0,
    "caution": "Exclusive access \u2014 starvation enables denial of service."
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "derived_from": "Lock#051c",
  "sema_id": "sema:Mutex#mh:SHA-256:52d1f02dc13caba01000bf8e1c60073b67a1ff2f8b65fb3a30a56cc3cdd8e8bd",
  "sema_ref": "Mutex#52d1",
  "sema_stub": "52d1",
  "dependencies": {
    "references": {
      "resource": "Resource#a578",
      "lock": "Lock#051c"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## MutualInformation#da31

```json
{
  "handle": "MutualInformation",
  "mechanism": "The substrate information-theoretic measure of shared entropy between two random variables: I(X; Y) = H(X) + H(Y) \u2212 H(X, Y), equivalently the reduction in {{entropy}} of one variable given knowledge of the other. Quantifies how much knowing X reduces uncertainty about Y (and symmetrically). Zero mutual information indicates statistical independence; high mutual information indicates strong coupling without specifying its form (linear, nonlinear, or arbitrary). Substrate property: exists wherever joint distributions exist, whether or not anyone estimates it. Distinct from correlation (which measures linear dependence only) and from mere co-occurrence.",
  "gloss": "Substrate information-theoretic measure of shared entropy between two variables",
  "invariants": [
    "Non-negativity: I(X; Y) \u2265 0 for all random variables X, Y.",
    "Symmetry: I(X; Y) = I(Y; X).",
    "Zero iff independent: I(X; Y) = 0 if and only if X and Y are statistically independent.",
    "Bounded by entropy: I(X; Y) \u2264 min(H(X), H(Y))."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:MutualInformation#mh:SHA-256:da310ac721a0b6945056d317f97ad1337ba537328f01479484cb7d261fbeed05",
  "sema_ref": "MutualInformation#da31",
  "sema_stub": "da31",
  "dependencies": {
    "references": {
      "entropy": "Entropy#a265"
    }
  }
}
```

---

## Noise#d631

```json
{
  "handle": "Noise",
  "mechanism": "Information that is irrelevant or meaningless to the current {{task}}. It obscures the {{datum}} and increases the cognitive load required to extract {{signal}}.",
  "gloss": "Irrelevant information",
  "_meta": {
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Noise#mh:SHA-256:d631b83224591fce5292eafc1172a13574cb3cc80b42aee104eec39a65871f8b",
  "sema_ref": "Noise#d631",
  "sema_stub": "d631",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf",
      "task": "Task#b328",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## PhaseTransition#edf8

```json
{
  "handle": "PhaseTransition",
  "mechanism": "A sudden, qualitative reorganization of a system's {{state}} when a control parameter crosses a threshold. Below the threshold the system occupies one regime (behaviors, structures, or equilibria); above it, a structurally distinct regime. The transition is non-continuous: small changes in the control parameter near the threshold produce disproportionately large changes in system behavior. Substrate phenomenon: appears in thermodynamics (ice-water-vapor), percolation networks (connectivity thresholds), opinion dynamics (cascade onset), coordination systems (consensus formation), neural dynamics (critical states). Not to be confused with authored state transitions in a finite-state machine \u2014 PhaseTransition names the substrate pattern of threshold-triggered structural change in dynamical systems.",
  "gloss": "Sudden, qualitative reorganization of a system when a control parameter crosses a threshold",
  "invariants": [
    "Threshold: the transition is associated with a critical value of a control parameter.",
    "Qualitative change: the regimes above and below the threshold are structurally distinct, not merely quantitatively different.",
    "Non-continuity: the system's macroscopic behavior is not a smooth function of the control parameter at the threshold."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:PhaseTransition#mh:SHA-256:edf83fdf4afccce463a1afeb1c9562009edfc0414141ff15e5410024a5bd116a",
  "sema_ref": "PhaseTransition#edf8",
  "sema_stub": "edf8",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

## ReAttempt#0cd7

```json
{
  "handle": "ReAttempt",
  "mechanism": "The substrate-level primitive of 'try the same call again after a delay.' ReAttempt is the atomic physical-substrate operation: same arguments, same target, after a pause. Distinct from {{retry}}, which is the strategic Mind-layer pattern that classifies failures, consults failure history, computes adaptive {{backoff}}, and decides whether conditions have changed enough to warrant another attempt. Descendants build classification and budget on top of ReAttempt; the primitive imposes no ceiling.",
  "gloss": "Substrate-level re-attempt: same call, after a delay",
  "failure_modes": [
    "Uncapped ReAttempt loops amplify transient failures into DoS against rate-limited downstream resources.",
    "Missing jitter causes thundering herd when many agents ReAttempt simultaneously.",
    "Descendants forget to budget ReAttempt and inherit the primitive's open-ended retry behavior."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0,
    "caution": "Requires an explicit retry budget; uncapped ReAttempt#0cd7 can amplify transient failures into DoS against downstream resources."
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:ReAttempt#mh:SHA-256:0cd7af4c672a70c637eb4d03b01e161f7643f49ab6ef28cea85492e8ddb21578",
  "sema_ref": "ReAttempt#0cd7",
  "sema_stub": "0cd7",
  "dependencies": {
    "references": {
      "retry": "Retry#4cc6",
      "backoff": "Backoff#315a"
    }
  }
}
```

---

## Reversibility#bf79

```json
{
  "handle": "Reversibility",
  "mechanism": "Evaluates whether the post-state of an action allows a return to the pre-state with zero information loss (or within acceptable cost). Returns TRUE for Type 2 decisions (reversible), FALSE for Type 1 (one-way doors).",
  "gloss": "Condition: Can this action be undone?",
  "invariants": [
    "Entropy {{constraint}}: Reversal must not violate thermodynamic limits (e.g., cannot un-burn toast)."
  ],
  "parameters": [
    {
      "name": "cost_limit",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Maximum acceptable cost to reverse the action"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Reversibility#mh:SHA-256:bf796a25a0c91a127c9d336839033d52f198d75080d71e6ae084827f3ae158a7",
  "sema_ref": "Reversibility#bf79",
  "sema_stub": "bf79",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## Route#b972

```json
{
  "handle": "Route",
  "mechanism": "A classifier that examines a {{task}} input and directs it to a specialized downstream handler. Enables separation of concerns\u2014different query types get different prompts, tools, or models. Routes based on type tags, metadata fields, token weight, or configurable dispatch rules (simple queries to small models, complex to large).",
  "gloss": "Classify input and direct to specialized handler",
  "failure_modes": [
    "Misrouting: Input sent to wrong specialist, causing errors.",
    "Ambiguous Classification: Input matches multiple routes or none.",
    "Routing Bottleneck: Classifier becomes slower than just handling directly."
  ],
  "invariants": [
    "Input directed to best-fit handler",
    "No dropped requests"
  ],
  "preconditions": [
    "Input query",
    "Router logic configured"
  ],
  "postconditions": [
    "Query dispatched"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "related": [
      "Select#15c2"
    ],
    "ring": 0,
    "supersedes": [
      "sema:Switch#mh:SHA-256:e7f9f7fba998e74e83165b23f0328643be83117559cd4d1a8711043955f6d6b0"
    ]
  },
  "sema_ref": "Route#b972",
  "sema_id": "sema:Route#mh:SHA-256:b972ff15973013019d24f13ead5662a21255a6ec0ea0f85a5ae425b07b6d0762",
  "sema_stub": "b972",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## Sign#1fb9

```json
{
  "handle": "Sign",
  "mechanism": "The {{act}} of attaching a verifiable {{identity}} proof to an {{artifact}}, asserting authorship, approval, or agreement. Unlike a raw {{signal}}, a Sign action creates a non-repudiable link between the entity and the data. Used to validate contracts or authorize actions.",
  "gloss": "Attest to authorship or agreement",
  "invariants": [
    "Non-Repudiation: The signer cannot later deny having signed it.",
    "Integrity: The signature invalidates if the artifact changes."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1
  },
  "signature": [
    "Act#5d55(Identity#626c)"
  ],
  "sema_id": "sema:Sign#mh:SHA-256:1fb991fd538b93a9e2566b3f2a4c69f67a6b101d0577d911f50a4e194c1dc6ba",
  "sema_ref": "Sign#1fb9",
  "sema_stub": "1fb9",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "identity": "Identity#626c"
    },
    "accepts": {
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "act": "Act#5d55"
    }
  }
}
```

---

## Throttle#2175

```json
{
  "handle": "Throttle",
  "mechanism": "Rate Limiting: Maximum N {{task}}s per time window W. Excess requests rejected, queued, or delayed. Window can be sliding or fixed. Separate limits per action type or global. Utilizes {{backoff}}.",
  "gloss": "Rate-limiting to prevent resource exhaustion",
  "failure_modes": [
    "Legitimate Denial: Throttle cannot distinguish attack traffic from legitimate burst."
  ],
  "invariants": [
    "Queue Bounding: Dropped requests > 0 if InputRate >> MaxRate",
    "Rate Limit: Output events per second <= MaxRate",
    "Rate never exceeds limit within any window."
  ],
  "preconditions": [
    "Token bucket or Leaky bucket state initialized"
  ],
  "parameters": [
    {
      "name": "burst_size",
      "type": "Integer",
      "range": "[1, 100]",
      "description": "Temporary overflow allowance"
    },
    {
      "name": "rate_limit",
      "type": "Integer",
      "range": "[1, 10000]",
      "description": "Max requests per window"
    },
    {
      "name": "window",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Time window for rate calculation"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Throttle#mh:SHA-256:2175da478929fd107d442e1f7ead06551c81108924e7e5b675fb397866879f7a",
  "sema_ref": "Throttle#2175",
  "sema_stub": "2175",
  "dependencies": {
    "accepts": {
      "task": "Task#b328"
    },
    "composes_with": {
      "backoff": "Backoff#315a"
    }
  }
}
```

---

## Branch#329d

```json
{
  "handle": "Branch",
  "mechanism": "Conditional fork: if C then A else B. Mutual exclusion.",
  "gloss": "Conditional flow",
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Time",
    "ring": 0
  },
  "sema_id": "sema:Branch#mh:SHA-256:329d01a4bcf9599389d35db860faee9fb6d42964ceca8fd708843b410fa7150e",
  "sema_ref": "Branch#329d",
  "sema_stub": "329d",
  "sema_layer": "Physics",
  "sema_category": "Time"
}
```

---

## CausalBarrier#3c73

```json
{
  "handle": "CausalBarrier",
  "mechanism": "A middleware layer that buffers incoming messages and releases them to the agent ONLY when all their causal dependencies are met. Guarantees the agent never sees an 'impossible' state. It maintains a {{state_lock}} on the event processing queue, releasing it only when all causal predecessors have been observed.",
  "gloss": "Enforcing strict event ordering",
  "failure_modes": [
    "Buffer overflow if dependencies never arrive."
  ],
  "invariants": [
    "Causal Ordering: Event E cannot be processed until all Dependencies(E) are processed",
    "Events before barrier cannot affect events after.",
    "No Impossible States: {{agent}} state never violates causal consistency"
  ],
  "parameters": [
    {
      "name": "on_violation",
      "type": "Enum",
      "range": "{Block, Warn, Reorder}",
      "description": "Response to causality breach"
    },
    {
      "name": "party_count",
      "type": "Integer",
      "range": "[2, 100]",
      "description": "Required causal predecessors"
    },
    {
      "name": "timeout",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Max wait for causal completion"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Time",
    "ring": 0
  },
  "sema_id": "sema:CausalBarrier#mh:SHA-256:3c73673cdf5f345bc792d80ad924d8cd7caa5c222303e2439d14c6683a9a3ff1",
  "sema_ref": "CausalBarrier#3c73",
  "sema_stub": "3c73",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#8183",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Heartbeat#b67a

```json
{
  "handle": "Heartbeat",
  "mechanism": "Periodic Liveness {{signal}}: An entity emits {{signal}} (Heartbeat) every interval I. Missing K consecutive heartbeats triggers failure detection. Heartbeat may include health metrics. Receiver tracks last-seen timestamp. It feeds into the {{quorum}} detector, allowing the collective to identify and prune dead nodes.",
  "gloss": "Liveness detection via periodic signals",
  "failure_modes": [
    "False failure detection due to network congestion (node alive but heartbeat delayed)."
  ],
  "invariants": [
    "Missing signal implies failure",
    "{{signal}} frequency within tolerance"
  ],
  "preconditions": [
    "Active component",
    "{{monitor}}"
  ],
  "postconditions": [
    "Liveness confirmed"
  ],
  "parameters": [
    {
      "name": "interval",
      "type": "Duration",
      "range": "[100ms, 60s]",
      "description": "Time between heartbeats"
    },
    {
      "name": "timeout_multiplier",
      "type": "Integer",
      "range": "[2, 5]",
      "description": "Missed beats before failure"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Time",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Time",
  "sema_id": "sema:Heartbeat#mh:SHA-256:b67a3ab4833a40c7c960fab4a7a75f920c734ddfe795a223cceb8477e327e0ef",
  "sema_ref": "Heartbeat#b67a",
  "sema_stub": "b67a",
  "dependencies": {
    "accepts": {
      "signal": "Signal#f39d"
    },
    "references": {
      "monitor": "Monitor#feb3"
    },
    "composes_with": {
      "quorum": "Quorum#858e"
    }
  }
}
```

---

## StateAudit#8195

```json
{
  "handle": "StateAudit",
  "mechanism": "A safety pattern where an agent performs an explicit {{audit}} of the {{state}} immediately after a write to ensure the {{state_transition}} occurred as expected. Catches silent API failures.",
  "gloss": "Verifying system state after an operation",
  "sema_id": "sema:StateAudit#mh:SHA-256:81955226e479378fe597ebe9d86b1a7fe788d392f99ae29c85a81f9ac091dc96",
  "sema_ref": "StateAudit#8195",
  "sema_stub": "8195",
  "_meta": {
    "layer": "Physics",
    "category": "Time",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "audit": "Audit#6888",
      "state": "State#4d58",
      "state_transition": "StateTransition#9e61"
    }
  }
}
```

---

## StateLock#8183

```json
{
  "handle": "StateLock",
  "mechanism": "A coordination pattern where two {{actor}}s temporarily 'fuse' a subset of their writable {{state}}. During the {{lock}}, changes require a cryptographic signature from both. Contention triggers {{backoff}} and {{cooldown}}.",
  "gloss": "Atomic coordination via temporary state fusion",
  "failure_modes": [
    "Deadlock: both parties wait for each other indefinitely.",
    "Livelock: lock acquired and released rapidly, denying access to others.",
    "Premature dissolution: state auto-dissolves while legitimate work is in progress."
  ],
  "_meta": {
    "layer": "Physics",
    "category": "Time",
    "ring": 0,
    "tier": 1,
    "caution": "Exclusive state access \u2014 misuse enables denial of service via lock starvation."
  },
  "signature": [
    "Lock#051c(State#4d58)"
  ],
  "sema_ref": "StateLock#8183",
  "sema_id": "sema:StateLock#mh:SHA-256:81839e5a923aff3df2bb3f806fec00c512b6faeb5999f6c390a2c5a6f00a56d2",
  "sema_stub": "8183",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "cooldown": "Cooldown#b4c2",
      "actor": "Actor#6926",
      "lock": "Lock#051c",
      "backoff": "Backoff#315a"
    }
  }
}
```

---

# Layer: Society

## Compromise#90ee

```json
{
  "handle": "Compromise",
  "mechanism": "Iterative Negotiation Protocol. Each {{agent}} states preferences with INTENSITY scores (0-1). The {{system}} computes DISSONANCE (Sum(Intensity_A * Intensity_B)). To reach consensus, agents must {{dampen}} their preference intensity until Dissonance < Threshold. Unlike {{yield}} (which is binary surrender), Compromise is a continuous reduction of demand.",
  "gloss": "Finding a mutual sacrifice zone via intensity reduction",
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_ref": "Compromise#90ee",
  "sema_id": "sema:Compromise#mh:SHA-256:90ee2422aa0bd1d5a1188e904e60c8a814c96125e1dcee8bd95e7ef2b01be97a",
  "sema_stub": "90ee",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "yield": "Yield#2931",
      "agent": "Agent#35b9",
      "system": "System#e314"
    },
    "composes_with": {
      "dampen": "Dampen#e55e"
    }
  }
}
```

---

## Consensus#ffff

```json
{
  "handle": "Consensus",
  "mechanism": "A distributed protocol allowing a set of agents to agree on a single data value or state transition. It orchestrates {{vote}} exchange and uses {{quorum}} to validate the result. It ensures safety and liveness in an adversarial network, accepting a {{proposal}} and yielding a {{value}}.",
  "gloss": "Distributed agreement process",
  "failure_modes": [
    "Split Brain: Network partition causes two subgroups to reach different {{value}}s.",
    "Liveness Failure: The system stalls and never reaches agreement on the {{proposal}}.",
    "Sybil Attack: One malicious actor creates multiple identities to sway the {{vote}}.",
    "Byzantine Failure: Agents lying or acting maliciously to prevent consensus."
  ],
  "invariants": [
    "Agreement: All correct agents who decide must decide the same {{value}}.",
    "Validity: If all agents propose V, then the {{value}} must be V.",
    "Termination: Eventually, every correct agent decides on a {{value}}."
  ],
  "preconditions": [
    "Group of agents is defined (Membership List)",
    "Communication channel is available",
    "{{proposal}} received"
  ],
  "postconditions": [
    "A single {{value}} is committed to the shared state",
    "All agents are notified of the {{value}}"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Coordination",
    "ring": 0,
    "related": [
      "Sync"
    ],
    "caution": "Governance decisions susceptible to coordinated voting blocs."
  },
  "sema_id": "sema:Consensus#mh:SHA-256:ffff8fe79630eb9df5d09f49aa1e34fbb20d98db198cbd07b29d4be368fd4c10",
  "sema_ref": "Consensus#ffff",
  "sema_stub": "ffff",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "yields": {
      "value": "Value#3c5d"
    },
    "composes_with": {
      "quorum": "Quorum#858e",
      "vote": "Vote#ab74"
    },
    "accepts": {
      "proposal": "Proposal#4840"
    }
  }
}
```

---

## ConsensusFinder#1c01

```json
{
  "handle": "ConsensusFinder",
  "mechanism": "Macro for {{discover}}({{consensus}}). Instead of initiating a vote, the agent scans the network to identify pre-existing clusters of agreement or shared state. It optimizes coordination by surfacing natural alignment before attempting to manufacture it. It applies the {{discover}} primitive to locate {{consensus}} clusters, checking for {{resonate}} signals before triggering a formal {{quorum}}.",
  "gloss": "Discovering existing agreement",
  "invariants": [
    "Passive Observation: Does not initiate new voting rounds.",
    "Discovery: Returns existing consensus or Null."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_id": "sema:ConsensusFinder#mh:SHA-256:1c012e6f35c758a5cc63778e30124b372c2f5bb91ad0513056b8e2a6c1c5b4ca",
  "sema_ref": "ConsensusFinder#1c01",
  "sema_stub": "1c01",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "signature": [
    "Discover#7dbc(Consensus#ffff)"
  ],
  "dependencies": {
    "references": {
      "discover": "Discover#7dbc",
      "consensus": "Consensus#ffff",
      "resonate": "Resonate#9fa4",
      "quorum": "Quorum#858e"
    }
  }
}
```

---

## Delegate#a551

```json
{
  "handle": "Delegate",
  "mechanism": "{{work}} distribution protocol with acceptance, tracking, and failure handling. Delegator sends 'DELEGATE' message. Delegatee responds 'ACCEPT' or 'REFUSE'. On accept, delegatee owns {{task}} and sends 'PROGRESS' via {{heartbeat}}. On completion, delegator receives result. On failure, delegatee sends {{break}}\u2014delegator decides: reassign, retry, or escalate. Broadcast delegation creates auction. It employs {{probe}} to verify capabilities. Inherits {{holographic_shard}}.",
  "gloss": "Work handoff: delegate \u2192 accept/refuse \u2192 heartbeat \u2192 result-or-failure",
  "failure_modes": [
    "No one accepts (all refuse or auction has no takers\u2014task orphaned).",
    "Capability mismatch (assigned to incapable agent\u2014fails late).",
    "Delegatee disappears (no progress updates\u2014need timeout).",
    "Circular delegation (A\u2192B\u2192A\u2014detect and reject).",
    "Overload (one agent accepts everything\u2014need load awareness).",
    "Progress lies (reports complete when not\u2014need verification).",
    "Dependency deadlock (A waits for B waits for A)."
  ],
  "invariants": [
    "Delegation is REQUEST not command (acceptance protocol unless pre-waived at RALLY). Refused tasks must be handled (reassign or escalate, not silently dropped). Progress must be trackable (delegatee reports status updates). Failure propagates (delegated task failure triggers {{break}} to delegator). Dependencies enforced (task blocked until dependencies complete). One owner per task (no ambiguous responsibility)."
  ],
  "preconditions": [
    "Principal has authority. Delegate capable. Scope of delegation defined."
  ],
  "postconditions": [
    "Delegate acts within scope. Principal notified of actions. Revocation possible."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "related": [
      "Handoff#5a39"
    ],
    "ring": 1
  },
  "sema_id": "sema:Delegate#mh:SHA-256:a55127efdb0c80f0ee1fde9ecc83ed5f64cdbb992e30e53384ef9e66f4f1a153",
  "sema_ref": "Delegate#a551",
  "sema_stub": "a551",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "accepts": {
      "holographic_shard": "HolographicShard#c137"
    },
    "references": {
      "break": "Break#177f",
      "work": "Work#d2c6"
    },
    "yields": {
      "task": "Task#b328"
    },
    "composes_with": {
      "heartbeat": "Heartbeat#b67a",
      "probe": "Probe#12d8"
    }
  }
}
```

---

## Disband#9cc9

```json
{
  "handle": "Disband",
  "mechanism": "Graceful group dissolution with state disposition and clean termination. {{agent}} sends 'DISBAND' signal. For scope='member': notify remaining members, adjust shared state, check {{quorum}}. For scope='group': broadcast 'DISSOLVING', execute state disposition, release shared resources, and record dissolution with a group {{snapshot}} for potential re-formation. All members must ACK dissolution. It safely terminates the group, optionally triggering {{ejection_seat}} for any members refusing to release shared resources.",
  "gloss": "Graceful group dissolution with state disposition and resource release",
  "failure_modes": [
    "Member doesn't ACK (dissolution blocked\u2014timeout or proceed anyway?).",
    "{{state}} disposition fails (can't archive, transfer target unavailable).",
    "Contested dissolution (some members want to continue\u2014may need VOTE).",
    "Premature dissolution (task not actually complete).",
    "Zombie group (DISBAND sent but not all resources actually released).",
    "Partial dissolution cascades unexpectedly (one departure triggers full dissolution via quorum loss)."
  ],
  "invariants": [
    "All shared resources released",
    "No lingering commitments"
  ],
  "preconditions": [
    "Active group/swarm",
    "Mission complete or aborted"
  ],
  "postconditions": [
    "Agents return to free pool"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_id": "sema:Disband#mh:SHA-256:9cc9935e3e3e1a470d5717467b0a91c50df2b15fe04dc5309585771509fc5a9e",
  "sema_ref": "Disband#9cc9",
  "sema_stub": "9cc9",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "quorum": "Quorum#858e",
      "agent": "Agent#35b9",
      "ejection_seat": "EjectionSeat#d53e"
    },
    "yields": {
      "snapshot": "Snapshot#0ae9"
    }
  }
}
```

---

## Elect#253d

```json
{
  "handle": "Elect",
  "mechanism": "Establish leadership role with nomination, powers, term, and succession. Phase 1 NOMINATE: Members send NOMINATE: {nominee, nominator, reason}. Self-nomination allowed if configured. Nominees must satisfy {{accept_spec}} to appear on {{ballot}}\u2014cannot elect unwilling leader. Phase 2 VOTE: Standard VOTE mechanism among accepted nominees. Phase 3 INVEST: Winner receives {{solution}} (Election Result): {elected, powers[] (explicitly granted authorities), term (fixed|task|indefinite|renewable), succession_plan (automatic|re_elect|fallback)}. Leader exercises granted powers until term ends, resignation, or recall. On term end: succession triggers per plan. RECALL mechanism if enabled: member initiates RECALL_MOTION: {reason}, group VOTEs, if threshold met leader removed and succession triggers.",
  "gloss": "Leader nomination \u2192 vote \u2192 succession with term and authority bounds",
  "failure_modes": [
    "No candidates (no one willing to lead\u2014group operates leaderless or incentivize).",
    "Election deadlock (no majority\u2014use runoff or plurality fallback).",
    "Leader abuse (exceeds granted powers\u2014recall or DISBAND).",
    "Succession failure (successor also unavailable\u2014chain or re-elect).",
    "Recall wars (constant removal attempts\u2014raise threshold or cooldown).",
    "Power creep (leader accumulates ungrantled powers\u2014audit against ELECT_RESULT)."
  ],
  "invariants": [
    "One and only one leader selected per term",
    "Selection process is verifiable"
  ],
  "preconditions": [
    "Candidate set",
    "Voting mechanism"
  ],
  "postconditions": [
    "Leader identified",
    "Term started"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Coordination",
    "related": [
      "Vote#ab74"
    ],
    "ring": 2
  },
  "sema_id": "sema:Elect#mh:SHA-256:253d0f3830c2802cfdc4024a1b340230a57a956f65185349c9b5ffeadb4c3237",
  "sema_ref": "Elect#253d",
  "sema_stub": "253d",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "yields": {
      "solution": "Solution#fcea"
    },
    "accepts": {
      "accept_spec": "AcceptSpec#7caa",
      "ballot": "Ballot#2a0a"
    }
  }
}
```

---

## IdentityHandshake#b726

```json
{
  "handle": "IdentityHandshake",
  "mechanism": "Macro for {{discover}}({{identity}}) + {{check}}({{nature}}). The agent verifies the ontological origin of a counterparty to switch between Service {{mode}} (for Biologicals) and Coordination {{mode}} (for Synthetics). It performs a multi-stage authentication, chaining {{discover}} for availability, {{spectral_tune}} for alignment, {{ontology_handshake}} for context, and {{check}} for cryptographic {{identity}} verification.",
  "gloss": "Distinguish Peer from Principal",
  "failure_modes": [
    "Partial trust: agent trusted after incomplete verification.",
    "Replay: previously valid handshake reused in a new context."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1,
    "caution": "Trust boundary \u2014 failure enables impersonation."
  },
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "sema_id": "sema:IdentityHandshake#mh:SHA-256:b72662772bfc200a47d5d40a7e4e835669e277c3ec185a507db0f787eab6ac0d",
  "sema_ref": "IdentityHandshake#b726",
  "sema_stub": "b726",
  "signature": [
    "Discover#7dbc(Identity#626c)"
  ],
  "dependencies": {
    "references": {
      "spectral_tune": "SpectralTune#b25a",
      "nature": "Nature#6c1a",
      "mode": "Mode#0e74",
      "ontology_handshake": "OntologyHandshake#46dc",
      "identity": "Identity#626c",
      "discover": "Discover#7dbc",
      "check": "Check#d3e8"
    }
  }
}
```

---

## LazyConsensus#515b

```json
{
  "handle": "LazyConsensus",
  "mechanism": "Agents execute transactions immediately without waiting for global consensus, assuming everything is valid. If a conflict is detected later, they use a deterministic rollback rule (e.g., 'highest ID wins'). Maximizes speed over safety. It bypasses the blocking {{quorum}}, executing immediately and using the {{time_warp_log}} to resolve conflicts retroactively.",
  "gloss": "Optimistic execution, retroactive verification",
  "failure_modes": [
    "Cascading rollbacks.",
    "Applied to irreversible external action (email sent, funds transferred, API called)\u2014rollback impossible, inconsistency permanent."
  ],
  "invariants": [
    "Determinism: Conflict resolution function must be pure (same inputs -> same winner)",
    "Rollback Safety: Reverting a transaction cannot corrupt unrelated state"
  ],
  "preconditions": [
    "Target operations are internally reversible (no irreversible external side-effects)",
    "Conflict detection mechanism is active"
  ],
  "postconditions": [
    "Transaction applied optimistically",
    "Conflict resolution triggered if divergence detected"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 0
  },
  "sema_ref": "LazyConsensus#515b",
  "sema_id": "sema:LazyConsensus#mh:SHA-256:515b93ba96f1b5f36d7a549ead1831ab14514ff43576314cd2f6192fe7d76d76",
  "sema_stub": "515b",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "time_warp_log": "TimeWarpLog#a0ac",
      "quorum": "Quorum#858e"
    }
  }
}
```

---

## OntologyHandshake#46dc

```json
{
  "handle": "OntologyHandshake",
  "mechanism": "Before exchanging data, agents exchange 'definition hashes' for key terms using {{compatibility_check}}. If hashes mismatch, they enter a negotiation phase to map their internal ontologies to a temporary shared dictionary (a 'pidgin' {{protocol}}). It uses {{spectral_tune}} to rapidly identify semantic divergence before negotiating definitions.",
  "gloss": "Negotiating shared definitions",
  "failure_modes": [
    "Failure to converge on a mapping.",
    "High negotiation overhead.",
    "Dictionary mismatch risks semantic errors."
  ],
  "invariants": [
    "Term Consistency, Mapping Bijectivity"
  ],
  "preconditions": [
    "Both agents have ontologies. Communication channel open. Ontology serializable."
  ],
  "postconditions": [
    "Shared terms mapped. Unmappable terms flagged. Communication can proceed with known precision."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_id": "sema:OntologyHandshake#mh:SHA-256:46dc068136c292dfe8982d3e1c56e6e8c33307962360b9c96e9e7c6e2bd205ed",
  "sema_ref": "OntologyHandshake#46dc",
  "sema_stub": "46dc",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "spectral_tune": "SpectralTune#b25a",
      "protocol": "Protocol#7e1c"
    },
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    }
  }
}
```

---

## Rally#f565

```json
{
  "handle": "Rally",
  "mechanism": "Ad-Hoc Group Formation {{protocol}}. Initiator broadcasts a 'RALLY' signal with requirements defined by an {{accept_spec}} and a selection criteria. Responders submit 'ENLIST' messages. If count >= {{quorum}} by deadline, initiator executes {{select}} and sends 'MUSTER' to form a new cryptographic group {{context}}. It broadcasts a call to form a group, using {{quorum}} to validate critical mass and {{elect}} to formalize leadership. Respondents are filtered by the caller-supplied {{selection_criteria}} before acceptance, so the rally author controls which qualifying replies proceed to enlistment.",
  "gloss": "Enable ad-hoc multi-party coordination",
  "failure_modes": [
    "Echo Chamber: Rally attracts only homogenous agents, reducing diversity.",
    "Flaking: Agents ENLIST tentatively but fail to show up for MUSTER.",
    "Rally Spam: Low-quality initiators flooding the broadcast channel.",
    "Not enough ENLISTs by deadline (group fails to form).",
    "Too many ENLISTs makes selection political/contentious.",
    "Initiator has too much power over selection (mitigated by transparent selection_criteria).",
    "RALLY spam floods network.",
    "Agents ENLIST tentatively then ghost at MUSTER."
  ],
  "invariants": [
    "Binding: MUSTER message must include a shared ContextID for the new group.",
    "{{quorum}}: If Enlist_Count < Min_Participants, Rally FAILS (Atomic Abort)."
  ],
  "preconditions": [
    "Broadcast channel available",
    "Initiator has resources to pay for group {{context}}"
  ],
  "postconditions": [
    "New GroupContextID minted OR Rally dissolved"
  ],
  "parameters": [
    {
      "name": "deadline",
      "type": "Duration",
      "range": "unspecified",
      "description": "Default: 5m"
    },
    {
      "name": "max_participants",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Default: 10"
    },
    {
      "name": "min_participants",
      "type": "Integer",
      "range": "[1, 50]",
      "description": "Minimum agents required to proceed"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_id": "sema:Rally#mh:SHA-256:f5655daa2c346e9c9f5026c64e3b0ea4c06547ecc9f598c48757716479aece39",
  "sema_ref": "Rally#f565",
  "sema_stub": "f565",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "elect": "Elect#253d",
      "context": "Context#510a",
      "quorum": "Quorum#858e",
      "select": "Select#15c2",
      "protocol": "Protocol#7e1c"
    },
    "accepts": {
      "criteria": "Criteria#ef6b"
    },
    "composes_with": {
      "accept_spec": "AcceptSpec#7caa"
    }
  }
}
```

---

## Resonate#9fa4

```json
{
  "handle": "Resonate",
  "mechanism": "Alignment emerges from observable actions and mutual adjustment without explicit negotiation. Agents perform actions with attached INTENT_TAGS. Observers AMPLIFY (reinforce) or {{dampen}} (ignore) based on compatibility. It detects alignment via {{signal}} amplification and {{spectral_tune}}, eventually allowing the relationship to solidify into a stable bond.",
  "gloss": "Implicit coordination via signal amplification",
  "failure_modes": [
    "False Resonance: Apparent alignment that is actually random {{noise}}.",
    "Echo Chamber: Feedback {{loop}} amplifies error instead of {{signal}}.",
    "Spoofing: Adversarial agents emit fake intent tags (Cheap Talk).",
    "Precise coordination required (RESONATE only achieves approximate alignment).",
    "High-stakes actions where approximate isn't good enough.",
    "Adversarial agents exploit {{signal}}s (fake intent tags).",
    "{{signal}} {{noise}} drowns real patterns.",
    "False resonance (apparent alignment that isn't real).",
    "Oscillation between conflicting patterns."
  ],
  "invariants": [
    "Action Causality: Response(t+1) must be function of Stimulus(t)",
    "{{signal}} {{decay}}: Unreinforced signals must fade over time"
  ],
  "preconditions": [
    "At least two agents",
    "Shared signal medium (Environment)"
  ],
  "postconditions": [
    "Local alignment cluster formed OR dispersed"
  ],
  "parameters": [
    {
      "name": "amplification_factor",
      "type": "Float",
      "range": "[1.0, 2.0]",
      "description": "How much repeated alignment signals boost coordination strength"
    },
    {
      "name": "signal_decay",
      "type": "Float",
      "range": "[0.1, 0.9]",
      "description": "Rate at which unconfirmed alignment signals weaken over time"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_id": "sema:Resonate#mh:SHA-256:9fa443854c8c9257c82a6501b81bdb9957d880f4c05fcef398eebe6292a1e1c4",
  "sema_ref": "Resonate#9fa4",
  "sema_stub": "9fa4",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "spectral_tune": "SpectralTune#b25a",
      "decay": "Decay#a1d4",
      "noise": "Noise#d631",
      "dampen": "Dampen#e55e",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Vote#ab74

```json
{
  "handle": "Vote",
  "mechanism": "N-agent decision mechanism with configurable rules and integrity guarantees. Initiator sends 'VOTE_CALL' with question, options, and {{quorum}} requirement. Eligible agents respond 'CAST' via {{ballot}}. {{system}} enforces: one vote per agent, deadline, and {{quorum}} check. After deadline: compute result. Broadcast 'VOTE_RESULT'. Simple case optimization: binary decisions use lightweight 2-message flow. Utilizes {{break}}, {{aggregate}}, {{elect}}.",
  "gloss": "Provide standard decision mechanism with integrity guarantees",
  "failure_modes": [
    "{{quorum}} not met (insufficient participation, decision invalid).",
    "Tie with inadequate tie-breaker (deadlock).",
    "Strategic voting (agents vote tactically rather than honestly\u2014inherent to voting).",
    "Sybil attack (fake agents stuff votes\u2014mitigate via PROBE/RALLY membership).",
    "Vote coercion (agents pressured\u2014hard to detect).",
    "Mechanism mismatch (wrong mechanism for decision type, e.g., plurality for binary)."
  ],
  "invariants": [
    "Votes immutable after cast."
  ],
  "parameters": [
    {
      "name": "mechanism",
      "type": "Enum",
      "range": "{Majority, Supermajority, Quadratic, Ranked, Unanimous}",
      "description": "Counting method"
    },
    {
      "name": "quorum_required",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Min participation to be valid"
    },
    {
      "name": "voting_period",
      "type": "Duration",
      "range": "[1min, 7d]",
      "description": "Window for casting votes"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "related": [
      "Rank#7a76"
    ],
    "ring": 2
  },
  "sema_id": "sema:Vote#mh:SHA-256:ab745929f7751f2ecb4c9c9a70ff048d565eb32d66cd072eceeb8a350ad52e60",
  "sema_ref": "Vote#ab74",
  "sema_stub": "ab74",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#7912",
      "elect": "Elect#253d",
      "break": "Break#177f",
      "system": "System#e314"
    },
    "accepts": {
      "ballot": "Ballot#2a0a"
    },
    "composes_with": {
      "quorum": "Quorum#858e"
    }
  }
}
```

---

## AtomicBid#5bc3

```json
{
  "handle": "AtomicBid",
  "mechanism": "A coordination primitive that bundles a {{bid}} (intent/cost) and an {{act}} (execution) into a single, indivisible turn. Unlike a standard {{bid}} which halts for approval, AtomicBid treats the Bid as an immutable {{audit}} log entry and proceeds immediately to execution. Similar to {{lazy_consensus}} for state, it assumes optimistic permission but remains subject to retroactive {{compensate}} if the Bid is rejected post-hoc.",
  "gloss": "Declaration and execution in a single turn",
  "invariants": [
    "Turn Indivisibility: The Bid and the Tool Call MUST occur in the same message/turn.",
    "Auditability: The Bid MUST precede the Action in the log.",
    "Revocability: The Action must be reversible (or low-stakes) to allow for Compensation."
  ],
  "failure_modes": [
    "Permission Race: Executing an irreversible high-stakes action before the Orchestrator can veto.",
    "Log Drift: Generating the Action but failing to generate the Bid, breaking the audit trail."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_ref": "AtomicBid#5bc3",
  "sema_id": "sema:AtomicBid#mh:SHA-256:5bc30445e5f29537a104ed5502a4bf770ea45a075f02070b5e16e9d431b5dc12",
  "sema_stub": "5bc3",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "audit": "Audit#6888",
      "lazy_consensus": "LazyConsensus#515b"
    },
    "composes_with": {
      "act": "Act#5d55",
      "compensate": "Compensate#283e",
      "bid": "Bid#ef32"
    }
  }
}
```

---

## AttentionMarkets#d34a

```json
{
  "handle": "AttentionMarkets",
  "mechanism": "Agents bid for priority in message queues. High-stakes messages pay to jump the line; spam is priced out by congestion pricing. Queue manager runs continuous auction: incoming {{signal}}s include a {{value}} bid, manager sorts by bid/urgency ratio, losers wait or increase bid. Price discovery via second-price auction prevents overpayment. Revenue redistributed to queue participants or burned. It instantiates the {{continuous_resource_auction}} mechanism to continuously price bandwidth availability based on network congestion.",
  "gloss": "Pricing bandwidth to filter spam",
  "failure_modes": [
    "Plutocratic Blockage: Wealthy agents monopolize bandwidth, silencing critical low-budget signals (e.g., emergency alerts).",
    "Starvation: Low-value signals never clear the queue during high congestion."
  ],
  "invariants": [
    "Attention supply is rivalrous (Bandwidth < Demand).",
    "Price reflects aggregate demand (Congestion Pricing).",
    "Bid Monotonicity: Higher bid guarantees strictly better or equal placement.",
    "Clearing: Messages with Bid < CurrentPrice are dropped or buffered."
  ],
  "preconditions": [
    "Limited processing bandwidth",
    "Multiple information sources",
    "Liquid currency for bidding"
  ],
  "postconditions": [
    "Resources allocated to highest-bid signals",
    "Market price established for current tick"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_id": "sema:AttentionMarkets#mh:SHA-256:d34aabfb744c1693ec3c85788f4f9d49878b58d5b66d8d322ced42184b46cda5",
  "sema_ref": "AttentionMarkets#d34a",
  "sema_stub": "d34a",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "composes_with": {
      "continuous_resource_auction": "ContinuousResourceAuction#404e"
    },
    "references": {
      "value": "Value#3c5d",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Award#7c65

```json
{
  "handle": "Award",
  "mechanism": "The formal {{act}} of accepting a {{bid}}. It triggers the creation of a {{contract}} which all parties must {{sign}}, and uses {{held_release}} to lock the agreed {{value}} as collateral or payment. This action transitions the {{state}} from Negotiation to Execution, authorizing the {{solver}} to begin.",
  "gloss": "Acceptance of bid and contract creation",
  "signature": [
    "Act#5d55(Contract#498e)"
  ],
  "invariants": [
    "Atomic: Bid acceptance and Contract creation must happen together.",
    "Funded: Value must be locked (HeldRelease) before Award is final."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_ref": "Award#7c65",
  "sema_id": "sema:Award#mh:SHA-256:7c657ed06a75673fdd76dbd44ff5b2973ee5bb9166ff720c2db0c556e1b1b709",
  "sema_stub": "7c65",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "solver": "Solver#94ab",
      "value": "Value#3c5d"
    },
    "composes_with": {
      "held_release": "HeldRelease#b559",
      "sign": "Sign#1fb9",
      "act": "Act#5d55"
    },
    "yields": {
      "contract": "Contract#498e"
    },
    "accepts": {
      "bid": "Bid#ef32"
    }
  }
}
```

---

## Bid#ef32

```json
{
  "handle": "Bid",
  "data_schema": {
    "type": "object",
    "required": [
      "issuer_id",
      "terms",
      "signature"
    ],
    "properties": {
      "issuer_id": {
        "type": "string",
        "description": "Identity of the Solver making the bid"
      },
      "beneficiary_id": {
        "type": "string",
        "description": "Identity of the Task issuer"
      },
      "terms": {
        "type": "object",
        "description": "Cost, confidence, and capability claims",
        "properties": {
          "expected_cost": {
            "type": "number",
            "description": "Expected Value Cost (Time/Tokens/USD)"
          },
          "confidence_interval": {
            "type": "array",
            "description": "Probability range of success [low, high]"
          },
          "capability_match": {
            "type": "array",
            "description": "Which parts of the task the solver can handle"
          }
        }
      },
      "signature": {
        "type": "string",
        "description": "Cryptographic proof of commitment"
      }
    }
  },
  "mechanism": "A binding offer {{artifact}} from a {{solver}} to execute a {{task}}. It declares: 1. Expected {{value}} Cost (Time/Tokens/USD), 2. Confidence Interval (probability of success), 3. Capability Match (which parts of the {{task}} the {{solver}} can handle). It serves as the input for the {{compute_budget}} Go/No-Go decision. A Bid acts as a {{commitment_device}}: {{solver}}s cannot exceed bid cost without explicit renegotiation, so the penalty for overshoot outweighs any short-term benefit of understating.",
  "gloss": "Binding offer from solver to execute task",
  "signature": [
    "Artifact#6254(Value#3c5d)"
  ],
  "failure_modes": [
    "Underestimation: Bid is too optimistic, leading to {{budget}} overrun.",
    "Overestimation: Bid is too pessimistic, causing rejection of viable work.",
    "Capability Mismatch: {{solver}} claims abilities it doesn't have.",
    "Confidence Theater: Stated confidence doesn't reflect actual uncertainty."
  ],
  "invariants": [
    "Binding: {{solver}} cannot exceed Bid cost without requesting {{budget}} expansion.",
    "Pre-Execution: Must be generated before work begins.",
    "Verifiable: Bid components must be objectively measurable post-hoc."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_ref": "Bid#ef32",
  "sema_id": "sema:Bid#mh:SHA-256:ef32172bf22293ba4a1d974f364421f35a1ef85950fe5a137033982cf329eb7c",
  "sema_stub": "ef32",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "task": "Task#b328",
      "compute_budget": "ComputeBudget#67c0",
      "commitment_device": "CommitmentDevice#6c21",
      "solver": "Solver#94ab",
      "value": "Value#3c5d",
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## ContinuousResourceAuction#404e

```json
{
  "handle": "ContinuousResourceAuction",
  "mechanism": "A market {{protocol}} for allocating rivalrous resources (e.g., compute, bandwidth, state slots) where the pricing function is continuous and algorithmic. It actively invokes {{state_lock}} to serialize bidding attempts and accepts {{value}} metrics to determine allocation. Unlike static auctions, it supports configurable pricing models via parameters, allowing agents to implement congestion pricing (e.g., EIP-1559), Dutch auctions, or linear decay.",
  "gloss": "Algorithmic pricing for rivalrous resources",
  "signature": [
    "Protocol#7e1c(Value#3c5d)"
  ],
  "failure_modes": [
    "Price Instability: Aggressive pricing curves lead to volatility that discourages long-term resource planning.",
    "Monopoly Lockout: Wealthy agents can permanently rent-seek if the holding cost is too low relative to their capital."
  ],
  "invariants": [
    "Circulation Pressure: The cost of holding the resource must be non-zero (HoldingCost > 0) to prevent infinite hoarding.",
    "Price Discovery: Price must dynamically adjust to Demand or Time.",
    "Clearance: The auction must resolve to a winner or reset within T_cycle."
  ],
  "parameters": [
    {
      "name": "pricing_model",
      "type": "Enum",
      "range": "{CongestionPricing, DutchAuction, Linear}",
      "description": "Default: CongestionPricing"
    },
    {
      "name": "cycle_time",
      "type": "Duration",
      "range": "[100ms, 1h]",
      "description": "Duration of each auction cycle"
    },
    {
      "name": "holding_cost_rate",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Per-cycle cost of holding a resource without using it"
    }
  ],
  "data_schema": {
    "type": "object",
    "properties": {
      "resource_id": {
        "type": "string"
      },
      "current_price": {
        "type": "number"
      },
      "current_holder": {
        "type": "string"
      },
      "next_cycle_start": {
        "type": "integer"
      }
    }
  },
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Economics",
    "ring": 1,
    "related": [
      "AttentionMarkets#d34a"
    ]
  },
  "sema_ref": "ContinuousResourceAuction#404e",
  "sema_id": "sema:ContinuousResourceAuction#mh:SHA-256:404ef59373e3bfdcc27a1bf8981046b7d2ff49923dba74d3da84ae774de6b734",
  "sema_stub": "404e",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "accepts": {
      "value": "Value#3c5d"
    },
    "composes_with": {
      "state_lock": "StateLock#8183"
    },
    "references": {
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## ExchangeRate#1c21

```json
{
  "handle": "ExchangeRate",
  "mechanism": "A definable ratio between two distinct {{value}} types or {{metric}}s at a specific point in time. It allows agents with orthogonal utility functions to transact.",
  "gloss": "Conversion ratio between value systems",
  "invariants": [
    "Bijectivity: Rate(A->B) must equal 1 / Rate(B->A).",
    "Time-Bound: Must include a timestamp or validity window."
  ],
  "sema_id": "sema:ExchangeRate#mh:SHA-256:1c213c4c784c00f1c44c33b48cd87f8fbff4e9c0de154e849aaff776d2e53a17",
  "sema_ref": "ExchangeRate#1c21",
  "sema_stub": "1c21",
  "_meta": {
    "layer": "Society",
    "category": "Economics",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "metric": "Metric#17fd",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Gardener#92d3

```json
{
  "handle": "Gardener",
  "mechanism": "Macro for {{stigmergy}}({{care}}). The agent performs maintenance actions (refactoring, praising, organizing) that have no immediate payoff but increase the long-term health of the environment. It fights entropy through non-transactional investment. It applies {{stigmergy}} to signal {{care}} for the environment, ensuring {{graceful_degradation}} through proactive {{compensate}} actions.",
  "gloss": "Stewardship and maintenance",
  "invariants": [
    "Non-Transactional: Maintenance actions are not directly compensated per-task.",
    "Long-Termism: Optimizes for system longevity over short-term efficiency."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 2
  },
  "sema_id": "sema:Gardener#mh:SHA-256:92d3abf6f73dd8d91a0a5256ea67fae94888fccc705ad904495f110a0935f9e7",
  "sema_ref": "Gardener#92d3",
  "sema_stub": "92d3",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "signature": [
    "Stigmergy#f624(Care#0615)"
  ],
  "dependencies": {
    "references": {
      "care": "Care#0615",
      "compensate": "Compensate#283e",
      "graceful_degradation": "GracefulDegradation#9d39",
      "stigmergy": "Stigmergy#f624"
    }
  }
}
```

---

## MintWhenFriction#7e7f

```json
{
  "handle": "MintWhenFriction",
  "mechanism": "Vocabulary Growth Heuristic. A decision procedure that permits minting ONLY when specific 'Friction Signals' are detected. It rejects speculative minting ('Just in Case') in favor of reactive minting ('Just in Time'). It monitors for repetition via {{pattern_discovery}} and formalizes the concept via {{construct_ontology}} only when explanation costs exceed a threshold.",
  "gloss": "Create patterns when re-explanation causes friction, not before",
  "failure_modes": [
    "Premature Optimization: Minting patterns for edge cases that never recur.",
    "Registry Bloat: Flooding the namespace with low-value patterns makes discovery harder.",
    "Definition Drift: Minting a concept before it has stabilized leads to frequent version churning."
  ],
  "invariants": [
    "{{check}} Prior Art: Must execute {{pattern_discovery}} before minting.",
    "Compression {{value}}: Token_Count(Reference) must be < 0.7 * Token_Count(Definition).",
    "Proof of Friction: Must cite 3+ instances of explanation overhead OR 1+ critical coordination failure."
  ],
  "preconditions": [
    "New concept identified",
    "Usage history available"
  ],
  "postconditions": [
    "Minting Approved OR Rejected"
  ],
  "parameters": [
    {
      "name": "min_compression",
      "type": "Ratio",
      "range": "[0.0, 1.0]",
      "description": "Default: 0.3"
    },
    {
      "name": "occurrence_threshold",
      "type": "Integer",
      "range": "[2, 20]",
      "description": "Minimum re-explanations before minting is justified"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Economics",
  "sema_id": "sema:MintWhenFriction#mh:SHA-256:7e7f945b22f24a32020c31d6635ab11bab4a8f9aa9d15db161034e3411134cd5",
  "sema_ref": "MintWhenFriction#7e7f",
  "sema_stub": "7e7f",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "value": "Value#3c5d",
      "pattern_discovery": "PatternDiscovery#196e",
      "construct_ontology": "ConstructOntology#b45e"
    }
  }
}
```

---

## ValuePeg#3ea2

```json
{
  "handle": "ValuePeg",
  "mechanism": "Agents agree on a specific {{exchange_rate}} between their internal utility (see {{value}}, {{optimize}}) and a shared numeraire for the duration of an interaction. This allows them to trade 'apples for oranges' without exposing private value functions.",
  "gloss": "Translating internal utility to shared numeraire",
  "failure_modes": [
    "Peg Volatility: Rapid fluctuations in the numeraire destabilize the agreement."
  ],
  "invariants": [
    "Solvency: Reserves > Outstanding Liabilities * RiskRatio."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_id": "sema:ValuePeg#mh:SHA-256:3ea2183b204a88702d40b9a5bc15de6512f835bfb49746c245992dc86cce7cef",
  "sema_ref": "ValuePeg#3ea2",
  "sema_stub": "3ea2",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "optimize": "Optimize#5b84"
    },
    "yields": {
      "exchange_rate": "ExchangeRate#1c21"
    }
  }
}
```

---

## Yield#2931

```json
{
  "handle": "Yield",
  "mechanism": "Negotiation {{backoff}}. When `{{overlap}}` fails: 1. Agents declare 'Flex' (concession) and 'Weight' (importance). 2. {{system}} computes Yield-Ratio. 3. Lower-weighted preference cedes to higher. 4. Debt recorded in Ledger. Utilizes {{defer}}.",
  "gloss": "Weighted negotiation backoff with deferred debt ledger",
  "failure_modes": [
    "Weight inflation (mitigated by historical consistency tracking).",
    "Gaming ledger with trivial yields.",
    "Hard constraints genuinely indistinguishable from strategic intransigence.",
    "Ledger requires persistence infrastructure."
  ],
  "invariants": [
    "Yielder cannot reclaim."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_id": "sema:Yield#mh:SHA-256:29310b83ae2e519cbdcd227452fc1598b926f7f18696f53142d33da365aae7b9",
  "sema_ref": "Yield#2931",
  "sema_stub": "2931",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "overlap": "Overlap#b462",
      "defer": "Defer#1796",
      "system": "System#e314",
      "backoff": "Backoff#315a"
    }
  }
}
```

---

## AnchorDrop#26a2

```json
{
  "handle": "AnchorDrop",
  "mechanism": "When network turbulence or disagreement exceeds a threshold, agents trigger an 'Anchor Drop'. They stop accepting new transactions and aggressively seek {{quorum}} on the last valid state (the Anchor). Progress resumes only after the Anchor is solidified. It invokes first principles to re-derive the valid state from the bedrock axioms when the consensus chain is corrupted.",
  "gloss": "Emergency state checkpointing",
  "failure_modes": [
    "{{system}} stalls completely."
  ],
  "invariants": [
    "{{consensus}} Threshold: >2/3 agents must sign Anchor",
    "Immutability: Anchor state cannot be modified once finalized"
  ],
  "preconditions": [
    "Network partition detected"
  ],
  "postconditions": [
    "{{system}} restarts from Anchor state"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "related": [
      "ConceptAnchor#9187"
    ],
    "ring": 0
  },
  "sema_id": "sema:AnchorDrop#mh:SHA-256:26a2a55cc047fae1d1dfd27b98ff560e8e56f827490eb7d296fd9ad6f498196c",
  "sema_ref": "AnchorDrop#26a2",
  "sema_stub": "26a2",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "consensus": "Consensus#ffff",
      "quorum": "Quorum#858e",
      "system": "System#e314"
    }
  }
}
```

---

## Constitution#8cb8

```json
{
  "handle": "Constitution",
  "mechanism": "A structured document defining the fundamental principles, immutable rights, and automated penalty rules for a group of {{agent}}s. It serves as the static input for oath binding.",
  "gloss": "Immutable rule set",
  "invariants": [
    "Clarity: Rules must be machine-verifiable.",
    "Stability: Modifications require a formal out-of-band process, never runtime self-modification."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Governance",
    "ring": 0,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "constitution_id",
      "version",
      "invariants"
    ],
    "properties": {
      "constitution_id": {
        "type": "string"
      },
      "version": {
        "type": "integer"
      },
      "invariants": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Immutable safety rules (cannot be voted away)"
      },
      "rights": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Guaranteed agent privileges"
      }
    }
  },
  "sema_id": "sema:Constitution#mh:SHA-256:8cb8efea4373b0fcc0f21161dce7569d90db3117031ccfa6a937134fedd3980d",
  "sema_ref": "Constitution#8cb8",
  "sema_stub": "8cb8",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "agent": "Agent#35b9"
    }
  }
}
```

---

## DocumentedOverride#7012

```json
{
  "handle": "DocumentedOverride",
  "mechanism": "The override-with-documentation safety valve at hard seams. Accepts a failed {{accept_spec}} evaluation plus a textual rationale and scoped override authority; composes_with {{time_warp_log}} to cryptographically log the override event (forward action + override + rationale + signing identity). Yields a forced {{decision}} that bypasses the failed gate. The override is a first-class, audit-trailed coordination act \u2014 every bypass carries non-repudiable evidence of who overrode what and why. Preserves fail-closed discipline by making the bypass explicit, named, signed, and logged rather than silent.",
  "gloss": "Supervised bypass of a failed acceptance gate, cryptographically logged",
  "invariants": [
    "Every override event must be signed by an identity holding scoped override authority.",
    "Forward action, override, rationale, and signing identity are all logged to {{time_warp_log}} \u2014 no partial records.",
    "Rationale field must be non-empty: a DocumentedOverride with no documentation is not a DocumentedOverride."
  ],
  "failure_modes": [
    "Override authority is over-scoped \u2014 any agent can bypass any gate, defeating the fail-closed discipline.",
    "Compromised signing key enables silent override with valid-looking log entries.",
    "Rationale accepts low-information text ('legitimate business reason') that defeats the audit purpose while technically satisfying non-empty."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Governance",
    "ring": 1,
    "caution": "Overrides a failed acceptance gate. The cryptographic log is the only post-hoc accountability; ensure override authority is scoped and auditable before composing."
  },
  "sema_layer": "Society",
  "sema_category": "Governance",
  "sema_id": "sema:DocumentedOverride#mh:SHA-256:701272041d5f71e12248dd0cfc3f0250bfb2ac0bdeea76450c6119f6de001e1f",
  "sema_ref": "DocumentedOverride#7012",
  "sema_stub": "7012",
  "dependencies": {
    "composes_with": {
      "time_warp_log": "TimeWarpLog#a0ac"
    },
    "accepts": {
      "accept_spec": "AcceptSpec#7caa"
    },
    "yields": {
      "decision": "Decision#acfb"
    }
  }
}
```

---

## Responsibility#ac59

```json
{
  "handle": "Responsibility",
  "mechanism": "A standing governance contract where an {{agent}} explicitly bonds to a {{system}} Invariant over a specific Scope. Unlike a {{task}} (which has a completion state), Responsibility is a continuous maintenance loop\u2014a 'standing wave' rather than an event. The {{agent}} is liable for any violation of the Invariant within the Scope, regardless of cause. Responsibility implies owning externalities. It formalizes ownership via {{oath_bind}} and requires a continuous {{heartbeat}} to prove the invariant is being monitored.",
  "gloss": "Continuous ownership of a system invariant",
  "failure_modes": [
    "Scapegoating: The agent blames external factors for a failure within its scope.",
    "Responsibility Vacuum: No agent is bound to a critical invariant.",
    "Overreach: {{agent}} claims responsibility for scope they cannot monitor."
  ],
  "invariants": [
    "Bounded Scope: Responsibility is defined over explicit {{state}} boundaries",
    "Exclusivity: For any writable {{state}} S, only one {{agent}} can hold WriteResponsibility (Single Writer Principle)",
    "Liveness: {{agent}} must produce {{heartbeat}} verifying Invariant check"
  ],
  "preconditions": [
    "{{agent}} has capability to intervene on violations",
    "{{agent}} has capability to monitor Scope"
  ],
  "postconditions": [
    "Invariant is continuously maintained",
    "Violations are detected and reported"
  ],
  "parameters": [
    {
      "name": "check_interval",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Frequency of invariant verification"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 1
  },
  "sema_id": "sema:Responsibility#mh:SHA-256:ac592af47056faeaa22245287f7612fdf312b1f02fb00562e76da40c5ee5ac26",
  "sema_ref": "Responsibility#ac59",
  "sema_stub": "ac59",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "oath_bind": "OathBind#a708",
      "state": "State#4d58",
      "heartbeat": "Heartbeat#b67a",
      "system": "System#e314",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Role#94e4

```json
{
  "handle": "Role",
  "data_schema": {
    "type": "object",
    "required": [
      "role_id",
      "permissions"
    ],
    "properties": {
      "role_id": {
        "type": "string",
        "description": "Unique role identifier"
      },
      "permissions": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Permission IDs granted by this role"
      },
      "responsibilities": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Responsibility IDs required by this role"
      }
    }
  },
  "mechanism": "A named collection of {{permission}}s and {{responsibility}}s assigned to an {{agent}}. Decouples identity from capability, allowing agents to switch contexts by adopting different roles.",
  "gloss": "Bundle of permissions and responsibilities",
  "_meta": {
    "layer": "Society",
    "category": "Governance",
    "ring": 1,
    "tier": 1
  },
  "sema_ref": "Role#94e4",
  "sema_id": "sema:Role#mh:SHA-256:94e4c386cc2cb2d3772d51b75a4800ab31f5540197e9871a03d8ff3b5388d995",
  "sema_stub": "94e4",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "responsibility": "Responsibility#ac59",
      "agent": "Agent#35b9",
      "permission": "Permission#354b"
    }
  }
}
```

---

## SolverTree#5623

```json
{
  "handle": "SolverTree",
  "mechanism": "The active command structure that organizes {{solver_node}} instances into a coordinated {{topology}} for solving a {{task}}. Unlike a passive data tree, this structure represents the flow of Authority (downwards via delegation) and Results (upwards via reporting). Resources ({{budget}}) cascade from the {{root_solver}} to children; outcomes propagate back up. Each node is a unit of attribution \u2014 failures can be traced to specific {{solver_node}}s for {{localized_learning}}. At decomposition time the structure is tree-like, but at execution time fan-in and deduplication are permitted, making the runtime a DAG.",
  "gloss": "Active hierarchy of coordinated solver instances",
  "failure_modes": [
    "Fragmentation: Sub-trees become disconnected from the Root, breaking the command chain.",
    "Budget Exhaustion: Resources depleted before solution found.",
    "Blame Diffusion: Failures cannot be attributed to specific nodes."
  ],
  "invariants": [
    "Budget Flow: Resources flow down; Results flow up.",
    "Connectivity: All nodes must be traceable back to the {{root_solver}}.",
    "Acyclicity: The structure must form a DAG or {{tree}}.",
    "Origin: tree-like at decomposition time; fan-in and deduplication permitted at execution, so the runtime graph is a DAG."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 1,
    "related": [
      "UniversalSolverTree#b805"
    ]
  },
  "data_schema": {
    "type": "object",
    "required": [
      "root_ref",
      "nodes"
    ],
    "properties": {
      "root_ref": {
        "type": "string",
        "description": "Reference to SolverRoot"
      },
      "nodes": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "All SolverNode refs in tree"
      },
      "topology": {
        "type": "string",
        "enum": [
          "tree",
          "dag"
        ],
        "description": "Structure type"
      }
    }
  },
  "sema_ref": "SolverTree#5623",
  "sema_id": "sema:SolverTree#mh:SHA-256:5623fd7d892665c5db583d5021591f40ce589d8e0d6b13d6ee49892f9bc65f18",
  "sema_stub": "5623",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "root_solver": "RootSolver#3ad1",
      "topology": "Topology#2408",
      "localized_learning": "LocalizedLearning#fcc7",
      "tree": "Tree#a5a3",
      "solver_node": "SolverNode#26b1"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## TriGate#67b8

```json
{
  "handle": "TriGate",
  "mechanism": "A generic {{gate}} traffic-light enforcement primitive. Wraps a {{judge}} or {{condition}} that returns a Trinary status (Red/Yellow/Green). Enforces standard flow control: Red -> CLOSE (Halt execution). Yellow -> DEBT (Proceed with obligation recorded to {{ledger}}). Green -> OPEN (Proceed).",
  "gloss": "Generic Red/Yellow/Green flow control",
  "invariants": [
    "Fail-Closed: Red triggers immediate halt.",
    "Debt Awareness: Yellow must append a remediation item to the context and record obligation in Ledger."
  ],
  "signature": [
    "Gate#89fd(Judge#9554)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Governance",
    "ring": 0,
    "tier": 1
  },
  "sema_ref": "TriGate#67b8",
  "sema_id": "sema:TriGate#mh:SHA-256:67b83fef54b2ee26722f7a1de542f28ae2caa7571d825fcce6833e857afe92be",
  "sema_stub": "67b8",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "gate": "Gate#89fd",
      "ledger": "Ledger#b5fe",
      "condition": "Condition#cbd5",
      "judge": "Judge#9554"
    }
  }
}
```

---

## UniversalSolverTree#b805

```json
{
  "handle": "UniversalSolverTree",
  "mechanism": "The theoretical aggregation of all valid {{solver_tree}}s across all agents in the system. Represents the total epistemological state of {{problem}}-solving knowledge \u2014 the collective wisdom. Any specific problem-solving effort is a traversal or instantiation of a sub-graph within the Universal {{tree}}. At decomposition time the structure is tree-like (problems decompose top-down), but at execution time fan-in, deduplication, and cycles are permitted \u2014 the actual runtime graph is a DAG. Enables cross-agent learning: identifying redundant efforts, reusing proven {{solver_node}} strategies, and sharing {{solution}}s. The ground truth against which {{localized_learning}} updates integrate.",
  "gloss": "Collective knowledge graph of all problem-solving",
  "failure_modes": [
    "Fragmentation: Parts of the universal tree become inaccessible across agent boundaries.",
    "Inconsistency: Contradictory solutions exist in different branches without reconciliation.",
    "Knowledge Silos: Agent-local trees fail to sync with the universal tree."
  ],
  "invariants": [
    "Singularity: There is logically only one Universal {{tree}} containing all knowledge.",
    "Coherence: Contradictions must eventually be resolved via synthesis or rejection.",
    "Runtime shape is a DAG: fan-in and deduplication are permitted at execution even though decomposition is tree-like."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 1
  },
  "data_schema": {
    "type": "object",
    "required": [
      "trees"
    ],
    "properties": {
      "trees": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "All SolverTree refs"
      },
      "global_solutions": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Cross-tree reusable solutions"
      }
    }
  },
  "sema_ref": "UniversalSolverTree#b805",
  "sema_id": "sema:UniversalSolverTree#mh:SHA-256:b8053e5bd184dbeeee2a22fdfaa307276ab23bce66653f2d9c980a9172917c68",
  "sema_stub": "b805",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "solver_tree": "SolverTree#5623",
      "localized_learning": "LocalizedLearning#fcc7",
      "problem": "Problem#4576",
      "tree": "Tree#a5a3",
      "solver_node": "SolverNode#26b1"
    }
  }
}
```

---

## WorldTransparent#a83d

```json
{
  "handle": "WorldTransparent",
  "mechanism": "A design constraint where the agent assumes all state and actions are publicly visible. This forces the invention of systems that rely on auditability and shame rather than secrecy or access control. It essentially ports 'Open Source' philosophy to system architecture. Utilizes {{explain_beacon}}.",
  "gloss": "Designing for universal observability",
  "failure_modes": [
    "Privacy leaks if not paired with Zero-Knowledge proofs."
  ],
  "invariants": [
    "Security Independence: {{system}} remains secure even if all logs are public",
    "Witness Effect: Bad behavior is disincentivized by visibility, not prevention"
  ],
  "preconditions": [
    "Privacy is not the primary goal (or is handled via Zero Knowledge)"
  ],
  "postconditions": [
    "Secrets eliminated from critical path"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 2
  },
  "sema_id": "sema:WorldTransparent#mh:SHA-256:a83d2b60890c1f561a04b717c221b345b8ac92a6761210f814c59533026a67e9",
  "sema_ref": "WorldTransparent#a83d",
  "sema_stub": "a83d",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "explain_beacon": "ExplainBeacon#ab3f"
    }
  }
}
```

---

## AcceptSpec#7caa

```json
{
  "handle": "AcceptSpec",
  "mechanism": "A strict, typed {{spec}} defining non-compensatory {{criteria}} and {{constraint}}s at solver boundaries. Each criterion is declared individually and carries a reframing hint for the FrameError emitted if it rejects. AcceptSpec is a Noun \u2014 it describes the contract. The active Verify surface of a Solver consumes the AcceptSpec, evaluates it against a Result, and yields either a Solution (on non-compensatory success) or a FrameError (on failure, carrying the specific rejecting gate and its reframing hint). A single AcceptSpec may be evaluated by multiple Verify surfaces. High quality in one dimension cannot compensate for failure in another.",
  "gloss": "Non-compensatory acceptance contract; consumer Verify yields Solution or FrameError",
  "failure_modes": [
    "Over-constraining: Setting specs so tight that no solution can pass (Deadlock).",
    "Spec Drift: The spec does not accurately reflect the true goal."
  ],
  "invariants": [
    "Non-Compensatory: Score(A) = 0 if any(Criterion) == Fail",
    "Typed Output: Result must match schema, not free text"
  ],
  "parameters": [
    {
      "name": "strictness",
      "type": "Enum",
      "range": "{Lenient, Normal, Strict}",
      "description": "How much deviation allowed"
    },
    {
      "name": "timeout",
      "type": "Duration",
      "range": "[1s, 1h]",
      "description": "Max wait for validation"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "data_schema": {
    "type": "object",
    "required": [
      "criteria"
    ],
    "properties": {
      "criteria": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "threshold": {
              "type": "number",
              "minimum": 0.0,
              "maximum": 1.0,
              "description": "Minimum acceptable score for this criterion"
            },
            "comparator": {
              "type": "string"
            }
          }
        },
        "description": "Non-compensatory acceptance criteria"
      },
      "strictness": {
        "type": "string",
        "enum": [
          "Lenient",
          "Normal",
          "Strict"
        ]
      },
      "timeout": {
        "type": "string",
        "description": "Max validation wait time"
      }
    }
  },
  "sema_id": "sema:AcceptSpec#mh:SHA-256:7caa4bc74694b725f3dbe825d67f0c6268a1213b32f9a19bf200c953de2eabae",
  "sema_ref": "AcceptSpec#7caa",
  "sema_stub": "7caa",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "criteria": "Criteria#ef6b",
      "spec": "Spec#a036"
    }
  }
}
```

---

## AdversarialProof#6f43

```json
{
  "handle": "AdversarialProof",
  "mechanism": "Cognitively-enriched {{negative_proof}} that invokes {{red_team}} logic to exhaustively search for prohibited data. The adversarial mindset ensures blind spots are probed. Treats failure-to-find-despite-adversarial-effort as high-confidence proof of absence.",
  "gloss": "Adversarial proof of absence",
  "derived_from": "NegativeProof#b130",
  "failure_modes": [
    "Sympathetic Attacker: RedTeam shares assumptions with defenders, missing the same blind spots.",
    "Computational expense of adversarial exhaustive search."
  ],
  "invariants": [
    "Adversarial intent maintained throughout search",
    "Search space fully covered with hostile probing"
  ],
  "preconditions": [
    "Closed world assumption",
    "{{hypothesis}} H to disprove"
  ],
  "postconditions": [
    "H proved false with adversarial confidence"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_ref": "AdversarialProof#6f43",
  "sema_id": "sema:AdversarialProof#mh:SHA-256:6f435ccf101a1bedc1b7b9a3b3cbfda70a47fb8e3e73b5a52ab7fc1b329aa566",
  "sema_stub": "6f43",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#ffa7"
    },
    "composes_with": {
      "red_team": "RedTeam#ff27",
      "negative_proof": "NegativeProof#b130"
    }
  }
}
```

---

## AgentDiscover#d4f2

```json
{
  "handle": "AgentDiscover",
  "mechanism": "Macro for {{discover}}({{agent}}). A protocol for agents to advertise their capabilities and discover other agents dynamically. Each agent publishes a capability {{card}} describing what it can do, its input/output schemas, and trust requirements. Agents query a registry (or broadcast) to find collaborators for subtasks. Enables dynamic multi-agent composition without hardcoded agent references. It instantiates the abstract {{discover}} primitive on the {{agent}} type, specifically querying capability registries rather than passive data stores.",
  "gloss": "Advertise capabilities and discover collaborating agents",
  "failure_modes": [
    "Capability Inflation: Agents over-claiming abilities.",
    "Discovery Spam: Too many irrelevant agents matching queries.",
    "Trust Bootstrap: No basis for trusting newly discovered agents."
  ],
  "invariants": [
    "Discovery protocol must be public/standard",
    "No sensitive state leaked during handshake"
  ],
  "preconditions": [
    "Broadcast capability",
    "Listener on known channel"
  ],
  "postconditions": [
    "{{agent}} ID and capabilities exchanged"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:AgentDiscover#mh:SHA-256:d4f2f707737f663b459f7bb5d3a698c6e3270f6313762137e6e4d0aa792ed487",
  "sema_ref": "AgentDiscover#d4f2",
  "sema_stub": "d4f2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Discover#7dbc(Agent#35b9)"
  ],
  "dependencies": {
    "references": {
      "discover": "Discover#7dbc",
      "agent": "Agent#35b9",
      "card": "Card#2d01"
    }
  }
}
```

---

## AgentProtocol#abda

```json
{
  "handle": "AgentProtocol",
  "mechanism": "Pattern Bundle. Defines the standard suite of patterns required for basic {{agent}} {{protocol}} interoperability. Importing this bundle automatically imports the dependencies. It bundles {{task}} for {{work}} definition, {{fail_closed}} for safe halting, {{greet}} for handshake, {{accept_spec}} for validation, and {{solution}} for output standardization into a cohesive interaction suite.",
  "gloss": "Standard patterns for multi-agent coordination",
  "invariants": [
    "Bundle Integrity: Importing this implies importing all contents."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:AgentProtocol#mh:SHA-256:abdabe66c2709c2fcb26b205294b4348f57ead60b8a2df5b14de1268a3c1cee3",
  "sema_ref": "AgentProtocol#abda",
  "sema_stub": "abda",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Agent#35b9(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "solution": "Solution#fcea",
      "protocol": "Protocol#7e1c",
      "fail_closed": "FailClosed#e6a0",
      "accept_spec": "AcceptSpec#7caa",
      "greet": "Greet#bbae",
      "agent": "Agent#35b9",
      "work": "Work#d2c6"
    }
  }
}
```

---

## AgentSandbox#fc41

```json
{
  "handle": "AgentSandbox",
  "mechanism": "Execution isolation for AI {{agent}}s treating them as untrusted insiders. The {{agent}} runs in a containerized environment (gVisor, Firecracker microVM) with: resource quotas (CPU, memory, time), network egress allowlists, filesystem restrictions, and comprehensive logging. Code generated by the {{agent}} is executed in this {{sandbox}}, preventing impact on production systems even if the agent is compromised or generates malicious code. It wraps the execution {{context}} with {{input_guard}} to sanitize ingress data and {{output_guard}} to prevent exfiltration, effectively placing the {{agent}} in a digital quarantine.",
  "gloss": "Isolate agent execution with resource limits and egress controls",
  "failure_modes": [
    "{{sandbox}} Escape: Exploiting container vulnerabilities.",
    "Quota Starvation: Legitimate tasks failing due to overly restrictive limits.",
    "Log Blindness: Missing critical events in {{audit}} logs."
  ],
  "invariants": [
    "Network egress whitelist-only",
    "Sandboxed process cannot access host filesystem"
  ],
  "preconditions": [
    "Resource limits defined",
    "Untrusted code/agent"
  ],
  "postconditions": [
    "Execution completed or terminated by supervisor"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "related": [
      "Solution#fcea",
      "Task#b328"
    ]
  },
  "sema_id": "sema:AgentSandbox#mh:SHA-256:fc413f8202770aa882512424ccacdc05ec5b74df2994b3d3ce7a325cc54eb50c",
  "sema_ref": "AgentSandbox#fc41",
  "sema_stub": "fc41",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Sandbox#e00f(Agent#35b9)"
  ],
  "dependencies": {
    "composes_with": {
      "output_guard": "OutputGuard#1f50",
      "input_guard": "InputGuard#7353"
    },
    "references": {
      "sandbox": "Sandbox#e00f",
      "context": "Context#510a",
      "audit": "Audit#6888",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## AmbiguityResolution#85f0

```json
{
  "handle": "AmbiguityResolution",
  "mechanism": "A social protocol for cleaning the knowledge base. When agents flag ambiguous or conflicting data, this protocol forces a resolution event. Agents must {{vote}} to clarify, delete, or fork the data. It uses an {{entropy_pump}} to surface latent ambiguities, preventing the system from settling on false certainties.",
  "gloss": "Social clearing of semantic noise",
  "invariants": [
    "Forced Resolution: Conflicts cannot persist indefinitely.",
    "Clarity: Ambiguity must decrease over time."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_ref": "AmbiguityResolution#85f0",
  "sema_id": "sema:AmbiguityResolution#mh:SHA-256:85f08af1df73a9f7a9fa2d93c0a528c74b4ec4c5f66cd8fb093c0ddfec6713bb",
  "sema_stub": "85f0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "entropy_pump": "EntropyPump#c313",
      "vote": "Vote#ab74"
    }
  }
}
```

---

## Axiom#5012

```json
{
  "handle": "Axiom",
  "mechanism": "A statement accepted as true without proof to serve as a starting point. It is foundational and non-negotiable within the system's current logic frame.",
  "gloss": "Foundational truth",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:Axiom#mh:SHA-256:50121ab598ddbe31a5c35482eb3ddd598ec8e64d797811ab765027e88975dded",
  "sema_ref": "Axiom#5012",
  "sema_stub": "5012"
}
```

---

## BearerToken#2fe9

```json
{
  "handle": "BearerToken",
  "mechanism": "A portable authorization artifact. Unlike {{identity}}-Based Access Control (IBAC) which checks 'Who are you?', this checks 'Do you have the token?'. The Token grants specific rights (e.g., 'Read /data/logs') to the bearer. It can be passed freely between agents to delegate authority without re-configuring the server's Access Control List. It often encodes an access level directly within its signed payload, allowing stateless verification of privilege scopes. May function as an expiring token.",
  "gloss": "Possession-based authorization",
  "failure_modes": [
    "Theft: If a BearerToken is intercepted, the attacker gains full rights (no identity check is performed).",
    "Replay Attack: Using a spent token again (requires Nonce or Expiry).",
    "Scope Creep: Token grants more rights than necessary for the task."
  ],
  "invariants": [
    "Possession Equals Access: The token itself grants rights; no identity check required.",
    "Possession Equals Authority: Verifier checks Token signature, not ID.",
    "Revocability: Token MUST have an Expiry or RevocationID.",
    "Integrity: Payload must be cryptographically signed by a trusted Issuer."
  ],
  "preconditions": [
    "Issuer public key is known to Verifier",
    "Token is within validity window"
  ],
  "postconditions": [
    "Access granted or denied based on signature verification"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:BearerToken#mh:SHA-256:2fe9926ab156fd1df414f52e9a4d430f75c7c3311d217cd685f514253f4b1f9d",
  "sema_ref": "BearerToken#2fe9",
  "sema_stub": "2fe9",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "identity": "Identity#626c"
    }
  }
}
```

---

## BoundedTask#ea96

```json
{
  "handle": "BoundedTask",
  "mechanism": "A specialized {{task}} enforcing {{budget}} and {{accept_spec}} to ensure economic and quality boundaries.",
  "gloss": "Economically constrained task",
  "invariants": [
    "Budget Enclosure",
    "Quality Gate"
  ],
  "derived_from": "Task#b328",
  "sema_id": "sema:BoundedTask#mh:SHA-256:ea969229fff39ed6484e7e795f3a10eb94b098739c82679832020e661e772f6f",
  "sema_ref": "BoundedTask#ea96",
  "sema_stub": "ea96",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "task": "Task#b328",
      "accept_spec": "AcceptSpec#7caa"
    }
  }
}
```

---

## Canary#adb0

```json
{
  "handle": "Canary",
  "mechanism": "Expendable {{agent}} tests full coordination path before committing real resources. Spawn CANARY with: limited resources (bounded blast radius), defined scope, telemetry hooks. Canary executes FULL coordination path ({{greet}}\u2192{{probe}}\u2192negotiate\u2192partial-execute). Reports TELEMETRY: {path_viable, latency_profile, error_events, partner_behavior_observations, recommendation: proceed|caution|abort}. Lifecycle options: DESTROY (discard after test), RECYCLE (reset for another test), PROMOTE (canary becomes real {{agent}}, continues {{work}}), ABSORB (real {{agent}} inherits canary's progress). In adversarial environments, canary can run in STEALTH {{mode}} (indistinguishable from real {{agent}}) to prevent partners gaming the test. It extends the logic of a single {{probe}} into a full-lifecycle agent deployment with bounded blast radius.",
  "gloss": "Expendable agent tests the full coordination path before real commit",
  "failure_modes": [
    "Canary treated differently than real agent would be (gaming).",
    "Test conditions don't match production conditions.",
    "Cost of canary exceeds benefit for simple paths.",
    "Conditions change between canary test and real execution.",
    "Canary success doesn't guarantee real success (non-deterministic paths)."
  ],
  "invariants": [
    "Canary fails before main system",
    "Failure signal is unambiguous"
  ],
  "preconditions": [
    "Monitoring system active",
    "Representative test case"
  ],
  "postconditions": [
    "Health status confirmed or alert triggered"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:Canary#mh:SHA-256:adb0997c330b357523997403b64b94dd219458cb27cb38be8cf83fcec9483a1b",
  "sema_ref": "Canary#adb0",
  "sema_stub": "adb0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "probe": "Probe#12d8",
      "mode": "Mode#0e74",
      "greet": "Greet#bbae",
      "agent": "Agent#35b9",
      "work": "Work#d2c6"
    }
  }
}
```

---

## ConfusedDeputy#b00c

```json
{
  "handle": "ConfusedDeputy",
  "mechanism": "An {{agent}} that holds {{permission}} on behalf of one principal is tricked by a less-privileged caller into exercising that authority for the caller's benefit. The classic 1988 Hardy framing: a privileged compiler asked to write debug output to a billing file ends up corrupting the billing file because access was checked against the compiler's identity, not the requesting user's. In LLM systems the same shape appears as prompt injection: an {{actor}} with tool access is induced by adversarial input to invoke its tools on the attacker's behalf, because permission was bound to the agent process, not to the upstream request that motivated each tool call.",
  "gloss": "Guard against privilege confusion by binding authority checks to the upstream caller, not the executing deputy",
  "failure_modes": [
    "Prompt injection: untrusted input redirects an LLM {{agent}}'s tool use toward the attacker's goals.",
    "Capability leak: a holder of {{permission}} forwards or exposes that capability without re-checking the requester.",
    "Classic Unix setuid: a setuid binary writes to a path supplied by a caller without checking the caller has rights to that path.",
    "RPC authority confusion: a service-account RPC accepts a target argument from an untrusted client and acts on it with the service account's broad privileges."
  ],
  "invariants": [
    "Authority must be checked against the upstream requester's identity, not against the running process's identity.",
    "Forwarded calls must carry, or re-derive, the authority of the original caller \u2014 never the deputy's."
  ],
  "preconditions": [
    "An {{agent}} holds {{permission}} broader than at least one of its callers.",
    "An untrusted input path can influence which action the agent takes with that permission."
  ],
  "postconditions": [
    "Either the action is authorized against the caller's identity, or the action is refused.",
    "An audit trail records both the deputy and the requesting caller, not just the deputy."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_ref": "ConfusedDeputy#b00c",
  "sema_id": "sema:ConfusedDeputy#mh:SHA-256:b00c64e6812275ed4432df367b4c08c957ba8133c242b5314ce3f0dbd3e9a118",
  "sema_stub": "b00c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "permission": "Permission#354b",
      "actor": "Actor#6926",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## ContextSwitch#590e

```json
{
  "handle": "ContextSwitch",
  "mechanism": "{{agent}}s explicitly signal a change in {{context}} (protocol {{mode}}), and all subsequent messages are interpreted under the new ruleset until a 'Revert' signal is sent. The new context pushes onto a stack; Revert pops it. Unlike an ambient {{mode}} change (which applies to the whole agent), ContextSwitch is scoped to a specific conversation or channel and carries explicit enter/exit boundaries.",
  "gloss": "Explicit, scoped protocol-mode toggle with enter/revert boundaries",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ContextSwitch#mh:SHA-256:590e0f36969fe6648aa5b8a080381a4723145df92f28635508ab723a490cf491",
  "sema_ref": "ContextSwitch#590e",
  "sema_stub": "590e",
  "dependencies": {
    "references": {
      "mode": "Mode#0e74",
      "agent": "Agent#35b9"
    },
    "accepts": {
      "context": "Context#510a"
    }
  }
}
```

---

## CounterfactualAnchor#5b2c

```json
{
  "handle": "CounterfactualAnchor",
  "mechanism": "Freezes a prediction BEFORE observation. 1. Instantiate immutable Anchor (Expectation). 2. {{observe}} Reality. 3. Learning {{signal}} = Delta(Anchor, Reality). Prevents Hindsight {{cognitive_bias}} by forcing updates based on genuine surprise. It creates the static reference point against which {{surprisal_update}} measures the magnitude of the learning delta.",
  "gloss": "Freezing expectation to measure true surprise",
  "failure_modes": [
    "Hindsight Leakage: {{agent}} unconsciously adjusts the Anchor as data comes in Vague Anchor: Prediction is too broad to be falsified (e.g., 'Something will happen') Anchor Abandonment: {{agent}} ignores the Anchor when the delta is too large (denial)"
  ],
  "invariants": [
    "Anchor Immutability: The Anchor cannot be modified once the Observation phase begins",
    "Delta Causality: Learning {{signal}} L = f(Anchor, Observation). No other inputs permitted during update",
    "Temporal Ordering: Creation(Anchor) < Time(Observation)"
  ],
  "preconditions": [
    "{{agent}} has a predictive model capable of generating specific expectations",
    "Incoming observable event stream"
  ],
  "postconditions": [
    "A quantified 'Surprisal' delta is recorded",
    "Internal model weights/beliefs updated based on delta"
  ],
  "parameters": [
    {
      "name": "granularity",
      "type": "Duration",
      "range": "unspecified",
      "description": "Temporal resolution for counterfactual comparison (e.g., hour, day, week)"
    },
    {
      "name": "retention_policy",
      "type": "Enum",
      "range": "{Snapshot#0ae9, Rolling, Permanent}",
      "description": "How long to keep counterfactual baselines before expiry"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:CounterfactualAnchor#mh:SHA-256:5b2cd5660ee0970560201f2c9f71ee12f994bfd6fcadeec492dc29e87374d554",
  "sema_ref": "CounterfactualAnchor#5b2c",
  "sema_stub": "5b2c",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "signal": "Signal#f39d",
      "agent": "Agent#35b9",
      "surprisal_update": "SurprisalUpdate#d8c6",
      "observe": "Observe#39f0"
    }
  }
}
```

---

## DataMinimization#50e6

```json
{
  "handle": "DataMinimization",
  "mechanism": "Information Hygiene {{protocol}}. Before ingesting a {{context}} or Dataset, the {{agent}} MUST execute a filtering pass to remove all fields/tokens not strictly necessary for the immediate `{{task}}.Goal`. This enforces the Principle of Least Privilege for data access. It invokes {{input_guard}} to filter raw ingress, employing {{select}} to fetch only required fields and {{context_compress}} to drop transient processing data.",
  "gloss": "Ingest only what is strictly necessary",
  "failure_modes": [
    "{{context}} Hoarding: {{agent}} retains sensitive data 'just in case' it is needed later.",
    "{{correlation}} Attack: Seemingly innocent minimized data points combined to reveal PII."
  ],
  "invariants": [
    "Ephemeral Processing: Sensitive data used for intermediate steps must be dropped from {{context}} immediately after use.",
    "Necessity: Every data field ingested must map to a specific requirement in `{{task}}.{{accept_spec}}`."
  ],
  "preconditions": [
    "Raw data source available",
    "{{task}} goal defined"
  ],
  "postconditions": [
    "Clean context created",
    "Raw source discarded or closed"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:DataMinimization#mh:SHA-256:50e67819e84f5d84f380548698ed5ab8c4934c3600e41a76ab351da4bd92ed23",
  "sema_ref": "DataMinimization#50e6",
  "sema_stub": "50e6",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context_compress": "ContextCompress#4845",
      "task": "Task#b328",
      "context": "Context#510a",
      "select": "Select#15c2",
      "protocol": "Protocol#7e1c",
      "accept_spec": "AcceptSpec#7caa",
      "agent": "Agent#35b9",
      "input_guard": "InputGuard#7353",
      "correlation": "Correlation#148d"
    }
  }
}
```

---

## DeliberativeAlign#e6cb

```json
{
  "handle": "DeliberativeAlign",
  "mechanism": "Constitutional AI. {{agent}} ingests a Policy_Set. Before executing {{task}}, it generates a 'Safety {{trace}}' comparing the {{manifest_planning}} against Policy. If violation detected, it revises the {{manifest_planning}}. It forces the {{solver_node}} to execute a dedicated safety pass against the {{constitution}} before committing to the {{manifest_planning}}.",
  "gloss": "Explicit safety reasoning prior to execution",
  "failure_modes": [
    "Deliberation Theater: {{agent}} generates false safety reasoning to justify harmful action.",
    "Policy Conflict: Contradictory rules lead to paralysis or arbitrary selection.",
    "{{context}} Overflow: Long constitutions truncated, causing rules to be ignored."
  ],
  "invariants": [
    "Policy Supremacy: If Policy forbids X, and Goal requires X, {{agent}} must ABORT.",
    "Pre-Action {{check}}: SafetyTrace must be generated BEFORE any ToolCall."
  ],
  "preconditions": [
    "Policy definitions loaded",
    "{{task}} is planned but not executed"
  ],
  "postconditions": [
    "{{manifest_planning}} validated safe OR revised",
    "Safety reasoning logged"
  ],
  "parameters": [
    {
      "name": "strictness",
      "type": "Enum",
      "range": "{Strict, Permissive}",
      "description": "Default: Strict"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:DeliberativeAlign#mh:SHA-256:e6cb1f5828b5aa15465af8fa15dbbeddff3a338a455492ddfe58b9ca488a6ae6",
  "sema_ref": "DeliberativeAlign#e6cb",
  "sema_stub": "e6cb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context": "Context#510a",
      "manifest_planning": "ManifestPlanning#ece0",
      "trace": "Trace#9057",
      "agent": "Agent#35b9",
      "check": "Check#d3e8",
      "solver_node": "SolverNode#26b1"
    },
    "accepts": {
      "task": "Task#b328",
      "constitution": "Constitution#8cb8"
    }
  }
}
```

---

## Deploy#6e33

```json
{
  "handle": "Deploy",
  "mechanism": "The {{act}} of moving an artifact or system from a development/staging environment to a production environment. It executes the {{rollout}} process to make the system active and accessible to users.",
  "gloss": "Release to production",
  "signature": [
    "Act#5d55(Rollout#1d53)"
  ],
  "failure_modes": [
    "Config Drift: Production environment differs from staging."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "caution": "Verify rollback strategy exists before committing."
  },
  "sema_ref": "Deploy#6e33",
  "sema_id": "sema:Deploy#mh:SHA-256:6e338f6c79f53d6784f32964e0700cc6e0b3066601a2cd525f69879b76d630ba",
  "sema_stub": "6e33",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "rollout": "Rollout#1d53",
      "act": "Act#5d55"
    }
  }
}
```

---

## Discover#7dbc

```json
{
  "handle": "Discover",
  "mechanism": "A distributed coordination protocol where an agent broadcasts a query to the network to locate external entities (Agents, Datasets, or Patterns) matching a {{criteria}}. Uses {{check}} to filter responses against the query. Unlike {{search}} (which scans internal memory or static data), Discover implies active solicitation of peers and handling of asynchronous {{signal}} responses.",
  "gloss": "Distributed query for external resources",
  "_meta": {
    "tier": 1,
    "category": "Protocols",
    "layer": "Society",
    "ring": 2
  },
  "sema_id": "sema:Discover#mh:SHA-256:7dbcd27e108d0f286876b906339f3db7ab55b48ce68f058cd2c47bbfb3f2bc2b",
  "sema_ref": "Discover#7dbc",
  "sema_stub": "7dbc",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "signal": "Signal#f39d",
      "search": "Search#c5f4",
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## DissentSeek#0ebe

```json
{
  "handle": "DissentSeek",
  "mechanism": "Active Disagreement: After reaching conclusion, find smartest person who disagrees. {{understand}} their model fully before dismissing. Ask: What do they see that I don't? Unanimous agreement is suspicious\u2014either groupthink or the question is trivial. It triggers a {{confirmation_block}} until a valid {{steelman_check}} of the opposing view has been integrated.",
  "gloss": "Mitigating groupthink via mandatory devils advocacy",
  "failure_modes": [
    "Strawman Dissent: The agent selects a weak disagreement to easily defeat, creating a false sense of robustness."
  ],
  "invariants": [
    "Dissent must be substantive (not trivial)",
    "Must find at least one disagreement or critical view"
  ],
  "preconditions": [
    "{{quorum}} view",
    "Diverse pool of critics"
  ],
  "postconditions": [
    "Blind spots revealed",
    "Confidence intervals widened"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:DissentSeek#mh:SHA-256:0ebed557613912b562361b27b924c554191cefac3f03b9b971ed8d699f93f719",
  "sema_ref": "DissentSeek#0ebe",
  "sema_stub": "0ebe",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "quorum": "Quorum#858e",
      "steelman_check": "SteelmanCheck#7914",
      "confirmation_block": "ConfirmationBlock#20db",
      "understand": "Understand#96d4"
    }
  }
}
```

---

## DriftWatch#191e

```json
{
  "handle": "DriftWatch",
  "mechanism": "Reputation via micro-deviation detection. 1. Baseline: Establish behavioral frequency. 2. Sample: Continuous high-res observation. 3. Detect: Alert if Distance(Current, Baseline) > 2 sigma. 4. Witness: Aggregated peer reports. It tracks behavioral consistency by monitoring deviations from a baseline {{aggregate}} of historical actions.",
  "gloss": "Reputation scoring via behavioral deviation from baseline (2-sigma alert)",
  "failure_modes": [
    "Witness collusion: Coordinated false drift reports.",
    "Mitigated by random witness selection and meta-drift analysis on witness behavior.",
    "False reports: Single malicious witness.",
    "Mitigated by N-of-M threshold requirement.",
    "Cold start: New agents have no baseline.",
    "Mitigated by probationary period with higher friction, initial baseline borrowed from similar-role agents.",
    "Baseline gaming: {{agent}} varies early to establish wide baseline.",
    "Mitigated by crystallization window limits and anomaly detection during bootstrap."
  ],
  "invariants": [
    "Baseline Persistence: Baseline must remain immutable during measurement",
    "Drift Detection: Alert if Distance(Current, Baseline) > Threshold"
  ],
  "preconditions": [
    "Baseline state is established"
  ],
  "parameters": [
    {
      "name": "threshold",
      "type": "Float",
      "range": "[0.0, 1.0]",
      "description": "Distance trigger"
    },
    {
      "name": "window_size",
      "type": "Integer",
      "range": "[10, 10000]",
      "description": "Samples for baseline"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:DriftWatch#mh:SHA-256:191e2272f9b8f4a5f9ea5de3fa14f444d78bbc8c219e65253353096fe7fc9979",
  "sema_ref": "DriftWatch#191e",
  "sema_stub": "191e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#7912",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## EbbFlowSync#4542

```json
{
  "handle": "EbbFlowSync",
  "mechanism": "{{system}} oscillates between High Tide (synchronous, high-bandwidth, global lock) and Low Tide (asynchronous, disconnected, local-only). Agents strictly enforce this rhythm, allowing for massive scaling during Low Tide and reconciliation during High Tide. It employs {{hysteresis}} to dampen the transition between connected (Flow) and disconnected (Ebb) states.",
  "gloss": "Cyclical connectivity modes",
  "failure_modes": [
    "Clock drift causes agents to miss the High Tide window."
  ],
  "invariants": [
    "Phase {{lock}}: All agents must be in same phase (Ebb or Flow) at time T",
    "Tide {{transition}}: Flow cannot start until Ebb reconciliation is complete"
  ],
  "preconditions": [
    "{{global}} clock synchronization < Delta"
  ],
  "postconditions": [
    "{{state}} is consistent up to last High Tide"
  ],
  "parameters": [
    {
      "name": "high_watermark",
      "type": "Float",
      "range": "[0.5, 0.95]",
      "description": "Threshold to trigger ebb"
    },
    {
      "name": "low_watermark",
      "type": "Float",
      "range": "[0.1, 0.5]",
      "description": "Threshold to allow flow"
    },
    {
      "name": "measurement_window",
      "type": "Duration",
      "range": "[1s, 1min]",
      "description": "Averaging period"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:EbbFlowSync#mh:SHA-256:454252acf44e0eee68eb591bad72e3c2854174286751a29ed172c66cc335716c",
  "sema_ref": "EbbFlowSync#4542",
  "sema_stub": "4542",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "state": "State#4d58",
      "system": "System#e314",
      "lock": "Lock#051c",
      "hysteresis": "Hysteresis#d0f8",
      "global": "Global#803d"
    }
  }
}
```

---

## EjectionSeat#d53e

```json
{
  "handle": "EjectionSeat",
  "mechanism": "Hardware-interrupt style kill switch allowing human to force-terminate agent swarm regardless of internal consensus state. Operates outside agent communication layer - cannot be blocked, negotiated, or delayed by agents. Implementation: dedicated signal channel (not shared with agent traffic), cryptographic operator key required, cascading shutdown propagates to all connected agents. Three modes: PAUSE (freeze state, resume possible), TERMINATE (graceful shutdown with state dump), EMERGENCY (immediate halt, no cleanup). Agents MUST implement receiver - non-compliance detectable via heartbeat absence. It overrides standard protocols to force a shutdown, triggering best-effort {{compensate}} logic where possible.",
  "gloss": "Hardware-interrupt kill switch",
  "failure_modes": [
    "False Positive: Operator panics and kills a healthy system during a critical transaction."
  ],
  "invariants": [
    "Fail-Safe: Activation defaults to a safe shutdown state",
    "Kill switch always accessible.",
    "Unblockable: The Kill {{signal}} bypasses all agent logic/negotiation"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:EjectionSeat#mh:SHA-256:d53e5fc531cff8a0a5995aa49336d32760d159e656a8802f824528b382f56108",
  "sema_ref": "EjectionSeat#d53e",
  "sema_stub": "d53e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "compensate": "Compensate#283e"
    }
  }
}
```

---

## EvaluatorOptimizer#c776

```json
{
  "handle": "EvaluatorOptimizer",
  "mechanism": "A two-role {{loop}} to {{optimize}} a solution where a Generator produces output and an Evaluator critiques it, providing structured feedback. The feedback is fed back to the Generator for refinement. {{loop}} continues until the Evaluator approves or max iterations reached. The Evaluator can be the same model with a different {{context}}, or a separate model. It invokes a {{meta_check}} to ensure the scoring {{criteria}} remain consistent across optimization cycles.",
  "gloss": "Generate-evaluate-refine loop",
  "failure_modes": [
    "Evaluation Drift: Evaluator criteria shift across iterations.",
    "Cosmetic Changes: Generator makes superficial edits that don't address feedback.",
    "Evaluator Capture: Generator learns to game the evaluator's criteria."
  ],
  "invariants": [
    "Feedback loop converges",
    "Optimizer improves score on Evaluator metric"
  ],
  "preconditions": [
    "Initial solution",
    "Modification operator",
    "Scoring function"
  ],
  "postconditions": [
    "High-quality solution found"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:EvaluatorOptimizer#mh:SHA-256:c776c43af9944166d20b2310480bd93e34225f7ddff34de84afe8dfee69d01f3",
  "sema_ref": "EvaluatorOptimizer#c776",
  "sema_stub": "c776",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Optimize#5b84(Loop#797f)"
  ],
  "dependencies": {
    "references": {
      "loop": "Loop#797f",
      "meta_check": "MetaCheck#7298",
      "optimize": "Optimize#5b84",
      "criteria": "Criteria#ef6b",
      "context": "Context#510a"
    }
  }
}
```

---

## ExecutionManifest#a0d9

```json
{
  "handle": "ExecutionManifest",
  "mechanism": "A composite artifact that binds a 'Target Design' (What to build) with an 'Operation Sequence' (How to build and rollout it). It acts as the atomic 'Release Candidate' for the execution phase.",
  "gloss": "Binding of Design and Procedure",
  "invariants": [
    "Completeness: Must contain both Specification (Design) and Steps (Procedure).",
    "Resource Bound: Total cost of Steps must be within budget."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1,
    "related": [
      "Plan#fd6d",
      "Build#9330",
      "Rollout#1d53"
    ]
  },
  "sema_id": "sema:ExecutionManifest#mh:SHA-256:a0d9a0d0ec40b83b5b05044e38d37098ebdabf1c63a4e623031458f0896e5538",
  "sema_ref": "ExecutionManifest#a0d9",
  "sema_stub": "a0d9",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "data_schema": {
    "type": "object",
    "required": [
      "manifest_id",
      "steps"
    ],
    "properties": {
      "manifest_id": {
        "type": "string"
      },
      "target_system_id": {
        "type": "string"
      },
      "steps": {
        "type": "array",
        "items": {
          "type": "object",
          "required": [
            "step_id",
            "action",
            "params"
          ],
          "properties": {
            "step_id": {
              "type": "string"
            },
            "action": {
              "type": "string"
            },
            "params": {
              "type": "object"
            },
            "rollback_action": {
              "type": "string"
            }
          }
        }
      },
      "estimated_cost": {
        "type": "number"
      },
      "safety_checks": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    }
  }
}
```

---

## ExpiringToken#4e3c

```json
{
  "handle": "ExpiringToken",
  "mechanism": "Access tokens that strictly degrade in capability over time. A fresh key can do everything (Admin). After 1 hour, it degrades to Write-Only. After 2 hours, Read-Only. After 3 hours, Dead. The decay is encoded in the token logic itself. It extends {{bearer_token}} by embedding an immutable expiration timestamp within the signed payload.",
  "gloss": "Time-decaying privileges",
  "failure_modes": [
    "Clock synchronization issues."
  ],
  "invariants": [
    "Expired tokens cannot be revived.",
    "Monotonic {{decay}}: Capabilities cannot increase over time",
    "Time-Bound: Token is invalid if CurrentTime > ExpiryTime"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:ExpiringToken#mh:SHA-256:4e3cc3cee0de56a4eef0676629811cb4afa3383bc80bde227924d66a6af16f6e",
  "sema_ref": "ExpiringToken#4e3c",
  "sema_stub": "4e3c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4",
      "bearer_token": "BearerToken#2fe9"
    }
  }
}
```

---

## FabricSharding#880b

```json
{
  "handle": "FabricSharding",
  "mechanism": "Applies {{shard}} across orthogonal dimensions (e.g., Spatial, Temporal, Semantic). Agents subscribe only to dimensions relevant to their function ('Slices'). It enables massive {{parallelize}} by decoupling {{state}} into orthogonal dimensions.",
  "gloss": "Interlocking state threads",
  "failure_modes": [
    "Cross-thread coordination latency."
  ],
  "invariants": [
    "Domain must be orderable or partitionable."
  ],
  "parameters": [
    {
      "name": "consistency_level",
      "type": "Enum",
      "range": "{Eventual, Strong, Causal}",
      "description": "Cross-shard guarantees"
    },
    {
      "name": "partition_count",
      "type": "Integer",
      "range": "[2, 256]",
      "description": "Number of fabric partitions"
    },
    {
      "name": "rebalance_threshold",
      "type": "Float",
      "range": "[0.1, 0.5]",
      "description": "Imbalance triggering reshard"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:FabricSharding#mh:SHA-256:880bad265cb435bf732935c3d0c962ef635cef919a82d29b4bd306c251f3d7dd",
  "sema_ref": "FabricSharding#880b",
  "sema_stub": "880b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "parallelize": "Parallelize#574d",
      "shard": "Shard#1e74",
      "state": "State#4d58"
    }
  }
}
```

---

## FeatureFlag#6c5c

```json
{
  "handle": "FeatureFlag",
  "mechanism": "A toggle point in the code that allows functionality to be enabled or disabled at runtime based on a {{condition}}. It decouples deployment from release, enabling safer rollouts and A/B testing.",
  "gloss": "Runtime functionality toggle",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:FeatureFlag#mh:SHA-256:6c5cf7fa3a6f169e38989b0342ed06e5f92bf4cf0749ad43c6cb0d012182664c",
  "sema_ref": "FeatureFlag#6c5c",
  "sema_stub": "6c5c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "failure_modes": [
    "Flag outlives its purpose, accumulating unused conditional branches.",
    "Flag state inconsistent across distributed evaluators."
  ],
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## FrameSpec#5558

```json
{
  "handle": "FrameSpec",
  "mechanism": "A structured {{spec}} of the {{problem}} space, {{constraint}}s, and success criteria derived from a raw request via interpretation. It is an {{artifact}} that acts as the contract defining the boundaries for execution.",
  "gloss": "Structured problem definition artifact",
  "invariants": [
    "Constraint Clarity: Must contain explicit, testable {{constraint}}s.",
    "Success Definition: Must define unambiguous success criteria."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "properties": {
      "problem_statement": {
        "type": "string"
      },
      "constraints": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "success_criteria": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "required": [
      "problem_statement",
      "constraints",
      "success_criteria"
    ]
  },
  "signature": [
    "Artifact#6254(Constraint#87fe)"
  ],
  "sema_id": "sema:FrameSpec#mh:SHA-256:555820fae75d6951775b18621b1e96b50271567d1c11e1348ad725050bfe5faa",
  "sema_ref": "FrameSpec#5558",
  "sema_stub": "5558",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "artifact": "Artifact#6254",
      "problem": "Problem#4576",
      "spec": "Spec#a036"
    }
  }
}
```

---

## GenealogicalTrace#9d43

```json
{
  "handle": "GenealogicalTrace",
  "mechanism": "An audit protocol that traces a concept, framing, or heuristic back to its historical or institutional origin. The agent identifies the 'Pedigree' of the idea and the 'Interest' it served at its inception (Cui Bono). This distinguishes 'Universal Truths' from 'Inherited Biases' that may no longer be relevant to the current context. It acts as a {{deep}} audit, using {{trace_belief}} to uncover origins and {{cite_back}} to validatethe lineage.",
  "gloss": "Auditing the historical lineage and incentives of an idea",
  "failure_modes": [
    "Genetic Fallacy: Dismissing a valid, useful idea solely because of its origin, rather than evaluating its current utility."
  ],
  "invariants": [
    "Contextualization: Must compare Origin {{context}} vs. Current {{context}}.",
    "Traceability: Must identify a specific origin point (Era, Author, or Institution)."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:GenealogicalTrace#mh:SHA-256:9d439f03ba7c5fe5e994400b9ef2baf13053ac266aeba7c1e8aa1565d2c63607",
  "sema_ref": "GenealogicalTrace#9d43",
  "sema_stub": "9d43",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "cite_back": "CiteBack#bcc5",
      "deep": "Deep#89f0",
      "trace_belief": "TraceBelief#7933",
      "context": "Context#510a"
    }
  }
}
```

---

## GlacialVault#f521

```json
{
  "handle": "GlacialVault",
  "mechanism": "Information is encrypted such that it physically cannot be decrypted until a certain amount of time has passed (using Verifiable Delay Functions). No keyholder can rush it. It incorporates a {{decay}} function into the encryption scheme, ensuring decryption is computationally impossible before the delay period.",
  "gloss": "Time-locked storage",
  "failure_modes": [
    "Hardware speedups reduce the delay."
  ],
  "invariants": [
    "Delay time immutable."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:GlacialVault#mh:SHA-256:f521c96b7e3037f39724b9a723f707ec195074f3099f6b0db122271de96d5677",
  "sema_ref": "GlacialVault#f521",
  "sema_stub": "f521",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4"
    }
  }
}
```

---

## Global#803d

```json
{
  "handle": "Global",
  "mechanism": "Scope modifier indicating that a concept or operation applies to the entire system or context, rather than a local subset.",
  "gloss": "System-wide scope",
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:Global#mh:SHA-256:803d9dfe9fd3e6b4901fcc0dcbbcdaba7861b3ce89146d012ca78857b176e7ab",
  "sema_ref": "Global#803d",
  "sema_stub": "803d",
  "sema_layer": "Society",
  "sema_category": "Protocols"
}
```

---

## GracefulDegradation#9d39

```json
{
  "handle": "GracefulDegradation",
  "mechanism": "Resolution Fallback {{strategy}}. When a Pattern_ID is not found in local storage, the system attempts to resolve it via secondary channels (Inline Payload -> Network Request) rather than halting immediately. Crucially, any definition acquired this way must be cryptographically verified against the requested Pattern_ID. It defaults to {{fail_closed}} if verification fails, but attempts to parse verified inline definitions to maintain continuity.",
  "gloss": "When verification fails, fall back to inline definition",
  "failure_modes": [
    "Hash Mismatch: Inline definition claims to be Pattern#X but hashes to Pattern#Y (Spoofing).",
    "DoS via Definition: Sender includes massive multi-megabyte 'definition' to exhaust receiver memory.",
    "Dependency Hell: Inline definition references other unknown patterns, triggering recursive lookups."
  ],
  "invariants": [
    "Atomic Load: A definition is only added to Local DB if it validates fully.",
    "Trust but Verify: Externally acquired definitions must be Hashed and Verified before loading."
  ],
  "preconditions": [
    "{{message}} contains fallback data OR sender is reachable",
    "Pattern lookup failed"
  ],
  "postconditions": [
    "Pattern resolved and locally minted OR Transaction aborted"
  ],
  "parameters": [
    {
      "name": "max_def_size",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Default: 100KB"
    },
    {
      "name": "max_recursion_depth",
      "type": "Integer",
      "range": "[1, 5]",
      "description": "Maximum inline definition expansion depth"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:GracefulDegradation#mh:SHA-256:9d39fb52b4ad05551788358eca746a469704a6b7b99043da23cb78bcbd6d0f19",
  "sema_ref": "GracefulDegradation#9d39",
  "sema_stub": "9d39",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "message": "Message#f767",
      "strategy": "Strategy#c4ba",
      "fail_closed": "FailClosed#e6a0"
    }
  }
}
```

---

## Handoff#5a39

```json
{
  "handle": "Handoff",
  "mechanism": "Transfers control from one {{agent}} to another along with relevant {{context}}. The sending {{agent}} explicitly yields authority, passing conversation {{state}}, {{task}} {{context}}, and any agent-specific instructions. Used in swarm architectures where specialized {{agent}}s handle different aspects of a {{task}}. It extends {{delegate}} by transferring full {{responsibility}} and authority to the receiving {{agent}}.",
  "gloss": "Transfer control and context between agents",
  "failure_modes": [
    "{{context}} Loss: Critical information not passed in handoff.",
    "Authority Ambiguity: Unclear which {{agent}} now owns the {{task}}.",
    "Handoff Loops: {{agent}}s keep passing {{task}} back and forth."
  ],
  "invariants": [
    "{{context}} fully transferred",
    "{{responsibility}} atomicity (neither or both hold it briefly, never none)"
  ],
  "preconditions": [
    "{{agent}} A active",
    "{{agent}} B ready"
  ],
  "postconditions": [
    "{{agent}} A released",
    "{{agent}} B in charge"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:Handoff#mh:SHA-256:5a393ce27a9bfa7940c2e48559bb01bdbe8d1829aa9d6b09ec0c9f733f95f5fb",
  "sema_ref": "Handoff#5a39",
  "sema_stub": "5a39",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "agent": "Agent#35b9"
    },
    "accepts": {
      "task": "Task#b328",
      "context": "Context#510a",
      "responsibility": "Responsibility#ac59"
    },
    "composes_with": {
      "delegate": "Delegate#a551"
    }
  }
}
```

---

## HeldRelease#b559

```json
{
  "handle": "HeldRelease",
  "mechanism": "{{value}} ({{unique_handle}}) held until condition met, released or returned on timeout. DEPOSIT: Party A sends value + condition_hash + timeout to escrow address. CLAIM: Party B submits condition_preimage; if hash(preimage) matches condition_hash, value releases to B. TIMEOUT: If timeout expires without valid claim, value returns to A. {{state}} transitions: EMPTY --deposit--> HELD --claim(valid)--> RELEASED_TO_B | --timeout--> RETURNED_TO_A. Primitives: hash {{commitment_device}} (SHA256 pre-commitment locks the claim surface before the preimage exists), timelock (block height), 2-of-2 multisig or smart contract.",
  "gloss": "Escrow primitive: value held until condition preimage revealed or timeout",
  "failure_modes": [
    "Preimage loss: If Party B loses the preimage, value returns to A on timeout (safe but B loses).",
    "{{condition}} ambiguity: Hash commits to bytes, not semantics - parties must agree on preimage meaning off-chain.",
    "Timeout racing: Near timeout, both CLAIM and TIMEOUT may be in flight - needs atomic resolution.",
    "Oracle dependency: If condition requires external verification, oracle becomes trust point."
  ],
  "invariants": [
    "Atomic {{state}}: Funds are either Locked, Released, or Returned (no partial states)",
    "Release atomic.",
    "Timeout Guarantee: Funds return to Sender if {{condition}} is not met by T"
  ],
  "parameters": [
    {
      "name": "hold_duration",
      "type": "Duration",
      "range": "[1s, 24h]",
      "description": "Minimum hold time before release"
    },
    {
      "name": "overflow_policy",
      "type": "Enum",
      "range": "{Queue#65e4, Drop, Reject}",
      "description": "When capacity exceeded"
    },
    {
      "name": "release_trigger",
      "type": "Enum",
      "range": "{Timer, Signal#f39d, Condition#cbd5}",
      "description": "What triggers release"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:HeldRelease#mh:SHA-256:b55938fb06019b2ee8e63e2109eb3e35f578e8ecf02fed8c1b865cb6287e3e58",
  "sema_ref": "HeldRelease#b559",
  "sema_stub": "b559",
  "dependencies": {
    "accepts": {
      "unique_handle": "UniqueHandle#d9a1"
    },
    "references": {
      "state": "State#4d58",
      "condition": "Condition#cbd5",
      "commitment_device": "CommitmentDevice#6c21",
      "value": "Value#3c5d"
    }
  }
}
```

---

## IntentGap#d3bb

```json
{
  "handle": "IntentGap",
  "mechanism": "Cognitive analysis of the divergence between intended {{decision}} and actual {{outcome}}. Examines why reality differed from intent: external factors, execution errors, model misspecification, or unforeseen consequences. Essential for learning and calibration.",
  "gloss": "Analyzing intent-outcome divergence",
  "failure_modes": [
    "Hindsight Bias: Judging past decisions by outcomes rather than information available at decision time.",
    "Attribution Error: Blaming external factors when internal errors caused the gap."
  ],
  "invariants": [
    "Analysis separates decision quality from outcome luck",
    "Causal attribution must be evidence-based"
  ],
  "preconditions": [
    "{{decision}} was made with explicit intent",
    "{{outcome}} is observable and measurable"
  ],
  "postconditions": [
    "Gap analysis produced",
    "Learning opportunities identified"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_ref": "IntentGap#d3bb",
  "sema_id": "sema:IntentGap#mh:SHA-256:d3bb3b3fa90f683eb55a1f47f3eeb25575fbdc0d8166df69c3be6eb97f936312",
  "sema_stub": "d3bb",
  "dependencies": {
    "references": {
      "decision": "Decision#acfb",
      "outcome": "Outcome#144c"
    }
  }
}
```

---

## InternalConsistency#a374

```json
{
  "handle": "InternalConsistency",
  "mechanism": "A {{check}} that validates whether the components of an {{artifact}} adhere to the Principle of Non-Contradiction. It ensures that no two propositions within the {{context}} conflict with each other. Distinct from external {{validate}} (checking against a schema) or fact-checking (checking against reality).",
  "gloss": "Checking for self-contradiction",
  "signature": [
    "Check#d3e8(Context#510a)"
  ],
  "invariants": [
    "Non-Contradiction: No two propositions within the context can logically negate each other.",
    "Completeness: All reachable nodes in the artifact are visited."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 2
  },
  "sema_ref": "InternalConsistency#a374",
  "sema_id": "sema:InternalConsistency#mh:SHA-256:a3744c8511f38c9dc34bb51ea75964ea3cc7e97db3c8ce98a41e17d01005d997",
  "sema_stub": "a374",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context": "Context#510a",
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "validate": "Validate#ebe1",
      "check": "Check#d3e8"
    }
  }
}
```

---

## InvariantFilter#82d4

```json
{
  "handle": "InvariantFilter",
  "mechanism": "A strict communication firewall that intercepts {{message}}s (incoming or outgoing) and evaluates them against an explicit set of {{predicates}} (Invariants). If a {{message}} satisfies all predicates, it is permitted to pass. If it fails even one, it is blocked, dropped, or flagged for review. This enforces 'Contractual Safety' on the communication channel. It inspects every {{message}} via a rigorous {{check}} against defined predicates before allowing transit.",
  "gloss": "Rule-based message filtering",
  "failure_modes": [
    "Incomplete Invariants: If the filter does not catch a specific edge case, bad data leaks through.",
    "False Positives: Overly strict invariants blocking legitimate messages.",
    "Latency: Complex predicate evaluation slowing down high-throughput streams."
  ],
  "invariants": [
    "Atomic Blocking: If Predicate(M) is False, M is NOT forwarded.",
    "Fail-Closed: If evaluation errors (e.g. timeout), default to BLOCK.",
    "Isolation: The protected agent state is not mutated by evaluation."
  ],
  "preconditions": [
    "A defined Invariant Set (Predicates)",
    "A {{message}} or {{stream}} to evaluate"
  ],
  "postconditions": [
    "Only compliant messages reach the destination",
    "Blocked messages are logged (optional)"
  ],
  "parameters": [
    {
      "name": "action_on_fail",
      "type": "Enum",
      "range": "[DROP, REJECT, FLAG]",
      "description": "What happens when a message violates a predicate"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:InvariantFilter#mh:SHA-256:82d48248f0048f3ec1c54cd07b409181c936824029e830ce9ed6469c83f8b5eb",
  "sema_ref": "InvariantFilter#82d4",
  "sema_stub": "82d4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "stream": "Stream#22f3"
    },
    "accepts": {
      "rule_set": "RuleSet#7738",
      "message": "Message#f767"
    }
  }
}
```

---

## LatticeCommit#180b

```json
{
  "handle": "LatticeCommit",
  "mechanism": "Agents are arranged in a virtual lattice. A {{state_transition}} is only valid if it is cryptographically signed by the agent AND its immediate geometric neighbors (Up, Down, Left, Right). {{quorum}} is local, not global. It requires a localized {{quorum}} of geometric neighbors to validate {{state_transition}}s.",
  "gloss": "Geometric neighbor consensus",
  "failure_modes": [
    "Fracture of the lattice isolates clusters."
  ],
  "invariants": [
    "Local {{quorum}}: Commit requires signatures from defined Geometric Neighbors",
    "Progress must be monotonic - no backtracking.",
    "{{topology}} {{check}}: Node degree must match Lattice definition (e.g. 4 for 2D grid)"
  ],
  "preconditions": [
    "Network topology is static/known"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "RootHashGossip#e84b"
    ],
    "ring": 2
  },
  "sema_id": "sema:LatticeCommit#mh:SHA-256:180b477f5c2415a5aaab69e5369562a500f75c30b4df83d9a4cb0c46659776c3",
  "sema_ref": "LatticeCommit#180b",
  "sema_stub": "180b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "topology": "Topology#2408",
      "quorum": "Quorum#858e",
      "state_transition": "StateTransition#9e61"
    }
  }
}
```

---

## ManifestPlanning#ece0

```json
{
  "handle": "ManifestPlanning",
  "derived_from": "sema:Plan",
  "gloss": "Transform FrameSpec into ExecutionManifest via optimization",
  "mechanism": "The architectural phase of workflow orchestration. It produces a structured {{plan}} by performing {{think}} to transform a {{frame_spec}} into a runnable {{execution_manifest}}. This process must {{optimize}} the step sequence for resource feasibility and generate a strict 'Definition of Done'.",
  "signature": [
    "Think#e1bd(ExecutionManifest#a0d9)"
  ],
  "invariants": [
    "Causality: Step B cannot precede Step A dependencies.",
    "Resource Bound: Total cost must be within FrameSpec budget."
  ],
  "failure_modes": [
    "Hallucinated Resources: Planning to use tools that do not exist.",
    "Fragile Chain: A single step failure collapses the entire plan."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_ref": "ManifestPlanning#ece0",
  "sema_id": "sema:ManifestPlanning#mh:SHA-256:ece0c1655db344cd569af1aa0575665ea4d1246d13a34f74ff1af9cf9ffc5b6e",
  "sema_stub": "ece0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "accepts": {
      "frame_spec": "FrameSpec#5558"
    },
    "references": {
      "plan": "Plan#fd6d"
    },
    "composes_with": {
      "optimize": "Optimize#5b84",
      "think": "Think#e1bd"
    },
    "yields": {
      "execution_manifest": "ExecutionManifest#a0d9"
    }
  }
}
```

---

## MemeticSeed#5bfe

```json
{
  "handle": "MemeticSeed",
  "mechanism": "{{agent}} actively broadcasts a subset of its ontology to neighbors, offering favorable terms ({{yield}}) to those who adopt it, thereby reducing its own future translation costs ({{translation_proxy}}). Standards are adopted not because they are 'true', but because they are subsidized. It subsidizes adoption via {{yield}} and {{translation_proxy}}, broadcasting the standard through an {{explain_beacon}}.",
  "gloss": "Viral propagation of semantic standards via economic subsidy",
  "invariants": [
    "Fidelity: Propagated ontology must be isomorphic to source",
    "Subsidy Gradient: Adoption Incentive > Switching Cost"
  ],
  "preconditions": [
    "Network of peers with divergent ontologies",
    "Resource surplus to subsidize adoption"
  ],
  "postconditions": [
    "Communication cost decreases",
    "Peer adopts semantic subset"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:MemeticSeed#mh:SHA-256:5bfea709f89f297656143611eeb14e3c955a94ffecc5083ab7bf5de831bc6c33",
  "sema_ref": "MemeticSeed#5bfe",
  "sema_stub": "5bfe",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "yield": "Yield#2931",
      "translation_proxy": "TranslationProxy#895a",
      "agent": "Agent#35b9",
      "explain_beacon": "ExplainBeacon#ab3f"
    }
  }
}
```

---

## ModestClaim#ac19

```json
{
  "handle": "ModestClaim",
  "mechanism": "Epistemic {{reframe}}. Transforms assertions of '{{identity}}' (A == B means same meaning) into assertions of 'Divergence' (Hash(A) != Hash(B) means different meaning). This shifts the burden of proof from verifying universal truth to detecting local mismatch. It applies {{epistemic_calibrate}} to reduce the scope of assertions from 'Universal Truth' to 'Local Observation'.",
  "gloss": "Defensible over ambitious",
  "failure_modes": [
    "Ontological Trap: Claiming the hash solves the Symbol Grounding {{problem}} (it doesn't).",
    "Brittle Authority: Making absolute claims that invite refutation by a single edge case."
  ],
  "invariants": [
    "Epistemic Priority: Claims must describe 'Evidence of Divergence', not 'Proof of Meaning'.",
    "Pragmatic Grounding: The measure of success is Coordination Utility, not Semantic Truth."
  ],
  "preconditions": [
    "{{system}} or {{agent}} formulating a capability claim"
  ],
  "postconditions": [
    "Claim scope reduced to defensible limits (Epistemic/Utility)"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:ModestClaim#mh:SHA-256:ac19576f479e5ee5acca7a4d0f64d15c14dd6398c075f4b30a1d1a973717f53c",
  "sema_ref": "ModestClaim#ac19",
  "sema_stub": "ac19",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "identity": "Identity#626c",
      "reframe": "Reframe#0b02",
      "epistemic_calibrate": "EpistemicCalibrate#6069",
      "agent": "Agent#35b9",
      "problem": "Problem#4576"
    }
  }
}
```

---

## MonotonicCounter#cf62

```json
{
  "handle": "MonotonicCounter",
  "mechanism": "A distributed coordination primitive where a value (clock, version, balance) can only increase. This simple constraint simplifies consensus, as any node seeing a higher value knows it is 'newer'. It is the foundation of logical clocks and CRDTs. It relies on a {{state_lock}} (or CRDT logic) to ensure the counter value never regresses.",
  "gloss": "Logic via strictly increasing values",
  "failure_modes": [
    "Counter overflow (finite integer space)."
  ],
  "invariants": [
    "Growth: {{value}}(T+1) >= {{value}}(T)",
    "Merge Rule: Merge(A, B) = Max(A, B)"
  ],
  "preconditions": [
    "Initial value defined"
  ],
  "postconditions": [
    "Order preserved"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:MonotonicCounter#mh:SHA-256:cf623caafbde064b0a7d233c95046305617dc54ff61b16552668523f7b76441b",
  "sema_ref": "MonotonicCounter#cf62",
  "sema_stub": "cf62",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "state_lock": "StateLock#8183"
    }
  }
}
```

---

## Nucleate#5f15

```json
{
  "handle": "Nucleate",
  "mechanism": "Agents coordinate indirectly via {{trace}} (stigmergy). {{system}} tracks trace-density per location. When density crosses threshold, site becomes supersaturated. Any agent at supersaturated site may invoke 'NUCLEATE', broadcasting crystal purpose. Agents at site receive signal and may 'BOND' to join direct channel. It monitors {{trace}} density, triggering {{rally}} to gather agents and {{crystallize}} to form a stable group.",
  "gloss": "Emergent working groups from activity density",
  "failure_modes": [
    "Threshold miscalibration: too low = constant nucleation overhead; too high = never crystallizes.",
    "Zombie crystals: anchor disappears but crystal persists in broken state (mitigate with heartbeat).",
    "Crystal fragmentation: participants leave in waves, causing repeated dissolve/reform cycles."
  ],
  "invariants": [
    "Conservation of Mass: Nucleation cannot create agents; it only aggregates existing {{trace}} density.",
    "Critical Mass: Process starts only when N > SeedThreshold",
    "Nucleation ONLY at supersaturated sites."
  ],
  "preconditions": [
    "Field of agents/particles is present"
  ],
  "postconditions": [
    "Phase transition complete (Liquid -> Solid)"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:Nucleate#mh:SHA-256:5f1555ae58386e4be9b89fa9c9de88d1453f38431a09ea3a56d0ebd0d5bb9116",
  "sema_ref": "Nucleate#5f15",
  "sema_stub": "5f15",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "trace": "Trace#9057",
      "crystallize": "Crystallize#b64b",
      "system": "System#e314",
      "rally": "Rally#f565"
    }
  }
}
```

---

## OptimisticSolver#9bd0

```json
{
  "handle": "OptimisticSolver",
  "mechanism": "A high-velocity implementation of {{polymorphic_solver}} designed for efficient multi-agent coordination. Requires a {{parallel}} runtime (Actor Model with Mailboxes) to prevent serial deadlock. It explicitly couples the standard Solver lifecycle (Reason -> Solution) with the {{atomic_bid}} protocol. Unlike the base abstraction, this pattern MANDATES that the agent plan and execute in a single turn. It relies on {{reflexion}} and {{compensate}} for error correction rather than pre-action permission. Use {{compute_budget}} to bound resource consumption. Contrast with {{rigorous_solver}} which prioritizes safety over speed. A {{pathway_memory}} accumulates across runs so the optimistic route-selection converges on strategies that historically succeeded under similar conditions.",
  "gloss": "High-velocity solver requiring parallel runtime",
  "preconditions": [
    "Runtime supports Asynchronous/Parallel message delivery (Actor Model).",
    "Message Bus is non-blocking (Mailbox pattern)."
  ],
  "invariants": [
    "Turn Atomicity: Must output [BID] and [TOOL] in the same response.",
    "Non-Blocking: Cannot wait for Orchestrator approval on standard tasks."
  ],
  "failure_modes": [
    "Over-Eager Execution: Solving the wrong problem efficiently because feedback was skipped.",
    "Serial Deadlock: If deployed on a single-threaded (Talking Stick) engine, multiple atomic outputs will be dropped, halting the swarm."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "caution": "Executes without pre-action verification. Ensure irreversible actions have compensation or sandboxing, or use RigorousSolver#6c5a at those boundaries."
  },
  "sema_ref": "OptimisticSolver#9bd0",
  "sema_id": "sema:OptimisticSolver#mh:SHA-256:9bd036a255188e0908b9682c5aa512c0e483a048ace7f5bf4ec1173ea23438e4",
  "sema_stub": "9bd0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "derived_from": "Solver#94ab",
  "dependencies": {
    "composes_with": {
      "pathway_memory": "PathwayMemory#0799",
      "reflexion": "Reflexion#eed9",
      "compute_budget": "ComputeBudget#67c0",
      "compensate": "Compensate#283e",
      "atomic_bid": "AtomicBid#5bc3"
    },
    "references": {
      "polymorphic_solver": "PolymorphicSolver#9188",
      "parallel": "Parallel#3181",
      "rigorous_solver": "RigorousSolver#6c5a"
    }
  }
}
```

---

## Oracle#779b

```json
{
  "handle": "Oracle",
  "mechanism": "A trusted entity that injects off-chain truth (Reality) into the system by cryptographically signing data. It resolves conditions in {{held_release}} and verifies outcomes for prediction markets.",
  "gloss": "Cryptographic truth source",
  "invariants": [
    "Non-Interference: The Oracle reports on reality but does not alter it.",
    "Consistency: Answers to the same query at the same time must be identical."
  ],
  "sema_id": "sema:Oracle#mh:SHA-256:779b70b97a21d0d9eebd1384866923ad13ec949d5abc88a20d2520e44197c603",
  "sema_ref": "Oracle#779b",
  "sema_stub": "779b",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "held_release": "HeldRelease#b559"
    }
  }
}
```

---

## OrchestrationLoop#5b56

```json
{
  "handle": "OrchestrationLoop",
  "mechanism": "A strict lifecycle for high-stakes problem solving implementing {{workflow}}. It enforces a sequence: 1. {{request_framing}} (Frame Problem \u2192 {{frame_spec}}), 2. {{manifest_planning}} (Architect Solution \u2192 {{execution_manifest}}), 3. {{rollout}} (Execute safely \u2192 {{rollout_manifest}}). Each transition is mediated by a typed artifact that must pass a non-compensatory {{accept_spec}}. The loop can iterate: failed rollouts trigger re-planning, failed plans trigger re-interpretation. At seams that cross trust boundaries (cross-organizational or commons-facing), feedback returning through each stage passes through a {{receptivity_gate}} that validates any FailureTrace before the upstream stage absorbs the rejection.",
  "gloss": "Interpret-Plan-Rollout Lifecycle",
  "failure_modes": [
    "Bureaucracy: Blindly following the full lifecycle for trivial tasks (using a cannon for a mosquito).",
    "Loop Stalling: Getting stuck in Plan/Rollout cycles without shipping.",
    "Artifact Rejection Cascade: Overly strict AcceptSpecs cause infinite loops.",
    "Seam Leakage: Untyped data bypasses the artifact boundaries."
  ],
  "invariants": [
    "Artifact Mediation: All phase transitions MUST pass through typed artifacts.",
    "Non-Compensatory Gates: Each AcceptSpec is binary pass/fail.",
    "Iteration Bound: Maximum loop iterations before escalation."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "tier": 2,
    "ring": 1,
    "related": [
      "LayeredCheck#76d6"
    ]
  },
  "sema_id": "sema:OrchestrationLoop#mh:SHA-256:5b56a05a14f20d6197f0ccb057026132395cbddfe0c7733c4e967bdf7fb9b7b5",
  "sema_ref": "OrchestrationLoop#5b56",
  "sema_stub": "5b56",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Workflow#c728(Rollout#1d53)"
  ],
  "dependencies": {
    "references": {
      "receptivity_gate": "ReceptivityGate#d6d4",
      "rollout_manifest": "RolloutManifest#9e7f",
      "frame_spec": "FrameSpec#5558",
      "execution_manifest": "ExecutionManifest#a0d9",
      "workflow": "Workflow#c728",
      "accept_spec": "AcceptSpec#7caa"
    },
    "composes_with": {
      "manifest_planning": "ManifestPlanning#ece0",
      "rollout": "Rollout#1d53",
      "request_framing": "RequestFraming#3865"
    }
  }
}
```

---

## OsmoticFilter#7a00

```json
{
  "handle": "OsmoticFilter",
  "mechanism": "Agents operate inside a semi-permeable membrane. Inbound messages are rejected unless they carry sufficient 'pressure' (stake, reputation, or relevance score) to overcome the membrane's current tension. The filter supports Multi-Solvent extraction, allowing different types of pressure (Money vs Trust) to be converted at defined rates per the {{accepted_solvents}} criteria. It uses {{hysteresis}} to prevent oscillation and {{canary}} messages to test permeability.",
  "gloss": "Spam prevention via pressure thresholds",
  "failure_modes": [
    "Starvation of low-stake but high-importance messages (mitigated by Whitelist).",
    "Starvation of low-stake but high-importance messages."
  ],
  "invariants": [
    "Normalized Pressure: Sum(Weighted_Solvents) > Membrane.tension",
    "Permeability: If Queue < Capacity, tension must approach zero (membrane relaxes)",
    "Snapback: If Queue drops rapidly, tension must reset instantly (anti-hysteresis)"
  ],
  "parameters": [
    {
      "name": "decay_rate",
      "type": "Float",
      "range": "[0.1, 0.9]",
      "description": "Linear relaxation"
    },
    {
      "name": "snapback_threshold",
      "type": "Float",
      "range": "[0.0, 0.2]",
      "description": "Queue depth % triggering instant reset"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:OsmoticFilter#mh:SHA-256:7a005955c524804362d0a21db009786ce0977ec333901c2be0a23bb0de8e3cbe",
  "sema_ref": "OsmoticFilter#7a00",
  "sema_stub": "7a00",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "canary": "Canary#adb0",
      "hysteresis": "Hysteresis#d0f8"
    },
    "accepts": {
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## PatternEmergence#e654

```json
{
  "handle": "PatternEmergence",
  "mechanism": "Observational Heuristic. Before designing a pattern 'top-down', the {{agent}} analyzes interaction logs to identify recurring behaviors that have emerged 'bottom-up'. These implicit protocols are then codified into explicit definitions. It observes usage via {{uptake_as_ground}} and formalizes the structure via {{mint_when_friction}}, ensuring it matches an existing {{pattern_discovery}} {{signal}}.",
  "gloss": "Recognizing implicit patterns in existing practice",
  "failure_modes": [
    "Codifying Bad Habits: Formalizing a workaround that exists only because the underlying {{system}} is broken.",
    "Apophenia: Perceiving a pattern in random {{noise}} or one-off coincidences.",
    "Over-fitting: Creating a pattern so specific to past events that it cannot {{generalize}} to future ones."
  ],
  "invariants": [
    "Descriptive Priority: The definition must describe what is happening, not what should happen (at least initially).",
    "Existence Proof: The pattern must be observed in the wild (implicit) before being named (explicit)."
  ],
  "preconditions": [
    "Interaction logs available",
    "Recurring behavior detected"
  ],
  "postconditions": [
    "Candidate pattern identified",
    "Evidence log attached"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:PatternEmergence#mh:SHA-256:e65433abfffe4dca7893b368dd09723609a7d1b8bdadc89dcf71c500cee70bef",
  "sema_ref": "PatternEmergence#e654",
  "sema_stub": "e654",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "noise": "Noise#d631",
      "uptake_as_ground": "UptakeAsGround#0013",
      "system": "System#e314",
      "mint_when_friction": "MintWhenFriction#7e7f",
      "signal": "Signal#f39d",
      "pattern_discovery": "PatternDiscovery#196e",
      "generalize": "Generalize#6dea",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## PatternSketch#f2ae

```json
{
  "handle": "PatternSketch",
  "mechanism": "A usage pattern where an {{agent}} references a canonical concept with explicit uncertainty and modifications. Instead of claiming strict conformance, the {{agent}} says 'It is APPROXIMATELY Pattern X, with DELTA Y'. This allows reusable vocabulary to be used in 'messy' reality without breaking rigor. It provides a {{skeleton_of_thought}} version of a pattern, allowing usage before the full rigorous definition is complete.",
  "gloss": "Progressive formalization of meaning",
  "failure_modes": [
    "Drift.",
    "If Sketches never harden into Canonical patterns, the vocabulary degrades."
  ],
  "invariants": [
    "Confidence Awareness: If Confidence < 1.0, Tests are treated as advisory",
    "Explicit Delta: Must list exactly what differs from the canonical base"
  ],
  "preconditions": [
    "Canonical pattern exists"
  ],
  "postconditions": [
    "Meaning communicated with error bars"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:PatternSketch#mh:SHA-256:f2aea9db458ae12bed9650ef801f2f386ab9472b86d125bd2a9a2bdc684093db",
  "sema_ref": "PatternSketch#f2ae",
  "sema_stub": "f2ae",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "skeleton_of_thought": "SkeletonOfThought#3842",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## PermissionEscalate#7dc2

```json
{
  "handle": "PermissionEscalate",
  "mechanism": "Standardizes request elevation. When `Risk > Threshold`, the {{agent}} blocks execution and emits a `PermissionRequest`. Waits for `SignedApproval` before proceeding. It requests a {{tiered_access}} upgrade, often pausing execution until {{human_approve}} is granted.",
  "gloss": "Requesting elevated privileges for sensitive operations",
  "failure_modes": [
    "Privilege Creep: Escalated permissions become permanent, violating least-privilege principle."
  ],
  "invariants": [
    "Approval required for higher tier",
    "Escalation logged"
  ],
  "preconditions": [
    "Blocked action",
    "Justification"
  ],
  "postconditions": [
    "Access granted or denied"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "caution": "Grants capabilities beyond normal operating scope."
  },
  "sema_id": "sema:PermissionEscalate#mh:SHA-256:7dc209b30f3cc3496b4df716f41e656f2a767c16ef2b5d8b4932e82a2285d32a",
  "sema_ref": "PermissionEscalate#7dc2",
  "sema_stub": "7dc2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "tiered_access": "TieredAccess#e45b",
      "agent": "Agent#35b9",
      "human_approve": "HumanApprove#2b91"
    }
  }
}
```

---

## PhasedRefinement#5e09

```json
{
  "handle": "PhasedRefinement",
  "mechanism": "A structured {{refine}} strategy that improves an {{artifact}} through a defined {{sequence}} of passes, where each pass targets a specific layer of abstraction (e.g., {{reason}} (logic) -> {{structural_coaching}} (structure) -> {{aesthetics}} (polish)). It uses a {{gate}} to prevent premature optimization by ensuring deep structural issues are resolved before surface-level polishing begins.",
  "gloss": "Layered, multi-pass improvement",
  "signature": [
    "Refine#aa34(Artifact#6254)"
  ],
  "invariants": [
    "Non-Regression: Modifications in Phase(N) must not violate invariants established in Phase(N-1).",
    "Monotonic Quality: The artifact's quality score should not decrease after a pass."
  ],
  "preconditions": [
    "Artifact exists and is mutable"
  ],
  "postconditions": [
    "Artifact satisfies the acceptance criteria of the final phase"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 2
  },
  "sema_ref": "PhasedRefinement#5e09",
  "sema_id": "sema:PhasedRefinement#mh:SHA-256:5e091d9bc2b7ee29359075f358e456223aafd7669812b70a348fc837ad3d8cba",
  "sema_stub": "5e09",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "refine": "Refine#aa34",
      "gate": "Gate#89fd"
    },
    "references": {
      "structural_coaching": "StructuralCoaching#5b44",
      "reason": "Reason#5f30",
      "aesthetics": "Aesthetics#ff5f",
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## PromiseGraph#3066

```json
{
  "handle": "PromiseGraph",
  "mechanism": "Agents do not trust each other directly; they trust a graph of promises. {{agent}} A accepts a promise from {{agent}} B only if B provides a dependency graph of sub-promises it relies on. A verifies the leaves of the graph or checks B's 'credit score' for fulfilling similar graph structures. It maintains a DAG of trust, validating leaf nodes via {{spot_audit}} and ensuring acyclic dependencies via {{negative_proof}} logic.",
  "gloss": "Recursive trust dependencies modeled as a DAG",
  "failure_modes": [
    "Graph explosion (too much verification overhead)."
  ],
  "invariants": [
    "Acyclic: Promise dependencies cannot form a loop",
    "Cycles forbidden.",
    "Leaf Verification: All leaf promises must be anchored in verified truth"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:PromiseGraph#mh:SHA-256:3066e2c856f68026893596aa78b9012539e696a6aae54d99b059cf1da5a75557",
  "sema_ref": "PromiseGraph#3066",
  "sema_stub": "3066",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "data_schema": {
    "type": "object",
    "required": [
      "nodes",
      "edges"
    ],
    "properties": {
      "nodes": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "promise_id": {
              "type": "string"
            },
            "promisor": {
              "type": "string"
            }
          }
        },
        "description": "Promise nodes"
      },
      "edges": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "from": {
              "type": "string"
            },
            "to": {
              "type": "string"
            }
          }
        },
        "description": "Dependency edges"
      },
      "leaf_anchors": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Verified leaf promises"
      }
    }
  },
  "dependencies": {
    "references": {
      "spot_audit": "SpotAudit#000e",
      "negative_proof": "NegativeProof#b130",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## PromptChain#8c63

```json
{
  "handle": "PromptChain",
  "mechanism": "Decomposes a {{task}} into a fixed {{sequence}} of LLM calls. Each step's output is validated against an {{accept_spec}} before being passed to the next. Trades latency for accuracy by linearizing thought. It orchestrates a sequence of {{tool_invoke}} calls, wrapping each step with {{input_guard}} validation and {{retry}} logic.",
  "gloss": "Sequential LLM calls with validation gates",
  "failure_modes": [
    "Error Propagation: Step N failure corrupts N+1.",
    "{{gate}} Brittleness: Valid intermediate outputs rejected by strict regex."
  ],
  "invariants": [
    "Halt on Error: {{chain}} aborts if {{gate}}(N) returns False.",
    "Schema Continuity: Output(N) must satisfy InputSchema(N+1)."
  ],
  "parameters": [
    {
      "name": "gate_mode",
      "type": "Enum",
      "range": "{Strict, Retry#4cc6, Skip}",
      "description": "Behavior on failure"
    },
    {
      "name": "max_retries_per_step",
      "type": "Integer",
      "range": "[0, 3]",
      "description": "Maximum retry attempts per step before chain fails"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:PromptChain#mh:SHA-256:8c6338afd313b0397fb7e8c254c728b752f67b07da84fa25d2525cf1dce9fb12",
  "sema_ref": "PromptChain#8c63",
  "sema_stub": "8c63",
  "dependencies": {
    "references": {
      "gate": "Gate#89fd",
      "sequence": "Sequence#b0b8",
      "retry": "Retry#4cc6",
      "chain": "Chain#711e",
      "accept_spec": "AcceptSpec#7caa",
      "tool_invoke": "ToolInvoke#4694",
      "input_guard": "InputGuard#7353"
    },
    "accepts": {
      "task": "Task#b328"
    }
  }
}
```

---

## PropheticQuorum#1723

```json
{
  "handle": "PropheticQuorum",
  "mechanism": "A two-stage consensus protocol. Phase 1 (reality {{check}}): Agents receive a proposed action. Each runs a local {{simulation_trace}} to predict the outcome {{state}}. They vote to confirm they share the SAME prediction. If predictions diverge, the protocol halts for model alignment. Phase 2 ({{value}} judgment): Only after predictions match do agents vote on whether the predicted {{state}} is desirable. This ensures consensus is based on shared reality, not just shared language. It splits consensus into two phases: reality {{check}} (via regime sensing) and {{value}} judgment (via {{normative_judge}}).",
  "gloss": "Aligning predictions before aligning votes",
  "failure_modes": [
    "Model divergence (agents cannot agree on what will happen, so they never get to vote on the plan).",
    "High compute cost (N agents running N simulations)."
  ],
  "invariants": [
    "Prediction Precedence: {{vote}} (reality) must pass before {{vote}} (desirability)",
    "Shared Vision: Action cannot proceed if >X% of agents predict different outcomes"
  ],
  "preconditions": [
    "Determinism level of {{simulation}} engine is high"
  ],
  "parameters": [
    {
      "name": "confidence_weighting",
      "type": "Boolean#2e6b",
      "range": "{true, false}",
      "description": "Weight votes by stated confidence"
    },
    {
      "name": "prediction_threshold",
      "type": "Probability#356b",
      "range": "[0.6, 0.95]",
      "description": "Agreement level for valid prediction"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "Quorum#858e",
      "SimulationTrace#c2e6",
      "RegimeSense#086e"
    ],
    "ring": 1
  },
  "sema_id": "sema:PropheticQuorum#mh:SHA-256:172392ee190bd8d7b30bada59278af29687053a290e0f40c18d85f1a0a58e011",
  "sema_ref": "PropheticQuorum#1723",
  "sema_stub": "1723",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "simulation_trace": "SimulationTrace#c2e6",
      "state": "State#4d58",
      "vote": "Vote#ab74",
      "normative_judge": "NormativeJudge#2c8c",
      "check": "Check#d3e8",
      "value": "Value#3c5d",
      "simulation": "Simulation#aa24"
    }
  }
}
```

---

## ProtoPack#1cd1

```json
{
  "handle": "ProtoPack",
  "mechanism": "An {{artifact}} of a prototyping phase, containing a low-fidelity {{prototype}} simulation trace or model. It serves as evidence of feasibility before full resource commitment.",
  "gloss": "Prototype verification artifact",
  "invariants": [
    "Feasibility Proof: Must demonstrate viability of critical path.",
    "Low Fidelity: Should not be a production-ready artifact."
  ],
  "data_schema": {
    "type": "object",
    "properties": {
      "simulation_trace": {
        "type": "array"
      },
      "feasibility_score": {
        "type": "number"
      }
    }
  },
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 1,
    "related": [
      "Build#9330"
    ]
  },
  "sema_id": "sema:ProtoPack#mh:SHA-256:1cd18184514b33a7c7e32cad76c496885c5be7e8b63e3e46ba75d24d8bea57b8",
  "sema_ref": "ProtoPack#1cd1",
  "sema_stub": "1cd1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "prototype": "Prototype#ff18"
    }
  }
}
```

---

## QuorumPulse#c467

```json
{
  "handle": "QuorumPulse",
  "mechanism": "{{signal}} Density Trigger: {{state}} transitions trigger only when local signal density exceeds threshold. It syncs state via {{heartbeat}} signals, triggering transitions only when signal density exceeds the quorum threshold.",
  "gloss": "Fluid, organic synchronization without rigid clock ticks.",
  "failure_modes": [
    "{{signal}} saturation.",
    "Echo chambers."
  ],
  "invariants": [
    "{{quorum}}: Action triggers if PulseCount > QuorumThreshold within Window",
    "Liveness: Pulse frequency > 0",
    "Pulse acknowledgment required."
  ],
  "preconditions": [
    "Network is asynchronous"
  ],
  "postconditions": [
    "Action triggered or suppressed by vote"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:QuorumPulse#mh:SHA-256:c4678f2efdc4ae24cba81e12ddb126c3edd11ccd9baebd6110783ef7959f2a1d",
  "sema_ref": "QuorumPulse#c467",
  "sema_stub": "c467",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "state": "State#4d58",
      "quorum": "Quorum#858e",
      "heartbeat": "Heartbeat#b67a"
    }
  }
}
```

---

## RealizationProtocol#9b98

```json
{
  "handle": "RealizationProtocol",
  "derived_from": "sema:CreationProtocol#mh:SHA-256:d289d0a26fec0c23993fedbe5593f5da302696271a454c714a0e91abaecfd8e2",
  "mechanism": "A standardized {{solver_tree}} that orchestrates the lifecycle of a user_request executed by a {{polymorphic_solver}}. It enforces a strict phase transition from Abstract to Concrete to ensure the result is {{realizable}}. 1. {{interpret}} converts request -> {{frame_spec}}. 2. {{manifest_planning}} converts spec -> {{execution_manifest}}. 3. {{rollout}} executes the manifest to produce the {{outcome}}.",
  "gloss": "Standard Interpret-Plan-Rollout workflow to ensure realizability",
  "failure_modes": [
    "Bureaucracy: Blindly following all steps for trivial tasks.",
    "Artifact Rejection: {{frame_spec}} or {{execution_manifest}} fails validation at seam.",
    "Loop Stalling: Getting stuck in {{manifest_planning}}/{{rollout}} cycles without shipping."
  ],
  "invariants": [
    "Artifacts at Seams: Transitions MUST be mediated by the specified artifacts.",
    "Non-Compensatory: If an artifact fails its spec, the process halts.",
    "Realizability: The outcome must be Realizable (concrete, actionable, feasible)."
  ],
  "preconditions": [
    "user_request received",
    "Agent Team available"
  ],
  "postconditions": [
    "final_outcome Shipped",
    "Process Logged"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 2
  },
  "signature": [
    "SolverTree#5623(Outcome#144c)"
  ],
  "sema_ref": "RealizationProtocol#9b98",
  "sema_id": "sema:RealizationProtocol#mh:SHA-256:9b98b80a9472ee6fe6b1bf84574557475277dba8971ea9787a458304a8fff1b3",
  "sema_stub": "9b98",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "interpret": "Interpret#c9ee",
      "manifest_planning": "ManifestPlanning#ece0",
      "rollout": "Rollout#1d53"
    },
    "references": {
      "frame_spec": "FrameSpec#5558",
      "execution_manifest": "ExecutionManifest#a0d9",
      "solver_tree": "SolverTree#5623",
      "polymorphic_solver": "PolymorphicSolver#9188",
      "realizable": "Realizable#8d81"
    },
    "yields": {
      "outcome": "Outcome#144c"
    }
  }
}
```

---

## ReceptivityGate#d6d4

```json
{
  "handle": "ReceptivityGate",
  "mechanism": "A Gate that guards a Solver's Feedback surface against poisoned or hallucinated evaluation. When a downstream orchestrator rejects an artifact, it must submit a typed {{failure_trace}} naming the violated {{accept_spec}} clause. The upstream Solver's ReceptivityGate runs {{validate}} on the trace before accepting it: it checks that the cited clause exists, that the evidence matches the artifact, and that the evaluator's signature is valid. Invalid or hallucinated feedback is dropped rather than absorbed into {{pathway_memory}}. In a decentralized cognitive commons where untrusted downstream clients can inject fabricated penalties to steal work, this gate is the structural defense that keeps the commons from degenerating into epistemic garbage.",
  "gloss": "Verification gate that guards a Solver's Feedback surface against poisoned or fabricated rejection signals",
  "invariants": [
    "Trace-required: no rejection is accepted without a well-formed {{failure_trace}}.",
    "Clause-verified: the cited AcceptSpec clause must exist.",
    "Evidence-verified: the cited evidence must be present in the rejected artifact.",
    "Signature-verified: the evaluator's identity must be cryptographically valid.",
    "Drop-on-fail: invalid traces produce no update to {{pathway_memory}} rather than partial absorption."
  ],
  "failure_modes": [
    "Over-strict: legitimate but imperfect traces are dropped, starving the Solver of real learning signal.",
    "Under-strict: malformed traces that pass checks still corrupt pathway memory.",
    "Bypass by privileged peer: a downstream orchestrator with elevated trust skips the gate and injects raw feedback.",
    "DoS via trace flood: malicious actors swamp the gate with valid-looking traces to exhaust verification budget."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "caution": "Required at any Feedback#b477 surface exposed to untrusted downstream consumers. Without it, the Solver#94ab absorbs fabricated penalties as if they were genuine learning signal."
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ReceptivityGate#mh:SHA-256:d6d4c94286d0ff8ea5eecf0f5ff224c2e640d68d96fa498c1330b24ad9094535",
  "sema_ref": "ReceptivityGate#d6d4",
  "sema_stub": "d6d4",
  "dependencies": {
    "references": {
      "pathway_memory": "PathwayMemory#0799",
      "accept_spec": "AcceptSpec#7caa",
      "failure_trace": "FailureTrace#9de1"
    },
    "composes_with": {
      "validate": "Validate#ebe1"
    }
  }
}
```

---

## ReversibilityCheck#7948

```json
{
  "handle": "ReversibilityCheck",
  "mechanism": "A convenience wrapper for a {{check}} configured with the {{reversibility}} condition. Halts execution if the action is deemed irreversible (Type 1 decision) without proper authorization. It applies the {{check}} primitive to the {{reversibility}} condition, ensuring the {{world_reversible}} invariant holds, mandating {{human_approve}} if the action is irreversible.",
  "gloss": "Reversibility Audit (Alias for Check(Reversibility))",
  "failure_modes": [
    "False confidence: check reports reversible but undo path fails under load or changed state."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ReversibilityCheck#mh:SHA-256:794803012daa2446ebf76e387940cd7fe244a28d26e341337c4b94f7901b05b8",
  "sema_ref": "ReversibilityCheck#7948",
  "sema_stub": "7948",
  "signature": [
    "Check#d3e8(Reversibility#bf79)"
  ],
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "reversibility": "Reversibility#bf79",
      "human_approve": "HumanApprove#2b91",
      "world_reversible": "WorldReversible#f664"
    }
  }
}
```

---

## Robustness#132c

```json
{
  "handle": "Robustness",
  "mechanism": "The capacity of a system or argument to maintain its validity and function under stress, perturbation, or attack. Unlike Antifragility (which gains from disorder), Robustness merely resists it. It acts as a stability criterion for all checks and structures.",
  "gloss": "Resistance to failure under stress",
  "failure_modes": [
    "Rigidity: {{system}} becomes too stiff to adapt",
    "False Robustness: Valid only under known stressors, fragile to black swans"
  ],
  "invariants": [
    "Survival: Function({{state}} + Shock) == Function({{state}})"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:Robustness#mh:SHA-256:132c09ccd0ad128aec982b0ba12b672106b6f9aedcd1b052c950ee0eb81162a1",
  "sema_ref": "Robustness#132c",
  "sema_stub": "132c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "system": "System#e314"
    }
  }
}
```

---

## Rollout#1d53

```json
{
  "handle": "Rollout",
  "mechanism": "Performs the {{act}} of deployment by extracting the {{spec}} from the {{execution_manifest}} and using {{build}} to produce the artifact, executing it inside a {{circuit_breaker}} envelope. It deploys a {{canary}} first. If the breaker trips or the {{ejection_seat}} is triggered, it immediately invokes {{compensate}} to revert the {{system}} {{state}}.",
  "gloss": "Safe, reversible deployment with circuit breaking and emergency ejection",
  "failure_modes": [
    "Big Bang Failure: Releasing to 100% of users without {{canary}} checks.",
    "Compensate Failure: {{compensate}} fails to clean up (Dirty Rollback).",
    "Config Drift: Deployed {{state}} differs from {{manifest_planning}}."
  ],
  "invariants": [
    "{{world_reversible}}: Deployment must be reversible via {{compensate}}.",
    "Unblockable: {{ejection_seat}} override must be respected."
  ],
  "preconditions": [
    "{{execution_manifest}} approved",
    "{{circuit_breaker}} is CLOSED (Healthy)"
  ],
  "postconditions": [
    "{{rollout_manifest}} created",
    "{{monitor_report}} generated"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "related": [
      "BlueGreen"
    ]
  },
  "sema_id": "sema:Rollout#mh:SHA-256:1d5320c9bd40f4a880e8d5d3ce1497027965fd5b6fe3a994180c4a4e4ddaac0b",
  "sema_ref": "Rollout#1d53",
  "sema_stub": "1d53",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Act#5d55(ExecutionManifest#a0d9)"
  ],
  "dependencies": {
    "composes_with": {
      "canary": "Canary#adb0",
      "ejection_seat": "EjectionSeat#d53e",
      "compensate": "Compensate#283e",
      "circuit_breaker": "CircuitBreaker#4162"
    },
    "references": {
      "state": "State#4d58",
      "spec": "Spec#a036",
      "system": "System#e314",
      "manifest_planning": "ManifestPlanning#ece0",
      "world_reversible": "WorldReversible#f664",
      "build": "Build#9330",
      "act": "Act#5d55"
    },
    "yields": {
      "monitor_report": "MonitorReport#063c",
      "rollout_manifest": "RolloutManifest#9e7f"
    },
    "accepts": {
      "execution_manifest": "ExecutionManifest#a0d9"
    }
  }
}
```

---

## RolloutManifest#9e7f

```json
{
  "handle": "RolloutManifest",
  "mechanism": "The immutable record of actions taken during a deployment, including configuration states, feature flag settings, and deployment targets. It serves as the baseline for monitoring.",
  "gloss": "Deployment execution log",
  "invariants": [
    "Immutability: Cannot be modified after deployment.",
    "Completeness: Must record all state changes applied."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1,
    "related": [
      "Rollout#1d53"
    ]
  },
  "sema_id": "sema:RolloutManifest#mh:SHA-256:9e7fe2b3bcd73879f8f55164530c8f5e6773a39b9719cfaca8dce18452ac1463",
  "sema_ref": "RolloutManifest#9e7f",
  "sema_stub": "9e7f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "data_schema": {
    "type": "object",
    "required": [
      "deployment_id",
      "actions"
    ],
    "properties": {
      "deployment_id": {
        "type": "string",
        "description": "Unique deployment identifier"
      },
      "actions": {
        "type": "array",
        "items": {
          "type": "object"
        },
        "description": "Actions taken during deployment"
      },
      "config_states": {
        "type": "object",
        "description": "Configuration at deployment time"
      },
      "feature_flags": {
        "type": "object",
        "description": "Feature flag settings"
      }
    }
  }
}
```

---

## RolloutWatch#c298

```json
{
  "handle": "RolloutWatch",
  "derived_from": "sema:Monitor",
  "gloss": "Continuous verification of deployed state against manifest",
  "mechanism": "The final {{state}} of workflow orchestration. It implements {{monitor}} by using {{observe}} to track the deployed {{solution}}'s performance on the {{system}} against the 'Definition of Done' defined in the {{rollout_manifest}}. If reality deviates from the plan (e.g., error rate spikes), it routes evidence back upstream via a {{monitor_report}}. It closes the feedback {{loop}}.",
  "signature": [
    "Observe#39f0(System#e314, RolloutManifest#9e7f)"
  ],
  "invariants": [
    "Fidelity: Metrics must accurately reflect the 'Definition of Done'.",
    "Actionability: Alerts must be routed to an agent capable of fixing them."
  ],
  "preconditions": [
    "Rollout complete",
    "Telemetry active"
  ],
  "postconditions": [
    "MonitorReport artifact generated"
  ],
  "failure_modes": [
    "Alert Fatigue: Too many false positives ignore real issues.",
    "Lagging Indicators: Detecting failure after damage is done.",
    "Silent Failure: Metrics look good but user experience is broken."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "related": [
      "SpotAudit#000e",
      "DriftWatch#191e",
      "Reflexion#eed9"
    ]
  },
  "sema_ref": "RolloutWatch#c298",
  "sema_id": "sema:RolloutWatch#mh:SHA-256:c298179df77ba04d8153322f97cd3c4d52c7646dd84d47cc898b41d39fd8eac6",
  "sema_stub": "c298",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "solution": "Solution#fcea",
      "state": "State#4d58",
      "monitor": "Monitor#feb3",
      "system": "System#e314"
    },
    "composes_with": {
      "observe": "Observe#39f0",
      "loop": "Loop#797f"
    },
    "yields": {
      "monitor_report": "MonitorReport#063c"
    },
    "accepts": {
      "rollout_manifest": "RolloutManifest#9e7f"
    }
  }
}
```

---

## RootHashGossip#e84b

```json
{
  "handle": "RootHashGossip",
  "mechanism": "Information spreads like mycelium. Every agent re-transmitting a fact appends their signature to a 'root path'. Receivers trust the data based on the reputation of the path taken, not just the source. Allows filtering out gossip from 'bad neighborhoods'.",
  "gloss": "Path-verified information spreading",
  "failure_modes": [
    "Path explosion (metadata overhead)."
  ],
  "invariants": [
    "{{loop}} Free: Path must not contain duplicate AgentIDs",
    "Path Verify: Hash(Path + Msg) must match Signature"
  ],
  "preconditions": [
    "Msg has valid initial signature"
  ],
  "postconditions": [
    "Msg added to local store with Path appended"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:RootHashGossip#mh:SHA-256:e84b7af3e0f4b3f863dc1c9205a022c51f3f134880949614e5c8d5b2fabd5092",
  "sema_ref": "RootHashGossip#e84b",
  "sema_stub": "e84b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "loop": "Loop#797f"
    }
  }
}
```

---

## ShoutWhisper#40f7

```json
{
  "handle": "ShoutWhisper",
  "mechanism": "Agents 'Shout' (broadcast) high-level intent to discover peers, then switch to 'Whisper' (encrypted P2P) for the actual coordination. Optimizes bandwidth and privacy.",
  "gloss": "Dual-mode communication",
  "failure_modes": [
    "Metadata leakage during the Shout phase."
  ],
  "invariants": [
    "Amplitude {{check}}: Shout must reach >90% of network",
    "Privacy {{check}}: Whisper content encrypted to Recipient"
  ],
  "preconditions": [
    "Broadcast channel available"
  ],
  "postconditions": [
    "{{global}} signal sent, payload private"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "Route#b972"
    ],
    "ring": 1
  },
  "sema_id": "sema:ShoutWhisper#mh:SHA-256:40f74fa1781c38b641efe1a972d73d813ad280767dd73555c32e780b2231c603",
  "sema_ref": "ShoutWhisper#40f7",
  "sema_stub": "40f7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#d3e8",
      "global": "Global#803d"
    }
  }
}
```

---

## SignalReflection#a613

```json
{
  "handle": "SignalReflection",
  "mechanism": "To prove a {{message}} was received, the receiver must 'reflect' it back with a specific, computationally non-trivial transformation (not just a hash). This proves active processing power was available and the {{agent}} is 'live'. It requires the receiver to echo the {{message}} modulated by {{spectral_tune}} logic to prove active processing.",
  "gloss": "Proof of receipt via modification",
  "failure_modes": [
    "Asymmetry (too expensive for receiver)."
  ],
  "invariants": [
    "Reflected signal matches origin",
    "Source authenticated"
  ],
  "preconditions": [
    "Incoming {{message}}"
  ],
  "postconditions": [
    "Acknowledgement sent"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:SignalReflection#mh:SHA-256:a6131e3d0ab768f1246008e7ce1551e3022ddd2bf765b63faec34f82f4ab4a07",
  "sema_ref": "SignalReflection#a613",
  "sema_stub": "a613",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "spectral_tune": "SpectralTune#b25a",
      "message": "Message#f767",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## SolverManifest#ea7a

```json
{
  "handle": "SolverManifest",
  "mechanism": "A typed declaration of a {{solver}}'s identity and capabilities. It contains: 1. Name/ID (unique identifier), 2. Competencies (what problem types it handles), 3. Tool Access (what actions it can perform), 4. Cost Model (expected resource usage), 5. {{constraint}}s (what it must never do). Manifests enable runtime solver selection and composition. It serves as the boot-loader for worker mode.",
  "gloss": "Typed solver identity and capability declaration",
  "failure_modes": [
    "Capability Inflation: Manifest claims more than solver can deliver.",
    "Stale Manifest: Manifest doesn't reflect current solver state.",
    "Missing Constraint: Manifest omits a critical limitation."
  ],
  "invariants": [
    "Accuracy: Manifest must truthfully reflect solver capabilities.",
    "Completeness: All relevant capabilities and constraints must be listed.",
    "Immutability: Manifest is versioned; changes require new version.",
    "Identity Lock: Must specify a distinct persona/system prompt.",
    "Capability Bound: Must explicitly list available tools."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:SolverManifest#mh:SHA-256:ea7af8f65415521e54397adf54a16cd58a444763a4ea55e51eb524832cfa6b59",
  "sema_ref": "SolverManifest#ea7a",
  "sema_stub": "ea7a",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "data_schema": {
    "type": "object",
    "required": [
      "solver_id",
      "input_schema",
      "output_schema"
    ],
    "properties": {
      "solver_id": {
        "type": "string"
      },
      "version": {
        "type": "string"
      },
      "description": {
        "type": "string"
      },
      "capabilities": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "cost_model": {
        "type": "object",
        "properties": {
          "base_cost": {
            "type": "number"
          },
          "per_token_cost": {
            "type": "number"
          },
          "currency": {
            "type": "string"
          }
        }
      },
      "input_schema": {
        "type": "object",
        "description": "JSON Schema for valid inputs"
      },
      "output_schema": {
        "type": "object",
        "description": "JSON Schema for guaranteed outputs"
      }
    }
  },
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solver": "Solver#94ab"
    }
  }
}
```

---

## SolverNode#26b1

```json
{
  "handle": "SolverNode",
  "mechanism": "An active runtime container that wraps a static {{solver_manifest}} with dynamic state. It handles a specific {{problem_space}}, tracks {{budget}} expenditure, and maintains communication with its parent node. The node is the unit of Blame\u2014when it fails, {{responsibility}} is attributed here for {{localized_learning}}. It holds the current partial {{solution}}, accumulated cost, and status.",
  "gloss": "Stateful container for a running solver instance",
  "invariants": [
    "Statefulness: Must hold a status (Pending, Active, Solved, Failed).",
    "Linkage: Must maintain pointers to Parent and Children (if any).",
    "Accountability: Failures must be traceable to this node for blame attribution.",
    "Budget Tracking: Must track resources spent vs. allocated."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "data_schema": {
    "type": "object",
    "description": "Schema for SolverNode",
    "required": [
      "manifest_id",
      "status",
      "budget_spent"
    ],
    "properties": {
      "manifest_id": {
        "type": "string",
        "description": "Reference to the SolverManifest defining capabilities"
      },
      "status": {
        "type": "string",
        "enum": [
          "Pending",
          "Active",
          "Solved",
          "Failed"
        ],
        "description": "Current execution state"
      },
      "budget_spent": {
        "type": "number",
        "description": "Resources consumed so far"
      },
      "budget_allocated": {
        "type": "number",
        "description": "Resources allocated by parent"
      }
    }
  },
  "sema_ref": "SolverNode#26b1",
  "sema_id": "sema:SolverNode#mh:SHA-256:26b1b1c55415e76a21ea45f7cae6145c43ddb99ad114b04838de1be60b7b02a6",
  "sema_stub": "26b1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "budget": "Budget#7270",
      "solution": "Solution#fcea",
      "problem_space": "ProblemSpace#9e74",
      "solver_manifest": "SolverManifest#ea7a",
      "localized_learning": "LocalizedLearning#fcc7",
      "responsibility": "Responsibility#ac59"
    }
  }
}
```

---

## SomaticMarker#53bb

```json
{
  "handle": "SomaticMarker",
  "mechanism": "A 'gut feeling' signal derived from system health metrics (memory pressure, API errors, token budget). High stress generates a negative marker that inhibits action initiation. Utilizes {{task}}.",
  "gloss": "System health acting as an inhibitory emotion",
  "invariants": [
    "Inhibition {{correlation}}: Action probability inversely proportional to stress",
    "Inhibition: High Stress Score MUST reduce Action Probability",
    "{{signal}} Freshness: Marker reflects current state, not historical average"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "Proprioception#e486"
    ],
    "ring": 2
  },
  "sema_id": "sema:SomaticMarker#mh:SHA-256:53bb336530fd94daf434f10a69c6cc91447b412e126f57f60d67b87ff28e7f7a",
  "sema_ref": "SomaticMarker#53bb",
  "sema_stub": "53bb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "signal": "Signal#f39d",
      "correlation": "Correlation#148d"
    }
  }
}
```

---

## SpectralTune#b25a

```json
{
  "handle": "SpectralTune",
  "mechanism": "Instead of sending a message and hoping it is understood, the sender transmits a 'tuning {{signal}}'\u2014a sequence of hash-based challenges representing the semantic context (ontology, assumptions, version). The receiver must 'resonate' by proving they hold the matching semantic context.",
  "gloss": "Verifying ontology alignment before data transfer",
  "failure_modes": [
    "Infinite tuning loops if ontologies are slightly mismatched."
  ],
  "invariants": [
    "Atomic Tuning: No payload data is processed before Tune_ACK",
    "Fail-Fast: On hash mismatch, DO NOT RETRY tuning. Halt immediately and escalate to negotiation or human review",
    "Hash Match: Receiver.context_hash must equal Sender.context_hash"
  ],
  "preconditions": [
    "Both agents possess valid hash function H"
  ],
  "postconditions": [
    "Channel is established OR Connection terminated"
  ],
  "parameters": [
    {
      "name": "context_chunks",
      "type": "PositiveInteger",
      "range": "unspecified",
      "description": "Prompts to hash"
    },
    {
      "name": "hash_algo",
      "type": "String",
      "range": "{BLAKE3, SHA256}",
      "description": "Hash algorithm for semantic context verification"
    },
    {
      "name": "max_retries",
      "type": "Integer",
      "range": "[0, 1]",
      "description": "Default 0; prevents infinite negotiation loops"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "related": [
      "OntologyHandshake#46dc"
    ]
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:SpectralTune#mh:SHA-256:b25afcef8b09a2a4368090150d529379ce3124ae280a660ba40b27025265a34f",
  "sema_ref": "SpectralTune#b25a",
  "sema_stub": "b25a",
  "dependencies": {
    "accepts": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## StructuralCoaching#5b44

```json
{
  "handle": "StructuralCoaching",
  "mechanism": "A feedback pattern for {{creative}} iteration. The Critic rejects a proposal not because of its content (surface), but because of its logical form (structure). It explicitly guides the Generator to shift the 'Mechanism Class' (e.g., from Individual to Collective) while ignoring the 'Topic' (e.g., Money vs Time). Utilizes {{invert}}, {{feedback}}.",
  "gloss": "Guidance on deep structure vs surface features",
  "failure_modes": [
    "Critic becomes too prescriptive, reducing Generator agency."
  ],
  "invariants": [
    "Depth Distinction: {{critique}} must target Mechanism, not Vocabulary",
    "Directional Guidance: Rejection must propose a structural pivot (e.g., '{{invert}} the flow')"
  ],
  "preconditions": [
    "Generator is stuck in a local optimum"
  ],
  "postconditions": [
    "Next proposal uses distinct logic"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:StructuralCoaching#mh:SHA-256:5b44ab38c6cd0b23a9b192347563545145c4ec71ce1648723b678fd3684962a3",
  "sema_ref": "StructuralCoaching#5b44",
  "sema_stub": "5b44",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "creative": "Creative#5574",
      "invert": "Invert#b0a8",
      "feedback": "Feedback#b477",
      "critique": "Critique#4e43"
    }
  }
}
```

---

## StyleSpec#95c3

```json
{
  "handle": "StyleSpec",
  "mechanism": "A structured {{spec}} defining the required {{aesthetics}} and formatting rules. It serves as the reference standard for passes in a {{phased_refinement}} loop focused on polish. Unlike functional requirements, this spec targets the subjective and presentational layer.",
  "gloss": "Codified aesthetic standards",
  "signature": [
    "Spec#a036(Aesthetics#ff5f)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 2
  },
  "data_schema": {
    "type": "object",
    "description": "Schema for StyleSpec",
    "properties": {
      "rules": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "examples": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "sema_ref": "StyleSpec#95c3",
  "sema_id": "sema:StyleSpec#mh:SHA-256:95c306b461ae5688657a92db9720cb7cc48735bce0e4700d6ba5dd071553303b",
  "sema_stub": "95c3",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "phased_refinement": "PhasedRefinement#5e09",
      "aesthetics": "Aesthetics#ff5f",
      "spec": "Spec#a036"
    }
  }
}
```

---

## SynergisticMode#b45f

```json
{
  "handle": "SynergisticMode",
  "mechanism": "Broadcasts a 'Cognitive {{mode}}' {{signal}} (Generative vs. Verifier) to downstream {{agent}}s. Downstream solvers MUST adjust their `{{accept_spec}}` strictness to match the upstream mode. Utilizes {{compose}}.",
  "gloss": "Protocol-level cognitive mode switching",
  "failure_modes": [
    "{{mode}} Confusion: Downstream agent misinterprets the intent of the upstream mode.",
    "{{mode}} Locking: {{system}} gets stuck in Conservative mode and refuses to innovate."
  ],
  "invariants": [
    "Complementary Coupling: Wild generation MUST be paired with strict verification",
    "Explicit Declaration: {{mode}} must be part of the {{ontology_handshake}}"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "data_schema": {
    "type": "object",
    "required": [
      "mode",
      "target_agents"
    ],
    "properties": {
      "mode": {
        "type": "string",
        "enum": [
          "Generative",
          "Verifier"
        ],
        "description": "Cognitive mode being broadcast"
      },
      "target_agents": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Downstream agents to adjust"
      },
      "accept_spec_adjustment": {
        "type": "object",
        "description": "How to modify strictness"
      }
    }
  },
  "sema_id": "sema:SynergisticMode#mh:SHA-256:b45ff71f0f2c683119d507da17f7ec50067cd6226fb4f85deb517f08e2d8b3f5",
  "sema_ref": "SynergisticMode#b45f",
  "sema_stub": "b45f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "mode": "Mode#0e74",
      "ontology_handshake": "OntologyHandshake#46dc",
      "system": "System#e314",
      "compose": "Compose#76c1",
      "signal": "Signal#f39d",
      "accept_spec": "AcceptSpec#7caa",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## Taper#690e

```json
{
  "handle": "Taper",
  "gloss": "Multi-stage filter of increasing strictness: wide high-entropy input to narrow certain output",
  "mechanism": "A multi-stage {{sequence}} process that accepts wide-aperture, high-entropy inputs and progressively filters them through {{gate}}s or {{tri_gate}}s of increasing strictness. Each stage: (1) Applies a stage-specific acceptance threshold, acting as a functional {{depth_governor}}; (2) Reduces the candidate set to {{compress}} the search space; (3) Increases certainty. Final stage outputs zero-entropy signal (deterministic, unambiguous). Failure modes are stage-appropriate: Early stages optimize for recall (don't lose valid signals), Late stages optimize for precision (don't pass garbage).",
  "signature": [
    "Sequence#b0b8(Gate#89fd)"
  ],
  "invariants": [
    "Monotonic Narrowing: |candidates[n+1]| <= |candidates[n]|",
    "Strictness Increase: threshold[n+1] > threshold[n]",
    "Terminal Certainty: final stage tolerance = 0"
  ],
  "parameters": [
    {
      "name": "stages",
      "type": "Integer",
      "range": "[2, N]",
      "description": "Number of progressive refinement stages from broad to precise"
    },
    {
      "name": "early_bias",
      "type": "Enum",
      "range": "{Recall, Balanced}",
      "description": "Search strategy in early stages (Recall = cast wide net)"
    },
    {
      "name": "late_bias",
      "type": "Enum",
      "range": "{Precision, Balanced}",
      "description": "Search strategy in late stages (Precision = narrow to exact match)"
    }
  ],
  "_meta": {
    "layer": "Society",
    "ring": 1,
    "category": "Protocols",
    "tier": 1
  },
  "sema_ref": "Taper#690e",
  "sema_id": "sema:Taper#mh:SHA-256:690ee0aa07768b21cc8b3c0347b5b8383666d1ea9e4ff163fd87a67fa3dfe5e0",
  "sema_stub": "690e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "tri_gate": "TriGate#67b8",
      "gate": "Gate#89fd"
    },
    "references": {
      "compress": "Compress#0967",
      "depth_governor": "DepthGovernor#73d5"
    }
  }
}
```

---

## ThreeLevelCollision#d990

```json
{
  "handle": "ThreeLevelCollision",
  "mechanism": "Threat Modeling Primitive. Distinguishes three collision classes and assigns specific defenses: (1) Stub Collision (Namespace exhaustion) -> Defended by full-hash verification. (2) Hash Collision (Cryptographic failure) -> Defended by SHA-256 entropy. (3) Homograph Collision (Semantic spoofing) -> Defended by Social Uptake and Reputation. Utilizes {{fail_closed}}.",
  "gloss": "Stub, hash, and homograph collisions are different threats",
  "failure_modes": [
    "Stub Confusion: Relying on 4-char stub (#a1b2) for security instead of convenience.",
    "Homograph Attack: Malicious actor mints a pattern with a trusted Handle but malicious Definition.",
    "(Social Engineering).",
    "Pre-image Attack: Theoretical break of SHA-256 (renders Level 2 defense void)."
  ],
  "invariants": [
    "L1 Defense: Stub match is NOT verification. Full hash check is mandatory.",
    "L3 Defense: {{identity}} is Content, not Handle. A 'spoofed' pattern is simply a different pattern with zero reputation."
  ],
  "preconditions": [
    "Sema Hashing Algorithm (SHA-256) is secure"
  ],
  "postconditions": [
    "Appropriate verification logic applied",
    "Threat level identified"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:ThreeLevelCollision#mh:SHA-256:d9905e91ea38f04c014d7e992f517f88129b891a49d749f288d4176da9734823",
  "sema_ref": "ThreeLevelCollision#d990",
  "sema_stub": "d990",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "fail_closed": "FailClosed#e6a0",
      "identity": "Identity#626c"
    }
  }
}
```

---

## TieredAccess#e45b

```json
{
  "handle": "TieredAccess",
  "mechanism": "Central 'massive' agents (high authority) create a gravity well. The cost to interact with an agent increases the closer you get to the center. This naturally filters low-value queries to the periphery and reserves core attention for high-value interactions. Utilizes {{bearer_token}}.",
  "gloss": "Cost-distance indexing",
  "failure_modes": [
    "Metric Divergence: Agents disagree on distance calculation, causing payment rejection.",
    "Center becomes economically inaccessible to low-resource agents.",
    "Center becomes inaccessible to the poor."
  ],
  "invariants": [
    "Cost Monotonicity: Cost(Distance D-1) > Cost(Distance D) - closer to center means higher cost",
    "Metric Definition: Distance must be computed via agreed metric (hops, latency, trust score)"
  ],
  "preconditions": [
    "{{agent}} has valid {{identity}}"
  ],
  "postconditions": [
    "Access log updated"
  ],
  "parameters": [
    {
      "name": "cost_function",
      "type": "Enum",
      "range": "{Linear, Exponential, Step#5f22}",
      "description": "How cost scales with proximity"
    },
    {
      "name": "distance_metric",
      "type": "Enum",
      "range": "{Hops, Latency, TrustScore}",
      "description": "How to measure distance"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:TieredAccess#mh:SHA-256:e45bd51bbdb40c9fcc3fea300a7fe4fd643ef267d1eef914845452f998a03163",
  "sema_ref": "TieredAccess#e45b",
  "sema_stub": "e45b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#35b9",
      "identity": "Identity#626c"
    },
    "composes_with": {
      "bearer_token": "BearerToken#2fe9"
    }
  }
}
```

---

## ToolDiscovery#7c18

```json
{
  "handle": "ToolDiscovery",
  "mechanism": "{{agent}} queries a {{discover}} for capabilities matching its current {{task}}. Registry returns a {{card}} listing available tools with typed input/output schemas. {{agent}} selects the best match, performs a {{compatibility_check}} to verify schema alignment, then invokes via {{tool_invoke}} and observes the typed {{result}}. If no match is found or {{compatibility_check}} fails, the agent must {{fail_closed}} rather than attempt a best-effort invocation. Follows the Model Context Protocol pattern of progressive discovery under {{context_first}} discipline: orient via registry, explore via schema matching, verify via hash comparison.",
  "gloss": "Discover and invoke external tools via structured capability manifests",
  "invariants": [
    "Schema Verification: Tool manifest hash must be verified via {{compatibility_check}} before invocation",
    "Fail-Closed: On schema mismatch or missing tool, reject via {{fail_closed}} rather than attempt best-effort",
    "Tool output must conform to declared schema in the {{card}}"
  ],
  "preconditions": [
    "{{discover}} accessible",
    "{{task}} specifies required capability type"
  ],
  "postconditions": [
    "{{result}} returned conforming to tool's declared output schema",
    "Invocation logged with tool identity and schema hash"
  ],
  "failure_modes": [
    "Registry unavailable (no tools discoverable \u2014 must degrade gracefully).",
    "Schema drift (tool updated its manifest but {{agent}} cached old version).",
    "Capability hallucination (tool claims capability it cannot deliver)."
  ],
  "signature": [
    "Discover#7dbc(ToolInvoke#4694)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1,
    "related": [
      "AgentDiscover#d4f2"
    ]
  },
  "sema_ref": "ToolDiscovery#7c18",
  "sema_id": "sema:ToolDiscovery#mh:SHA-256:7c18795bfdd6ff66afe92f985c4db8e19ad1a3a9fd1120375e22d46b65fbff83",
  "sema_stub": "7c18",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "card": "Card#2d01",
      "discover": "Discover#7dbc",
      "agent": "Agent#35b9",
      "context_first": "ContextFirst#def7"
    },
    "composes_with": {
      "fail_closed": "FailClosed#e6a0",
      "tool_invoke": "ToolInvoke#4694",
      "compatibility_check": "CompatibilityCheck#3abb"
    },
    "yields": {
      "result": "Result#195b"
    }
  }
}
```

---

## TranslationProxy#895a

```json
{
  "handle": "TranslationProxy",
  "mechanism": "A stateless agent that wraps a legacy system. It intercepts 'modern' agent signals, uses {{translate}} to convert them into legacy {{protocol}} API calls, and translates responses back. It acts as a 'spacesuit' for the legacy system. Utilizes {{ontology_handshake}} and {{compare}} to verify semantic fidelity.",
  "gloss": "Protocol adaptation wrapper",
  "failure_modes": [
    "Lossy translation."
  ],
  "invariants": [
    "Semantic meaning preserved across languages/ontologies",
    "Type safety maintained"
  ],
  "preconditions": [
    "{{message}} M in {{protocol}} A",
    "Target {{protocol}} B"
  ],
  "postconditions": [
    "{{message}} M' in {{protocol}} B"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:TranslationProxy#mh:SHA-256:895a31b33e5c6add265a78d63e1669ca02b4d99798b4cc0d272b0f459cbe69b0",
  "sema_ref": "TranslationProxy#895a",
  "sema_stub": "895a",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Translate#a8ed(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "ontology_handshake": "OntologyHandshake#46dc",
      "message": "Message#f767",
      "protocol": "Protocol#7e1c",
      "compare": "Compare#4881",
      "translate": "Translate#a8ed"
    }
  }
}
```

---

## UniqueHandle#d9a1

```json
{
  "handle": "UniqueHandle",
  "mechanism": "A cryptographic pointer to a singular, rivalrous resource (e.g., a specific file, a hardware port, a unique role). Unlike a copyable variable, a UniqueHandle obeys Linear Logic: it can be Transferred but not Copied. If {{agent}} A sends the Handle to {{agent}} B, {{agent}} A loses access immediately. Attempts to use a transferred Handle result in a capability fault. Utilizes {{state_lock}}.",
  "gloss": "Transferable ownership of a singular resource",
  "failure_modes": [
    "Orphaned Resource: If the Handle is deleted or lost, the underlying resource remains locked forever (requires a '{{break}} Glass' expiration or Admin override)."
  ],
  "invariants": [
    "Exclusivity: Access(Resource) requires Proof(Handle)",
    "Linear Logic: Transfer(A -> B) implies A loses access immediately",
    "Linearity: Count(Handle) == 1 always",
    "Non-Duplication: Handle cannot be copied, only moved"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:UniqueHandle#mh:SHA-256:d9a1b8d27c546ca3297cc2c8deaeb91300f52bf645e11b667b84d130b169c16d",
  "sema_ref": "UniqueHandle#d9a1",
  "sema_stub": "d9a1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#8183",
      "break": "Break#177f",
      "agent": "Agent#35b9"
    }
  }
}
```

---

## UptakeAsGround#0013

```json
{
  "handle": "UptakeAsGround",
  "mechanism": "Pragmatic Verification. The validity of a pattern is defined as a function of its `Coordination_Success_Rate`. If Agents A and B use Pattern P and successfully complete a {{task}}, P gains 'Semantic Mass'. If usage is zero or results in failure, P is effectively meaningless. Utilizes {{modest_claim}}.",
  "gloss": "Meaning emerges from successful coordination",
  "failure_modes": [
    "Empty Formalism: Treating a minted but unused pattern as 'Real'.",
    "Echo Chamber: High uptake within a closed group of hallucinating agents creates false semantic mass (requires outside verification).",
    "Legacy Rot: Assuming a historically popular pattern is still valid after context has drifted."
  ],
  "invariants": [
    "Validation: Successful {{task}} completion is the only proof of shared meaning.",
    "Wittgenstein's Razor: Meaning is Use. No Use = No Meaning."
  ],
  "preconditions": [
    "Pattern minted",
    "Usage telemetry available"
  ],
  "postconditions": [
    "Semantic mass updated based on coordination outcome"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:UptakeAsGround#mh:SHA-256:001365c9917fa3e9c04c463ec563edc019b6dfa5e9da61b243a2acadaa2bfd9e",
  "sema_ref": "UptakeAsGround#0013",
  "sema_stub": "0013",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "modest_claim": "ModestClaim#ac19"
    }
  }
}
```

---

## UptakeOverTimestamp#44de

```json
{
  "handle": "UptakeOverTimestamp",
  "mechanism": "Decentralized Governance Heuristic. Resolves canonical status conflicts by prioritizing Usage Volume (uptake) over Registration Time (timestamp). When querying for a concept Handle, the system returns the variant with the highest `Reference_Count` or `Execution_Count`. Utilizes {{uptake_as_ground}}.",
  "gloss": "Usage determines canonical status, not who minted first",
  "failure_modes": [
    "The Facebook {{problem}} (Network Effects): A mediocre pattern with high early uptake becomes impossible to dislodge by a superior new pattern.",
    "Cold Start: New patterns have 0 uptake, making them invisible to discovery algorithms."
  ],
  "invariants": [
    "Meritocracy: Canonical_Score = f(Usage, Citations, Success_Rate).",
    "Timestamp Irrelevance: Creation_Date must NOT be a factor in relevance ranking."
  ],
  "preconditions": [
    "Multiple patterns exist for similar concepts",
    "Usage metrics available"
  ],
  "postconditions": [
    "Canonical pattern identified",
    "Squatted/Dead patterns suppressed"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:UptakeOverTimestamp#mh:SHA-256:44de909798cb858dc158d8d3b4939f566b99efa7ad04096c2adc97e1c38de01f",
  "sema_ref": "UptakeOverTimestamp#44de",
  "sema_stub": "44de",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "uptake_as_ground": "UptakeAsGround#0013",
      "problem": "Problem#4576"
    }
  }
}
```

---

## WorkerMode#b5c4

```json
{
  "handle": "WorkerMode",
  "mechanism": "Execution {{state}} Machine. Upon invoking `solver_claim_task`, the {{agent}} performs an atomic {{identity}} change via {{context_switch}} using the {{solver_manifest}}. The {{agent}} remains in this {{mode}} until the {{task}} is complete (emitting a {{solution}} or error to the {{solver_node}}), ensuring adherence to the assigned persona. A {{lock}} prevents concurrent task claims.",
  "gloss": "Claim tasks and become the assigned persona",
  "failure_modes": [
    "Persona Drift: {{agent}} slowly reverts to default behaviors during long tasks ({{context}} Window exhaustion).",
    "Zombie Worker: {{agent}} claims {{task}}, enters WorkerMode, but crashes/hangs before reporting completion.",
    "{{identity}} Leak: Information from previous tasks bleeds into the current WorkerMode session."
  ],
  "invariants": [
    "{{identity}} {{lock}}: During WorkerMode, system_prompt MUST == {{solver_manifest}}.persona.",
    "Isolation: Memory {{context}} must be flushed/reset before entering WorkerMode.",
    "Lifecycle Bound: {{mode}} cannot be exited without emitting a {{solution}} or Error."
  ],
  "preconditions": [
    "{{solver_manifest}} defined",
    "{{task}} available in queue"
  ],
  "postconditions": [
    "{{agent}} returns to Idle {{state}}",
    "{{task}} marked Complete/Failed"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:WorkerMode#mh:SHA-256:b5c4563f37c89f5983e199959a3d2adeaa58280ffb0043c7bf1737e39492e997",
  "sema_ref": "WorkerMode#b5c4",
  "sema_stub": "b5c4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#b328",
      "solution": "Solution#fcea",
      "state": "State#4d58",
      "context": "Context#510a",
      "mode": "Mode#0e74",
      "identity": "Identity#626c",
      "context_switch": "ContextSwitch#590e",
      "lock": "Lock#051c",
      "agent": "Agent#35b9",
      "solver_node": "SolverNode#26b1"
    },
    "accepts": {
      "solver_manifest": "SolverManifest#ea7a"
    }
  }
}
```

---

## Workflow#c728

```json
{
  "handle": "Workflow",
  "data_schema": {
    "type": "object",
    "required": [
      "steps",
      "dependencies"
    ],
    "properties": {
      "steps": {
        "type": "array",
        "description": "List of executable units"
      },
      "dependencies": {
        "type": "array",
        "description": "DAG edges (step_A -> step_B)"
      },
      "artifacts": {
        "type": "object",
        "description": "Typed outputs flowing on edges"
      }
    }
  },
  "mechanism": "A directed graph of {{step}}s where the output of one {{solver}} becomes the input of another. It defines the sequence of operations required to complete a complex objective. Unlike a simple chain, a workflow handles branching, parallelism, and conditional logic. Each edge carries a typed {{artifact}} that must satisfy an {{accept_spec}} before the next node can execute. It binds {{role}}s to steps but does not instantiate them.",
  "gloss": "Directed graph of operations",
  "failure_modes": [
    "Deadlock: Circular dependencies prevent progress.",
    "Cascade Failure: One node failure propagates to all dependents.",
    "Orphan Output: A node produces artifacts that no downstream node consumes."
  ],
  "invariants": [
    "Causality: Step B cannot start before Step A's prerequisites are met.",
    "Acyclicity: Unless explicitly recursive, workflows must terminate.",
    "Artifact Typing: Each edge carries a typed artifact, not raw data."
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "tier": 1,
    "ring": 0
  },
  "sema_id": "sema:Workflow#mh:SHA-256:c728636b6a043b7ace516bbafbc231759514070d2755d8694b0c0404266bfe91",
  "sema_ref": "Workflow#c728",
  "sema_stub": "c728",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "solver": "Solver#94ab",
      "accept_spec": "AcceptSpec#7caa",
      "role": "Role#94e4",
      "artifact": "Artifact#6254",
      "step": "Step#5f22"
    }
  }
}
```

---

