import pandas as pd
import psycopg2


DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "defaultdb"
DB_USER = "postgres"
DB_PASSWORD = "root"


conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)


# start_date = '2023-01-02'
# end_date = '2023-01-05'

start_date = input("Enter the START date in the format 'YEAR-MONTH-DATE' :")
end_date = input("Enter the END date in the format 'YEAR-MONTH-DATE' :")

query = f"""
SELECT strike, instrument_type,
    MAX(CASE WHEN date = '{start_date}' THEN OI ELSE 0 END) AS oi1,
    MAX(CASE WHEN date = '{end_date}' THEN OI ELSE 0 END) AS oi2
FROM test_assignment
WHERE date IN ('{start_date}', '{end_date}')
GROUP BY strike, instrument_type;
"""

df = pd.read_sql(query, conn)

conn.close()

df['oi_diff'] = df['oi2'] - df['oi1']

df_pivot = df.pivot(index='strike', columns='instrument_type', values='oi_diff')

print(df_pivot)
