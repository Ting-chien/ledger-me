# API Document

API document records all API endpoint and interface in this project.

## Transactions Module

Base URL: `/transactions`

### List Transactions (Index)

* **Description**: Retrieve a paginated list of transactions with optional filtering by search text, category, and date. Renders the transactions index page.
* **Endpoint**: `GET /transactions/`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `search` | Query | String | No | Filter by transaction item name (partial match). |
| `category` | Query | Integer | No | Filter by category ID. |
| `date` | Query | String | No | Filter by precise date (YYYY-MM-DD). |
| `page` | Query | Integer | No | Page number (default: 1). |
| `page_size` | Query | Integer | No | Items per page (default: 10). |

* **Output**: HTML Page (`transactions/index.html`)

### Create Transaction

* **Description**: Create a new transaction record. Redirects to the index upon success.
* **Endpoint**: `POST /transactions/`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `item` | Form Data | String | Yes | Name/Description of the expense. |
| `category` | Form Data | Integer | No | ID of the transaction category. |
| `expense` | Form Data | Integer | Yes | Amount of the expense. |
| `date` | Form Data | String | Yes | Date of transaction (YYYY-MM-DD). |
| `remark` | Form Data | String | No | Additional notes. |

* **Output**: Redirects to `/transactions/` (HTTP 302).

### Update Transaction

* **Description**: Update details of an existing transaction.
* **Endpoint**: `PUT /transactions/<transaction_id>`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | Path | Integer | Yes | Unique ID of the transaction. |
| `item` | Form Data | String | Yes | Name/Description of the expense. |
| `category` | Form Data | Integer | No | ID of the transaction category. |
| `expense` | Form Data | Integer | Yes | Amount of the expense. |
| `date` | Form Data | String | Yes | Date of transaction (YYYY-MM-DD). |
| `remark` | Form Data | String | No | Additional notes. |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `success` | Boolean | Operation status. |
| `transaction` | Object | The updated transaction details. |

* **Example**:
```json
{
  "success": true,
  "transaction": {
    "id": 12,
    "item": "Lunch",
    "category_id": 3,
    "expense": 150,
    "date": "2024-03-15",
    "remark": "Team lunch"
  }
}
```

### Delete Transaction

* **Description**: Delete a specific transaction.
* **Endpoint**: `DELETE /transactions/<transaction_id>`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | Path | Integer | Yes | Unique ID of the transaction. |

* **Output**: Empty body (HTTP 204).

---

## Reports Module

Base URL: `/reports`

### Reports Dashboard

* **Description**: Renders the main reports overview page.
* **Endpoint**: `GET /reports/`
* **Parameter**: None
* **Output**: HTML Page (`reports/index.html`)

### Total Expenses

* **Description**: Get the total sum of expenses for a specific month.
* **Endpoint**: `GET /reports/total-expenses`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Query | Integer | No | Year (default: current year). |
| `month` | Query | Integer | No | Month (default: current month). |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `total_expenses` | Integer | Total expense amount. |

* **Example**:
```json
{
  "total_expenses": 5400
}
```

### Month Projection

* **Description**: Calculate projected expenses for the current month based on daily average spending.
* **Endpoint**: `GET /reports/month-projection`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Query | Integer | No | Year. |
| `month` | Query | Integer | No | Month. |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `projection` | Integer | Estimated total expense for the month. |
| `is_current_month` | Boolean | True if querying the ongoing month. |
| `days_remaining` | Integer | Number of days left in the month. |

* **Example**:
```json
{
  "projection": 8500,
  "is_current_month": true,
  "days_remaining": 10
}
```

### Month-over-Month (MoM) Comparison

* **Description**: Compare current month's expenses with the previous month.
* **Endpoint**: `GET /reports/mom-comparison`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Query | Integer | No | Year. |
| `month` | Query | Integer | No | Month. |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `current_total` | Integer | Total expenses for selected month. |
| `prev_total` | Integer | Total expenses for previous month. |
| `diff_amount` | Integer | Difference (Current - Previous). |
| `diff_percent` | Float | Percentage change. |

* **Example**:
```json
{
  "current_total": 5400,
  "prev_total": 5000,
  "diff_amount": 400,
  "diff_percent": 8.0
}
```

### Expenses Breakdown

* **Description**: Get expenses aggregated by category.
* **Endpoint**: `GET /reports/expenses-breakdown`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Query | Integer | No | Year. |
| `month` | Query | Integer | No | Month. |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `labels` | Array[String] | List of category names. |
| `data` | Array[Integer] | Corresponding expense totals. |

* **Example**:
```json
{
  "labels": ["Food", "Transport", "Entertainment"],
  "data": [3000, 1500, 900]
}
```

### Expenses Trend

* **Description**: Get daily expense totals for the month to show spending trends.
* **Endpoint**: `GET /reports/expenses-trend`
* **Parameter**:

| Parameter | Location | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Query | Integer | No | Year. |
| `month` | Query | Integer | No | Month. |

* **Output**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `labels` | Array[String] | List of dates (MM/DD). |
| `data` | Array[Integer] | Daily expense totals. |

* **Example**:
```json
{
  "labels": ["01/01", "01/02", "01/03"],
  "data": [200, 0, 450]
}
```

