# Sema Vocabulary (Short Hand JSON)

**Total Patterns:** 452
**Format:** JSON with short-hand references.

---

# Layer: Infrastructure

## AcceptSpec#762e

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
    "layer": "Infrastructure",
    "category": "Data Structures",
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
  "sema_id": "sema:AcceptSpec#mh:SHA-256:762e284648ca2f4d9898526f902e00f31399e5586120720650a0a0dec0cd1a26",
  "sema_ref": "AcceptSpec#762e",
  "sema_stub": "762e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "spec": "Spec#68b4",
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## Aesthetics#c912

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
  "sema_id": "sema:Aesthetics#mh:SHA-256:c912f414b11624e629406b19c5b4472e40678839f6a613f7d9e1c26c6ca655ed",
  "sema_ref": "Aesthetics#c912",
  "sema_stub": "c912",
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
      "artifact": "Artifact#6254",
      "parsimony": "Parsimony#6d67",
      "metric": "Metric#17fd"
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
      "system": "System#e314",
      "state": "State#4d58"
    }
  }
}
```

---

## Ballot#1934

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
  "sema_ref": "Ballot#1934",
  "sema_id": "sema:Ballot#mh:SHA-256:1934bd52e662c4df304637cc1c05f78635643dcacf49b4b0fe37e84900446be9",
  "sema_stub": "1934",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "select": "Select#15c2",
      "monotonic_counter": "MonotonicCounter#c7ab"
    }
  }
}
```

---

## Belief#cafb

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
  "sema_id": "sema:Belief#mh:SHA-256:cafbdbf0b6df5e9daae96a0fd2e9985415eb6ee79fd65708b7a16ea7c3f76959",
  "sema_ref": "Belief#cafb",
  "sema_stub": "cafb",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "accepts": {
      "context": "Context#e88a"
    },
    "references": {
      "agent": "Agent#d183",
      "state": "State#4d58"
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

## Break#0bb3

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
      "EjectionSeat#b71c",
      "Retry#cb3a"
    ]
  },
  "sema_id": "sema:Break#mh:SHA-256:0bb3432f8b2bbd83c52323f16912e59d9f68248e42db0eb84916435f7680b9dd",
  "sema_ref": "Break#0bb3",
  "sema_stub": "0bb3",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "system": "System#e314",
      "message": "Message#f767",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Cache#08ed

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
  "sema_id": "sema:Cache#mh:SHA-256:08ede75502246829cb9313bd69e53d3f1560a7ac41890c5a3f1f5e37c942bf10",
  "sema_ref": "Cache#08ed",
  "sema_stub": "08ed",
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
    "description": "Keyed-value storage with lookup semantics.",
    "properties": {
      "key": {
        "type": "string",
        "description": "Lookup key"
      },
      "value": {
        "description": "Stored value"
      },
      "hit": {
        "type": "boolean",
        "description": "Whether the key was found on lookup"
      }
    }
  },
  "dependencies": {
    "references": {
      "datum": "Datum#31cf",
      "state": "State#4d58"
    }
  }
}
```

---

## Card#f63d

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
  "sema_id": "sema:Card#mh:SHA-256:f63d05a3e64ce7dd98121e23b559334726c6664a4d0579acd48f88871980d108",
  "sema_ref": "Card#f63d",
  "sema_stub": "f63d",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "latent_attachment": "LatentAttachment#640e",
      "agent": "Agent#d183",
      "probe": "Probe#12d8"
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

## ConceptAnchor#828b

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
    "Immutability: The definition pointed to by the Anchor Hash cannot change.",
    "Resolution: The Anchor must resolve to a valid schema or content."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:ConceptAnchor#mh:SHA-256:828bd82b36e985b1cd6b115ad27c44c7f5b34d463fa8bbebb101968f9226a46f",
  "sema_ref": "ConceptAnchor#828b",
  "sema_stub": "828b"
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

## Context#e88a

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
    "Agent has a valid environment to execute."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Data Structures",
    "related": [
      "ContextCompress#4845",
      "ContextSwitch#3a3c",
      "AnchorDrop#ad75"
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
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Context#mh:SHA-256:e88aa7f08b065746d26535db4cb40965ee62226f9dfbbd92fb091ae0ba8d8c03",
  "sema_ref": "Context#e88a",
  "sema_stub": "e88a",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Contract#087b

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
  "sema_id": "sema:Contract#mh:SHA-256:087b5926e0c8293891ca4768de891de29d921ba95dfdb162a538886ce46d809f",
  "sema_ref": "Contract#087b",
  "sema_stub": "087b",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "sign": "Sign#d60d",
      "commitment_device": "CommitmentDevice#3aeb",
      "context": "Context#e88a",
      "judge": "Judge#b8d6",
      "identity": "Identity#626c"
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
      "causation": "Causation#d360",
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

## Cyclic#e187

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
  "sema_ref": "Cyclic#e187",
  "sema_id": "sema:Cyclic#mh:SHA-256:e187ac5a01c82a2e06556ae52dcf5c2715ef317f9a1850e0e7b4322a2c1a6c3c",
  "sema_stub": "e187",
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
      "topology": "Topology#2408",
      "loop": "Loop#a316"
    }
  }
}
```

---

## DAG#b3f5

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
  "sema_id": "sema:DAG#mh:SHA-256:b3f5e8128c54a9b4e1a0de8b407ed313d8a8a1e32165687af9862e3566fef7d3",
  "sema_ref": "DAG#b3f5",
  "sema_stub": "b3f5",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "parallelize": "Parallelize#b943"
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

## Decision#934e

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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:Decision#mh:SHA-256:934e336cd9323a59a2af8f1248d0a4122183efe479c561162289f23d4226944c",
  "sema_ref": "Decision#934e",
  "sema_stub": "934e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "A committed choice \u2014 artifact recording which option was selected.",
    "required": [
      "option",
      "committed_at"
    ],
    "properties": {
      "option": {
        "type": "string"
      },
      "committed_at": {
        "type": "string",
        "format": "date-time"
      },
      "rationale": {
        "type": "string"
      },
      "reviewer": {
        "type": "string"
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

## Exception#53bb

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
  "sema_id": "sema:Exception#mh:SHA-256:53bbe52ae45a1898ae6acf9099e12ce01f2a7fd34dea4e964cb45b0f0a7dc52a",
  "sema_ref": "Exception#53bb",
  "sema_stub": "53bb",
  "dependencies": {
    "references": {
      "fail_closed": "FailClosed#59d8",
      "circuit_breaker": "CircuitBreaker#0577",
      "state": "State#4d58"
    }
  }
}
```

---

## ExecutionManifest#6cf5

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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1,
    "related": [
      "Plan#31a7",
      "Build#8143",
      "Rollout#5475"
    ]
  },
  "sema_id": "sema:ExecutionManifest#mh:SHA-256:6cf5e67e580558a7f0704a5046ac45ebb766d2498be800d070d331a756a57502",
  "sema_ref": "ExecutionManifest#6cf5",
  "sema_stub": "6cf5",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "Binds design with operation sequence.",
    "required": [
      "target_design",
      "operation_sequence"
    ],
    "properties": {
      "target_design": {
        "type": "object"
      },
      "operation_sequence": {
        "type": "array"
      },
      "constraints": {
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

## FailureTrace#b1f0

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
  "sema_id": "sema:FailureTrace#mh:SHA-256:b1f03ef9518526636f228deaa449d1ee9c345714c10d12721f111fe2ccd0c4c2",
  "sema_ref": "FailureTrace#b1f0",
  "sema_stub": "b1f0",
  "dependencies": {
    "references": {
      "accept_spec": "AcceptSpec#762e"
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

## FrameSpec#edff

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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1
  },
  "data_schema": {
    "type": "object",
    "description": "Structured problem definition.",
    "required": [
      "problem_statement",
      "constraints"
    ],
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
      },
      "hidden_assumptions": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "signature": [
    "Artifact#6254(Constraint#87fe)"
  ],
  "sema_id": "sema:FrameSpec#mh:SHA-256:edffd10df1ca5722b9d7f92a4efbe1a45e5ef172289ff6744a135978b1718ad2",
  "sema_ref": "FrameSpec#edff",
  "sema_stub": "edff",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "artifact": "Artifact#6254",
      "problem": "Problem#64d0",
      "spec": "Spec#68b4"
    }
  }
}
```

---

## Goal#5f27

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
  "sema_id": "sema:Goal#mh:SHA-256:5f2705b0bb55d1543c9e2cea970a4add42f227ee67b57ffaa3e11233a98f0127",
  "sema_ref": "Goal#5f27",
  "sema_stub": "5f27",
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
      "work": "Work#bc56",
      "result": "Result#f29e"
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

## Ledger#6fc4

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
  "sema_id": "sema:Ledger#mh:SHA-256:6fc40493b9af3dd60fe8b329339359a411fb14c117e71e6dbbef78543a48f59c",
  "sema_ref": "Ledger#6fc4",
  "sema_stub": "6fc4",
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
      "agent": "Agent#d183",
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
      "Decompose#5471"
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

## MechanisticDesignProposal#c3ed

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
  "sema_ref": "MechanisticDesignProposal#c3ed",
  "sema_id": "sema:MechanisticDesignProposal#mh:SHA-256:c3ed15925af85be4141a1c93824187b38e765fba5622b9683159341a8ad72d8f",
  "sema_stub": "c3ed",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "risk": "Risk#1980"
    },
    "accepts": {
      "system": "System#e314",
      "problem": "Problem#64d0"
    },
    "yields": {
      "solution": "Solution#445c"
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
      "system": "System#e314",
      "state": "State#4d58"
    }
  }
}
```

---

## Mode#3df1

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
      "WorkerMode#3d61",
      "SynergisticMode#fa9f"
    ]
  },
  "sema_id": "sema:Mode#mh:SHA-256:3df185d5794eb12f71d2606b7b16e309f58f75b52264e94de1448fec11d7a12e",
  "sema_ref": "Mode#3df1",
  "sema_stub": "3df1",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "agent": "Agent#d183",
      "state": "State#4d58"
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

## Outcome#9bf0

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
  "sema_id": "sema:Outcome#mh:SHA-256:9bf0d5ecb1486ba1f14eac8c1bb50be650d6fcb725c8cb0a3087b137e1428e6b",
  "sema_ref": "Outcome#9bf0",
  "sema_stub": "9bf0",
  "dependencies": {
    "references": {
      "plan": "Plan#31a7"
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

## PerformanceSignal#d211

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
  "sema_id": "sema:PerformanceSignal#mh:SHA-256:d211b4c6b870013d8b5cc8ae3066caf738409799932557309e8b3aa741890417",
  "sema_ref": "PerformanceSignal#d211",
  "sema_stub": "d211",
  "dependencies": {
    "references": {
      "feedback": "Feedback#dc36",
      "frame_error": "FrameError#edf5",
      "pathway_memory": "PathwayMemory#7899"
    }
  }
}
```

---

## Permission#d981

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
  "sema_ref": "Permission#d981",
  "sema_id": "sema:Permission#mh:SHA-256:d981e3410909de3ac0c4fa4b8203ad1db8b024de78fb4f3f2b64a645fe98c198",
  "sema_stub": "d981",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "agent": "Agent#d183",
      "act": "Act#dc2d"
    }
  }
}
```

---

## Plan#31a7

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
  "sema_ref": "Plan#31a7",
  "sema_id": "sema:Plan#mh:SHA-256:31a7c18c6584ec1f0966abe53dfcfc0e6c759573a8ba1d768ddb9a45dc2ae23b",
  "sema_stub": "31a7",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "step": "Step#5f22",
      "goal": "Goal#5f27",
      "system": "System#e314",
      "risk": "Risk#1980",
      "state": "State#4d58",
      "artifact": "Artifact#6254",
      "sequence": "Sequence#b0b8"
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

## Problem#64d0

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
  "sema_id": "sema:Problem#mh:SHA-256:64d0f0f9577f850e62e350817995bed218d466d655cc641b9e4f5e689d7fd4f3",
  "sema_ref": "Problem#64d0",
  "sema_stub": "64d0",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "state": "State#4d58"
    }
  }
}
```

---

## ProblemSpace#6e74

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
  "sema_ref": "ProblemSpace#6e74",
  "sema_id": "sema:ProblemSpace#mh:SHA-256:6e7467a68a2f24707fb81f125020b1d64a88d693e26610d801b03ad9296dee33",
  "sema_stub": "6e74",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solution": "Solution#445c",
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

## Proposal#ab24

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
  "sema_ref": "Proposal#ab24",
  "sema_id": "sema:Proposal#mh:SHA-256:ab244c2a0c2715df0b7c48b200d94c62c207ff9f7510f7df4d45b6d5a698eae0",
  "sema_stub": "ab24",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "transition": "Transition#072d",
      "act": "Act#dc2d"
    },
    "composes_with": {
      "message": "Message#f767"
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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2,
    "tier": 1,
    "related": [
      "Build#8143"
    ]
  },
  "sema_id": "sema:ProtoPack#mh:SHA-256:1cd18184514b33a7c7e32cad76c496885c5be7e8b63e3e46ba75d24d8bea57b8",
  "sema_ref": "ProtoPack#1cd1",
  "sema_stub": "1cd1",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "prototype": "Prototype#ff18",
      "artifact": "Artifact#6254"
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

## Queue#7ca9

```json
{
  "handle": "Queue",
  "mechanism": "A linear container holding {{task}}s or {{message}}s under an explicit ordering discipline (FIFO, LIFO, or Priority). Consumers dequeue one element at a time; producers enqueue at the discipline-dictated position. Distinct from a {{stream}} (continuous, unbounded, with no single consumer) and from a plain list (no consumer semantics).",
  "gloss": "Ordered container with FIFO/LIFO/priority discipline and explicit dequeue semantics",
  "sema_id": "sema:Queue#mh:SHA-256:7ca9c0e018ff83fb95ed910137e844544899adb371390af2da9402026c03d3e3",
  "sema_ref": "Queue#7ca9",
  "sema_stub": "7ca9",
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
      "stream": "Stream#22f3",
      "task": "Task#b290"
    }
  }
}
```

---

## Resource#553a

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
  "sema_ref": "Resource#553a",
  "sema_id": "sema:Resource#mh:SHA-256:553ab0cf44d99e80943d4190f2520897bdc3b2581fdf4c57582e61930943076b",
  "sema_stub": "553a",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "budget": "Budget#0934"
    }
  }
}
```

---

## Result#f29e

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
  "sema_id": "sema:Result#mh:SHA-256:f29e7289b78b2ec608db42892fad4c1db47c5ad215231685ad4786935baa8da2",
  "sema_ref": "Result#f29e",
  "sema_stub": "f29e",
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
          "Budget#0934",
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
      "solution": "Solution#445c",
      "metric": "Metric#17fd"
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
      "metric": "Metric#17fd",
      "probability": "Probability#356b"
    }
  }
}
```

---

## RolloutManifest#5596

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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0,
    "tier": 1,
    "related": [
      "Rollout#5475"
    ]
  },
  "sema_id": "sema:RolloutManifest#mh:SHA-256:55968fc104d6ae67466bddb0eda77cb62b3a9e0e98311f9d308bdd86a3b8f035",
  "sema_ref": "RolloutManifest#5596",
  "sema_stub": "5596",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "Immutable deployment record.",
    "required": [
      "deployment_id",
      "actions"
    ],
    "properties": {
      "deployment_id": {
        "type": "string"
      },
      "actions": {
        "type": "array"
      },
      "feature_flag_state": {
        "type": "object"
      },
      "targets": {
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

## RuleSet#ac40

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
  "sema_ref": "RuleSet#ac40",
  "sema_id": "sema:RuleSet#mh:SHA-256:ac408521af277bb770e0ccbadaeebf2dd2630036f0adf8c3a2873836d95a799a",
  "sema_stub": "ac40",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "constitution": "Constitution#d2e5",
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
      "StateSnapshot#5a11"
    ]
  },
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
  "sema_id": "sema:Snapshot#mh:SHA-256:0ae992361f9dfef49e88efa9a985826833260038fb99978615f5df709eba04f1",
  "sema_ref": "Snapshot#0ae9",
  "sema_stub": "0ae9",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "state": "State#4d58"
    }
  }
}
```

---

## Solution#445c

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
  "sema_id": "sema:Solution#mh:SHA-256:445c7e7ec6df43cc59d06ea718632979b7fb9045f4157a6ef74dfc611e4ff51d",
  "sema_ref": "Solution#445c",
  "sema_stub": "445c",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "chain": "Chain#711e",
      "tree": "Tree#a5a3",
      "artifact": "Artifact#6254",
      "work": "Work#bc56"
    },
    "accepts": {
      "task": "Task#b290"
    }
  }
}
```

---

## SolverManifest#11ea

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
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 0
  },
  "sema_id": "sema:SolverManifest#mh:SHA-256:11ea36aad4d25c3997cfb46d5d84a2522c3de92484202850091c598871fdd727",
  "sema_ref": "SolverManifest#11ea",
  "sema_stub": "11ea",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "data_schema": {
    "type": "object",
    "description": "Typed solver identity + capabilities.",
    "required": [
      "solver_id",
      "capabilities"
    ],
    "properties": {
      "solver_id": {
        "type": "string"
      },
      "capabilities": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "input_types": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "output_types": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "solver": "Solver#4ed4"
    }
  }
}
```

---

## Spec#68b4

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
  "sema_ref": "Spec#68b4",
  "sema_id": "sema:Spec#mh:SHA-256:68b4a7de6903d953979547572fc95ddc63da8ba24b7e39b06e22d84daacefa1c",
  "sema_stub": "68b4",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "goal": "Goal#5f27",
      "plan": "Plan#31a7",
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
      "Plan#31a7"
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

## StyleSpec#754e

```json
{
  "handle": "StyleSpec",
  "mechanism": "A structured {{spec}} defining the required {{aesthetics}} and formatting rules. It serves as the reference standard for passes in a {{phased_refinement}} loop focused on polish. Unlike functional requirements, this spec targets the subjective and presentational layer.",
  "gloss": "Codified aesthetic standards",
  "signature": [
    "Spec#68b4(Aesthetics#c912)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Data Structures",
    "ring": 2,
    "tier": 2
  },
  "data_schema": {
    "type": "object",
    "description": "Codified aesthetic and formatting standards.",
    "required": [
      "style_id"
    ],
    "properties": {
      "style_id": {
        "type": "string"
      },
      "rules": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "examples": {
        "type": "array"
      }
    }
  },
  "sema_ref": "StyleSpec#754e",
  "sema_id": "sema:StyleSpec#mh:SHA-256:754ed76d78d392f5ccba298808a23c6c505f83cbaed3ec6f9dc04b13f860437b",
  "sema_stub": "754e",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "spec": "Spec#68b4",
      "aesthetics": "Aesthetics#c912",
      "phased_refinement": "PhasedRefinement#11af"
    }
  }
}
```

---

## Subject#9a60

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
  "sema_ref": "Subject#9a60",
  "sema_id": "sema:Subject#mh:SHA-256:9a606630bd3637a57b39b520bc1641963eb6a362c9c3637d215ba7deeea6f666",
  "sema_stub": "9a60",
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "dependencies": {
    "references": {
      "act": "Act#dc2d"
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

## Task#b290

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
  "sema_id": "sema:Task#mh:SHA-256:b290c7f79fd936d3a3035c5b35658f94b85b6e1b749b1916576a1cf587d8e8c5",
  "sema_ref": "Task#b290",
  "sema_stub": "b290",
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
      "context": "Context#e88a",
      "constraint": "Constraint#87fe",
      "hierarchy": "Hierarchy#d530",
      "system": "System#e314"
    }
  }
}
```

---

## Tension#92e3

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
  "sema_id": "sema:Tension#mh:SHA-256:92e31e8f2daa129400d7270a856f016095f9c5879a7a21d93cfe8322b3277d01",
  "sema_ref": "Tension#92e3",
  "sema_stub": "92e3",
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
      "yield": "Yield#0de8",
      "dialectic": "Dialectic#2e3c"
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
          "DAG#b3f5",
          "Cyclic#e187",
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
      "system": "System#e314",
      "state": "State#4d58"
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
      "LatentAttachment#640e"
    ]
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Vector#mh:SHA-256:c7c4d97d3416646673aa3d70d27aa4da40c7c2ae86180c92901a0e23429ffedc",
  "sema_ref": "Vector#c7c4",
  "sema_stub": "c7c4"
}
```

---

## Work#bc56

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
      "EntropyPump#ed3b"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Data Structures",
  "sema_id": "sema:Work#mh:SHA-256:bc56cced064291f9c994564930993c5f601a4311d33aeeb0e32511ea154e82a3",
  "sema_ref": "Work#bc56",
  "sema_stub": "bc56",
  "dependencies": {
    "references": {
      "budget": "Budget#0934",
      "act": "Act#dc2d"
    },
    "composes_with": {
      "task": "Task#b290"
    }
  }
}
```

---

## Act#dc2d

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
      "ToolInvoke#bd2b",
      "ReAct#05f2",
      "AgentSandbox#1838"
    ],
    "ring": 0
  },
  "sema_id": "sema:Act#mh:SHA-256:dc2d664fa788a0cd307e733dd233853f5f3c6095fe8e86a29b29d966c1a7b200",
  "sema_ref": "Act#dc2d",
  "sema_stub": "dc2d",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "select": "Select#15c2"
    }
  }
}
```

---

## Actor#57f6

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
  "sema_ref": "Actor#57f6",
  "sema_id": "sema:Actor#mh:SHA-256:57f6b9dbc9b8fc596a5238327f29fc24e27d4e0228bfed7352d41f0bfacd4ea4",
  "sema_stub": "57f6",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "act": "Act#dc2d"
    },
    "references": {
      "nature": "Nature#6c1a",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Aggregate#8c2a

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
      "range": "{Mean, Median, Mode#3df1, Sum, Min, Max, Variance, StdDev}",
      "description": "Default: Mean"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Aggregate#mh:SHA-256:8c2ae987064dabf80b6ff9a6a2bcca7ae223ae9b6b2f6f3642fa754b004f45b5",
  "sema_ref": "Aggregate#8c2a",
  "sema_stub": "8c2a",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "mode": "Mode#3df1"
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

## Backoff#c6d1

```json
{
  "handle": "Backoff",
  "mechanism": "Exponential Delay: On failure, wait delay D before retry. On repeated failure, D *= multiplier (typically 2). Add jitter to prevent thundering herd. Cap at maximum delay. Reset on success.",
  "gloss": "Exponential delay to reduce contention",
  "failure_modes": [
    "Starvation: Unlucky agents keep backing off while others succeed, never getting a slot."
  ],
  "invariants": [
    "Retry budget must be finite (max_attempts set before first attempt)."
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
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Backoff#mh:SHA-256:c6d1d5ba3a4d0347d9191a13c52d9eb43b7b3a19ed611fbb17a0e4dd49249482",
  "sema_ref": "Backoff#c6d1",
  "sema_stub": "c6d1"
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Branch#mh:SHA-256:329d01a4bcf9599389d35db860faee9fb6d42964ceca8fd708843b410fa7150e",
  "sema_ref": "Branch#329d",
  "sema_stub": "329d",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Budget#0934

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
    "{{conservation}}: Allocated + Remaining = Total."
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
  "sema_ref": "Budget#0934",
  "sema_id": "sema:Budget#mh:SHA-256:09342288ae2b22b04b2e8eed72b5871e0cd1ad096cc795a5cbfbe7923f038431",
  "sema_stub": "0934",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "conservation": "Conservation#d63a"
    }
  }
}
```

---

## Care#b01c

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
  "sema_id": "sema:Care#mh:SHA-256:b01cd396a009eed74ea4e11f288b8e686c02ba85411f1d14038076e66bbd3ee6",
  "sema_ref": "Care#b01c",
  "sema_stub": "b01c",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "work": "Work#bc56",
      "entropy": "Entropy#a265"
    }
  }
}
```

---

## Check#410e

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
      "Validate#aebf",
      "Judge#b8d6"
    ]
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Check#mh:SHA-256:410e2942d6d61487cc7e0ee04291a96ba2e37771f24928577f63b21f376de4a9",
  "sema_ref": "Check#410e",
  "sema_stub": "410e",
  "dependencies": {
    "yields": {
      "status": "Status#1cf9"
    },
    "references": {
      "gate": "Gate#02f6",
      "condition": "Condition#cbd5"
    }
  }
}
```

---

## CircuitBreaker#0577

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
  "sema_ref": "CircuitBreaker#0577",
  "sema_id": "sema:CircuitBreaker#mh:SHA-256:05770c1edb2895638cabde8b997d396f531a73f6f37cb7af97b35e9c98116912",
  "sema_stub": "0577",
  "dependencies": {
    "references": {
      "backoff": "Backoff#c6d1",
      "state": "State#4d58"
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Compare#mh:SHA-256:48815374a8845487f135578867a9a36ffeeb0e786007b63da5713292723e2109",
  "sema_ref": "Compare#4881",
  "sema_stub": "4881",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Compensate#985e

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "related": [
      "Retry#cb3a"
    ],
    "caution": "Compensation must not erase the audit trail of what was rolled back \u2014 log both the forward action and the compensation."
  },
  "sema_id": "sema:Compensate#mh:SHA-256:985ef5c13b644c687417409aef081d29994ef64a7a5cf8961e8fbd4e115a7b29",
  "sema_ref": "Compensate#985e",
  "sema_stub": "985e",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "time_warp_log": "TimeWarpLog#8751",
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Compress#mh:SHA-256:0967b06ee8a76319b59ee923f2302ff5aebac89f396d79b55f2a0f9e1239f621",
  "sema_ref": "Compress#0967",
  "sema_stub": "0967",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives"
}
```

---

## Cooldown#6eb2

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Cooldown#mh:SHA-256:6eb28c0493afc961191d1b5585d358ee6df332758229c56f75829c0e6b777b52",
  "sema_ref": "Cooldown#6eb2",
  "sema_stub": "6eb2",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "throttle": "Throttle#4d47"
    }
  }
}
```

---

## EntropyPump#ed3b

```json
{
  "handle": "EntropyPump",
  "mechanism": "A mechanism that prevents system stagnation by injecting {{entropy}} (randomness/noise) into decision-making processes. It acts as a counterbalance to convergence, ensuring that the system explores the solution space rather than getting stuck in local optima. By adding {{noise}}, it forces re-evaluation of settled states.",
  "gloss": "Controlled randomization to escape convergence deadlocks",
  "failure_modes": [
    "Over-injection destabilizing productive {{equilibrium}}.",
    "Insufficient injection failing to break persistent deadlocks."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1
  },
  "sema_id": "sema:EntropyPump#mh:SHA-256:ed3b97a2f0de4b0c3dac225aa578e266e9fce41cbb7c92d670d29a7366313818",
  "sema_ref": "EntropyPump#ed3b",
  "sema_stub": "ed3b",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "equilibrium": "Equilibrium#f7c5",
      "entropy": "Entropy#a265",
      "noise": "Noise#3d9a"
    }
  }
}
```

---

## FailClosed#59d8

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
      "range": "{Reject, Retry#cb3a, Fallback}",
      "description": "Default: Reject"
    }
  ],
  "_meta": {
    "tier": 1,
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:FailClosed#mh:SHA-256:59d855305c8f8ac7493b0e6e5c078d9cf7a7a9d2e181b8fefd88f7151f4fb9b8",
  "sema_ref": "FailClosed#59d8",
  "sema_stub": "59d8",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "output_guard": "OutputGuard#1c09",
      "system": "System#e314",
      "circuit_breaker": "CircuitBreaker#0577"
    }
  }
}
```

---

