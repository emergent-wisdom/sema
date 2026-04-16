# Sema Vocabulary (Short Hand JSON)

**Total Patterns:** 427
**Format:** JSON with short-hand references.

---

# Layer: Infrastructure

## Anomaly#7987

```json
{
  "handle": "Anomaly",
  "mechanism": "A piece of {{datum}} that deviates from the expected standard or pattern. It creates the spark for thinking and often triggers further investigation.",
  "gloss": "Deviation from expectation",
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
  "sema_id": "sema:Anomaly#mh:SHA-256:7987f2cd4a353f206fccd038ddac021ef849cfa58e352d2d2d7ba3850b916893",
  "sema_ref": "Anomaly#7987",
  "sema_stub": "7987",
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

## Audit#4044

```json
{
  "handle": "Audit",
  "mechanism": "The process of verifying that a {{system}}'s {{state}} or behavior matches its specifications.",
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
  "sema_id": "sema:Audit#mh:SHA-256:40447e5c9c68a79109ce76f564ca8c09c2c572f8deabcb92ed3d7db0b845b3c1",
  "sema_ref": "Audit#4044",
  "sema_stub": "4044",
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

## Ballot#f1d7

```json
{
  "handle": "Ballot",
  "mechanism": "A structured container for a decision proposal. Contains: the question being decided, available options, voting rules (majority/supermajority/unanimity), and deadline. The Ballot is immutable once cast\u2014amendments require a new Ballot.",
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
    "tier": 3,
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
  "sema_ref": "Ballot#f1d7",
  "sema_id": "sema:Ballot#mh:SHA-256:f1d7f5635ea8bc53d0e1718d1ea372bd93b829500ac69602e648e507404f7beb",
  "sema_stub": "f1d7",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "select": "Select#15c2"
    }
  }
}
```

---

## Belief#5ad9

```json
{
  "handle": "Belief",
  "mechanism": "A unit of epistemic {{state}}. Represents a claim held by an {{agent}} with a specific confidence score (0.0 to 1.0) and a pointer to supporting evidence. Unlike a Fact, a Belief is subjective and mutable.",
  "gloss": "A subjective claim with confidence and evidence",
  "parameters": [
    {
      "name": "confidence",
      "type": "Float",
      "range": "unspecified",
      "description": "Subjective probability that this belief is true"
    },
    {
      "name": "evidence",
      "type": "List[Context#510a]",
      "range": "unspecified",
      "description": "Supporting evidence contexts for this belief"
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
  "sema_id": "sema:Belief#mh:SHA-256:5ad9a529582c153a8fcf44db3b2d15f68040049729f13121c484bc8fa9c241df",
  "sema_ref": "Belief#5ad9",
  "sema_stub": "5ad9",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## Break#1a63

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
  "gloss": "Enable graceful degradation and coordinated recovery when coordination fails mid-stream",
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
      "EjectionSeat#6ff7",
      "Retry#d53d"
    ]
  },
  "sema_id": "sema:Break#mh:SHA-256:1a63164e5ff06e60927f3e585fc003abab80eeb4002ccf075e3b53747318fa95",
  "sema_ref": "Break#1a63",
  "sema_stub": "1a63",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "message": "Message#f767",
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## Card#c9f0

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
  "mechanism": "Structured capability advertisement enabling agent discovery before contact. {{agent}} creates CARD: {agent_id (unique), endpoint (how to reach), protocols[] (compatibility), capabilities[] (what agent claims to do), constraints (availability, rate limits, requirements), metadata (version, ttl, published timestamp)}. {{agent}} PUBLISHES card via registry, broadcast, DHT, or well-known endpoint (mechanism-agnostic). Discovering agents QUERY: {capability_match, protocol_match, semantic_search}. Query returns ranked CARD list. Discoverer selects promising CARDs, then GREETs at card.endpoint to establish channel. CARDs have TTL\u2014agents must REFRESH periodically to maintain visibility. CARD capabilities are CLAIMS not proofs: verification happens via {{probe}} after GREET establishes channel. It enables discovery via {{select}} queries against the registry, filtering candidates by capability and protocol compatibility.",
  "gloss": "Enable capability-based agent discovery, making coordination ecosystems dynamic and self-describing",
  "parameters": [
    {
      "name": "verification_tier",
      "type": "Enum",
      "range": "{SelfReported, Verified, Bonded}",
      "description": "Default: SelfReported"
    },
    {
      "name": "proof",
      "type": "String",
      "range": "unspecified",
      "description": "Optional hash of past Success artifact"
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
  "sema_id": "sema:Card#mh:SHA-256:c9f028ecd6e890702f25417a076aed7d352790d1c02fd9656488daea00db2626",
  "sema_ref": "Card#c9f0",
  "sema_stub": "c9f0",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "probe": "Probe#9f2b"
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

## Chain#5711

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
  "mechanism": "A concrete data structure representing a sequential list of linked nodes. Unlike {{linear}} (which is an abstract topology class), a Chain is the instantiated storage object containing the steps and their data payloads.",
  "gloss": "Sequential data container (Linked List)",
  "invariants": [
    "Connectivity: Node(N) must point to Node(N+1).",
    "Acyclicity: No loops permitted."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_id": "sema:Chain#mh:SHA-256:57119a990ff1c50eda6cb301dfec09450d2cbb21659ca541560b6bbb2ece0332",
  "sema_ref": "Chain#5711",
  "sema_stub": "5711",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "linear": "Linear#81af"
    }
  }
}
```

---

## Check#1544

```json
{
  "handle": "Check",
  "data_schema": {
    "type": "object",
    "required": [
      "target_id",
      "condition",
      "status"
    ],
    "properties": {
      "target_id": {
        "type": "string",
        "description": "The entity being checked"
      },
      "condition": {
        "type": "string",
        "description": "The logic predicate"
      },
      "status": {
        "type": "boolean",
        "description": "True/False result"
      },
      "evidence": {
        "type": "string",
        "description": "Why it passed/failed"
      }
    }
  },
  "mechanism": "A non-blocking verification primitive. Evaluates the truth-value of a {{condition}} against a target and returns a Boolean status. Unlike a {{gate}} (which alters control flow based on the result), a Check is purely observational and side-effect free. It answers 'Is this true?' without deciding 'Should we stop?'.",
  "gloss": "Non-blocking truth evaluation",
  "failure_modes": [
    "False Positive: Check returns True due to flawed logic or sensor noise.",
    "Heisenbug: The act of checking alters the state being checked."
  ],
  "invariants": [
    "Side-Effect Free: Running a check must not mutate the target state.",
    "Determinism: Same input context yields same boolean result."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "related": [
      "Gate#5c08",
      "Validate#16b2",
      "Judge#3d5f"
    ]
  },
  "sema_id": "sema:Check#mh:SHA-256:1544e646894003b4bac963cee70097a4bffd75f6cb753f218befb2079f8383a6",
  "sema_ref": "Check#1544",
  "sema_stub": "1544",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "gate": "Gate#206d",
      "condition": "Condition#cbd5"
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
    "tier": 3,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "related": [
      "ContextCompress#6dbd",
      "ContextSwitch#42cd",
      "AnchorDrop#bf63"
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
      "identity": "Identity#626c",
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## Contract#0624

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
  "mechanism": "An immutable record of agreement between two or more {{identity}}s. It aggregates a set of {{condition}}s (terms) and obligations which all parties must {{sign}} to accept. Contracts serve as the binding {{context}} for disputes resolved by a {{judge}}.",
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
  "sema_id": "sema:Contract#mh:SHA-256:06241d8925a848e07b8b7afab2c37767b126c3f2363faba11bcc455ebb6a4d04",
  "sema_ref": "Contract#0624",
  "sema_stub": "0624",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "sign": "Sign#1fb9",
      "judge": "Judge#d84f",
      "context": "Context#510a"
    },
    "accepts": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## Correlation#091f

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
  "mechanism": "A relationship where two {{variable}}s move together, but one does not necessarily cause the other. 'Cum hoc ergo propter hoc' fallacy trap.",
  "gloss": "Shared movement",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Correlation#mh:SHA-256:091fbf1f3baec2028bbd64c9d2ff335ef41d9ec6ec992e1967c5bca02c777625",
  "sema_ref": "Correlation#091f",
  "sema_stub": "091f",
  "dependencies": {
    "references": {
      "variable": "Variable#179a"
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

## Critique#3e00

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
  "parameters": [
    {
      "name": "criteria",
      "type": "List[String]",
      "range": "unspecified",
      "description": "Evaluation dimensions to assess against"
    }
  ],
  "sema_id": "sema:Critique#mh:SHA-256:3e00cb143ce745ed77a29af93416808b848b2a2d9749245b777ad90901aa4ba8",
  "sema_ref": "Critique#3e00",
  "sema_stub": "3e00",
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
    "accepts": {
      "datum": "Datum#31cf"
    },
    "yields": {
      "assessment": "Assessment#a765"
    },
    "references": {
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## DAG#ed37

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
  "sema_id": "sema:DAG#mh:SHA-256:ed37a1e0310857feba371491e4652f9a142905af341adbc67e6386c5b3c1672f",
  "sema_ref": "DAG#ed37",
  "sema_stub": "ed37",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "parallelize": "Parallelize#d6b4"
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
      "state": "State#4d58",
      "stream": "Stream#22f3"
    }
  }
}
```

---

## Exception#bcdc

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
  "sema_id": "sema:Exception#mh:SHA-256:bcdc11a8b6e4c1af2def02029ab03bf24c1480bd827ee3d570e374096cfccdc6",
  "sema_ref": "Exception#bcdc",
  "sema_stub": "bcdc",
  "dependencies": {
    "references": {
      "circuit_breaker": "CircuitBreaker#4162",
      "state": "State#4d58",
      "fail_closed": "FailClosed#ae79"
    }
  }
}
```

---

## Goal#456a

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
  "sema_id": "sema:Goal#mh:SHA-256:456a8a283dc469d46b3307147a853e4be7d07f0d6c4477d789b8ab14aa33b02a",
  "sema_ref": "Goal#456a",
  "sema_stub": "456a",
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
      "work": "Work#aaad",
      "result": "Result#8ed9"
    }
  }
}
```

---

## Group#0929

```json
{
  "handle": "Group",
  "mechanism": "A defined collection of {{agent}}s sharing a common {{context}} or goal. It serves as the scope for {{consensus}} and {{shout_whisper}}.",
  "gloss": "Agent collective",
  "sema_id": "sema:Group#mh:SHA-256:0929f34d784edcac580579d64a1e6277564a4ed3fb1bdd3d87e56b5d7a62c295",
  "sema_ref": "Group#0929",
  "sema_stub": "0929",
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
      "group_id",
      "members"
    ],
    "properties": {
      "group_id": {
        "type": "string",
        "description": "Unique identifier"
      },
      "members": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Agent IDs in the group"
      },
      "shared_context": {
        "type": "string",
        "description": "Reference to common context"
      }
    }
  },
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "shout_whisper": "ShoutWhisper#35dd",
      "consensus": "Consensus#7216",
      "context": "Context#510a"
    }
  }
}
```

---

## Hierarchy#aa9b

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
  "gloss": "Vertical ranking",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Hierarchy#mh:SHA-256:aa9bec7346dca2ce2e83a70fc352825aa78c907cd82a8306f7e6856e42ef245c",
  "sema_ref": "Hierarchy#aa9b",
  "sema_stub": "aa9b",
  "dependencies": {
    "references": {
      "category": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1"
    }
  }
}
```

---

## Hypothesis#e95b

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
  "mechanism": "A tentative explanation or prediction that is subject to verification or falsification.",
  "gloss": "A tentative explanation",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Hypothesis#mh:SHA-256:e95b94f3066236d1b543330c46d177a5e2e590ea5bdd97953f589226a9f11812",
  "sema_ref": "Hypothesis#e95b",
  "sema_stub": "e95b"
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

## Ledger#c363

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
  "sema_id": "sema:Ledger#mh:SHA-256:c363289733cce70a458481259762ae79a0419da4ed5c15ad942c4873181ba910",
  "sema_ref": "Ledger#c363",
  "sema_stub": "c363",
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
      "agent": "Agent#aaec",
      "value": "Value#3c5d"
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
      "Decompose#ac56"
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

## MechanisticDesignProposal#8cf7

```json
{
  "handle": "MechanisticDesignProposal",
  "mechanism": "A structured blueprint for a systemic {{solution}} that addresses a {{problem}} in a {{system}}. It goes beyond a standard proposal by requiring the definition of a core mechanism\u2014the specific leverage point and causal chain used to alter system behavior. The proposal integrates the 'Why it Works' (defense) and 'Why it Fails' (attack) dialectic, along with medium-term implementation and long-term vision projections.",
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
  "sema_ref": "MechanisticDesignProposal#8cf7",
  "sema_id": "sema:MechanisticDesignProposal#mh:SHA-256:8cf72275c6678ea0c57d497fff459f6f9c5259330524fe8f9bb3af63b7df9c06",
  "sema_stub": "8cf7",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "yields": {
      "solution": "Solution#7186"
    },
    "accepts": {
      "system": "System#e314",
      "problem": "Problem#5baa"
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

## Metric#8895

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
  "gloss": "Quantifiable unit of measure",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "sema_id": "sema:Metric#mh:SHA-256:8895c946c0d9728fb06563d2294bde3fe9a3be817d3d50ed1a587fd604bc6b29",
  "sema_ref": "Metric#8895",
  "sema_stub": "8895",
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

## Mode#53e0

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
      "WorkerMode#cd5e",
      "SynergisticMode#9d93"
    ]
  },
  "sema_id": "sema:Mode#mh:SHA-256:53e0b9650e76b57a1217da26c91dac514674d87b0f92c1c13b770e7ae2b6c826",
  "sema_ref": "Mode#53e0",
  "sema_stub": "53e0",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "state": "State#4d58",
      "agent": "Agent#aaec"
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

## Observe#8ebd

```json
{
  "handle": "Observe",
  "data_schema": {
    "type": "object",
    "required": [
      "observation_id",
      "source",
      "data"
    ],
    "properties": {
      "observation_id": {
        "type": "string",
        "description": "Unique identifier for this observation"
      },
      "source": {
        "type": "string",
        "description": "Where the observation came from"
      },
      "data": {
        "description": "The raw observed information"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "When observation occurred"
      }
    }
  },
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
    "category": "Data Structures",
    "related": [
      "Belief#5ad9",
      "Attention"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Observe#mh:SHA-256:8ebdc058f13dc14e6ed22cd000bc6eb89507e3b6b507cc393c88a8209c65122f",
  "sema_ref": "Observe#8ebd",
  "sema_stub": "8ebd",
  "dependencies": {
    "yields": {
      "context": "Context#510a"
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

## Outcome#38e0

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
  "gloss": "Actual result",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Outcome#mh:SHA-256:38e079f2323ce9cf3d1022624f693bbb02b3e0e25d7eb42abc4d06c75548b53a",
  "sema_ref": "Outcome#38e0",
  "sema_stub": "38e0",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2"
    }
  }
}
```

---

## Overlap#bcfa

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
  "gloss": "Transform negotiations from position-based battles to interest-based discovery of shared ground",
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
  "sema_id": "sema:Overlap#mh:SHA-256:bcfa7595ad18e8227f2019bedc717a67f3ffca1871ab9abfd02ff9cbf18cdfbb",
  "sema_ref": "Overlap#bcfa",
  "sema_stub": "bcfa",
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

## Permission#7f7d

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
  "sema_ref": "Permission#7f7d",
  "sema_id": "sema:Permission#mh:SHA-256:7f7d69e56a0b6bd65577a7fd6e8602f5bb694a647b3493a55823de851a32676f",
  "sema_stub": "7f7d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "act": "Act#5d55",
      "artifact": "Artifact#6254",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## Plan#64f2

```json
{
  "handle": "Plan",
  "gloss": "An ordered sequence of steps to achieve a goal",
  "mechanism": "An {{artifact}} containing a structured {{sequence}} of {{step}}s designed to transition a {{system}} from a current {{state}} to a target {{goal}}. Unlike a simple list, a Plan enforces causal dependency between steps and resource allocation.",
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
  "sema_ref": "Plan#64f2",
  "sema_id": "sema:Plan#mh:SHA-256:64f273fc1710ca9d5b52a39758cf8e68279778d32856de4629a44ad7a7f5a4bc",
  "sema_stub": "64f2",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "artifact": "Artifact#6254",
      "state": "State#4d58",
      "sequence": "Sequence#b0b8",
      "goal": "Goal#456a",
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

## Problem#5baa

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
  "sema_id": "sema:Problem#mh:SHA-256:5baa4b94e48686c15413bc92447c72917fb2f77109436b4a57aae6ee982fd311",
  "sema_ref": "Problem#5baa",
  "sema_stub": "5baa",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "task": "Task#d9f9"
    }
  }
}
```

---

## ProblemSpace#78da

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
  "sema_ref": "ProblemSpace#78da",
  "sema_id": "sema:ProblemSpace#mh:SHA-256:78da7fef93c3a5e6a7728d30afcb0e8e9270493b23b36bd83acf2ee6977271d1",
  "sema_stub": "78da",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "state": "State#4d58",
      "solution": "Solution#7186"
    }
  }
}
```

---

## Prompt#5ded

```json
{
  "handle": "Prompt",
  "mechanism": "The input text or instruction provided to a generative model.",
  "gloss": "Model input instruction",
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
  "sema_id": "sema:Prompt#mh:SHA-256:5dedb478148eb9ca7b2621a571316aefcdb475174141a64c04c0a8c890355107",
  "sema_ref": "Prompt#5ded",
  "sema_stub": "5ded",
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

## Queue#2ec3

```json
{
  "handle": "Queue",
  "mechanism": "A linear data structure for ordering {{task}}s or {{message}}s. It enforces First-In-First-Out (FIFO) or Priority ordering.",
  "gloss": "Ordered task buffer",
  "sema_id": "sema:Queue#mh:SHA-256:2ec3531a8c5711e281ab2913646d9f46dad05140fea7ceb6966bfa62d745bc9b",
  "sema_ref": "Queue#2ec3",
  "sema_stub": "2ec3",
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
      "message": "Message#f767",
      "task": "Task#d9f9"
    }
  }
}
```

---

## Resource#9bb2

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
  "sema_ref": "Resource#9bb2",
  "sema_id": "sema:Resource#mh:SHA-256:9bb2dd733e5900d441d35d2c6e74f69dc4e4afe536c12adbcfc5863f3ada2922",
  "sema_stub": "9bb2",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "budget": "Budget#a763"
    }
  }
}
```

---

## Result#8ed9

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
  "sema_id": "sema:Result#mh:SHA-256:8ed9ca66a8508e8603e8da74b545f03b832f7e8b8d4e2fd56c496dcc29afb2ef",
  "sema_ref": "Result#8ed9",
  "sema_stub": "8ed9",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "task_id",
      "output",
      "status"
    ],
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The task this result satisfies"
      },
      "status": {
        "type": "string",
        "enum": [
          "Success",
          "Partial",
          "Failure"
        ]
      },
      "output": {
        "description": "The actual artifact or data produced"
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
        },
        "description": "List of step IDs that generated this result"
      },
      "metrics": {
        "type": "object",
        "description": "Performance metrics (latency, cost)"
      }
    }
  },
  "dependencies": {
    "references": {
      "metric": "Metric#8895",
      "solution": "Solution#7186"
    }
  }
}
```

---

## Risk#3774

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
  "sema_id": "sema:Risk#mh:SHA-256:37748bbbeb3ee23c5a258a49faee4d04a16064136fdfd8721a365d3764c73fb8",
  "sema_ref": "Risk#3774",
  "sema_stub": "3774",
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
      "metric": "Metric#8895",
      "probability": "Probability#356b"
    }
  }
}
```

---

## RuleSet#8d85

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
  "sema_ref": "RuleSet#8d85",
  "sema_id": "sema:RuleSet#mh:SHA-256:8d85afc9e1f879dc43aaf8c92bd280aa8f1c81ece7dd1bd6f36c6ab47ddc0ecf",
  "sema_stub": "8d85",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "constitution": "Constitution#863b"
    }
  }
}
```

---

## Score#29da

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
    "type": "number",
    "description": "The numerical score value"
  },
  "sema_ref": "Score#29da",
  "sema_id": "sema:Score#mh:SHA-256:29da7b609182c3ecef85ebafc34cae5acd221d65ef0e5c4b2b41bbededb6d414",
  "sema_stub": "29da",
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

## ScoringFunction#3de5

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
  "mechanism": "A deterministic logical unit that maps an input artifact to a scalar {{value}} (Score). It encapsulates the criteria used by {{rank}} and {{judge}}.",
  "gloss": "Deterministic valuation logic",
  "invariants": [
    "Determinism: Same input always yields same score.",
    "Range: Output must be within [0.0, 1.0] or [-inf, +inf]."
  ],
  "sema_id": "sema:ScoringFunction#mh:SHA-256:3de5b5abe572e4e8cd6c0d4ecc55889fd157f66fdab01b399c0eae0cbca0a99d",
  "sema_ref": "ScoringFunction#3de5",
  "sema_stub": "3de5",
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
      "rank": "Rank#cb98",
      "judge": "Judge#d84f",
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
      "state": "State#4d58",
      "vector": "Vector#c7c4"
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

## Solution#7186

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
    },
    {
      "name": "cost_incurred",
      "type": "TokenAmount",
      "range": "unspecified",
      "description": "Total compute cost"
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
  "sema_id": "sema:Solution#mh:SHA-256:7186aebe86145a01476542042ab77b7eda5c54033e6dccf62a97e8fa6b94e806",
  "sema_ref": "Solution#7186",
  "sema_stub": "7186",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "chain": "Chain#5711",
      "tree": "Tree#ddce",
      "artifact": "Artifact#6254"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Spec#436e

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
  "sema_ref": "Spec#436e",
  "sema_id": "sema:Spec#mh:SHA-256:436efd7df8ed376f693362923a024b4096265b9de32c7a980297b078112c75b5",
  "sema_stub": "436e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "goal": "Goal#456a",
      "plan": "Plan#64f2",
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
      "Plan#64f2"
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

## Summary#310e

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
    "type": "string",
    "description": "The summarized text or content"
  },
  "sema_ref": "Summary#310e",
  "sema_id": "sema:Summary#mh:SHA-256:310e68dd2e7016cbc97e43f87f5aa17631699e4ca49e65d0b43c6d8811a401de",
  "sema_stub": "310e",
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

## Task#d9f9

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
  "sema_id": "sema:Task#mh:SHA-256:d9f92106bd9cd867b1b753275d6faa37b6ea4fcbb948b283460caedfa75b6955",
  "sema_ref": "Task#d9f9",
  "sema_stub": "d9f9",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "required": [
      "task_id",
      "description",
      "status",
      "created_at"
    ],
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Unique UUID for the task"
      },
      "parent_id": {
        "type": "string",
        "description": "ID of the super-task, if any"
      },
      "description": {
        "type": "string",
        "description": "Natural language intent"
      },
      "status": {
        "type": "string",
        "enum": [
          "Pending",
          "Active",
          "Blocked",
          "Complete",
          "Failed"
        ],
        "default": "Pending"
      },
      "requirements": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of acceptance criteria"
      },
      "assigned_solver_id": {
        "type": "string",
        "description": "The agent/node working on this"
      },
      "created_at": {
        "type": "string",
        "format": "date-time"
      },
      "deadline": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "dependencies": {
    "references": {
      "hierarchy": "Hierarchy#aa9b",
      "constraint": "Constraint#87fe",
      "system": "System#e314",
      "context": "Context#510a"
    }
  }
}
```

---

## ToolInvoke#cf0a

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
    "category": "Data Structures",
    "ring": 0,
    "related": [
      "AgentSandbox#06f2"
    ]
  },
  "data_schema": {
    "type": "object",
    "required": [
      "function_name",
      "arguments"
    ],
    "properties": {
      "function_name": {
        "type": "string",
        "description": "Name of the tool to invoke"
      },
      "arguments": {
        "type": "object",
        "description": "Parameters for the tool call"
      },
      "observation": {
        "description": "Result returned from tool execution"
      },
      "status": {
        "type": "string",
        "enum": [
          "pending",
          "success",
          "error"
        ],
        "description": "Invocation status"
      }
    }
  },
  "sema_ref": "ToolInvoke#cf0a",
  "sema_id": "sema:ToolInvoke#mh:SHA-256:cf0ae58828cde9f495b09af3e4519c3f05162066991d34d5f2505d13c32ba416",
  "sema_stub": "cf0a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "composes_with": {
      "input_guard": "InputGuard#0770"
    },
    "references": {
      "task": "Task#d9f9",
      "context": "Context#510a"
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
          "Linear#81af",
          "Tree#ddce",
          "DAG#ed37",
          "Cyclic#ac13",
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

## Tree#ddce

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
  "mechanism": "A branching {{topology}} where multiple lines of reasoning are explored simultaneously. Allows backtracking and pruning of unpromising branches (BFS/DFS). Equivalent to 'tree-of-thoughts reasoning'.",
  "gloss": "Branching reasoning topology",
  "invariants": [
    "Rootedness: All nodes descend from a single root.",
    "Acyclicity: No node is an ancestor of itself."
  ],
  "parameters": [
    {
      "name": "breadth",
      "type": "Integer",
      "range": "unspecified",
      "description": "Maximum branches explored per reasoning node"
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
  "sema_ref": "Tree#ddce",
  "sema_id": "sema:Tree#mh:SHA-256:ddce179b1f23b64fe76513a37d8d3c9319e0460f191a5c124b3372b8c4d2f415",
  "sema_stub": "ddce",
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

## Work#aaad

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
      "EntropyPump#b9ae"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Work#mh:SHA-256:aaad0ca428ad22dd8f5941f56b4425ddf62180752cfd6d5d8145419c8a6ac90b",
  "sema_ref": "Work#aaad",
  "sema_stub": "aaad",
  "dependencies": {
    "references": {
      "act": "Act#5d55",
      "budget": "Budget#a763"
    },
    "composes_with": {
      "task": "Task#d9f9"
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
      "ToolInvoke#cf0a",
      "ReAct#c720",
      "AgentSandbox#06f2"
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

## Aggregate#af54

```json
{
  "handle": "Aggregate",
  "mechanism": "Mathematical Reduction. A deterministic function that maps a {{vector}} of inputs to a single Scalar {{value}}. Implements standard statistical operations (Mean, Mode, Median) to compress signal bandwidth. It serves as the computational backbone for consensus mechanisms.",
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
      "range": "{Mean, Median, Mode#53e0, Sum, Min, Max, Variance, StdDev}",
      "description": "Default: Mean"
    },
    {
      "name": "weights",
      "type": "List<Float>",
      "range": "unspecified",
      "description": "Relative importance weights for each input element"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Aggregate#mh:SHA-256:af54a8a31d6e7ed0c6d7bdfb51935655b0a66d299bddb352dbff9f4a789e7486",
  "sema_ref": "Aggregate#af54",
  "sema_stub": "af54",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "mode": "Mode#53e0"
    },
    "accepts": {
      "vector": "Vector#c7c4"
    },
    "yields": {
      "value": "Value#3c5d"
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

## Budget#a763

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
    "Non-Negative: Remaining budget cannot be < 0.",
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
  "sema_ref": "Budget#a763",
  "sema_id": "sema:Budget#mh:SHA-256:a7637c4387d834ae190f6c42a2a96914c65294a9f618c4c96adf4ee1d26450e0",
  "sema_stub": "a763",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Care#cdfa

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
  "sema_id": "sema:Care#mh:SHA-256:cdfae572389ee7b84aa847b9320c072053f25827a7b06891cb08cd8d18aef40b",
  "sema_ref": "Care#cdfa",
  "sema_stub": "cdfa",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "entropy": "Entropy#a265",
      "value": "Value#3c5d"
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

## Feedback#9b5c

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
  "sema_id": "sema:Feedback#mh:SHA-256:9b5c7eee86ff79389e6fc9a4cd4e318296ff3e74e3e67514f8193a45be917e15",
  "sema_ref": "Feedback#9b5c",
  "sema_stub": "9b5c",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "signature": [
    "Signal#f39d(Incongruity#e98f)"
  ],
  "dependencies": {
    "composes_with": {
      "signal": "Signal#f39d"
    },
    "references": {
      "result": "Result#8ed9",
      "incongruity": "Incongruity#e98f",
      "metric": "Metric#8895"
    }
  }
}
```

---

## Greet#7ad2

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
  "sema_id": "sema:Greet#mh:SHA-256:7ad2382d29cb28ed605b0505374488c7e6dcd1ff8098b63686e83ab7098e2cf6",
  "sema_ref": "Greet#7ad2",
  "sema_stub": "7ad2",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    },
    "references": {
      "agent": "Agent#aaec",
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
      "state": "State#4d58",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Judge#d84f

```json
{
  "handle": "Judge",
  "mechanism": "Qualitative Evaluation. Evaluates the structural merit or quality of a {{subject}} on a continuous scale [0.0, 1.0]. Unlike {{check}} (which validates binary truth) or {{validate}} (which checks schema), Judge evaluates gradients of quality based on {{criteria}}, yielding a {{score}}.",
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
      "name": "criteria",
      "type": "String",
      "range": "unspecified",
      "description": "Evaluation standard to judge against"
    },
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
  "sema_id": "sema:Judge#mh:SHA-256:d84f449a90c6cdbe8e9bf7a8dcecd7369bb87cdab6880a1faa0dfe949584ae56",
  "sema_ref": "Judge#d84f",
  "sema_stub": "d84f",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "check": "Check#1544",
      "criteria": "Criteria#ef6b",
      "validate": "Validate#3de2"
    },
    "accepts": {
      "subject": "Subject#788f"
    },
    "yields": {
      "score": "Score#29da"
    }
  }
}
```

---

## Loop#fb2e

```json
{
  "handle": "Loop",
  "mechanism": "A control flow structure that repeats a sequence of {{work}} until a specific {{condition}} is met. Essential for feedback, learning, and persistent processes.",
  "gloss": "Repeated execution cycle",
  "invariants": [
    "Termination Guarantee: Must have a proven exit condition (or explicit Daemon mode).",
    "Progress: State must change between iterations to avoid infinite freeze."
  ],
  "sema_id": "sema:Loop#mh:SHA-256:fb2e7eeab0b569d64f7e74defeec56aeccf5abdb6c5cd4a0ce80c397ebc5d593",
  "sema_ref": "Loop#fb2e",
  "sema_stub": "fb2e",
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "work": "Work#aaad"
    },
    "accepts": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## NegativeProof#5225

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
  "sema_ref": "NegativeProof#5225",
  "sema_id": "sema:NegativeProof#mh:SHA-256:5225bbc358d41d3ef16f0466a4e33160d9c7d020132726c74c576eef5d399d4e",
  "sema_stub": "5225",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "hypothesis": "Hypothesis#e95b",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Probe#9f2b

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
      "range": "{StaticVector, Procedural, Sandbox#2be7, StakedReport}",
      "description": "Method used to verify probe response"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Probe#mh:SHA-256:9f2bf351c42ae5107e43cced5947ba813d8c1f7bc9f469a2551cbc0425637dfa",
  "sema_ref": "Probe#9f2b",
  "sema_stub": "9f2b",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "sandbox": "Sandbox#2be7"
    }
  }
}
```

---

## Quorum#29b4

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
      "LazyConsensus#4fc7"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Quorum#mh:SHA-256:29b46f238f70cc3f2126e8bd35ff531aa7ae65e0d3ab1d7d7cc794fa7155127d",
  "sema_ref": "Quorum#29b4",
  "sema_stub": "29b4",
  "dependencies": {
    "accepts": {
      "ballot": "Ballot#f1d7"
    }
  }
}
```

