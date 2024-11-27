from flask import Flask
from blueprint import scoring_bp

app = Flask(__name__)

app.register_blueprint(scoring_bp)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5003, debug=True)
