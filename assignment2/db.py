import mariadb
import sys

# 1. Database Connection URI (Available since MariaDB Connector/Python 2.0)
DATABASE_URL = "mariadb://mysql:@localhost:3306/mysql"


def run_db_operations():
    conn = None
    cursor = None
    try:
        # 2. Establish a Connection
        print("Connecting to MariaDB...")
        conn = mariadb.connect(DATABASE_URL)
        print("Connection successful!")

        # 3. Create a Cursor Object
        cursor = conn.cursor()

        # --- Example: Create a Table (if it doesn't exist) ---
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE
                )
            """)
            conn.commit()  # Commit the transaction for DDL
            print("Table 'users' created or already exists.")
        except mariadb.Error as e:
            print(f"Error creating table: {e}")
            conn.rollback()  # Rollback in case of DDL error

        # --- Example: Insert Data (Parameterized Query) ---
        print("\nInserting data...")
        insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
        try:
            cursor.execute(
                insert_query, ("Alice Wonderland", "alice@example.com"))
            cursor.execute(insert_query, ("Bob Builder", "bob@example.com"))
            conn.commit()  # Commit the transaction for DML
            print(f"Inserted {cursor.rowcount} rows.")
            print(f"Last inserted ID: {cursor.lastrowid}")
        except mariadb.IntegrityError as e:
            print(f"Error inserting data (might be duplicate email): {e}")
            conn.rollback()
        except mariadb.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()

        # --- Example: Select Data ---
        print("\nSelecting data...")
        select_query = "SELECT id, name, email FROM users WHERE name LIKE ?"
        # Note the comma for single parameter tuple
        cursor.execute(select_query, ("%Alice%",))

        print("Fetched data:")
        for row in cursor:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

        # --- Example: Update Data ---
        print("\nUpdating data...")
        update_query = "UPDATE users SET name = ? WHERE email = ?"
        cursor.execute(
            update_query, ("Alicia Wonderland", "alice@example.com"))
        conn.commit()
        print(f"Rows updated: {cursor.rowcount}")

        # --- Example: Delete Data ---
        print("\nDeleting data...")
        delete_query = "DELETE FROM users WHERE name = ?"
        cursor.execute(delete_query, ("Bob Builder",))
        conn.commit()
        print(f"Rows deleted: {cursor.rowcount}")

    except mariadb.Error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # 4. Close Cursor and Connection
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if conn:
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    run_db_operations()