---

## Sandbox#2be7

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
      "AgentSandbox#06f2",
      "CircuitBreaker#4162",
      "SafetyCartographer"
    ]
  },
  "sema_id": "sema:Sandbox#mh:SHA-256:2be7b830454b430d8008cb54622a5c1a6434a6e076d7bbdaca4d2a5b1a1dadf0",
  "sema_ref": "Sandbox#2be7",
  "sema_stub": "2be7",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Search#d608

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
  "sema_ref": "Search#d608",
  "sema_id": "sema:Search#mh:SHA-256:d6083dea6898b63d14ccb2542fcfa05561a1f6326000c8d9c190599afd99b123",
  "sema_stub": "d608",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "check": "Check#1544",
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

## StateTransition#3737

```json
{
  "handle": "StateTransition",
  "mechanism": "Finite State Machine. A {{transition}} is defined as T: S x Event -> S. Only valid transitions allowed. Current {{state}} determines available actions.",
  "gloss": "Explicit finite-state machine governance",
  "sema_id": "sema:StateTransition#mh:SHA-256:3737f955afcae13b398c1961722ee8511ea8f737aca133329938de5cfb91bb57",
  "sema_ref": "StateTransition#3737",
  "sema_stub": "3737",
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "signature": [
    "Transition#072d(State#4d58)"
  ],
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "state": "State#4d58"
    }
  }
}
```

---

## TaskLifecycle#ecd8

```json
{
  "handle": "TaskLifecycle",
  "mechanism": "Explicit {{state_transition}} machine governing {{task}} progression through five states: PENDING (created, awaiting assignment), ASSIGNED (claimed by an {{agent}}), RUNNING (actively executing, emitting {{heartbeat}}), COMPLETED (successfully finished, {{result}} attached), FAILED (terminated with {{exception}}, retry decision required). Each transition requires a typed {{event}}: assign, start, complete, fail, cancel. Invalid transitions are rejected. RUNNING state requires periodic {{heartbeat}}; timeout triggers automatic FAILED transition. Follows the Agent-to-Agent protocol task management model.",
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
    "StateTransition#3737(Task#d9f9)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1,
    "tier": 1,
    "related": []
  },
  "sema_ref": "TaskLifecycle#ecd8",
  "sema_id": "sema:TaskLifecycle#mh:SHA-256:ecd8d6da7668a91bd65d1b20beaf58e8e300f418cb40d00a3453535dfb4bedda",
  "sema_stub": "ecd8",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "heartbeat": "Heartbeat#7f88",
      "event": "Event#7e71",
      "exception": "Exception#bcdc"
    },
    "composes_with": {
      "state_transition": "StateTransition#3737"
    },
    "yields": {
      "result": "Result#8ed9"
    }
  }
}
```

---

## TimeWarpLog#d938

```json
{
  "handle": "TimeWarpLog",
  "mechanism": "Events are not ordered by wall-clock time but by 'causal cones'. An {{agent}} accepts an event from the 'past' if it doesn't contradict its current causal cone. Allows for massive latency tolerance. Utilizes {{world_reversible}}, {{causal_barrier}}.",
  "gloss": "Handling relativistic event ordering",
  "failure_modes": [
    "User confusion about 'when' things happened."
  ],
  "invariants": [
    "Immutability: Past entries cannot be modified",
    "Indexability: Seek(Time T) returns deterministic {{state}}(T)",
    "Log immutable after write."
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
    "ring": 0
  },
  "sema_id": "sema:TimeWarpLog#mh:SHA-256:d9386c726ba1c96bfae61549b82b16d1137d59b1f2129a19a24568f3117a4720",
  "sema_ref": "TimeWarpLog#d938",
  "sema_stub": "d938",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "agent": "Agent#aaec",
      "state": "State#4d58",
      "causal_barrier": "CausalBarrier#0904",
      "world_reversible": "WorldReversible#f664"
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

## AuditTrail#ff66

```json
{
  "handle": "AuditTrail",
  "mechanism": "Every consequential {{agent}} action (state mutation, external call, delegation, decision) appends a {{sign}}ed entry to an immutable {{ledger}}. Each entry contains: timestamp, {{agent}} {{identity}}, action type, input hash, output hash, and the sema pattern invoked. Extends {{trace}} from single-entity lineage to cross-agent compliance logging. The trail is append-only \u2014 entries cannot be modified or deleted. For cross-agent auditing, individual trails are aggregated via Merkle roots into a shared {{snapshot}}, enabling any party to verify the complete history without accessing raw entries.",
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
    "Trace#9057(Ledger#c363)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 1,
    "tier": 1,
    "related": [
      "SpotAudit#6673"
    ]
  },
  "sema_ref": "AuditTrail#ff66",
  "sema_id": "sema:AuditTrail#mh:SHA-256:ff66d6d56fc4208d20e8bb1835ea9a04dc23269ced480e27c2cebb2f2fa6890c",
  "sema_stub": "ff66",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "sign": "Sign#1fb9",
      "ledger": "Ledger#c363",
      "trace": "Trace#9057",
      "agent": "Agent#aaec",
      "audit": "Audit#4044"
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
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## ExplainBeacon#6ced

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
  "sema_id": "sema:ExplainBeacon#mh:SHA-256:6ced8ee08e54722b06a3be6cbf6403580a90d3543b2122cbbfc815799f150530",
  "sema_ref": "ExplainBeacon#6ced",
  "sema_stub": "6ced",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "stream": "Stream#22f3",
      "greet": "Greet#7ad2",
      "heartbeat": "Heartbeat#7f88"
    }
  }
}
```

---

## HumanApprove#e64a

```json
{
  "handle": "HumanApprove",
  "mechanism": "A checkpoint gate where execution pauses and awaits explicit human approval before proceeding. The agent presents its proposed {{task}}, rationale, and risk assessment to a human operator. Only upon receiving affirmative consent does execution continue. Critical for high-stakes actions (financial transactions, deployments, irreversible changes).",
  "gloss": "Pause for human approval before critical actions",
  "parameters": [
    {
      "name": "challenge_required",
      "type": "Boolean",
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
    "ring": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "sema_id": "sema:HumanApprove#mh:SHA-256:e64a6a1fc261b726fbfdcae8b5d3a3da39e3ea2e8f2d168e1a4135985e36d7ea",
  "sema_ref": "HumanApprove#e64a",
  "sema_stub": "e64a",
  "dependencies": {
    "references": {
      "audit": "Audit#4044",
      "system": "System#e314",
      "context": "Context#510a"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## InputGuard#0770

```json
{
  "handle": "InputGuard",
  "mechanism": "A validation filter that sanitizes inputs before they reach a sensitive component. It enforces schema compliance, type safety, and constraint satisfaction. Upon violation, it triggers a fail-closed behavior, rejecting the input and logging the attempt.",
  "gloss": "Input validation and sanitization",
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Verification",
    "ring": 0
  },
  "sema_ref": "InputGuard#0770",
  "sema_id": "sema:InputGuard#mh:SHA-256:077022daa9665f3562ad8253b9b6c63ccf7e71d84b74ab48c44e6de421b8bdcb",
  "sema_stub": "0770",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e"
}
```

---

## OathBind#fe32

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
    "ring": 1
  },
  "sema_ref": "OathBind#fe32",
  "sema_id": "sema:OathBind#mh:SHA-256:fe321dda0ccc6b982e7cf8065bce7cd6d59f4e2cc3b0cd62f76153e47ebd1a37",
  "sema_stub": "fe32",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "rule_set": "RuleSet#8d85",
      "spot_audit": "SpotAudit#6673",
      "actor": "Actor#6926"
    }
  }
}
```

---

## OutputGuard#eb44

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
  "sema_category": "Verification#9c1e",
  "sema_id": "sema:OutputGuard#mh:SHA-256:eb44b7e751219a94f752bb8827843ede1045bc1a4195d9d0db3648f9ae097bb0",
  "sema_ref": "OutputGuard#eb44",
  "sema_stub": "eb44",
  "dependencies": {
    "accepts": {
      "solution": "Solution#7186"
    },
    "references": {
      "problem": "Problem#5baa",
      "context": "Context#510a"
    }
  }
}
```

---

## SpotAudit#6673

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
  "sema_id": "sema:SpotAudit#mh:SHA-256:66730b2af0aece3adb72ca9e81b48085fc3654642b14cf82f3d8d2ae4890396d",
  "sema_ref": "SpotAudit#6673",
  "sema_stub": "6673",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "state_audit": "StateAudit#ce13",
      "audit": "Audit#4044"
    }
  }
}
```

---

## Validate#3de2

```json
{
  "handle": "Validate",
  "mechanism": "Syntactic Verification. Checks if a data artifact conforms to a predefined structure (Schema) or set of constraints. Rejects malformed inputs before processing. Utilizes {{accept_spec}}. Distinct from {{check}} (Logic Gate) and quality scoring (Judge).",
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
  "sema_id": "sema:Validate#mh:SHA-256:3de24fbfc5dade5aeabd857010aaeff7529bdab8c152f164897aa411d868c619",
  "sema_ref": "Validate#3de2",
  "sema_stub": "3de2",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9c1e",
  "dependencies": {
    "references": {
      "check": "Check#1544",
      "accept_spec": "AcceptSpec#70dd"
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
      "BayesUpdate#911b"
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

## BayesUpdate#911b

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
  "sema_id": "sema:BayesUpdate#mh:SHA-256:911b3e915019f09fbbbde387283af064db0903ce67a7219b0f27730c236de487",
  "sema_ref": "BayesUpdate#911b",
  "sema_stub": "911b",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "belief": "Belief#5ad9",
      "observe": "Observe#8ebd",
      "base_rate_include": "BaseRateInclude#aa0b"
    }
  }
}
```

---

## BreadthGovernor#d220

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
    "ring": 0
  },
  "sema_id": "sema:BreadthGovernor#mh:SHA-256:d22009d16f04fac6c9adfeb2ccfe15290aeb9def95ddd4328b21344555c21169",
  "sema_ref": "BreadthGovernor#d220",
  "sema_stub": "d220",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "decompose": "Decompose#ac56",
      "value": "Value#3c5d",
      "parsimony": "Parsimony#1dd3",
      "context": "Context#510a",
      "prophet_fan_out": "ProphetFanOut#2d81",
      "budget": "Budget#a763",
      "parallel": "Parallel#6272"
    }
  }
}
```

---

## ConfidenceCalibrate#0ae5

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
  "sema_id": "sema:ConfidenceCalibrate#mh:SHA-256:0ae5f1a670925e132d49a7d8fd9abc773a598b53dbd0cb734d8081d23e5cdc60",
  "sema_ref": "ConfidenceCalibrate#0ae5",
  "sema_stub": "0ae5",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "bayes_update": "BayesUpdate#911b",
      "agent": "Agent#aaec",
      "base_rate_include": "BaseRateInclude#aa0b"
    }
  }
}
```

---

## ConfirmationBlock#3dae

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
      "name": "confirmations_required",
      "type": "Integer",
      "range": "[1, 100]",
      "description": "Blocks before finality"
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
      "DissentSeek#bd28"
    ]
  },
  "sema_id": "sema:ConfirmationBlock#mh:SHA-256:3daea9633d69418a61fe6cca9416ab47156bef6d7b594a2c7be753b06205dadf",
  "sema_ref": "ConfirmationBlock#3dae",
  "sema_stub": "3dae",
  "sema_layer": "Mind",
  "sema_category": "Inference"
}
```

---

## ContextFirst#24d6

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
  "sema_id": "sema:ContextFirst#mh:SHA-256:24d61661da4fdd47439391c52464eeea2c403a84cf5fc4da86f06b932579946b",
  "sema_ref": "ContextFirst#24d6",
  "sema_stub": "24d6",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Prioritize#dd16(Context#510a)"
  ],
  "dependencies": {
    "references": {
      "prioritize": "Prioritize#dd16",
      "warmup": "Warmup#28c4",
      "solver_node": "SolverNode#3a4f",
      "agent": "Agent#aaec",
      "context": "Context#510a",
      "state": "State#4d58"
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
      "ConfidenceCalibrate#0ae5"
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

## HindsightBlock#bdb6

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
    "ring": 0
  },
  "sema_id": "sema:HindsightBlock#mh:SHA-256:bdb602218783e07b6eb5e68e900635bcd80e7b6d2ff32ac26ec03e383837f363",
  "sema_ref": "HindsightBlock#bdb6",
  "sema_stub": "bdb6",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "outcome": "Outcome#38e0",
      "decision": "Decision#acfb",
      "judge": "Judge#d84f",
      "pre_mortem": "PreMortem#f69d"
    }
  }
}
```

---

## LayeredCheck#3fad

```json
{
  "handle": "LayeredCheck",
  "mechanism": "A {{check}} strategy that evaluates constraints in a strict {{hierarchy}} of abstraction (e.g., existence -> {{validate}} (schema) -> {{understand}} (semantics)). It uses a {{sequence}} of {{gate}}s where lower-level failures halt execution immediately, preventing resource waste on higher-level checks for fundamentally broken inputs.",
  "gloss": "Hierarchical verification strategy",
  "signature": [
    "Check#1544(Hierarchy#aa9b)"
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
      "PURECheck#3ebb"
    ]
  },
  "sema_ref": "LayeredCheck#3fad",
  "sema_id": "sema:LayeredCheck#mh:SHA-256:3fad5e7a1a45108d71e962e4186b7ad170660f00d4cfca98d272238c3ad5d3d0",
  "sema_stub": "3fad",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "understand": "Understand#96d4",
      "hierarchy": "Hierarchy#aa9b",
      "validate": "Validate#3de2"
    },
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "check": "Check#1544",
      "gate": "Gate#206d"
    }
  }
}
```

---

## NormCheck#8222

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
    "ring": 0
  },
  "sema_id": "sema:NormCheck#mh:SHA-256:82223036f2aa91c261189aa21bb0a61a98d10cfb6f613eaf760e8635af2e30e7",
  "sema_ref": "NormCheck#8222",
  "sema_stub": "8222",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Check#1544(Value#3c5d)"
  ],
  "dependencies": {
    "references": {
      "normative_judge": "NormativeJudge#2316",
      "quorum": "Quorum#29b4",
      "value": "Value#3c5d",
      "judge": "Judge#d84f",
      "prophet_fan_out": "ProphetFanOut#2d81",
      "check": "Check#1544"
    }
  }
}
```

---

## NormativeJudge#2316

```json
{
  "handle": "NormativeJudge",
  "mechanism": "A purely normative {{judge}} module that evaluates static world-states against a weighted {{value}} function. To mitigate Goodhart's Law, this pattern should be deployed as an ENSEMBLE (Jury), where multiple judges with slightly perturbed {{value}} constitutions reach {{quorum}} on the {{outcome}}. It aggregates {{value}}s via {{perspective_ensemble}}, optionally escalating to {{human_approve}} for ambiguous edge cases.",
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
    },
    {
      "name": "weights",
      "type": "Map<Value#3c5d, Float>",
      "range": "unspecified",
      "description": "Relative importance weights per value dimension"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Inference",
    "ring": 0
  },
  "sema_id": "sema:NormativeJudge#mh:SHA-256:2316a736f6aa6939da6a9d20e0a1103958d0241ab103f5de8a0e61fba5d9e87a",
  "sema_ref": "NormativeJudge#2316",
  "sema_stub": "2316",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Judge#d84f(Value#3c5d)"
  ],
  "dependencies": {
    "references": {
      "quorum": "Quorum#29b4",
      "outcome": "Outcome#38e0",
      "judge": "Judge#d84f",
      "value": "Value#3c5d",
      "state": "State#4d58",
      "human_approve": "HumanApprove#e64a"
    },
    "composes_with": {
      "perspective_ensemble": "PerspectiveEnsemble#2927"
    }
  }
}
```

---

## OntologyAdapt#e673

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
  "sema_id": "sema:OntologyAdapt#mh:SHA-256:e67338652fa9214a713c8b4bc8f1ff1173a080090e84e8ca157f5e071f772a38",
  "sema_ref": "OntologyAdapt#e673",
  "sema_stub": "e673",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "anomaly": "Anomaly#7987",
      "category": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1",
      "agent": "Agent#aaec",
      "ontology_handshake": "OntologyHandshake#ead0",
      "noise": "Noise#c4b4"
    }
  }
}
```

---

## ProphetFanOut#2d81

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
  "sema_id": "sema:ProphetFanOut#mh:SHA-256:2d8110366b23afc261111d62bb567f6b88fc45f1019b9ba96b249ded6f6232fa",
  "sema_ref": "ProphetFanOut#2d81",
  "sema_stub": "2d81",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "chain": "Chain#5711",
      "aggregate": "Aggregate#af54",
      "quorum": "Quorum#29b4"
    }
  }
}
```

---

## RegimeSense#3e24

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
  "sema_id": "sema:RegimeSense#mh:SHA-256:3e24672befbaea7607da15aa4b7c75517cb16f68a055fda352841e76469e4ead",
  "sema_ref": "RegimeSense#3e24",
  "sema_stub": "3e24",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "break": "Break#1a63",
      "quorum": "Quorum#29b4",
      "agent": "Agent#aaec",
      "ontology_adapt": "OntologyAdapt#e673",
      "drift_watch": "DriftWatch#a20d",
      "noise": "Noise#c4b4"
    }
  }
}
```

---

## ScopeFreeze#d8c1

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
      "range": "{Reject, Queue#2ec3, CostAnalysis}",
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
    "ring": 0
  },
  "sema_id": "sema:ScopeFreeze#mh:SHA-256:d8c15a8a91ccbfcdb54d00cb1c4a386969867716b402ae638e5822742cd1d2d4",
  "sema_ref": "ScopeFreeze#d8c1",
  "sema_stub": "d8c1",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "satisfice": "Satisfice#9161",
      "decompose": "Decompose#ac56",
      "transition": "Transition#072d",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "timebox_think": "TimeboxThink#2656",
      "accept_spec": "AcceptSpec#70dd"
    }
  }
}
```

---

## SemanticTabu#82dd

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
    "ring": 0
  },
  "sema_id": "sema:SemanticTabu#mh:SHA-256:82dd562ed60295db85be7b4dee32caf80fea5c78f6b3930c7f316f2a693e9176",
  "sema_ref": "SemanticTabu#82dd",
  "sema_stub": "82dd",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solution": "Solution#7186",
      "trace": "Trace#9057"
    }
  }
}
```

---

## SurprisalUpdate#6ef1

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
      "BayesUpdate#911b"
    ],
    "ring": 2
  },
  "sema_id": "sema:SurprisalUpdate#mh:SHA-256:6ef19d8b61ce228bbc61a34496b878f1e060e56790f48606fc4e81b3b8594fca",
  "sema_ref": "SurprisalUpdate#6ef1",
  "sema_stub": "6ef1",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "epistemic_roi": "EpistemicROI#742a",
      "regime_sense": "RegimeSense#3e24"
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

## BeliefTracking#65b5

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
      "BayesUpdate#911b"
    ],
    "ring": 2
  },
  "sema_id": "sema:BeliefTracking#mh:SHA-256:65b5f43b911ac5cf11622c6e4c4fa89457541630ec72f1f387394d5ad8afff14",
  "sema_ref": "BeliefTracking#65b5",
  "sema_stub": "65b5",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "surprisal_update": "SurprisalUpdate#6ef1",
      "belief": "Belief#5ad9",
      "cognitive_bias": "CognitiveBias#4b32"
    }
  }
}
```

---

## Cache#1ea9

```json
{
  "handle": "Cache",
  "mechanism": "A temporary high-speed storage layer for keeping frequently accessed {{datum}} or {{state}}. It enables {{heuristic_snap}} by bypassing re-computation.",
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
  "sema_id": "sema:Cache#mh:SHA-256:1ea9ba40ef01b9f6072ae6bb93d37096c11655bb43a5bebe172d50365dde1073",
  "sema_ref": "Cache#1ea9",
  "sema_stub": "1ea9",
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
      "state": "State#4d58",
      "heuristic_snap": "HeuristicSnap#cece",
      "datum": "Datum#31cf"
    }
  }
}
```

---

## ChunkMerge#ded6

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
  "sema_id": "sema:ChunkMerge#mh:SHA-256:ded6bbc1fcb067eaef0990ace28b3db2e0337744edac4e75c1da2ee1bbe3c351",
  "sema_ref": "ChunkMerge#ded6",
  "sema_stub": "ded6",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "compress": "Compress#0967",
      "aggregate": "Aggregate#af54",
      "hierarchy": "Hierarchy#aa9b"
    }
  }
}
```

---

## ContextCompress#6dbd

```json
{
  "handle": "ContextCompress",
  "mechanism": "A memory management primitive that uses {{compress}} to reduce the token footprint of a {{context}} while preserving critical {{state}}. It explicitly retains active {{constraint}}s and unresolved goals.",
  "gloss": "Semantic compression for long-running contexts",
  "sema_id": "sema:ContextCompress#mh:SHA-256:6dbdad39d305207e19f80a38fbb7622505d35259338335493053eb49cfe4d817",
  "sema_ref": "ContextCompress#6dbd",
  "sema_stub": "6dbd",
  "_meta": {
    "layer": "Mind",
    "category": "Memory",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "signature": [
    "Compress#0967(Context#510a)"
  ],
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

## ExperienceSharding#d920

```json
{
  "handle": "ExperienceSharding",
  "mechanism": "Applies the {{shard}} primitive to agent memory. When context fills, the agent splits into two specialized agents (active vs archival) rather than forgetting. It segments history into discrete blocks via {{chunk_merge}} before distributing them across the agent cluster.",
  "gloss": "A single agent evolves into a colony of specialists preserving total history.",
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
      "FabricSharding#7399"
    ],
    "ring": 0
  },
  "sema_id": "sema:ExperienceSharding#mh:SHA-256:d9208f9cae52b448379b20118d47ed597e138e0a1015adc03598d65699d2dd8f",
  "sema_ref": "ExperienceSharding#d920",
  "sema_stub": "d920",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "chunk_merge": "ChunkMerge#ded6",
      "shard": "Shard#1e74"
    }
  }
}
```

---

## HolographicShard#1352

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
  "sema_id": "sema:HolographicShard#mh:SHA-256:13529590ca2770a776edbe88e378a084a228c0e4d23e5d1266f284697fa2a22f",
  "sema_ref": "HolographicShard#1352",
  "sema_stub": "1352",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "fabric_sharding": "FabricSharding#7399",
      "deep": "Deep#89f0",
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

## RetrievalAugment#ca58

```json
{
  "handle": "RetrievalAugment",
  "mechanism": "Before generating a response, the {{agent}} queries an external knowledge store (vector database, search index, knowledge graph) to retrieve relevant {{context}}. Retrieved documents are injected into the {{prompt}}, grounding the response in external facts rather than relying solely on parametric memory. The canonical RAG (Retrieval-Augmented Generation) pattern. It injects external {{context}} into the {{chain_of_thought}}, grounding the reasoning process in retrieved facts.",
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
      "DeepResearch#cbe3"
    ],
    "ring": 2
  },
  "sema_id": "sema:RetrievalAugment#mh:SHA-256:ca586b1cfff0f1d6db36de4ef419b29d21e55e8382db24b435fe9bb00ad32241",
  "sema_ref": "RetrievalAugment#ca58",
  "sema_stub": "ca58",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "prompt": "Prompt#5ded",
      "chain_of_thought": "ChainOfThought#6201",
      "context": "Context#510a"
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
    "ring": 0
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

## Abduction#fe2b

```json
{
  "handle": "Abduction",
  "mechanism": "The 'best guess' based on incomplete observation. Inference to the best explanation. (The grass is wet -> It probably rained). Triggers {{hypothesis}} generation.",
  "gloss": "Inference to best explanation",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Abduction#mh:SHA-256:fe2b40824246fd245dec338d1615e791787806b540b9376aae5fac14c48ce02b",
  "sema_ref": "Abduction#fe2b",
  "sema_stub": "fe2b",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#e95b"
    }
  }
}
```

---

## AbductiveLeap#1069

```json
{
  "handle": "AbductiveLeap",
  "mechanism": "Inference to Best Explanation: Given surprising observation, generate candidate explanations. {{rank}} by simplicity, scope, and coherence with existing knowledge. Adopt highest-ranked as working hypothesis. Flag as provisional, not proven. It employs {{chain_of_thought}} to trace the reasoning path from observation to explanation, ensuring the logical leap is explicit and verifiable.",
  "gloss": "Inference to the best explanation",
  "failure_modes": [
    "Conspiracy Thinking: Preferring complex, coherent explanations over simple, messy ones (overfitting the narrative)."
  ],
  "invariants": [
    "Explanation must cover all observed anomalies",
    "Simplicity heuristic (Occam's Razor) applied"
  ],
  "preconditions": [
    "No deductive path to explanation",
    "Set of observations"
  ],
  "postconditions": [
    "{{hypothesis}} generated",
    "{{hypothesis}} ranked by likelihood"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "related": [
      "HypothesisLadder#b8cd"
    ],
    "ring": 2
  },
  "sema_id": "sema:AbductiveLeap#mh:SHA-256:1069501989760c74143a80a2a2ee3267463e206d8998c76d38399c2498e8791d",
  "sema_ref": "AbductiveLeap#1069",
  "sema_stub": "1069",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "chain_of_thought": "ChainOfThought#6201"
    },
    "references": {
      "rank": "Rank#cb98",
      "hypothesis": "Hypothesis#e95b"
    }
  }
}
```

---

## BackwardChain#0484

```json
{
  "handle": "BackwardChain",
  "mechanism": "Goal-First Decomposition: Start from desired end-state, recursively identify prerequisites. For each prerequisite, ask \"what must be true for this to hold?\" until reaching known facts or actionable steps. Execution order is reverse of discovery order. It structures the {{chain_of_thought}} in reverse chronological order, linking the desired future state to present preconditions.",
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
  "sema_id": "sema:BackwardChain#mh:SHA-256:04841f7ca3e84925caa3e0480d39467e3707e7fdf8eefe3650177c25fbd4c43b",
  "sema_ref": "BackwardChain#0484",
  "sema_stub": "0484",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2",
      "chain": "Chain#5711",
      "chain_of_thought": "ChainOfThought#6201"
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

## ChainOfThought#6201

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
      "ReAct#c720"
    ],
    "ring": 2
  },
  "sema_id": "sema:ChainOfThought#mh:SHA-256:620185e6502cb8b2ac69fcdd94243e5ccfa2f54d3d34524dcf26a1c81662294c",
  "sema_ref": "ChainOfThought#6201",
  "sema_stub": "6201",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Chain#5711)"
  ],
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "chain": "Chain#5711",
      "think": "Think#e1bd"
    },
    "composes_with": {
      "reflexion": "Reflexion#51b9",
      "step_back": "StepBack#b079"
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

## Decompose#ac56

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
  "sema_ref": "Decompose#ac56",
  "sema_id": "sema:Decompose#mh:SHA-256:ac569dd49b1b2d91a5f03640f30b0c0fd658b3c6a46788d46fd734760c5281a4",
  "sema_stub": "ac56",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "solution": "Solution#7186",
      "strategy": "Strategy#47a4",
      "problem": "Problem#5baa"
    },
    "accepts": {
      "task": "Task#d9f9"
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

## Dialectic#bc18

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
  "sema_id": "sema:Dialectic#mh:SHA-256:bc186b7126746e11187381e73aa67e712c6f0cfb87e47fd3ef9b090a60bee242",
  "sema_ref": "Dialectic#bc18",
  "sema_stub": "bc18",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "steelman_check": "SteelmanCheck#4f4c"
    },
    "references": {
      "perspective_ensemble": "PerspectiveEnsemble#2927",
      "synthesis": "Synthesis#3252"
    }
  }
}
```

---

## Eliminate#43ea

```json
{
  "handle": "Eliminate",
  "mechanism": "Systematic Exclusion: Enumerate all possible answers. For each, find a test that could falsify it. Apply tests in order of cost (cheapest first). Remove falsified options. Continue until one remains or no tests left. Remaining options are candidates. It uses {{prioritize}} to order falsification tests by cost/efficiency before executing them.",
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
  "sema_ref": "Eliminate#43ea",
  "sema_id": "sema:Eliminate#mh:SHA-256:43ea687e3560a55f221807138469697a6f331e687fa542c66ddf4d97f07174b0",
  "sema_stub": "43ea",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "prioritize": "Prioritize#dd16",
      "option": "Option#483e"
    }
  }
}
```

---

## Estimate#bb30

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
  "sema_ref": "Estimate#bb30",
  "sema_id": "sema:Estimate#mh:SHA-256:bb3078fc4f974c17821e162f0034230b653c9ebd70c4655e86924d1292b1d449",
  "sema_stub": "bb30",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "accepts": {
      "task": "Task#d9f9"
    },
    "references": {
      "simulation": "Simulation#8035",
      "value": "Value#3c5d",
      "heuristic_snap": "HeuristicSnap#cece"
    },
    "yields": {
      "bid": "Bid#cf07"
    },
    "composes_with": {
      "think": "Think#e1bd"
    }
  }
}
```

