# Checks to run while making a patch

Use the target project's test entry points, dependency pins and required gates. Select extra cases from what the patch changes.

- **Parser or API.** Reproduce a reported input through the public entry point. Exercise a nearby valid input that must keep its old meaning. For structured data, use the documented parser or structured API and check the resulting values, error behavior and output format a caller consumes.
- **Persisted format.** Keep an example written by the prior version. Read it through the new code and run the old reader on new data if that combination is supported during rollout. Check whether reverting code would leave unreadable data. A coordinated reader and writer can agree on a broken format when tested only with each other.
- **Retry or partial write.** Use a local substitute that preserves the operation's commit point. Interrupt after the effect and before confirmation, then try the request again. Inspect the durable result and what the caller receives. Keep live accounts and production state out of the exercise.
- **Documented or packaged interface.** Run the affected command or example with its documented working directory and inputs. When packaging changes, try the built artifact from outside the source tree so an unshipped file cannot satisfy the check.

Give the next engineer a short account of the original failure, what now passes, and any case you could not exercise. A regression should fail if the defect returns while continuing to pass for an equivalent correct implementation.
