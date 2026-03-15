import yaml
from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load
from logger.logger import create_logger
import logging

def get_yaml(file_path: str) -> dict:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    file_path : str
        Path to the YAML file to be loaded.

    Returns
    -------
    dict
        Parsed YAML content as a dictionary.
    """
    
    with open(file_path) as file:
        config = yaml.safe_load(file)

    return config


def logger_config(config: dict) -> logging.Logger:
    """
    Configure and create a logger using a configuration dictionary.

    Parameters
    ----------
    config : dict
        Dictionary containing logger configuration values. Expected keys are:
        'logger_format', 'logger_level', 'disable', 'propagate', and 'file_path'.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    logger_format = config['logger_format']
    logger_level = config['logger_level']
    disable = config['disable']
    propagate = config['propagate']
    file_path = config['file_path']
    logger = create_logger(
        logger_format,
        file_path,
        logger_level,
        propagate,
        disable
    )

    return logger

def main() -> None:
    """
    Run the ETL pipeline.

    This function orchestrates the main workflow of the application:
    loading configuration, setting up logging, extracting raw data,
    transforming the data, and loading the processed data to the
    target destination.

    Returns
    -------
    None
        This function does not return a value.
    """

    yaml_file_path = 'config/config.yaml'
    config = get_yaml(yaml_file_path)
    logger = logger_config(config['logs'])
    raw_data = extract(config, logger)
    df = transform(raw_data, config, logger)
    load(config, df, logger) 

if __name__ == "__main__":
    main()
