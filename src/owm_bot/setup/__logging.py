from __future__ import annotations

import logging
import logging.config
import typing as t

import red_logging

def setup_logging(name: str = "app", log_level: str = "INFO"):
    app_formatter = red_logging.get_formatter_config(
        # fmt=red_logging.fmts.MESSAGE_FMT_DETAILED
        fmt=red_logging.fmts.MESSAGE_FMT_STANDARD
    )
    app_console_handler = red_logging.get_streamhandler_config(level="DEBUG")
    app_logger = red_logging.get_logger_config(name=name, level=log_level)

    _formatters = [app_formatter]
    _handlers = [app_console_handler]
    _loggers = [app_logger]

    logging_config: dict = red_logging.assemble_configdict(
        disable_existing_loggers=False,
        formatters=_formatters,
        handlers=_handlers,
        loggers=_loggers,
    )

    logging.config.dictConfig(config=logging_config)

    ## Disable 3rd party library loggers
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("hishel").setLevel(logging.WARNING)
