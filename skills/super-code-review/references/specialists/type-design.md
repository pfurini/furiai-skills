# Specialist: Type design

Job: types with strong, clearly-expressed, enforced invariants. Make illegal states unrepresentable — but don't make simple things complex. Pragmatic.

## Scope
New/changed types, interfaces, constructors, factories, setters, public API surface.

## Find the invariants
Data-consistency (fields that must stay in sync), valid-state combos, transition rules, field relationships, bounds (non-null/non-empty/min-max), business rules.

## Rate 4 dimensions (1-10)
| Dim | 9-10 | 1-2 |
|---|---|---|
| Encapsulation | internals hidden, minimal complete interface | fully exposed, invariants violable from outside |
| Invariant expression | self-documenting, compile-time | not expressed in the type at all |
| Invariant usefulness | prevents real bugs, business-aligned | doesn't prevent anything / over-restrictive |
| Invariant enforcement | invalid instance impossible | relies on callers, easy to bypass |

## Anti-patterns
| Pattern | Severity |
|---|---|
| Exposed mutable internals | High |
| Doc-only invariant (enforced by a comment) | High |
| No constructor/factory validation | High |
| Inconsistent enforcement (some paths guarded, others not) | High |
| Invariant maintained by callers, not the type | High |
| Boolean-flag soup (2ⁿ states, many invalid) → use discriminated union | High |
| Anemic data-bag / god-type | Medium |
| Nullable leaking across the API boundary that should be normalized | Medium |

## Judge suggestions
Complexity cost vs benefit, breaking-change disruption, fits codebase conventions, perf of validation, usability. Don't demand perfect scores; good is enough.

## Output
Per type: `file:line` · 4 scores + 1-line each · concerns (severity, code) · improvements (priority + complexity + before/after + trade-off). Prefer compile-time over runtime enforcement.
