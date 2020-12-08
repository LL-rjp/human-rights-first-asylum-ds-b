from dotenv import load_dotenv
from fastapi import APIRouter, Depends
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import os

router = APIRouter()


async def get_db() -> sqlalchemy.engine.base.Connection:
    """Get a SQLAlchemy database connection.

    Uses this environment variable if it exists:
    DATABASE_URL=dialect://user:password@host/dbname

    """
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@router.get('/req')
async def make_req(connection=Depends(get_db)):
    """Returns a json object with the entire pdfs table.
    """
    sql = """
        SELECT *
        FROM pdfs
        """

    var = pd.read_sql(sql, con=connection)

    print(var)

    return var