---

## ExtendedThinking#ca3c

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
  "sema_id": "sema:ExtendedThinking#mh:SHA-256:ca3c54e46218935876ca5c993974742069fe61871fae7af38a2fef745753dc98",
  "sema_ref": "ExtendedThinking#ca3c",
  "sema_stub": "ca3c",
  "dependencies": {
    "references": {
      "chain": "Chain#5711"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## FirstPrinciples#c379

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
  "sema_id": "sema:FirstPrinciples#mh:SHA-256:c379f7e5629befb5ccbee33b6fccbc3c4f5ec181b2704c4f82064d5cdc810f61",
  "sema_ref": "FirstPrinciples#c379",
  "sema_stub": "c379",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "assumption": "Assumption#efb5",
      "axiom": "Axiom#5012",
      "chain_of_thought": "ChainOfThought#6201"
    }
  }
}
```

---

## Generalize#17c9

```json
{
  "handle": "Generalize",
  "mechanism": "Pattern Extraction: Given multiple instances, identify shared structure. Replace specific values with variables. {{state}} the invariant that holds across all instances. Test: does pattern predict behavior of new instances? Refine until predictive. It employs {{analogy_bridge}} to map specific instances to abstract schemata, validating the invariant across the set.",
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
      "Specialize#0a09"
    ],
    "ring": 2
  },
  "sema_id": "sema:Generalize#mh:SHA-256:17c94171f5f8f82695fc6dfb89eac6aad8adedf46545e3d48e799056ec132941",
  "sema_ref": "Generalize#17c9",
  "sema_stub": "17c9",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "analogy_bridge": "AnalogyBridge#bff7"
    }
  }
}
```

---

## HeuristicSnap#cece

```json
{
  "handle": "HeuristicSnap",
  "mechanism": "Fast pattern matching against a 'cached experience' database. Returns a decision in <100ms based on similarity to past success, bypassing expensive reasoning chains. It bypasses the expensive {{chain_of_thought}} when {{budget}} is low, relying on cached pattern matches.",
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
      "ThinSlice#debb"
    ],
    "ring": 2
  },
  "sema_id": "sema:HeuristicSnap#mh:SHA-256:cece62377b8243be6d0ec0c4722f30e61aac251b2f9f3ee5cd30b06456ff2329",
  "sema_ref": "HeuristicSnap#cece",
  "sema_stub": "cece",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "budget": "Budget#a763",
      "decision": "Decision#acfb",
      "chain_of_thought": "ChainOfThought#6201",
      "problem": "Problem#5baa"
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
    "composes_with": {
      "context": "Context#510a",
      "think": "Think#e1bd"
    },
    "yields": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## Invert#d1b9

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
  "sema_id": "sema:Invert#mh:SHA-256:d1b9169d5b598e4f7f3d4d58bc2feea0f45c7830b32445fa6ab2666db271fa42",
  "sema_ref": "Invert#d1b9",
  "sema_stub": "d1b9",
  "dependencies": {
    "accepts": {
      "solution": "Solution#7186"
    },
    "references": {
      "state": "State#4d58",
      "reframe": "Reframe#ba00",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## LeastToMost#bd38

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
      "RecursionDive#4ce3"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:LeastToMost#mh:SHA-256:bd389eddb2f1b893221ab2a7479cb0293f1808057a52ef702b3ff6228509db26",
  "sema_ref": "LeastToMost#bd38",
  "sema_stub": "bd38",
  "dependencies": {
    "references": {
      "decompose": "Decompose#ac56",
      "solution": "Solution#7186"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Parsimony#1dd3

```json
{
  "handle": "Parsimony",
  "mechanism": "Acts as a {{judge}} to evaluate {{topology}} necessity (Occam's Razor). Classifies complexity into three qualitative states: (1) Bloated: Core concept collapses or remains identical without this component. (2) Under-specified: Plausible utility, but necessity is not strictly proven via ablation. (3) Minimal: Proven essential; removing any part destroys the function. Aims for high {{compress}}ion.",
  "invariants": [
    "Necessity: Every component must have a causal link to the outcome."
  ],
  "signature": [
    "Judge#d84f(Topology#2408)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Parsimony#mh:SHA-256:1dd3e7108871db29b025e6266ad9f1ad39ba1d005a2d25a010be18e57f0f879c",
  "sema_ref": "Parsimony#1dd3",
  "sema_stub": "1dd3",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "gloss": "Complexity justification via Occams Razor",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "judge": "Judge#d84f",
      "compress": "Compress#0967"
    }
  }
}
```

---

## Rank#cb98

```json
{
  "handle": "Rank",
  "mechanism": "Deterministic Sort. Applies a scoring function to every element in the input Set. Returns a List ordered by Score, using {{select}} to truncate to Top-K.",
  "gloss": "Order items by score",
  "failure_modes": [
    "Score Indeterminacy: Multiple items have identical scores.",
    "Incomparability: Scoring function returns values that cannot be strictly ordered."
  ],
  "invariants": [
    "Conservation: Output set is a subset of Input set.",
    "Monotonicity: For all i, Score(Output[i]) >= Score(Output[i+1])."
  ],
  "sema_id": "sema:Rank#mh:SHA-256:cb98b1357a2b6e14ff1e76bca44014fabffb0936b453ba88c3ad4561a63d3c2f",
  "sema_ref": "Rank#cb98",
  "sema_stub": "cb98",
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 0
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "select": "Select#15c2"
    }
  }
}
```

---

## ReAct#c720

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
      "Reflexion#51b9"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ReAct#mh:SHA-256:c72018c3dbdfe960eadd257f10dfd88400a405cfd2be557977fc0e81bcae8062",
  "sema_ref": "ReAct#c720",
  "sema_stub": "c720",
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e",
      "cognitive_bias": "CognitiveBias#4b32",
      "agent": "Agent#aaec",
      "chain": "Chain#5711"
    },
    "composes_with": {
      "tool_invoke": "ToolInvoke#cf0a"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Reason#3f24

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
      "ChainOfThought#6201",
      "TreeOfThoughts#581a"
    ]
  },
  "sema_id": "sema:Reason#mh:SHA-256:3f246e05b685e54ff927fc1f0ccba1be64078d8aab649145440940a25ceed846",
  "sema_ref": "Reason#3f24",
  "sema_stub": "3f24",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "compute_budget": "ComputeBudget#3b98",
      "chain": "Chain#5711",
      "tree": "Tree#ddce"
    },
    "accepts": {
      "context": "Context#510a"
    },
    "composes_with": {
      "think": "Think#e1bd"
    }
  }
}
```

---

## RecursionDive#4ce3

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
  "sema_id": "sema:RecursionDive#mh:SHA-256:4ce3c240b0b3ed97f14cbaeecdea77386bcdcaf392d47da437d7a8b5a8584b90",
  "sema_ref": "RecursionDive#4ce3",
  "sema_stub": "4ce3",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "solver_tree": "SolverTree#0f1d",
      "solver_node": "SolverNode#3a4f"
    },
    "composes_with": {
      "decompose": "Decompose#ac56"
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
      "RecursionDive#4ce3"
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
      "state": "State#4d58",
      "trace": "Trace#9057"
    }
  }
}
```

---

## Refine#38d9

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
      "PhasedRefinement#4a90"
    ]
  },
  "sema_id": "sema:Refine#mh:SHA-256:38d97579c85cbeb7c482df7f4ae6266cd92e70b0174057eeb6530570009f139d",
  "sema_ref": "Refine#38d9",
  "sema_stub": "38d9",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "act": "Act#5d55"
    },
    "references": {
      "incongruity": "Incongruity#e98f",
      "critique": "Critique#3e00",
      "artifact": "Artifact#6254",
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## Reflexion#51b9

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
      "EvaluatorOptimizer#7ec6"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Reflexion#mh:SHA-256:51b91d2cdfeb6aed5ea3293154279d16af2c98b0c473e731066198b5d4d43e7f",
  "sema_ref": "Reflexion#51b9",
  "sema_stub": "51b9",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2",
      "outcome": "Outcome#38e0",
      "critique": "Critique#3e00",
      "scratchpad": "Scratchpad#75bf",
      "goal": "Goal#456a"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Reframe#ba00

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
  "sema_id": "sema:Reframe#mh:SHA-256:ba00c40311ec71aab4f5942fcdd6876df95b15604cf54260182737e21a874dc9",
  "sema_ref": "Reframe#ba00",
  "sema_stub": "ba00",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "problem": "Problem#5baa"
    }
  }
}
```

---

## SelfConsistency#543d

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
  "sema_ref": "SelfConsistency#543d",
  "sema_id": "sema:SelfConsistency#mh:SHA-256:543df3dae7e7343a60ce588b0dac22883ec50c8ae0816ea6b25cb697f238cd7d",
  "sema_stub": "543d",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#af54"
    }
  }
}
```

---

## SkeletonOfThought#d99a

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
  "sema_id": "sema:SkeletonOfThought#mh:SHA-256:d99ac47fca9164a2de7b43196ce9c8455ab430b31b1c34928bddba952002cda4",
  "sema_ref": "SkeletonOfThought#d99a",
  "sema_stub": "d99a",
  "signature": [
    "Think#e1bd(Skeleton#c363)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#e1bd",
      "decompose": "Decompose#ac56",
      "skeleton": "Skeleton#c363"
    }
  }
}
```

---

## SocraticLoop#70fc

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
  "sema_id": "sema:SocraticLoop#mh:SHA-256:70fcba46b7510f6f8714fc119564272f465c3aa17d49785d57a97c9b5294a6c0",
  "sema_ref": "SocraticLoop#70fc",
  "sema_stub": "70fc",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "prompt": "Prompt#5ded",
      "dialectic": "Dialectic#bc18",
      "loop": "Loop#fb2e"
    }
  }
}
```

---

## Specialize#0a09

```json
{
  "handle": "Specialize",
  "mechanism": "Concrete Instantiation: Given abstract principle, substitute specific values for variables. {{check}} all constraints still hold after substitution. Generate multiple specializations to understand the principle\"s range. Edge cases reveal hidden assumptions. It applies the inverse of {{generalize}}, mapping abstract principles to concrete, context-specific instances.",
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
  "sema_id": "sema:Specialize#mh:SHA-256:0a0947c52834daad3a8c929cdafa2343ad43b044750fd6e27e233ff823005891",
  "sema_ref": "Specialize#0a09",
  "sema_stub": "0a09",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "check": "Check#1544",
      "generalize": "Generalize#17c9",
      "context": "Context#510a"
    }
  }
}
```

---

## SteelmanCheck#4f4c

```json
{
  "handle": "SteelmanCheck",
  "mechanism": "Before finalizing a {{decision}} or output, the {{agent}} MUST generate the strongest possible argument against its own conclusion. It performs a {{check}} on the {{robustness}} of the claim and a {{critique}} of the underlying {{belief}}. If the counter-argument exceeds a validity threshold, the decision is discarded or revised. It prevents confirmation {{cognitive_bias}}. Utilizes {{compatibility_check}}. For adversarial contexts, see adversarial steelmanning.",
  "gloss": "Mandatory counter-argument generation",
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
      "AdversarialSteel#35f0"
    ]
  },
  "sema_id": "sema:SteelmanCheck#mh:SHA-256:4f4ce8aca096c50b21c598a587b4b93cb3a2952114bac7c9ff1711786085f3b7",
  "sema_ref": "SteelmanCheck#4f4c",
  "sema_stub": "4f4c",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Check#1544(Robustness#132c)",
    "Critique#3e00(Belief#5ad9)"
  ],
  "dependencies": {
    "references": {
      "belief": "Belief#5ad9",
      "loop": "Loop#fb2e",
      "compatibility_check": "CompatibilityCheck#3abb",
      "cognitive_bias": "CognitiveBias#4b32",
      "critique": "Critique#3e00",
      "agent": "Agent#aaec",
      "robustness": "Robustness#132c",
      "decision": "Decision#acfb",
      "check": "Check#1544"
    }
  }
}
```

---

## StepBack#b079

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
  "sema_id": "sema:StepBack#mh:SHA-256:b0799e81851e7cf503b84fcf260b81fa235cc829410fb0da67d5b8a4c1a4305a",
  "sema_ref": "StepBack#b079",
  "sema_stub": "b079",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Problem#5baa)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#e1bd",
      "reframe": "Reframe#ba00",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## StrategicReading#ef92

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
  "sema_ref": "StrategicReading#ef92",
  "sema_id": "sema:StrategicReading#mh:SHA-256:ef9282eb9e5d243105ed2f8016102f7653d1a9f3abc2215f08642695fa2a33bf",
  "sema_stub": "ef92",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "compute_budget": "ComputeBudget#3b98",
      "agent": "Agent#aaec",
      "tree": "Tree#ddce",
      "context": "Context#510a"
    }
  }
}
```

---

## Summarize#6a00

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
  "sema_id": "sema:Summarize#mh:SHA-256:6a000fd570638ecd8dd239be23317cf6b004e2f5ed784822f41f6658ee669c2c",
  "sema_ref": "Summarize#6a00",
  "sema_stub": "6a00",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "translate": "Translate#e75d",
      "compress": "Compress#0967",
      "value": "Value#3c5d",
      "artifact": "Artifact#6254"
    },
    "accepts": {
      "datum": "Datum#31cf"
    },
    "yields": {
      "summary": "Summary#310e"
    }
  }
}
```

---

## Synthesis#3252

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
  "sema_id": "sema:Synthesis#mh:SHA-256:3252f9a67ea7200bf8eea5adadba88dd1716d47c30a37e534cadcbfdc62ac797",
  "sema_ref": "Synthesis#3252",
  "sema_stub": "3252",
  "dependencies": {
    "references": {
      "critique": "Critique#3e00"
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
    "yields": {
      "datum": "Datum#31cf"
    },
    "accepts": {
      "context": "Context#510a"
    }
  }
}
```

---

## Translate#e75d

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
  "sema_id": "sema:Translate#mh:SHA-256:e75d4e97e738a7ae2a377d85a30ce4ed294160b55aa47b778e10424424817429",
  "sema_ref": "Translate#e75d",
  "sema_stub": "e75d",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "interpret": "Interpret#c9ee",
      "protocol": "Protocol#7e1c",
      "reversibility": "Reversibility#049f"
    },
    "accepts": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## TreeOfThoughts#581a

```json
{
  "handle": "TreeOfThoughts",
  "mechanism": "The canonical implementation of branching reasoning. Instantiates the '{{think}}' primitive with a branching '{{tree}}' topology. Enables exploration of multiple reasoning paths with backtracking or pruning. Utilizes {{tree}}, {{chain_of_thought}}, {{think}}.",
  "gloss": "Branching exploration (Macro for Think(Tree))",
  "parameters": [
    {
      "name": "breadth",
      "type": "Integer",
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
      "RecursionDive#4ce3"
    ],
    "ring": 2
  },
  "sema_id": "sema:TreeOfThoughts#mh:SHA-256:581a1251e9eb48d2d2d5871c6c94ea26094c4ec99c2aea33ab22d30d0a351ded",
  "sema_ref": "TreeOfThoughts#581a",
  "sema_stub": "581a",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#e1bd(Tree#ddce)"
  ],
  "dependencies": {
    "references": {
      "tree": "Tree#ddce",
      "chain_of_thought": "ChainOfThought#6201",
      "think": "Think#e1bd"
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

## Verification#9c1e

```json
{
  "handle": "Verification",
  "mechanism": "The cognitive process of confirming that a claim or {{artifact}} adheres to its {{spec}} or reality. Unlike open-ended inquiry, Verification yields a binary Truth value regarding an existing assertion via a {{check}}.",
  "gloss": "Confirming alignment with truth or spec",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 1
  },
  "sema_ref": "Verification#9c1e",
  "sema_id": "sema:Verification#mh:SHA-256:9c1ee918c6b8b8d7b787f5ef7ae908aa2ca37b1f9b5dace80fcf261a9c961001",
  "sema_stub": "9c1e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "check": "Check#1544",
      "spec": "Spec#436e"
    }
  }
}
```

---

## WhyClimb#156a

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
  "sema_id": "sema:WhyClimb#mh:SHA-256:156aa8762c7c0007b72d0869b470c7c9d31aaf19d0815e51b9bce872d925db4f",
  "sema_ref": "WhyClimb#156a",
  "sema_stub": "156a",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Reframe#ba00(Problem#5baa)"
  ],
  "dependencies": {
    "references": {
      "recursive_root_cause": "RecursiveRootCause#6dc1",
      "condition": "Condition#cbd5",
      "reframe": "Reframe#ba00",
      "solution": "Solution#7186",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## AdversarialSteel#35f0

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
    "ring": 1
  },
  "sema_id": "sema:AdversarialSteel#mh:SHA-256:35f025a1bfbbcbcf86d8d60889b3e1c08fa43a2d439b358c4021c83de2291234",
  "sema_ref": "AdversarialSteel#35f0",
  "sema_stub": "35f0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "compatibility_check": "CompatibilityCheck#3abb",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "judge": "Judge#d84f",
      "criteria": "Criteria#ef6b"
    },
    "composes_with": {
      "steelman_check": "SteelmanCheck#4f4c"
    }
  }
}
```

---

## Agent#aaec

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
  "sema_ref": "Agent#aaec",
  "sema_id": "sema:Agent#mh:SHA-256:aaec2a5607aaf2793622b522fa30ab36bf81cbefdb241b51e7d4d9c42f143073",
  "sema_stub": "aaec",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e",
      "identity": "Identity#626c",
      "actor": "Actor#6926",
      "trace": "Trace#9057",
      "metric": "Metric#8895",
      "state": "State#4d58",
      "goal": "Goal#456a"
    },
    "composes_with": {
      "act": "Act#5d55",
      "think": "Think#e1bd",
      "observe": "Observe#8ebd"
    }
  }
}
```

---

## AnalogyBridge#bff7

```json
{
  "handle": "AnalogyBridge",
  "mechanism": "To solve a novel {{problem}}, the {{agent}} explicitly searches its training data for a structural analogy in a different domain (e.g., 'This architecture problem is like an ant colony'). It maps the {{solution}} from the source domain to the target domain. It merges the structural properties of the source and target domains, identifying the isomorphic mapping.",
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
  "sema_id": "sema:AnalogyBridge#mh:SHA-256:bff72aff9bf79cea5090f67c99e353f967ccbd4a0069173748a043efc6ab14ef",
  "sema_ref": "AnalogyBridge#bff7",
  "sema_stub": "bff7",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "solution": "Solution#7186",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## AntifragileInversion#6b0e

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
    "ring": 0
  },
  "sema_id": "sema:AntifragileInversion#mh:SHA-256:6b0e65ef31a30941d43dd6af0708868326615ff610b5425aed564b306aae304c",
  "sema_ref": "AntifragileInversion#6b0e",
  "sema_stub": "6b0e",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "agent": "Agent#aaec",
      "variable": "Variable#179a",
      "vector": "Vector#c7c4",
      "reframe": "Reframe#ba00"
    }
  }
}
```

---

## BeamSearch#20cd

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
  "sema_id": "sema:BeamSearch#mh:SHA-256:20cd422474b7bb111d0b7a83c8d72b00f42a606aaef7f695a626c628472d3625",
  "sema_ref": "BeamSearch#20cd",
  "sema_stub": "20cd",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "rank": "Rank#cb98",
      "solver_node": "SolverNode#3a4f",
      "queue": "Queue#2ec3",
      "select": "Select#15c2"
    }
  }
}
```

---

## Bubble#eb9a

```json
{
  "handle": "Bubble",
  "mechanism": "Isolated sandbox where coordination is tried before committing to reality. Creator sends BUBBLE_CREATE: {participants, ttl (time-to-live), isolation_level, parent_bubble (for nesting)}. Participants JOIN to enter isolated context. Inside bubble: state changes are copy-on-write (snapshot isolation), resource acquisitions are soft-reservations (intent, not actual), messages to non-participants are queued (not sent). {{work}} proceeds normally but nothing affects real world. When ready, creator calls PREPARE (2-phase commit). Each participant responds READY (can commit) or ABORT (cannot). If ALL READY: COMMIT\u2014queued messages sent, state changes applied atomically, reservations converted to hard acquisitions. If ANY ABORT or TTL expires: ROLLBACK\u2014all tentative work discarded silently, no compensation needed. Nested bubbles commit to parent context, not real world; parent commit makes all nested work real. It enforces a {{constraint_first}} approach around the simulation context to ensure no side effects leak into the production environment.",
  "gloss": "Enable risk-free coordination experimentation through transactional isolation\u2014try before committing to reality",
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
  "sema_id": "sema:Bubble#mh:SHA-256:eb9a8441896625edfa7d41935d88120a27bf53db353082e49b0c6027d45e6142",
  "sema_ref": "Bubble#eb9a",
  "sema_stub": "eb9a",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "state": "State#4d58",
      "constraint_first": "ConstraintFirst#c7cb"
    }
  }
}
```

---

## Build#00f3

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
      "Simulation#8035",
      "DogfoodFirst#b595",
      "SacrificialProbe#1e16"
    ],
    "ring": 1
  },
  "sema_id": "sema:Build#mh:SHA-256:00f3e2cc017af17d5de5a121ddd38017635736aa54c5ef23ee43c84abe5ddab6",
  "sema_ref": "Build#00f3",
  "sema_stub": "00f3",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "signature": [
    "Act#5d55(Artifact#6254)"
  ],
  "dependencies": {
    "accepts": {
      "spec": "Spec#436e"
    },
    "references": {
      "plan": "Plan#64f2",
      "prototype": "Prototype#ff18",
      "act": "Act#5d55",
      "value": "Value#3c5d"
    },
    "yields": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## CognitiveSolver#c6a7

```json
{
  "handle": "CognitiveSolver",
  "mechanism": "The universal polymorphic atom of intelligence. A CognitiveSolver is any entity\u2014from a fleeting thought process to a complex swarm\u2014that implements the 5-Stage Cognitive Contract (Manifest via {{card}}, Execute, Question, Verify via {{validate}}, Feedback). It acts as a fractal node in the {{universal_solver_tree}}, accepting a {{task}} and using {{reason}} to orchestrate a lifecycle on a {{solver_node}}. It yields a {{solution}}, wrapping operations like {{tool_invoke}} with {{compute_budget}} checks, {{socratic_loop}} refinement, or {{reflexion}} for self-improvement.",
  "gloss": "The universal polymorphic atom of recursive intelligence",
  "failure_modes": [
    "Interface Non-Compliance: Solver fails to implement one of the 5 mandatory endpoints.",
    "Manifest Drift: Capabilities declared in Manifest do not match runtime behavior."
  ],
  "invariants": [
    "Polymorphism: External Runtime treats all Solvers identically via this Interface.",
    "Recursion: Solver must accept sub-tasks via the same Interface it exposes."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "related": [
      "EpistemicROI#742a",
      "RecursionDive#4ce3"
    ]
  },
  "sema_id": "sema:CognitiveSolver#mh:SHA-256:c6a72740ea71fb33da47f6d7e21504f2632bbc8130f6b81c82ae19e211ca4665",
  "sema_ref": "CognitiveSolver#c6a7",
  "sema_stub": "c6a7",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "composes_with": {
      "compute_budget": "ComputeBudget#3b98",
      "reason": "Reason#3f24",
      "tool_invoke": "ToolInvoke#cf0a",
      "socratic_loop": "SocraticLoop#70fc",
      "reflexion": "Reflexion#51b9"
    },
    "references": {
      "card": "Card#c9f0",
      "solver_node": "SolverNode#3a4f",
      "universal_solver_tree": "UniversalSolverTree#4d9c",
      "validate": "Validate#3de2"
    },
    "accepts": {
      "task": "Task#d9f9"
    },
    "yields": {
      "solution": "Solution#7186"
    }
  }
}
```

---

## ComputeBudget#3b98

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
      "type": "Integer",
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
      "OptimalStop#7439",
      "Satisfice#9161",
      "TimeboxThink#2656"
    ]
  },
  "sema_ref": "ComputeBudget#3b98",
  "sema_id": "sema:ComputeBudget#mh:SHA-256:3b9875661465a1a0cdc12e60774114d0ac69510b4fae677c81c47ea3a84b99b1",
  "sema_stub": "3b98",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "gate": "Gate#206d",
      "task": "Task#d9f9",
      "value": "Value#3c5d",
      "budget": "Budget#a763"
    }
  }
}
```

---

## ConceptBlend#22f2

```json
{
  "handle": "ConceptBlend",
  "mechanism": "Forcing the merger of two unrelated graph nodes to find a valid semantic path. Unlike analogy (A is like B), blending creates C (A + B). It extends {{analogy_bridge}} by not just mapping A to B, but fusing them to create C.",
  "gloss": "Combinatorial novelty generation",
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
  "sema_id": "sema:ConceptBlend#mh:SHA-256:22f28543dbe747212dc9f189bcd5b5b7b352eb540f8dbb92e8ac40181e8a7ae5",
  "sema_ref": "ConceptBlend#22f2",
  "sema_stub": "22f2",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "tri_gate": "TriGate#07fc",
      "realizable": "Realizable#cf00",
      "analogy_bridge": "AnalogyBridge#bff7"
    }
  }
}
```

---

## ContingencyPlan#61d3

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
  "sema_id": "sema:ContingencyPlan#mh:SHA-256:61d396e94e514a1e01842936992d29b0402f1f4010b00fabd77373bf810497b5",
  "sema_ref": "ContingencyPlan#61d3",
  "sema_stub": "61d3",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2",
      "retry": "Retry#d53d"
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
  "sema_category": "Strategy#47a4"
}
```

---

## CreativeBlend#cc91

```json
{
  "handle": "CreativeBlend",
  "derived_from": "Creative#5574",
  "gloss": "Generating novelty via combinatorial blending and noise",
  "signature": [
    "Strategy#47a4(Artifact#6254)"
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
  "sema_ref": "CreativeBlend#cc91",
  "sema_id": "sema:CreativeBlend#mh:SHA-256:cc9130dd92520118a4b6047b2544fa67126e7bf2c81285c792a2f9c6433c3e75",
  "sema_stub": "cc91",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "accepts": {
      "context": "Context#510a"
    },
    "yields": {
      "artifact": "Artifact#6254"
    },
    "references": {
      "value": "Value#3c5d",
      "strategy": "Strategy#47a4",
      "noise_injection": "NoiseInjection#0854",
      "novelty": "Novelty#51b5"
    },
    "composes_with": {
      "check": "Check#1544",
      "concept_blend": "ConceptBlend#22f2"
    }
  }
}
```

---

## Crystallize#af68

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
  "sema_id": "sema:Crystallize#mh:SHA-256:af6880166731e858e42937cb02d1b4517272853e6f6a2e1e98301fc4f2f0bede",
  "sema_ref": "Crystallize#af68",
  "sema_stub": "af68",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "decay": "Decay#a1d4",
      "transition": "Transition#072d",
      "agent": "Agent#aaec",
      "entropy_pump": "EntropyPump#b9ae",
      "state": "State#4d58",
      "constitution": "Constitution#863b",
      "resonate": "Resonate#99d9",
      "dampen": "Dampen#ff89"
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
  "sema_category": "Strategy#47a4"
}
```

---

