from datetime import datetime

LEVELS = {
    "INFO": "[i]",
    "DEBUG": "[d]",
    "WARNING": "[w]",
    "ERROR": "[e]",
    "SUCCESS": "[s]"
}

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    icon = LEVELS.get(level.upper(), "")
    print(f"[{timestamp}] [{level.upper()}] {icon} {message}")
