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
    cursor.execute("DELETE FROM helloworld WHERE id = 1")
    cursor.execute("INSERT INTO helloworld(id, set) VALUES (1, hll_empty());")

    start_time = time.perf_counter()
    for _ in range(1, 1000):
        id = bson.ObjectId().__str__()
        cursor.execute("""
                      UPDATE helloworld 
                      SET set = hll_add(set, hll_hash_text(%s))
                      WHERE id=1
                      """, (id,))
        conn.commit()
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Function Took {total_time:.4f} seconds')

    # print result
    cursor.execute("SELECT hll_cardinality(set) FROM helloworld WHERE id = 1")
    result = cursor.fetchone()
    # Close the cursor and connection
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error: {e}")
