import logging

from portfolio_tracker.cli import run

LOG_FILE = "portfolio_tracker.log"

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    # Logs go to a file so the user's screen only shows what they need to see.
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        encoding="utf-8",
    )

def main ():
    configure_logging()
    logger.info("Application started")
    try:
        run()
    except Exception:
        logger.exception("Unexpected error; the application is closing")
        print("Something unexpected went wrong and the app has to close. Details are in the log file.")
    logger.info("Application stopped") 
        

# if this module is executed from the command line then run the main function. 
# However, if this function is imported into another module do not run the main function 
if __name__=="__main__":
    main()