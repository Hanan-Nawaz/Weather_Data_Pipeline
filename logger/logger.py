import logging

def create_logger(
        format: str,
        file_path: str,
        level: int,
        propgate: bool,
        disabled: bool = False
    ) -> logging.Logger:
    """
    Create and configure a logger instance.

    Parameters
    ----------
    format : str
        Logging message format string used by the formatter.
    file_path : str
        Path to the log file where log messages will be written.
    level : int
        Logging level (e.g., logging.INFO, logging.DEBUG).
    propgate : bool
        Whether log messages should propagate to parent loggers.
    disabled : bool, optional
        Whether the logger should be disabled, by default False.

    Returns
    -------
    logging.Logger
        Configured logger instance with a file handler attached.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.propagate = propgate
    logger.disabled = disabled

    if not logger.handlers:
        formatter = logging.Formatter(format)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger