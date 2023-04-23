from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import settings
import constans
from app.models.dfcandle import DataFrameCandle

app = Flask(__name__, template_folder='../views', static_folder='../static')

@app.teardown_appcontext
def remove_session(ex=None):
    from app.models.base import Session
    Session.remove()

@app.route('/')
def index():
    return render_template('./chart.html')

@app.route('/api/candle/', methods=['GET'])
def api_make_handler():
    
    symbole = request.args.get('symbol')
    if not symbole:
        return jsonify({'error': 'no symbole params'}), 400

    limit_str = request.args.get('limit')
    limit = 1000
    if limit_str:
        limit = int(limit_str)

    if limit < 0 or limit > 1000:
        limit = 1000

    duration = request.args.get('duration')
    if not duration:
        duration = constans.DURATION_5M

    df = DataFrameCandle(symbole, duration)
    df.set_all_candles(limit)
    return jsonify(df.value), 200 
    # df = DataFrameCandle(settings.symbol, settings.trade_duration)
    # df.set_all_candles(settings.past_period)
    
    # candles = df.candles
    # return render_template('./google.html', candles=candles) 


def start():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