## Feedback#dc36

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
  "sema_id": "sema:Feedback#mh:SHA-256:dc367877c9161b9d4ba77075cfe19157680bb190f8834f81c925a4a035d2fe43",
  "sema_ref": "Feedback#dc36",
  "sema_stub": "dc36",
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
      "incongruity": "Incongruity#e98f",
      "result": "Result#f29e",
      "metric": "Metric#17fd"
    }
  }
}
```

---

## FeedbackSignal#afac

```json
{
  "handle": "FeedbackSignal",
  "mechanism": "A structured packet containing the evaluation of a specific {{solution}} for a {{task}}. Carries outcome and details to the {{feedback}} mechanism.",
  "gloss": "Standardized learning feedback packet",
  "invariants": [
    "Targeted: each signal cites the specific {{solution}} and {{task}} it evaluates.",
    "Structured: payload conforms to the defined data_schema (solution_ref, task_ref, outcome \u2208 {success, failure, partial})."
  ],
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
  "sema_id": "sema:FeedbackSignal#mh:SHA-256:afacbe954e69fc922c467f83dc1624d9b2e8e5651a1923554aed161443e59108",
  "sema_ref": "FeedbackSignal#afac",
  "sema_stub": "afac",
  "dependencies": {
    "references": {
      "feedback": "Feedback#dc36",
      "task": "Task#b290",
      "solution": "Solution#445c"
    }
  }
}
```

---

## Gate#02f6

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Gate#mh:SHA-256:02f682e5f7ba995d66c0a7b7d48a82cd37c07fa06ae5b04fd68a26f58a00e13d",
  "sema_ref": "Gate#02f6",
  "sema_stub": "02f6",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5"
    },
    "yields": {
      "decision": "Decision#934e"
    }
  }
}
```

---

## Greet#ff79

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
  "sema_id": "sema:Greet#mh:SHA-256:ff7922e2f2c31a160124615bf9319b11b87f8dea4df015f5ec6c22699b67a9f4",
  "sema_ref": "Greet#ff79",
  "sema_stub": "ff79",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    },
    "references": {
      "agent": "Agent#d183",
      "identity": "Identity#626c"
    }
  }
}
```

---

## Heartbeat#8e36

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Heartbeat#mh:SHA-256:8e3615550a11d28fdf434eedbb19eb51577a226aa3eea5e6221384f5bcfb6503",
  "sema_ref": "Heartbeat#8e36",
  "sema_stub": "8e36",
  "dependencies": {
    "references": {
      "monitor": "Monitor#6773"
    },
    "accepts": {
      "signal": "Signal#f39d"
    },
    "composes_with": {
      "quorum": "Quorum#a295"
    }
  }
}
```

---

## Hysteresis#addb

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_id": "sema:Hysteresis#mh:SHA-256:addbf14e04e773a9a6b2313b0b300392bb2c33d79aace9d3b9d9a2ea600c42cb",
  "sema_ref": "Hysteresis#addb",
  "sema_stub": "addb",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "dampen": "Dampen#3f0c",
      "state": "State#4d58"
    }
  }
}
```

---

## IdempotentWrite#1023

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
      "UniqueHandle#9b3c"
    ],
    "ring": 0
  },
  "sema_id": "sema:IdempotentWrite#mh:SHA-256:102320da989eb7e2422d943ab8482cb0aa88481aa843794a7928fc531ef1acef",
  "sema_ref": "IdempotentWrite#1023",
  "sema_stub": "1023",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#5602",
      "cache": "Cache#08ed",
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

## Judge#b8d6

```json
{
  "handle": "Judge",
  "mechanism": "Qualitative Evaluation. Evaluates the structural merit or quality of a {{subject}} on a continuous scale [0.0, 1.0]. Unlike {{check}} (which validates binary truth) or {{validate}} (which checks schema), Judge evaluates {{gradient}}s of quality by applying a {{scoring_function}} that encodes the {{criteria}}, yielding a {{score}}.",
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
  "sema_id": "sema:Judge#mh:SHA-256:b8d60cf6d7f4c087b09f576533d1eb077bce121fafc6ea8905c60539a663a7d1",
  "sema_ref": "Judge#b8d6",
  "sema_stub": "b8d6",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "scoring_function": "ScoringFunction#3a4e",
      "subject": "Subject#9a60"
    },
    "references": {
      "gradient": "Gradient#480b",
      "criteria": "Criteria#ef6b",
      "validate": "Validate#aebf",
      "check": "Check#410e",
      "agent": "Agent#d183"
    },
    "yields": {
      "score": "Score#d220"
    }
  }
}
```

---

## Loop#a316

```json
{
  "handle": "Loop",
  "mechanism": "A control flow structure that repeats a sequence of {{work}} until a specific {{condition}} is met. Essential for feedback, learning, and persistent processes.",
  "gloss": "Repeated execution cycle",
  "invariants": [
    "Termination Guarantee: Must have a proven exit condition (or explicit Daemon mode).",
    "Progress: State must change between iterations to avoid infinite freeze."
  ],
  "sema_id": "sema:Loop#mh:SHA-256:a316611f7d6278db4f0fa1f06bcdbd49eb47fd0c084f1b1956c9f688b922e2ca",
  "sema_ref": "Loop#a316",
  "sema_stub": "a316",
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
      "work": "Work#bc56"
    }
  }
}
```

---

## Monitor#6773

```json
{
  "handle": "Monitor",
  "gloss": "Continuous observation of state over time",
  "mechanism": "A persistent process that uses a {{loop}} to repeatedly execute {{observe}} on a target {{system}} or {{state}} at defined intervals. It compares the observed state against a baseline or invariant, emitting a {{signal}} if a deviation ({{anomaly}}) is detected.",
  "signature": [
    "Loop#a316(State#4d58)"
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
  "sema_ref": "Monitor#6773",
  "sema_id": "sema:Monitor#mh:SHA-256:6773980f55c9a9be28d6ff45fe338e020b7bf585367b52a9ac28156b85ec9752",
  "sema_stub": "6773",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "loop": "Loop#a316",
      "observe": "Observe#abc0"
    },
    "references": {
      "system": "System#e314",
      "state": "State#4d58",
      "anomaly": "Anomaly#fac8",
      "signal": "Signal#f39d"
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
      "Monitor#6773"
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

## NegativeProof#14ee

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
  "sema_ref": "NegativeProof#14ee",
  "sema_id": "sema:NegativeProof#mh:SHA-256:14eea706b599283b9597da8ab87d4f4a41cbdf1597c31fc0dd96c96db29bad51",
  "sema_stub": "14ee",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#ffa7",
      "agent": "Agent#d183",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Observe#abc0

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
      "Belief#cafb",
      "Attention"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Observe#mh:SHA-256:abc0f98910ec9f78f075f0ee9afb963a01a77d2c2a6d58b18e96c5760056ce4e",
  "sema_ref": "Observe#abc0",
  "sema_stub": "abc0",
  "dependencies": {
    "yields": {
      "context": "Context#e88a"
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

## Quorum#a295

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
    "N agents in voting set.",
    "K threshold defined where K \u2264 N.",
    "Proposal formulated."
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
      "LazyConsensus#bd8f"
    ],
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Quorum#mh:SHA-256:a295620c00226d81fa6218bae4cc88714365179ef9cfa18cbfb65bd34e6fc19a",
  "sema_ref": "Quorum#a295",
  "sema_stub": "a295",
  "dependencies": {
    "accepts": {
      "ballot": "Ballot#1934"
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
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

## ReAttempt#8f48

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "caution": "Requires an explicit retry budget; uncapped ReAttempt#8f48 can amplify transient failures into DoS against downstream resources."
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:ReAttempt#mh:SHA-256:8f4881fc81cc8467e762c7b14381e95007953d358e107427a9eb14a1539141fe",
  "sema_ref": "ReAttempt#8f48",
  "sema_stub": "8f48",
  "dependencies": {
    "references": {
      "backoff": "Backoff#c6d1",
      "retry": "Retry#cb3a"
    }
  }
}
```

---

## Route#34c7

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "related": [
      "Select#15c2"
    ],
    "ring": 0,
    "supersedes": [
      "sema:Switch#mh:SHA-256:e7f9f7fba998e74e83165b23f0328643be83117559cd4d1a8711043955f6d6b0"
    ]
  },
  "sema_ref": "Route#34c7",
  "sema_id": "sema:Route#mh:SHA-256:34c7ac9e2640ce630821dc4d77e6a00bce56e47aff15976fd40acbc0a10eceb6",
  "sema_stub": "34c7",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
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
      "AgentSandbox#1838",
      "CircuitBreaker#0577",
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

## Search#82c8

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
  "sema_ref": "Search#82c8",
  "sema_id": "sema:Search#mh:SHA-256:82c8512d7ffa16d03cffacbc84a2f27a2f68965b21d495f489325ea87dc84db7",
  "sema_stub": "82c8",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "check": "Check#410e",
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

## Sign#d60d

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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1
  },
  "signature": [
    "Act#dc2d(Identity#626c)"
  ],
  "sema_id": "sema:Sign#mh:SHA-256:d60d27217d8d1f219460f69a9971b9f73c1e279c5fddbb7db51a87c8015e34e8",
  "sema_ref": "Sign#d60d",
  "sema_stub": "d60d",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "composes_with": {
      "act": "Act#dc2d"
    },
    "references": {
      "identity": "Identity#626c",
      "signal": "Signal#f39d"
    },
    "accepts": {
      "artifact": "Artifact#6254"
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "state_transition": "StateTransition#9e61",
      "state": "State#4d58",
      "audit": "Audit#6888"
    }
  }
}
```

---

## StateSnapshot#5a11

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
  "sema_id": "sema:StateSnapshot#mh:SHA-256:5a11e42d46f259b1e618969b879bf1e1143349efee16bfe29af680d25db01d2d",
  "sema_ref": "StateSnapshot#5a11",
  "sema_stub": "5a11",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "idempotent_write": "IdempotentWrite#1023",
      "snapshot": "Snapshot#0ae9",
      "state": "State#4d58"
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

## TaskLifecycle#fecc

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
    "StateTransition#9e61(Task#b290)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 1,
    "tier": 1,
    "related": []
  },
  "sema_ref": "TaskLifecycle#fecc",
  "sema_id": "sema:TaskLifecycle#mh:SHA-256:feccada92c845fa22500b7cb4960113affe56f52be76e21b836bebc52c7d657a",
  "sema_stub": "fecc",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "heartbeat": "Heartbeat#8e36",
      "event": "Event#7e71",
      "risk": "Risk#1980",
      "exception": "Exception#53bb",
      "agent": "Agent#d183"
    },
    "composes_with": {
      "state_transition": "StateTransition#9e61"
    },
    "yields": {
      "result": "Result#f29e"
    }
  }
}
```

---

## Throttle#4d47

```json
{
  "handle": "Throttle",
  "mechanism": "Rate Limiting: Maximum N {{task}}s per time window W. Excess requests rejected, queued, or delayed. Window can be sliding or fixed. Separate limits per action type or global. Utilizes {{backoff}}.",
  "gloss": "Rate-limiting to prevent resource exhaustion",
  "failure_modes": [
    "Legitimate Denial: Throttle cannot distinguish attack traffic from legitimate burst."
  ],
  "invariants": [
    "Rate Limit: Output rate \u2264 MaxRate within any window (sliding or fixed).",
    "Queue Bounding: Dropped requests > 0 if InputRate >> MaxRate."
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
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Throttle#mh:SHA-256:4d479e4b025f72c347424f50b7ac6a3503a9447bd3f085f6e032c326936e56cc",
  "sema_ref": "Throttle#4d47",
  "sema_stub": "4d47",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "composes_with": {
      "backoff": "Backoff#c6d1"
    }
  }
}
```

---

## TimeWarpLog#8751

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
  "sema_id": "sema:TimeWarpLog#mh:SHA-256:87517c40ac4eed4b0ac6a1a3077a0781715ae4644cf018a32226e116e4eb1b34",
  "sema_ref": "TimeWarpLog#8751",
  "sema_stub": "8751",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "monotonic_counter": "MonotonicCounter#c7ab",
      "system": "System#e314",
      "world_reversible": "WorldReversible#f664",
      "agent": "Agent#d183",
      "state": "State#4d58",
      "causal_barrier": "CausalBarrier#cb43"
    }
  }
}
```

---

## ToolInvoke#bd2b

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
      "AgentSandbox#1838"
    ]
  },
  "sema_ref": "ToolInvoke#bd2b",
  "sema_id": "sema:ToolInvoke#mh:SHA-256:bd2b35e0886f79fde129e2a1185845ecb644c14c4b89b90ec5dc8eb54c51ba10",
  "sema_stub": "bd2b",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "task": "Task#b290"
    },
    "composes_with": {
      "input_guard": "InputGuard#7353"
    }
  }
}
```

---

## Trace#2836

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
  "sema_id": "sema:Trace#mh:SHA-256:2836bfb80d859fb0e87d1426101a44aff10d69487ac2d31f0919626e06512733",
  "sema_ref": "Trace#2836",
  "sema_stub": "2836",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "decay": "Decay#1e8b"
    }
  }
}
```

---

## TriGate#66aa

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
    "Gate#02f6(Judge#b8d6)"
  ],
  "_meta": {
    "layer": "Infrastructure",
    "category": "Primitives",
    "ring": 0,
    "tier": 1
  },
  "sema_ref": "TriGate#66aa",
  "sema_id": "sema:TriGate#mh:SHA-256:66aa3ca5cbe8da66ba689e906a9b9b7ed99191386f116e597e8aba12ec0fdf60",
  "sema_stub": "66aa",
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "gate": "Gate#02f6",
      "ledger": "Ledger#6fc4",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## Warmup#c9e4

```json
{
  "handle": "Warmup",
  "mechanism": "Gradual Capacity Ramp: On activation, start at reduced capacity C_min and increase to C_max over time T following a defined curve. Prevents 'thundering herd' overload on cold systems. Utilizes {{greet}}, {{throttle}}.",
  "gloss": "Gradual capacity increase to stabilize cold systems",
  "failure_modes": [
    "Premature Load: Traffic arrives before warmup completes.",
    "False Warmth: Timer completes but internal state (e.g. cache) is still cold."
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
  "sema_layer": "Infrastructure",
  "sema_category": "Primitives",
  "sema_id": "sema:Warmup#mh:SHA-256:c9e476dea8a55fbc1c8f608fd42f84409d7d0ba5230a5f394398d2a52a0ebaa1",
  "sema_ref": "Warmup#c9e4",
  "sema_stub": "c9e4",
  "dependencies": {
    "references": {
      "throttle": "Throttle#4d47",
      "system": "System#e314",
      "greet": "Greet#ff79"
    }
  }
}
```

---

## AuditTrail#3c71

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
    "Trace#2836(Ledger#6fc4)"
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
  "sema_ref": "AuditTrail#3c71",
  "sema_id": "sema:AuditTrail#mh:SHA-256:3c71c3459eb16bd99cc1d004f08b70d1b8ba5bcc606c1e3430b1ca8e7136969f",
  "sema_stub": "3c71",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9f0c",
  "dependencies": {
    "references": {
      "monotonic_counter": "MonotonicCounter#c7ab",
      "sign": "Sign#d60d",
      "ledger": "Ledger#6fc4",
      "trace": "Trace#2836",
      "identity": "Identity#626c",
      "agent": "Agent#d183",
      "audit": "Audit#6888"
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
  "sema_category": "Verification#9f0c",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## ExplainBeacon#9d6d

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
  "sema_id": "sema:ExplainBeacon#mh:SHA-256:9d6d4458df5002502fc645e29e7b5d60c0f981bd3957e55fb9aa6c75191fa141",
  "sema_ref": "ExplainBeacon#9d6d",
  "sema_stub": "9d6d",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9f0c",
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "stream": "Stream#22f3",
      "greet": "Greet#ff79",
      "heartbeat": "Heartbeat#8e36"
    }
  }
}
```

---

## HumanApprove#6434

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
  "sema_category": "Verification#9f0c",
  "sema_id": "sema:HumanApprove#mh:SHA-256:64349d0a8daadf838541313b0ad126768854b279d8cdafa70ac06fd59b997b15",
  "sema_ref": "HumanApprove#6434",
  "sema_stub": "6434",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "audit": "Audit#6888",
      "context": "Context#e88a",
      "system": "System#e314"
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
  "sema_category": "Verification#9f0c"
}
```

---

## OathBind#af30

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
  "sema_ref": "OathBind#af30",
  "sema_id": "sema:OathBind#mh:SHA-256:af30b46c08a384e82ae9080eec339d644c59f02530469ad43c30b441a5c54645",
  "sema_stub": "af30",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9f0c",
  "failure_modes": [
    "Penalty severity decoupled from deviation severity.",
    "Rule set ambiguity triggers unintended penalty."
  ],
  "dependencies": {
    "references": {
      "spot_audit": "SpotAudit#000e",
      "rule_set": "RuleSet#ac40",
      "actor": "Actor#57f6"
    }
  }
}
```

---

## OutputGuard#1c09

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
  "sema_category": "Verification#9f0c",
  "sema_id": "sema:OutputGuard#mh:SHA-256:1c0983452e0c7f55fd7862c360d7edf6be3043338d0844fdefd72ef6ddc41383",
  "sema_ref": "OutputGuard#1c09",
  "sema_stub": "1c09",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "problem": "Problem#64d0"
    },
    "accepts": {
      "solution": "Solution#445c"
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
  "sema_category": "Verification#9f0c",
  "dependencies": {
    "references": {
      "audit": "Audit#6888",
      "state_audit": "StateAudit#8195"
    }
  }
}
```

---

## Validate#aebf

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
  "sema_id": "sema:Validate#mh:SHA-256:aebfb015224719006acab6ffc4eed37a94ecb262ac59b0af4c2c43b58c2f1ca7",
  "sema_ref": "Validate#aebf",
  "sema_stub": "aebf",
  "sema_layer": "Infrastructure",
  "sema_category": "Verification#9f0c",
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "accept_spec": "AcceptSpec#762e"
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
      "BayesUpdate#ee85"
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

## BayesUpdate#ee85

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
    "Prior probability defined in (0,1)",
    "New evidence observed.",
    "Likelihood computable."
  ],
  "postconditions": [
    "Posterior probability in (0,1)",
    "{{belief}} updated proportional to evidence strength.",
    "Prior recoverable given likelihood."
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
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "sema_id": "sema:BayesUpdate#mh:SHA-256:ee85444cb2388d0b73a897f719d6eb36dcea5c3bac76e1cf863132d57a6b4494",
  "sema_ref": "BayesUpdate#ee85",
  "sema_stub": "ee85",
  "dependencies": {
    "references": {
      "base_rate_include": "BaseRateInclude#aa0b",
      "belief": "Belief#cafb",
      "observe": "Observe#abc0"
    }
  }
}
```

---

## BreadthGovernor#d021

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
  "sema_id": "sema:BreadthGovernor#mh:SHA-256:d0217ed8bdde21c38d9dd237c43b7c74912d7b9fd16a2879b21343178e32b481",
  "sema_ref": "BreadthGovernor#d021",
  "sema_stub": "d021",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "prophet_fan_out": "ProphetFanOut#c8d0",
      "parsimony": "Parsimony#6d67",
      "value": "Value#3c5d",
      "budget": "Budget#0934",
      "context": "Context#e88a",
      "decompose": "Decompose#5471",
      "parallel": "Parallel#3181"
    }
  }
}
```

---

## ConfidenceCalibrate#e454

```json
{
  "handle": "ConfidenceCalibrate",
  "mechanism": "Track Record Alignment: For claims rated 70% confident, ~70% should be true. Track predictions vs outcomes. If 90% claims are right only 60% of time, you are overconfident\u2014widen uncertainty. If 90% claims are right 99% of time, you are underconfident\u2014tighten. It adjusts the internal probability model using {{bayes_update}} on historical accuracy data, ensuring {{base_rate_include}} is respected.",
  "gloss": "Aligning subjective confidence with objective frequency",
  "failure_modes": [
    "Over-correction: {{agent}} becomes under-confident to avoid being wrong, refusing to act on strong signals."
  ],
  "invariants": [
    "Post-calibration monotonicity: the adjusted confidence\u2192frequency mapping must be monotonic non-decreasing (higher stated confidence implies higher or equal actual frequency). The observed pre-calibration curve may be non-monotonic; the pattern's job is to produce a monotonic output."
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
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "sema_id": "sema:ConfidenceCalibrate#mh:SHA-256:e454e65f7f5cb51ae4ca34181b14d2bb0d592dd05dc97673a08909b5d2e9a8ba",
  "sema_ref": "ConfidenceCalibrate#e454",
  "sema_stub": "e454",
  "dependencies": {
    "references": {
      "base_rate_include": "BaseRateInclude#aa0b",
      "agent": "Agent#d183",
      "bayes_update": "BayesUpdate#ee85"
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
      "DissentSeek#89c2"
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

## ContextFirst#dbb4

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
  "sema_id": "sema:ContextFirst#mh:SHA-256:dbb4decbd9e35f6e913ba9aa07c53facd707d0da2081ae20a9f117fd949a1a36",
  "sema_ref": "ContextFirst#dbb4",
  "sema_stub": "dbb4",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Prioritize#420e(Context#e88a)"
  ],
  "dependencies": {
    "references": {
      "solver_node": "SolverNode#86bb",
      "prioritize": "Prioritize#420e",
      "context": "Context#e88a",
      "state": "State#4d58",
      "agent": "Agent#d183",
      "warmup": "Warmup#c9e4"
    }
  }
}
```

---

## EpistemicCalibrate#3e32

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
      "ConfidenceCalibrate#e454"
    ],
    "ring": 2
  },
  "sema_id": "sema:EpistemicCalibrate#mh:SHA-256:3e32459cf46f6d4492af69d5c6be854e9ea96d4a87c6f699d54422b9a1a7be52",
  "sema_ref": "EpistemicCalibrate#3e32",
  "sema_stub": "3e32",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "decay": "Decay#1e8b"
    }
  }
}
```

---

## HackDetect#e160

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
  "sema_id": "sema:HackDetect#mh:SHA-256:e160512d54efe12cd529d205e15cfd5696a60ca7f0f50dff509a62bb2a30b862",
  "sema_ref": "HackDetect#e160",
  "sema_stub": "e160",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "input_guard": "InputGuard#7353",
      "system": "System#e314",
      "agent": "Agent#d183",
      "ejection_seat": "EjectionSeat#b71c"
    }
  }
}
```

---

## HindsightBlock#54f4

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
  "sema_id": "sema:HindsightBlock#mh:SHA-256:54f41365c03c1e56010dff7f60f0012c17f4ce09dfc293041bfd608ff3d87e82",
  "sema_ref": "HindsightBlock#54f4",
  "sema_stub": "54f4",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "pre_mortem": "PreMortem#8ca0",
      "decision": "Decision#934e",
      "outcome": "Outcome#9bf0",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## LayeredCheck#0dbc

```json
{
  "handle": "LayeredCheck",
  "mechanism": "A {{check}} strategy that evaluates constraints in a strict {{hierarchy}} of abstraction (e.g., existence -> {{validate}} (schema) -> {{understand}} (semantics)). It uses a {{sequence}} of {{gate}}s where lower-level failures halt execution immediately, preventing resource waste on higher-level checks for fundamentally broken inputs.",
  "gloss": "Hierarchical verification strategy",
  "signature": [
    "Check#410e(Hierarchy#d530)"
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
      "PURECheck#21dc"
    ]
  },
  "sema_ref": "LayeredCheck#0dbc",
  "sema_id": "sema:LayeredCheck#mh:SHA-256:0dbcfa9017555acf30aa68099113de2e509e7223c25e780effd785f57a74206d",
  "sema_stub": "0dbc",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "understand": "Understand#c38c",
      "hierarchy": "Hierarchy#d530",
      "validate": "Validate#aebf"
    },
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "gate": "Gate#02f6",
      "check": "Check#410e"
    }
  }
}
```

---

## NormCheck#a2be

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
  "sema_id": "sema:NormCheck#mh:SHA-256:a2be1909e9cb7487aac74578574ad7c7ffd0ceb323b9a9d89d216349efadeb4e",
  "sema_ref": "NormCheck#a2be",
  "sema_stub": "a2be",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Check#410e(Value#3c5d)"
  ],
  "dependencies": {
    "references": {
      "prophet_fan_out": "ProphetFanOut#c8d0",
      "value": "Value#3c5d",
      "check": "Check#410e",
      "judge": "Judge#b8d6",
      "quorum": "Quorum#a295",
      "normative_judge": "NormativeJudge#1900"
    }
  }
}
```

---

## NormativeJudge#1900

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
  "sema_id": "sema:NormativeJudge#mh:SHA-256:19007a150e1bd0c5f36ccc33b3afe710b09006a8379b182cbf2a9d1875c8665f",
  "sema_ref": "NormativeJudge#1900",
  "sema_stub": "1900",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Judge#b8d6(Value#3c5d)"
  ],
  "dependencies": {
    "accepts": {
      "vector": "Vector#c7c4"
    },
    "composes_with": {
      "perspective_ensemble": "PerspectiveEnsemble#e277"
    },
    "references": {
      "human_approve": "HumanApprove#6434",
      "value": "Value#3c5d",
      "state": "State#4d58",
      "judge": "Judge#b8d6",
      "quorum": "Quorum#a295",
      "outcome": "Outcome#9bf0"
    }
  }
}
```

---

## OntologyAdapt#e429

```json
{
  "handle": "OntologyAdapt",
  "mechanism": "Derived from Piagetian psychology. When new data defies classification within the current ontology, the {{agent}} does not force-fit it or discard it. Instead, it triggers a 'Restructure' event, creating new root {{category}}s that accommodate the {{anomaly}} as a fundamental feature. Utilizes {{ontology_handshake}}.",
  "gloss": "Restructuring categories to fit data",
  "failure_modes": [
    "{{category}} explosion (creating a new {{category}} for every {{noise}} point)."
  ],
  "invariants": [
    "{{conservation}} of Data: No anomaly is discarded during accommodation",
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
  "sema_id": "sema:OntologyAdapt#mh:SHA-256:e42969c642c58242d050f5dc150fbfbae49fb4cffe192515cd20ce648f7b8ac8",
  "sema_ref": "OntologyAdapt#e429",
  "sema_stub": "e429",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "conservation": "Conservation#d63a",
      "ontology_handshake": "OntologyHandshake#8443",
      "category": "sema:Category#mh:SHA-256:1ab7e3c9863286a33d2be0ec51112ecfadef9e46a07f5f15b9f6cd33f74d8bd1",
      "anomaly": "Anomaly#fac8",
      "agent": "Agent#d183",
      "noise": "Noise#3d9a"
    }
  }
}
```

---

## ProphetFanOut#c8d0

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
  "sema_id": "sema:ProphetFanOut#mh:SHA-256:c8d0f17a0bf8be9fd40e9e69ef88d54f23216b2860d0602a1f88b29f64418709",
  "sema_ref": "ProphetFanOut#c8d0",
  "sema_stub": "c8d0",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "quorum": "Quorum#a295",
      "chain": "Chain#711e",
      "aggregate": "Aggregate#8c2a"
    }
  }
}
```

---

## RegimeSense#d8f0

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
  "sema_id": "sema:RegimeSense#mh:SHA-256:d8f093bdb5efb28c7c1a5ad8fecd5e420ed3a289382bfc3cf3c3ab7a6e19c2d3",
  "sema_ref": "RegimeSense#d8f0",
  "sema_stub": "d8f0",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "ontology_adapt": "OntologyAdapt#e429",
      "quorum": "Quorum#a295",
      "drift_watch": "DriftWatch#5baa",
      "agent": "Agent#d183",
      "noise": "Noise#3d9a"
    }
  }
}
```

---

