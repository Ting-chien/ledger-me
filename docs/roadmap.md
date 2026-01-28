# Feature Roadmap

Feature roadmap shows features we want to add, update or fix. Requirements should be written in the scope of version and module, and will be marked as DONE if implemented.

## v1.3.0 - Big UI improvement !

Report Page (`/reports`)
- [x] **Month Navigator**: Allow users to switch between months to view historical data.
- [x] **Month-End Projection**: Estimate total monthly expenses based on current daily spending average.
- [x] **MoM Comparison**: Month-over-Month comparison to show spending trends vs previous periods.

Transaction Page (`/transactions`)
- [x] **Daily Grouping**: Group transactions by date (e.g., "Today", "Yesterday") for better readability.
- [x] **RESTful API Improvements**: Return JSON/204 for PUT/DELETE actions to handle UI updates via JS instead of page reloads.
- [x] **Data Validation**: enhance backend validation for dates and amounts.
- [x] Optimize calander UI in transaction modal
