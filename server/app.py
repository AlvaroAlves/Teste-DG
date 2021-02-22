#importar flask
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from datetime import date
import uuid
from mysql.connector import connect, Error
import json
import pip 

#configuração
DEBUG = True
connection = connect(
        host= "localhost",
        user= "root",
        password="",
        database= "dg"
    )

#helpers
def listAllPessoas():
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

def salvar_pessoa(nome, nascimento):
    try:
        select_pessoas = 'insert into pessoas(nome, nascimento) VALUES(%s,%s)'
        with connection.cursor() as cursor:
            datanascimento = datetime.strptime(nascimento, '%d/%m/%Y')
            cursor.execute(select_pessoas, (nome, datanascimento.strftime('%Y-%m-%d %H:%M:%S')))
            connection.commit()
    except Error as e:
        print(e)
    
def remove_pessoa(pessoa_id):
    try:
        delete_pessoas = "delete from pessoas WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(delete_pessoas, (pessoa_id,))
            return True
    except Error as e:
        print(e)
        return False

def update_pessoa(pessoa_id, nome, nascimento):
    try:
        update_pessoas = 'update pessoas set nome = %s, nascimento = %s WHERE id= %s'
        with connection.cursor() as cursor:
            datanascimento = datetime.strptime(nascimento, '%d/%m/%Y')
            cursor.execute(update_pessoas, (nome, datanascimento.strftime('%Y-%m-%d %H:%M:%S'),pessoa_id))
            connection.commit()
    except Error as e:
        print(e)

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
        salvar_pessoa(post_data.get('nome'),post_data.get('nascimento'))

        response_object['message'] = 'Pessoa Cadastrada!'
    else:
        response_object['pessoas'] = listAllPessoas()
    return jsonify(response_object)

@app.route('/pessoas/<pessoa_id>', methods=['PUT', 'DELETE'])
def single_pessoa(pessoa_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        update_pessoa(pessoa_id,post_data.get('nome'),post_data.get('nascimento'))
        
        response_object['message'] = 'Pessoa Atualizada!'
    if request.method == 'DELETE':
        remove_pessoa(pessoa_id)
        response_object['message'] = 'Pessoa Excluída!'
    return jsonify(response_object)
if __name__ == '__main__':
    app.run()