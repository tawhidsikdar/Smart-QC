"""Logging setup for SMARTQC. Call setup_logging() once,once the programme starts"""

import logging
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LOG_DIR = REPO_ROOT / "logs"

#print(f'The desired folder is {REPO_ROOT}')

def setup_logging(name = "smartqc" , console_level = logging.INFO):

    LOG_DIR.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"{name}_{stamp}.log"

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    #the log file(keeps everything)-route 1
    file_handler = logging.FileHandler(log_path,encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s %(name)-12s %(message)s")
    )
    root.addHandler(file_handler)

    # the screen only- route 2(only the important stuffs)
    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(logging.Formatter("%(levelname)-8s %(name)-12s %(message)s"))

    root.addHandler(console)

    logging.getLogger(__name__).info("Logging started,writing to %s",log_path)
    return log_path

if __name__ == "__main__":
    setup_logging("logtest")
    log = logging.getLogger("demo")

    log.debug("A detail: sent <12,HB*2F>")
    log.info("Move Done , position %d steps",6945)
    log.warning("Camera read retried,attempt %d of 3",2)
    log.error("No ACK after %d tries",3)

    start = time.monotonic()
    time.sleep(0.15)
    log.info("Settle wait took %.3f s", time.monotonic() - start)
