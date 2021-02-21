#importar flask
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from datetime import date
import uuid
from mysql.connector import connect, Error
import json

#configuração
DEBUG = True
connection = connect(
        host= "localhost",
        user= "root",
        password="",
        database= "dg"
    )

#helpers
def listAllPessoas(connection):
    try:
        select_pessoas = "select id, nome, nascimento, YEAR(FROM_DAYS(TO_DAYS(NOW())-TO_DAYS(nascimento))) AS idade from pessoas"
        PESSOAS = []

        with connection.cursor() as cursor:
            cursor.execute(select_pessoas)
            result = cursor.fetchall()
            for row in result:
                PESSOAS.append({
                    'id': row[0],
                    'nome': row[1],
                    'nascimento': datetime.strftime(row[2], '%d/%m/%Y'),
                    'idade': row[3]
                })
            return PESSOAS
    except Error as e:
        return []

def salvarPessoa(nome, nascimento):
    try:
        select_pessoas = 'insert into pessoas(nome, nascimento) VALUES(%s,%s)'
        with connection.cursor() as cursor:
            datanascimento = datetime.strptime(nascimento, '%d/%m/%Y')
            cursor.execute(select_pessoas, (nome, datanascimento.strftime('%Y-%m-%d %H:%M:%S')))
            connection.commit()
    except Error as e:
        print(e)
    

def remove_pessoa(pessoa_id):
    for pessoa in PESSOAS:
        if pessoa['id'] == pessoa_id:
            PESSOAS.remove(pessoa)
            return True
    return False

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
        salvarPessoa(post_data.get('nome'),post_data.get('nascimento'))

        response_object['message'] = 'Pessoa Cadastrada!'
    else:
        response_object['pessoas'] = listAllPessoas(connection)
    return jsonify(response_object)

@app.route('/pessoas/<pessoa_id>', methods=['PUT', 'DELETE'])
def single_pessoa(pessoa_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_pessoa(pessoa_id)
        nascimento = post_data.get('nascimento')

        #PESSOAS.append({
        #    'id': uuid.uuid4().hex,
        #    'nome': post_data.get('nome'),
        #    'nascimento': nascimento,
        #    'idade': calcular_idade(datetime.strptime(nascimento, '%d/%m/%Y'))
        #})
        response_object['message'] = 'Pessoa Atualizada!'
    if request.method == 'DELETE':
        remove_pessoa(pessoa_id)
        response_object['message'] = 'Pessoa Excluída!'
    return jsonify(response_object)
if __name__ == '__main__':
    app.run()