## ScopeFreeze#7abb

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
      "range": "{Reject, Queue#7ca9, CostAnalysis}",
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
  "sema_id": "sema:ScopeFreeze#mh:SHA-256:7abbb1c81b0b97b80efcb1c9c053b336aeea7863f2a98e35b9c97a3f3fe1f3fa",
  "sema_ref": "ScopeFreeze#7abb",
  "sema_stub": "7abb",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "satisfice": "Satisfice#64ac",
      "task": "Task#b290",
      "accept_spec": "AcceptSpec#762e",
      "transition": "Transition#072d",
      "timebox_think": "TimeboxThink#9e1b",
      "decompose": "Decompose#5471",
      "agent": "Agent#d183"
    }
  }
}
```

---

## SemanticTabu#d1eb

```json
{
  "handle": "SemanticTabu",
  "mechanism": "An ideation protocol where the agent explicitly lists existing mechanisms as 'Tabu' (forbidden). It must then solve the problem without using any mechanism on the list. This forces the activation of latent, low-probability pathways in the semantic network. It broadcasts the forbidden list via {{trace}} to ensure the entire swarm respects the constraint.",
  "gloss": "Constraint-based novelty enforcement",
  "failure_modes": [
    "Paralysis: if the Tabu list covers all possible physics."
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
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "sema_id": "sema:SemanticTabu#mh:SHA-256:d1ebb04c973e6f2c0e3a4dbe07f9feeb88707f7cbb0ee210713041de2bef90de",
  "sema_ref": "SemanticTabu#d1eb",
  "sema_stub": "d1eb",
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "constraint": "Constraint#87fe",
      "solution": "Solution#445c"
    }
  }
}
```

---

## SourceEvaluate#3488

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
  "sema_id": "sema:SourceEvaluate#mh:SHA-256:3488f8766ed315587ca2de4b0e6560358f2affb79e14a9cb0e484cd0d6143628",
  "sema_ref": "SourceEvaluate#3488",
  "sema_stub": "3488",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "signature": [
    "Judge#b8d6(Agent#d183)"
  ],
  "dependencies": {
    "references": {
      "cite_back": "CiteBack#0a08",
      "agent": "Agent#d183",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## SurprisalUpdate#9db2

```json
{
  "handle": "SurprisalUpdate",
  "mechanism": "A learning protocol where the agent updates its internal model (weights, embeddings, or context) based on failed predictions, weighted by the magnitude of surprise. Higher surprisal = larger update. 'Learn most from what confused you most.' This implements Surprisal-Weighted Fine-Tuning (SWFT): loss contribution is proportional to -log(P(observed|predicted)). Utilizes {{regime_sense}}, {{epistemic_roi}}.",
  "gloss": "Learning weighted by prediction failure magnitude",
  "failure_modes": [
    "Outlier Overfitting: Rare high-surprisal events dominating learning.",
    "Catastrophic Forgetting: Aggressive updates erasing previously stable knowledge.",
    "Compute Cost: High-surprisal events require expensive {{gradient}} updates."
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
      "BayesUpdate#ee85"
    ],
    "ring": 2
  },
  "sema_id": "sema:SurprisalUpdate#mh:SHA-256:9db262c4006d612677ef684ff294995aa1f5013e19c26b0e3f79b5bd01cb8e78",
  "sema_ref": "SurprisalUpdate#9db2",
  "sema_stub": "9db2",
  "sema_layer": "Mind",
  "sema_category": "Inference",
  "dependencies": {
    "references": {
      "epistemic_roi": "EpistemicROI#9e4f",
      "regime_sense": "RegimeSense#d8f0",
      "gradient": "Gradient#480b"
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

## TemporalEnsembleForecasting#8010

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
  "sema_id": "sema:TemporalEnsembleForecasting#mh:SHA-256:80105ef1dcbd4d011bbc93a73358fc9d7d326d2392a1c50601786c151c7f7bd5",
  "sema_ref": "TemporalEnsembleForecasting#8010",
  "sema_stub": "8010",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#739b"
    }
  }
}
```

---

## TruthseekingProtocol#fcad

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
  "sema_id": "sema:TruthseekingProtocol#mh:SHA-256:fcad8e83d5980bf36c70d2861905d8fa1d0c9137ecc1db159b55cdc64784e022",
  "sema_ref": "TruthseekingProtocol#fcad",
  "sema_stub": "fcad",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#739b",
      "marginal_value_rule": "MarginalValueRule#8660"
    },
    "references": {
      "validate": "Validate#aebf"
    }
  }
}
```

---

## BeliefTracking#5a14

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
      "BayesUpdate#ee85"
    ],
    "ring": 2
  },
  "sema_id": "sema:BeliefTracking#mh:SHA-256:5a146bb1fcc101d6283b32b2304637b5adc6fe976a8ddefab113845a6daec1e3",
  "sema_ref": "BeliefTracking#5a14",
  "sema_stub": "5a14",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "surprisal_update": "SurprisalUpdate#9db2",
      "cognitive_bias": "CognitiveBias#4b32",
      "belief": "Belief#cafb",
      "agent": "Agent#d183"
    }
  }
}
```

---

## ChunkMerge#ac72

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
    "{{conservation}} of information: Merged chunk retains key retrieval hooks of parts",
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
  "sema_id": "sema:ChunkMerge#mh:SHA-256:ac727e19b98b3c1043c437da0131bf23f38a7b34e994dfc3c138103f5286bac4",
  "sema_ref": "ChunkMerge#ac72",
  "sema_stub": "ac72",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "conservation": "Conservation#d63a",
      "aggregate": "Aggregate#8c2a",
      "constraint": "Constraint#87fe",
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
  "sema_id": "sema:ContextCompress#mh:SHA-256:4845cff7c2a6371afdb2d199ed427a5e5d8d8c5f6a2d24a3b6b8278eb8dff0ee",
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
      "compress": "Compress#0967",
      "constraint": "Constraint#87fe",
      "context": "Context#e88a",
      "state": "State#4d58"
    }
  }
}
```

---

## CurriculumReplay#ea48

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
  "sema_id": "sema:CurriculumReplay#mh:SHA-256:ea4813af7f49a5dc9ca8ef4080f13d87373e2e728c511298abed92c2dcf92613",
  "sema_ref": "CurriculumReplay#ea48",
  "sema_stub": "ea48",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "experience_sharding": "ExperienceSharding#4158",
      "agent": "Agent#d183",
      "decay": "Decay#1e8b"
    }
  }
}
```

---

## ExperienceSharding#4158

```json
{
  "handle": "ExperienceSharding",
  "mechanism": "Applies the {{shard}} primitive to agent memory. When context fills, the agent splits into two specialized agents (active vs archival) rather than forgetting. It segments history into discrete blocks via {{chunk_merge}} before distributing them across the agent cluster.",
  "gloss": "Agent bifurcation on context saturation: active vs archival specialists",
  "failure_modes": [
    "Coordination Overhead: Overhead between shards increases as shard count grows."
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
      "FabricSharding#3946"
    ],
    "ring": 0
  },
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "sema_id": "sema:ExperienceSharding#mh:SHA-256:415806a13e3ba84483094912eb1d966e28595f56938bb00f7b3489f5ec58ebe3",
  "sema_ref": "ExperienceSharding#4158",
  "sema_stub": "4158",
  "dependencies": {
    "references": {
      "shard": "Shard#1e74",
      "chunk_merge": "ChunkMerge#ac72"
    }
  }
}
```

---

## HolographicShard#34d0

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
  "sema_id": "sema:HolographicShard#mh:SHA-256:34d0f881cdafeafc666f65821f0d2832f9fd044189745d414bae885fafcd1b0f",
  "sema_ref": "HolographicShard#34d0",
  "sema_stub": "34d0",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "deep": "Deep#89f0",
      "fabric_sharding": "FabricSharding#3946"
    }
  }
}
```

---

## LatentAttachment#640e

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
  "sema_id": "sema:LatentAttachment#mh:SHA-256:640effb57697210d6b0f9c583d706aeac2d5203635437b407f690333dceb5860",
  "sema_ref": "LatentAttachment#640e",
  "sema_stub": "640e",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "concept_anchor": "ConceptAnchor#828b"
    }
  }
}
```

---

## LocalizedLearning#eb5a

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
  "sema_id": "sema:LocalizedLearning#mh:SHA-256:eb5a8dec05991d7b8bc28ec2c06e27a77f02eb884646526303febcbac67004f8",
  "sema_ref": "LocalizedLearning#eb5a",
  "sema_stub": "eb5a",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "signature": [
    "Act#dc2d(FeedbackSignal#afac)"
  ],
  "dependencies": {
    "accepts": {
      "feedback_signal": "FeedbackSignal#afac"
    },
    "references": {
      "solver_manifest": "SolverManifest#11ea",
      "act": "Act#dc2d"
    }
  }
}
```

---

## PathwayMemory#7899

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
  "sema_id": "sema:PathwayMemory#mh:SHA-256:7899805e7e4497c1bbd072db6763026b3f0b966e773b1901bdf40701f21861d9",
  "sema_ref": "PathwayMemory#7899",
  "sema_stub": "7899",
  "dependencies": {
    "references": {
      "cache": "Cache#08ed"
    }
  }
}
```

---

## Proprioception#ec6c

```json
{
  "handle": "Proprioception",
  "mechanism": "Continuous self-monitoring of position in the {{task}} graph. An {{agent}} periodic 'ping' to itself to verify {{context}}, active tool state, and depth in recursion. Prevents 'getting lost' in long chains of thought. It maintains internal {{state}} awareness, using {{somatic_marker}} to detect recursion depth limits or resource fatigue.",
  "gloss": "Self-location awareness within the task graph",
  "failure_modes": [
    "Stagnation: {{agent}} remains in same node > N ticks.",
    "Orphaned: Parent {{task}} ID not found or unresponsive.",
    "Hallucinated {{context}}: Stack {{trace}} does not match environmental reality."
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
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "sema_id": "sema:Proprioception#mh:SHA-256:ec6c0681f6d5482fffd1cf6057c98c7b832f1445c9fd63a7107f2be8f57efc71",
  "sema_ref": "Proprioception#ec6c",
  "sema_stub": "ec6c",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "context": "Context#e88a",
      "somatic_marker": "SomaticMarker#7250",
      "state": "State#4d58",
      "trace": "Trace#2836",
      "agent": "Agent#d183"
    }
  }
}
```

---

## RetrievalAugment#f401

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
      "DeepResearch#d937"
    ],
    "ring": 2
  },
  "sema_id": "sema:RetrievalAugment#mh:SHA-256:f401dbfd92b4775ec02091329df7626ef81a2edbd9264fcbde9b148e79a14b8b",
  "sema_ref": "RetrievalAugment#f401",
  "sema_stub": "f401",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "prompt": "Prompt#b18a",
      "latent_attachment": "LatentAttachment#640e",
      "context": "Context#e88a",
      "context_first": "ContextFirst#dbb4",
      "agent": "Agent#d183",
      "chain_of_thought": "ChainOfThought#380a"
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

## SelfReminder#cd98

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
  "sema_id": "sema:SelfReminder#mh:SHA-256:cd9882d36fb491f3a1514093812b5faa5aec92cd11f539b4c2370c41253ea186",
  "sema_ref": "SelfReminder#cd98",
  "sema_stub": "cd98",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "constraint": "Constraint#87fe",
      "trace": "Trace#2836"
    }
  }
}
```

---

## SimulationTrace#1b91

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
  "sema_id": "sema:SimulationTrace#mh:SHA-256:1b91cf6bf63e7b541719e7d1f05c35210bf26e012c80a4964f89d7f554b8f608",
  "sema_ref": "SimulationTrace#1b91",
  "sema_stub": "1b91",
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "mental_sim": "MentalSim#b817",
      "simulation": "Simulation#398f"
    }
  }
}
```

---

## TraceBelief#3902

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
  "sema_id": "sema:TraceBelief#mh:SHA-256:3902408bf0eb4f57be0b17bdb00b227be02ba1e5c513009d71f4346af2aa782a",
  "sema_ref": "TraceBelief#3902",
  "sema_stub": "3902",
  "sema_layer": "Mind",
  "sema_category": "Memory",
  "signature": [
    "Trace#2836(Belief#cafb)"
  ],
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "surprisal_update": "SurprisalUpdate#9db2",
      "time_warp_log": "TimeWarpLog#8751",
      "belief": "Belief#cafb"
    }
  }
}
```

---

## Abduction#f9ea

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
  "sema_id": "sema:Abduction#mh:SHA-256:f9eae03bb7d903b8ad05840b6ad212f448052a4d1f796db8bfecf99c1f732445",
  "sema_ref": "Abduction#f9ea",
  "sema_stub": "f9ea",
  "dependencies": {
    "references": {
      "deduction": "Deduction#9c88",
      "induction": "Induction#2487",
      "hypothesis": "Hypothesis#ffa7",
      "rank": "Rank#7a76"
    },
    "composes_with": {
      "chain_of_thought": "ChainOfThought#380a"
    }
  }
}
```

---

## BackwardChain#e6ea

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
    "Goal state clearly defined.",
    "Domain has prerequisite structure.",
    "Knowledge base queryable."
  ],
  "postconditions": [
    "Execution plan produced OR goal proven unachievable.",
    "{{plan}} steps in executable order.",
    "All prerequisites satisfied."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:BackwardChain#mh:SHA-256:e6ea717895d0c9dcf85627d0fc8bf3eca4201962fe4f0cfab8712e3764f65e6d",
  "sema_ref": "BackwardChain#e6ea",
  "sema_stub": "e6ea",
  "dependencies": {
    "references": {
      "plan": "Plan#31a7",
      "chain": "Chain#711e",
      "chain_of_thought": "ChainOfThought#380a",
      "deduction": "Deduction#9c88"
    }
  }
}
```

---

## Bisect#30ea

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
  "sema_id": "sema:Bisect#mh:SHA-256:30ea03cad159deceac2ed6c489873b74fecd989621b6b304a4b44666b8d08454",
  "sema_ref": "Bisect#30ea",
  "sema_stub": "30ea",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "recursive_root_cause": "RecursiveRootCause#7074"
    }
  }
}
```

---

## ChainOfThought#380a

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
      "ReAct#05f2"
    ],
    "ring": 2
  },
  "sema_id": "sema:ChainOfThought#mh:SHA-256:380a1995038f9976d8feb4d1f6d9dd8efafdaed3e75ac4fe0963b63c2f9dd98b",
  "sema_ref": "ChainOfThought#380a",
  "sema_stub": "380a",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#0bb4(Chain#711e)"
  ],
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "think": "Think#0bb4",
      "chain": "Chain#711e"
    },
    "composes_with": {
      "step_back": "StepBack#35ad",
      "reflexion": "Reflexion#3b52"
    }
  }
}
```

---

## CiteBack#0a08

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
  "sema_id": "sema:CiteBack#mh:SHA-256:0a0874ee3139b8e10f66c607f4d6e00f56dda53491b92d3225eb74a70e2fc1c9",
  "sema_ref": "CiteBack#0a08",
  "sema_stub": "0a08",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "retrieval_augment": "RetrievalAugment#f401"
    }
  }
}
```

---

## CognitiveEcho#ffb5

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
      "SignalReflection#9f56"
    ],
    "ring": 2
  },
  "sema_id": "sema:CognitiveEcho#mh:SHA-256:ffb5d06faa726230d8522156450b15fb7640cdedaeb0698b7df2bf6898aba43c",
  "sema_ref": "CognitiveEcho#ffb5",
  "sema_stub": "ffb5",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "signal": "Signal#f39d",
      "simulation": "Simulation#398f"
    }
  }
}
```

---

## CollaborativeWritingProtocol#5c51

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
  "sema_id": "sema:CollaborativeWritingProtocol#mh:SHA-256:5c5131b0199f3ab495d531cfd246fb8218d1b677a22d1e28d59193704e23ebfa",
  "sema_ref": "CollaborativeWritingProtocol#5c51",
  "sema_stub": "5c51",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#739b",
      "marginal_value_rule": "MarginalValueRule#8660"
    }
  }
}
```

---

## ConceptualDecomposition#739b

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
  "sema_id": "sema:ConceptualDecomposition#mh:SHA-256:739bb7c08037f084b04c81466f61fa86545b406b93f3e944c3c3f3f73c58b835",
  "sema_ref": "ConceptualDecomposition#739b",
  "sema_stub": "739b",
  "dependencies": {
    "composes_with": {
      "synthesis": "Synthesis#26b9",
      "decomposition_gate": "DecompositionGate#5704"
    },
    "references": {
      "decompose": "Decompose#5471",
      "solver": "Solver#4ed4"
    }
  }
}
```

---

## ConstructOntology#d5a0

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
  "sema_id": "sema:ConstructOntology#mh:SHA-256:d5a06d700bbb9da7605d83238881b6039556b1ddc25be343e0eb228d868980c6",
  "sema_ref": "ConstructOntology#d5a0",
  "sema_stub": "d5a0",
  "dependencies": {
    "references": {
      "ontology_handshake": "OntologyHandshake#8443",
      "adversarial_steel": "AdversarialSteel#380c",
      "first_principles": "FirstPrinciples#1a7e"
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
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
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
      "criteria": "Criteria#ef6b",
      "datum": "Datum#31cf"
    },
    "yields": {
      "assessment": "Assessment#a765"
    }
  }
}
```

---

## Decompose#5471

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
    "{{problem}} too large to solve directly.",
    "Decomposition axis identifiable.",
    "Subproblems can be independent."
  ],
  "postconditions": [
    "Set of independent subproblems.",
    "Combined {{solution}} equals original.",
    "No subproblem depends on sibling."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Decompose#mh:SHA-256:5471aed0463cb78290a3f65e42b1eb80aad555734355477500cd91a392b60cc7",
  "sema_ref": "Decompose#5471",
  "sema_stub": "5471",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "strategy": "Strategy#a0af",
      "problem": "Problem#64d0",
      "solution": "Solution#445c"
    }
  }
}
```

---

## DecompositionGate#5704

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
  "sema_id": "sema:DecompositionGate#mh:SHA-256:570403353e0547e54cdf752598dc418f070fcff1ba429bcdd2c49004a94656cb",
  "sema_ref": "DecompositionGate#5704",
  "sema_stub": "5704",
  "dependencies": {
    "references": {
      "frame_error": "FrameError#edf5"
    },
    "yields": {
      "decision": "Decision#934e"
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

## DeepResearch#d937

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
  "sema_id": "sema:DeepResearch#mh:SHA-256:d937f26b6ab3add7be9ca610e6864801b4cdb076572a7961b2d6de9ee390330f",
  "sema_ref": "DeepResearch#d937",
  "sema_stub": "d937",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Deep#89f0(Discover#aa70)"
  ],
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "retrieval_augment": "RetrievalAugment#f401",
      "synthesis": "Synthesis#26b9",
      "deep": "Deep#89f0",
      "discover": "Discover#aa70"
    }
  }
}
```

---

## Dialectic#2e3c

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
  "sema_id": "sema:Dialectic#mh:SHA-256:2e3c31e1dea1334d4419087fc1ec14fbc9fab8692af785f5ecb5f204c439dc03",
  "sema_ref": "Dialectic#2e3c",
  "sema_stub": "2e3c",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "perspective_ensemble": "PerspectiveEnsemble#e277",
      "synthesis": "Synthesis#26b9"
    },
    "composes_with": {
      "steelman_check": "SteelmanCheck#dd78"
    }
  }
}
```

---

## Eliminate#ee96

```json
{
  "handle": "Eliminate",
  "mechanism": "Systematic Exclusion (Sherlock Holmes): Enumerate all possible answers. For each, find a test that could falsify it. Apply tests in order of cost (cheapest first). Remove falsified options. Continue until one remains or no tests left. Remaining options are candidates. Combines {{deduction}} (ruling out what's impossible) with {{falsification}} (empirical testing of each hypothesis). It uses {{prioritize}} to order falsification tests by cost/efficiency before executing them.",
  "gloss": "Sherlock Holmes deduction via falsification",
  "failure_modes": [
    "Premature Exclusion: Eliminating the true cause because of a faulty test, leaving an empty set."
  ],
  "invariants": [
    "Monotonic Reduction: {{option}} set size strictly decreases or stays the same across iterations \u2014 options are only eliminated, never added back.",
    "Evidence-Required Exclusion: Each eliminated option must have falsifying evidence; exclusion without evidence is not permitted."
  ],
  "preconditions": [
    "{{option}} set exhaustive at start.",
    "Falsification tests available.",
    "At least one option must survive."
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
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Eliminate#mh:SHA-256:ee96bd91d065e8a5000163b00a727c417dbc8231edd52fa3f824449ec98739bd",
  "sema_ref": "Eliminate#ee96",
  "sema_stub": "ee96",
  "dependencies": {
    "references": {
      "option": "Option#483e",
      "prioritize": "Prioritize#420e",
      "falsification": "Falsification#0215",
      "deduction": "Deduction#9c88"
    }
  }
}
```

---

## Estimate#e07e

```json
{
  "handle": "Estimate",
  "mechanism": "The predictive {{think}} process of calculating the probable {{value}} cost of a {{task}} before execution. It produces a resource cost projection. It has two modes: 1. {{heuristic_snap}} for fast, rough estimates (pattern matching), 2. {{simulation}} for accurate, expensive estimates (mental execution). The output is a {{bid}} with confidence intervals. Estimation itself consumes budget and is subject to the Meta-Cap invariant.",
  "gloss": "Predictive resource costing",
  "signature": [
    "Think#0bb4(Value#3c5d)"
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
  "sema_ref": "Estimate#e07e",
  "sema_id": "sema:Estimate#mh:SHA-256:e07eb10e9887f605c68cffac1e3c68e9df7b2bbb020f934d4d820cfb1a5b8e0c",
  "sema_stub": "e07e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "heuristic_snap": "HeuristicSnap#f15c",
      "value": "Value#3c5d",
      "simulation": "Simulation#398f"
    },
    "accepts": {
      "task": "Task#b290"
    },
    "yields": {
      "bid": "Bid#cffa"
    },
    "composes_with": {
      "think": "Think#0bb4"
    }
  }
}
```

---

## EthicalReasoningProtocol#fee3

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
  "sema_id": "sema:EthicalReasoningProtocol#mh:SHA-256:fee3e79159b9c11a52dfdea86fd69156a72666aa47461209196a451c40344761",
  "sema_ref": "EthicalReasoningProtocol#fee3",
  "sema_stub": "fee3",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#739b"
    },
    "references": {
      "deliberative_align": "DeliberativeAlign#4a26"
    }
  }
}
```

---

## Expansive#bfaa

```json
{
  "handle": "Expansive",
  "gloss": "Evaluates generalization potential",
  "mechanism": "A {{judge}} of generalization potential: does the mechanism or concept transfer beyond the original domain it was designed in? Applies wherever breadth-of-application is the evaluative question \u2014 scientific generality, platform reuse, pattern-library transferability, business model cross-market viability. The essential move is stress-testing the artifact against domains deliberately outside its origin (hostile-domain probe) rather than demonstrating it on familiar cases. Specific rating semantics belong on descendants or on the composing protocol. The signature Judge({{value}}) captures that the output is a {{value}}-graded breadth score rather than a binary transferable/not-transferable verdict.",
  "invariants": [
    "Transfer: Must operate outside training distribution."
  ],
  "signature": [
    "Judge#b8d6(Value#3c5d)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Expansive#mh:SHA-256:bfaa526704a9c66a9cfe0453f2c1a911cc54e7620bf71c70d3aed0bbb17f053f",
  "sema_ref": "Expansive#bfaa",
  "sema_stub": "bfaa",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## ExtendedThinking#f9eb

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
  "sema_id": "sema:ExtendedThinking#mh:SHA-256:f9ebb3ff9fc1a5450b33e4bf50cc66315c1711169750e3fb3e700464fa1a80aa",
  "sema_ref": "ExtendedThinking#f9eb",
  "sema_stub": "f9eb",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "chain": "Chain#711e"
    }
  }
}
```

---

## Fermi#6397

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
  "sema_id": "sema:Fermi#mh:SHA-256:63972ccb8ebe94dd6104eeea6155f2f3f326808564546ed238715dbabad1bd09",
  "sema_ref": "Fermi#6397",
  "sema_stub": "6397",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "composes_with": {
      "estimate": "Estimate#e07e",
      "decompose": "Decompose#5471"
    }
  }
}
```

---

## FirstPrinciples#1a7e

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
  "sema_id": "sema:FirstPrinciples#mh:SHA-256:1a7e7661605fc85fd4fb2d23b6b0d9945746df6f8b71b8fed70ec7db5536812d",
  "sema_ref": "FirstPrinciples#1a7e",
  "sema_stub": "1a7e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "axiom": "Axiom#5012",
      "assumption": "Assumption#efb5",
      "chain_of_thought": "ChainOfThought#380a"
    }
  }
}
```

---

## FrameError#edf5

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
  "sema_id": "sema:FrameError#mh:SHA-256:edf5e1f2d169520949a7b8eb7d3beeee581186922d3fb665430c7ca1711186ac",
  "sema_ref": "FrameError#edf5",
  "sema_stub": "edf5",
  "dependencies": {
    "references": {
      "retry": "Retry#cb3a",
      "compensate": "Compensate#985e",
      "accept_spec": "AcceptSpec#762e"
    }
  }
}
```

---

## Generalize#9684

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
      "Specialize#3ad7"
    ],
    "ring": 2
  },
  "sema_id": "sema:Generalize#mh:SHA-256:96848e5d61a66064f3bab37da24d0c8dbb6056b72964d1f4e0691a6c188fc154",
  "sema_ref": "Generalize#9684",
  "sema_stub": "9684",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "analogy_bridge": "AnalogyBridge#8b52",
      "induction": "Induction#2487",
      "state": "State#4d58"
    }
  }
}
```

---

## GraphOfThought#32b1

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
    "Think#0bb4(DAG#b3f5)"
  ],
  "sema_id": "sema:GraphOfThought#mh:SHA-256:32b11def6b2ac6fae1c72fc35897d54d7aaed7a6985745f682abb8d22805dd54",
  "sema_ref": "GraphOfThought#32b1",
  "sema_stub": "32b1",
  "dependencies": {
    "composes_with": {
      "dag": "DAG#b3f5",
      "think": "Think#0bb4"
    }
  }
}
```

---

## HeuristicSnap#f15c

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
      "ThinSlice#2938"
    ],
    "ring": 2
  },
  "sema_id": "sema:HeuristicSnap#mh:SHA-256:f15ccef72bb0044b92ef26aba87f49751e4b08718121acbe4a1ee79a6e81efa0",
  "sema_ref": "HeuristicSnap#f15c",
  "sema_stub": "f15c",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "cache": "Cache#08ed",
      "problem": "Problem#64d0",
      "budget": "Budget#0934",
      "decision": "Decision#934e",
      "chain_of_thought": "ChainOfThought#380a"
    }
  }
}
```

---

## HumanEmulatorProtocol#9abb

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
  "sema_id": "sema:HumanEmulatorProtocol#mh:SHA-256:9abb378f53cb903054ce383930efaf01c3fb5212240529679cd570770cb30bed",
  "sema_ref": "HumanEmulatorProtocol#9abb",
  "sema_stub": "9abb",
  "dependencies": {
    "composes_with": {
      "conceptual_decomposition": "ConceptualDecomposition#739b",
      "marginal_value_rule": "MarginalValueRule#8660"
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

## Interpret#8ee3

```json
{
  "handle": "Interpret",
  "gloss": "Deriving semantic meaning from raw signal",
  "mechanism": "The cognitive {{think}} act of applying a semantic {{context}} to a raw {{datum}} or {{signal}} to extract {{value}}. Unlike `Translate` (which changes form), Interpret changes the abstraction level, moving from syntax to semantics.",
  "signature": [
    "Think#0bb4(Value#3c5d)"
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
  "sema_ref": "Interpret#8ee3",
  "sema_id": "sema:Interpret#mh:SHA-256:8ee3b4a80afed7f69b8a1ef9c81d89279e5620e781d000ad8a25f32456b72b24",
  "sema_stub": "8ee3",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "yields": {
      "value": "Value#3c5d"
    },
    "composes_with": {
      "think": "Think#0bb4",
      "context": "Context#e88a"
    },
    "accepts": {
      "signal": "Signal#f39d",
      "datum": "Datum#31cf"
    }
  }
}
```

---

## Invert#d39f

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
  "sema_id": "sema:Invert#mh:SHA-256:d39f3691c8c9dc55e50c11b808b5e9480a8522f291341acb499b979fa31a07ba",
  "sema_ref": "Invert#d39f",
  "sema_stub": "d39f",
  "dependencies": {
    "references": {
      "reframe": "Reframe#44c5",
      "problem": "Problem#64d0",
      "state": "State#4d58"
    },
    "accepts": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## LeastToMost#f06a

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
      "RecursionDive#c9eb"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:LeastToMost#mh:SHA-256:f06af399de5e773e510798acc4f6a913d89949078f347bbff1de48f85d17379c",
  "sema_ref": "LeastToMost#f06a",
  "sema_stub": "f06a",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "decompose": "Decompose#5471",
      "solution": "Solution#445c"
    }
  }
}
```

---

