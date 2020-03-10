'''
IP的调用api
'''
from flask import Flask,g
from ipsave import Redissaveip

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = Redissaveip()
    return g.redis

@app.route('/')
def index():
    return '<h2>IP池首页<h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.randomip()

@app.route('/count')
def get_count():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    pass
    #app.run('127.0.0.1',8888)