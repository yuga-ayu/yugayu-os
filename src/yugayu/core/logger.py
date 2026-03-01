# TODO: [SECURITY] Merkle Chain Ledger: Upgrade RotatingFileHandler to hash (SHA-256) each log entry against the previous entry's fingerprint.
# TODO: [TRACKING] Append compute usage metadata (tokens, VRAM lease time) to the daily execution ledger.

import logging
import getpass
import os
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from yugayu.core.state.ledger_manager import load_config

LOG_ROOT = Path.home() / ".yugayu" / "logs"
LOG_FORMAT = "[%(asctime)s] [USER: %(user)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_daily_log_file() -> Path:
    """Dynamically generates the log path: ~/.yugayu/logs/YYYY/MM/YYYY-MM-DD.log"""
    now = datetime.now()
    log_dir = LOG_ROOT / str(now.year) / f"{now.month:02d}"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{now.strftime('%Y-%m-%d')}.log"

def setup_logger():
    """Configures the infinite, chunked daily logger."""
    logger = logging.getLogger("yugayu_history")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # 20MB chunks, practically infinite backups (9999)
    file_handler = RotatingFileHandler(
        get_daily_log_file(),
        maxBytes=20 * 1024 * 1024,
        backupCount=9999            
    )
    
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

def check_log_size_warning() -> bool:
    """Returns True if the total size of all logs exceeds the config limit."""
    if not LOG_ROOT.exists():
        return False
        
    total_bytes = sum(f.stat().st_size for f in LOG_ROOT.rglob('*') if f.is_file())
    config = load_config()
    limit_bytes = config.max_log_size_mb * 1024 * 1024
    
    return total_bytes > limit_bytes

def log_command(command: str, status: str = "SUCCESS", origin: str = None):
    logger = setup_logger()
    user = origin or os.environ.get("YUGAYU_ACTOR") or getpass.getuser()
    message = f"[STATUS: {status}] [CMD: {command}]"
    logger.info(message, extra={"user": user})

def log_error(command: str, error_msg: str, origin: str = None):
    logger = setup_logger()
    user = origin or os.environ.get("YUGAYU_ACTOR") or getpass.getuser()
    message = f"[STATUS: FAILED] [CMD: {command}] [ERROR: {error_msg}]"
    logger.error(message, extra={"user": user})
