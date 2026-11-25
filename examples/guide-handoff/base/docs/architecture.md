# Receipt format and rollout

The append-only receipt stream is the source of truth for the total. Readers and writers can deploy or roll back independently. The previous reader requires `total_pence` on each record. It ignores additional fields. Reinstalling that reader does not rewrite data already appended.

During the field rename, the writer must emit `amount_minor` and `total_pence` with equal integer GBP minor-unit values. The new reader must also total historical records that only contain `total_pence`. As directed by the issue, it accepts records that supply only `amount_minor`. A separate decision by the format owner is required to remove `total_pence` from newly written receipts once the rollback reader no longer needs it.

A rollback must be able to total a stream containing both an old record and a record written during the rollout. Record the compatibility check in the handoff for format changes.
