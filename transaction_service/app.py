from flask import Flask
from blueprint import transaction_bp
from init_db import init_neo4j, init_redis

app = Flask(__name__)

app.register_blueprint(transaction_bp)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

with app.app_context():
    app.neo4j_driver = init_neo4j()
    app.redis_client = init_redis()

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5001)
