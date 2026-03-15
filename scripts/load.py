import psycopg2
import pandas as pd
import logging

def open_conn(config: dict, logger: logging.Logger) -> psycopg2.extensions.connection:
    """
    Open a connection to the PostgreSQL database.

    Parameters
    ----------
    config : dict
        Application configuration containing database connection settings.
    logger : logging.Logger
        Logger instance used to record errors.

    Returns
    -------
    psycopg2.extensions.connection
        Active PostgreSQL database connection.
    """

    try:
        conn = psycopg2.connect(
            host = config['database']['host'],
            port = config['database']['port'],
            user =config['database']['username'],
            password = config['database']['password'],
            dbname = config['database']['name']
        )

        return conn

    except Exception as e:
        logger.info(e)

def create_cursor(
    conn: psycopg2.extensions.connection,
    logger: logging.Logger
) -> psycopg2.extensions.cursor:
    """
    Create a database cursor from an existing connection.

    Parameters
    ----------
    conn : psycopg2.extensions.connection
        Active PostgreSQL database connection.
    logger : logging.Logger
        Logger instance used for logging errors.

    Returns
    -------
    psycopg2.extensions.cursor
        Cursor object used to execute SQL queries.
    """
    
    try:
        cur = conn.cursor()
        return cur
    except Exception as e:
        logger.info(e)

def create_table(
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    logger: logging.Logger
) -> None:
    """
    Create the weather table in the database if it does not exist.

    Parameters
    ----------
    conn : psycopg2.extensions.connection
        Active PostgreSQL database connection.
    cur : psycopg2.extensions.cursor
        Cursor used to execute SQL statements.
    logger : logging.Logger
        Logger instance used to record errors.

    Returns
    -------
    None
    """
    
    query = """
            CREATE TABLE IF NOT EXISTS weather
                ( 
                    id SERIAL PRIMARY KEY  NOT NULL,
                    date TIMESTAMP NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    description VARCHAR(50) NOT NULL,
                    temp FLOAT NOT NULL,
                    feels_like FLOAT NOT NULL,
                    temp_min FLOAT NOT NULL,
                    temp_max FLOAT NOT NULL,
                    humidity INT NOT NULL,
                    sunrise TIMESTAMP NOT NULL,
                    sunset TIMESTAMP NOT NULL,
                    wind_speed FLOAT NOT NULL
                )
            """
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.info(e)

def load_data(
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    logger: logging.Logger
) -> None:
    """
    Insert weather data into the database.

    Parameters
    ----------
    conn : psycopg2.extensions.connection
        Active PostgreSQL database connection.
    cur : psycopg2.extensions.cursor
        Cursor used to execute SQL queries.
    df : pandas.DataFrame
        DataFrame containing weather data to be inserted.
    logger : logging.Logger
        Logger instance used for logging errors.

    Returns
    -------
    None
    """
    
    query = """
                INSERT INTO weather (date, name, description,
                                    temp, feels_like, temp_min, temp_max, 
                                    humidity, sunrise, sunset, wind_speed
                                    )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        data = list(df.itertuples(index=False, name=None))
        cur.executemany(query, data)
        conn.commit()
    except Exception as e:
        logger.info(e)


def load(config: dict, df: pd.DataFrame, logger: logging.Logger) -> None:
    """
    Execute the loading stage of the ETL pipeline.

    This function establishes a database connection, ensures the
    weather table exists, and inserts the transformed weather data.

    Parameters
    ----------
    config : dict
        Application configuration containing database settings.
    df : pandas.DataFrame
        DataFrame containing transformed weather data.
    logger : logging.Logger
        Logger instance used to log loading progress.

    Returns
    -------
    None
    """
    
    logger.info('----Loading Successded!-----')
    conn = open_conn(config, logger)
    cur = create_cursor(conn, logger)
    try:
        create_table(conn, cur, logger)
        load_data(conn, cur, df, logger)
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('----Loading Succeeded!-----')
        cur.close()
        conn.close()