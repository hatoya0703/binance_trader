import configparser
import ccxt

from utils.utils import bool_from_str

conf = configparser.ConfigParser()
conf.read('settings.ini')

binance_access_key = conf['binance']['access_key']
binance_secret_access_key = conf['binance']['secret_access_key']

db_name = conf['db']['name']
db_driver = conf['db']['driver']

web_port = int(conf['web']['port'])

client = ccxt.binance({'apiKey':conf['binance']['access_key'],'secret':conf['binance']['secret_access_key']})
ticker = conf['trading']['ticker']
currency = conf['trading']['currency']
symbol = ticker + currency
trade_duration = conf['trading']['trade_duration'].lower()
back_test = bool_from_str(conf['trading']['back_test'])
use_percent = float(conf['trading']['use_percent'])
past_period = int(conf['trading']['past_period'])
stop_limit_percent = float(conf['trading']['stop_limit_percent'])
num_ranking = int(conf['trading']['num_ranking'])