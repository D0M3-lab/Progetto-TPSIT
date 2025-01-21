# Store Budget Management
A simple GUI application built in Python with **Tkinter** to manage a store's budget. It allows you to add, edit, and view transactions, automatically calculating the total balance.

## Features
- **Add Transactions**: Enables you to record transactions as income or expenses.
- **Edit Transactions**: Each recorded transaction can be edited directly from the interface.
- **View Transactions**: Displays a complete summary of recorded transactions.
- **Balance Calculation**: Automatically updates the total balance based on transactions.

## Requirements
- Python 3.x
- Standard libraries: `tkinter`, `json`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/store-budget-management.git
   ```

2. Navigate to the project directory:
   ```bash
   cd store-budget-management
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. **Add a transaction**:
   - Click the "Add Transaction" button.
   - Enter the type (income/expense), description, and amount.

2. **Edit a transaction**:
   - Press the "Edit" button next to a transaction.
   - Update the details as needed.

3. **View balance**:
   - The total balance is displayed at the top of the interface and updates automatically.

4. **Transaction list**:
   - Scroll through the list to view all recorded transactions.

## Project Structure
- `main.py`: Main file containing the application code.
- `bilancio.json`: Automatically generated file to save transaction data in JSON format.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
