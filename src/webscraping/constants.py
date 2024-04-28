from datetime import datetime

URL_FBREF = 'https://fbref.com'
URL_TRANSFERMARKT = 'https://www.transfermarkt.com'

now = datetime.now()
SEASONS_LIST = list(map(str, range(2014, now.year)))