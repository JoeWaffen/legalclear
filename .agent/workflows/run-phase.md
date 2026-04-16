# Workflow: /run-phase

Execute a LegalClear build phase completely.

Steps:
1. Read the phase instructions carefully.
2. Switch to Planning mode and show the implementation plan.
3. Wait for approval before writing any files.
4. Execute the implementation.
5. Run the verification test for this phase.
6. If any assertion fails, fix the error and re-run.
7. Only print PHASE N COMPLETE when all assertions pass.
8. Do not proceed to the next phase automatically.
