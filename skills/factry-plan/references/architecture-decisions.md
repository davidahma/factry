# Planning a change across a boundary

Read the nearest contract and follow one real caller before drawing the boundary. Use the repo's existing design records to understand why it exists. The examples below show how a design choice affects the order of work and the evidence a reviewer needs.

| Change | Decision the plan should settle | Evidence to hand the implementer |
| --- | --- | --- |
| A writer changes a persisted format. | Which component owns the format? Can an old reader open a new record? Can the old binary still run after the new writer has committed data? | List supported reader/writer pairs and a real record for each. If an old reader rejects new output, upgrade readers first and identify the last reversible step. |
| A caller retries a write after a timeout. | Where does the effect become durable? Who can tell whether an earlier attempt completed? | Locate the authority for the result. In a disposable environment, lose the reply after the write and repeat the same request. Specify the expected record count and caller response. |
| Two workers update the same state. | Which update must win, and what tells the losing worker to retry or stop? | Specify an interleaving of the two writes and what the reader must see afterwards. |
| One request now fans out to more work. | Which workload exercises the change and which latency or resource limit matters to users? | Identify a representative input size, the existing budget or baseline, and where the operator can observe degradation. |

Record an architectural decision when future maintainers need the rationale to change a public contract, state owner, failure behavior, trust boundary or consequential performance tradeoff. Follow the target project's convention. If it has no template, a paragraph in the requested plan can name the alternatives, choice, consequences and rollback limit. Treat missing repository facts as questions or testable assumptions.