## LivedProof#9876

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
  "sema_id": "sema:LivedProof#mh:SHA-256:9876cab516deabc169d1ebe818b9c4816fcad6bfbf1c9b1840c6c4473467224b",
  "sema_ref": "LivedProof#9876",
  "sema_stub": "9876",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "identity": "Identity#626c",
      "dogfood_first": "DogfoodFirst#fb58",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## MetaPrompt#62de

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
  "sema_id": "sema:MetaPrompt#mh:SHA-256:62de6b1b19597765edda0bda74a48fca2248e82fcddb30413c7cc96cdd94bba9",
  "sema_ref": "MetaPrompt#62de",
  "sema_stub": "62de",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Meta#90f4(Prompt#b18a)"
  ],
  "dependencies": {
    "references": {
      "prompt": "Prompt#b18a",
      "task": "Task#b290",
      "meta": "Meta#90f4",
      "prompt_chain": "PromptChain#7f67"
    }
  }
}
```

---

## Parsimony#6d67

```json
{
  "handle": "Parsimony",
  "mechanism": "A {{judge}} of structural necessity (Occam's Razor): does the minimum-complexity form of the artifact still perform its function? Applies wherever a definition, model, design, or decomposition needs to be tested for excess parts. The essential move is ablation \u2014 remove a component and see if the whole collapses \u2014 which works on theories, codebases, system designs, and cognitive schemas alike. Specific rating semantics (binary pass/fail, traffic-light ranges, ordinal ablation scores) belong on descendants or on the composing protocol; Parsimony itself names only the question and the ablation discipline. The signature Judge({{topology}}) reflects that the question operates over structural shape rather than quantitative score; an ablation is itself a topology operation, removing nodes and seeing whether the remaining shape still performs.",
  "invariants": [
    "Necessity: Every component must have a causal link to the outcome."
  ],
  "signature": [
    "Judge#b8d6(Topology#2408)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Parsimony#mh:SHA-256:6d67429f03b5de8222068f834b6214aa5f5e660ea203e8a2123368e25c4fa108",
  "sema_ref": "Parsimony#6d67",
  "sema_stub": "6d67",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "gloss": "Complexity justification via Occams Razor",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## PatternDiscovery#99dd

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
  "sema_id": "sema:PatternDiscovery#mh:SHA-256:99dd1615c53e7355c584a40cc77cba223f4c4617224a6274ed370031c3b49da4",
  "sema_ref": "PatternDiscovery#99dd",
  "sema_stub": "99dd",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "construct_ontology": "ConstructOntology#d5a0",
      "latent_attachment": "LatentAttachment#640e",
      "check": "Check#410e",
      "search": "Search#82c8",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#d183"
    }
  }
}
```

---

## ReAct#05f2

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
      "Reflexion#3b52"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:ReAct#mh:SHA-256:05f2853a62a134412f0ab43bf17f487094c9a206e0c23910a2c865d76d38c097",
  "sema_ref": "ReAct#05f2",
  "sema_stub": "05f2",
  "dependencies": {
    "references": {
      "chain": "Chain#711e",
      "cognitive_bias": "CognitiveBias#4b32",
      "loop": "Loop#a316",
      "agent": "Agent#d183"
    },
    "accepts": {
      "task": "Task#b290"
    },
    "composes_with": {
      "tool_invoke": "ToolInvoke#bd2b"
    }
  }
}
```

---

## Realizable#613e

```json
{
  "handle": "Realizable",
  "gloss": "Evaluates execution feasibility of a plan",
  "mechanism": "A {{judge}} of execution feasibility: can the declared artifact actually be built or enacted in the world it targets, given its stated inputs, {{step}}s, and constraints? Applies wherever a {{plan}} or design must be checked against physical, computational, or institutional reality \u2014 engineering feasibility, policy implementation, software design, research program scoping. The essential move is grounding every {{step}} in a primitive or sub-component that is itself realizable, recursively. Specific rating semantics belong on descendants or on the composing protocol. The signature Judge({{value}}) captures that the question yields a {{value}}-rating of feasibility, not a binary verdict \u2014 'mostly realizable with two unverified links' is a legitimate output.",
  "signature": [
    "Judge#b8d6(Value#3c5d)"
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
  "sema_ref": "Realizable#613e",
  "sema_id": "sema:Realizable#mh:SHA-256:613eaaf6e2e01185adf55ad296d3ad34c8d00d18fb8a29dccd88904f1fc2d798",
  "sema_stub": "613e",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "step": "Step#5f22",
      "value": "Value#3c5d",
      "plan": "Plan#31a7",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## Reason#3067

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
      "ChainOfThought#380a",
      "TreeOfThoughts#fc58"
    ]
  },
  "sema_id": "sema:Reason#mh:SHA-256:306711325c6e3366efe3e3ea371f89379311d36fbd1f64430ede33739601bca8",
  "sema_ref": "Reason#3067",
  "sema_stub": "3067",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "compute_budget": "ComputeBudget#8a42",
      "chain": "Chain#711e",
      "tree": "Tree#a5a3"
    },
    "accepts": {
      "context": "Context#e88a"
    },
    "composes_with": {
      "think": "Think#0bb4"
    }
  }
}
```

---

## RecursionDive#c9eb

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
      "SolverNode#86bb"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:RecursionDive#mh:SHA-256:c9eb4a8c8eb3f7b266fa063748b82777b480986a7619a45df41bdad69d1aa3e5",
  "sema_ref": "RecursionDive#c9eb",
  "sema_stub": "c9eb",
  "dependencies": {
    "references": {
      "solver_node": "SolverNode#86bb",
      "solver_tree": "SolverTree#65f2"
    },
    "composes_with": {
      "decompose": "Decompose#5471"
    }
  }
}
```

---

## RecursiveRootCause#7074

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
      "Bisect#30ea",
      "RecursionDive#c9eb"
    ],
    "ring": 2
  },
  "sema_id": "sema:RecursiveRootCause#mh:SHA-256:7074d06ab2b317d810e688866049a24f8b303099548f033d6edab2d0d16710b9",
  "sema_ref": "RecursiveRootCause#7074",
  "sema_stub": "7074",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "state": "State#4d58"
    }
  }
}
```

---

## Refine#78b7

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
      "PhasedRefinement#11af"
    ]
  },
  "sema_id": "sema:Refine#mh:SHA-256:78b79a62b1ecf8a4a00537a19db4a71e06039fb5bd2792a497b9ccf16fbe8cee",
  "sema_ref": "Refine#78b7",
  "sema_stub": "78b7",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "incongruity": "Incongruity#e98f",
      "critique": "Critique#4e43",
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "act": "Act#dc2d"
    }
  }
}
```

---

## Reflexion#3b52

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
      "EvaluatorOptimizer#2b2e"
    ],
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Reflexion#mh:SHA-256:3b52910b4b2f5413df0ac4ffa6b825cdc8c889157ec09e288643f78a0ddb662f",
  "sema_ref": "Reflexion#3b52",
  "sema_stub": "3b52",
  "dependencies": {
    "references": {
      "plan": "Plan#31a7",
      "goal": "Goal#5f27",
      "scratchpad": "Scratchpad#75bf",
      "critique": "Critique#4e43",
      "outcome": "Outcome#9bf0"
    },
    "accepts": {
      "task": "Task#b290"
    }
  }
}
```

---

## Reframe#44c5

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
    "Perspective shifted."
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
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:Reframe#mh:SHA-256:44c576a9631661094e0b507c6e2ec3a9cfd5761ab217fa2f32628c9dd4c9db88",
  "sema_ref": "Reframe#44c5",
  "sema_stub": "44c5",
  "dependencies": {
    "references": {
      "problem": "Problem#64d0"
    }
  }
}
```

---

## RequestFraming#b776

```json
{
  "handle": "RequestFraming",
  "derived_from": "Interpret#8ee3",
  "gloss": "Clarify intent and constraints before planning",
  "mechanism": "The initial state of workflow orchestration. It performs the act of {{interpret}} by accepting a {{message}} and using {{think}} to {{understand}} the 'real ask' within the given {{context}} before committing resources. The pattern enforces {{context_first}}: no resource commitment is permitted until the frame is resolved. It clarifies constraints, success criteria, and hidden assumptions, producing a {{frame_spec}} artifact. It acts as a semantic firewall against vague or dangerous instructions.",
  "signature": [
    "Think#0bb4(FrameSpec#edff)"
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
      "Reframe#44c5",
      "Decompose#5471"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "sema_id": "sema:RequestFraming#mh:SHA-256:b7764eaf57c8974a34c62c907fe275dacc253ad43313fbd7fcc13eadd2114e3b",
  "sema_ref": "RequestFraming#b776",
  "sema_stub": "b776",
  "dependencies": {
    "yields": {
      "frame_spec": "FrameSpec#edff"
    },
    "references": {
      "context": "Context#e88a",
      "interpret": "Interpret#8ee3",
      "context_first": "ContextFirst#dbb4"
    },
    "accepts": {
      "message": "Message#f767"
    },
    "composes_with": {
      "understand": "Understand#c38c",
      "think": "Think#0bb4"
    }
  }
}
```

---

## SelfConsistency#2068

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
  "sema_ref": "SelfConsistency#2068",
  "sema_id": "sema:SelfConsistency#mh:SHA-256:20688805ed499618cdb8122d200764cc721221b64645cb741d341715416935f6",
  "sema_stub": "2068",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "aggregate": "Aggregate#8c2a"
    }
  }
}
```

---

## SkeletonOfThought#ab3e

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
  "sema_id": "sema:SkeletonOfThought#mh:SHA-256:ab3e787f23cd67466a17c75d6dba6e21056265aaaee67fd8fca561580222a6ac",
  "sema_ref": "SkeletonOfThought#ab3e",
  "sema_stub": "ab3e",
  "signature": [
    "Think#0bb4(Skeleton#c363)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#0bb4",
      "decompose": "Decompose#5471",
      "skeleton": "Skeleton#c363"
    }
  }
}
```

---

## SocraticLoop#bc73

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
  "sema_id": "sema:SocraticLoop#mh:SHA-256:bc73d4cecee28e54d9fecb9ea9e7088ed7a3f73274e2f5dbea9d59473da05091",
  "sema_ref": "SocraticLoop#bc73",
  "sema_stub": "bc73",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "loop": "Loop#a316",
      "prompt": "Prompt#b18a",
      "agent": "Agent#d183",
      "dialectic": "Dialectic#2e3c"
    }
  }
}
```

---

## Specialize#3ad7

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
  "sema_id": "sema:Specialize#mh:SHA-256:3ad7bafd9ba2b8662d5affb01d92bf34d789f239a9427d932a2ecaed3b50ca8c",
  "sema_ref": "Specialize#3ad7",
  "sema_stub": "3ad7",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "check": "Check#410e",
      "generalize": "Generalize#9684",
      "deduction": "Deduction#9c88"
    }
  }
}
```

---

## SteelmanCheck#dd78

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
      "AdversarialSteel#380c"
    ]
  },
  "sema_id": "sema:SteelmanCheck#mh:SHA-256:dd78ffe0d335b88f5a9fa19e8c8c07ba85e87033a4d6687e13e085b456f8f718",
  "sema_ref": "SteelmanCheck#dd78",
  "sema_stub": "dd78",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Check#410e(Robustness#132c)",
    "Critique#4e43(Belief#cafb)"
  ],
  "dependencies": {
    "references": {
      "robustness": "Robustness#132c",
      "cognitive_bias": "CognitiveBias#4b32",
      "compatibility_check": "CompatibilityCheck#3abb",
      "critique": "Critique#4e43",
      "check": "Check#410e",
      "loop": "Loop#a316",
      "decision": "Decision#934e",
      "belief": "Belief#cafb",
      "agent": "Agent#d183"
    }
  }
}
```

---

## StepBack#35ad

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
  "sema_id": "sema:StepBack#mh:SHA-256:35ad31171daed52a64436fc24ac0f61729ca54bb9b5425d341e4763e30a968c9",
  "sema_ref": "StepBack#35ad",
  "sema_stub": "35ad",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#0bb4(Problem#64d0)"
  ],
  "dependencies": {
    "references": {
      "reframe": "Reframe#44c5",
      "think": "Think#0bb4",
      "problem": "Problem#64d0"
    }
  }
}
```

---

## StrategicReading#e058

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
  "sema_ref": "StrategicReading#e058",
  "sema_id": "sema:StrategicReading#mh:SHA-256:e0584ca5f61077a6f7c8d0011c60ddbaf88c7acbc36883a76bc241043c97b898",
  "sema_stub": "e058",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#8a42",
      "cognitive_bias": "CognitiveBias#4b32",
      "tree": "Tree#a5a3",
      "context": "Context#e88a",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Summarize#d9db

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
  "sema_id": "sema:Summarize#mh:SHA-256:d9db027acbfceb679cdf599cdf0475e48cccf3cfdbe1d30b15e4c048ce87ed0c",
  "sema_ref": "Summarize#d9db",
  "sema_stub": "d9db",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "translate": "Translate#edeb",
      "value": "Value#3c5d",
      "compress": "Compress#0967",
      "artifact": "Artifact#6254"
    },
    "yields": {
      "summary": "Summary#f785"
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

## Think#0bb4

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
  "sema_id": "sema:Think#mh:SHA-256:0bb444287b2c8715bd6d7b0aaba25fe44a3ed8551ffa420a4a8d9a6cb8e4585b",
  "sema_ref": "Think#0bb4",
  "sema_stub": "0bb4",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "yields": {
      "datum": "Datum#31cf"
    },
    "accepts": {
      "context": "Context#e88a"
    }
  }
}
```

---

## Translate#edeb

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
  "sema_id": "sema:Translate#mh:SHA-256:edeb5de688448dd2554f9b5c7cabde53b99149b994957661946c4e3983b72f3b",
  "sema_ref": "Translate#edeb",
  "sema_stub": "edeb",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "reversibility": "Reversibility#bf79",
      "protocol": "Protocol#7e1c",
      "interpret": "Interpret#8ee3"
    },
    "accepts": {
      "datum": "Datum#31cf"
    }
  }
}
```

---

## TreeOfThoughts#fc58

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
      "RecursionDive#c9eb"
    ],
    "ring": 2
  },
  "sema_id": "sema:TreeOfThoughts#mh:SHA-256:fc589ab7ea91c0f2672b3e00ab58971df07a67ac61bbdcfc9961412ac276c752",
  "sema_ref": "TreeOfThoughts#fc58",
  "sema_stub": "fc58",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#0bb4(Tree#a5a3)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#0bb4",
      "chain_of_thought": "ChainOfThought#380a",
      "tree": "Tree#a5a3"
    }
  }
}
```

---

## Uncertain#fed9

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
  "sema_id": "sema:Uncertain#mh:SHA-256:fed933930ca0756b73d4c0f56f50b2ef106436b70274b1b85249fab62451924f",
  "sema_ref": "Uncertain#fed9",
  "sema_stub": "fed9",
  "dependencies": {
    "references": {
      "uncertainty_map": "UncertaintyMap#9a55",
      "variable": "Variable#179a",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Understand#c38c

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
  "sema_id": "sema:Understand#mh:SHA-256:c38c510b051d292e7c85629a389e2de521ad95fab03476acabf2fa94774425ac",
  "sema_ref": "Understand#c38c",
  "sema_stub": "c38c",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Think#0bb4(Context#e88a)"
  ],
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "think": "Think#0bb4"
    }
  }
}
```

---

## Verification#9f0c

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
  "sema_ref": "Verification#9f0c",
  "sema_id": "sema:Verification#mh:SHA-256:9f0ca43164b59291b52fa0dedcdbe22ec1394bc91792dffe1d648a53016cd44d",
  "sema_stub": "9f0c",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "dependencies": {
    "references": {
      "artifact": "Artifact#6254",
      "check": "Check#410e",
      "spec": "Spec#68b4"
    }
  }
}
```

---

## WhyClimb#ea4a

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
  "sema_id": "sema:WhyClimb#mh:SHA-256:ea4ab0ff6f1d7205d7f5ba2ef620f611b195f051f9931c436c850012e6bf2279",
  "sema_ref": "WhyClimb#ea4a",
  "sema_stub": "ea4a",
  "sema_layer": "Mind",
  "sema_category": "Reasoning",
  "signature": [
    "Reframe#44c5(Problem#64d0)"
  ],
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "reframe": "Reframe#44c5",
      "recursive_root_cause": "RecursiveRootCause#7074",
      "problem": "Problem#64d0",
      "solution": "Solution#445c"
    }
  }
}
```

---

## AdversarialSteel#380c

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
  "sema_id": "sema:AdversarialSteel#mh:SHA-256:380c8ef1d2fdd4564ab1e91fb4caf7b13eb8b3d13fc243ed3bb4ff93a422dd14",
  "sema_ref": "AdversarialSteel#380c",
  "sema_stub": "380c",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "meta": "Meta#90f4",
      "compatibility_check": "CompatibilityCheck#3abb",
      "system": "System#e314",
      "criteria": "Criteria#ef6b",
      "judge": "Judge#b8d6",
      "agent": "Agent#d183"
    },
    "composes_with": {
      "steelman_check": "SteelmanCheck#dd78"
    }
  }
}
```

---

## Agent#d183

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
  "sema_ref": "Agent#d183",
  "sema_id": "sema:Agent#mh:SHA-256:d1831f418150b85822228d2dadc230f6296058f5db48f0874f9b3736d5a33f81",
  "sema_stub": "d183",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "goal": "Goal#5f27",
      "loop": "Loop#a316",
      "state": "State#4d58",
      "metric": "Metric#17fd",
      "trace": "Trace#2836",
      "identity": "Identity#626c",
      "actor": "Actor#57f6"
    },
    "composes_with": {
      "observe": "Observe#abc0",
      "act": "Act#dc2d",
      "think": "Think#0bb4"
    }
  }
}
```

---

## AnalogyBridge#8b52

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
  "sema_id": "sema:AnalogyBridge#mh:SHA-256:8b52456853af974b4820395247f8375091a9dd8b7785a1571f4ff1dfd8e71ac6",
  "sema_ref": "AnalogyBridge#8b52",
  "sema_stub": "8b52",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "problem": "Problem#64d0",
      "solution": "Solution#445c",
      "agent": "Agent#d183",
      "latent_attachment": "LatentAttachment#640e"
    }
  }
}
```

---

## AntifragileInversion#b9d8

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
  "sema_id": "sema:AntifragileInversion#mh:SHA-256:b9d88841704c19f7286568d24dc6e921c946f725376d995e869dbb8b291e98bb",
  "sema_ref": "AntifragileInversion#b9d8",
  "sema_stub": "b9d8",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "reframe": "Reframe#44c5",
      "system": "System#e314",
      "variable": "Variable#179a",
      "vector": "Vector#c7c4",
      "agent": "Agent#d183"
    }
  }
}
```

---

## BeamSearch#cb0e

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
  "sema_id": "sema:BeamSearch#mh:SHA-256:cb0ed1f92a4b218498a4a6661f91fd1caa832d28d7ac2424166a159d3667c395",
  "sema_ref": "BeamSearch#cb0e",
  "sema_stub": "cb0e",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "solver_node": "SolverNode#86bb",
      "select": "Select#15c2",
      "queue": "Queue#7ca9",
      "rank": "Rank#7a76"
    }
  }
}
```

---

## Bubble#6d71

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
  "sema_id": "sema:Bubble#mh:SHA-256:6d710acdf85e4ba84fc97d49c2f5c4f605c7224b2434e666fac4e483944b7923",
  "sema_ref": "Bubble#6d71",
  "sema_stub": "6d71",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "constraint_first": "ConstraintFirst#c7cb",
      "work": "Work#bc56",
      "state": "State#4d58"
    }
  }
}
```

---

## Build#8143

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
      "Simulation#398f",
      "DogfoodFirst#fb58",
      "SacrificialProbe#d2d4"
    ],
    "ring": 1
  },
  "sema_id": "sema:Build#mh:SHA-256:8143240ba549ce730ef09c35198e11ea5cd9df8512b253de8958f16f5a098c0d",
  "sema_ref": "Build#8143",
  "sema_stub": "8143",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Act#dc2d(Artifact#6254)"
  ],
  "dependencies": {
    "accepts": {
      "spec": "Spec#68b4"
    },
    "references": {
      "plan": "Plan#31a7",
      "value": "Value#3c5d",
      "act": "Act#dc2d",
      "prototype": "Prototype#ff18"
    },
    "yields": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## CapacityPressure#bc5a

```json
{
  "handle": "CapacityPressure",
  "mechanism": "A regularization pattern that forces abstraction by artificially constraining resources (bandwidth, memory, parameter count, or time). By creating a bottleneck where Capacity < Information, the agent is compelled to compress the signal, discarding noise and memorized details in favor of high-level concepts and generalizations. It artificially tightens the {{budget}}, forcing the agent to employ {{generalize}}, {{concept_blend}}, and {{context_compress}} to fit the signal within the bottleneck.",
  "gloss": "Forcing abstraction via resource starvation",
  "failure_modes": [
    "Collapse: {{constraint}} is too tight; signal is lost entirely (underfitting).",
    "Adversarial Encoding: {{agent}} finds a way to 'zip' noise rather than abstracting (violating the spirit of the constraint).",
    "False Abstraction: {{agent}} hallucinates simple rules that don't actually exist to satisfy the budget."
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
      "range": "{Compute, Memory, Attention, Budget#0934}",
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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:CapacityPressure#mh:SHA-256:bc5a10d2e32765bf39bd050b927380180baa94455c3db01607a4f2b5ff142c4f",
  "sema_ref": "CapacityPressure#bc5a",
  "sema_stub": "bc5a",
  "dependencies": {
    "references": {
      "concept_blend": "ConceptBlend#2894",
      "constraint": "Constraint#87fe",
      "context_compress": "ContextCompress#4845",
      "budget": "Budget#0934",
      "generalize": "Generalize#9684",
      "agent": "Agent#d183"
    }
  }
}
```

---

## CommitmentDevice#3aeb

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
  "sema_id": "sema:CommitmentDevice#mh:SHA-256:3aeb7bb718ebf906d99e71ddf4008b773fed718ac07d14443961abec0ad06602",
  "sema_ref": "CommitmentDevice#3aeb",
  "sema_stub": "3aeb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
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
      "oath_bind": "OathBind#af30",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Compose#389f

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
    "Subproblem solutions available.",
    "Interface contracts defined.",
    "Composition order known if order-dependent."
  ],
  "postconditions": [
    "Combined solution satisfies original problem.",
    "No interface violations.",
    "Emergent interactions handled."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Combine#5a44(PromptChain#7f67)"
  ],
  "sema_id": "sema:Compose#mh:SHA-256:389f4d23861b1382b3d046c9193fcae322a33407ee7130564a9e971192de2bf4",
  "sema_ref": "Compose#389f",
  "sema_stub": "389f",
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "combine": "Combine#5a44",
      "prompt_chain": "PromptChain#7f67"
    }
  }
}
```

---

## ComputeBudget#8a42

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
      "OptimalStop#4dee",
      "Satisfice#64ac",
      "TimeboxThink#9e1b"
    ]
  },
  "sema_ref": "ComputeBudget#8a42",
  "sema_id": "sema:ComputeBudget#mh:SHA-256:8a428848cb249cd1f79c8b83f1eba3afc4ca6efab3067ffd9fc080691c915317",
  "sema_stub": "8a42",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "gate": "Gate#02f6",
      "task": "Task#b290",
      "value": "Value#3c5d",
      "budget": "Budget#0934"
    }
  }
}
```

---

## ConceptBlend#2894

```json
{
  "handle": "ConceptBlend",
  "mechanism": "Forcing the merger of two unrelated graph nodes to find a valid semantic path. Unlike analogy (A is like B), blending creates C (A + B). It extends {{analogy_bridge}} by not just mapping A to B, but fusing them to create C.",
  "gloss": "Atomic fusion of two unrelated concepts into a novel third",
  "invariants": [
    "Orthogonality: Inputs must be semantically distant (> threshold {{distance}})",
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
  "sema_id": "sema:ConceptBlend#mh:SHA-256:289473f83c17f1f4938c68dd5dd07d3c4a96b1069897e58b40bb46cc3981f036",
  "sema_ref": "ConceptBlend#2894",
  "sema_stub": "2894",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "analogy_bridge": "AnalogyBridge#8b52",
      "realizable": "Realizable#613e",
      "tri_gate": "TriGate#66aa",
      "distance": "Distance#3e1e"
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
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe"
    }
  }
}
```

---

## ContingencyPlan#2a5b

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
  "sema_id": "sema:ContingencyPlan#mh:SHA-256:2a5b4ec5cd06cee22dc1929c0b50ee8a6a4d29cdb3be05fe2a9cf762d2dbfbd2",
  "sema_ref": "ContingencyPlan#2a5b",
  "sema_stub": "2a5b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "retry": "Retry#cb3a",
      "plan": "Plan#31a7"
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
  "sema_category": "Strategy#a0af"
}
```

---

## CreativeBlend#c564

```json
{
  "handle": "CreativeBlend",
  "derived_from": "Creative#5574",
  "gloss": "Full creative pipeline: ConceptBlend + NoiseInjection with novelty/value gates",
  "signature": [
    "Strategy#a0af(Artifact#6254)"
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
  "sema_ref": "CreativeBlend#c564",
  "sema_id": "sema:CreativeBlend#mh:SHA-256:c5640a318323ba9dd58c467aa97284a62736cedffd86da2846dae13f19ab5040",
  "sema_stub": "c564",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "noise_injection": "NoiseInjection#2131",
      "value": "Value#3c5d",
      "novelty": "Novelty#53a0",
      "strategy": "Strategy#a0af"
    },
    "composes_with": {
      "concept_blend": "ConceptBlend#2894",
      "check": "Check#410e"
    },
    "accepts": {
      "context": "Context#e88a"
    },
    "yields": {
      "artifact": "Artifact#6254"
    }
  }
}
```

---

## Crystallize#f680

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
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Crystallize#mh:SHA-256:f6807d6a8349b37b11341537f5c1c6f88f8743b2ecc175ad9cb52c1fd72b7646",
  "sema_ref": "Crystallize#f680",
  "sema_stub": "f680",
  "dependencies": {
    "references": {
      "constitution": "Constitution#d2e5",
      "resonate": "Resonate#155f",
      "entropy_pump": "EntropyPump#ed3b",
      "dampen": "Dampen#3f0c",
      "transition": "Transition#072d",
      "agent": "Agent#d183",
      "state": "State#4d58",
      "decay": "Decay#1e8b"
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
  "sema_category": "Strategy#a0af"
}
```

---

## Defer#2500

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
  "sema_id": "sema:Defer#mh:SHA-256:25009267741451774e6343fa3d6fa335f8cb19758f87ded652f42653c9b6a45d",
  "sema_ref": "Defer#2500",
  "sema_stub": "2500",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "prioritize": "Prioritize#420e",
      "context": "Context#e88a",
      "state": "State#4d58",
      "decision": "Decision#934e"
    }
  }
}
```

---

## DepthGovernor#8f06

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
  "sema_id": "sema:DepthGovernor#mh:SHA-256:8f068793431f9eb8c95bc54382e6d43012a027c4fda009a5621b0c74ed121eae",
  "sema_ref": "DepthGovernor#8f06",
  "sema_stub": "8f06",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "plan": "Plan#31a7",
      "problem": "Problem#64d0",
      "recursion_dive": "RecursionDive#c9eb",
      "loop": "Loop#a316",
      "decompose": "Decompose#5471",
      "agent": "Agent#d183"
    }
  }
}
```

---

## DesignArchitect#1613

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
  "sema_ref": "DesignArchitect#1613",
  "sema_id": "sema:DesignArchitect#mh:SHA-256:16137ca2e38512f89eb270435556f8959b160eb5743ad3a84756984459a368d5",
  "sema_stub": "1613",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#c3ed"
    },
    "composes_with": {
      "translate": "Translate#edeb",
      "pre_mortem": "PreMortem#8ca0",
      "steelman_check": "SteelmanCheck#dd78",
      "strategy": "Strategy#a0af",
      "summarize": "Summarize#d9db"
    }
  }
}
```

---

