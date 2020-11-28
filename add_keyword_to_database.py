from datetime import datetime
import pytz
from database import Database

database = Database()

keywords = ['evelyne 16 amazone bag',
        'herbag zip 31',
        'picotin lock 18',
        'picotin lock 22',
        'kelly classique to go',
        'lindy 26',
        'lindy mini',
        'roulis mini',
        'roulis 23',
        'rodeo',
        'constance long to go',
        'oran nano',]
for keyword in keywords:
    timestamp = datetime.now(pytz.timezone('US/Pacific'))
    document_name = keyword.lower().replace(' ', '_')
    data = {
        'keyword': keyword,
        'is_valid': True,
        'created_at': timestamp,
        'updated_at': timestamp,
    }

    if not database.document('hermes_us_keyword', document_name).get().to_dict():
        database.update_document('hermes_us_keyword', document_name, data, False)