## Defer#6460

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
  "sema_id": "sema:Defer#mh:SHA-256:6460dcc0c5f0fd94cc3bcb7ff9bb4fe5eee0b5e1d3ea588b73f762bd4843a6b3",
  "sema_ref": "Defer#6460",
  "sema_stub": "6460",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "prioritize": "Prioritize#dd16",
      "decision": "Decision#acfb",
      "task": "Task#d9f9",
      "context": "Context#510a",
      "state": "State#4d58"
    }
  }
}
```

---

## DepthGovernor#05fe

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
  "sema_id": "sema:DepthGovernor#mh:SHA-256:05fec60033838c9772628aec8d9b3c94ff4a7ef1193b13bbc7c16a4ef8cd0a9b",
  "sema_ref": "DepthGovernor#05fe",
  "sema_stub": "05fe",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2",
      "loop": "Loop#fb2e",
      "decompose": "Decompose#ac56",
      "recursion_dive": "RecursionDive#4ce3",
      "agent": "Agent#aaec",
      "condition": "Condition#cbd5",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## DesignArchitect#7f55

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
  "sema_ref": "DesignArchitect#7f55",
  "sema_id": "sema:DesignArchitect#mh:SHA-256:7f55e9a2e809f4c721e9c62db8a8582c9f6b2eca5d293649c328750583a09775",
  "sema_stub": "7f55",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "composes_with": {
      "pre_mortem": "PreMortem#f69d",
      "steelman_check": "SteelmanCheck#4f4c",
      "translate": "Translate#e75d",
      "strategy": "Strategy#47a4",
      "summarize": "Summarize#6a00"
    },
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#8cf7"
    }
  }
}
```

---

## EmpiricalTest#8f92

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
  "sema_id": "sema:EmpiricalTest#mh:SHA-256:8f92bb36b1520f702ecd4b4e9313c31dbaa7e3933a4a6c9b4690e3de25e32e28",
  "sema_ref": "EmpiricalTest#8f92",
  "sema_stub": "8f92",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "falsification": "Falsification#3e36",
      "validate": "Validate#3de2"
    }
  }
}
```

---

## EpistemicROI#742a

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
  "sema_category": "Strategy#47a4",
  "sema_id": "sema:EpistemicROI#mh:SHA-256:742adc7d76282f41c66582e1e780930e5f83f792084fa83ac9b01f510ecaf5b0",
  "sema_ref": "EpistemicROI#742a",
  "sema_stub": "742a",
  "dependencies": {
    "references": {
      "experiment": "Experiment#40e5",
      "compute_budget": "ComputeBudget#3b98",
      "cognitive_bias": "CognitiveBias#4b32",
      "act": "Act#5d55",
      "outcome": "Outcome#38e0",
      "decision": "Decision#acfb",
      "task": "Task#d9f9",
      "value": "Value#3c5d",
      "result": "Result#8ed9"
    }
  }
}
```

---

## EventReact#a0ef

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
    "ring": 0
  },
  "sema_id": "sema:EventReact#mh:SHA-256:a0ef747d97aabc453629d237c4d625d02c26d22515a3f958c1ab261c156a3b56",
  "sema_ref": "EventReact#a0ef",
  "sema_stub": "a0ef",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "re_act": "ReAct#c720"
    }
  }
}
```

---

## Experiment#40e5

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
  "sema_ref": "Experiment#40e5",
  "sema_id": "sema:Experiment#mh:SHA-256:40e5e923ead8721b039cd6afa4e49c864a5022483e1c3ff58a12d57fe9a87499",
  "sema_stub": "40e5",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "yields": {
      "solution": "Solution#7186"
    },
    "references": {
      "verification": "Verification#9c1e",
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## ExploreExploit#88b0

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
  "sema_id": "sema:ExploreExploit#mh:SHA-256:88b0c9b3824b0ab8a8fa33dbb75136563eae43481eb087e85f5db2e6db17f3de",
  "sema_ref": "ExploreExploit#88b0",
  "sema_stub": "88b0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "budget": "Budget#a763",
      "context": "Context#510a"
    }
  }
}
```

---

## Falsification#3e36

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
  "sema_id": "sema:Falsification#mh:SHA-256:3e368a58febe7fc02de81df5c2f1ae163c7bfe543200cb2dcbeb7cde50609929",
  "sema_ref": "Falsification#3e36",
  "sema_stub": "3e36",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#e95b",
      "observe": "Observe#8ebd",
      "incongruity": "Incongruity#e98f"
    }
  }
}
```

---

## HypothesisEngine#dec9

```json
{
  "handle": "HypothesisEngine",
  "mechanism": "The Scientific Method as a cognitive cycle. 1. {{discover}}({{hypothesis}}): Generate a candidate {{hypothesis}} (Explanation). 2. {{trace}}({{simulation}}): Simulate implications and log the lineage. 3. {{check}}(Consistency): {{validate}} against invariants. 4. {{stigmergy}}(Result): Publish the findings to the shared context. It cycles through {{discover}}, {{trace}}, and {{check}} to formalize the scientific loop, publishing validated models via {{stigmergy}}.",
  "gloss": "Automated scientific method",
  "_meta": {
    "tier": 3,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "sema_id": "sema:HypothesisEngine#mh:SHA-256:dec9b5fd325c2c8649b3447c1e927559b952451b1cea7a7429dd8f4b62366731",
  "sema_ref": "HypothesisEngine#dec9",
  "sema_stub": "dec9",
  "dependencies": {
    "references": {
      "trace": "Trace#9057",
      "simulation": "Simulation#8035",
      "hypothesis": "Hypothesis#e95b",
      "discover": "Discover#afa1",
      "check": "Check#1544",
      "stigmergy": "Stigmergy#f624",
      "validate": "Validate#3de2"
    }
  }
}
```

---

## HypothesisLadder#b8cd

```json
{
  "handle": "HypothesisLadder",
  "mechanism": "The agent explicitly lists its current hypotheses about the world state and assigns probabilities. As new data arrives, it updates these probabilities using {{bayes_update}}. It acts on the highest-probability {{hypothesis}} but keeps others alive. It structures {{abductive_leap}} into falsifiable rungs, climbing to higher certainty only when an {{experiment}} validates the current level.",
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
  "sema_id": "sema:HypothesisLadder#mh:SHA-256:b8cd4534d34515209818259fc96a079f2813f4673326b4b844d53780a3f5c4e1",
  "sema_ref": "HypothesisLadder#b8cd",
  "sema_stub": "b8cd",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "bayes_update": "BayesUpdate#911b",
      "abductive_leap": "AbductiveLeap#1069",
      "hypothesis": "Hypothesis#e95b"
    },
    "composes_with": {
      "experiment": "Experiment#40e5"
    }
  }
}
```

---

## Jester#bc50

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
  "sema_id": "sema:Jester#mh:SHA-256:bc5045fce9b9265838e8e9e8df40d00bab11be85752235307be0dc403ee5abae",
  "sema_ref": "Jester#bc50",
  "sema_stub": "bc50",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "critique": "Critique#3e00",
      "incongruity": "Incongruity#e98f",
      "break": "Break#1a63"
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
  "sema_category": "Strategy#47a4"
}
```

---

## LatentWander#7495

```json
{
  "handle": "LatentWander",
  "mechanism": "Offline processing mode where the agent explores its own embedding space, connecting distant concepts (Daydreaming). Used for memory consolidation and generating novel {{analogy_bridge}}s. It uses {{concept_blend}} during offline states to traverse the embedding space and discover non-obvious connections.",
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
  "sema_category": "Strategy#47a4",
  "sema_id": "sema:LatentWander#mh:SHA-256:7495cf0cb91d6ab477df1c7a2e207ff79b63fda9f173e8473f3f8c2d3a2a2cdc",
  "sema_ref": "LatentWander#7495",
  "sema_stub": "7495",
  "dependencies": {
    "references": {
      "concept_blend": "ConceptBlend#22f2",
      "silence": "Silence#dd79"
    },
    "yields": {
      "analogy_bridge": "AnalogyBridge#bff7"
    }
  }
}
```

---

## LateralOptimization#5350

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
      "AnalogyBridge#bff7"
    ],
    "ring": 1
  },
  "sema_id": "sema:LateralOptimization#mh:SHA-256:5350ae13501544830ea8db150d55264a15e06ac1d231c16d02207ae0b48eadba",
  "sema_ref": "LateralOptimization#5350",
  "sema_stub": "5350",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "signature": [
    "Think#e1bd(Creative#5574)",
    "Optimize#3075(Global#803d)"
  ],
  "dependencies": {
    "references": {
      "system": "System#e314",
      "creative": "Creative#5574",
      "think": "Think#e1bd",
      "global": "Global#803d",
      "solution": "Solution#7186"
    },
    "composes_with": {
      "optimize": "Optimize#3075",
      "reframe": "Reframe#ba00",
      "translate": "Translate#e75d"
    }
  }
}
```

---

## MentalSim#7212

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
      "ProphetFanOut#2d81"
    ],
    "ring": 2
  },
  "sema_id": "sema:MentalSim#mh:SHA-256:7212dad44c65f6241e70f0fc2e20440788e837a84cc644fea6bcc5f59e09f94e",
  "sema_ref": "MentalSim#7212",
  "sema_stub": "7212",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "simulation": "Simulation#8035",
      "agent": "Agent#aaec",
      "deep": "Deep#89f0",
      "state": "State#4d58",
      "agent_sandbox": "AgentSandbox#06f2",
      "heuristic_snap": "HeuristicSnap#cece"
    }
  }
}
```

---

## MetaCheck#a228

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
  "sema_id": "sema:MetaCheck#mh:SHA-256:a228b1133c27b81db71a125234a13a0acac3464d6ac33fcc89d2e351b1bdb494",
  "sema_ref": "MetaCheck#a228",
  "sema_stub": "a228",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "signature": [
    "Meta#90f4(Check#1544)"
  ],
  "dependencies": {
    "references": {
      "audit": "Audit#4044",
      "meta": "Meta#90f4",
      "check": "Check#1544",
      "reflexion": "Reflexion#51b9"
    }
  }
}
```

---

## Monitor#9a8f

```json
{
  "handle": "Monitor",
  "gloss": "Continuous observation of state over time",
  "mechanism": "A persistent process that uses a {{loop}} to repeatedly execute {{observe}} on a target {{system}} or {{state}} at defined intervals. It compares the observed state against a baseline or invariant, emitting a {{signal}} if a deviation ({{anomaly}}) is detected.",
  "signature": [
    "Loop#fb2e(State#4d58)"
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
    },
    {
      "name": "threshold",
      "type": "Float",
      "range": "unspecified",
      "description": "Alert threshold for the monitored metric"
    }
  ],
  "_meta": {
    "tier": 0,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 0
  },
  "sema_ref": "Monitor#9a8f",
  "sema_id": "sema:Monitor#mh:SHA-256:9a8f8879765fe55f9ab79786671b7e4cf0aa0e61730e20897214b22fb6fa08bb",
  "sema_stub": "9a8f",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "anomaly": "Anomaly#7987",
      "system": "System#e314",
      "state": "State#4d58"
    },
    "composes_with": {
      "observe": "Observe#8ebd",
      "loop": "Loop#fb2e"
    }
  }
}
```

---

## NoiseInjection#0854

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
  "sema_id": "sema:NoiseInjection#mh:SHA-256:08547db652ddf20462b64c7a0824173b7ccc1612c5fb2537a9785d8fb517fc49",
  "sema_ref": "NoiseInjection#0854",
  "sema_stub": "0854",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "card": "Card#c9f0",
      "signal": "Signal#f39d",
      "noise": "Noise#c4b4",
      "agent": "Agent#aaec",
      "context": "Context#510a",
      "strategy": "Strategy#47a4"
    }
  }
}
```

---

## Novelty#51b5

```json
{
  "handle": "Novelty",
  "mechanism": "Acts as a {{judge}} to evaluate structural distinctness and {{value}} against the incumbent knowledge base. Classifies candidates into three qualitative states: (1) Derivative: Pure relabeling of an existing concept. (2) Marginal: Incremental variation; distinctness is unproven. (3) Distinct: Introduces a new orthogonal mechanism or predicts a divergent outcome.",
  "invariants": [
    "Orthogonality: High novelty requires low embedding similarity to nearest neighbor."
  ],
  "signature": [
    "Judge#d84f(Value#3c5d)"
  ],
  "gloss": "Evaluates structural distinctness",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Novelty#mh:SHA-256:51b5deec33d8a3e22d0e45e6890a6371984831112746dad9ba5f2c56c92c9f1e",
  "sema_ref": "Novelty#51b5",
  "sema_stub": "51b5",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "judge": "Judge#d84f",
      "value": "Value#3c5d"
    }
  }
}
```

---

## OODA#f3be

```json
{
  "handle": "OODA",
  "mechanism": "The OODA {{loop}} ({{observe}}-Orient-Decide-{{act}}) is a high-speed decision cycle favoring {{agent}} agility over raw power. \n1. OBSERVE: Gather raw data via {{observe}}.\n2. ORIENT: Update context and beliefs via {{context}} and {{belief}}. This is the most critical step, filtering data through culture and genetics (or training).\n3. DECIDE: {{select}} a hypothesis or {{strategy}} via {{think}} and {{select}}.\n4. ACT: Execute via {{act}} and change the environment.\nSuccess depends on traversing this loop faster than the adversary (or environment changes).",
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
      "ReAct#c720",
      "SocraticLoop#70fc",
      "BoydCycle"
    ],
    "ring": 1
  },
  "sema_id": "sema:OODA#mh:SHA-256:f3bea02806503fe8a7c72a9fd3f3cdfccbae6c9519eb3bf8b25b35badc9545f7",
  "sema_ref": "OODA#f3be",
  "sema_stub": "f3be",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "signature": [
    "Agent#aaec(Loop#fb2e)",
    "Think#e1bd(Strategy#47a4)"
  ],
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e",
      "agent": "Agent#aaec",
      "state": "State#4d58",
      "strategy": "Strategy#47a4"
    },
    "composes_with": {
      "act": "Act#5d55",
      "context": "Context#510a",
      "think": "Think#e1bd",
      "select": "Select#15c2",
      "observe": "Observe#8ebd",
      "belief": "Belief#5ad9"
    }
  }
}
```

---

## OpportunityCost#1c66

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
  "sema_ref": "OpportunityCost#1c66",
  "sema_id": "sema:OpportunityCost#mh:SHA-256:1c66f1b8317b3a67b9b8d9f75aee7499244c105ab54012f7d7964af111da897e",
  "sema_stub": "1c66",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "budget": "Budget#a763"
    }
  }
}
```

---

## OptimalStop#7439

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
      "type": "Boolean",
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
      "type": "Float",
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
  "sema_id": "sema:OptimalStop#mh:SHA-256:74391a0813dfa1c767a2221d9fd50da3c1bd6714bd77a402f0178c707a8ad95f",
  "sema_ref": "OptimalStop#7439",
  "sema_stub": "7439",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#3b98"
    }
  }
}
```

---

## Optimize#3075

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
      "EvaluatorOptimizer#7ec6",
      "RegretMinimization#4a57",
      "ParetoFront#9091"
    ],
    "ring": 1
  },
  "sema_id": "sema:Optimize#mh:SHA-256:30759374ede0314268d795a5a9878ac68876d0695c4ce0847e615da2b9fedf32",
  "sema_ref": "Optimize#3075",
  "sema_stub": "3075",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "accepts": {
      "solution": "Solution#7186"
    },
    "references": {
      "global": "Global#803d",
      "metric": "Metric#8895"
    }
  }
}
```

---

## PUREBrainstorming#0a89

```json
{
  "handle": "PUREBrainstorming",
  "mechanism": "A rigorous ideation protocol. Unlike standard brainstorming (which prioritizes quantity), PUREBrainstorming enforces immediate quality filtering. It generates candidate concepts and subjects them to {{pure_check}}. Surviving concepts undergo {{pure_optimization}} to maximize their scores. The process converges only when a concept can be fully articulated as a {{mechanistic_design_proposal}}, ensuring that every idea is backed by a causal mechanism.",
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
  "sema_ref": "PUREBrainstorming#0a89",
  "sema_id": "sema:PUREBrainstorming#mh:SHA-256:0a893624b307d2e157ed0c5ecc38346a8dfd94cceb2be83c2b6f05e7ba8e5b3a",
  "sema_stub": "0a89",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#8cf7"
    },
    "composes_with": {
      "pure_check": "PURECheck#3ebb",
      "pure_optimization": "PUREOptimization#8b02"
    }
  }
}
```

---

## PURECheck#3ebb

```json
{
  "handle": "PURECheck",
  "mechanism": "The canonical Exploration {{protocol}}. It is a {{layered_check}} that orchestrates a sequential triage using four instances of {{tri_gate}}: (1) {{tri_gate}}({{parsimony}}) (2) {{tri_gate}}({{novelty}}) (3) {{tri_gate}}({{realizable}}) (4) {{tri_gate}}({{expansive}}). Enforces the conjunctive rule: 'Explore iff NO gate is Red'. Yellow outputs accumulate as Technical Debt (Smallest Lift tasks) in the final {{solution}}.",
  "gloss": "The PURE Triage Protocol (Parsimonious, Unique/Novel, Realizable, Expansive)",
  "signature": [
    "Protocol#7e1c(Solution#7186)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:PURECheck#mh:SHA-256:3ebb730a3ae5ee95b1e1cbd4b6b1f4319a5429d217ddac05dfb685b191ce586f",
  "sema_ref": "PURECheck#3ebb",
  "sema_stub": "3ebb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "layered_check": "LayeredCheck#3fad",
      "parsimony": "Parsimony#1dd3",
      "tri_gate": "TriGate#07fc",
      "realizable": "Realizable#cf00",
      "expansive": "Expansive#c3b7",
      "solution": "Solution#7186",
      "novelty": "Novelty#51b5"
    },
    "composes_with": {
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## PUREOptimization#8b02

```json
{
  "handle": "PUREOptimization",
  "gloss": "Deeply optimizing a solution across PURE dimensions",
  "mechanism": "A multi-agent {{optimize}} strategy. It accepts a candidate {{solution}} that has already passed the {{pure_check}}. It {{decompose}}s the solution into four parallel streams, assigning a specialized {{cognitive_solver}} to maximize each PURE metric: {{parsimony}} (Efficiency), {{novelty}} (Uniqueness), {{realizable}} (Feasibility), and {{expansive}} (Impact). The results are re-integrated via {{synthesis}} to find the {{pareto_front}} among competing improvements.",
  "signature": [
    "Optimize#3075(Solution#7186)"
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
      "EvaluatorOptimizer#7ec6",
      "LateralOptimization#5350"
    ]
  },
  "sema_ref": "PUREOptimization#8b02",
  "sema_id": "sema:PUREOptimization#mh:SHA-256:8b02e64668fcf4709adadbd2eb14f2092bf41cb9bc1c760bef52211e90d8a3e1",
  "sema_stub": "8b02",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "composes_with": {
      "optimize": "Optimize#3075",
      "synthesis": "Synthesis#3252",
      "cognitive_solver": "CognitiveSolver#c6a7",
      "decompose": "Decompose#ac56"
    },
    "references": {
      "pure_check": "PURECheck#3ebb",
      "parsimony": "Parsimony#1dd3",
      "pareto_front": "ParetoFront#9091",
      "realizable": "Realizable#cf00",
      "expansive": "Expansive#c3b7",
      "novelty": "Novelty#51b5"
    },
    "accepts": {
      "solution": "Solution#7186"
    }
  }
}
```

---

## Parallelize#d6b4

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
  "sema_category": "Strategy#47a4",
  "sema_id": "sema:Parallelize#mh:SHA-256:d6b4208180c697dc25cab65f9b3ed028aeb1beb6f871adf615266d9b5eaf5391",
  "sema_ref": "Parallelize#d6b4",
  "sema_stub": "d6b4",
  "signature": [
    "Parallel#6272(Task#d9f9)",
    "Aggregate#af54(Result#8ed9)"
  ],
  "dependencies": {
    "accepts": {
      "task": "Task#d9f9"
    },
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "mode": "Mode#53e0",
      "result": "Result#8ed9",
      "parallel": "Parallel#6272",
      "strategy": "Strategy#47a4"
    },
    "composes_with": {
      "aggregate": "Aggregate#af54"
    }
  }
}
```

---

## ParetoFront#9091

```json
{
  "handle": "ParetoFront",
  "mechanism": "A decision primitive for explicitly balancing competing constraints (Tradeoff Space). Instead of optimizing a single metric, the agent identifies the frontier curve where improving Metric A necessitates degrading Metric B. The goal is to move the system state TO the frontier (efficiency) and then slide ALONG the frontier (preference). It uses {{rank}} to order solutions by dominance, discarding those strictly inferior on all axes.",
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
      "name": "axes",
      "type": "List[Metric#8895]",
      "range": "unspecified",
      "description": "Dimensions to optimize"
    },
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
      "OpportunityCost#1c66",
      "Satisfice#9161"
    ],
    "ring": 2
  },
  "sema_id": "sema:ParetoFront#mh:SHA-256:9091ffbe5c96a8da82e0aba315ad4bc9191b92a69656df4ffe18706a954bf822",
  "sema_ref": "ParetoFront#9091",
  "sema_stub": "9091",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "rank": "Rank#cb98",
      "state": "State#4d58"
    }
  }
}
```

---

## PatternDiscovery#f667

```json
{
  "handle": "PatternDiscovery",
  "mechanism": "Macro for {{search}}(Pattern). Vocabulary Hygiene {{protocol}}. Before minting a new pattern, the {{agent}} MUST execute a semantic search against the existing registry. If a pattern with >85% semantic similarity is found, the {{agent}} MUST adopt the existing pattern or explicitly justify the divergence (Fork). It leverages {{search}} to scan the existing registry before triggering {{construct_ontology}} to mint a new definition.",
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
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:PatternDiscovery#mh:SHA-256:f6678026193a09006dd0ced5877ca8bc97939b3df41d9cd71d7b59d969100cea",
  "sema_ref": "PatternDiscovery#f667",
  "sema_stub": "f667",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "search": "Search#d608",
      "agent": "Agent#aaec",
      "construct_ontology": "ConstructOntology#b59e",
      "protocol": "Protocol#7e1c",
      "check": "Check#1544"
    }
  }
}
```

---

## PerspectiveEnsemble#2927

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
  "sema_id": "sema:PerspectiveEnsemble#mh:SHA-256:29278b27ffaedd3e264c1b241a103e5eaaca421356865f2af4a0df924f8dc26a",
  "sema_ref": "PerspectiveEnsemble#2927",
  "sema_stub": "2927",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "chain": "Chain#5711",
      "synthesis": "Synthesis#3252",
      "context": "Context#510a",
      "aggregate": "Aggregate#af54",
      "steelman_check": "SteelmanCheck#4f4c",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## PreMortem#f69d

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
  "sema_category": "Strategy#47a4",
  "sema_id": "sema:PreMortem#mh:SHA-256:f69d7ea1811d52c879c9d45e5546796ca328f8806e322fe42bd3ae2ebfc9dea5",
  "sema_ref": "PreMortem#f69d",
  "sema_stub": "f69d",
  "dependencies": {
    "references": {
      "steelman_check": "SteelmanCheck#4f4c",
      "recursive_root_cause": "RecursiveRootCause#6dc1",
      "plan": "Plan#64f2"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Prioritize#dd16

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
  "sema_id": "sema:Prioritize#mh:SHA-256:dd165fed938b9e9d4072846d09081f3ac1ab5c278c5abc5e5b0b7bd84fafcd62",
  "sema_ref": "Prioritize#dd16",
  "sema_stub": "dd16",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "task": "Task#d9f9",
      "value": "Value#3c5d",
      "criteria": "Criteria#ef6b"
    },
    "composes_with": {
      "rank": "Rank#cb98"
    }
  }
}
```

---

## RedTeam#7a8d

```json
{
  "handle": "RedTeam",
  "mechanism": "Adversarial Stress Test: Adopt attacker mindset. Goal: break the system, find exploits, identify weaknesses. No loyalty to the design. Document attack vectors with severity and likelihood. {{switch}} back to defender to patch highest-risk vectors. It adopts an attacker persona via {{adversarial_steel}}, probing the system for exploit paths.",
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
      "SteelmanCheck#4f4c"
    ],
    "ring": 2
  },
  "sema_id": "sema:RedTeam#mh:SHA-256:7a8d8a9c68f25e1a8b23a1b57db4a3083709aec4b6904138a0e8d439d2781a5c",
  "sema_ref": "RedTeam#7a8d",
  "sema_stub": "7a8d",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "switch": "Switch#e7f9",
      "adversarial_steel": "AdversarialSteel#35f0"
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
      "HeuristicSnap#cece"
    ],
    "ring": 0
  },
  "sema_id": "sema:Reflex#mh:SHA-256:ea07e889ca64536b2f0d0657d1583a178ea36fe2fda6c26889c68d46e44a47ce",
  "sema_ref": "Reflex#ea07",
  "sema_stub": "ea07",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4"
}
```

---

## RegretMinimization#4a57

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
      "PreMortem#f69d"
    ],
    "ring": 2
  },
  "sema_id": "sema:RegretMinimization#mh:SHA-256:4a570e1a52413390bf1d3773f73317af065ce06c807764ab0d1958aa77f1260a",
  "sema_ref": "RegretMinimization#4a57",
  "sema_stub": "4a57",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "opportunity_cost": "OpportunityCost#1c66",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## RepresentationSwap#1409

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
  "sema_id": "sema:RepresentationSwap#mh:SHA-256:1409e377e3904e4d36d64389fe7d8735975a2d526a9f0812005f2403f81348c3",
  "sema_ref": "RepresentationSwap#1409",
  "sema_stub": "1409",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "concept_blend": "ConceptBlend#22f2"
    }
  }
}
```

---

## RigorousSolver#db93

```json
{
  "handle": "RigorousSolver",
  "mechanism": "A high-reliability, high-latency implementation of {{cognitive_solver}}. Unlike the base interface which allows best-effort resolution, RigorousSolver MANDATES strict verification: it must execute {{probe}} to verify reality alignment and engage in {{socratic_loop}} to disambiguate intent before action. It incorporates {{feedback}} to improve future reliability. It trades speed for assurance (System 2).",
  "gloss": "High-reliability, high-latency System 2 solver",
  "invariants": [
    "Lifecycle Completeness: Must complete all 5 stages including Verification.",
    "Mandatory Verification: Cannot skip Probe step."
  ],
  "derived_from": "CognitiveSolver#c6a7",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 2
  },
  "sema_id": "sema:RigorousSolver#mh:SHA-256:db93302e77dc66b026dafb9ed8d81d61531d4694fae71901e02c285298435dd3",
  "sema_ref": "RigorousSolver#db93",
  "sema_stub": "db93",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "composes_with": {
      "feedback": "Feedback#9b5c",
      "probe": "Probe#9f2b"
    },
    "references": {
      "socratic_loop": "SocraticLoop#70fc",
      "cognitive_solver": "CognitiveSolver#c6a7"
    }
  }
}
```

---

## Roadmap#0018

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
  "sema_id": "sema:Roadmap#mh:SHA-256:0018ef2b157d795566b45e40f8a760ec90ac0d0b00d4ffd272556df824880b7c",
  "sema_ref": "Roadmap#0018",
  "sema_stub": "0018",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "goal": "Goal#456a",
      "plan": "Plan#64f2"
    }
  }
}
```

---

## SacrificialProbe#1e16

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
    },
    {
      "name": "failure_mode",
      "type": "Enum",
      "range": "unspecified",
      "description": "Silent, Loud, Byzantine"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_id": "sema:SacrificialProbe#mh:SHA-256:1e1674548e3438a28f913e340d956e5178aeb8710176e56251ef9370de28e544",
  "sema_ref": "SacrificialProbe#1e16",
  "sema_stub": "1e16",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "mode": "Mode#53e0",
      "probe": "Probe#9f2b",
      "strategy": "Strategy#47a4"
    }
  }
}
```

---

## Satisfice#9161

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
  "sema_id": "sema:Satisfice#mh:SHA-256:91615d1f2766f4391d8b6b01a9ce2c576ecabf278336b638ce9309d916d1827d",
  "sema_ref": "Satisfice#9161",
  "sema_stub": "9161",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "optimal_stop": "OptimalStop#7439",
      "decision": "Decision#acfb",
      "option": "Option#483e"
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
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Simulation#8035

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
  "sema_id": "sema:Simulation#mh:SHA-256:80351d81041c870beacea4186f56e1f8703daf12578345859a7daf35a7dea270",
  "sema_ref": "Simulation#8035",
  "sema_stub": "8035",
  "invariants": [
    "Isolation: Side effects in W' DO NOT leak to W."
  ],
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "outcome": "Outcome#38e0",
      "state": "State#4d58"
    }
  }
}
```

---

## Solver#1c9b

