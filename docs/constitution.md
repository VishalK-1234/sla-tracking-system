# Project Constitution — SLA Desk

1. **Spec-first delivery:** requirements, plan, and tasks must be reviewed before implementation.
2. **Correct SLA semantics:** priority targets are explicit; all timestamps are UTC; calendar hours include weekends.
3. **Derived overdue state:** overdue is computed from `due_at` and current time; it is never manually toggled or persisted as truth.
4. **Separation of concerns:** API routes, business rules, persistence, and UI components remain separate.
5. **Validation:** reject blank titles/descriptions and unsupported priorities/statuses at the API boundary.
6. **Testability:** SLA calculations, overdue boundaries, API behavior, UI behavior, and a critical E2E flow must be tested.
7. **Accessible UI:** semantic controls, visible focus, labels, responsive layouts, and readable status indicators.
8. **Training security:** no real credentials or sensitive data; clearly document the absence of production authentication.
