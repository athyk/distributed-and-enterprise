import psycopg2

tags_db_config = {
    "dbname": "tags_db",
    "user": "unihub",
    "password": "hVvBgjrKY5wx9dv56Zadbi4AKbFK",
    "host": "127.0.0.1",
    "port": "5432"
}

degree_db_config = {
    "dbname": "degree_db",
    "user": "unihub",
    "password": "hVvBgjrKY5wx9dv56Zadbi4AKbFK",
    "host": "127.0.0.1",
    "port": "5432"
}

account_db_config = {
    "dbname": "account_db",
    "user": "unihub",
    "password": "hVvBgjrKY5wx9dv56Zadbi4AKbFK",
    "host": "127.0.0.1",
    "port": "5432"
}

community_db_config = {
    "dbname": "community_db",
    "user": "unihub",
    "password": "hVvBgjrKY5wx9dv56Zadbi4AKbFK",
    "host": "127.0.0.1",
    "port": "5432"
}


def insert_data(config, file_name):
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        with open(file_name, 'r') as file:
            sql = file.read()

        cursor.execute(sql)

        conn.commit()
        print("Data Successfully Inserted")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    insert_data(tags_db_config, 'backend/tests/test_data/Tag.sql')
    insert_data(degree_db_config, 'backend/tests/test_data/Degree.sql')
    insert_data(account_db_config, 'backend/tests/test_data/Account.sql')
    insert_data(account_db_config, 'backend/tests/test_data/AccountPost.sql')
    insert_data(community_db_config, 'backend/tests/test_data/Community.sql')

    print('\nAll Data Insertion Functions Completed')
