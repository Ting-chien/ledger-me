# Feature Roadmap

Feature roadmap shows features we want to add, update or fix. Requirements should be written in the scope of version and module, and will be marked as DONE if implemented.

## v1.4.0

Dashboard Page (`/dashboard`)
- [x] Move reports and charts in Report Page to Dashboard Page, the main point of Dashboard Page is to show a quick overview of the current month's expenses.
- [x] Replace top three cards with a summary card showing total income, total expense, and balance for the current month.
- [x] Add a table to show top 5 expense transactions of the current month.
- [x] Update existing charts to fit the new layout.

Transaction Page (`/transactions`)
- [x] Add a new column named `type` in model to show the type of the transaction (e.g., income, expense).
- [x] Update transaction modal to allow users to select the type of the transaction.
- [x] Update transaction list to show the type of the transaction.
- [x] Remve the daily grouping in transaction list.

Report Page (`/reports`)
- [x] Remove Report Page, move all reports to Dashboard Page.

Wallet Page (`/wallet`) - I want to add a wallet page to show all my wallets and their balances.
- [] Add a card to show the total balance of the history.
- [] Add a bar chart to show the income and expense in the past 6 months.
- [] Add a table to show the latest 6 transactions.
- [] Add a pie chart to show the expense of each category in the past 6 months.

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
