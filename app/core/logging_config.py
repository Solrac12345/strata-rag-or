# EN: Basic logging configuration (extend in later steps)
# FR: Configuration de logging basique (à étendre plus tard)
import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )