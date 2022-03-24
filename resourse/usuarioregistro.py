from flask_restful import Resource, reqparse
from models.usuarios import UsuariosModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import check_password_hash
from blacklist import BLACKLIST

class UsuarioLogin(Resource):

    @classmethod
    def post(cls):

        # Opções de login por email, cpf ou pis + senha
        valores = reqparse.RequestParser()
        valores.add_argument('email', type=str)
        valores.add_argument('cpf', type=str)
        valores.add_argument('pis', type=str)
        valores.add_argument('senha', type=str)
        dados = valores.parse_args()

        user = UsuariosModel.find_by_login(dados['email'], dados['cpf'], dados['pis'])
        #if (user) and check_password_hash(user.senha, senha): 
        if user and check_password_hash(user['senha'], dados['senha']):
            # safe_str_cmp: forma segura de comparar duas strings.
            token_de_acesso = create_access_token(identity=user['cpf'])
            return {'access_token': token_de_acesso}, 200
        return {'message':'The username or password is incorret.'}, 401

class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # jti - JWT Token Identifier
        BLACKLIST.app(jwt_id)
        return {'message':'Logged out successfully'}, 200