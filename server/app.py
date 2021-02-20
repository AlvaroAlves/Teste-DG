#importar flask
from flask import Flask, jsonify
from flask_cors import CORS

#configuração
DEBUG = True

#instanciar o app
app = Flask(__name__)
app.config.from_object(__name__)

#habilitar o CORS
CORS(app, resources={r'/*': {'origins':'*'}})

#sanitizar a rota de verificação
@app.route('/ping', methods=['get'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()