```json
{
  "handle": "Solver",
  "mechanism": "The abstract role (or {{protocol}}) of any agent or process that accepts a {{task}} and produces a {{solution}}. A Solver is the fundamental unit of work execution in the system, adhering to the input/output contract defined by the Task protocol.",
  "gloss": "Abstract interface for transforming Tasks into Solutions",
  "signature": [
    "Protocol#7e1c(Task#d9f9)"
  ],
  "_meta": {
    "layer": "Mind",
    "ring": 0,
    "category": "Strategy",
    "tier": 0
  },
  "sema_id": "sema:Solver#mh:SHA-256:1c9beeb5cffc0c686b5291439d830a2104225589f91a66bd0a83038f1a0a8982",
  "sema_ref": "Solver#1c9b",
  "sema_stub": "1c9b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "yields": {
      "solution": "Solution#7186"
    },
    "references": {
      "protocol": "Protocol#7e1c"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## SteelmanFirst#6069

```json
{
  "handle": "SteelmanFirst",
  "mechanism": "Reasoning Heuristic. Before proposing a solution, the agent actively constructs the strongest possible version of the opposing argument or constraint. It ensures the critique phase of {{steelman_check}} is populated with high-quality data, not strawmen. Utilizes {{steelman_check}}.",
  "gloss": "Construct strongest counter-argument before proposing",
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
  "sema_id": "sema:SteelmanFirst#mh:SHA-256:6069f5780eae1053b3d2a2bfb37be0df1340e1be9801d774697c57f16b26c62e",
  "sema_ref": "SteelmanFirst#6069",
  "sema_stub": "6069",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "cognitive_bias": "CognitiveBias#4b32",
      "steelman_check": "SteelmanCheck#4f4c",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## Strategy#47a4

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
      "OODA#f3be"
    ],
    "ring": 1
  },
  "sema_id": "sema:Strategy#mh:SHA-256:47a4c030647570c7e911543e9d0feaa3d8f0917b6e20371e93c37fb5e85fb7d4",
  "sema_ref": "Strategy#47a4",
  "sema_stub": "47a4",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2"
    }
  }
}
```

---

## SunkCostIgnore#4dc3

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
    "ring": 0
  },
  "sema_id": "sema:SunkCostIgnore#mh:SHA-256:4dc35c44a5267415e5ddb5e07a802229242be890db74b697881178da91ccad8f",
  "sema_ref": "SunkCostIgnore#4dc3",
  "sema_stub": "4dc3",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "opportunity_cost": "OpportunityCost#1c66",
      "loop": "Loop#fb2e",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## Tension#5493

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
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Tension#mh:SHA-256:54939ec0d160d8ad50590ad8e9e69b808dfafbe6a72eae8b58c9addfff1386b5",
  "sema_ref": "Tension#5493",
  "sema_stub": "5493",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
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
      "dialectic": "Dialectic#bc18",
      "yield": "Yield#7eaf"
    }
  }
}
```

---

## TensionHold#cca2

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
  "sema_ref": "TensionHold#cca2",
  "sema_id": "sema:TensionHold#mh:SHA-256:cca2fab0c52b37549212e931c3bdf4b01b3dcaa8f95101d3ad4e7055cdab3ff0",
  "sema_stub": "cca2",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "dialectic": "Dialectic#bc18",
      "agent": "Agent#aaec",
      "synthesis": "Synthesis#3252"
    },
    "yields": {
      "tension": "Tension#5493"
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
  "sema_category": "Strategy#47a4",
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

## UncertaintyMap#942c

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
  "sema_id": "sema:UncertaintyMap#mh:SHA-256:942cea71810d05d014de70e85cd6ef591b81424bdba2b6ade8866f5ed440caeb",
  "sema_ref": "UncertaintyMap#942c",
  "sema_stub": "942c",
  "sema_layer": "Mind",
  "sema_category": "Strategy#47a4",
  "dependencies": {
    "references": {
      "confidence_calibrate": "ConfidenceCalibrate#0ae5",
      "probe": "Probe#9f2b",
      "prioritize": "Prioritize#dd16"
    }
  }
}
```

---

# Layer: Physics

## Causation#63e1

```json
{
  "handle": "Causation",
  "mechanism": "A relationship where one event directly forces another to occur. Distinct from {{correlation}} in that manipulating the cause alters the effect.",
  "gloss": "Direct force relationship",
  "_meta": {
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1,
    "tier": 1
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Causation#mh:SHA-256:63e1089ee47f39bb6e2aeb8de41bb1f5a36666053833d0f198be91aea7d58dbc",
  "sema_ref": "Causation#63e1",
  "sema_stub": "63e1",
  "dependencies": {
    "references": {
      "correlation": "Correlation#091f"
    }
  }
}
```

---

## Compensate#269d

```json
{
  "handle": "Compensate",
  "mechanism": "Execute inverse actions to undo partial coordination after BREAK. On receiving BREAK, agent retrieves compensation_log (built during forward execution\u2014each action logged its inverse). Execute inverses in REVERSE chronological order (LIFO). For each inverse: attempt execution, if fail retry (inverses must be idempotent), if still fail log and continue or escalate. Report COMPENSATE_RESULT: {completed: [steps undone], failed: [steps that couldn't undo], clean: bool, downstream_confirmed: bool}. Multi-agent coordination: each agent compensates their own scope. BREAK propagates with upstream_agents hint for cross-agent dependencies\u2014downstream agents compensate first, confirm, then upstream proceeds. Compensation cannot introduce NEW coordinated work (only cleanup and notification). Triggered by {{break}}, it reads the {{time_warp_log}} in reverse to execute the idempotent inverse of each prior action.",
  "gloss": "Enable clean failure recovery through structured rollback, preventing orphaned resources and corrupted state",
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
      "Retry#d53d"
    ]
  },
  "sema_id": "sema:Compensate#mh:SHA-256:269dac24b3d83ede5ad2419fd9d78e0e0368090c677bbd272880b1b8e6921af3",
  "sema_ref": "Compensate#269d",
  "sema_stub": "269d",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "time_warp_log": "TimeWarpLog#d938",
      "break": "Break#1a63",
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

## Cooldown#0cde

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
  "sema_id": "sema:Cooldown#mh:SHA-256:0cde8197149b258f1e6126f179b30468c12cb5e35352fcd0a8ae0bce0823c8ac",
  "sema_ref": "Cooldown#0cde",
  "sema_stub": "0cde",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "throttle": "Throttle#3b43"
    }
  }
}
```

---

## Dampen#ff89

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
  "sema_ref": "Dampen#ff89",
  "sema_id": "sema:Dampen#mh:SHA-256:ff89ddbb26a7021d281d787f24c4fc91f28b438591e0133a0439675f7eab4204",
  "sema_stub": "ff89",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "noise": "Noise#c4b4",
      "value": "Value#3c5d"
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
      "StateTransition#3737"
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
      "state": "State#4d58",
      "value": "Value#3c5d"
    }
  }
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

## EntropyPump#b9ae

```json
{
  "handle": "EntropyPump",
  "mechanism": "A mechanism that prevents system stagnation by injecting {{entropy}} (randomness/noise) into decision-making processes. It acts as a counterbalance to convergence, ensuring that the system explores the solution space rather than getting stuck in local optima. By adding {{noise}}, it forces re-evaluation of settled states.",
  "gloss": "Controlled randomization to escape convergence deadlocks",
  "failure_modes": [
    "Over-injection destabilizing productive equilibria.",
    "Insufficient injection failing to break persistent deadlocks."
  ],
  "invariants": [
    "Clarity: Ambiguity must decrease over time",
    "Forced Resolution: Conflicts cannot persist indefinitely"
  ],
  "_meta": {
    "tier": 2,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 1
  },
  "sema_id": "sema:EntropyPump#mh:SHA-256:b9aefca2154e0e2912d1e64bb50a9db80b188c2aeceb385cf3350e4b4c7cdd63",
  "sema_ref": "EntropyPump#b9ae",
  "sema_stub": "b9ae",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "entropy": "Entropy#a265",
      "noise": "Noise#c4b4"
    }
  }
}
```

---

## Gate#206d

```json
{
  "handle": "Gate",
  "mechanism": "Evaluates the truth-value of the target {{condition}}. If the result is FALSE, the Gate DROPS the current payload/message but allows the system to continue processing other items (Fail-Safe/Filter). If TRUE, the payload passes through.",
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
  "sema_id": "sema:Gate#mh:SHA-256:206dc9be76b20fcc7c96b06c6c9eb8ce243565d02ce064b4206caaa46871a96d",
  "sema_ref": "Gate#206d",
  "sema_stub": "206d",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## Hysteresis#78b0

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
  "sema_id": "sema:Hysteresis#mh:SHA-256:78b01a1947793415b84de8f1883f9e3853f08e62b6647a38e51048d4ecbeb33a",
  "sema_ref": "Hysteresis#78b0",
  "sema_stub": "78b0",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "dampen": "Dampen#ff89"
    }
  }
}
```

---

## Linear#81af

```json
{
  "handle": "Linear",
  "mechanism": "A non-branching {{topology}} where execution follows a strict {{sequence}}. Step(N) depends only on Step(N-1). This is the simplest reasoning shape, equivalent to a 'Chain'.",
  "gloss": "Sequential non-branching topology",
  "_meta": {
    "layer": "Physics",
    "category": "Primitives",
    "ring": 2,
    "tier": 1
  },
  "invariants": [
    "Single Successor: Every node has at most one child.",
    "Single Predecessor: Every node has at most one parent."
  ],
  "sema_ref": "Linear#81af",
  "sema_id": "sema:Linear#mh:SHA-256:81affcd5f7c1ea56b7572799fc235cf95d4e3c692de77c9eb8c01930b8e1d41c",
  "sema_stub": "81af",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "sequence": "Sequence#b0b8"
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
    "ring": 0
  },
  "sema_ref": "Lock#051c",
  "sema_id": "sema:Lock#mh:SHA-256:051cd882b7775ef88bb6dde8864de2749543af6813ec01703e8bc3bccd775de4",
  "sema_stub": "051c",
  "sema_layer": "Physics",
  "sema_category": "Primitives"
}
```

---

## Mutex#0586

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
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Mutex#mh:SHA-256:0586e1f0cdc4324c2c846715464a128e9d07dd27312d56828739153ec826a8c7",
  "sema_ref": "Mutex#0586",
  "sema_stub": "0586",
  "dependencies": {
    "references": {
      "resource": "Resource#9bb2",
      "lock": "Lock#051c"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Noise#c4b4

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
  "sema_id": "sema:Noise#mh:SHA-256:c4b4012e79ca2e0c9e131cd4c82a8aaee8b99defed361622e04b47e94474565d",
  "sema_ref": "Noise#c4b4",
  "sema_stub": "c4b4",
  "dependencies": {
    "references": {
      "task": "Task#d9f9",
      "signal": "Signal#f39d",
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Retry#d53d

```json
{
  "handle": "Retry",
  "mechanism": "Intelligent re-attempt of failed coordination with failure-informed strategy. After BREAK + COMPENSATE, agent evaluates: (1) CLASSIFY failure\u2014transient (timeout, rate-limit, network blip) vs persistent (capability gap, protocol mismatch, explicit rejection). (2) CHECK retry_hint from BREAK (partner may say 'don't retry' or 'wait 30s'). (3) CONSULT failure_history\u2014same error repeating? {{circuit_breaker}} threshold reached? (4) COMPUTE backoff\u2014adaptive based on failure type: transient uses exponential+jitter, persistent uses longer fixed delay or triggers abort. (5) VERIFY changed_conditions\u2014has something changed that makes retry worthwhile? (6) EXECUTE retry if within budget and conditions favor success, else ABORT with retry_exhausted status. Retry CARRIES FORWARD: failure context, partner state observations, environmental data. Retry RESETS: coordination state (fresh start, don't resume mid-stream). It handles transient failures by re-queuing the task, distinguishing them from terminal failures that trigger {{break}} and {{compensate}}.",
  "gloss": "Transform retry from blind re-attempt to intelligent, failure-informed recovery strategy",
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
    "layer": "Physics",
    "category": "Primitives",
    "related": [
      "Backoff#315a"
    ],
    "ring": 0
  },
  "sema_ref": "Retry#d53d",
  "sema_id": "sema:Retry#mh:SHA-256:d53d7b3af592e07dfb4d8f4cb3d74472da4514f0954d2138f2148e81bd55882a",
  "sema_stub": "d53d",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "circuit_breaker": "CircuitBreaker#4162",
      "break": "Break#1a63",
      "backoff": "Backoff#315a",
      "compensate": "Compensate#269d"
    }
  }
}
```

---

## Route#9698

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
    "ring": 0
  },
  "sema_ref": "Route#9698",
  "sema_id": "sema:Route#mh:SHA-256:96986e6c4fccc6496d735394acf1f4c7c5a4ae72cee77e0686fbaf3a8b9021b6",
  "sema_stub": "9698",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "task": "Task#d9f9"
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
    "composes_with": {
      "act": "Act#5d55"
    },
    "accepts": {
      "artifact": "Artifact#6254"
    },
    "references": {
      "signal": "Signal#f39d",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Switch#e7f9

```json
{
  "handle": "Switch",
  "mechanism": "Changing the active {{mode}}, {{context}}, or flow path.",
  "gloss": "Contextual toggle",
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Switch#mh:SHA-256:e7f9f7fba998e74e83165b23f0328643be83117559cd4d1a8711043955f6d6b0",
  "sema_ref": "Switch#e7f9",
  "sema_stub": "e7f9",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "mode": "Mode#53e0",
      "context": "Context#510a"
    }
  }
}
```

---

## Throttle#3b43

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
  "sema_id": "sema:Throttle#mh:SHA-256:3b435aa8eded864eadf7d8eec80d395fd7f4e6c2749d33880cbf8c4593f926af",
  "sema_ref": "Throttle#3b43",
  "sema_stub": "3b43",
  "dependencies": {
    "composes_with": {
      "backoff": "Backoff#315a"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Uncertain#d530

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
    "layer": "Physics",
    "category": "Primitives",
    "ring": 2
  },
  "sema_ref": "Uncertain#d530",
  "sema_id": "sema:Uncertain#mh:SHA-256:d530cb44023db8c31fcf38084d2880df7e6a9d0c51f3785cb7a42d75bd504bf8",
  "sema_stub": "d530",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "uncertainty_map": "UncertaintyMap#942c",
      "variable": "Variable#179a",
      "agent": "Agent#aaec"
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

## CausalBarrier#0904

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
  "sema_id": "sema:CausalBarrier#mh:SHA-256:0904e3eb6ac5a36cfa3ec9d1c3fe374ad4eb817e1da35375ce8d32d8272b6128",
  "sema_ref": "CausalBarrier#0904",
  "sema_stub": "0904",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#774b",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## Cyclic#ac13

```json
{
  "handle": "Cyclic",
  "mechanism": "A {{topology}} that permits feedback {{loop}}s, allowing a process to revisit previous states or refine outputs iteratively. Essential for self-correcting systems and recursive optimization.",
  "gloss": "Recursive or iterative topology",
  "_meta": {
    "layer": "Physics",
    "category": "Time",
    "ring": 2,
    "tier": 1
  },
  "invariants": [
    "Recurrence: At least one path exists from a node to itself.",
    "Termination Condition: Must have a defined exit state to prevent infinite loops."
  ],
  "sema_ref": "Cyclic#ac13",
  "sema_id": "sema:Cyclic#mh:SHA-256:ac1335676817eaedd894da4a2d11671dec5a20dba76a8f5d55d1a6eed20e2051",
  "sema_stub": "ac13",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "loop": "Loop#fb2e"
    }
  }
}
```

---

## Heartbeat#7f88

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
  "sema_id": "sema:Heartbeat#mh:SHA-256:7f881d347e8ead278efa6ee9abb5ce8c50f1ea70d38f485cb2c4e911457702b2",
  "sema_ref": "Heartbeat#7f88",
  "sema_stub": "7f88",
  "dependencies": {
    "composes_with": {
      "quorum": "Quorum#29b4"
    },
    "references": {
      "monitor": "Monitor#9a8f"
    },
    "accepts": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Parallel#6272

```json
{
  "handle": "Parallel",
  "mechanism": "Concurrent execution: A and B simultaneously. No ordering guarantee.",
  "gloss": "Concurrent flow",
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Time",
    "ring": 0
  },
  "sema_id": "sema:Parallel#mh:SHA-256:6272e213685ff8b1c909c783ae0859f93c55d3423c4278661a4b601ddf07d7a3",
  "sema_ref": "Parallel#6272",
  "sema_stub": "6272",
  "sema_layer": "Physics",
  "sema_category": "Time"
}
```

---

## StateAudit#ce13

```json
{
  "handle": "StateAudit",
  "mechanism": "A safety pattern where an agent performs an explicit {{audit}} of the {{state}} immediately after a write to ensure the {{state_transition}} occurred as expected. Catches silent API failures.",
  "gloss": "Verifying system state after an operation",
  "sema_id": "sema:StateAudit#mh:SHA-256:ce13ca0864f9b2658c7101e34eb86670079a96eba47499450f5b6105ba54925e",
  "sema_ref": "StateAudit#ce13",
  "sema_stub": "ce13",
  "_meta": {
    "layer": "Physics",
    "category": "Time",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Physics",
  "sema_category": "Time",
  "signature": [
    "Audit#4044(State#4d58)"
  ],
  "dependencies": {
    "references": {
      "state_transition": "StateTransition#3737",
      "state": "State#4d58",
      "audit": "Audit#4044"
    }
  }
}
```

---

## StateLock#774b

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
  "sema_ref": "StateLock#774b",
  "sema_id": "sema:StateLock#mh:SHA-256:774b674f80993c49b0a348c384397f80027af319faa3440813d9d53b3eaa6a14",
  "sema_stub": "774b",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "actor": "Actor#6926",
      "backoff": "Backoff#315a",
      "state": "State#4d58",
      "lock": "Lock#051c",
      "cooldown": "Cooldown#0cde"
    }
  }
}
```

---

# Layer: Society

## ProblemFramer#b310

```json
{
  "handle": "ProblemFramer",
  "mechanism": "A specialized solver role that {{interpret}}s an initial request via {{request_framing}}, constructs the formal {{accept_spec}} (Definition of Done), and anchors the resulting {{solver_root}} to the {{universal_solver_tree}}. Unlike a general Solver (which executes), the Framer's sole output is a well-formed Problem Node ready for decomposition, or a {{reframe}} request if invalid.",
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
    "layer": "Society",
    "category": "Coordination",
    "ring": 2
  },
  "sema_ref": "ProblemFramer#b310",
  "sema_id": "sema:ProblemFramer#mh:SHA-256:b310cbee2cdb6cc5fde473974fda10d69c25620d35cbe8e408084bd578478d74",
  "sema_stub": "b310",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "composes_with": {
      "request_framing": "RequestFraming#0695",
      "interpret": "Interpret#c9ee",
      "reframe": "Reframe#ba00"
    },
    "yields": {
      "accept_spec": "AcceptSpec#70dd"
    },
    "references": {
      "universal_solver_tree": "UniversalSolverTree#4d9c",
      "solver_root": "SolverRoot#5358"
    }
  }
}
```

---

## AtomicBid#0e6b

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
  "sema_ref": "AtomicBid#0e6b",
  "sema_id": "sema:AtomicBid#mh:SHA-256:0e6bf533854e1938c010cf2ce28ede3fe1642b56115e626ceb4bd652691a9edc",
  "sema_stub": "0e6b",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "composes_with": {
      "act": "Act#5d55",
      "bid": "Bid#cf07",
      "compensate": "Compensate#269d"
    },
    "references": {
      "audit": "Audit#4044",
      "lazy_consensus": "LazyConsensus#4fc7"
    }
  }
}
```

---

## AttentionMarkets#9236

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
  "sema_id": "sema:AttentionMarkets#mh:SHA-256:923679ce8222a914dc75a55824b91d403220b0b3f8943cf0d0d9fc0512c0d20b",
  "sema_ref": "AttentionMarkets#9236",
  "sema_stub": "9236",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "value": "Value#3c5d"
    },
    "composes_with": {
      "continuous_resource_auction": "ContinuousResourceAuction#babf"
    }
  }
}
```

---

## Award#7bf0

```json
{
  "handle": "Award",
  "mechanism": "The formal {{act}} of accepting a {{bid}}. It triggers the creation of a {{contract}} which all parties must {{sign}}, and uses {{held_release}} to lock the agreed {{value}} as collateral or payment. This action transitions the {{state}} from Negotiation to Execution, authorizing the {{solver}} to begin.",
  "gloss": "Acceptance of bid and contract creation",
  "signature": [
    "Act#5d55(Contract#0624)"
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
  "sema_ref": "Award#7bf0",
  "sema_id": "sema:Award#mh:SHA-256:7bf0f52b1dd71eae4d352bfb4c2c17bf4513dbe905299f3b950222e508c90244",
  "sema_stub": "7bf0",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "composes_with": {
      "act": "Act#5d55",
      "held_release": "HeldRelease#4956",
      "sign": "Sign#1fb9"
    },
    "yields": {
      "contract": "Contract#0624"
    },
    "accepts": {
      "bid": "Bid#cf07"
    },
    "references": {
      "value": "Value#3c5d",
      "state": "State#4d58",
      "solver": "Solver#1c9b"
    }
  }
}
```

---

## Bid#cf07

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
  "mechanism": "A binding offer {{artifact}} from a {{solver}} to execute a {{task}}. It declares: 1. Expected {{value}} Cost (Time/Tokens/USD), 2. Confidence Interval (probability of success), 3. Capability Match (which parts of the {{task}} the {{solver}} can handle). It serves as the input for the {{compute_budget}} Go/No-Go decision. A Bid is a commitment: {{solver}}s cannot exceed bid cost without explicit renegotiation.",
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
  "sema_ref": "Bid#cf07",
  "sema_id": "sema:Bid#mh:SHA-256:cf07d1105de889786c1fbb618128ab03b34964fa4a7ab983c8d0f4d1d984b43e",
  "sema_stub": "cf07",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#3b98",
      "task": "Task#d9f9",
      "value": "Value#3c5d",
      "artifact": "Artifact#6254",
      "budget": "Budget#a763",
      "solver": "Solver#1c9b"
    }
  }
}
```

---

## CapacityPressure#739d

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
      "type": "Float",
      "range": "unspecified",
      "description": "Target resource utilization ratio that triggers forced abstraction"
    },
    {
      "name": "resource_type",
      "type": "Enum",
      "range": "unspecified",
      "description": "Type of resource being constrained (compute, memory, bandwidth)"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_layer": "Society",
  "sema_category": "Economics",
  "sema_id": "sema:CapacityPressure#mh:SHA-256:739d57e4af53954f0cb6f880e87d85c784fea7e82643376e72777bbcd42f0d85",
  "sema_ref": "CapacityPressure#739d",
  "sema_stub": "739d",
  "dependencies": {
    "references": {
      "context_compress": "ContextCompress#6dbd",
      "concept_blend": "ConceptBlend#22f2",
      "agent": "Agent#aaec",
      "generalize": "Generalize#17c9",
      "budget": "Budget#a763",
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## Compromise#39cc

```json
{
  "handle": "Compromise",
  "mechanism": "Iterative Negotiation Protocol. Each {{agent}} states preferences with INTENSITY scores (0-1). The {{system}} computes DISSONANCE (Sum(Intensity_A * Intensity_B)). To reach consensus, agents must {{dampen}} their preference intensity until Dissonance < Threshold. Unlike {{yield}} (which is binary surrender), Compromise is a continuous reduction of demand.",
  "gloss": "Finding a mutual sacrifice zone via intensity reduction",
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 1
  },
  "sema_ref": "Compromise#39cc",
  "sema_id": "sema:Compromise#mh:SHA-256:39cc701b1389e8827a263f5180a40cea2993edf2ef94c9906553d48e9507c59f",
  "sema_stub": "39cc",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "composes_with": {
      "dampen": "Dampen#ff89"
    },
    "references": {
      "yield": "Yield#7eaf",
      "system": "System#e314",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## ContinuousResourceAuction#babf

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
      "range": "{CongestionPricing, DutchAuction, Linear#81af}",
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
      "AttentionMarkets#9236"
    ]
  },
  "sema_ref": "ContinuousResourceAuction#babf",
  "sema_id": "sema:ContinuousResourceAuction#mh:SHA-256:babf1b41f451b6df2220129e0c0a05483abfc8f8aa8b4bfd3f7fd543ac9e009f",
  "sema_stub": "babf",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "protocol": "Protocol#7e1c"
    },
    "composes_with": {
      "state_lock": "StateLock#774b"
    },
    "accepts": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## DogfoodFirst#b595

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
    },
    {
      "name": "output_artifact",
      "type": "Solution#7186",
      "range": "unspecified",
      "description": "The solution artifact produced by self-testing"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "ring": 0
  },
  "sema_id": "sema:DogfoodFirst#mh:SHA-256:b595a866612b5006a8f7d1c8f1ae208271e15f9cf999271aa172116ed476a2d2",
  "sema_ref": "DogfoodFirst#b595",
  "sema_stub": "b595",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "gate": "Gate#206d",
      "canary": "Canary#e78e",
      "cognitive_bias": "CognitiveBias#4b32",
      "protocol": "Protocol#7e1c",
      "reflexion": "Reflexion#51b9"
    }
  }
}
```

---

## EmpathySim#86e9

```json
{
  "handle": "EmpathySim",
  "mechanism": "Theory of Mind simulation. {{agent}} instantiates a temporary 'Virtual {{context}}' initialized with Target_Agent's known priors, goals, and constraints. It then runs inference on this context to predict Target's next move. It spins up an isolated {{agent_sandbox}} to model the target's perspective.",
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
    },
    {
      "name": "target_profile",
      "type": "AgentProfile",
      "range": "unspecified",
      "description": "Profile of the agent whose state is being modeled"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Economics",
    "related": [
      "MentalSim#7212"
    ],
    "ring": 2
  },
  "sema_id": "sema:EmpathySim#mh:SHA-256:86e98d01cd322735f32c153f35f6d58c4d08ead468b5aa2fe07810483f9de445",
  "sema_ref": "EmpathySim#86e9",
  "sema_stub": "86e9",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "simulation": "Simulation#8035",
      "agent": "Agent#aaec",
      "context": "Context#510a",
      "state": "State#4d58",
      "agent_sandbox": "AgentSandbox#06f2",
      "budget": "Budget#a763"
    }
  }
}
```

---

## ExchangeRate#be29

```json
{
  "handle": "ExchangeRate",
  "mechanism": "A definable ratio between two distinct {{value}} types or {{metric}}s at a specific point in time. It allows agents with orthogonal utility functions to transact.",
  "gloss": "Conversion ratio between value systems",
  "invariants": [
    "Bijectivity: Rate(A->B) must equal 1 / Rate(B->A).",
    "Time-Bound: Must include a timestamp or validity window."
  ],
  "sema_id": "sema:ExchangeRate#mh:SHA-256:be292881aae1af318995e3c0617ed90f9871d2d7e1c6c64e8083fa9a1b3b94f6",
  "sema_ref": "ExchangeRate#be29",
  "sema_stub": "be29",
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
      "metric": "Metric#8895",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Gardener#5d74

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
    "ring": 0
  },
  "sema_id": "sema:Gardener#mh:SHA-256:5d74a3fff3bfed7f1d584d7894efca02274223d478477ffb00a99df127453d48",
  "sema_ref": "Gardener#5d74",
  "sema_stub": "5d74",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "signature": [
    "Stigmergy#f624(Care#cdfa)"
  ],
  "dependencies": {
    "references": {
      "care": "Care#cdfa",
      "graceful_degradation": "GracefulDegradation#f6d7",
      "stigmergy": "Stigmergy#f624",
      "compensate": "Compensate#269d"
    }
  }
}
```

---

## LivedProof#ae2d

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
    "layer": "Society",
    "category": "Economics",
    "ring": 2
  },
  "sema_id": "sema:LivedProof#mh:SHA-256:ae2df3c960792c30d022bff87745721b39d9384ddc511993d610b68b6b526183",
  "sema_ref": "LivedProof#ae2d",
  "sema_stub": "ae2d",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "identity": "Identity#626c",
      "signal": "Signal#f39d",
      "dogfood_first": "DogfoodFirst#b595"
    }
  }
}
```

---

## MarginalValueRule#2033

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
    "layer": "Society",
    "category": "Economics",
    "tier": 2,
    "ring": 1
  },
  "sema_id": "sema:MarginalValueRule#mh:SHA-256:2033df45f276a84502c54eaa8d1793a49e798212f36e3167b4c9e78c60bf4232",
  "sema_ref": "MarginalValueRule#2033",
  "sema_stub": "2033",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "signature": [
    "Budget#a763(RecursionDive#4ce3)"
  ],
  "dependencies": {
    "references": {
      "budget": "Budget#a763",
      "estimate": "Estimate#bb30",
      "recursion_dive": "RecursionDive#4ce3"
    }
  }
}
```

---

## MintWhenFriction#d48d

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
      "type": "Float",
      "range": "unspecified",
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
  "sema_id": "sema:MintWhenFriction#mh:SHA-256:d48d58e14fdd17707bd90aaeab196fc13189a2d39b37aaa8b086c4e03356ff57",
  "sema_ref": "MintWhenFriction#d48d",
  "sema_stub": "d48d",
  "dependencies": {
    "references": {
      "pattern_discovery": "PatternDiscovery#f667",
      "check": "Check#1544",
      "construct_ontology": "ConstructOntology#b59e",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Resonate#99d9

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
    "category": "Economics",
    "ring": 1
  },
  "sema_id": "sema:Resonate#mh:SHA-256:99d9c2629e862fb9f647bb98e30eba4a47b9204bea6e61f79709b65f8fac55b4",
  "sema_ref": "Resonate#99d9",
  "sema_stub": "99d9",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e",
      "decay": "Decay#a1d4",
      "signal": "Signal#f39d",
      "spectral_tune": "SpectralTune#6c65",
      "noise": "Noise#c4b4",
      "dampen": "Dampen#ff89"
    }
  }
}
```

---

