import logging

numeric_level = logging.INFO

# Chose the streamhandler as Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(numeric_level)
# Create a formatter and attach it to the handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
console_handler.setFormatter(formatter)

# Get the root logger and set its level to the specified level
logger = logging.getLogger()
logger.setLevel(numeric_level)
# Add the console handler to the logger
logger.addHandler(console_handler)
# Set the TDP-lib logger at level WARNING
# logging.getLogger("tdp").setLevel(logging.WARNING)
