from __future__ import absolute_import

import logging
import logging.config

def init_log():
    logging.config.fileConfig('./utils/logging.conf')
    logger = logging.getLogger(__name__)
    logger.info("Custom logging started.")
    logger.info("Complete!")
    return logger