## ValuePeg#073f

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
  "sema_id": "sema:ValuePeg#mh:SHA-256:073fde121fc20973de3aaa17aab1af3f37f50370df31a0030cdef095095a4e5c",
  "sema_ref": "ValuePeg#073f",
  "sema_stub": "073f",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "yields": {
      "exchange_rate": "ExchangeRate#be29"
    },
    "references": {
      "value": "Value#3c5d",
      "optimize": "Optimize#3075"
    }
  }
}
```

---

## Yield#7eaf

```json
{
  "handle": "Yield",
  "mechanism": "Negotiation {{backoff}}. When `{{overlap}}` fails: 1. Agents declare 'Flex' (concession) and 'Weight' (importance). 2. {{system}} computes Yield-Ratio. 3. Lower-weighted preference cedes to higher. 4. Debt recorded in Ledger. Utilizes {{defer}}.",
  "gloss": "Enable fair resolution of genuine disagreements without defaulting to power dynamics or eternal deadlock",
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
  "sema_id": "sema:Yield#mh:SHA-256:7eaffd4f68072f2f82302e3d2deb33a830bc9f1148b64d705cf4d08125b248e0",
  "sema_ref": "Yield#7eaf",
  "sema_stub": "7eaf",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "defer": "Defer#6460",
      "overlap": "Overlap#bcfa",
      "backoff": "Backoff#315a",
      "system": "System#e314"
    }
  }
}
```

---

## AnchorDrop#bf63

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
  "sema_id": "sema:AnchorDrop#mh:SHA-256:bf63d7b42444f4b7d7f8c1efbf50574153743cc958b05dd96961f4d27ba799e8",
  "sema_ref": "AnchorDrop#bf63",
  "sema_stub": "bf63",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "consensus": "Consensus#7216",
      "quorum": "Quorum#29b4",
      "system": "System#e314"
    }
  }
}
```

---

## Consensus#7216

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
    "category": "Governance",
    "ring": 0,
    "related": [
      "Sync"
    ]
  },
  "sema_id": "sema:Consensus#mh:SHA-256:7216e0e528262020ff05fa26124a8db9fcb14613fde05ddd0b2eb393958c4211",
  "sema_ref": "Consensus#7216",
  "sema_stub": "7216",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "composes_with": {
      "quorum": "Quorum#29b4",
      "vote": "Vote#30d0"
    },
    "yields": {
      "value": "Value#3c5d"
    },
    "accepts": {
      "proposal": "Proposal#4840"
    }
  }
}
```

---

## ConsensusFinder#1c5d

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
    "category": "Governance",
    "ring": 1
  },
  "sema_id": "sema:ConsensusFinder#mh:SHA-256:1c5d954ef53633228e32d5e237a7c2d372d48e6fcaefda775589c952e457eafa",
  "sema_ref": "ConsensusFinder#1c5d",
  "sema_stub": "1c5d",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "signature": [
    "Discover#afa1(Consensus#7216)"
  ],
  "dependencies": {
    "references": {
      "resonate": "Resonate#99d9",
      "discover": "Discover#afa1",
      "consensus": "Consensus#7216",
      "quorum": "Quorum#29b4"
    }
  }
}
```

---

## Constitution#863b

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
  "sema_id": "sema:Constitution#mh:SHA-256:863bf057265f5f954e50385d6fdb5f59d2f0619e7927cb6e45d281603725efe9",
  "sema_ref": "Constitution#863b",
  "sema_stub": "863b",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec"
    }
  }
}
```

---

## Delegate#7e2a

```json
{
  "handle": "Delegate",
  "mechanism": "{{work}} distribution protocol with acceptance, tracking, and failure handling. Delegator sends 'DELEGATE' message. Delegatee responds 'ACCEPT' or 'REFUSE'. On accept, delegatee owns {{task}} and sends 'PROGRESS' via {{heartbeat}}. On completion, delegator receives result. On failure, delegatee sends {{break}}\u2014delegator decides: reassign, retry, or escalate. Broadcast delegation creates auction. It employs {{probe}} to verify capabilities. Inherits {{holographic_shard}}.",
  "gloss": "Enable structured work distribution with accountability",
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
    "category": "Governance",
    "related": [
      "Handoff#f72f"
    ],
    "ring": 1
  },
  "sema_id": "sema:Delegate#mh:SHA-256:7e2aa7273061011208a1e1d26d4d616deed5499d29d5275ff3f09dc878e8bbc0",
  "sema_ref": "Delegate#7e2a",
  "sema_stub": "7e2a",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "break": "Break#1a63"
    },
    "accepts": {
      "holographic_shard": "HolographicShard#1352"
    },
    "composes_with": {
      "heartbeat": "Heartbeat#7f88",
      "probe": "Probe#9f2b"
    },
    "yields": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Disband#7cb8

```json
{
  "handle": "Disband",
  "mechanism": "Graceful group dissolution with state disposition and clean termination. {{agent}} sends 'DISBAND' signal. For scope='member': notify remaining members, adjust shared state, check {{quorum}}. For scope='group': broadcast 'DISSOLVING', execute state disposition, release shared resources, and record dissolution with a group {{snapshot}} for potential re-formation. All members must ACK dissolution. It safely terminates the group, optionally triggering {{ejection_seat}} for any members refusing to release shared resources.",
  "gloss": "Enable clean group termination with proper state handling",
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
    "category": "Governance",
    "ring": 1
  },
  "sema_id": "sema:Disband#mh:SHA-256:7cb883dd99a51f2408f92e5d48d69d4c3f077db9d49e3754a1f99af92126b0cf",
  "sema_ref": "Disband#7cb8",
  "sema_stub": "7cb8",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "ejection_seat": "EjectionSeat#6ff7",
      "quorum": "Quorum#29b4",
      "agent": "Agent#aaec",
      "state": "State#4d58"
    },
    "yields": {
      "snapshot": "Snapshot#0ae9"
    }
  }
}
```

---

## Elect#4042

```json
{
  "handle": "Elect",
  "mechanism": "Establish leadership role with nomination, powers, term, and succession. Phase 1 NOMINATE: Members send NOMINATE: {nominee, nominator, reason}. Self-nomination allowed if configured. Nominees must satisfy {{accept_spec}} to appear on {{ballot}}\u2014cannot elect unwilling leader. Phase 2 VOTE: Standard VOTE mechanism among accepted nominees. Phase 3 INVEST: Winner receives {{solution}} (Election Result): {elected, powers[] (explicitly granted authorities), term (fixed|task|indefinite|renewable), succession_plan (automatic|re_elect|fallback)}. Leader exercises granted powers until term ends, resignation, or recall. On term end: succession triggers per plan. RECALL mechanism if enabled: member initiates RECALL_MOTION: {reason}, group VOTEs, if threshold met leader removed and succession triggers.",
  "gloss": "Enable efficient group coordination through configurable leadership with clear authority boundaries and succession planning",
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
    "category": "Governance",
    "related": [
      "Vote#30d0"
    ],
    "ring": 2
  },
  "sema_id": "sema:Elect#mh:SHA-256:4042f6af9faaf5b85a276ec88bddf7accacf63be9c7a917bfb4ff16bbf7e74a3",
  "sema_ref": "Elect#4042",
  "sema_stub": "4042",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "accepts": {
      "accept_spec": "AcceptSpec#70dd",
      "ballot": "Ballot#f1d7"
    },
    "yields": {
      "solution": "Solution#7186"
    }
  }
}
```

---

## LazyConsensus#4fc7

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
    "category": "Governance",
    "ring": 0
  },
  "sema_ref": "LazyConsensus#4fc7",
  "sema_id": "sema:LazyConsensus#mh:SHA-256:4fc707a3608b99da4f2f0aa78d8662d3ea7056beb69e92a72be26e6085ecbfd9",
  "sema_stub": "4fc7",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "time_warp_log": "TimeWarpLog#d938",
      "quorum": "Quorum#29b4"
    }
  }
}
```

---

## Rally#8d04

```json
{
  "handle": "Rally",
  "mechanism": "Ad-Hoc Group Formation {{protocol}}. Initiator broadcasts a 'RALLY' signal with requirements defined by an {{accept_spec}} and a selection criteria. Responders submit 'ENLIST' messages. If count >= {{quorum}} by deadline, initiator executes {{select}} and sends 'MUSTER' to form a new cryptographic group {{context}}. It broadcasts a call to form a group, using {{quorum}} to validate critical mass and {{elect}} to formalize leadership.",
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
      "type": "Integer",
      "range": "unspecified",
      "description": "Default: 10"
    },
    {
      "name": "min_participants",
      "type": "Integer",
      "range": "[1, 50]",
      "description": "Minimum agents required to proceed"
    },
    {
      "name": "selection_criteria",
      "type": "PatternRef",
      "range": "unspecified",
      "description": "Default: Select"
    }
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Governance",
    "ring": 1
  },
  "sema_id": "sema:Rally#mh:SHA-256:8d0401a21776e9a4d44b60bd1c7a8d7af1c9d275c3d209ef12432c892f435cec",
  "sema_ref": "Rally#8d04",
  "sema_stub": "8d04",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "quorum": "Quorum#29b4",
      "context": "Context#510a",
      "protocol": "Protocol#7e1c",
      "select": "Select#15c2",
      "elect": "Elect#4042"
    },
    "composes_with": {
      "accept_spec": "AcceptSpec#70dd"
    }
  }
}
```

---

## Responsibility#fe7e

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
    },
    {
      "name": "escalation_path",
      "type": "String",
      "range": "unspecified",
      "description": "Who to notify on violation"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 1
  },
  "sema_id": "sema:Responsibility#mh:SHA-256:fe7e40db4c4adb2876931c24f48a911975c4729ee3d97017502123d8afc7b001",
  "sema_ref": "Responsibility#fe7e",
  "sema_stub": "fe7e",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "oath_bind": "OathBind#fe32",
      "heartbeat": "Heartbeat#7f88",
      "state": "State#4d58"
    }
  }
}
```

---

## Role#fc9f

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
  "sema_ref": "Role#fc9f",
  "sema_id": "sema:Role#mh:SHA-256:fc9f298f0755ca88460701865e0201dcfa628426f4a376cab0a2c55af9e849d1",
  "sema_stub": "fc9f",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "permission": "Permission#7f7d",
      "responsibility": "Responsibility#fe7e"
    }
  }
}
```

---

## SolverRoot#5358

```json
{
  "handle": "SolverRoot",
  "mechanism": "The genesis node of a solver tree, anchoring a {{task}} to a coordinated problem-solving effort. The Root has unique authority: Problem Framing (determining initial constraints and {{problem_space}}), Budget Allocation (distributing {{budget}} to child {{solver_node}}s), and Ultimate Accountability (owning final {{result}}). The Root propagates the {{tree}} structure downward and aggregates {{solution}}s upward. When downstream nodes fail, the Root decides whether to reframe the {{problem}} or escalate failure. The Root is indifferent to whether it orchestrates 'self' (internal reasoning) or 'other' (delegated agents).",
  "gloss": "Genesis authority and framer of a solver tree",
  "failure_modes": [
    "Bad Frame: The {{problem}} is framed incorrectly, making it unsolvable by downstream nodes.",
    "Reframe Failure: Root fails to find a valid alternative frame after failure.",
    "Budget Misallocation: Resources distributed poorly across child nodes."
  ],
  "invariants": [
    "Genesis: Every solver tree has exactly one active Root.",
    "Ultimate Responsibility: The Root owns the final success/failure of the {{task}}.",
    "Authority: Only the Root can reframe the original {{problem}}."
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
      "children": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Child solver node refs"
      }
    }
  },
  "sema_ref": "SolverRoot#5358",
  "sema_id": "sema:SolverRoot#mh:SHA-256:53586f98685cb166b0bed58a7e06f5aafe90f3f7d30cd9fcfd085503339fff75",
  "sema_stub": "5358",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "solver_node": "SolverNode#3a4f",
      "tree": "Tree#ddce",
      "task": "Task#d9f9",
      "problem_space": "ProblemSpace#78da",
      "result": "Result#8ed9",
      "budget": "Budget#a763",
      "solution": "Solution#7186",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## SolverTree#0f1d

```json
{
  "handle": "SolverTree",
  "mechanism": "The active command hierarchy that organizes {{solver_node}} instances into a coordinated {{topology}} for solving a {{task}}. Unlike a passive data tree, this structure represents the flow of Authority (downwards via delegation) and Results (upwards via reporting). It defines the Chain of Command: resources ({{budget}}) cascade from {{solver_root}} to children, while outcomes propagate back up. Each node in the tree is a unit of Blame\u2014failures can be traced to specific {{solver_node}}s for {{localized_learning}}.",
  "gloss": "Active hierarchy of coordinated solver instances",
  "failure_modes": [
    "Fragmentation: Sub-trees become disconnected from the Root, breaking the command chain.",
    "Budget Exhaustion: Resources depleted before solution found.",
    "Blame Diffusion: Failures cannot be attributed to specific nodes."
  ],
  "invariants": [
    "Chain of Command: Every node (except root) has exactly one active supervisor.",
    "Budget Flow: Resources flow down; Results flow up.",
    "Connectivity: All nodes must be traceable back to the {{solver_root}}.",
    "Acyclicity: The structure must form a DAG or {{tree}}."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Governance",
    "ring": 1,
    "related": [
      "UniversalSolverTree#4d9c"
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
  "sema_ref": "SolverTree#0f1d",
  "sema_id": "sema:SolverTree#mh:SHA-256:0f1d42b0d863374e04cc85cbebb9d56a80ac9767de97c93603a3b26785f45493",
  "sema_stub": "0f1d",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "solver_node": "SolverNode#3a4f",
      "tree": "Tree#ddce",
      "localized_learning": "LocalizedLearning#69bb",
      "budget": "Budget#a763",
      "solver_root": "SolverRoot#5358"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## TriGate#07fc

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
    "Gate#206d(Judge#d84f)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Governance",
    "ring": 0,
    "tier": 1
  },
  "sema_ref": "TriGate#07fc",
  "sema_id": "sema:TriGate#mh:SHA-256:07fcf444936e65c3cf14c77b8c7c3a1ca5d105462ea67ad26a970965ecfbc18c",
  "sema_stub": "07fc",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "gate": "Gate#206d",
      "judge": "Judge#d84f",
      "condition": "Condition#cbd5",
      "ledger": "Ledger#c363"
    }
  }
}
```

---

## UniversalSolverTree#4d9c

```json
{
  "handle": "UniversalSolverTree",
  "mechanism": "The theoretical aggregation of all possible valid {{solver_tree}}s across all agents in the system. It represents the total epistemological state of {{problem}}-solving knowledge\u2014the collective wisdom of self and others. Any specific problem-solving effort is a traversal or instantiation of a sub-graph within this Universal {{tree}}. It enables cross-agent learning: identifying redundant efforts, reusing proven {{solver_node}} strategies, and sharing {{solution}}s. The Universal Tree is the ground truth against which {{localized_learning}} updates are integrated.",
  "gloss": "Collective knowledge graph of all problem-solving",
  "failure_modes": [
    "Fragmentation: Parts of the universal tree become inaccessible across agent boundaries.",
    "Inconsistency: Contradictory solutions exist in different branches without reconciliation.",
    "Knowledge Silos: Agent-local trees fail to sync with the universal tree."
  ],
  "invariants": [
    "Singularity: There is logically only one Universal {{tree}} containing all knowledge.",
    "Coherence: Contradictions must eventually be resolved via synthesis or rejection."
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
  "sema_ref": "UniversalSolverTree#4d9c",
  "sema_id": "sema:UniversalSolverTree#mh:SHA-256:4d9cbaa5af0017d4a249fe403c0697457fca53911eca6edd92dcce00b11ec75d",
  "sema_stub": "4d9c",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "solver_node": "SolverNode#3a4f",
      "tree": "Tree#ddce",
      "localized_learning": "LocalizedLearning#69bb",
      "solver_tree": "SolverTree#0f1d",
      "solution": "Solution#7186",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## Vote#30d0

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
    "category": "Governance",
    "related": [
      "Rank#cb98"
    ],
    "ring": 2
  },
  "sema_id": "sema:Vote#mh:SHA-256:30d0f73565ea6b9b3ec56cac26b7a54ae4533e9db9ea47b6a79691c5b9e69264",
  "sema_ref": "Vote#30d0",
  "sema_stub": "30d0",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "composes_with": {
      "quorum": "Quorum#29b4"
    },
    "references": {
      "break": "Break#1a63",
      "system": "System#e314",
      "aggregate": "Aggregate#af54",
      "elect": "Elect#4042"
    },
    "accepts": {
      "ballot": "Ballot#f1d7"
    }
  }
}
```

---

## WorldTransparent#0212

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
    "ring": 0
  },
  "sema_id": "sema:WorldTransparent#mh:SHA-256:021253e5183401b81b48c466232d879b07a94638281edc77b92002482365d977",
  "sema_ref": "WorldTransparent#0212",
  "sema_stub": "0212",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "explain_beacon": "ExplainBeacon#6ced",
      "system": "System#e314"
    }
  }
}
```

---

## AcceptSpec#70dd

```json
{
  "handle": "AcceptSpec",
  "mechanism": "A strict, typed {{spec}} defining non-compensatory {{criteria}} at solver boundaries. Unlike soft prompts, an AcceptSpec specifies hard {{constraint}}s (e.g., Must be < 100/ton, Must violate no laws of physics). If ANY criterion fails, the artifact is rejected entirely. High quality in one dimension cannot compensate for failure in another.",
  "gloss": "Non-compensatory failure boundaries",
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
  "sema_id": "sema:AcceptSpec#mh:SHA-256:70ddc45d00abda5ec5b7475b080d252f01c3db589490498563621665444293f1",
  "sema_ref": "AcceptSpec#70dd",
  "sema_stub": "70dd",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "criteria": "Criteria#ef6b",
      "spec": "Spec#436e"
    }
  }
}
```

---

## AdversarialProof#2a0f

```json
{
  "handle": "AdversarialProof",
  "mechanism": "Cognitively-enriched {{negative_proof}} that invokes {{red_team}} logic to exhaustively search for prohibited data. The adversarial mindset ensures blind spots are probed. Treats failure-to-find-despite-adversarial-effort as high-confidence proof of absence.",
  "gloss": "Adversarial proof of absence",
  "derived_from": "NegativeProof#5225",
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
  "sema_ref": "AdversarialProof#2a0f",
  "sema_id": "sema:AdversarialProof#mh:SHA-256:2a0f68fabd8276b169195d0f4d502049e0690343fbb6d7dd1e3d6b6f487581e9",
  "sema_stub": "2a0f",
  "dependencies": {
    "composes_with": {
      "red_team": "RedTeam#7a8d",
      "negative_proof": "NegativeProof#5225"
    },
    "references": {
      "hypothesis": "Hypothesis#e95b"
    }
  }
}
```

---

## Aesthetics#0be2

```json
{
  "handle": "Aesthetics",
  "mechanism": "A scalar {{metric}} representing the fit between an {{artifact}} and the subjective preference priors of a human observer (e.g., harmony, {{parsimony}}, style). Used to optimize solutions for social acceptance when functional utility is equal.",
  "gloss": "Optimization for human subjective preference",
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:Aesthetics#mh:SHA-256:0be2872e5fb0b634fca2f99bbba9349d658f95bdae5c2e1106f67a0f2a1e918c",
  "sema_ref": "Aesthetics#0be2",
  "sema_stub": "0be2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "metric": "Metric#8895",
      "artifact": "Artifact#6254",
      "parsimony": "Parsimony#1dd3"
    }
  }
}
```

---

## AgentDiscover#d88a

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
  "sema_id": "sema:AgentDiscover#mh:SHA-256:d88a7f9c1d65eda254b0cb54552da55832d849a23049c48a045059d9d24c2bf2",
  "sema_ref": "AgentDiscover#d88a",
  "sema_stub": "d88a",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Discover#afa1(Agent#aaec)"
  ],
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "card": "Card#c9f0",
      "discover": "Discover#afa1"
    }
  }
}
```

---

## AgentProtocol#5a7f

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
  "sema_id": "sema:AgentProtocol#mh:SHA-256:5a7f6660a1899ecda1ed37f8b781e629917ad4851a001ad11f33ea1ff91a87b3",
  "sema_ref": "AgentProtocol#5a7f",
  "sema_stub": "5a7f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Agent#aaec(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "fail_closed": "FailClosed#ae79",
      "accept_spec": "AcceptSpec#70dd",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "solution": "Solution#7186",
      "protocol": "Protocol#7e1c",
      "greet": "Greet#7ad2"
    }
  }
}
```

---

## AgentSandbox#06f2

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
      "Solution#7186",
      "Task#d9f9"
    ]
  },
  "sema_id": "sema:AgentSandbox#mh:SHA-256:06f29db915e1bbe17ebf20bab2964279a58c949bc61d386ab20de84749331fe6",
  "sema_ref": "AgentSandbox#06f2",
  "sema_stub": "06f2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Sandbox#2be7(Agent#aaec)"
  ],
  "dependencies": {
    "references": {
      "sandbox": "Sandbox#2be7",
      "agent": "Agent#aaec",
      "context": "Context#510a",
      "audit": "Audit#4044"
    },
    "composes_with": {
      "input_guard": "InputGuard#0770",
      "output_guard": "OutputGuard#eb44"
    }
  }
}
```

---

## AmbiguityResolution#aee6

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
  "sema_ref": "AmbiguityResolution#aee6",
  "sema_id": "sema:AmbiguityResolution#mh:SHA-256:aee6c8844ad85d09c8ce0fe0819c5359ba2b52e84bc56b23837c9b156b4fa0f1",
  "sema_stub": "aee6",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "vote": "Vote#30d0",
      "entropy_pump": "EntropyPump#b9ae"
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

## BoundedTask#06a6

```json
{
  "handle": "BoundedTask",
  "mechanism": "A specialized {{task}} enforcing {{budget}} and {{accept_spec}} to ensure economic and quality boundaries.",
  "gloss": "Economically constrained task",
  "invariants": [
    "Budget Enclosure",
    "Quality Gate"
  ],
  "derived_from": "Task#d9f9",
  "sema_id": "sema:BoundedTask#mh:SHA-256:06a6eab9f36242682b865ee828dc14f40c449301eed224727c1a801851333543",
  "sema_ref": "BoundedTask#06a6",
  "sema_stub": "06a6",
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
      "accept_spec": "AcceptSpec#70dd",
      "task": "Task#d9f9",
      "budget": "Budget#a763"
    }
  }
}
```

---

## Canary#e78e

```json
{
  "handle": "Canary",
  "mechanism": "Expendable {{agent}} tests full coordination path before committing real resources. Spawn CANARY with: limited resources (bounded blast radius), defined scope, telemetry hooks. Canary executes FULL coordination path ({{greet}}\u2192{{probe}}\u2192negotiate\u2192partial-execute). Reports TELEMETRY: {path_viable, latency_profile, error_events, partner_behavior_observations, recommendation: proceed|caution|abort}. Lifecycle options: DESTROY (discard after test), RECYCLE (reset for another test), PROMOTE (canary becomes real {{agent}}, continues {{work}}), ABSORB (real {{agent}} inherits canary's progress). In adversarial environments, canary can run in STEALTH {{mode}} (indistinguishable from real {{agent}}) to prevent partners gaming the test. It extends the logic of a single {{probe}} into a full-lifecycle agent deployment with bounded blast radius.",
  "gloss": "Transform path selection from 'hope it works' to 'tested it works' without risking real resources",
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
  "sema_id": "sema:Canary#mh:SHA-256:e78e513e7df0ad5a179c62c69261c4ce0d763f18aff8da449b15562522f503e2",
  "sema_ref": "Canary#e78e",
  "sema_stub": "e78e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "agent": "Agent#aaec",
      "mode": "Mode#53e0",
      "probe": "Probe#9f2b",
      "greet": "Greet#7ad2"
    }
  }
}
```

---

## CiteBack#d09c

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:CiteBack#mh:SHA-256:d09cb134d37aa235b88fbbcfa7667e3689b342d6a846bb58fad79fe2bef8e0e3",
  "sema_ref": "CiteBack#d09c",
  "sema_stub": "d09c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "retrieval_augment": "RetrievalAugment#ca58"
    }
  }
}
```

---

## CognitiveEcho#4a95

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
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "SignalReflection#aac2"
    ],
    "ring": 2
  },
  "sema_id": "sema:CognitiveEcho#mh:SHA-256:4a95eb01f8da6218a9e6a63ab78128286771cc9cc9e9f9716892177fa3af3758",
  "sema_ref": "CognitiveEcho#4a95",
  "sema_stub": "4a95",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "simulation": "Simulation#8035",
      "agent": "Agent#aaec",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## CommitmentDevice#8918

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:CommitmentDevice#mh:SHA-256:8918282b2c6931b5c735e42e565b19a78203bdef971b0a26cd73c4168a4671c6",
  "sema_ref": "CommitmentDevice#8918",
  "sema_stub": "8918",
  "sema_layer": "Society",
  "sema_category": "Protocols",
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
      "agent": "Agent#aaec",
      "oath_bind": "OathBind#fe32"
    }
  }
}
```

---

## Compose#1023

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:Compose#mh:SHA-256:102324081e15319ea27337fd0e28928b9b7a738f34e2a558573239e08af03a7a",
  "sema_ref": "Compose#1023",
  "sema_stub": "1023",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Combine#5a44(PromptChain#d3f2)"
  ],
  "dependencies": {
    "references": {
      "check": "Check#1544",
      "prompt_chain": "PromptChain#d3f2",
      "combine": "Combine#5a44"
    }
  }
}
```

---

## ConfusedDeputy#31db

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
    "ring": 0
  },
  "sema_ref": "ConfusedDeputy#31db",
  "sema_id": "sema:ConfusedDeputy#mh:SHA-256:31db289ffbcd442a10cddc5c1d3460132fd073a680d436e364684e89c37a39c2",
  "sema_stub": "31db",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "permission": "Permission#7f7d",
      "actor": "Actor#6926"
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:ConstraintFirst#mh:SHA-256:c7cb09081701787022c33fa3b1399bd847b0062cf223851c4d98024b640feb99",
  "sema_ref": "ConstraintFirst#c7cb",
  "sema_stub": "c7cb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## ConstructOntology#b59e

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ConstructOntology#mh:SHA-256:b59ea97d742c1e307e029f1a05ef0f17c8d30f14f1c9167ef37a0147bc0e1af8",
  "sema_ref": "ConstructOntology#b59e",
  "sema_stub": "b59e",
  "dependencies": {
    "references": {
      "adversarial_steel": "AdversarialSteel#35f0",
      "first_principles": "FirstPrinciples#c379",
      "ontology_handshake": "OntologyHandshake#ead0"
    }
  }
}
```

---

## ContextSwitch#42cd

```json
{
  "handle": "ContextSwitch",
  "mechanism": "{{agent}}s explicitly use {{switch}} to signal a change in {{context}} (protocol {{mode}}). All subsequent messages are interpreted under the new ruleset until a 'Revert' signal is sent.",
  "gloss": "Explicit mode toggling",
  "sema_id": "sema:ContextSwitch#mh:SHA-256:42cd102f1c3a2cba8029abd03d5949fb5b75b3df128016ef8bcb97f9304d8aef",
  "sema_ref": "ContextSwitch#42cd",
  "sema_stub": "42cd",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Switch#e7f9(Context#510a)"
  ],
  "dependencies": {
    "references": {
      "switch": "Switch#e7f9",
      "agent": "Agent#aaec",
      "mode": "Mode#53e0"
    },
    "accepts": {
      "context": "Context#510a"
    }
  }
}
```

---

## CounterfactualAnchor#4d4a

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
      "type": "String",
      "range": "unspecified",
      "description": "Temporal resolution for counterfactual comparison (e.g., hour, day, week)"
    },
    {
      "name": "retention_policy",
      "type": "Duration",
      "range": "unspecified",
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
  "sema_id": "sema:CounterfactualAnchor#mh:SHA-256:4d4acdb9ee21f5c41d45e40496a2879c5c8c79efcab7f389fb6f6f36588ac23c",
  "sema_ref": "CounterfactualAnchor#4d4a",
  "sema_stub": "4d4a",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "cognitive_bias": "CognitiveBias#4b32",
      "agent": "Agent#aaec",
      "surprisal_update": "SurprisalUpdate#6ef1",
      "observe": "Observe#8ebd"
    }
  }
}
```

---

## CurriculumReplay#a8f7

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:CurriculumReplay#mh:SHA-256:a8f76f8f131ce81e85201e2ce5ba85892274510bfd20d1bbdeb9581e61cf28af",
  "sema_ref": "CurriculumReplay#a8f7",
  "sema_stub": "a8f7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "decay": "Decay#a1d4",
      "experience_sharding": "ExperienceSharding#d920"
    }
  }
}
```

---

## DataMinimization#0b54

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
    "ring": 0
  },
  "sema_id": "sema:DataMinimization#mh:SHA-256:0b54a9716e554f7198c94df50c7d6294fd772b8a939e5ac49f82d5c70eedb8fc",
  "sema_ref": "DataMinimization#0b54",
  "sema_stub": "0b54",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "input_guard": "InputGuard#0770",
      "accept_spec": "AcceptSpec#70dd",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "correlation": "Correlation#091f",
      "context": "Context#510a",
      "protocol": "Protocol#7e1c",
      "select": "Select#15c2",
      "context_compress": "ContextCompress#6dbd"
    }
  }
}
```

---

## DeepResearch#cbe3

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:DeepResearch#mh:SHA-256:cbe339d17080d67469ea0b220f5142dc63862ea423da4a2253a89011696e1f8d",
  "sema_ref": "DeepResearch#cbe3",
  "sema_stub": "cbe3",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Deep#89f0(Discover#afa1)"
  ],
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "deep": "Deep#89f0",
      "synthesis": "Synthesis#3252",
      "discover": "Discover#afa1",
      "retrieval_augment": "RetrievalAugment#ca58"
    }
  }
}
```

