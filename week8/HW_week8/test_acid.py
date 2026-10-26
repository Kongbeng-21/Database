"""
ACID Properties Stress Test
Tests concurrent transactions to demonstrate ACID properties.
"""

import pymysql
import threading
import time
import random
from typing import List

# Database Configuration (match compose.yaml)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'student',
    'password': 'change-this-user-password',
    'database': 'student_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Test Configuration
NUM_ACCOUNTS = 10
NUM_THREADS = 20
TRANSACTIONS_PER_THREAD = 50
INITIAL_BALANCE = 1000.00


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def setup_test_accounts():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            print("Setting up test accounts...")
            cursor.execute("DELETE FROM Transactions")
            cursor.execute("DELETE FROM Accounts")
            cursor.execute("DELETE FROM Customers WHERE name LIKE 'Test%'")
            cursor.execute("UPDATE BankReserves SET total_reserve = 0.00")

            # Reset IDs so test accounts are always 1..10 (random.randint(1, 10) below)
            cursor.execute("ALTER TABLE Accounts AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE Transactions AUTO_INCREMENT = 1")

            for i in range(NUM_ACCOUNTS):
                cursor.execute(
                    "INSERT INTO Customers (name, tax_id) VALUES (%s, %s)",
                    (f"TestUser{i}", f"TEST{i:04d}"))
                customer_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO Accounts (customer_id, balance) VALUES (%s, %s)",
                    (customer_id, INITIAL_BALANCE))

            total_initial = NUM_ACCOUNTS * INITIAL_BALANCE
            cursor.execute(
                "UPDATE BankReserves SET total_reserve = %s WHERE branch_id = 1",
                (total_initial,))
            conn.commit()
            print(f"Created {NUM_ACCOUNTS} test accounts with ${INITIAL_BALANCE} each")
            print(f"Total bank reserves: ${total_initial}")
    finally:
        conn.close()


def concurrent_transfer_worker(worker_id: int, results: List):
    conn = get_connection()
    success_count = 0
    failure_count = 0
    try:
        for i in range(TRANSACTIONS_PER_THREAD):
            from_account = random.randint(1, NUM_ACCOUNTS)
            to_account = random.randint(1, NUM_ACCOUNTS)
            if from_account == to_account:
                continue
            amount = round(random.uniform(1.0, 50.0), 2)

            try:
                with conn.cursor() as cursor:
                    cursor.execute("START TRANSACTION")

                    # Lock both rows in ascending ID order (prevents deadlock)
                    cursor.execute(
                        "SELECT account_id, balance FROM Accounts "
                        "WHERE account_id IN (%s, %s) ORDER BY account_id FOR UPDATE",
                        (from_account, to_account))
                    rows = {r['account_id']: float(r['balance']) for r in cursor.fetchall()}

                    if from_account not in rows or to_account not in rows:
                        raise Exception("Account not found")
                    if rows[from_account] < amount:
                        raise Exception("Insufficient funds")

                    cursor.execute(
                        "UPDATE Accounts SET balance = balance - %s WHERE account_id = %s",
                        (amount, from_account))
                    cursor.execute(
                        "UPDATE Accounts SET balance = balance + %s WHERE account_id = %s",
                        (amount, to_account))
                    cursor.execute(
                        "INSERT INTO Transactions (account_id, transaction_type, amount) "
                        "VALUES (%s, 'TRANSFER_OUT', %s)", (from_account, amount))
                    cursor.execute(
                        "INSERT INTO Transactions (account_id, transaction_type, amount) "
                        "VALUES (%s, 'TRANSFER_IN', %s)", (to_account, amount))
                conn.commit()
                success_count += 1
            except Exception:
                conn.rollback()
                failure_count += 1

        results.append({'worker_id': worker_id, 'success': success_count, 'failure': failure_count})
    finally:
        conn.close()


