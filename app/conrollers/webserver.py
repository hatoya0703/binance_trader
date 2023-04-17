from flask import Flask
from flask import render_template

import settings
from app.models.dfcandle import DataFrameCandle

app = Flask(__name__, template_folder='../views')

@app.teardown_appcontext
def remove_session(ex=None):
    from app.models.base import Session
    Session.remove()

@app.route('/')
def index():
    df = DataFrameCandle(settings.symbol, settings.trade_duration)
    df.set_all_candles(settings.past_period)
    
    candles = df.candles
    return render_template('./google.html', candles=candles) 


def start():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
