# Excel Budget Tracker

An automated personal finance management system built entirely in Microsoft Excel using Power Query, VBA, and PivotTables.

What started as a simple spreadsheet for tracking income and expenses evolved into a system for importing bank statements, automatically categorizing transactions, handling manual corrections, and visualizing financial data.

## Features

- **Automated CSV Import** — Power Query imports bank statements from a designated folder.
- **Rule-Based Categorization** — Custom rules classify transactions based on payment details, transaction type, and amount.
- **Duplicate Prevention** — Transaction identifiers and filtering logic help prevent duplicate entries.
- **VBA Transaction Editor** — A custom interface for editing transaction categories, subcategories, amounts, and review statuses.
- **Persistent Manual Overrides** — Corrections are stored separately and reapplied during data refreshes.
- **Interactive Dashboard** — Financial summaries, PivotTables, slicers, and monthly spending visualizations.

## Screenshots

### Financial Dashboard

![Financial Dashboard](screenshots/dashboard.png)

### Transaction Management

![Transaction Management](screenshots/transactions.png)

### VBA Transaction Editor

![VBA Transaction Editor](screenshots/transaction-editor.png)

### Power Query Automation

![Power Query Editor](screenshots/power-query.png)

## Technologies

| Technology | Purpose |
|---|---|
| Microsoft Excel | Main application and user interface |
| Power Query (M) | Data import, transformation, and categorization |
| VBA | Transaction editing and automation |

## Getting Started

### Requirements

- Microsoft Excel Desktop for Windows
- VBA macro support

### Installation

1. Download or clone this repository.
2. Keep `BudgetTracker.xlsm` and the `fake_data` folder together in the same parent directory.
3. Open `BudgetTracker.xlsm` in Microsoft Excel.
4. Review the VBA code and enable macros if you trust the workbook.
5. Go to **Data → Refresh All**.
6. Explore the dashboard and transaction table.

The workbook is designed to locate the demonstration CSV folder relative to its own location.

### Adding Transactions

1. Place CSV bank statements in the `fake_data` folder.
2. Open the workbook.
3. Select **Data → Refresh All**.
4. Power Query imports and processes the transactions.
5. Review transactions that require manual classification.

CSV files must follow the expected structure.

## How It Works

1. Bank statements are imported from CSV files.
2. Power Query cleans and combines the data.
3. Custom rules assign categories and subcategories.
4. Transactions are consolidated into a unified dataset.
5. VBA allows users to make manual corrections.
6. Corrections are stored in a separate exceptions table and reapplied during refreshes.
7. The dashboard presents the processed data through interactive visualizations.

## Demonstration Data

The repository uses synthetic financial transactions for demonstration purposes. No real personal banking information is intended to be included.

## Project Background

Initially, I relied on AI to help analyze and categorize bank transactions. This required preparing the data, reviewing the results, and manually transferring information into Excel.

I wanted to eliminate these repetitive steps.

By combining Power Query, VBA, and Excel's analytical capabilities, I developed a workflow where importing new transactions requires little manual intervention.

The biggest technical challenge was making Power Query and VBA work together while preserving manual corrections across data refreshes.

## License

No license has been selected yet.