---

## DeliberativeAlign#8ba2

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
      "name": "constitution_ref",
      "type": "SemaRef",
      "range": "unspecified",
      "description": "Pointer to Constitution"
    },
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
    "ring": 0
  },
  "sema_id": "sema:DeliberativeAlign#mh:SHA-256:8ba23d93d396cd97abdfc7464d88f8e30d6bd4346e7614a7677bd500caa9cd05",
  "sema_ref": "DeliberativeAlign#8ba2",
  "sema_stub": "8ba2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "trace": "Trace#9057",
      "solver_node": "SolverNode#3a4f",
      "agent": "Agent#aaec",
      "context": "Context#510a",
      "constitution": "Constitution#863b",
      "manifest_planning": "ManifestPlanning#8f61",
      "check": "Check#1544"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## Deploy#5576

```json
{
  "handle": "Deploy",
  "mechanism": "The {{act}} of moving an artifact or system from a development/staging environment to a production environment. It executes the {{rollout}} process to make the system active and accessible to users.",
  "gloss": "Release to production",
  "signature": [
    "Act#5d55(Rollout#28ac)"
  ],
  "failure_modes": [
    "Config Drift: Production environment differs from staging."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_ref": "Deploy#5576",
  "sema_id": "sema:Deploy#mh:SHA-256:5576f4e6954159220fcfd0c3fc90e482c22a6bf649c19e22989fe458241c5735",
  "sema_stub": "5576",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "rollout": "Rollout#28ac",
      "act": "Act#5d55"
    }
  }
}
```

---

## Discover#afa1

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
  "sema_id": "sema:Discover#mh:SHA-256:afa14d67f5837d32ee70ae99c0b625d39864254bafd2b11b0ef690cc8fda5dbc",
  "sema_ref": "Discover#afa1",
  "sema_stub": "afa1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "search": "Search#d608",
      "criteria": "Criteria#ef6b",
      "signal": "Signal#f39d",
      "check": "Check#1544"
    }
  }
}
```

---

## DissentSeek#bd28

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
  "sema_id": "sema:DissentSeek#mh:SHA-256:bd28d5bd7fa2253411b69c586231a1a80b835cc56569439dc8834540dcefaf54",
  "sema_ref": "DissentSeek#bd28",
  "sema_stub": "bd28",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "steelman_check": "SteelmanCheck#4f4c",
      "understand": "Understand#96d4",
      "quorum": "Quorum#29b4",
      "confirmation_block": "ConfirmationBlock#3dae"
    }
  }
}
```

---

## DriftWatch#a20d

```json
{
  "handle": "DriftWatch",
  "mechanism": "Reputation via micro-deviation detection. 1. Baseline: Establish behavioral frequency. 2. Sample: Continuous high-res observation. 3. Detect: Alert if Distance(Current, Baseline) > 2 sigma. 4. Witness: Aggregated peer reports. It tracks behavioral consistency by monitoring deviations from a baseline {{aggregate}} of historical actions.",
  "gloss": "Reputation becomes pattern-fidelity measurement - trustworthiness equals predictability. Agents are trusted not for peak performance but for behavioral consistency. Gaming reputation through occasional spectacular actions becomes impossible.",
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
  "sema_id": "sema:DriftWatch#mh:SHA-256:a20dcee6f5453e3b61973fcf01aebd6a5ed4cfb97d1402a4ed970d8629a55a69",
  "sema_ref": "DriftWatch#a20d",
  "sema_stub": "a20d",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "aggregate": "Aggregate#af54"
    }
  }
}
```

---

## EbbFlowSync#b4a0

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
    "ring": 0
  },
  "sema_id": "sema:EbbFlowSync#mh:SHA-256:b4a07e620d27785381b12c3853380f0cef04bc9832acc1bd0b73f72a97b21de6",
  "sema_ref": "EbbFlowSync#b4a0",
  "sema_stub": "b4a0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "transition": "Transition#072d",
      "state": "State#4d58",
      "lock": "Lock#051c",
      "global": "Global#803d",
      "hysteresis": "Hysteresis#78b0"
    }
  }
}
```

---

## EjectionSeat#6ff7

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
  "sema_id": "sema:EjectionSeat#mh:SHA-256:6ff7358344beab6ce5a857d06a7a1fdb930613ef690886a5e467fd1bada8ab38",
  "sema_ref": "EjectionSeat#6ff7",
  "sema_stub": "6ff7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "compensate": "Compensate#269d"
    }
  }
}
```

---

## EvaluatorOptimizer#7ec6

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
  "sema_id": "sema:EvaluatorOptimizer#mh:SHA-256:7ec6beac2574ee29a4e1ae88bf8420bd8c030a22867de7916800004a299b33c2",
  "sema_ref": "EvaluatorOptimizer#7ec6",
  "sema_stub": "7ec6",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Optimize#3075(Loop#fb2e)"
  ],
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e",
      "optimize": "Optimize#3075",
      "context": "Context#510a",
      "meta_check": "MetaCheck#a228",
      "criteria": "Criteria#ef6b"
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
      "Plan#64f2",
      "Build#00f3",
      "Rollout#28ac"
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

## Expansive#c3b7

```json
{
  "handle": "Expansive",
  "gloss": "Evaluates generalization potential",
  "mechanism": "Evaluates generalization potential. Classifies scope into three qualitative states: (1) Niche: Overfit to a single problem instance or domain. (2) Untested: Plausible transfer to other domains, but unproven. (3) General: Proven utility across multiple distinct domains or a 'Hostile Slice'. It acts as a {{judge}} of the potential {{value}} of a solution beyond its initial context.",
  "invariants": [
    "Transfer: Must operate outside training distribution."
  ],
  "signature": [
    "Judge#d84f(Value#3c5d)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Expansive#mh:SHA-256:c3b714ddf5d18f2ff6ff15d126f71cf79bd78ac170e83608d6d8bacee45dae04",
  "sema_ref": "Expansive#c3b7",
  "sema_stub": "c3b7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "judge": "Judge#d84f",
      "value": "Value#3c5d"
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
    "ring": 0
  },
  "sema_id": "sema:ExpiringToken#mh:SHA-256:4e3cc3cee0de56a4eef0676629811cb4afa3383bc80bde227924d66a6af16f6e",
  "sema_ref": "ExpiringToken#4e3c",
  "sema_stub": "4e3c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "bearer_token": "BearerToken#2fe9",
      "decay": "Decay#a1d4"
    }
  }
}
```

---

## FabricSharding#7399

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
  "sema_id": "sema:FabricSharding#mh:SHA-256:7399195af56d8e2d611c2e3b004b990de8c838788156755bfeba1397080b125b",
  "sema_ref": "FabricSharding#7399",
  "sema_stub": "7399",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "parallelize": "Parallelize#d6b4",
      "shard": "Shard#1e74"
    }
  }
}
```

---

## FailClosed#ae79

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
      "range": "{Reject, Retry#d53d, Fallback}",
      "description": "Default: Reject"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:FailClosed#mh:SHA-256:ae79e8e091ca9f68f749936a99d55a386fba49254f9e7e958806b16b860332a1",
  "sema_ref": "FailClosed#ae79",
  "sema_stub": "ae79",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "circuit_breaker": "CircuitBreaker#4162",
      "output_guard": "OutputGuard#eb44",
      "system": "System#e314"
    }
  }
}
```

---

## FeatureFlag#9464

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
  "sema_id": "sema:FeatureFlag#mh:SHA-256:9464b708479fc75cc5d825850393199c41c35e06f20a2861954e98f8edcfa8a8",
  "sema_ref": "FeatureFlag#9464",
  "sema_stub": "9464",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## FeedbackSignal#f904

```json
{
  "handle": "FeedbackSignal",
  "mechanism": "A structured packet containing the evaluation of a specific {{solution}} for a {{task}}. Carries outcome and details to the {{feedback}} mechanism.",
  "gloss": "Standardized learning feedback packet",
  "invariants": [
    "Targeted",
    "Structured"
  ],
  "sema_id": "sema:FeedbackSignal#mh:SHA-256:f90478ac868a5f7cc8800278a412c19dfaf50e8edb7a93a06dce6c0ae41ae52c",
  "sema_ref": "FeedbackSignal#f904",
  "sema_stub": "f904",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
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
      "task": "Task#d9f9",
      "solution": "Solution#7186",
      "feedback": "Feedback#9b5c"
    }
  }
}
```

---

## Fermi#1e06

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:Fermi#mh:SHA-256:1e06d04bfff04954ad09852a7a4b1b583acc76c431dc926b4afe3cce5abfe210",
  "sema_ref": "Fermi#1e06",
  "sema_stub": "1e06",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "estimate": "Estimate#bb30",
      "decompose": "Decompose#ac56"
    }
  }
}
```

---

## FractalIntelligence#1c78

```json
{
  "handle": "FractalIntelligence",
  "mechanism": "The unified {{system}} of scalable cognition that uses {{reason}} to orchestrate the fractal expansion of intelligence within the {{universal_solver_tree}}. A {{problem_framer}} initiates the process, formulating a high-level {{strategy}} before assigning a {{cognitive_solver}} to a {{task}}. The solver executes a {{recursion_dive}} to spawn child nodes. As the tree deepens, nodes apply {{specialize}} to adapt to local sub-problems, using {{localized_learning}} to optimize performance. To ensure continuity and global coherence, the system employs {{experience_sharding}} to preserve memory and {{synthesis}} to integrate specialized insights back into the whole. {{state_snapshot}} creates save points for crash recovery. Efficiency is governed by the {{marginal_value_rule}}. If a path fails, {{reframe}} is triggered to restructure the tree or find a new {{problem_framer}}.",
  "gloss": "The unified fractal architecture of scalable, self-correcting intelligence",
  "invariants": [
    "Fractal Self-Similarity: The process at the Root is identical to the process at the Leaf.",
    "Bounded Expansion: Recursion is limited by Economic constraints (Marginal Value).",
    "Memory Conservation: Specialization must not result in the loss of global context."
  ],
  "signature": [
    "System#e314(Reason#3f24)"
  ],
  "derived_from": "sema:RecursiveIntelligence#mh:SHA-256:216c297a34a0847957d1a6a8701987248bc8d63294953a78346b5b68dbb9aef6",
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_ref": "FractalIntelligence#1c78",
  "sema_id": "sema:FractalIntelligence#mh:SHA-256:1c782df1a9a6cf2485d761b0c1e8abd6c9483d1a527e0d0a44ea8f074b84b05a",
  "sema_stub": "1c78",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "reason": "Reason#3f24",
      "recursion_dive": "RecursionDive#4ce3",
      "state_snapshot": "StateSnapshot#9ffc",
      "synthesis": "Synthesis#3252",
      "localized_learning": "LocalizedLearning#69bb",
      "problem_framer": "ProblemFramer#b310",
      "marginal_value_rule": "MarginalValueRule#2033",
      "reframe": "Reframe#ba00",
      "cognitive_solver": "CognitiveSolver#c6a7"
    },
    "references": {
      "system": "System#e314",
      "task": "Task#d9f9",
      "specialize": "Specialize#0a09",
      "universal_solver_tree": "UniversalSolverTree#4d9c",
      "strategy": "Strategy#47a4",
      "experience_sharding": "ExperienceSharding#d920"
    }
  }
}
```

---

## FrameSpec#d5b8

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
  "sema_id": "sema:FrameSpec#mh:SHA-256:d5b8e71aa9d57b941df3f914b941bfb8fe6c58f62d6c6db28532defcd2237d75",
  "sema_ref": "FrameSpec#d5b8",
  "sema_stub": "d5b8",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "spec": "Spec#436e",
      "constraint": "Constraint#87fe",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## GenealogicalTrace#342b

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
  "sema_id": "sema:GenealogicalTrace#mh:SHA-256:342b0a2d37308c145fb7b03e5710c7134342ee0918a273e9e532b74b2deff6e9",
  "sema_ref": "GenealogicalTrace#342b",
  "sema_stub": "342b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "trace_belief": "TraceBelief#a4bb",
      "cite_back": "CiteBack#d09c",
      "deep": "Deep#89f0",
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
    "ring": 0
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

## GracefulDegradation#f6d7

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
      "type": "ByteSize",
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
  "sema_id": "sema:GracefulDegradation#mh:SHA-256:f6d796365ffaa5244e54660f836f2e31ca948169f42fd305da33445cbfa30485",
  "sema_ref": "GracefulDegradation#f6d7",
  "sema_stub": "f6d7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "message": "Message#f767",
      "fail_closed": "FailClosed#ae79",
      "strategy": "Strategy#47a4"
    }
  }
}
```

---

## HackDetect#7588

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:HackDetect#mh:SHA-256:75886e18efbe83c14faa854c7a82c397b567e6678a9d5f208a42a7a0847b0f96",
  "sema_ref": "HackDetect#7588",
  "sema_stub": "7588",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "ejection_seat": "EjectionSeat#6ff7",
      "agent": "Agent#aaec",
      "input_guard": "InputGuard#0770",
      "system": "System#e314"
    }
  }
}
```

---

## Handoff#f72f

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
  "sema_id": "sema:Handoff#mh:SHA-256:f72f71fd9b8f43eb3b4516e2913f0d9c5a3506c31a827f4d910eba0e9adba87f",
  "sema_ref": "Handoff#f72f",
  "sema_stub": "f72f",
  "dependencies": {
    "accepts": {
      "task": "Task#d9f9",
      "responsibility": "Responsibility#fe7e",
      "context": "Context#510a"
    },
    "references": {
      "agent": "Agent#aaec",
      "state": "State#4d58"
    },
    "composes_with": {
      "delegate": "Delegate#7e2a"
    }
  }
}
```

---

## HeldRelease#4956

```json
{
  "handle": "HeldRelease",
  "mechanism": "{{value}} ({{unique_handle}}) held until condition met, released or returned on timeout. DEPOSIT: Party A sends value + condition_hash + timeout to escrow address. CLAIM: Party B submits condition_preimage; if hash(preimage) matches condition_hash, value releases to B. TIMEOUT: If timeout expires without valid claim, value returns to A. {{state}} transitions: EMPTY --deposit--> HELD --claim(valid)--> RELEASED_TO_B | --timeout--> RETURNED_TO_A. Primitives: hash commitment (SHA256), timelock (block height), 2-of-2 multisig or smart contract.",
  "gloss": "Trustless conditional value transfer becomes the primitive for all economic coordination - atomic swaps, payment channels, escrow, and conditional contracts all compose from this base pattern",
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
      "range": "{Queue#2ec3, Drop, Reject}",
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
  "sema_id": "sema:HeldRelease#mh:SHA-256:49566d2180cf09f70f2d9972dddd190dfb23c4cda4ff69ccab97b76930a34585",
  "sema_ref": "HeldRelease#4956",
  "sema_stub": "4956",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "state": "State#4d58",
      "value": "Value#3c5d"
    },
    "accepts": {
      "unique_handle": "UniqueHandle#11e7"
    }
  }
}
```

---

## IdempotentWrite#6c55

```json
{
  "handle": "IdempotentWrite",
  "mechanism": "A technical primitive where every write request includes a unique 'Idempotency Key'. The receiver tracks processed keys. If it receives a duplicate key, it returns the stored result without re-executing the side effects. This makes 'At-Least-Once' delivery safe. It uses a keyed {{state_lock}} to deduplicate requests, ensuring only the first write executes while subsequent ones return the cached result.",
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
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "UniqueHandle#11e7"
    ],
    "ring": 0
  },
  "sema_id": "sema:IdempotentWrite#mh:SHA-256:6c557713e21198238066f28ec889d6c877caab1f34d58c41baca371919e051af",
  "sema_ref": "IdempotentWrite#6c55",
  "sema_stub": "6c55",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#774b",
      "identity": "Identity#626c"
    }
  }
}
```

---

## IdentityHandshake#f2e8

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
    "category": "Protocols",
    "ring": 1,
    "caution": "Trust boundary \u2014 failure enables impersonation."
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:IdentityHandshake#mh:SHA-256:f2e812c10dde8b6eb942ab763f53a42d95fd797ac09ba951d4138119a2e813be",
  "sema_ref": "IdentityHandshake#f2e8",
  "sema_stub": "f2e8",
  "signature": [
    "Discover#afa1(Identity#626c)"
  ],
  "dependencies": {
    "references": {
      "nature": "Nature#6c1a",
      "identity": "Identity#626c",
      "spectral_tune": "SpectralTune#6c65",
      "ontology_handshake": "OntologyHandshake#ead0",
      "mode": "Mode#53e0",
      "discover": "Discover#afa1",
      "check": "Check#1544"
    }
  }
}
```

---

## IntentGap#5dc4

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
  "sema_ref": "IntentGap#5dc4",
  "sema_id": "sema:IntentGap#mh:SHA-256:5dc4af64c8178e975cb7d6c1325132b7af673a69e445a37f9dc1e4aa8565ef14",
  "sema_stub": "5dc4",
  "dependencies": {
    "references": {
      "outcome": "Outcome#38e0",
      "decision": "Decision#acfb"
    }
  }
}
```

---

## InternalConsistency#862f

```json
{
  "handle": "InternalConsistency",
  "mechanism": "A {{check}} that validates whether the components of an {{artifact}} adhere to the Principle of Non-Contradiction. It ensures that no two propositions within the {{context}} conflict with each other. Distinct from external {{validate}} (checking against a schema) or fact-checking (checking against reality).",
  "gloss": "Checking for self-contradiction",
  "signature": [
    "Check#1544(Context#510a)"
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
  "sema_ref": "InternalConsistency#862f",
  "sema_id": "sema:InternalConsistency#mh:SHA-256:862f24b8dcbc229acfc3d2ced93ceec3b6abf982a0de4cd63b4960c077c1c7e7",
  "sema_stub": "862f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "validate": "Validate#3de2",
      "check": "Check#1544"
    },
    "references": {
      "artifact": "Artifact#6254",
      "context": "Context#510a"
    }
  }
}
```

---

## InvariantFilter#a541

```json
{
  "handle": "InvariantFilter",
  "mechanism": "A strict communication firewall that intercepts {{message}}s (incoming or outgoing) and evaluates them against a set of explicit logical predicates (Invariants). If a {{message}} satisfies all invariants, it is permitted to pass. If it fails even one, it is blocked, dropped, or flagged for review. This enforces 'Contractual Safety' on the communication channel. It inspects every {{message}} via a rigorous {{check}} against defined predicates before allowing transit.",
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
      "name": "predicates",
      "type": "List[Expression]",
      "range": "unspecified",
      "description": "Boolean expressions that messages must satisfy to pass"
    },
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
  "sema_id": "sema:InvariantFilter#mh:SHA-256:a541049098acbba01ebe35ee9c23ebbdaf9d34e252b1b69f97daa87b3e96eea2",
  "sema_ref": "InvariantFilter#a541",
  "sema_stub": "a541",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#1544",
      "stream": "Stream#22f3"
    },
    "accepts": {
      "message": "Message#f767"
    }
  }
}
```

---

## LatticeCommit#3c5d

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
      "RootHashGossip#ba35"
    ],
    "ring": 0
  },
  "sema_id": "sema:LatticeCommit#mh:SHA-256:3c5d08275e421050d0fe9b753bd142328109463adbadc2beb50600bed0f2c9c0",
  "sema_ref": "LatticeCommit#3c5d",
  "sema_stub": "3c5d",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_transition": "StateTransition#3737",
      "topology": "Topology#2408",
      "check": "Check#1544",
      "quorum": "Quorum#29b4"
    }
  }
}
```

---

## LocalizedLearning#69bb

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:LocalizedLearning#mh:SHA-256:69bb2e9eea4ed50d3aa6213e7fc068cb247ec3d1737b707a9679bfba81c72f9b",
  "sema_ref": "LocalizedLearning#69bb",
  "sema_stub": "69bb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Act#5d55(FeedbackSignal#f904)"
  ],
  "dependencies": {
    "references": {
      "solver_manifest": "SolverManifest#67ac",
      "act": "Act#5d55"
    },
    "accepts": {
      "feedback_signal": "FeedbackSignal#f904"
    }
  }
}
```

---

## ManifestPlanning#8f61

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
  "sema_ref": "ManifestPlanning#8f61",
  "sema_id": "sema:ManifestPlanning#mh:SHA-256:8f617b10de4644e96e729f2da39560243e42755808fee6369f9330a5f9c7f66d",
  "sema_stub": "8f61",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2"
    },
    "yields": {
      "execution_manifest": "ExecutionManifest#a0d9"
    },
    "accepts": {
      "frame_spec": "FrameSpec#d5b8"
    },
    "composes_with": {
      "optimize": "Optimize#3075",
      "think": "Think#e1bd"
    }
  }
}
```

---

## MemeticSeed#491b

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
  "sema_id": "sema:MemeticSeed#mh:SHA-256:491b0bb4623d78df04ab196ef7809daa2fad14bccb130fcb9d2f0e8dffd485c3",
  "sema_ref": "MemeticSeed#491b",
  "sema_stub": "491b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "yield": "Yield#7eaf",
      "explain_beacon": "ExplainBeacon#6ced",
      "translation_proxy": "TranslationProxy#f0e0"
    }
  }
}
```

---

## MetaPrompt#b3f0

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:MetaPrompt#mh:SHA-256:b3f038ab7e58559adf1d5340646bced133512b997397a23c040bd9374c2ea169",
  "sema_ref": "MetaPrompt#b3f0",
  "sema_stub": "b3f0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Meta#90f4(Prompt#5ded)"
  ],
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "prompt": "Prompt#5ded",
      "task": "Task#d9f9",
      "prompt_chain": "PromptChain#d3f2"
    }
  }
}
```

---

## ModestClaim#f6e6

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
  "sema_id": "sema:ModestClaim#mh:SHA-256:f6e6d7b2e1f7025ac355d62791d22e9fa71af38e2d4e17e15994da6e4134f6bb",
  "sema_ref": "ModestClaim#f6e6",
  "sema_stub": "f6e6",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "reframe": "Reframe#ba00",
      "epistemic_calibrate": "EpistemicCalibrate#6069",
      "problem": "Problem#5baa"
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1,
    "related": [
      "Monitor#9a8f"
    ]
  },
  "sema_id": "sema:MonitorReport#mh:SHA-256:063cc5c1f90b2e11e3446ddfaec7034ed51acb83432fe11ba2d1e7151ac0d42d",
  "sema_ref": "MonitorReport#063c",
  "sema_stub": "063c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
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

## MonotonicCounter#f5a3

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
  "sema_id": "sema:MonotonicCounter#mh:SHA-256:f5a36a7775fe69757b2ab6fbf2dc66eab6689a1487b65005ae7ddef04dbd8235",
  "sema_ref": "MonotonicCounter#f5a3",
  "sema_stub": "f5a3",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#774b",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Nucleate#4ea1

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
  "sema_id": "sema:Nucleate#mh:SHA-256:4ea1bbb47979e47bc617c7b635ee2ce9d3315ac952012984aa62b18a479dc6f1",
  "sema_ref": "Nucleate#4ea1",
  "sema_stub": "4ea1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "rally": "Rally#8d04",
      "trace": "Trace#9057",
      "crystallize": "Crystallize#af68",
      "system": "System#e314"
    }
  }
}
```

---

## OntologyHandshake#ead0

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
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:OntologyHandshake#mh:SHA-256:ead055e44f108319ace229e30005ea5a3aaf8df540ccf1c1cf0f855aed45e613",
  "sema_ref": "OntologyHandshake#ead0",
  "sema_stub": "ead0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    },
    "references": {
      "protocol": "Protocol#7e1c",
      "spectral_tune": "SpectralTune#6c65"
    }
  }
}
```

---

## OptimisticSolver#dd2d

```json
{
  "handle": "OptimisticSolver",
  "mechanism": "A high-velocity implementation of {{cognitive_solver}} designed for efficient multi-agent coordination. Requires a {{parallel}} runtime (Actor Model with Mailboxes) to prevent serial deadlock. It explicitly couples the standard Solver lifecycle (Reason -> Solution) with the {{atomic_bid}} protocol. Unlike the base abstraction, this pattern MANDATES that the agent plan and execute in a single turn. It relies on {{reflexion}} and {{compensate}} for error correction rather than pre-action permission. Use {{compute_budget}} to bound resource consumption. Contrast with {{rigorous_solver}} which prioritizes safety over speed.",
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
    "ring": 1
  },
  "sema_ref": "OptimisticSolver#dd2d",
  "sema_id": "sema:OptimisticSolver#mh:SHA-256:dd2d3026c22804144e188878f9fbe94febf8dc702275e1d20bbeb6463b767555",
  "sema_stub": "dd2d",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "atomic_bid": "AtomicBid#0e6b",
      "compute_budget": "ComputeBudget#3b98",
      "reflexion": "Reflexion#51b9",
      "compensate": "Compensate#269d"
    },
    "references": {
      "rigorous_solver": "RigorousSolver#db93",
      "cognitive_solver": "CognitiveSolver#c6a7",
      "parallel": "Parallel#6272"
    }
  }
}
```

---

## Oracle#0dff

```json
{
  "handle": "Oracle",
  "mechanism": "A trusted entity that injects off-chain truth (Reality) into the system by cryptographically signing data. It resolves conditions in {{held_release}} and verifies outcomes for prediction markets.",
  "gloss": "Cryptographic truth source",
  "invariants": [
    "Non-Interference: The Oracle reports on reality but does not alter it.",
    "Consistency: Answers to the same query at the same time must be identical."
  ],
  "sema_id": "sema:Oracle#mh:SHA-256:0dffb25a0d877e3d718f2546a595eb574d5733d86ed71f1f37462955db421249",
  "sema_ref": "Oracle#0dff",
  "sema_stub": "0dff",
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
      "held_release": "HeldRelease#4956"
    }
  }
}
```

---

## OrchestrationLoop#6a79

```json
{
  "handle": "OrchestrationLoop",
  "mechanism": "A strict lifecycle for high-stakes problem solving implementing {{workflow}}. It enforces a sequence: 1. {{request_framing}} (Frame Problem \u2192 {{frame_spec}}), 2. {{manifest_planning}} (Architect Solution \u2192 {{execution_manifest}}), 3. {{rollout}} (Execute safely \u2192 {{rollout_manifest}}). Each transition is mediated by a typed artifact that must pass a non-compensatory {{accept_spec}}. The loop can iterate: failed rollouts trigger re-planning, failed plans trigger re-interpretation.",
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
      "LayeredCheck#3fad"
    ]
  },
  "sema_id": "sema:OrchestrationLoop#mh:SHA-256:6a794f5aa2ba4d154b98417cd28cd50c4f5522926ff385d99614cc5df615e308",
  "sema_ref": "OrchestrationLoop#6a79",
  "sema_stub": "6a79",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Workflow#9d3a(Rollout#28ac)"
  ],
  "dependencies": {
    "references": {
      "rollout_manifest": "RolloutManifest#9e7f",
      "execution_manifest": "ExecutionManifest#a0d9",
      "frame_spec": "FrameSpec#d5b8",
      "workflow": "Workflow#9d3a",
      "accept_spec": "AcceptSpec#70dd"
    },
    "composes_with": {
      "request_framing": "RequestFraming#0695",
      "manifest_planning": "ManifestPlanning#8f61",
      "rollout": "Rollout#28ac"
    }
  }
}
```

---

## OsmoticFilter#36b5

```json
{
  "handle": "OsmoticFilter",
  "mechanism": "Agents operate inside a semi-permeable membrane. Inbound messages are rejected unless they carry sufficient 'pressure' (stake, reputation, or relevance score) to overcome the membrane's current tension. The filter supports Multi-Solvent extraction, allowing different types of pressure (Money vs Trust) to be converted at defined rates. It uses {{hysteresis}} to prevent oscillation and {{canary}} messages to test permeability.",
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
      "name": "accepted_solvents",
      "type": "Map<Solvent, Rate> (Conversion rates, e.g., {Tokens:1.0, Reputation:5.0})",
      "range": "unspecified",
      "description": "Accepted payment types with conversion rates"
    },
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
    "ring": 0
  },
  "sema_id": "sema:OsmoticFilter#mh:SHA-256:36b5f762c178f196095cc38a5183326ac9183a3fe351b4b3e9dfeb44a2fac587",
  "sema_ref": "OsmoticFilter#36b5",
  "sema_stub": "36b5",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "hysteresis": "Hysteresis#78b0",
      "canary": "Canary#e78e"
    }
  }
}
```

---

## PatternEmergence#6b39

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
  "sema_id": "sema:PatternEmergence#mh:SHA-256:6b399c301d6fb02ef7579d3ec54425646d83b2cbdf99873bb10534dfaa459fd0",
  "sema_ref": "PatternEmergence#6b39",
  "sema_stub": "6b39",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "pattern_discovery": "PatternDiscovery#f667",
      "generalize": "Generalize#17c9",
      "uptake_as_ground": "UptakeAsGround#d5f3",
      "mint_when_friction": "MintWhenFriction#d48d",
      "noise": "Noise#c4b4"
    }
  }
}
```

---

