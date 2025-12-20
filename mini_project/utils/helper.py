from utils import math_ops
from common import logger

def help_me():
    logger.log("Helper function active")
    return math_ops.add(2, 3)
