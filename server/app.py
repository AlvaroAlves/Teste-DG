#importar flask
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from datetime import date
import uuid

#configuração
DEBUG = True

#data de nascimento aleatoria
date_time_str = '11/05/1987'
date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')

#helpers
def calcular_idade(dataNascimento):
    hoje = date.today()
    idade = hoje.year - dataNascimento.year - ((hoje.month, hoje.day) < (dataNascimento.month, dataNascimento.day))
    return idade

def remove_pessoa(pessoa_id):
    for pessoa in PESSOAS:
        if pessoa['id'] == pessoa_id:
            PESSOAS.remove(pessoa)
            return True
    return False
#Cria uma lista de pessoas
PESSOAS = [
    {
        'id': uuid.uuid4().hex,
        'nome':'Alvaro Alves',
        'nascimento': date_time_obj.strftime('%d/%m/%Y'),
        'idade': calcular_idade(date_time_obj)
    }
]

#instanciar o app
app = Flask(__name__)
app.config.from_object(__name__)

#habilitar o CORS
CORS(app, resources={r'/*': {'origins':'*'}})

#sanitizar a rota de verificação
@app.route('/ping', methods=['get'])
def ping_pong():
    return jsonify('pong!')

@app.route('/pessoas', methods=['GET', 'POST'])
def all_pessoas():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        nascimento = post_data.get('nascimento')

        PESSOAS.append({
            'id': uuid.uuid4().hex,
            'nome': post_data.get('nome'),
            'nascimento': nascimento,
            'idade': calcular_idade(datetime.strptime(nascimento, '%d/%m/%Y'))
        })
        response_object['message'] = 'Pessoa Cadastrada!'
    else:
        response_object['pessoas'] = PESSOAS
    return jsonify(response_object)

@app.route('/pessoas/<pessoa_id>', methods=['PUT', 'DELETE'])
def single_pessoa(pessoa_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_pessoa(pessoa_id)
        nascimento = post_data.get('nascimento')

        PESSOAS.append({
            'id': uuid.uuid4().hex,
            'nome': post_data.get('nome'),
            'nascimento': nascimento,
            'idade': calcular_idade(datetime.strptime(nascimento, '%d/%m/%Y'))
        })
        response_object['message'] = 'Pessoa Atualizada!'
    if request.method == 'DELETE':
        remove_pessoa(pessoa_id)
        response_object['message'] = 'Pessoa Excluída!'
    return jsonify(response_object)
if __name__ == '__main__':
    app.run()