## DiscoveryProtocol#b8aa

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:DiscoveryProtocol#mh:SHA-256:b8aa614c35ac5d1ff90dacde609548d606f049ecb65f4ace17fcb23d15e99a44",
  "sema_ref": "DiscoveryProtocol#b8aa",
  "sema_stub": "b8aa",
  "dependencies": {
    "composes_with": {
      "synthesis": "Synthesis#26b9",
      "conceptual_decomposition": "ConceptualDecomposition#739b"
    },
    "references": {
      "discover": "Discover#aa70"
    }
  }
}
```

---

## DogfoodFirst#fb58

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
  "sema_id": "sema:DogfoodFirst#mh:SHA-256:fb58131dec88f464ae501ce7db7d8973366afa8d415d9616fbd7e17c9adc1aa4",
  "sema_ref": "DogfoodFirst#fb58",
  "sema_stub": "fb58",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "canary": "Canary#86d6",
      "reflexion": "Reflexion#3b52",
      "gate": "Gate#02f6",
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## EmpathySim#57cb

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
      "MentalSim#b817"
    ],
    "ring": 2
  },
  "sema_id": "sema:EmpathySim#mh:SHA-256:57cb59996c169e88a9ac02a23ca4e3450029641935108b0c88e524fd349d6dc2",
  "sema_ref": "EmpathySim#57cb",
  "sema_stub": "57cb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "accepts": {
      "agent": "Agent#d183"
    },
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "agent_sandbox": "AgentSandbox#1838",
      "budget": "Budget#0934",
      "context": "Context#e88a",
      "state": "State#4d58",
      "simulation": "Simulation#398f",
      "agent": "Agent#d183"
    }
  }
}
```

---

## EmpiricalTest#9ef5

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
  "sema_id": "sema:EmpiricalTest#mh:SHA-256:9ef5dbf1d5ccc9ae742c53f93d0e2509191966a70b412ecd54b4e9a97f470ef8",
  "sema_ref": "EmpiricalTest#9ef5",
  "sema_stub": "9ef5",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "falsification": "Falsification#0215",
      "validate": "Validate#aebf"
    }
  }
}
```

---

## EpistemicROI#9e4f

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:EpistemicROI#mh:SHA-256:9e4f16a3fbd1040bce8feddba74491615b1b721324b070846317f26a871491f2",
  "sema_ref": "EpistemicROI#9e4f",
  "sema_stub": "9e4f",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#8a42",
      "task": "Task#b290",
      "cognitive_bias": "CognitiveBias#4b32",
      "result": "Result#f29e",
      "value": "Value#3c5d",
      "experiment": "Experiment#a816",
      "act": "Act#dc2d",
      "decision": "Decision#934e",
      "outcome": "Outcome#9bf0"
    }
  }
}
```

---

## EventReact#6f08

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
  "sema_id": "sema:EventReact#mh:SHA-256:6f083d07d58832607b6c81b68e78d6f6f46d62aee2875453cf3d11ef9eebcf24",
  "sema_ref": "EventReact#6f08",
  "sema_stub": "6f08",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "re_act": "ReAct#05f2",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Experiment#a816

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
      "HypothesisLadder#71cc"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Experiment#mh:SHA-256:a816fe78b29e05515da63e5ae977e266fbfc265defd2ceb555c6ed0a4e45aafe",
  "sema_ref": "Experiment#a816",
  "sema_stub": "a816",
  "dependencies": {
    "references": {
      "verification": "Verification#9f0c",
      "protocol": "Protocol#7e1c"
    },
    "yields": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## ExploreExploit#c937

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
  "sema_id": "sema:ExploreExploit#mh:SHA-256:c9379413b64d56ae8342ed56a9f67a4b7f09b3e6f13886690332b58b214913aa",
  "sema_ref": "ExploreExploit#c937",
  "sema_stub": "c937",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "budget": "Budget#0934"
    }
  }
}
```

---

## Falsification#0215

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
      "HypothesisLadder#71cc"
    ]
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Falsification#mh:SHA-256:021560b40fc737a96a5b716a3bac434acea9b6a1e0debe6f010740bb915aa376",
  "sema_ref": "Falsification#0215",
  "sema_stub": "0215",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#ffa7",
      "observe": "Observe#abc0",
      "incongruity": "Incongruity#e98f"
    }
  }
}
```

---

## FractalIntelligence#74f8

```json
{
  "handle": "FractalIntelligence",
  "mechanism": "Expansion of cognitive capability through {{conceptual_decomposition}}: a concept (problem or task) is broken into contract-bound sub-concepts, each governed by the same five-surface Solver Contract (Manifest, Execute, Consult, Verify, Feedback) that governs the parent. A few {{agent}}s can assign solver roles to themselves and perform lightweight fractal intelligence for a specific problem \u2014 the resulting structure may persist as a reusable pattern that improves through use, or may be torn down at completion; both are legitimate modes. The unified {{system}} of scalable cognition uses {{reason}} to orchestrate fractal expansion within the {{universal_solver_tree}}. A {{problem_framer}} initiates by formulating a high-level {{strategy}} before assigning a {{polymorphic_solver}} to a {{task}}; the solver executes a {{recursion_dive}} to spawn child nodes, each applying {{specialize}} with {{localized_learning}}, while {{experience_sharding}} and {{synthesis}} preserve global coherence. {{state_snapshot}} provides crash recovery for persistent instances. {{marginal_value_rule}} governs recursion depth. On failure, {{reframe}} restructures the tree.",
  "gloss": "Expansion of cognitive capability through recursive decomposition of concepts into contract-bounded sub-concepts",
  "invariants": [
    "Fractal Self-Similarity: The process at the Root is identical to the process at the Leaf.",
    "Bounded Expansion: Recursion is limited by Economic constraints (Marginal Value).",
    "Memory {{conservation}}: Specialization must not result in the loss of global context."
  ],
  "signature": [
    "System#e314(Reason#3067)"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:FractalIntelligence#mh:SHA-256:74f8a9510d3c2d52e07d3405d3143271eb2ef86fb8fbef8a5a679f89720aee9e",
  "sema_ref": "FractalIntelligence#74f8",
  "sema_stub": "74f8",
  "dependencies": {
    "references": {
      "conservation": "Conservation#d63a",
      "strategy": "Strategy#a0af",
      "task": "Task#b290",
      "universal_solver_tree": "UniversalSolverTree#2c55",
      "specialize": "Specialize#3ad7",
      "system": "System#e314",
      "experience_sharding": "ExperienceSharding#4158",
      "agent": "Agent#d183"
    },
    "composes_with": {
      "synthesis": "Synthesis#26b9",
      "state_snapshot": "StateSnapshot#5a11",
      "marginal_value_rule": "MarginalValueRule#8660",
      "problem_framer": "ProblemFramer#a3fc",
      "conceptual_decomposition": "ConceptualDecomposition#739b",
      "polymorphic_solver": "PolymorphicSolver#bbe4",
      "localized_learning": "LocalizedLearning#eb5a",
      "reframe": "Reframe#44c5",
      "recursion_dive": "RecursionDive#c9eb",
      "reason": "Reason#3067"
    }
  }
}
```

---

## HypothesisEngine#8dec

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:HypothesisEngine#mh:SHA-256:8decc37b70580305007fec7ebb8b589a0df8ccd84aeaebb025d0ca9180c9c99a",
  "sema_ref": "HypothesisEngine#8dec",
  "sema_stub": "8dec",
  "dependencies": {
    "references": {
      "hypothesis": "Hypothesis#ffa7",
      "validate": "Validate#aebf",
      "check": "Check#410e",
      "stigmergy": "Stigmergy#53d4",
      "simulation": "Simulation#398f",
      "trace": "Trace#2836",
      "discover": "Discover#aa70"
    }
  }
}
```

---

## HypothesisLadder#71cc

```json
{
  "handle": "HypothesisLadder",
  "mechanism": "The agent explicitly lists its current hypotheses about the world state and assigns probabilities. As new data arrives, it updates these probabilities using {{bayes_update}}. It acts on the highest-probability {{hypothesis}} but keeps others alive. It structures {{abduction}} into falsifiable rungs, climbing to higher certainty only when an {{experiment}} validates the current level.",
  "gloss": "Bayesian belief updating via falsification rungs",
  "failure_modes": [
    "Clinging to low-probability priors."
  ],
  "invariants": [
    "Ascension Rule: Cannot move to {{hypothesis}}(N+1) until {{hypothesis}}(N) is validated by evidence.",
    "Exclusivity: Hypotheses at the same rung must be mutually exclusive (required for Bayesian probability assignment).",
    "Falsifiability: Each rung must have a testable disprove condition."
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
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:HypothesisLadder#mh:SHA-256:71cca12525a69cf20fc8258dd019369788c2077988629e0b2b39e7539b20eb02",
  "sema_ref": "HypothesisLadder#71cc",
  "sema_stub": "71cc",
  "dependencies": {
    "references": {
      "abduction": "Abduction#f9ea",
      "hypothesis": "Hypothesis#ffa7",
      "bayes_update": "BayesUpdate#ee85"
    },
    "composes_with": {
      "experiment": "Experiment#a816"
    }
  }
}
```

---

## Jester#9bbe

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
  "sema_id": "sema:Jester#mh:SHA-256:9bbe675454c8b3ca630c09cd2514230592998416834877ad224b9aaae128d61c",
  "sema_ref": "Jester#9bbe",
  "sema_stub": "9bbe",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "incongruity": "Incongruity#e98f",
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
  "sema_category": "Strategy#a0af"
}
```

---

## LatentWander#53fb

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:LatentWander#mh:SHA-256:53fb756ee4d848d14c25d454642e49f50616bab2d704d03a8daf4e1487f99264",
  "sema_ref": "LatentWander#53fb",
  "sema_stub": "53fb",
  "dependencies": {
    "yields": {
      "analogy_bridge": "AnalogyBridge#8b52"
    },
    "references": {
      "latent_attachment": "LatentAttachment#640e",
      "silence": "Silence#dd79",
      "concept_blend": "ConceptBlend#2894"
    }
  }
}
```

---

## LateralOptimization#61e2

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
      "AnalogyBridge#8b52"
    ],
    "ring": 1
  },
  "sema_id": "sema:LateralOptimization#mh:SHA-256:61e2ab651546dcb1b62465c39dcd0f32bcf2a82fecb2b60ffd06c1a2a2638ff7",
  "sema_ref": "LateralOptimization#61e2",
  "sema_stub": "61e2",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Think#0bb4(Creative#5574)",
    "Optimize#b98b(Global#803d)"
  ],
  "dependencies": {
    "references": {
      "think": "Think#0bb4",
      "creative": "Creative#5574",
      "system": "System#e314",
      "solution": "Solution#445c",
      "global": "Global#803d"
    },
    "composes_with": {
      "translate": "Translate#edeb",
      "optimize": "Optimize#b98b",
      "reframe": "Reframe#44c5"
    }
  }
}
```

---

## ManifestPlanning#b9ad

```json
{
  "handle": "ManifestPlanning",
  "derived_from": "Plan#31a7",
  "gloss": "Transform FrameSpec into ExecutionManifest via optimization",
  "mechanism": "The architectural phase of workflow orchestration. It produces a structured {{plan}} by performing {{think}} to transform a {{frame_spec}} into a runnable {{execution_manifest}}. This process must {{optimize}} the step sequence for resource feasibility and generate a strict 'Definition of Done'.",
  "signature": [
    "Think#0bb4(ExecutionManifest#6cf5)"
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
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:ManifestPlanning#mh:SHA-256:b9adf897bad7746e76b4833754949a7176147a62dae927b38b3d281eb94cfb8d",
  "sema_ref": "ManifestPlanning#b9ad",
  "sema_stub": "b9ad",
  "dependencies": {
    "yields": {
      "execution_manifest": "ExecutionManifest#6cf5"
    },
    "references": {
      "plan": "Plan#31a7"
    },
    "composes_with": {
      "optimize": "Optimize#b98b",
      "think": "Think#0bb4"
    },
    "accepts": {
      "frame_spec": "FrameSpec#edff"
    }
  }
}
```

---

## MarginalValueRule#8660

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
  "sema_id": "sema:MarginalValueRule#mh:SHA-256:86602ffacd78c14b36209d317ab0684fefd181cf0963a0c4f1abb6e3e83591c0",
  "sema_ref": "MarginalValueRule#8660",
  "sema_stub": "8660",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Budget#0934(RecursionDive#c9eb)"
  ],
  "dependencies": {
    "references": {
      "recursion_dive": "RecursionDive#c9eb",
      "estimate": "Estimate#e07e",
      "budget": "Budget#0934"
    }
  }
}
```

---

## MentalSim#b817

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
      "ProphetFanOut#c8d0"
    ],
    "ring": 2
  },
  "sema_id": "sema:MentalSim#mh:SHA-256:b81797fef55020eda55aa383f5c0ae59c06272df0deb5e891aace630d75569d5",
  "sema_ref": "MentalSim#b817",
  "sema_stub": "b817",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "heuristic_snap": "HeuristicSnap#f15c",
      "agent_sandbox": "AgentSandbox#1838",
      "system": "System#e314",
      "state": "State#4d58",
      "simulation": "Simulation#398f",
      "deep": "Deep#89f0",
      "agent": "Agent#d183"
    }
  }
}
```

---

## MetaCheck#c660

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
  "sema_id": "sema:MetaCheck#mh:SHA-256:c660a055a802bee10abbfb87cb9c97e8dd23eda0363834f49587041d45d2a27d",
  "sema_ref": "MetaCheck#c660",
  "sema_stub": "c660",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Meta#90f4(Check#410e)"
  ],
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "audit": "Audit#6888",
      "meta": "Meta#90f4",
      "reflexion": "Reflexion#3b52"
    }
  }
}
```

---

## MetaProtocols#e1f5

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:MetaProtocols#mh:SHA-256:e1f5dc5dfd1b360706933d318ac8210e7069ce696891b774fa85bc367f0fc767",
  "sema_ref": "MetaProtocols#e1f5",
  "sema_stub": "e1f5",
  "dependencies": {
    "references": {
      "reframe": "Reframe#44c5",
      "pathway_memory": "PathwayMemory#7899"
    },
    "composes_with": {
      "marginal_value_rule": "MarginalValueRule#8660"
    }
  }
}
```

---

## NoiseInjection#2131

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
  "sema_id": "sema:NoiseInjection#mh:SHA-256:2131a366290fec6ee5756ff5c6fe3466df4bfb96fd013b34d825d46d156c02c1",
  "sema_ref": "NoiseInjection#2131",
  "sema_stub": "2131",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "noise": "Noise#3d9a",
      "card": "Card#f63d",
      "context": "Context#e88a",
      "strategy": "Strategy#a0af",
      "agent": "Agent#d183",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Novelty#53a0

```json
{
  "handle": "Novelty",
  "mechanism": "A {{judge}} of structural distinctness: does this artifact introduce a genuinely new mechanism relative to a reference knowledge base, or is it a rename or incremental variation of something already there? Applies wherever originality needs to be separated from surface variety \u2014 scientific contribution, design proposals, creative work, trademark/patent review, pattern minting. The essential move is a structural comparison against the incumbent set rather than a similarity score on surface tokens. Specific rating semantics (binary, traffic-light, continuous distance) belong on descendants or on the composing protocol. The signature Judge({{value}}) places the result on a {{value}}-scale (how novel is this, on a measurable axis) rather than returning a binary yes/no.",
  "invariants": [
    "Orthogonality: High novelty requires low embedding similarity to nearest neighbor."
  ],
  "signature": [
    "Judge#b8d6(Value#3c5d)"
  ],
  "gloss": "Evaluates structural distinctness",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 1
  },
  "sema_id": "sema:Novelty#mh:SHA-256:53a0735aae257b366e75eb95455674504363a24332c4e21327007fd359e2dc11",
  "sema_ref": "Novelty#53a0",
  "sema_stub": "53a0",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "judge": "Judge#b8d6"
    }
  }
}
```

---

## OODA#a143

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
      "ReAct#05f2",
      "SocraticLoop#bc73",
      "BoydCycle"
    ],
    "ring": 1
  },
  "sema_id": "sema:OODA#mh:SHA-256:a143b7d5df946d3d1c05847e30ccbfdbfe64b8fbb9a63f06406bae9bda7e78fc",
  "sema_ref": "OODA#a143",
  "sema_stub": "a143",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "signature": [
    "Agent#d183(Loop#a316)",
    "Think#0bb4(Strategy#a0af)"
  ],
  "dependencies": {
    "references": {
      "strategy": "Strategy#a0af",
      "loop": "Loop#a316",
      "context_first": "ContextFirst#dbb4",
      "state": "State#4d58",
      "agent": "Agent#d183"
    },
    "composes_with": {
      "belief": "Belief#cafb",
      "observe": "Observe#abc0",
      "act": "Act#dc2d",
      "select": "Select#15c2",
      "think": "Think#0bb4",
      "context": "Context#e88a"
    }
  }
}
```

---

## OpportunityCost#6b5f

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
  "sema_ref": "OpportunityCost#6b5f",
  "sema_id": "sema:OpportunityCost#mh:SHA-256:6b5f9f3742a34add470e56df30ff462bfdf6c8830705a371aa43a73afcee8585",
  "sema_stub": "6b5f",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "budget": "Budget#0934"
    }
  }
}
```

---

## OptimalStop#4dee

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
  "sema_id": "sema:OptimalStop#mh:SHA-256:4deea2f266dbff3345db2878c8acfc0b75067a9aa1b38d9007dd82690a5979e5",
  "sema_ref": "OptimalStop#4dee",
  "sema_stub": "4dee",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#8a42"
    }
  }
}
```

---

## Optimize#b98b

```json
{
  "handle": "Optimize",
  "mechanism": "The iterative process of adjusting parameters or structure to maximize (or minimize) a specific Objective Function defined by a {{metric}}. It involves generating candidate {{solution}}s, evaluating them against the metric, and selecting the best. It can be Local ({{gradient}} Descent) or {{global}} (Evolutionary).",
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
      "EvaluatorOptimizer#2b2e",
      "RegretMinimization#a15f",
      "ParetoFront#c1fb"
    ],
    "ring": 1
  },
  "sema_id": "sema:Optimize#mh:SHA-256:b98b1c33709a1fdc9ba8ab845c951614766081a0a83821acf0f102eb55f85327",
  "sema_ref": "Optimize#b98b",
  "sema_stub": "b98b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "global": "Global#803d",
      "gradient": "Gradient#480b",
      "metric": "Metric#17fd"
    },
    "accepts": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## PURE#9f3f

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:PURE#mh:SHA-256:9f3f6c4e6d7d631238b154db544ca97441debc2263883dca86afc20eebbeae30",
  "sema_ref": "PURE#9f3f",
  "sema_stub": "9f3f",
  "dependencies": {
    "composes_with": {
      "expansive": "Expansive#bfaa",
      "realizable": "Realizable#613e",
      "parsimony": "Parsimony#6d67",
      "novelty": "Novelty#53a0"
    }
  }
}
```

---

## PUREBrainstorming#d632

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
  "sema_ref": "PUREBrainstorming#d632",
  "sema_id": "sema:PUREBrainstorming#mh:SHA-256:d632371983c65d0ee02d84e9466073e4e63ba1fab91394bd8c5625b1eb243df9",
  "sema_stub": "d632",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "yields": {
      "mechanistic_design_proposal": "MechanisticDesignProposal#c3ed"
    },
    "composes_with": {
      "pure_check": "PURECheck#21dc",
      "pure_optimization": "PUREOptimization#e44f"
    },
    "references": {
      "pure": "PURE#9f3f"
    }
  }
}
```

---

## PURECheck#21dc

```json
{
  "handle": "PURECheck",
  "mechanism": "The PURE triage specialization of the {{p_u_r_e}} framework: the canonical Exploration {{protocol}}. It is a {{layered_check}} that orchestrates a sequential triage using four instances of {{tri_gate}}: (1) {{tri_gate}}({{parsimony}}) (2) {{tri_gate}}({{novelty}}) (3) {{tri_gate}}({{realizable}}) (4) {{tri_gate}}({{expansive}}). Enforces the conjunctive rule: 'Explore iff NO gate is Red'. Yellow outputs accumulate as Technical Debt (Smallest Lift tasks) in the final {{solution}}.",
  "gloss": "The PURE Triage Protocol (Parsimonious, Unique/Novel, Realizable, Expansive)",
  "signature": [
    "Protocol#7e1c(Solution#445c)"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 1
  },
  "sema_id": "sema:PURECheck#mh:SHA-256:21dc65c05c76d2496a4627961aa447b2f2af33302f3ac7b5e31a3daf59c04ad2",
  "sema_ref": "PURECheck#21dc",
  "sema_stub": "21dc",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "layered_check": "LayeredCheck#0dbc",
      "parsimony": "Parsimony#6d67",
      "realizable": "Realizable#613e",
      "tri_gate": "TriGate#66aa",
      "expansive": "Expansive#bfaa",
      "novelty": "Novelty#53a0",
      "pure": "PURE#9f3f",
      "solution": "Solution#445c"
    },
    "composes_with": {
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## PUREOptimization#e44f

```json
{
  "handle": "PUREOptimization",
  "gloss": "Deeply optimizing a solution across PURE dimensions",
  "mechanism": "The PURE optimization specialization of the {{p_u_r_e}} framework: a multi-agent {{optimize}} strategy. It accepts a candidate {{solution}} that has already passed the {{pure_check}}. It {{decompose}}s the solution into four parallel streams, assigning a specialized {{polymorphic_solver}} to maximize each PURE metric: {{parsimony}} (Efficiency), {{novelty}} (Uniqueness), {{realizable}} (Feasibility), and {{expansive}} (Impact). The results are re-integrated via {{synthesis}} to find the {{pareto_front}} among competing improvements.",
  "signature": [
    "Optimize#b98b(Solution#445c)"
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
      "EvaluatorOptimizer#2b2e",
      "LateralOptimization#61e2"
    ]
  },
  "sema_ref": "PUREOptimization#e44f",
  "sema_id": "sema:PUREOptimization#mh:SHA-256:e44f694e0f5b2e503822747bafcda8eebaf770594a07991961c235b24ac34701",
  "sema_stub": "e44f",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "pure_check": "PURECheck#21dc",
      "parsimony": "Parsimony#6d67",
      "realizable": "Realizable#613e",
      "expansive": "Expansive#bfaa",
      "novelty": "Novelty#53a0",
      "pure": "PURE#9f3f",
      "pareto_front": "ParetoFront#c1fb"
    },
    "composes_with": {
      "synthesis": "Synthesis#26b9",
      "optimize": "Optimize#b98b",
      "decompose": "Decompose#5471",
      "polymorphic_solver": "PolymorphicSolver#bbe4"
    },
    "accepts": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## Parallelize#b943

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Parallelize#mh:SHA-256:b9430cfb73cdaeef11b79f3619c8dcdf4c1f418e6986d1fb1e249b92dd1efae8",
  "sema_ref": "Parallelize#b943",
  "sema_stub": "b943",
  "signature": [
    "Parallel#3181(Task#b290)",
    "Aggregate#8c2a(Result#f29e)"
  ],
  "dependencies": {
    "composes_with": {
      "aggregate": "Aggregate#8c2a"
    },
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "result": "Result#f29e",
      "parallel": "Parallel#3181",
      "mode": "Mode#3df1",
      "strategy": "Strategy#a0af"
    },
    "accepts": {
      "task": "Task#b290"
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
      "OpportunityCost#6b5f",
      "Satisfice#64ac"
    ],
    "ring": 2
  },
  "sema_id": "sema:ParetoFront#mh:SHA-256:c1fb20ece1fc1f524f90d03106f76a4fcbb7107640a6258153bb273177d654be",
  "sema_ref": "ParetoFront#c1fb",
  "sema_stub": "c1fb",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "rank": "Rank#7a76",
      "state": "State#4d58"
    },
    "accepts": {
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## PerspectiveEnsemble#e277

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
  "sema_id": "sema:PerspectiveEnsemble#mh:SHA-256:e277b5ebcdc10690124359ad976ab905abd5b39c51488d1eca2614b5b7739c64",
  "sema_ref": "PerspectiveEnsemble#e277",
  "sema_stub": "e277",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "chain": "Chain#711e",
      "aggregate": "Aggregate#8c2a",
      "problem": "Problem#64d0",
      "context": "Context#e88a",
      "synthesis": "Synthesis#26b9",
      "steelman_check": "SteelmanCheck#dd78",
      "agent": "Agent#d183"
    }
  }
}
```

---

## PolymorphicSolver#bbe4

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
  "sema_category": "Strategy#a0af",
  "invariants": [
    "Polymorphism: External Runtime treats all Solvers identically via this Interface.",
    "Recursion: Solver must accept sub-tasks via the same Interface it exposes."
  ],
  "failure_modes": [
    "Interface Non-Compliance: Solver fails to implement one of the 5 mandatory endpoints.",
    "Manifest Drift: Capabilities declared in Manifest do not match runtime behavior."
  ],
  "derived_from": "Solver#4ed4",
  "sema_id": "sema:PolymorphicSolver#mh:SHA-256:bbe4e13d44f051dd0cecd2ce4ea9a1dc2f9f16d13817a1fe13704e4cef3fcef7",
  "sema_ref": "PolymorphicSolver#bbe4",
  "sema_stub": "bbe4",
  "dependencies": {
    "references": {
      "universal_solver_tree": "UniversalSolverTree#2c55",
      "performance_signal": "PerformanceSignal#d211",
      "solver_node": "SolverNode#86bb",
      "validate": "Validate#aebf",
      "card": "Card#f63d"
    },
    "accepts": {
      "task": "Task#b290"
    },
    "composes_with": {
      "reflexion": "Reflexion#3b52",
      "tool_invoke": "ToolInvoke#bd2b",
      "socratic_loop": "SocraticLoop#bc73",
      "pathway_memory": "PathwayMemory#7899",
      "compute_budget": "ComputeBudget#8a42",
      "reason": "Reason#3067"
    },
    "yields": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## PreMortem#8ca0

```json
{
  "handle": "PreMortem",
  "mechanism": "Prospective Hindsight: Before executing {{task}} ({{plan}}), assume it has failed catastrophically. Ask: \"What went wrong?\" Generate failure scenarios without defensiveness. For each plausible failure, add mitigation to plan or reconsider approach entirely. It invokes {{recursive_root_cause}} on a hypothetical failure state, often employing {{steelman_check}} to ensure the disaster scenario is plausible.",
  "gloss": "Simulating failure to identify hidden risks",
  "failure_modes": [
    "Performative Doomerism: Listing generic catastrophes (e.g., Asteroid Strike) instead of specific, endogenous failure modes."
  ],
  "invariants": [
    "Future Perspective: Analysis must assume failure has ALREADY happened (Probability=1.0).",
    "Specific Cause: Failure reasons must be actionable and endogenous, not generic bad luck."
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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:PreMortem#mh:SHA-256:8ca0f6838ca171fc8aea06174357c6d867b4217299e11dfb136a98c7993a32c7",
  "sema_ref": "PreMortem#8ca0",
  "sema_stub": "8ca0",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "recursive_root_cause": "RecursiveRootCause#7074",
      "steelman_check": "SteelmanCheck#dd78",
      "plan": "Plan#31a7"
    }
  }
}
```

---

## Prioritize#420e

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
  "sema_id": "sema:Prioritize#mh:SHA-256:420e04f6d680d32a9561c274f134dcc4f46a8417ba4398c10b23b0bd955f2def",
  "sema_ref": "Prioritize#420e",
  "sema_stub": "420e",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "criteria": "Criteria#ef6b",
      "value": "Value#3c5d",
      "work": "Work#bc56"
    },
    "composes_with": {
      "rank": "Rank#7a76"
    }
  }
}
```

---

## ProblemFramer#a3fc

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
  "sema_ref": "ProblemFramer#a3fc",
  "sema_id": "sema:ProblemFramer#mh:SHA-256:a3fc034f9afc2797a089d13d4f267eea68626002da80f51c6fe70997c7b2cf6b",
  "sema_stub": "a3fc",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "composes_with": {
      "request_framing": "RequestFraming#b776",
      "interpret": "Interpret#8ee3",
      "reframe": "Reframe#44c5"
    },
    "references": {
      "universal_solver_tree": "UniversalSolverTree#2c55",
      "root_solver": "RootSolver#0529"
    },
    "yields": {
      "accept_spec": "AcceptSpec#762e"
    }
  }
}
```

---

## RedTeam#c72c

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
      "SteelmanCheck#dd78"
    ],
    "ring": 2
  },
  "sema_id": "sema:RedTeam#mh:SHA-256:c72cc15f0c34cec80f78c90a059c6f6b305d8fcd9a8f788f8193d0369dc6877f",
  "sema_ref": "RedTeam#c72c",
  "sema_stub": "c72c",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "adversarial_steel": "AdversarialSteel#380c"
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
      "HeuristicSnap#f15c"
    ],
    "ring": 2
  },
  "sema_id": "sema:Reflex#mh:SHA-256:ea07e889ca64536b2f0d0657d1583a178ea36fe2fda6c26889c68d46e44a47ce",
  "sema_ref": "Reflex#ea07",
  "sema_stub": "ea07",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af"
}
```

