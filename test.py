from sqlalchemy import create_engine
from sqlalchemy.sql import text

db_uri = "dremio+flight://admin:admin123@localhost:32010/dremio?UseEncryption=false"
engine = create_engine(db_uri)
sql = 'SELECT * FROM sys.options limit 5 -- SQL Alchemy Flight Test '

with engine.connect() as con:
    result = con.execute(text(sql))
    for row in result:
        print(row[0])
