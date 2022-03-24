import re
from urllib import response
from flask_restful import Resource, reqparse
from models.usuarios import UsuariosModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from flask import make_response, jsonify


# Criado de forma global para evitar que o mesmo código seja repetido em mais de um ponto como no post e put
atributos = reqparse.RequestParser()
atributos.add_argument('cpf', type=str)
atributos.add_argument('nome', type=str, required=True, help="The field 'Nome' cannot be left blank.")
atributos.add_argument('email', type=str, required=True, help="The field 'E-Mail' cannot be left blank.")
atributos.add_argument('pais', type=str, required=True, help="The field 'País' cannot be left blank.")
atributos.add_argument('estado', type=str, required=True, help="The field 'Estado' cannot be left blank.")
atributos.add_argument('municipio', type=str, required=True, help="The field 'Município' cannot be left blank.")
atributos.add_argument('cep', type=str, required=True, help="The field 'CEP' cannot be left blank.")
atributos.add_argument('rua', type=str, required=True, help="The field 'Rua' cannot be left blank.")
atributos.add_argument('numero', type=str, required=True, help="The field 'Número' cannot be left blank.")
atributos.add_argument('complemento', type=str)
atributos.add_argument('pis', type=str, required=True, help="The field 'PIS' cannot be left blank.")
atributos.add_argument('senha', type=str)

class UsuarioCad(Resource):

    def post(self):
        # Cadastrar Usuário - CREATE
        # Input: Formulário com todos os dados da tabela tb_users, não usa token
        # Output: Mensagem + Código 201 ou 500        
        dados = atributos.parse_args()

        if UsuariosModel.find_by_cpf_pis(dados['cpf']):
            return {"message":"The cpf {} already exists.".format(dados['cpf'])}        
        try:
            usuario = UsuariosModel(**dados)
            usuario.save_usuario()
            return {"message":"User created successfull!"}, 201
        except:
            return {"message":"An internal error ocurred tryping to save user."}, 500

class Usuario(Resource):    
    @jwt_required()
    def put(self, cpf):
        # Alterar dados do usuário - UPDATE
        # Input: Formulário com todos os dados da tabela (tb_users), exceto senha, esta alteração não considera alteração de senha.
        # Output: Mensagem + Código 201 ou 500        
        dados = atributos.parse_args()
        dados['cpf'] = cpf # como o cpf foi informado na url ficou em branco no dict
        usuario = UsuariosModel.find_by_cpf_pis(cpf)

        if usuario:            
            del dados['senha']
            usuario.update_user(**dados)
            try:
                usuario.save_usuario()
                return usuario.json(), 200 # success
            except:
                return {'message':'An internal error ocurred tryping to save user.'}, 500               
        else:
            usuario = UsuariosModel(**dados)
            try:
                usuario.save_usuario()
                return usuario.json(), 201 # create
            except:
                return {'message':'An internal error ocurred tryping to save user.'}, 500   
    
    @jwt_required()        
    def delete(self, cpf):
        # Deleta usuário pelo cpf - DELETE
        # Input: CPF
        # Output: Mensagem + Código 404 ou 500        

        usuario = UsuariosModel.find_by_cpf_pis(cpf)
        if usuario:
            try:
                usuario.delete_usuario()
                return {'message':'User deleted.'}
            except:
                return {'message':'An internal error ocorred tryping to delete user.'}, 500          
        return {'message':'User not found.'}, 404

class Buscas(Resource):  

    @jwt_required()  
    def get(self):
        # Deleta usuário pelo cpf - READ
        # Input: CPF ou PIS ou nome. CPF e PIS são consultas exatas, já o nome busca por partes/like.
        # Output: Usuários localizados na consulta - Mensagem + Código 404 ou 500               
        path_params = reqparse.RequestParser()
        path_params.add_argument('cpf', type=str)
        path_params.add_argument('pis', type=str)
        path_params.add_argument('nome', type=str)        
        param = path_params.parse_args() 

        if param['cpf']:
            cpfn = re.sub('[^0-9]+','',param['cpf']) # retornar somente números
            if (len(cpfn) == 11):        
                cpfn = re.sub("(\d{3})(\d{3})(\d{3})(\d{2})","\\1.\\2.\\3-\\4",cpfn) # Formatar cpf antes da busca
                usuario = UsuariosModel.find_by_cpf_pis(cpfn)
        elif param['nome']:     
            nome = re.sub('\b[^a-zA-Z]+','',param['nome']) # retornar somente letras e espaço
            if (len(nome) >=1):
                usuario = UsuariosModel.find_by_nome(nome)
        elif param['pis']: 
            pis = re.sub('[^0-9]+','',param['pis']) # retornar somente números                         
            if (len(pis) == 11):
                pis = re.sub("(\d{3})(\d{5})(\d{2})(\d{1})","\\1.\\2.\\3-\\4",pis) # Formatar PIS
                usuario = UsuariosModel.find_by_cpf_pis(pis)                

        if usuario:
            return usuario, 201
        return {'message':'User not found'}, 404

class Index(Resource):
    def get(self):
        responseBody = {'Sistema':'REST API'}
        return make_response(jsonify(responseBody), 200)


        
        