---

## RegretMinimization#a15f

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
      "PreMortem#8ca0"
    ],
    "ring": 2
  },
  "sema_id": "sema:RegretMinimization#mh:SHA-256:a15fcbca53a62214a5c6906166ccfbc900722d517d970f63d0773d5b87d832f4",
  "sema_ref": "RegretMinimization#a15f",
  "sema_stub": "a15f",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "opportunity_cost": "OpportunityCost#6b5f",
      "decision": "Decision#934e"
    }
  }
}
```

---

## RepresentationSwap#1787

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
  "sema_id": "sema:RepresentationSwap#mh:SHA-256:17873eb0620df825d30ce77bb60440f64d7124741c5038c63009bcac481417cd",
  "sema_ref": "RepresentationSwap#1787",
  "sema_stub": "1787",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "concept_blend": "ConceptBlend#2894"
    }
  }
}
```

---

## Retry#cb3a

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
      "Backoff#c6d1"
    ],
    "ring": 1
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Retry#mh:SHA-256:cb3a4a6bfdea3e5b580c343e8f9eccd8c39eee535edf1823b6a31e3bcb358ccc",
  "sema_ref": "Retry#cb3a",
  "sema_stub": "cb3a",
  "dependencies": {
    "references": {
      "backoff": "Backoff#c6d1",
      "compensate": "Compensate#985e",
      "circuit_breaker": "CircuitBreaker#0577",
      "break": "Break#0bb3"
    }
  }
}
```

---

## RigorousSolver#483b

```json
{
  "handle": "RigorousSolver",
  "mechanism": "A high-reliability, high-latency implementation of {{polymorphic_solver}} that mandates the full five-surface Solver Contract (Manifest, Execute, Consult, Verify, Feedback) with non-compensatory acceptance gates \u2014 every declared invariant must pass before a Result becomes a Solution; partial success is not permitted to propagate. Uses {{probe}} to verify reality alignment and {{socratic_loop}} to disambiguate intent before action. Incorporates {{feedback}} to improve future reliability. Trades speed for assurance (System 2).",
  "gloss": "High-reliability, high-latency System 2 solver",
  "invariants": [
    "Lifecycle Completeness: Must complete all 5 stages including Verification.",
    "Mandatory Verification: Cannot skip Probe step."
  ],
  "derived_from": "PolymorphicSolver#bbe4",
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2,
    "tier": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:RigorousSolver#mh:SHA-256:483bc3ca7455aaab502322ea889798acde0ce1dd0af8a46b6a181a33ee7f0573",
  "sema_ref": "RigorousSolver#483b",
  "sema_stub": "483b",
  "dependencies": {
    "composes_with": {
      "feedback": "Feedback#dc36",
      "probe": "Probe#12d8"
    },
    "references": {
      "polymorphic_solver": "PolymorphicSolver#bbe4",
      "socratic_loop": "SocraticLoop#bc73"
    }
  }
}
```

---

## Roadmap#b236

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
  "sema_id": "sema:Roadmap#mh:SHA-256:b236b2faa4925583008ee6d464c09e9425ce1faf600763be945591c849f7c94d",
  "sema_ref": "Roadmap#b236",
  "sema_stub": "b236",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "goal": "Goal#5f27",
      "plan": "Plan#31a7"
    }
  }
}
```

---

## RootSolver#0529

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:RootSolver#mh:SHA-256:05296ff1cd30a98016a32352ab1c55a401eecf926e11e4c95b328302163c2b37",
  "sema_ref": "RootSolver#0529",
  "sema_stub": "0529",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "tree": "Tree#a5a3",
      "solver_node": "SolverNode#86bb",
      "problem": "Problem#64d0",
      "result": "Result#f29e",
      "budget": "Budget#0934",
      "solution": "Solution#445c",
      "problem_space": "ProblemSpace#6e74"
    },
    "composes_with": {
      "pathway_memory": "PathwayMemory#7899"
    }
  }
}
```

---

## SacrificialProbe#d2d4

```json
{
  "handle": "SacrificialProbe",
  "mechanism": "A Generalized Pattern where an {{agent}} sends a low-cost 'probe' into a {{system}} expecting it to fail, but designs the failure to be instructive. The probe must be cheap relative to the main payload, and the failure {{mode}} must update the {{strategy}} for the main payload. Common in startups (landing pages), immunology (dendritic cells), and warfare (reconnaissance). It wraps the concept of a staked probe in a higher-order strategy where the probe's destruction is the intended {{signal}}.",
  "gloss": "Learning via cheap, instructive failure",
  "failure_modes": [
    "Probe too expensive: breaks the Cost Asymmetry invariant, making the sacrifice unaffordable.",
    "Silent probe failure: {{probe}} fails but produces no observable signal, destroying the Instructive Failure property."
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
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:SacrificialProbe#mh:SHA-256:d2d446fef99984ac5c3abcc28b133834293714329910109f083214d4a1da37b4",
  "sema_ref": "SacrificialProbe#d2d4",
  "sema_stub": "d2d4",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "signal": "Signal#f39d",
      "mode": "Mode#3df1",
      "strategy": "Strategy#a0af",
      "agent": "Agent#d183",
      "probe": "Probe#12d8"
    }
  }
}
```

---

## Satisfice#64ac

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
    "{{option}} space enumerable.",
    "Acceptance threshold defined.",
    "Evaluation function exists."
  ],
  "postconditions": [
    "{{option}} meeting threshold found OR space exhausted.",
    "No backtracking occurred.",
    "{{decision}} final."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Mind",
    "category": "Strategy",
    "ring": 2
  },
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:Satisfice#mh:SHA-256:64ac7b839b043d6ffb4649cef58b6298c9edffb215f0eff8d4108fa25b32279c",
  "sema_ref": "Satisfice#64ac",
  "sema_stub": "64ac",
  "dependencies": {
    "references": {
      "optimal_stop": "OptimalStop#4dee",
      "option": "Option#483e",
      "decision": "Decision#934e"
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
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Simulation#398f

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
  "sema_id": "sema:Simulation#mh:SHA-256:398fb8a076fa02a90e2090899409644442669f6a16c3557d6e630a2872fcd707",
  "sema_ref": "Simulation#398f",
  "sema_stub": "398f",
  "invariants": [
    "Isolation: Side effects in W' DO NOT leak to W."
  ],
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "outcome": "Outcome#9bf0",
      "state": "State#4d58"
    }
  }
}
```

---

## Solver#4ed4

```json
{
  "handle": "Solver",
  "mechanism": "The abstract {{protocol}} exposing the five-surface Solver Contract \u2014 Manifest (what can you do?), Execute (perform the {{task}}), Consult (cost/quality/rationale), Verify (post-execution assurance), and Feedback (emits a typed {{performance_signal}} \u2014 structured evaluation, or a FrameError escalation). Manifest and Execute are mandatory; Consult/Verify/Feedback are optional but strongly recommended at hard seams. Accepts a typed Task and yields a typed {{solution}}. Solver is an interface, not a class: any {{agent}} can take on the role of a Solver for the duration of a Task. The \"[descriptor]Solver\" naming convention is the library's construction pattern \u2014 DiagnosticSolver, PlanningSolver, ReduceSolver, PUREOptimizationSolver, and so on are all minted by appending \"Solver\" to a domain descriptor, each specialising the contract. The same agent can wear many solver roles simultaneously or sequentially; lightweight roles (Manifest + Execute only) scale up to permanent instances as tasks compound. Recursion follows naturally: when a Solver decomposes its Task, it becomes the root of a sub-tree whose children are themselves Solvers \u2014 the mechanism that gives the UniversalSolverTree its fractal shape.",
  "gloss": "Abstract five-surface contract: Manifest, Execute, Consult, Verify, Feedback",
  "signature": [
    "Protocol#7e1c(Task#b290)"
  ],
  "_meta": {
    "layer": "Mind",
    "ring": 0,
    "category": "Strategy",
    "tier": 0
  },
  "sema_id": "sema:Solver#mh:SHA-256:4ed4703e641b4d38bc4179df117643b295206b9417a0c2f0d64a1e6a8e9a031f",
  "sema_ref": "Solver#4ed4",
  "sema_stub": "4ed4",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "performance_signal": "PerformanceSignal#d211",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#d183"
    },
    "accepts": {
      "task": "Task#b290"
    },
    "yields": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## SteelmanFirst#6516

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
  "sema_id": "sema:SteelmanFirst#mh:SHA-256:65165d1746590a58cc839da22e0c5536b6b9854472916dcb8e26b3efc074ffb1",
  "sema_ref": "SteelmanFirst#6516",
  "sema_stub": "6516",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "problem": "Problem#64d0",
      "steelman_check": "SteelmanCheck#dd78",
      "agent": "Agent#d183",
      "cognitive_bias": "CognitiveBias#4b32"
    }
  }
}
```

---

## Strategy#a0af

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
      "OODA#a143"
    ],
    "ring": 1
  },
  "sema_id": "sema:Strategy#mh:SHA-256:a0af3319c722d77ab549566285da23d1eed95a4f26a3c32859ca3877bd3c1031",
  "sema_ref": "Strategy#a0af",
  "sema_stub": "a0af",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "plan": "Plan#31a7"
    }
  }
}
```

---

## SunkCostIgnore#9dec

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
  "sema_id": "sema:SunkCostIgnore#mh:SHA-256:9dec2a21e106ee25043c8a1289c09967e579ce927ee7a0d92e896d736889d04b",
  "sema_ref": "SunkCostIgnore#9dec",
  "sema_stub": "9dec",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "loop": "Loop#a316",
      "opportunity_cost": "OpportunityCost#6b5f",
      "decision": "Decision#934e"
    }
  }
}
```

---

## TensionHold#ec3b

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
  "sema_ref": "TensionHold#ec3b",
  "sema_id": "sema:TensionHold#mh:SHA-256:ec3b5dcf8b3d366184d42b04654f2a33f28645582259d335c4f39b8da10ed220",
  "sema_stub": "ec3b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "dialectic": "Dialectic#2e3c",
      "synthesis": "Synthesis#26b9"
    },
    "yields": {
      "tension": "Tension#92e3"
    }
  }
}
```

---

## ThinSlice#2938

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
  "sema_id": "sema:ThinSlice#mh:SHA-256:29385129b74822e0c4ad282a96e82553a93efd42cc0ec632242afe14ac5a1bf5",
  "sema_ref": "ThinSlice#2938",
  "sema_stub": "2938",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "route": "Route#34c7",
      "somatic_marker": "SomaticMarker#7250",
      "extended_thinking": "ExtendedThinking#f9eb"
    }
  }
}
```

---

## TimeboxThink#9e1b

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
  "sema_id": "sema:TimeboxThink#mh:SHA-256:9e1b4a5f760daa82a8c535a45e74d4808c6854e2b8dc9b2471d7d7d35ef28282",
  "sema_ref": "TimeboxThink#9e1b",
  "sema_stub": "9e1b",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "constraint": "Constraint#87fe",
      "work": "Work#bc56",
      "value": "Value#3c5d",
      "budget": "Budget#0934"
    }
  }
}
```

---

## TradeOff#1838

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
  "sema_category": "Strategy#a0af",
  "sema_id": "sema:TradeOff#mh:SHA-256:18382c0953f988f4640c73c0f333d15a8cf5f29c884b3dda8342420d4c8c8e76",
  "sema_ref": "TradeOff#1838",
  "sema_stub": "1838",
  "dependencies": {
    "references": {
      "decision": "Decision#934e"
    }
  }
}
```

---

## UncertaintyMap#9a55

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
  "sema_id": "sema:UncertaintyMap#mh:SHA-256:9a55205b4bc9e75593bd56f7ae528b4a71b2ea76f34881574b459c1cea589878",
  "sema_ref": "UncertaintyMap#9a55",
  "sema_stub": "9a55",
  "sema_layer": "Mind",
  "sema_category": "Strategy#a0af",
  "dependencies": {
    "references": {
      "confidence_calibrate": "ConfidenceCalibrate#e454",
      "prioritize": "Prioritize#420e",
      "probe": "Probe#12d8"
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
  "sema_category": "Strategy#a0af",
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

## Dampen#3f0c

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
  "sema_ref": "Dampen#3f0c",
  "sema_id": "sema:Dampen#mh:SHA-256:3f0c7b83e6f4573c0ba43deb323efe1058f76dcb9ceeb11c3cc0bc5cb03eeaa3",
  "sema_stub": "3f0c",
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "signal": "Signal#f39d",
      "noise": "Noise#3d9a"
    }
  }
}
```

---

## Decay#1e8b

```json
{
  "handle": "Decay",
  "mechanism": "Gradual Attenuation: Without reinforcement, {{value}} V decreases over time. Decay rate R determines half-life. Reinforcement resets or boosts V. Zero threshold triggers {{state}} change or removal.",
  "gloss": "Automatic expiration of stale state",
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
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Decay#mh:SHA-256:1e8b3dab66b0ccef4d350f94e38aa66dc3757d6b5c429f024d90a98ec67ed924",
  "sema_ref": "Decay#1e8b",
  "sema_stub": "1e8b",
  "dependencies": {
    "references": {
      "state": "State#4d58",
      "value": "Value#3c5d"
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
      "EntropyPump#ed3b"
    ]
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Entropy#mh:SHA-256:a2652f69c57b3c737f3d0d910e6751d61ea2e9007046ac0f75ee336d178c9212",
  "sema_ref": "Entropy#a265",
  "sema_stub": "a265",
  "dependencies": {
    "references": {
      "message": "Message#f767",
      "system": "System#e314"
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

## Gradient#480b

```json
{
  "handle": "Gradient",
  "mechanism": "The directional rate of change of a scalar field across a differentiable space. For any sufficiently smooth field f over a differentiable space, the gradient \u2207f at a point is the vector whose direction is the one of steepest ascent of f and whose magnitude is the rate of increase in that direction. Substrate property: gradients exist wherever fields exist, whether or not anyone measures them. Specific cases include {{entropy}} gradients (the direction of maximum disorder increase), attention gradients, credibility gradients, information-density gradients. Higher patterns use gradients for hill-climbing search, attention allocation, credit assignment, and flow routing.",
  "gloss": "The directional rate of change of a scalar field \u2014 substrate for hill-climbing, attention flow, and credit assignment",
  "invariants": [
    "Existence: every sufficiently smooth field on a differentiable space has a gradient defined at every interior point.",
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
  "sema_id": "sema:Gradient#mh:SHA-256:480b30ac75af5c4fb2509b9889b184b6691482045af22a9dfbdbdf362535fb99",
  "sema_ref": "Gradient#480b",
  "sema_stub": "480b",
  "dependencies": {
    "references": {
      "entropy": "Entropy#a265"
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

## Measurement#5da6

```json
{
  "handle": "Measurement",
  "mechanism": "The substrate act of extracting information about a system's {{state}} \u2014 an operation that, in general, *changes the state being measured*. Distinct from the cognitive `Observe` primitive: Measurement is the substrate-level phenomenon, Observe is the agent-level process. In quantum systems, measurement collapses superposition. In distributed systems, observing a clock at node A introduces latency and ambiguity about the clock's value elsewhere. In classical measurement, even reading a variable in a concurrent system can race with writers. The substrate property is that observation is never free \u2014 it takes resources, it takes time, and it perturbs the measured system. The degree of perturbation is domain-dependent (negligible for a thermometer in a large water tank; total for a measurement on a qubit); the substrate fact of perturbation is universal.",
  "gloss": "The substrate act of extracting information from a system \u2014 in general, changes the state being measured",
  "invariants": [
    "Perturbation: measurement, in general, changes the state of the measured system. The degree varies by domain; the fact does not.",
    "Cost: measurement requires resources (time, energy, channel capacity) \u2014 there is no free observation.",
    "Irreversibility: once a measurement has extracted information, the prior state is not recoverable merely by unobserving \u2014 collapse of superposition in quantum systems, record of observation in classical systems."
  ],
  "_meta": {
    "tier": 1,
    "layer": "Physics",
    "category": "Primitives",
    "ring": 0
  },
  "sema_layer": "Physics",
  "sema_category": "Primitives",
  "sema_id": "sema:Measurement#mh:SHA-256:5da6ed7d2127c41bdeb1cfaa0d737425ec5c0d762eb6288601e0f781aa18a9e0",
  "sema_ref": "Measurement#5da6",
  "sema_stub": "5da6",
  "dependencies": {
    "references": {
      "state": "State#4d58"
    }
  }
}
```

---

## Mutex#1334

```json
{
  "handle": "Mutex",
  "mechanism": "Exclusive access token. Lifecycle: ACQUIRE {{task}} -> GRANT/QUEUE -> HOLD -> RELEASE/YIELD. Token represents a unique handle ({{resource}}). Sequence increments on transfer. Priority queue prevents starvation. Fencing tokens handle revocation. It manages exclusive access by enforcing a strict queue via delegation or throttling, often isolating the critical section.",
  "gloss": "Physical possession token",
  "failure_modes": [
    "Totem loss (requires regeneration protocol).",
    "Holder crash: token orphaned (mitigated by expires_at + heartbeat).",
    "Token corruption (mitigated by REGENERATE protocol).",
    "Deadlock (mitigated by wait-for graph detection + ordered acquisition).",
    "Starvation (mitigated by aging + anti-starvation rule \u2014 no consecutive preemption).",
    "Byzantine holder (mitigated by forcible REVOKE + fencing).",
    "Split brain (mitigated by fencing tokens that invalidate on revocation)."
  ],
  "invariants": [
    "Uniqueness, {{conservation}} of the fencing totem"
  ],
  "preconditions": [
    "Resource exists and is lockable.",
    "At least 2 agents contending.",
    "Agents can communicate."
  ],
  "postconditions": [
    "Exactly one agent holds lock.",
    "Other agents blocked or notified.",
    "{{lock}} state consistent across all observers."
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
  "sema_id": "sema:Mutex#mh:SHA-256:1334485e8f4235f91fec5fedc9b391b636101ab50948e25e3cffea26adfecc68",
  "sema_ref": "Mutex#1334",
  "sema_stub": "1334",
  "dependencies": {
    "accepts": {
      "task": "Task#b290"
    },
    "references": {
      "resource": "Resource#553a",
      "lock": "Lock#051c",
      "conservation": "Conservation#d63a"
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

## Noise#3d9a

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
  "sema_id": "sema:Noise#mh:SHA-256:3d9a1d81d0ed1dbb9b14ab1d1f466e0ee229330c4f1dae8f2a5ddb7e02126d8e",
  "sema_ref": "Noise#3d9a",
  "sema_stub": "3d9a",
  "dependencies": {
    "references": {
      "datum": "Datum#31cf",
      "task": "Task#b290",
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

## CausalBarrier#cb43

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
  "sema_id": "sema:CausalBarrier#mh:SHA-256:cb43841ba6f2f96fc5308b501c9f194263859f7cdc067478ce3ac3c212edbf47",
  "sema_ref": "CausalBarrier#cb43",
  "sema_stub": "cb43",
  "sema_layer": "Physics",
  "sema_category": "Time",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#5602",
      "agent": "Agent#d183"
    }
  }
}
```

---

# Layer: Society

## Compromise#f646

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
  "sema_ref": "Compromise#f646",
  "sema_id": "sema:Compromise#mh:SHA-256:f6466240787604b0fc101e13935a2bc7a4859c9eadb4285734125f9932b76880",
  "sema_stub": "f646",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "yield": "Yield#0de8",
      "agent": "Agent#d183",
      "system": "System#e314"
    },
    "composes_with": {
      "dampen": "Dampen#3f0c"
    }
  }
}
```

---

## Consensus#cc1d

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
  "sema_id": "sema:Consensus#mh:SHA-256:cc1d5318fed3420ecaac8748bd2ebd935b9e7d48cd8f874fcfc731d8e87f1f11",
  "sema_ref": "Consensus#cc1d",
  "sema_stub": "cc1d",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "composes_with": {
      "vote": "Vote#625c",
      "quorum": "Quorum#a295"
    },
    "accepts": {
      "proposal": "Proposal#ab24"
    },
    "yields": {
      "value": "Value#3c5d"
    }
  }
}
```

---

## ConsensusFinder#299d

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
  "sema_id": "sema:ConsensusFinder#mh:SHA-256:299d1024dad094583f6af34160c81a3442d7523d9566c0af749f51746c98d063",
  "sema_ref": "ConsensusFinder#299d",
  "sema_stub": "299d",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "signature": [
    "Discover#aa70(Consensus#cc1d)"
  ],
  "dependencies": {
    "references": {
      "resonate": "Resonate#155f",
      "quorum": "Quorum#a295",
      "discover": "Discover#aa70",
      "consensus": "Consensus#cc1d"
    }
  }
}
```

---

## Delegate#60aa

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
    "Principal has authority.",
    "Delegate capable.",
    "Scope of delegation defined."
  ],
  "postconditions": [
    "Delegate acts within scope.",
    "Principal notified of actions.",
    "Revocation possible."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "related": [
      "Handoff#d5e6"
    ],
    "ring": 1
  },
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "sema_id": "sema:Delegate#mh:SHA-256:60aa6cc18e942205d17401e1feafee733dac5ceffcae1fb9f9abffc51ff91afa",
  "sema_ref": "Delegate#60aa",
  "sema_stub": "60aa",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "work": "Work#bc56"
    },
    "yields": {
      "task": "Task#b290"
    },
    "accepts": {
      "holographic_shard": "HolographicShard#34d0"
    },
    "composes_with": {
      "heartbeat": "Heartbeat#8e36",
      "probe": "Probe#12d8"
    }
  }
}
```

---

## Disband#fc51

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
  "sema_id": "sema:Disband#mh:SHA-256:fc51c8ce6fbd55c1c462132187da2bf1890267dff00dc32fc03cce5c764da566",
  "sema_ref": "Disband#fc51",
  "sema_stub": "fc51",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "yields": {
      "snapshot": "Snapshot#0ae9"
    },
    "references": {
      "ejection_seat": "EjectionSeat#b71c",
      "state": "State#4d58",
      "quorum": "Quorum#a295",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Elect#0635

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
      "Vote#625c"
    ],
    "ring": 2
  },
  "sema_id": "sema:Elect#mh:SHA-256:0635df9ddda6928d4ecb80d5a9fd82aab8b17bae03880e5420c44b99cb5e7b93",
  "sema_ref": "Elect#0635",
  "sema_stub": "0635",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "accepts": {
      "accept_spec": "AcceptSpec#762e",
      "ballot": "Ballot#1934"
    },
    "yields": {
      "solution": "Solution#445c"
    }
  }
}
```

---

## IdentityHandshake#6c90

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
  "sema_id": "sema:IdentityHandshake#mh:SHA-256:6c901e82514035eb5434a1f3971306786fa08e62092ca599b0debcb82c286a8f",
  "sema_ref": "IdentityHandshake#6c90",
  "sema_stub": "6c90",
  "signature": [
    "Discover#aa70(Identity#626c)"
  ],
  "dependencies": {
    "references": {
      "ontology_handshake": "OntologyHandshake#8443",
      "nature": "Nature#6c1a",
      "check": "Check#410e",
      "mode": "Mode#3df1",
      "identity": "Identity#626c",
      "discover": "Discover#aa70",
      "spectral_tune": "SpectralTune#b25a"
    }
  }
}
```

---

## LazyConsensus#bd8f

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
  "sema_ref": "LazyConsensus#bd8f",
  "sema_id": "sema:LazyConsensus#mh:SHA-256:bd8f747e8499cf012145cd432c0b5a3fa9019396e7482a3dbe46af9500cf468f",
  "sema_stub": "bd8f",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "quorum": "Quorum#a295",
      "time_warp_log": "TimeWarpLog#8751"
    }
  }
}
```

---

## OntologyHandshake#8443

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
    "Both agents have ontologies.",
    "Communication channel open.",
    "Ontology serializable."
  ],
  "postconditions": [
    "Shared terms mapped.",
    "Unmappable terms flagged.",
    "Communication can proceed with known precision."
  ],
  "_meta": {
    "tier": 2,
    "layer": "Society",
    "category": "Coordination",
    "ring": 1
  },
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "sema_id": "sema:OntologyHandshake#mh:SHA-256:8443a5ff6918e7aefbb04017aaaf658c9bdbd39a80bc9663bd731060a6adb23f",
  "sema_ref": "OntologyHandshake#8443",
  "sema_stub": "8443",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb"
    },
    "references": {
      "protocol": "Protocol#7e1c",
      "spectral_tune": "SpectralTune#b25a"
    }
  }
}
```

---

## Rally#15b1

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
    "Initiator has too much power over selection (mitigated by transparent selection_criteria)."
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
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "sema_id": "sema:Rally#mh:SHA-256:15b169519920ab5fbae1023353dda80750cb3317545fa6c354fc3711c3cade41",
  "sema_ref": "Rally#15b1",
  "sema_stub": "15b1",
  "dependencies": {
    "composes_with": {
      "accept_spec": "AcceptSpec#762e"
    },
    "references": {
      "select": "Select#15c2",
      "elect": "Elect#0635",
      "context": "Context#e88a",
      "protocol": "Protocol#7e1c",
      "quorum": "Quorum#a295"
    },
    "accepts": {
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## Resonate#155f

```json
{
  "handle": "Resonate",
  "mechanism": "Alignment emerges from observable actions and mutual adjustment without explicit negotiation. Agents perform actions with attached INTENT_TAGS. Observers AMPLIFY (reinforce) or {{dampen}} (ignore) based on compatibility. It detects alignment via {{signal}} amplification and {{spectral_tune}}, eventually allowing the relationship to solidify into a stable bond.",
  "gloss": "Implicit coordination via signal amplification",
  "failure_modes": [
    "False Resonance: Apparent alignment that is actually random {{noise}}.",
    "Echo Chamber: Feedback {{loop}} amplifies error instead of {{signal}}.",
    "Spoofing: Adversarial agents emit fake intent tags (Cheap Talk).",
    "Precise-coordination mismatch: RESONATE only achieves approximate alignment; high-stakes actions requiring precision need a different coordination primitive.",
    "{{signal}} {{noise}} drowns real patterns.",
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
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "sema_id": "sema:Resonate#mh:SHA-256:155f6c11d3e0ea4d22870a496ced173a776b8b403a7a07b38527e403fc7ce011",
  "sema_ref": "Resonate#155f",
  "sema_stub": "155f",
  "dependencies": {
    "references": {
      "dampen": "Dampen#3f0c",
      "loop": "Loop#a316",
      "signal": "Signal#f39d",
      "decay": "Decay#1e8b",
      "noise": "Noise#3d9a",
      "spectral_tune": "SpectralTune#b25a"
    }
  }
}
```

---

## Vote#625c

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
  "sema_id": "sema:Vote#mh:SHA-256:625c38775074a5eaf09c8fc54cf58b12f54d0cbb53681aae52c781e51c04fab4",
  "sema_ref": "Vote#625c",
  "sema_stub": "625c",
  "sema_layer": "Society",
  "sema_category": "Coordination",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "aggregate": "Aggregate#8c2a",
      "elect": "Elect#0635",
      "system": "System#e314"
    },
    "accepts": {
      "ballot": "Ballot#1934"
    },
    "composes_with": {
      "quorum": "Quorum#a295"
    }
  }
}
```

---

## AtomicBid#1800

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
  "sema_ref": "AtomicBid#1800",
  "sema_id": "sema:AtomicBid#mh:SHA-256:1800c69013908f208b903cc3ce2edfb756a898f8797c19f3ec6a9132dd180ecc",
  "sema_stub": "1800",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "composes_with": {
      "bid": "Bid#cffa",
      "compensate": "Compensate#985e",
      "act": "Act#dc2d"
    },
    "references": {
      "lazy_consensus": "LazyConsensus#bd8f",
      "audit": "Audit#6888"
    }
  }
}
```

---

## AttentionMarkets#459c

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
  "sema_id": "sema:AttentionMarkets#mh:SHA-256:459cc3d717065f99e48d51011237f81d3f1ea6ea29e82db4494c5f7cd7b59fda",
  "sema_ref": "AttentionMarkets#459c",
  "sema_stub": "459c",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "value": "Value#3c5d",
      "signal": "Signal#f39d"
    },
    "composes_with": {
      "continuous_resource_auction": "ContinuousResourceAuction#0361"
    }
  }
}
```

