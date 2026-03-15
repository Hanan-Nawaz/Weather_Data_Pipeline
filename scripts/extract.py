import logging
import requests
from typing import List, Dict


def get_all_cities(
    cities: List[Dict],
    api: Dict,
    base_url: str,
    logger: logging.Logger
) -> List[Dict]:
    """
    Fetch weather data for a list of cities from the API.

    Parameters
    ----------
    cities : list of dict
        List of city configurations containing city names.
    api : dict
        API configuration containing the API key and unit settings.
    base_url : str
        Base URL of the weather API endpoint.
    logger : logging.Logger
        Logger instance used for logging.

    Returns
    -------
    list of dict
        List of weather data responses for each city.
    """

    raw_data = []

    for city in cities:
        params = {
            "q": city["name"],
            "appid": api["key"],
            "units": api["units"],
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()

            raw_data.append(response.json())

            logger.info(f"Data fetched for {city['name']}")

        except requests.exceptions.RequestException as e:
            logger.info(f"API request failed for {city['name']}")

    return raw_data


def api_call(config: Dict, logger: logging.Logger) -> List[Dict]:
    """
    Execute API calls to retrieve weather data.

    Parameters
    ----------
    config : dict
        Application configuration containing API and city settings.
    logger : logging.Logger
        Logger instance used to log extraction progress.

    Returns
    -------
    list of dict
        List of raw weather data responses.
    """

    api = config["api"]
    base_url = f"{api['base_url']}/weather"
    cities = config["cities"]

    raw_data = get_all_cities(cities, api, base_url, logger)

    if not raw_data:
        logger.info("Extraction failed: No data returned.")
    
    logger.info("Extraction succeeded.")

    return raw_data


def extract(config: Dict, logger: logging.Logger) -> List[Dict]:
    """
    Run the extraction stage of the ETL pipeline.

    Parameters
    ----------
    config : dict
        Application configuration.
    logger : logging.Logger
        Logger instance used for logging extraction progress.

    Returns
    -------
    list of dict
        Raw weather data retrieved from the API.
    """

    logger.info("Extraction started.")

    data = api_call(config, logger)

    logger.info("Extraction finished.")

    return data