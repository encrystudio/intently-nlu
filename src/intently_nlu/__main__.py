"""Main entry point for the IntentlyNLU CLI

Raises:
    Exception: Caught if any uncaught error occurs
"""

if __name__ == "__main__":
    from intently_nlu.cli import main

    try:
        main()
    except Exception as e:
        # catch and log any exception
        from intently_nlu.util.intently_logging import get_logger, log_error

        raise log_error(get_logger("CLI-MAIN"), e, "main CLI") from e