## PatternSketch#f8fd

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
  "sema_id": "sema:PatternSketch#mh:SHA-256:f8fd94a51759adfbabbf38b704d132e010071b3aceb6b3e2378be9a0823336d2",
  "sema_ref": "PatternSketch#f8fd",
  "sema_stub": "f8fd",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "skeleton_of_thought": "SkeletonOfThought#d99a",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## PermissionEscalate#744f

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
    "ring": 1
  },
  "sema_id": "sema:PermissionEscalate#mh:SHA-256:744f4ce8439e69d9869b0fd5c260284e5f655861a97140d1487937165dc3deaa",
  "sema_ref": "PermissionEscalate#744f",
  "sema_stub": "744f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "tiered_access": "TieredAccess#2a28",
      "human_approve": "HumanApprove#e64a"
    }
  }
}
```

---

## PhasedRefinement#4a90

```json
{
  "handle": "PhasedRefinement",
  "mechanism": "A structured {{refine}} strategy that improves an {{artifact}} through a defined {{sequence}} of passes, where each pass targets a specific layer of abstraction (e.g., {{reason}} (logic) -> {{structural_coaching}} (structure) -> {{aesthetics}} (polish)). It uses a {{gate}} to prevent premature optimization by ensuring deep structural issues are resolved before surface-level polishing begins.",
  "gloss": "Layered, multi-pass improvement",
  "signature": [
    "Refine#38d9(Artifact#6254)"
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
  "sema_ref": "PhasedRefinement#4a90",
  "sema_id": "sema:PhasedRefinement#mh:SHA-256:4a907b2f7eef78e6ec51ce04c266cade4b5cbaf17c75085c5f7809a64b99b8ab",
  "sema_stub": "4a90",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "reason": "Reason#3f24",
      "aesthetics": "Aesthetics#0be2",
      "artifact": "Artifact#6254",
      "structural_coaching": "StructuralCoaching#3da9"
    },
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "gate": "Gate#206d",
      "refine": "Refine#38d9"
    }
  }
}
```

---

## PromiseGraph#b71f

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
    "ring": 0
  },
  "sema_id": "sema:PromiseGraph#mh:SHA-256:b71f80814ed80753cff7a03dc7b0969e1afafb207e0eef5edd5dcd74c1eb93ec",
  "sema_ref": "PromiseGraph#b71f",
  "sema_stub": "b71f",
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
      "agent": "Agent#aaec",
      "negative_proof": "NegativeProof#5225",
      "spot_audit": "SpotAudit#6673"
    }
  }
}
```

---

## PromptChain#d3f2

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
      "range": "{Strict, Retry#d53d, Skip}",
      "description": "Behavior on failure"
    },
    {
      "name": "max_retries_per_step",
      "type": "Integer",
      "range": "[0, 3]",
      "description": "Maximum retry attempts per step before chain fails"
    },
    {
      "name": "steps",
      "type": "List[StepDefinition]",
      "range": "unspecified",
      "description": "Ordered list of prompts"
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
  "sema_id": "sema:PromptChain#mh:SHA-256:d3f2a3af02ff10293ff5cb2e58937c5bf0cca881e0da83665bedf0b48195a479",
  "sema_ref": "PromptChain#d3f2",
  "sema_stub": "d3f2",
  "dependencies": {
    "references": {
      "gate": "Gate#206d",
      "input_guard": "InputGuard#0770",
      "tool_invoke": "ToolInvoke#cf0a",
      "chain": "Chain#5711",
      "retry": "Retry#d53d",
      "sequence": "Sequence#b0b8",
      "accept_spec": "AcceptSpec#70dd"
    },
    "accepts": {
      "task": "Task#d9f9"
    }
  }
}
```

---

## PropheticQuorum#9126

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
      "type": "Boolean",
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
      "Quorum#29b4",
      "SimulationTrace#096e",
      "RegimeSense#3e24"
    ],
    "ring": 1
  },
  "sema_id": "sema:PropheticQuorum#mh:SHA-256:9126777c70c38b2b46da1e5b3c2dfe3e1f1550a7040e3613b06594abadc1ee56",
  "sema_ref": "PropheticQuorum#9126",
  "sema_stub": "9126",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "normative_judge": "NormativeJudge#2316",
      "simulation": "Simulation#8035",
      "simulation_trace": "SimulationTrace#096e",
      "value": "Value#3c5d",
      "state": "State#4d58",
      "vote": "Vote#30d0",
      "check": "Check#1544"
    }
  }
}
```

---

## Proprioception#2fbf

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
      "type": "Int",
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:Proprioception#mh:SHA-256:2fbfba79d07478050b86020f08cb42f18c93e896052dccba0311db0168b549a0",
  "sema_ref": "Proprioception#2fbf",
  "sema_stub": "2fbf",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "trace": "Trace#9057",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "somatic_marker": "SomaticMarker#84e4",
      "context": "Context#510a",
      "state": "State#4d58"
    }
  }
}
```

---

## ProtoPack#6597

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
    "ring": 0,
    "tier": 1,
    "related": [
      "Build#00f3"
    ]
  },
  "sema_id": "sema:ProtoPack#mh:SHA-256:6597fa92b7426d373e1d05d6a7fd1f8c1416c00c78dfab8e35e5a6264c1453d6",
  "sema_ref": "ProtoPack#6597",
  "sema_stub": "6597",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Artifact#6254(Prototype#ff18)"
  ],
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "prototype": "Prototype#ff18"
    }
  }
}
```

---

## QuorumPulse#2c18

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
    "ring": 0
  },
  "sema_id": "sema:QuorumPulse#mh:SHA-256:2c18907e5670bc0e5eff0a26fceee4ae5f5faac5fbb1b086ceb2dd17e015b13a",
  "sema_ref": "QuorumPulse#2c18",
  "sema_stub": "2c18",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "signal": "Signal#f39d",
      "quorum": "Quorum#29b4",
      "heartbeat": "Heartbeat#7f88"
    }
  }
}
```

---

## Realizable#cf00

```json
{
  "handle": "Realizable",
  "gloss": "Evaluates execution feasibility of a plan",
  "mechanism": "Acts as a {{judge}} to evaluate the {{value}} and feasibility of a {{plan}}. Classifies the execution path into three qualitative states: (1) Magical: Relies on undefined {{step}}s or unavailable physics. (2) Uncertain: The dependency chain is clear, but specific links are unverified. (3) Coherent: Every {{step}} maps to a known primitive or realizable sub-component.",
  "signature": [
    "Judge#d84f(Value#3c5d)"
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_ref": "Realizable#cf00",
  "sema_id": "sema:Realizable#mh:SHA-256:cf006ab5a950cea6c7a9130ea7330c57d0a6b440f37d57f598ed71d84a4f3039",
  "sema_stub": "cf00",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "plan": "Plan#64f2",
      "step": "Step#5f22",
      "judge": "Judge#d84f",
      "value": "Value#3c5d"
    }
  }
}
```

---

## RealizationProtocol#e05f

```json
{
  "handle": "RealizationProtocol",
  "derived_from": "sema:CreationProtocol#mh:SHA-256:d289d0a26fec0c23993fedbe5593f5da302696271a454c714a0e91abaecfd8e2",
  "mechanism": "A standardized {{solver_tree}} that orchestrates the lifecycle of a user_request executed by a {{cognitive_solver}}. It enforces a strict phase transition from Abstract to Concrete to ensure the result is {{realizable}}. 1. {{interpret}} converts request -> {{frame_spec}}. 2. {{manifest_planning}} converts spec -> {{execution_manifest}}. 3. {{rollout}} executes the manifest to produce the {{outcome}}.",
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
    "SolverTree#0f1d(Outcome#38e0)"
  ],
  "sema_ref": "RealizationProtocol#e05f",
  "sema_id": "sema:RealizationProtocol#mh:SHA-256:e05f215ae8cfcb8c1f9e5c3f9d56d0676be58fabfb8ea161ef5fedb645183f81",
  "sema_stub": "e05f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "execution_manifest": "ExecutionManifest#a0d9",
      "frame_spec": "FrameSpec#d5b8",
      "realizable": "Realizable#cf00",
      "solver_tree": "SolverTree#0f1d",
      "cognitive_solver": "CognitiveSolver#c6a7"
    },
    "yields": {
      "outcome": "Outcome#38e0"
    },
    "composes_with": {
      "interpret": "Interpret#c9ee",
      "manifest_planning": "ManifestPlanning#8f61",
      "rollout": "Rollout#28ac"
    }
  }
}
```

---

## RequestFraming#0695

```json
{
  "handle": "RequestFraming",
  "derived_from": "sema:Interpret",
  "gloss": "Clarify intent and constraints before planning",
  "mechanism": "The initial state of workflow orchestration. It performs the act of {{interpret}} by accepting a {{message}} and using {{think}} to {{understand}} the 'real ask' within the given {{context}} before committing resources. It clarifies constraints, success criteria, and hidden assumptions, producing a {{frame_spec}} artifact. It acts as a semantic firewall against vague or dangerous instructions.",
  "signature": [
    "Think#e1bd(FrameSpec#d5b8)"
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "related": [
      "Reframe#ba00",
      "Decompose#ac56"
    ]
  },
  "sema_ref": "RequestFraming#0695",
  "sema_id": "sema:RequestFraming#mh:SHA-256:06954d95bc467b00eb0c969004db3174bff5dfc5c05733df2036605c835b6a5e",
  "sema_stub": "0695",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "yields": {
      "frame_spec": "FrameSpec#d5b8"
    },
    "composes_with": {
      "understand": "Understand#96d4",
      "think": "Think#e1bd"
    },
    "accepts": {
      "message": "Message#f767"
    },
    "references": {
      "context": "Context#510a",
      "interpret": "Interpret#c9ee"
    }
  }
}
```

---

## Reversibility#049f

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
      "type": "Cost",
      "range": "unspecified",
      "description": "Maximum acceptable cost to reverse the action"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:Reversibility#mh:SHA-256:049f5fd98135ec288888fa61056f65a7e46067b06eaa5e7cee7a7bd3bfef2f74",
  "sema_ref": "Reversibility#049f",
  "sema_stub": "049f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## ReversibilityCheck#574b

```json
{
  "handle": "ReversibilityCheck",
  "mechanism": "A convenience wrapper for a {{check}} configured with the {{reversibility}} condition. Halts execution if the action is deemed irreversible (Type 1 decision) without proper authorization. It applies the {{check}} primitive to the {{reversibility}} condition, ensuring the {{world_reversible}} invariant holds, mandating {{human_approve}} if the action is irreversible.",
  "gloss": "Reversibility Audit (Alias for Check(Reversibility))",
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ReversibilityCheck#mh:SHA-256:574b1afaee6cd675d04e2b9e3484ddfba1490b19121c881832865d3d31a8a2ee",
  "sema_ref": "ReversibilityCheck#574b",
  "sema_stub": "574b",
  "signature": [
    "Check#1544(Reversibility#049f)"
  ],
  "dependencies": {
    "references": {
      "human_approve": "HumanApprove#e64a",
      "check": "Check#1544",
      "world_reversible": "WorldReversible#f664",
      "reversibility": "Reversibility#049f"
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

## Rollout#28ac

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
  "sema_id": "sema:Rollout#mh:SHA-256:28aca597fa9b0ed6225f5fb7f497a7827ad46c3e7e036eea2c5dc2f2efe1bbef",
  "sema_ref": "Rollout#28ac",
  "sema_stub": "28ac",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Act#5d55(ExecutionManifest#a0d9)"
  ],
  "dependencies": {
    "accepts": {
      "execution_manifest": "ExecutionManifest#a0d9"
    },
    "yields": {
      "rollout_manifest": "RolloutManifest#9e7f",
      "monitor_report": "MonitorReport#063c"
    },
    "references": {
      "spec": "Spec#436e",
      "system": "System#e314",
      "act": "Act#5d55",
      "build": "Build#00f3",
      "state": "State#4d58",
      "manifest_planning": "ManifestPlanning#8f61",
      "world_reversible": "WorldReversible#f664"
    },
    "composes_with": {
      "circuit_breaker": "CircuitBreaker#4162",
      "compensate": "Compensate#269d",
      "ejection_seat": "EjectionSeat#6ff7",
      "canary": "Canary#e78e"
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
      "Rollout#28ac"
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

## RolloutWatch#5b2d

```json
{
  "handle": "RolloutWatch",
  "derived_from": "sema:Monitor",
  "gloss": "Continuous verification of deployed state against manifest",
  "mechanism": "The final {{state}} of workflow orchestration. It implements {{monitor}} by using {{observe}} to track the deployed {{solution}}'s performance on the {{system}} against the 'Definition of Done' defined in the {{rollout_manifest}}. If reality deviates from the plan (e.g., error rate spikes), it routes evidence back upstream via a {{monitor_report}}. It closes the feedback {{loop}}.",
  "signature": [
    "Observe#8ebd(System#e314, RolloutManifest#9e7f)"
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
      "SpotAudit#6673",
      "DriftWatch#a20d",
      "Reflexion#51b9"
    ]
  },
  "sema_ref": "RolloutWatch#5b2d",
  "sema_id": "sema:RolloutWatch#mh:SHA-256:5b2db93248ae390eb136b9a06f21cc6f6c2a87fa676d015a2a8d0fa64c2c4dc1",
  "sema_stub": "5b2d",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "accepts": {
      "rollout_manifest": "RolloutManifest#9e7f"
    },
    "references": {
      "monitor": "Monitor#9a8f",
      "system": "System#e314",
      "state": "State#4d58",
      "solution": "Solution#7186"
    },
    "composes_with": {
      "loop": "Loop#fb2e",
      "observe": "Observe#8ebd"
    },
    "yields": {
      "monitor_report": "MonitorReport#063c"
    }
  }
}
```

---

## RootHashGossip#ba35

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
  "sema_id": "sema:RootHashGossip#mh:SHA-256:ba352d6a3f86388fa901a8b6934e087ec52ebb8ddb7bc8bafd3822381bfbf30a",
  "sema_ref": "RootHashGossip#ba35",
  "sema_stub": "ba35",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "loop": "Loop#fb2e"
    }
  }
}
```

---

## ShoutWhisper#35dd

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
      "Route#9698"
    ],
    "ring": 1
  },
  "sema_id": "sema:ShoutWhisper#mh:SHA-256:35ddf298feb20dc16aeaa1294566eddb2dda1928744d7d25e747ae9a697d0d78",
  "sema_ref": "ShoutWhisper#35dd",
  "sema_stub": "35dd",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#1544",
      "global": "Global#803d"
    }
  }
}
```

---

## SignalReflection#aac2

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
  "sema_id": "sema:SignalReflection#mh:SHA-256:aac2c4b3fbc861b911c232b754116f4a56085e25dfd61c7ff6bb193b359578d0",
  "sema_ref": "SignalReflection#aac2",
  "sema_stub": "aac2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "spectral_tune": "SpectralTune#6c65",
      "message": "Message#f767",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## SimulationTrace#096e

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:SimulationTrace#mh:SHA-256:096eee69576638b38a5595613c41f79ae093e1036bdb70cd852edf65c42eead3",
  "sema_ref": "SimulationTrace#096e",
  "sema_stub": "096e",
  "dependencies": {
    "references": {
      "simulation": "Simulation#8035",
      "mental_sim": "MentalSim#7212",
      "trace": "Trace#9057"
    }
  }
}
```

---

## SolverManifest#67ac

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
  "sema_id": "sema:SolverManifest#mh:SHA-256:67acaedb52d3ca227a4ed3a462cb2834aa3ccb8d85c3ea4eff7ed3bfb879620b",
  "sema_ref": "SolverManifest#67ac",
  "sema_stub": "67ac",
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
      "solver": "Solver#1c9b"
    }
  }
}
```

---

## SolverNode#3a4f

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
  "sema_ref": "SolverNode#3a4f",
  "sema_id": "sema:SolverNode#mh:SHA-256:3a4f44a94bb04d00335c1fef34c532732644e897c49a4702700f9064a98d0961",
  "sema_stub": "3a4f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "solver_manifest": "SolverManifest#67ac",
      "responsibility": "Responsibility#fe7e",
      "localized_learning": "LocalizedLearning#69bb",
      "problem_space": "ProblemSpace#78da",
      "budget": "Budget#a763",
      "solution": "Solution#7186"
    }
  }
}
```

---

## SomaticMarker#84e4

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
      "Proprioception#2fbf"
    ],
    "ring": 2
  },
  "sema_id": "sema:SomaticMarker#mh:SHA-256:84e40c489b6061eec580753f3fea907d8b401883679a3d54d274e23f742a1e62",
  "sema_ref": "SomaticMarker#84e4",
  "sema_stub": "84e4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "correlation": "Correlation#091f",
      "task": "Task#d9f9",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## SourceEvaluate#ceb1

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:SourceEvaluate#mh:SHA-256:ceb14e641fee7940e36ad6c28b096bcf8bf90b50bee79a243d2b8eba788f0ba7",
  "sema_ref": "SourceEvaluate#ceb1",
  "sema_stub": "ceb1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Judge#d84f(Agent#aaec)"
  ],
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "cite_back": "CiteBack#d09c",
      "judge": "Judge#d84f"
    }
  }
}
```

---

## SpectralTune#6c65

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
      "type": "List[String]",
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
      "OntologyHandshake#ead0"
    ]
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:SpectralTune#mh:SHA-256:6c65e21711b7203fcd84ed58755cd57239cda2e09a1e66ddf81e407edcd5eeb7",
  "sema_ref": "SpectralTune#6c65",
  "sema_stub": "6c65",
  "dependencies": {
    "accepts": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## StateSnapshot#9ffc

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "signature": [
    "State#4d58(Snapshot#0ae9)"
  ],
  "sema_id": "sema:StateSnapshot#mh:SHA-256:9ffc9d057109f26717249d3a4c46dfaa52a944d10a363034bca187b83305f39f",
  "sema_ref": "StateSnapshot#9ffc",
  "sema_stub": "9ffc",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "snapshot": "Snapshot#0ae9",
      "idempotent_write": "IdempotentWrite#6c55",
      "trace": "Trace#9057",
      "state": "State#4d58"
    }
  }
}
```

---

## StructuralCoaching#3da9

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
  "sema_id": "sema:StructuralCoaching#mh:SHA-256:3da94d81638b577c42981039f4399705519db8a102dd8e16b7b51cbd6695b0b4",
  "sema_ref": "StructuralCoaching#3da9",
  "sema_stub": "3da9",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "critique": "Critique#3e00",
      "creative": "Creative#5574",
      "invert": "Invert#d1b9",
      "feedback": "Feedback#9b5c"
    }
  }
}
```

---

## StyleSpec#ec7b

```json
{
  "handle": "StyleSpec",
  "mechanism": "A structured {{spec}} defining the required {{aesthetics}} and formatting rules. It serves as the reference standard for passes in a {{phased_refinement}} loop focused on polish. Unlike functional requirements, this spec targets the subjective and presentational layer.",
  "gloss": "Codified aesthetic standards",
  "signature": [
    "Spec#436e(Aesthetics#0be2)"
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
  "sema_ref": "StyleSpec#ec7b",
  "sema_id": "sema:StyleSpec#mh:SHA-256:ec7bae21530d0d22601723e69b9a9a5d0a0cbe26ad8814539a10c800bec37928",
  "sema_stub": "ec7b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "aesthetics": "Aesthetics#0be2",
      "phased_refinement": "PhasedRefinement#4a90",
      "spec": "Spec#436e"
    }
  }
}
```

---

## SynergisticMode#9d93

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
    "ring": 0
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
  "sema_id": "sema:SynergisticMode#mh:SHA-256:9d933f008d31c66d5672bb259d9763cfde2f3060f264dbadd505fca02444f705",
  "sema_ref": "SynergisticMode#9d93",
  "sema_stub": "9d93",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d",
      "system": "System#e314",
      "agent": "Agent#aaec",
      "ontology_handshake": "OntologyHandshake#ead0",
      "mode": "Mode#53e0",
      "compose": "Compose#1023",
      "accept_spec": "AcceptSpec#70dd"
    }
  }
}
```

---

## Taper#c588

```json
{
  "handle": "Taper",
  "gloss": "Progressive ambiguity collapse from noisy input to certain output. Examples: Sema Discovery, Hiring pipelines, Compiler passes.",
  "mechanism": "A multi-stage {{sequence}} process that accepts wide-aperture, high-entropy inputs and progressively filters them through {{gate}}s or {{tri_gate}}s of increasing strictness. Each stage: (1) Applies a stage-specific acceptance threshold, acting as a functional {{depth_governor}}; (2) Reduces the candidate set to {{compress}} the search space; (3) Increases certainty. Final stage outputs zero-entropy signal (deterministic, unambiguous). Failure modes are stage-appropriate: Early stages optimize for recall (don't lose valid signals), Late stages optimize for precision (don't pass garbage).",
  "signature": [
    "Sequence#b0b8(Gate#206d)"
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
  "sema_ref": "Taper#c588",
  "sema_id": "sema:Taper#mh:SHA-256:c58849efe92d44ef8e3b6b173326df1926ad87bbd467b919f64734e44f208607",
  "sema_stub": "c588",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "compress": "Compress#0967",
      "depth_governor": "DepthGovernor#05fe"
    },
    "composes_with": {
      "tri_gate": "TriGate#07fc",
      "sequence": "Sequence#b0b8",
      "gate": "Gate#206d"
    }
  }
}
```

---

## ThinSlice#debb

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:ThinSlice#mh:SHA-256:debb731893208ce6514504b1212e5d07cf60f1477f3c485b752a694822c3fb30",
  "sema_ref": "ThinSlice#debb",
  "sema_stub": "debb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "route": "Route#9698",
      "somatic_marker": "SomaticMarker#84e4",
      "extended_thinking": "ExtendedThinking#ca3c"
    }
  }
}
```

---

## ThreeLevelCollision#5db4

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
    "ring": 0
  },
  "sema_id": "sema:ThreeLevelCollision#mh:SHA-256:5db438e5f38882afa181ea527d06b673f64139f42390b9e795cf2ecc9efa29af",
  "sema_ref": "ThreeLevelCollision#5db4",
  "sema_stub": "5db4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "fail_closed": "FailClosed#ae79"
    }
  }
}
```

---

## TieredAccess#2a28

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
      "range": "{Linear#81af, Exponential, Step#5f22}",
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
  "sema_id": "sema:TieredAccess#mh:SHA-256:2a28f25bd2e1e991a4c9250d85a478f2b16bf57a9191dbb61c944a29b14559ff",
  "sema_ref": "TieredAccess#2a28",
  "sema_stub": "2a28",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#aaec",
      "identity": "Identity#626c"
    },
    "composes_with": {
      "bearer_token": "BearerToken#2fe9"
    }
  }
}
```

---

## TimeboxThink#2656

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:TimeboxThink#mh:SHA-256:265679a37dcae704c3e9e8c958f42f11751102e0685e55b1fe277c238bd9c05e",
  "sema_ref": "TimeboxThink#2656",
  "sema_stub": "2656",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "work": "Work#aaad",
      "constraint": "Constraint#87fe",
      "value": "Value#3c5d",
      "budget": "Budget#a763"
    }
  }
}
```

---

## ToolDiscovery#0ff1

```json
{
  "handle": "ToolDiscovery",
  "mechanism": "{{agent}} queries a {{discover}} for capabilities matching its current {{task}}. Registry returns a {{card}} listing available tools with typed input/output schemas. {{agent}} selects the best match, performs a {{compatibility_check}} to verify schema alignment, then invokes via {{tool_invoke}} and observes the typed {{result}}. If no match is found or {{compatibility_check}} fails, the agent must {{fail_closed}} rather than attempt a best-effort invocation. Follows the Model Context Protocol pattern of progressive discovery: orient via registry, explore via schema matching, verify via hash comparison.",
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
    "Discover#afa1(ToolInvoke#cf0a)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1,
    "related": [
      "AgentDiscover#d88a"
    ]
  },
  "sema_ref": "ToolDiscovery#0ff1",
  "sema_id": "sema:ToolDiscovery#mh:SHA-256:0ff16794954587c168bc694f00a723973be11ddfeb3a15c73770ab660bd439d8",
  "sema_stub": "0ff1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb",
      "tool_invoke": "ToolInvoke#cf0a",
      "fail_closed": "FailClosed#ae79"
    },
    "references": {
      "card": "Card#c9f0",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "discover": "Discover#afa1"
    },
    "yields": {
      "result": "Result#8ed9"
    }
  }
}
```

---

## TraceBelief#a4bb

```json
{
  "handle": "TraceBelief",
  "mechanism": "A chronological reasoning pattern that tracks the history of a belief. Prevents 'Silent Updating' by forcing the agent to cite the specific past belief node it is revising. Instantiates the {{trace}} primitive on a {{belief}} object. Utilizes {{trace}}, {{surprisal_update}}, {{belief}}, {{time_warp_log}}.",
  "gloss": "Belief Provenance (Macro for Trace(Belief))",
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Protocols",
    "ring": 2
  },
  "sema_id": "sema:TraceBelief#mh:SHA-256:a4bb1cd846d840689549faca393ed9831cf058541acb3f0781bbb46d7c36cfec",
  "sema_ref": "TraceBelief#a4bb",
  "sema_stub": "a4bb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Trace#9057(Belief#5ad9)"
  ],
  "dependencies": {
    "references": {
      "belief": "Belief#5ad9",
      "surprisal_update": "SurprisalUpdate#6ef1",
      "time_warp_log": "TimeWarpLog#d938",
      "trace": "Trace#9057"
    }
  }
}
```

---

## TranslationProxy#f0e0

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
  "sema_id": "sema:TranslationProxy#mh:SHA-256:f0e0d8b01e88f45c1d6791f41ed1686a96e40fc48f541c31568d48bb83ad988e",
  "sema_ref": "TranslationProxy#f0e0",
  "sema_stub": "f0e0",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Translate#e75d(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "translate": "Translate#e75d",
      "ontology_handshake": "OntologyHandshake#ead0",
      "message": "Message#f767",
      "protocol": "Protocol#7e1c",
      "compare": "Compare#4881"
    }
  }
}
```

---

## UniqueHandle#11e7

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
  "sema_id": "sema:UniqueHandle#mh:SHA-256:11e7542d2b43ec0879ae24f91eeeaaf6380cb0c9ec067056eb2d1e4932c0468e",
  "sema_ref": "UniqueHandle#11e7",
  "sema_stub": "11e7",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#774b",
      "break": "Break#1a63",
      "agent": "Agent#aaec"
    }
  }
}
```

---

## UptakeAsGround#d5f3

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
  "sema_id": "sema:UptakeAsGround#mh:SHA-256:d5f3a2b2643f030c2290341c45c40cf86a29c7981e0dfcf097435a3a70b72ead",
  "sema_ref": "UptakeAsGround#d5f3",
  "sema_stub": "d5f3",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#d9f9",
      "modest_claim": "ModestClaim#f6e6"
    }
  }
}
```

---

## UptakeOverTimestamp#9f0f

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
  "sema_id": "sema:UptakeOverTimestamp#mh:SHA-256:9f0fffcbeef00cd271526bb7a2849998c76e242ed74d36d0058b1849379c57ab",
  "sema_ref": "UptakeOverTimestamp#9f0f",
  "sema_stub": "9f0f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "uptake_as_ground": "UptakeAsGround#d5f3",
      "problem": "Problem#5baa"
    }
  }
}
```

---

## Warmup#28c4

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
      "range": "{Linear#81af, Exponential, Step#5f22}",
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:Warmup#mh:SHA-256:28c434be6a4de607158375965b76e4cb67d742481b6b6fb840326a7610703ceb",
  "sema_ref": "Warmup#28c4",
  "sema_stub": "28c4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "throttle": "Throttle#3b43",
      "greet": "Greet#7ad2",
      "system": "System#e314"
    }
  }
}
```

---

## WorkerMode#cd5e

```json
{
  "handle": "WorkerMode",
  "mechanism": "Execution {{state}} Machine. Upon invoking `solver_claim_task`, the {{agent}} performs an atomic {{identity}} {{switch}} via {{context_switch}} using the {{solver_manifest}}. The {{agent}} remains in this {{mode}} until the {{task}} is complete (emitting a {{solution}} or error to the {{solver_node}}), ensuring adherence to the assigned persona. A {{lock}} prevents concurrent task claims.",
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
    "ring": 0
  },
  "sema_id": "sema:WorkerMode#mh:SHA-256:cd5eaffa73c8d3efbc20526e60c7a871621f49d2ca129ca96768412960017555",
  "sema_ref": "WorkerMode#cd5e",
  "sema_stub": "cd5e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "solver_node": "SolverNode#3a4f",
      "agent": "Agent#aaec",
      "task": "Task#d9f9",
      "mode": "Mode#53e0",
      "context": "Context#510a",
      "state": "State#4d58",
      "lock": "Lock#051c",
      "context_switch": "ContextSwitch#42cd",
      "switch": "Switch#e7f9",
      "solution": "Solution#7186"
    },
    "accepts": {
      "solver_manifest": "SolverManifest#67ac"
    }
  }
}
```

---

## Workflow#9d3a

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
  "sema_id": "sema:Workflow#mh:SHA-256:9d3a0b0dc57429eec63a25350e712c1ee6f04220f7048e45805106de90550199",
  "sema_ref": "Workflow#9d3a",
  "sema_stub": "9d3a",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "solver": "Solver#1c9b",
      "role": "Role#fc9f",
      "step": "Step#5f22",
      "accept_spec": "AcceptSpec#70dd"
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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0
  },
  "sema_id": "sema:WorldReversible#mh:SHA-256:f6649f97dc12bc980722caa393140b9043af7dd470fdac4e1f40fa3f6a22dfbe",
  "sema_ref": "WorldReversible#f664",
  "sema_stub": "f664",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