def concurrent_deposit_withdraw_worker(worker_id: int, results: List):
    conn = get_connection()
    success_count = 0
    failure_count = 0
    try:
        for i in range(TRANSACTIONS_PER_THREAD):
            account_id = random.randint(1, NUM_ACCOUNTS)
            amount = round(random.uniform(10.0, 100.0), 2)
            operation = random.choice(['deposit', 'withdraw'])

            try:
                with conn.cursor() as cursor:
                    cursor.execute("START TRANSACTION")

                    # Lock the account row first
                    cursor.execute(
                        "SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE",
                        (account_id,))
                    row = cursor.fetchone()
                    if row is None:
                        raise Exception("Account not found")

                    if operation == 'deposit':
                        cursor.execute(
                            "UPDATE Accounts SET balance = balance + %s WHERE account_id = %s",
                            (amount, account_id))
                        cursor.execute(
                            "UPDATE BankReserves SET total_reserve = total_reserve + %s WHERE branch_id = 1",
                            (amount,))
                        cursor.execute(
                            "INSERT INTO Transactions (account_id, transaction_type, amount) "
                            "VALUES (%s, 'DEPOSIT', %s)", (account_id, amount))
                    else:
                        if float(row['balance']) < amount:
                            raise Exception("Insufficient funds")
                        cursor.execute(
                            "UPDATE Accounts SET balance = balance - %s WHERE account_id = %s",
                            (amount, account_id))
                        cursor.execute(
                            "UPDATE BankReserves SET total_reserve = total_reserve - %s WHERE branch_id = 1",
                            (amount,))
                        cursor.execute(
                            "INSERT INTO Transactions (account_id, transaction_type, amount) "
                            "VALUES (%s, 'WITHDRAW', %s)", (account_id, amount))
                conn.commit()
                success_count += 1
            except Exception:
                conn.rollback()
                failure_count += 1

        results.append({'worker_id': worker_id, 'success': success_count, 'failure': failure_count})
    finally:
        conn.close()


def verify_consistency():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT SUM(balance) AS total_accounts FROM Accounts WHERE customer_id IN "
                "(SELECT customer_id FROM Customers WHERE name LIKE 'Test%')")
            total_accounts = float(cursor.fetchone()['total_accounts'] or 0)

            cursor.execute("SELECT total_reserve FROM BankReserves WHERE branch_id = 1")
            total_reserves = float(cursor.fetchone()['total_reserve'] or 0)

            expected_total = NUM_ACCOUNTS * INITIAL_BALANCE

            print("\n" + "=" * 60)
            print("CONSISTENCY CHECK")
            print("=" * 60)
            print(f"Initial total:           ${expected_total:,.2f}")
            print(f"Sum of account balances: ${total_accounts:,.2f}")
            print(f"Bank reserves:           ${total_reserves:,.2f}")
            print(f"Difference (accounts vs reserves): ${abs(total_accounts - total_reserves):,.2f}")

            # Deposits/withdrawals change the total, so the invariant is:
            # sum of all balances == bank reserves
            if abs(total_accounts - total_reserves) < 0.01:
                print("\n✅ CONSISTENCY: PASS - Money is conserved!")
                print("   This proves Atomicity and Consistency properties.")
            else:
                print("\n❌ CONSISTENCY: FAIL - Money was created or lost!")

            cursor.execute("SELECT COUNT(*) AS count FROM Transactions")
            print(f"\nTotal transactions logged: {cursor.fetchone()['count']}")
            print("=" * 60)
    finally:
        conn.close()


def run_stress_test(test_type: str):
    print(f"\n{'=' * 60}")
    print(f"Running {test_type.upper()} stress test")
    print(f"Threads: {NUM_THREADS}, Transactions per thread: {TRANSACTIONS_PER_THREAD}")
    print(f"{'=' * 60}\n")

    threads = []
    results = []
    worker_func = concurrent_transfer_worker if test_type == 'transfer' else concurrent_deposit_withdraw_worker

    start_time = time.time()
    for i in range(NUM_THREADS):
        t = threading.Thread(target=worker_func, args=(i, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    elapsed_time = time.time() - start_time

    total_success = sum(r['success'] for r in results)
    total_failure = sum(r['failure'] for r in results)
    print(f"\nCompleted in {elapsed_time:.2f} seconds")
    print(f"Successful transactions: {total_success}")
    print(f"Failed transactions (rolled back, e.g. insufficient funds): {total_failure}")
    print(f"Success rate: {(total_success / (total_success + total_failure) * 100):.1f}%")


if __name__ == "__main__":
    print("ACID Properties Stress Test")
    print("=" * 60)
    setup_test_accounts()

    print("\nChoose test type:")
    print("1. Transfer test (concurrent transfers between accounts)")
    print("2. Deposit/Withdraw test (concurrent deposits and withdrawals)")
    print("3. Both")
    choice = input("\nEnter choice (1-3): ").strip()

    if choice in ['1', '3']:
        run_stress_test('transfer')
        verify_consistency()

    if choice in ['2', '3']:
        if choice == '3':
            setup_test_accounts()
        run_stress_test('deposit_withdraw')
        verify_consistency()

    print("\n" + "=" * 60)
    print("LEARNING POINTS:")
    print("=" * 60)
    print("1. ATOMICITY: All operations in a transaction succeed or fail together")
    print("2. CONSISTENCY: Sum of balances always equals bank reserves")
    print("3. ISOLATION: Use FOR UPDATE to prevent race conditions")
    print("4. DURABILITY: Committed transactions persist in database")
    print("=" * 60)