---

## Award#71bc

```json
{
  "handle": "Award",
  "mechanism": "The formal {{act}} of accepting a {{bid}}. It triggers the creation of a {{contract}} which all parties must {{sign}}, and uses {{held_release}} to lock the agreed {{value}} as collateral or payment. This action transitions the {{state}} from Negotiation to Execution, authorizing the {{solver}} to begin.",
  "gloss": "Acceptance of bid and contract creation",
  "signature": [
    "Act#dc2d(Contract#087b)"
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
  "sema_ref": "Award#71bc",
  "sema_id": "sema:Award#mh:SHA-256:71bc33959fbfcd71a3e4a7a6b85c18adbbd4e2f4b480277f6338ae0ffd25cc78",
  "sema_stub": "71bc",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "accepts": {
      "bid": "Bid#cffa"
    },
    "references": {
      "value": "Value#3c5d",
      "state": "State#4d58",
      "solver": "Solver#4ed4"
    },
    "composes_with": {
      "act": "Act#dc2d",
      "held_release": "HeldRelease#33cb",
      "sign": "Sign#d60d"
    },
    "yields": {
      "contract": "Contract#087b"
    }
  }
}
```

---

## Bid#cffa

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
  "sema_ref": "Bid#cffa",
  "sema_id": "sema:Bid#mh:SHA-256:cffac75862caade2aa7760b56a1accf4dff2d497c879861193f00e09efde4e93",
  "sema_stub": "cffa",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "compute_budget": "ComputeBudget#8a42",
      "task": "Task#b290",
      "commitment_device": "CommitmentDevice#3aeb",
      "value": "Value#3c5d",
      "budget": "Budget#0934",
      "artifact": "Artifact#6254",
      "solver": "Solver#4ed4"
    }
  }
}
```

---

## ContinuousResourceAuction#0361

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
      "AttentionMarkets#459c"
    ]
  },
  "sema_ref": "ContinuousResourceAuction#0361",
  "sema_id": "sema:ContinuousResourceAuction#mh:SHA-256:0361f5fe7efb3045c6f96b1b98909949cfc83665a3f222c1fef32857b7574a81",
  "sema_stub": "0361",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "protocol": "Protocol#7e1c"
    },
    "composes_with": {
      "state_lock": "StateLock#5602"
    },
    "accepts": {
      "value": "Value#3c5d"
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
      "value": "Value#3c5d",
      "metric": "Metric#17fd"
    }
  }
}
```

---

## Gardener#6ccb

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
  "sema_id": "sema:Gardener#mh:SHA-256:6ccb65d3234713718d1c62fc3ae69c983eaf80cb7a21a80f126a5a207f48f826",
  "sema_ref": "Gardener#6ccb",
  "sema_stub": "6ccb",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "signature": [
    "Stigmergy#53d4(Care#b01c)"
  ],
  "dependencies": {
    "references": {
      "stigmergy": "Stigmergy#53d4",
      "care": "Care#b01c",
      "graceful_degradation": "GracefulDegradation#a692",
      "compensate": "Compensate#985e"
    }
  }
}
```

---

## MintWhenFriction#4e33

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
  "sema_id": "sema:MintWhenFriction#mh:SHA-256:4e338a8ce80bc1463a72368440045ba8385dd7edee03e30e935bfeb24c490dff",
  "sema_ref": "MintWhenFriction#4e33",
  "sema_stub": "4e33",
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "pattern_discovery": "PatternDiscovery#99dd",
      "value": "Value#3c5d",
      "construct_ontology": "ConstructOntology#d5a0"
    }
  }
}
```

---

## ValuePeg#ab74

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
  "sema_id": "sema:ValuePeg#mh:SHA-256:ab743dbc7830fe27ab36115f3777678ceadfcf47168885700c6c476fdc5598b1",
  "sema_ref": "ValuePeg#ab74",
  "sema_stub": "ab74",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "yields": {
      "exchange_rate": "ExchangeRate#1c21"
    },
    "references": {
      "optimize": "Optimize#b98b",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Yield#0de8

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
  "sema_id": "sema:Yield#mh:SHA-256:0de85f1f0d25974e6aa1b306009a0abfd06fa875b467a8c1ba02936af3aa9a26",
  "sema_ref": "Yield#0de8",
  "sema_stub": "0de8",
  "sema_layer": "Society",
  "sema_category": "Economics",
  "dependencies": {
    "references": {
      "backoff": "Backoff#c6d1",
      "defer": "Defer#2500",
      "system": "System#e314",
      "overlap": "Overlap#b462"
    }
  }
}
```

---

## AnchorDrop#ad75

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
      "ConceptAnchor#828b"
    ],
    "ring": 0
  },
  "sema_id": "sema:AnchorDrop#mh:SHA-256:ad75980e19412c138b06045391e31b3f351b47a4a8e368dc902d2f98fe522c31",
  "sema_ref": "AnchorDrop#ad75",
  "sema_stub": "ad75",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "quorum": "Quorum#a295",
      "system": "System#e314",
      "consensus": "Consensus#cc1d"
    }
  }
}
```

---

## Constitution#d2e5

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
  "sema_id": "sema:Constitution#mh:SHA-256:d2e5ca2eb2c651927da977d2df49fa52bf0875c3ac2040a350a5d21511f625de",
  "sema_ref": "Constitution#d2e5",
  "sema_stub": "d2e5",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "agent": "Agent#d183"
    }
  }
}
```

---

## DocumentedOverride#4356

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
  "sema_id": "sema:DocumentedOverride#mh:SHA-256:4356e3fdc9292f0c3573925ce588fa0dd159830d1ef410b4153767741f3ec65e",
  "sema_ref": "DocumentedOverride#4356",
  "sema_stub": "4356",
  "dependencies": {
    "accepts": {
      "accept_spec": "AcceptSpec#762e"
    },
    "composes_with": {
      "time_warp_log": "TimeWarpLog#8751"
    },
    "yields": {
      "decision": "Decision#934e"
    }
  }
}
```

---

## Responsibility#b3b1

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
  "sema_id": "sema:Responsibility#mh:SHA-256:b3b1e537f4e49dc2bc607b1edbd2b5c54f0649ea0751ebdfb7df05a7ca5a983c",
  "sema_ref": "Responsibility#b3b1",
  "sema_stub": "b3b1",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "heartbeat": "Heartbeat#8e36",
      "system": "System#e314",
      "state": "State#4d58",
      "oath_bind": "OathBind#af30",
      "agent": "Agent#d183"
    }
  }
}
```

---

## Role#dcb2

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
  "sema_ref": "Role#dcb2",
  "sema_id": "sema:Role#mh:SHA-256:dcb27d5c73551c3543a19343ee31cde4d98d7cd09ef9f6e07aa10f52ae8df12c",
  "sema_stub": "dcb2",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "permission": "Permission#d981",
      "agent": "Agent#d183",
      "responsibility": "Responsibility#b3b1"
    }
  }
}
```

---

## SolverTree#65f2

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
      "UniversalSolverTree#2c55"
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
  "sema_ref": "SolverTree#65f2",
  "sema_id": "sema:SolverTree#mh:SHA-256:65f2ab7b6cbd34eccfa1de9908566b186c5ab6937b547752a43ea5833d22898a",
  "sema_stub": "65f2",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "tree": "Tree#a5a3",
      "solver_node": "SolverNode#86bb",
      "root_solver": "RootSolver#0529",
      "budget": "Budget#0934",
      "localized_learning": "LocalizedLearning#eb5a"
    },
    "accepts": {
      "task": "Task#b290"
    }
  }
}
```

---

## UniversalSolverTree#2c55

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
  "sema_ref": "UniversalSolverTree#2c55",
  "sema_id": "sema:UniversalSolverTree#mh:SHA-256:2c551bc0c0f026077f0edd124fbfdbf4908275b2438197406104505d047f7d55",
  "sema_stub": "2c55",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "tree": "Tree#a5a3",
      "solver_node": "SolverNode#86bb",
      "problem": "Problem#64d0",
      "solver_tree": "SolverTree#65f2",
      "solution": "Solution#445c",
      "localized_learning": "LocalizedLearning#eb5a"
    }
  }
}
```

---

## WorldTransparent#dc1c

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
  "sema_id": "sema:WorldTransparent#mh:SHA-256:dc1c1731924848a8a52cdfe9e17c24817797fced7cde53792418145eff7eaee9",
  "sema_ref": "WorldTransparent#dc1c",
  "sema_stub": "dc1c",
  "sema_layer": "Society",
  "sema_category": "Governance",
  "dependencies": {
    "references": {
      "system": "System#e314",
      "explain_beacon": "ExplainBeacon#9d6d"
    }
  }
}
```

---

## AdversarialProof#d04c

```json
{
  "handle": "AdversarialProof",
  "mechanism": "Cognitively-enriched {{negative_proof}} that invokes {{red_team}} logic to exhaustively search for prohibited data. The adversarial mindset ensures blind spots are probed. Treats failure-to-find-despite-adversarial-effort as high-confidence proof of absence.",
  "gloss": "Adversarial proof of absence",
  "derived_from": "NegativeProof#14ee",
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
  "sema_id": "sema:AdversarialProof#mh:SHA-256:d04c3986b0dc7efa63e57d4cdbb9eb5f8bf7172910763c5d8c08e3270822040e",
  "sema_ref": "AdversarialProof#d04c",
  "sema_stub": "d04c",
  "dependencies": {
    "composes_with": {
      "negative_proof": "NegativeProof#14ee",
      "red_team": "RedTeam#c72c"
    },
    "references": {
      "hypothesis": "Hypothesis#ffa7"
    }
  }
}
```

---

## AgentDiscover#5a6c

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
  "sema_id": "sema:AgentDiscover#mh:SHA-256:5a6c5a923cda1549edce5e43954b7663e297aba09656a256c80e8b84f9c4b08b",
  "sema_ref": "AgentDiscover#5a6c",
  "sema_stub": "5a6c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Discover#aa70(Agent#d183)"
  ],
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "discover": "Discover#aa70",
      "card": "Card#f63d"
    }
  }
}
```

---

## AgentProtocol#1350

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
  "sema_id": "sema:AgentProtocol#mh:SHA-256:1350a3908d1c2493a5156e4fa54a10f5297d658553659cc29fd05c0bca6ed101",
  "sema_ref": "AgentProtocol#1350",
  "sema_stub": "1350",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Agent#d183(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "greet": "Greet#ff79",
      "accept_spec": "AcceptSpec#762e",
      "work": "Work#bc56",
      "solution": "Solution#445c",
      "fail_closed": "FailClosed#59d8",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#d183"
    }
  }
}
```

---

## AgentSandbox#1838

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
      "Solution#445c",
      "Task#b290"
    ]
  },
  "sema_id": "sema:AgentSandbox#mh:SHA-256:18387c4cfc5c99e7e7a6d03a954bdc74b312ce422521a1aa6fd2a432ee49f9cf",
  "sema_ref": "AgentSandbox#1838",
  "sema_stub": "1838",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Sandbox#e00f(Agent#d183)"
  ],
  "dependencies": {
    "composes_with": {
      "output_guard": "OutputGuard#1c09",
      "input_guard": "InputGuard#7353"
    },
    "references": {
      "sandbox": "Sandbox#e00f",
      "context": "Context#e88a",
      "audit": "Audit#6888",
      "agent": "Agent#d183"
    }
  }
}
```

---

## AmbiguityResolution#6cb8

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
  "sema_ref": "AmbiguityResolution#6cb8",
  "sema_id": "sema:AmbiguityResolution#mh:SHA-256:6cb8f13d0b6ed8a75e42db359f5c6ab4ae471c8d1b56f0adad4601ba630c1d83",
  "sema_stub": "6cb8",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "vote": "Vote#625c",
      "entropy_pump": "EntropyPump#ed3b"
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

## BoundedTask#96e1

```json
{
  "handle": "BoundedTask",
  "mechanism": "A specialized {{task}} enforcing {{budget}} and {{accept_spec}} to ensure economic and quality boundaries.",
  "gloss": "Economically constrained task",
  "invariants": [
    "Budget Enclosure: total cost across all child tasks, retries, and recursions must stay within the declared {{budget}}.",
    "Quality Gate: output must pass the declared {{accept_spec}} before the task is marked complete."
  ],
  "derived_from": "Task#b290",
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 2,
    "tier": 2
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:BoundedTask#mh:SHA-256:96e14b831c3dec6d938fcfb5522c2629e3b69048ea14097dae95a0258090ff61",
  "sema_ref": "BoundedTask#96e1",
  "sema_stub": "96e1",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "accept_spec": "AcceptSpec#762e",
      "budget": "Budget#0934"
    }
  }
}
```

---

## Canary#86d6

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
  "sema_id": "sema:Canary#mh:SHA-256:86d6889719d684744ebf19311b800f3b92aa7389a98d3950f342a3e8d7bf2ff3",
  "sema_ref": "Canary#86d6",
  "sema_stub": "86d6",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "greet": "Greet#ff79",
      "work": "Work#bc56",
      "mode": "Mode#3df1",
      "agent": "Agent#d183",
      "probe": "Probe#12d8"
    }
  }
}
```

---

## ConfusedDeputy#0cfe

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
  "sema_ref": "ConfusedDeputy#0cfe",
  "sema_id": "sema:ConfusedDeputy#mh:SHA-256:0cfec9ab5d9db48a523e1d1da75876897dbf7c1e56a58bd962789f52f4df5e82",
  "sema_stub": "0cfe",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "permission": "Permission#d981",
      "actor": "Actor#57f6",
      "agent": "Agent#d183"
    }
  }
}
```

---

## ContextSwitch#3a3c

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
  "sema_id": "sema:ContextSwitch#mh:SHA-256:3a3c77415835f1560105a1b2d9dc0ddf0a6c08add99612b95ef03da04773aa15",
  "sema_ref": "ContextSwitch#3a3c",
  "sema_stub": "3a3c",
  "dependencies": {
    "accepts": {
      "context": "Context#e88a"
    },
    "references": {
      "agent": "Agent#d183",
      "mode": "Mode#3df1"
    }
  }
}
```

---

## CounterfactualAnchor#c56d

```json
{
  "handle": "CounterfactualAnchor",
  "mechanism": "Freezes a prediction BEFORE observation. 1. Instantiate immutable Anchor (Expectation). 2. {{observe}} Reality. 3. Learning {{signal}} = Delta(Anchor, Reality). Prevents Hindsight {{cognitive_bias}} by forcing updates based on genuine surprise. It creates the static reference point against which {{surprisal_update}} measures the magnitude of the learning delta.",
  "gloss": "Freezing expectation to measure true surprise",
  "failure_modes": [
    "Hindsight Leakage: {{agent}} unconsciously adjusts the Anchor as data comes in.",
    "Vague Anchor: Prediction is too broad to be falsified (e.g., 'Something will happen').",
    "Anchor Abandonment: {{agent}} ignores the Anchor when the delta is too large (denial)."
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
  "sema_id": "sema:CounterfactualAnchor#mh:SHA-256:c56d31792fc767614c6638ee89224c3ad240969823ebff82f174946137524ae7",
  "sema_ref": "CounterfactualAnchor#c56d",
  "sema_stub": "c56d",
  "dependencies": {
    "references": {
      "cognitive_bias": "CognitiveBias#4b32",
      "surprisal_update": "SurprisalUpdate#9db2",
      "observe": "Observe#abc0",
      "agent": "Agent#d183",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## DataMinimization#9e2c

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
  "sema_id": "sema:DataMinimization#mh:SHA-256:9e2c2ffd1e47951cadee0136e4a377e16d4503645d0d5322665897ffcdc78ded",
  "sema_ref": "DataMinimization#9e2c",
  "sema_stub": "9e2c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "input_guard": "InputGuard#7353",
      "task": "Task#b290",
      "correlation": "Correlation#148d",
      "select": "Select#15c2",
      "accept_spec": "AcceptSpec#762e",
      "context_compress": "ContextCompress#4845",
      "context": "Context#e88a",
      "protocol": "Protocol#7e1c",
      "agent": "Agent#d183"
    }
  }
}
```

---

## DeliberativeAlign#4a26

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
  "sema_id": "sema:DeliberativeAlign#mh:SHA-256:4a26cd842d2e9f760d6e5acef27501dfdf47e10b4d08d7e9924f68861c8b5792",
  "sema_ref": "DeliberativeAlign#4a26",
  "sema_stub": "4a26",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "accepts": {
      "task": "Task#b290",
      "constitution": "Constitution#d2e5"
    },
    "references": {
      "solver_node": "SolverNode#86bb",
      "context": "Context#e88a",
      "check": "Check#410e",
      "trace": "Trace#2836",
      "agent": "Agent#d183",
      "manifest_planning": "ManifestPlanning#b9ad"
    }
  }
}
```

---

## Deploy#742d

```json
{
  "handle": "Deploy",
  "mechanism": "The {{act}} of moving an artifact or system from a development/staging environment to a production environment. It executes the {{rollout}} process to make the system active and accessible to users.",
  "gloss": "Release to production",
  "signature": [
    "Act#dc2d(Rollout#5475)"
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
  "sema_ref": "Deploy#742d",
  "sema_id": "sema:Deploy#mh:SHA-256:742d3a6944e334ba70bacf08ae7acffe9347e20dba4ad0be41f4b42b198e5270",
  "sema_stub": "742d",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "act": "Act#dc2d",
      "rollout": "Rollout#5475"
    }
  }
}
```

---

## Discover#aa70

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
  "sema_id": "sema:Discover#mh:SHA-256:aa709470f6d2f97f561d6d0a181ee8980688ce91c6b0ee2f6c8d2a33586f6dfd",
  "sema_ref": "Discover#aa70",
  "sema_stub": "aa70",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "search": "Search#82c8",
      "check": "Check#410e",
      "criteria": "Criteria#ef6b",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## DissentSeek#89c2

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
  "sema_id": "sema:DissentSeek#mh:SHA-256:89c200b54eefbf13bbe87598c8d73cb00f93afb81d24168fc3b96ed5c06df07e",
  "sema_ref": "DissentSeek#89c2",
  "sema_stub": "89c2",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "quorum": "Quorum#a295",
      "confirmation_block": "ConfirmationBlock#20db",
      "understand": "Understand#c38c",
      "steelman_check": "SteelmanCheck#dd78"
    }
  }
}
```

---

## DriftWatch#5baa

```json
{
  "handle": "DriftWatch",
  "mechanism": "Reputation via micro-deviation detection. 1. Baseline: Establish behavioral frequency. 2. Sample: Continuous high-res observation. 3. Detect: Alert if {{distance}}(Current, Baseline) > 2 sigma. 4. Witness: Aggregated peer reports. It tracks behavioral consistency by monitoring deviations from a baseline {{aggregate}} of historical actions.",
  "gloss": "Reputation scoring via behavioral deviation from baseline (2-sigma alert)",
  "failure_modes": [
    "Witness collusion: Coordinated false drift reports (mitigated by random witness selection and meta-drift analysis on witness behavior).",
    "False reports: Single malicious witness (mitigated by N-of-M threshold requirement).",
    "Cold start: New agents have no baseline (mitigated by probationary period with higher friction, initial baseline borrowed from similar-role agents).",
    "Baseline gaming: {{agent}} varies early to establish wide baseline (mitigated by crystallization window limits and anomaly detection during bootstrap)."
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
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:DriftWatch#mh:SHA-256:5baa1af8d0368a6e4a3df1a876e6407f7225933d354a5406cf9f0cb631f42f38",
  "sema_ref": "DriftWatch#5baa",
  "sema_stub": "5baa",
  "dependencies": {
    "references": {
      "distance": "Distance#3e1e",
      "agent": "Agent#d183",
      "aggregate": "Aggregate#8c2a"
    }
  }
}
```

---

## EbbFlowSync#2af4

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
  "sema_id": "sema:EbbFlowSync#mh:SHA-256:2af47b0405b0951de55fc87ba9aed30674632d32b3838140769b712ddaea54ef",
  "sema_ref": "EbbFlowSync#2af4",
  "sema_stub": "2af4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "hysteresis": "Hysteresis#addb",
      "lock": "Lock#051c",
      "system": "System#e314",
      "transition": "Transition#072d",
      "state": "State#4d58",
      "global": "Global#803d"
    }
  }
}
```

---

## EjectionSeat#b71c

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
  "sema_id": "sema:EjectionSeat#mh:SHA-256:b71cbac714d333de39bd00c140ab214c1db4fa28db6562fbbbe75c160312ef30",
  "sema_ref": "EjectionSeat#b71c",
  "sema_stub": "b71c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "compensate": "Compensate#985e",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## EvaluatorOptimizer#2b2e

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
  "sema_id": "sema:EvaluatorOptimizer#mh:SHA-256:2b2e2e833d65dfc461cd8b6041f6bbe72324015b07daaebca65d1dc94aef139e",
  "sema_ref": "EvaluatorOptimizer#2b2e",
  "sema_stub": "2b2e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Optimize#b98b(Loop#a316)"
  ],
  "dependencies": {
    "references": {
      "optimize": "Optimize#b98b",
      "criteria": "Criteria#ef6b",
      "context": "Context#e88a",
      "loop": "Loop#a316",
      "meta_check": "MetaCheck#c660"
    }
  }
}
```

---

## ExpiringToken#8bc1

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
  "sema_id": "sema:ExpiringToken#mh:SHA-256:8bc1a75bca402bc51d11342914b50bfbb511875f537dcd5913e30f79b4c8e79e",
  "sema_ref": "ExpiringToken#8bc1",
  "sema_stub": "8bc1",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "decay": "Decay#1e8b",
      "bearer_token": "BearerToken#2fe9"
    }
  }
}
```

---

## FabricSharding#3946

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
  "sema_id": "sema:FabricSharding#mh:SHA-256:394664a2a586523570c90b0436aa1af99173f75f275f7efad3bf063b10a8d537",
  "sema_ref": "FabricSharding#3946",
  "sema_stub": "3946",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "parallelize": "Parallelize#b943",
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

## GenealogicalTrace#ca43

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
  "sema_id": "sema:GenealogicalTrace#mh:SHA-256:ca433cac70b66a0442fa4b4d2230ca55c6efc91c685dc82576dd3de085b6ae0c",
  "sema_ref": "GenealogicalTrace#ca43",
  "sema_stub": "ca43",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "deep": "Deep#89f0",
      "cite_back": "CiteBack#0a08",
      "trace_belief": "TraceBelief#3902"
    }
  }
}
```

---

## GlacialVault#0a81

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
  "sema_id": "sema:GlacialVault#mh:SHA-256:0a81732a0a3572f9829b71aeff53347a1451f44f1d793070ae821d52443f7a1a",
  "sema_ref": "GlacialVault#0a81",
  "sema_stub": "0a81",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "decay": "Decay#1e8b"
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

## GracefulDegradation#a692

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
  "sema_id": "sema:GracefulDegradation#mh:SHA-256:a6926db667fe18bcab72197b1cb10a0a3899e021a8bf12e1e1337e5e42cd12b0",
  "sema_ref": "GracefulDegradation#a692",
  "sema_stub": "a692",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "fail_closed": "FailClosed#59d8",
      "strategy": "Strategy#a0af",
      "message": "Message#f767"
    }
  }
}
```

---

## Handoff#d5e6

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
  "sema_id": "sema:Handoff#mh:SHA-256:d5e6c0bda8bc9b192609c2393439ed5794dd2c20fc43d1ac6f9ea3b8261234ae",
  "sema_ref": "Handoff#d5e6",
  "sema_stub": "d5e6",
  "dependencies": {
    "accepts": {
      "task": "Task#b290",
      "context": "Context#e88a",
      "responsibility": "Responsibility#b3b1"
    },
    "composes_with": {
      "delegate": "Delegate#60aa"
    },
    "references": {
      "state": "State#4d58",
      "agent": "Agent#d183"
    }
  }
}
```

---

## HeldRelease#33cb

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
      "range": "{Queue#7ca9, Drop, Reject}",
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
  "sema_id": "sema:HeldRelease#mh:SHA-256:33cb2db85bfe41d383182062afb9413016ec0cf4375eee2909f3e40626d459e8",
  "sema_ref": "HeldRelease#33cb",
  "sema_stub": "33cb",
  "dependencies": {
    "references": {
      "condition": "Condition#cbd5",
      "commitment_device": "CommitmentDevice#3aeb",
      "value": "Value#3c5d",
      "state": "State#4d58"
    },
    "accepts": {
      "unique_handle": "UniqueHandle#9b3c"
    }
  }
}
```

---

## IntentGap#b049

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
  "sema_ref": "IntentGap#b049",
  "sema_id": "sema:IntentGap#mh:SHA-256:b04973168f896cc6fedab491bc44f98fc3f700514f2a9d41f8bb70415d493b56",
  "sema_stub": "b049",
  "dependencies": {
    "references": {
      "decision": "Decision#934e",
      "outcome": "Outcome#9bf0"
    }
  }
}
```

---

## InternalConsistency#d572

```json
{
  "handle": "InternalConsistency",
  "mechanism": "A {{check}} that validates whether the components of an {{artifact}} adhere to the Principle of Non-Contradiction. It ensures that no two propositions within the {{context}} conflict with each other. Distinct from external {{validate}} (checking against a schema) or fact-checking (checking against reality).",
  "gloss": "Checking for self-contradiction",
  "signature": [
    "Check#410e(Context#e88a)"
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
  "sema_ref": "InternalConsistency#d572",
  "sema_id": "sema:InternalConsistency#mh:SHA-256:d5724f3cc4a62f48c8c1b4c6fbb16bd35f731cf8b2c880566673e70035faf65f",
  "sema_stub": "d572",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context": "Context#e88a",
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "check": "Check#410e",
      "validate": "Validate#aebf"
    }
  }
}
```

---

## InvariantFilter#0b7c

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
  "sema_id": "sema:InvariantFilter#mh:SHA-256:0b7cfb40a7410861ee9ab5a6193f513e6abb22b7f8ca59144163909465069fd2",
  "sema_ref": "InvariantFilter#0b7c",
  "sema_stub": "0b7c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "accepts": {
      "rule_set": "RuleSet#ac40",
      "message": "Message#f767"
    },
    "references": {
      "stream": "Stream#22f3",
      "check": "Check#410e"
    }
  }
}
```

---

## LatticeCommit#1eed

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
      "RootHashGossip#2bac"
    ],
    "ring": 2
  },
  "sema_id": "sema:LatticeCommit#mh:SHA-256:1eed855c184a7af0afda0ad6cf5e2571ef112bf31647915190d1818238d38113",
  "sema_ref": "LatticeCommit#1eed",
  "sema_stub": "1eed",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "topology": "Topology#2408",
      "quorum": "Quorum#a295",
      "state_transition": "StateTransition#9e61",
      "check": "Check#410e"
    }
  }
}
```

---

## MemeticSeed#909b

```json
{
  "handle": "MemeticSeed",
  "mechanism": "{{agent}} actively broadcasts a subset of its ontology to neighbors, offering favorable terms ({{yield}}) to those who adopt it, thereby reducing its own future translation costs ({{translation_proxy}}). Standards are adopted not because they are 'true', but because they are subsidized. It subsidizes adoption via {{yield}} and {{translation_proxy}}, broadcasting the standard through an {{explain_beacon}}.",
  "gloss": "Viral propagation of semantic standards via economic subsidy",
  "invariants": [
    "Fidelity: Propagated ontology must be isomorphic to source",
    "Subsidy {{gradient}}: Adoption Incentive > Switching Cost"
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
  "sema_id": "sema:MemeticSeed#mh:SHA-256:909bb23ae0a1949f924dc1012db17f43c5dc1fb7d7893075c2378eb19ec09e01",
  "sema_ref": "MemeticSeed#909b",
  "sema_stub": "909b",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "gradient": "Gradient#480b",
      "translation_proxy": "TranslationProxy#3422",
      "explain_beacon": "ExplainBeacon#9d6d",
      "yield": "Yield#0de8",
      "agent": "Agent#d183"
    }
  }
}
```

---

## ModestClaim#481e

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
  "sema_id": "sema:ModestClaim#mh:SHA-256:481ec98ce0818663446de9661e338477983a02d30778b01b2878c47460e04876",
  "sema_ref": "ModestClaim#481e",
  "sema_stub": "481e",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "reframe": "Reframe#44c5",
      "problem": "Problem#64d0",
      "system": "System#e314",
      "epistemic_calibrate": "EpistemicCalibrate#3e32",
      "identity": "Identity#626c",
      "agent": "Agent#d183"
    }
  }
}
```

