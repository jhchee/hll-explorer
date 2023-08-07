import time
import psycopg2
import bson

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432',
}
try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    # prepare the table
    cursor.execute("DROP TABLE IF EXISTS public.visitor")
    cursor.execute("""CREATE TABLE visitor (event_date TEXT, set hll)""")
    cursor.execute("DELETE FROM visitor WHERE event_date = '2023-07-01'")
    cursor.execute("INSERT INTO visitor(event_date, set) VALUES ('2023-07-01', hll_empty())")

    start_time = time.perf_counter()
    for _ in range(1, 1000):
        id = bson.ObjectId().__str__()
        cursor.execute("""
                      UPDATE visitor 
                      SET set = hll_add(set, hll_hash_text(%s))
                      WHERE event_date = '2023-07-01'
                      """, (id,))
        conn.commit()
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Function Took {total_time:.4f} seconds')

    # print result
    cursor.execute("SELECT hll_cardinality(set) FROM visitor WHERE event_date = '2023-07-01'")
    result = cursor.fetchone()
    print(result)
    # Close the cursor and connection
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error: {e}")
