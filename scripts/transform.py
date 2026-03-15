import pandas as pd
import logging

def create_df(raw_data: list) -> pd.DataFrame:
    """
    Create a pandas DataFrame from raw API data.

    Parameters
    ----------
    raw_data : list
        List of JSON responses containing weather data.

    Returns
    -------
    pandas.DataFrame
        DataFrame constructed from the raw weather data.
    """

    df = pd.DataFrame(raw_data, index=None)
    return df

def droping_columns(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Drop unnecessary columns from the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing weather data.
    config : dict
        Configuration dictionary containing transformation settings,
        including columns to drop.

    Returns
    -------
    pandas.DataFrame
        DataFrame with specified columns removed.
    """

    for col in config['transform']['columns_to_drop']:
        if col not in df.columns.to_list():
            print('column not exists')
        df.drop(columns=[col], inplace=True)

    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize nested JSON columns into flat columns.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing nested weather data.

    Returns
    -------
    pandas.DataFrame
        DataFrame with normalized and flattened columns.
    """

    df['description'] = df['weather'].apply(lambda x: x[0]['main'])
    df_main = pd.json_normalize(df['main'])
    df = pd.concat([df, df_main], axis=1)
    df['sunrise'] = df['sys'].apply(lambda x: (x)['sunrise'])
    df['sunset'] = df['sys'].apply(lambda x: (x)['sunset'])
    df['wind_speed'] = df['wind'].apply(lambda x: (x)['speed'])

    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename DataFrame columns.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame whose columns need to be renamed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with renamed columns.
    """

    df.rename(columns={'dt': 'date'}, inplace=True)

    return df

def change_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column data types.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing weather data.

    Returns
    -------
    pandas.DataFrame
        DataFrame with converted column types.
    """

    df['date'] = pd.to_datetime(df['date'], unit='s').dt.date
    df['sunrise'] = pd.to_datetime(df['sunrise'], unit='s').dt.date
    df['sunset'] = pd.to_datetime(df['sunset'], unit='s').dt.date

    return df

def cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning operations.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing weather data.

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame with duplicates and missing values removed.
    """

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    return df

def transform(raw_data: list, config: dict, logger: logging.Logger) -> pd.DataFrame:
    """
    Execute the transformation stage of the ETL pipeline.

    This function converts raw API data into a cleaned and structured
    DataFrame suitable for loading into a database.

    Parameters
    ----------
    raw_data : list
        List of raw weather data responses.
    config : dict
        Application configuration containing transformation settings.
    logger : logging.Logger
        Logger instance used to log transformation progress.

    Returns
    -------
    pandas.DataFrame
        Transformed and cleaned weather dataset.
    """

    logger.info('----Transormation Started!-----')
    try:
        df = create_df(raw_data)
        df = normalize_columns(df)
        df = droping_columns(df, config)
        df = rename_columns(df)
        df = change_types(df)
        df = cleaning(df)
    except Exception as e:
        logger.info(e)

    logger.info('----Extraction Successded!-----')

    return df