"""
Centralized Logger Configuration
--------------------------------

Features
--------
✔ Console Logging (Development)
✔ File Logging
✔ Rotating Log Files
✔ Production Ready
✔ Single Logger Across Application
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# =====================================================
# Environment
# =====================================================

ENV = os.getenv("ENV", "development").lower()

# =====================================================
# Log Directory
# =====================================================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "intelliflow.log")

# =====================================================
# Logger
# =====================================================

logger = logging.getLogger("IntelliFlowAI")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# Remove duplicate handlers (useful during reload)
if logger.hasHandlers():
    logger.handlers.clear()

# =====================================================
# Formatter
# =====================================================

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# =====================================================
# File Handler (Always Enabled)
# =====================================================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)