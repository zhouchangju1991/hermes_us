from datetime import datetime
import logging, pytz, os
from pytz import timezone, utc

class Log:
    def __init__(self):
        today = datetime.now(pytz.timezone('US/Pacific')).strftime('%Y%m%d')
        file_name = '{}/log/hermes_us_{}.log'.format(os.path.dirname(os.path.realpath(__file__)), today)
        logging.basicConfig(filename=file_name,
                filemode='a',
                level=logging.INFO,
                format="%(asctime)s %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S")
        logging.Formatter.converter = self.__PacificTime
        self.__logger = logging.getLogger(__name__)

    def __PacificTime(*args):
        utc_dt = utc.localize(datetime.utcnow())
        pt_tz = timezone("US/Pacific")
        converted = utc_dt.astimezone(pt_tz)
        return converted.timetuple()

    def debug(self, message):
        self.__logger.debug(message)

    def info(self, message):
        self.__logger.info(message)

    def warning(self, message):
        self.__logger.warning(message)

    def error(self, message):
        self.__logger.error(message)