---

## MonotonicCounter#c7ab

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
  "sema_id": "sema:MonotonicCounter#mh:SHA-256:c7ab5a704cf6435c4e976029c884f170c39d2dfdfa3d22d8b819cf63cbdc9f0c",
  "sema_ref": "MonotonicCounter#c7ab",
  "sema_stub": "c7ab",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "state_lock": "StateLock#5602",
      "value": "Value#3c5d"
    }
  }
}
```

---

## Nucleate#e094

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
    "{{conservation}} of Mass: Nucleation cannot create agents; it only aggregates existing {{trace}} density.",
    "Critical Mass: Process starts only when N > SeedThreshold",
    "Nucleation ONLY at supersaturated sites."
  ],
  "preconditions": [
    "Field of agents/particles is present"
  ],
  "postconditions": [
    "{{phase_transition}} complete (Liquid \u2192 Solid)"
  ],
  "_meta": {
    "tier": 1,
    "layer": "Society",
    "category": "Protocols",
    "ring": 1
  },
  "sema_id": "sema:Nucleate#mh:SHA-256:e0944d1b5aca43aa6ae8095d4f66d95d4ce23229b7565923bd1f05760197f21a",
  "sema_ref": "Nucleate#e094",
  "sema_stub": "e094",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "conservation": "Conservation#d63a",
      "crystallize": "Crystallize#f680",
      "system": "System#e314",
      "rally": "Rally#15b1",
      "trace": "Trace#2836",
      "phase_transition": "PhaseTransition#edf8"
    }
  }
}
```

---

## OptimisticSolver#2698

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
    "caution": "Executes without pre-action verification. Ensure irreversible actions have compensation or sandboxing, or use RigorousSolver#483b at those boundaries."
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "derived_from": "Solver#4ed4",
  "sema_id": "sema:OptimisticSolver#mh:SHA-256:26981ac90612e6fdb30197da0f4104d77210607ccb81933dc4d535c8f4023f62",
  "sema_ref": "OptimisticSolver#2698",
  "sema_stub": "2698",
  "dependencies": {
    "references": {
      "polymorphic_solver": "PolymorphicSolver#bbe4",
      "rigorous_solver": "RigorousSolver#483b",
      "parallel": "Parallel#3181"
    },
    "composes_with": {
      "atomic_bid": "AtomicBid#1800",
      "compensate": "Compensate#985e",
      "reflexion": "Reflexion#3b52",
      "pathway_memory": "PathwayMemory#7899",
      "compute_budget": "ComputeBudget#8a42"
    }
  }
}
```

---

## Oracle#6b9f

```json
{
  "handle": "Oracle",
  "mechanism": "A trusted entity that injects off-chain truth (Reality) into the system by cryptographically signing data. It resolves conditions in {{held_release}} and verifies outcomes for prediction markets.",
  "gloss": "Cryptographic truth source",
  "invariants": [
    "Non-Interference: The Oracle reports on reality but does not alter it.",
    "Consistency: Answers to the same query at the same time must be identical."
  ],
  "sema_id": "sema:Oracle#mh:SHA-256:6b9faa34456f1e1f284da6666c64e12dad36bbac74a2208078894eee88ca2220",
  "sema_ref": "Oracle#6b9f",
  "sema_stub": "6b9f",
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
      "held_release": "HeldRelease#33cb"
    }
  }
}
```

---

## OrchestrationLoop#c836

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
      "LayeredCheck#0dbc"
    ]
  },
  "sema_id": "sema:OrchestrationLoop#mh:SHA-256:c836308a3d2097c48f6843591b6c6c154d25d0fbe683f0f019b86d28d1ac5c4a",
  "sema_ref": "OrchestrationLoop#c836",
  "sema_stub": "c836",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Workflow#eaa9(Rollout#5475)"
  ],
  "dependencies": {
    "composes_with": {
      "request_framing": "RequestFraming#b776",
      "manifest_planning": "ManifestPlanning#b9ad",
      "rollout": "Rollout#5475"
    },
    "references": {
      "rollout_manifest": "RolloutManifest#5596",
      "receptivity_gate": "ReceptivityGate#0d20",
      "workflow": "Workflow#eaa9",
      "accept_spec": "AcceptSpec#762e",
      "execution_manifest": "ExecutionManifest#6cf5",
      "frame_spec": "FrameSpec#edff"
    }
  }
}
```

---

## OsmoticFilter#6d82

```json
{
  "handle": "OsmoticFilter",
  "mechanism": "Agents operate inside a semi-permeable membrane. Inbound messages are rejected unless they carry sufficient 'pressure' (stake, reputation, or relevance score) to overcome the membrane's current tension. The filter supports Multi-Solvent extraction, allowing different types of pressure (Money vs Trust) to be converted at defined rates per the {{accepted_solvents}} criteria. It uses {{hysteresis}} to prevent oscillation and {{canary}} messages to test permeability.",
  "gloss": "Spam prevention via pressure thresholds",
  "failure_modes": [
    "Starvation of low-stake but high-importance messages (mitigated by Whitelist)."
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
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:OsmoticFilter#mh:SHA-256:6d82bdbb7cbf0733c756ae35875db76ea3d6c8d11e3006cb6709c161fdd66e69",
  "sema_ref": "OsmoticFilter#6d82",
  "sema_stub": "6d82",
  "dependencies": {
    "references": {
      "canary": "Canary#86d6",
      "hysteresis": "Hysteresis#addb"
    },
    "accepts": {
      "criteria": "Criteria#ef6b"
    }
  }
}
```

---

## PatternEmergence#77c5

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
  "sema_id": "sema:PatternEmergence#mh:SHA-256:77c51abd834594d88f4b9fdd95391a42228c7777507f8bbf7133bf5f53d78391",
  "sema_ref": "PatternEmergence#77c5",
  "sema_stub": "77c5",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "pattern_discovery": "PatternDiscovery#99dd",
      "mint_when_friction": "MintWhenFriction#4e33",
      "noise": "Noise#3d9a",
      "system": "System#e314",
      "generalize": "Generalize#9684",
      "uptake_as_ground": "UptakeAsGround#c5cb",
      "agent": "Agent#d183",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## PatternSketch#c5d8

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
  "sema_id": "sema:PatternSketch#mh:SHA-256:c5d85d3c467e9521cf3a111ae75fbfb779eacf9e8ba9bdf96ac2b661c197bad8",
  "sema_ref": "PatternSketch#c5d8",
  "sema_stub": "c5d8",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "agent": "Agent#d183",
      "skeleton_of_thought": "SkeletonOfThought#ab3e"
    }
  }
}
```

---

## PermissionEscalate#e2d8

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
  "sema_id": "sema:PermissionEscalate#mh:SHA-256:e2d8d33afd8644ddad1b450e1d48f1eb46242c1de805c69a1ae533313ac79660",
  "sema_ref": "PermissionEscalate#e2d8",
  "sema_stub": "e2d8",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "tiered_access": "TieredAccess#6722",
      "agent": "Agent#d183",
      "human_approve": "HumanApprove#6434"
    }
  }
}
```

---

## PhasedRefinement#11af

```json
{
  "handle": "PhasedRefinement",
  "mechanism": "A structured {{refine}} strategy that improves an {{artifact}} through a defined {{sequence}} of passes, where each pass targets a specific layer of abstraction (e.g., {{reason}} (logic) -> {{structural_coaching}} (structure) -> {{aesthetics}} (polish)). It uses a {{gate}} to prevent premature optimization by ensuring deep structural issues are resolved before surface-level polishing begins.",
  "gloss": "Layered, multi-pass improvement",
  "signature": [
    "Refine#78b7(Artifact#6254)"
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
  "sema_ref": "PhasedRefinement#11af",
  "sema_id": "sema:PhasedRefinement#mh:SHA-256:11afaa3e3784b6007ea101affd09ceb75c3f46882bedad0567766fb0900c085a",
  "sema_stub": "11af",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "structural_coaching": "StructuralCoaching#824a",
      "reason": "Reason#3067",
      "aesthetics": "Aesthetics#c912",
      "artifact": "Artifact#6254"
    },
    "composes_with": {
      "sequence": "Sequence#b0b8",
      "gate": "Gate#02f6",
      "refine": "Refine#78b7"
    }
  }
}
```

---

## PromiseGraph#b839

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
  "sema_id": "sema:PromiseGraph#mh:SHA-256:b8391aa549f3afd19542e41ae0812b1a5d6a67ecca2542c666bae12b7c9b46b2",
  "sema_ref": "PromiseGraph#b839",
  "sema_stub": "b839",
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
      "negative_proof": "NegativeProof#14ee",
      "agent": "Agent#d183"
    }
  }
}
```

---

## PromptChain#7f67

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
      "range": "{Strict, Retry#cb3a, Skip}",
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
  "sema_id": "sema:PromptChain#mh:SHA-256:7f67f2925e5b99a4a3752cbf9bd736f5ebd2562f7ca6986b94cbe91d9ae73707",
  "sema_ref": "PromptChain#7f67",
  "sema_stub": "7f67",
  "dependencies": {
    "references": {
      "input_guard": "InputGuard#7353",
      "chain": "Chain#711e",
      "accept_spec": "AcceptSpec#762e",
      "tool_invoke": "ToolInvoke#bd2b",
      "gate": "Gate#02f6",
      "retry": "Retry#cb3a",
      "sequence": "Sequence#b0b8"
    },
    "accepts": {
      "task": "Task#b290"
    }
  }
}
```

---

## PropheticQuorum#44ae

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
      "Quorum#a295",
      "SimulationTrace#1b91",
      "RegimeSense#d8f0"
    ],
    "ring": 1
  },
  "sema_id": "sema:PropheticQuorum#mh:SHA-256:44ae526c00d60dbf7c3c6cf562872251407a54fd7d18a50128cb964fb541eb4b",
  "sema_ref": "PropheticQuorum#44ae",
  "sema_stub": "44ae",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "simulation_trace": "SimulationTrace#1b91",
      "value": "Value#3c5d",
      "check": "Check#410e",
      "state": "State#4d58",
      "simulation": "Simulation#398f",
      "vote": "Vote#625c",
      "normative_judge": "NormativeJudge#1900"
    }
  }
}
```

---

## QuorumPulse#0ece

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
  "sema_id": "sema:QuorumPulse#mh:SHA-256:0eceaaf1ced92b3b9716e8e1a6f3b44a6ed96aa719e1e2612df32781e3cb0837",
  "sema_ref": "QuorumPulse#0ece",
  "sema_stub": "0ece",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "quorum": "Quorum#a295",
      "state": "State#4d58",
      "heartbeat": "Heartbeat#8e36",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## RealizationProtocol#8c19

```json
{
  "handle": "RealizationProtocol",
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
    "SolverTree#65f2(Outcome#9bf0)"
  ],
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:RealizationProtocol#mh:SHA-256:8c19456a357e89a16e2da763e14b958d03cfe93bbfb8dfb24c635dae3a236b55",
  "sema_ref": "RealizationProtocol#8c19",
  "sema_stub": "8c19",
  "dependencies": {
    "references": {
      "polymorphic_solver": "PolymorphicSolver#bbe4",
      "solver_tree": "SolverTree#65f2",
      "realizable": "Realizable#613e",
      "execution_manifest": "ExecutionManifest#6cf5",
      "frame_spec": "FrameSpec#edff"
    },
    "composes_with": {
      "manifest_planning": "ManifestPlanning#b9ad",
      "interpret": "Interpret#8ee3",
      "rollout": "Rollout#5475"
    },
    "yields": {
      "outcome": "Outcome#9bf0"
    }
  }
}
```

---

## ReceptivityGate#0d20

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
    "caution": "Required at any Feedback#dc36 surface exposed to untrusted downstream consumers. Without it, the Solver#4ed4 absorbs fabricated penalties as if they were genuine learning signal."
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:ReceptivityGate#mh:SHA-256:0d20a814990c6ebc6e89aab0e0029baad72b5270588b3be453cbc704067b6144",
  "sema_ref": "ReceptivityGate#0d20",
  "sema_stub": "0d20",
  "dependencies": {
    "references": {
      "failure_trace": "FailureTrace#b1f0",
      "accept_spec": "AcceptSpec#762e",
      "pathway_memory": "PathwayMemory#7899"
    },
    "composes_with": {
      "validate": "Validate#aebf"
    }
  }
}
```

---

## ReversibilityCheck#f055

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
  "sema_id": "sema:ReversibilityCheck#mh:SHA-256:f055085a0c6636bce52a660ade47246078ae342499b353df3b5bf45129f7735c",
  "sema_ref": "ReversibilityCheck#f055",
  "sema_stub": "f055",
  "signature": [
    "Check#410e(Reversibility#bf79)"
  ],
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "reversibility": "Reversibility#bf79",
      "world_reversible": "WorldReversible#f664",
      "human_approve": "HumanApprove#6434"
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
      "system": "System#e314",
      "state": "State#4d58"
    }
  }
}
```

---

## Rollout#5475

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
  "sema_id": "sema:Rollout#mh:SHA-256:54750268d2da96defb669783bcbbe57bdcbe6e8f66251dcff0e82f51493df555",
  "sema_ref": "Rollout#5475",
  "sema_stub": "5475",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Act#dc2d(ExecutionManifest#6cf5)"
  ],
  "dependencies": {
    "yields": {
      "monitor_report": "MonitorReport#063c",
      "rollout_manifest": "RolloutManifest#5596"
    },
    "accepts": {
      "execution_manifest": "ExecutionManifest#6cf5"
    },
    "references": {
      "manifest_planning": "ManifestPlanning#b9ad",
      "build": "Build#8143",
      "system": "System#e314",
      "world_reversible": "WorldReversible#f664",
      "state": "State#4d58",
      "act": "Act#dc2d",
      "spec": "Spec#68b4"
    },
    "composes_with": {
      "compensate": "Compensate#985e",
      "canary": "Canary#86d6",
      "circuit_breaker": "CircuitBreaker#0577",
      "ejection_seat": "EjectionSeat#b71c"
    }
  }
}
```

---

## RolloutWatch#20b5

```json
{
  "handle": "RolloutWatch",
  "derived_from": "Monitor#6773",
  "gloss": "Continuous verification of deployed state against manifest",
  "mechanism": "The final {{state}} of workflow orchestration. It implements {{monitor}} by using {{observe}} to track the deployed {{solution}}'s performance on the {{system}} against the 'Definition of Done' defined in the {{rollout_manifest}}. If reality deviates from the plan (e.g., error rate spikes), it routes evidence back upstream via a {{monitor_report}}. It closes the feedback {{loop}}.",
  "signature": [
    "Observe#abc0(System#e314, RolloutManifest#5596)"
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
      "DriftWatch#5baa",
      "Reflexion#3b52"
    ]
  },
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:RolloutWatch#mh:SHA-256:20b55fcd88cf88b6036edd5b974cd57018e5268d3b54c91747b1214113a6c83d",
  "sema_ref": "RolloutWatch#20b5",
  "sema_stub": "20b5",
  "dependencies": {
    "composes_with": {
      "loop": "Loop#a316",
      "observe": "Observe#abc0"
    },
    "yields": {
      "monitor_report": "MonitorReport#063c"
    },
    "references": {
      "system": "System#e314",
      "monitor": "Monitor#6773",
      "solution": "Solution#445c",
      "state": "State#4d58"
    },
    "accepts": {
      "rollout_manifest": "RolloutManifest#5596"
    }
  }
}
```

---

## RootHashGossip#2bac

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
  "sema_id": "sema:RootHashGossip#mh:SHA-256:2bac6fbf3454dff8cf83206aae939a4b79595d0e72a4576ecfc720f43d1ffdbe",
  "sema_ref": "RootHashGossip#2bac",
  "sema_stub": "2bac",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "loop": "Loop#a316"
    }
  }
}
```

---

## ShoutWhisper#7204

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
      "Route#34c7"
    ],
    "ring": 1
  },
  "sema_id": "sema:ShoutWhisper#mh:SHA-256:72045961851506fcc23a5b4d3bd7daba60634a529ef5146fea7d39b882271bb1",
  "sema_ref": "ShoutWhisper#7204",
  "sema_stub": "7204",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "check": "Check#410e",
      "global": "Global#803d"
    }
  }
}
```

---

## SignalReflection#9f56

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
  "sema_id": "sema:SignalReflection#mh:SHA-256:9f5601289afd8ec3e2b59b75e85db19bce1471714aee8dd53a6155900b59d0b7",
  "sema_ref": "SignalReflection#9f56",
  "sema_stub": "9f56",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "message": "Message#f767",
      "agent": "Agent#d183",
      "spectral_tune": "SpectralTune#b25a"
    }
  }
}
```

---

## SolverNode#86bb

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
  "sema_ref": "SolverNode#86bb",
  "sema_id": "sema:SolverNode#mh:SHA-256:86bb3f560e1394d3f684b4811a6c42ede31eac8ba9738355f8c0c33097150cdb",
  "sema_stub": "86bb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "solver_manifest": "SolverManifest#11ea",
      "budget": "Budget#0934",
      "solution": "Solution#445c",
      "problem_space": "ProblemSpace#6e74",
      "responsibility": "Responsibility#b3b1",
      "localized_learning": "LocalizedLearning#eb5a"
    }
  }
}
```

---

## SomaticMarker#7250

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
      "Proprioception#ec6c"
    ],
    "ring": 2
  },
  "sema_id": "sema:SomaticMarker#mh:SHA-256:7250740ec4cb55bd03e0b2a0070c21795cd61e18247c06deb53f41e778ed032f",
  "sema_ref": "SomaticMarker#7250",
  "sema_stub": "7250",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "task": "Task#b290",
      "correlation": "Correlation#148d",
      "signal": "Signal#f39d"
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
      "OntologyHandshake#8443"
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

## StateLock#5602

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
    "layer": "Society",
    "category": "Protocols",
    "ring": 0,
    "tier": 1,
    "caution": "Exclusive state access \u2014 misuse enables denial of service via lock starvation."
  },
  "signature": [
    "Lock#051c(State#4d58)"
  ],
  "sema_ref": "StateLock#5602",
  "sema_id": "sema:StateLock#mh:SHA-256:560229dacf3ebeebd3461dd3c4a9553d3658bf0f447741b31e38e0418db45e3a",
  "sema_stub": "5602",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "backoff": "Backoff#c6d1",
      "lock": "Lock#051c",
      "cooldown": "Cooldown#6eb2",
      "state": "State#4d58",
      "actor": "Actor#57f6"
    }
  }
}
```

---

## Stigmergy#53d4

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
    "layer": "Society",
    "category": "Protocols",
    "related": [
      "sema:GhostTrail#mh:SHA-256:ec5b2ca0ee009f2aec90a8fb2cec9ee5feb29a1d98f20a7211d973b26a629e6a",
      "Signal#f39d"
    ],
    "ring": 0
  },
  "sema_id": "sema:Stigmergy#mh:SHA-256:53d4073df67b0c81011a3c328c1994e4d84c6d9e5c6f0c3f944ee7d9b1c34aa2",
  "sema_ref": "Stigmergy#53d4",
  "sema_stub": "53d4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "trace": "Trace#2836",
      "decay": "Decay#1e8b"
    }
  }
}
```

---

## StructuralCoaching#824a

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
  "sema_id": "sema:StructuralCoaching#mh:SHA-256:824a3098be26a7e5c1e62cc6f37052416d2f03d0d3bd1d395288ef12b8c27270",
  "sema_ref": "StructuralCoaching#824a",
  "sema_stub": "824a",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "feedback": "Feedback#dc36",
      "creative": "Creative#5574",
      "critique": "Critique#4e43",
      "invert": "Invert#d39f"
    }
  }
}
```

---

## SynergisticMode#fa9f

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
  "sema_id": "sema:SynergisticMode#mh:SHA-256:fa9f9c350f4b30263a89276c00ae4ed39170666ede1ced92daa88a2ceedcae52",
  "sema_ref": "SynergisticMode#fa9f",
  "sema_stub": "fa9f",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "compose": "Compose#389f",
      "ontology_handshake": "OntologyHandshake#8443",
      "system": "System#e314",
      "accept_spec": "AcceptSpec#762e",
      "mode": "Mode#3df1",
      "agent": "Agent#d183",
      "signal": "Signal#f39d"
    }
  }
}
```

---

## Taper#4ce4

```json
{
  "handle": "Taper",
  "gloss": "Multi-stage filter of increasing strictness: wide high-entropy input to narrow certain output",
  "mechanism": "A multi-stage {{sequence}} process that accepts wide-aperture, high-entropy inputs and progressively filters them through {{gate}}s or {{tri_gate}}s of increasing strictness. Each stage: (1) Applies a stage-specific acceptance threshold, acting as a functional {{depth_governor}}; (2) Reduces the candidate set to {{compress}} the search space; (3) Increases certainty. Final stage outputs zero-entropy signal (deterministic, unambiguous). Failure modes are stage-appropriate: Early stages optimize for recall (don't lose valid signals), Late stages optimize for precision (don't pass garbage).",
  "signature": [
    "Sequence#b0b8(Gate#02f6)"
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
  "sema_ref": "Taper#4ce4",
  "sema_id": "sema:Taper#mh:SHA-256:4ce41dce11bb018f87f56c7019d23b1e1fda5747fb829618d79264f64b4a106d",
  "sema_stub": "4ce4",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "tri_gate": "TriGate#66aa",
      "sequence": "Sequence#b0b8",
      "gate": "Gate#02f6"
    },
    "references": {
      "compress": "Compress#0967",
      "depth_governor": "DepthGovernor#8f06"
    }
  }
}
```

---

## ThreeLevelCollision#9e89

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
  "sema_id": "sema:ThreeLevelCollision#mh:SHA-256:9e893b211139022decb998c0679fd54082fb4146fbbd94d28a58d2d519c0c3f4",
  "sema_ref": "ThreeLevelCollision#9e89",
  "sema_stub": "9e89",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "fail_closed": "FailClosed#59d8",
      "identity": "Identity#626c"
    }
  }
}
```

---

## TieredAccess#6722

```json
{
  "handle": "TieredAccess",
  "mechanism": "Central 'massive' agents (high authority) create a gravity well. The cost to interact with an agent increases the closer you get to the center. This naturally filters low-value queries to the periphery and reserves core attention for high-value interactions. Utilizes {{bearer_token}}.",
  "gloss": "Cost-distance indexing",
  "failure_modes": [
    "Metric Divergence: Agents disagree on distance calculation, causing payment rejection.",
    "Center becomes economically inaccessible to low-resource agents."
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
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:TieredAccess#mh:SHA-256:672204bbe348969d6d06ce2170e45f4c58f43e697ee2f68a67c9899f6c79229e",
  "sema_ref": "TieredAccess#6722",
  "sema_stub": "6722",
  "dependencies": {
    "references": {
      "identity": "Identity#626c",
      "agent": "Agent#d183"
    },
    "composes_with": {
      "bearer_token": "BearerToken#2fe9"
    }
  }
}
```

---

## ToolDiscovery#61fb

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
    "Discover#aa70(ToolInvoke#bd2b)"
  ],
  "_meta": {
    "layer": "Society",
    "category": "Protocols",
    "ring": 1,
    "tier": 1,
    "related": [
      "AgentDiscover#5a6c"
    ]
  },
  "sema_ref": "ToolDiscovery#61fb",
  "sema_id": "sema:ToolDiscovery#mh:SHA-256:61fbd23f9b7eaf220570075e3688e60fb40cf12822701fb4e486de6ed7e2f9e8",
  "sema_stub": "61fb",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "composes_with": {
      "compatibility_check": "CompatibilityCheck#3abb",
      "fail_closed": "FailClosed#59d8",
      "tool_invoke": "ToolInvoke#bd2b"
    },
    "references": {
      "task": "Task#b290",
      "card": "Card#f63d",
      "discover": "Discover#aa70",
      "context_first": "ContextFirst#dbb4",
      "agent": "Agent#d183"
    },
    "yields": {
      "result": "Result#f29e"
    }
  }
}
```

---

## TranslationProxy#3422

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
  "sema_id": "sema:TranslationProxy#mh:SHA-256:342219e51cc568b1133fb7eea62a611a0ad65304d0ec26c569e1a8e40765ce61",
  "sema_ref": "TranslationProxy#3422",
  "sema_stub": "3422",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "signature": [
    "Translate#edeb(Protocol#7e1c)"
  ],
  "dependencies": {
    "references": {
      "compare": "Compare#4881",
      "translate": "Translate#edeb",
      "ontology_handshake": "OntologyHandshake#8443",
      "message": "Message#f767",
      "protocol": "Protocol#7e1c"
    }
  }
}
```

---

## UniqueHandle#9b3c

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
  "sema_id": "sema:UniqueHandle#mh:SHA-256:9b3c01474f6bde69d161fbaeffc51da51a91b77e7a42122d3d579eb31a9a7d20",
  "sema_ref": "UniqueHandle#9b3c",
  "sema_stub": "9b3c",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "break": "Break#0bb3",
      "state_lock": "StateLock#5602",
      "agent": "Agent#d183"
    }
  }
}
```

---

## UptakeAsGround#c5cb

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
    "Pragmatic Validation (Wittgenstein's Razor): Successful {{task}} completion is the only proof of shared meaning \u2014 meaning is use. A pattern with zero successful coordination has no semantic mass."
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
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "sema_id": "sema:UptakeAsGround#mh:SHA-256:c5cbf1f2f52a90ba2648a826ff8421d334e5b32bf892d9b5578f7ec013616a69",
  "sema_ref": "UptakeAsGround#c5cb",
  "sema_stub": "c5cb",
  "dependencies": {
    "references": {
      "modest_claim": "ModestClaim#481e",
      "task": "Task#b290"
    }
  }
}
```

---

## UptakeOverTimestamp#d3dd

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
  "sema_id": "sema:UptakeOverTimestamp#mh:SHA-256:d3dd545439e2903c5f4e0bfb056bc94bb18b2ef75a2137ade6a3d6d56dd4a346",
  "sema_ref": "UptakeOverTimestamp#d3dd",
  "sema_stub": "d3dd",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "uptake_as_ground": "UptakeAsGround#c5cb",
      "problem": "Problem#64d0"
    }
  }
}
```

---

## WorkerMode#3d61

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
  "sema_id": "sema:WorkerMode#mh:SHA-256:3d616acccfc84b9abafe7ec564181b783f30cf59fd629c0e29771ae9d2074e2a",
  "sema_ref": "WorkerMode#3d61",
  "sema_stub": "3d61",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "context_switch": "ContextSwitch#3a3c",
      "task": "Task#b290",
      "solver_node": "SolverNode#86bb",
      "lock": "Lock#051c",
      "context": "Context#e88a",
      "solution": "Solution#445c",
      "state": "State#4d58",
      "mode": "Mode#3df1",
      "identity": "Identity#626c",
      "agent": "Agent#d183"
    },
    "accepts": {
      "solver_manifest": "SolverManifest#11ea"
    }
  }
}
```

---

## Workflow#eaa9

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
  "sema_id": "sema:Workflow#mh:SHA-256:eaa9b0edcdad11739fabc7d752baf0bacead4a58fe9c04fb61c45cbd1aae5175",
  "sema_ref": "Workflow#eaa9",
  "sema_stub": "eaa9",
  "sema_layer": "Society",
  "sema_category": "Protocols",
  "dependencies": {
    "references": {
      "step": "Step#5f22",
      "accept_spec": "AcceptSpec#762e",
      "role": "Role#dcb2",
      "artifact": "Artifact#6254",
      "solver": "Solver#4ed4"
    }
  }
}
```

---

