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

    sma = request.args.get('sma')
    if sma:
        str_sma_period1 = request.args.get('smaPeriod1')
        str_sma_period2 = request.args.get('smaPeriod2')
        str_sma_period3 = request.args.get('smaPeriod3')

        if str_sma_period1:
            period1 = int(str_sma_period1)
        if str_sma_period2:
            period2 = int(str_sma_period2)
        if str_sma_period3:
            period3 = int(str_sma_period3)

        if not str_sma_period1 or period1 < 0:
            period1 = 7
        if not str_sma_period2 or period2 < 0:
            period2 = 14
        if not str_sma_period3 or period3 < 0:
            period3 = 50
        
        df.add_sma(period1)
        df.add_sma(period2)
        df.add_sma(period3)

    return jsonify(df.value), 200


def start():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
