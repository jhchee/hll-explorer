import psycopg2
import bson
from psycopg2.extras import execute_values

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432',
}
try:
    # Establish the connection to the database
    conn = psycopg2.connect(**db_params)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    update_template = """
                      UPDATE helloworld 
                      SET set = hll_add(set, hll_hash_text(t.name))
                      WHERE id=1
                      """

    tuples = [(bson.ObjectId().__str__(),) for i in range(1, 10)]
    print(tuples)
    ex(cursor, update_template, tuples)
    conn.commit()

    cursor.execute("SELECT hll_cardinality(set) FROM helloworld WHERE id = 1")

    result = cursor.fetchone()
    print(result)
    # Close the cursor and connection
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error: {e}")
