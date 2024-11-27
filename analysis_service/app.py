from flask import Flask
from blueprint import analysis_bp
from init_db import init_neo4j, init_redis

app = Flask(__name__)

app.register_blueprint(analysis_bp)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

with app.app_context():
    app.neo4j_driver = init_neo4j()
    app.redis_client = init_redis()

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5002, debug=True)
