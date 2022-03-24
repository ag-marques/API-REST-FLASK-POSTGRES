from flask import Flask, jsonify
from flask_restful import Api
from resourse.usuarios import Buscas, Usuario, UsuariosModel, UsuarioCad, Index
from resourse.usuarioregistro import UsuarioLogin
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pronkgcntlhwgf:53422c537823b0475e7e0b95f20fd0584ad015e211c986d88c148ebe0a08dbe8@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d92ktmm9ee7pa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secretkey'  # Definindo a chave secreta
app.config['JWT_BLACKLIST_ENABLED'] = True  # Ativando o blacklist

api = Api(app)
jwt = JWTManager(app)

# Verifica se o token já está na blacklist
@jwt.token_in_blocklist_loader
def verificar_blacklist(self, token):
    return token['jti'] in BLACKLIST

# Se o token existir na BlackList 
@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message':'You have been logged out.'}), 401

# EndPoints
api.add_resource(Usuario,'/cadastro/<string:cpf>') # resourse.usuarios.Usuario + delete <string>
api.add_resource(UsuarioCad,'/cadastro/') # resourse.usuarios.UsuarioCad
api.add_resource(UsuarioLogin,'/login/') # resourse.usuarioregistro.UsuarioLogin
api.add_resource(Buscas,'/usuario') # resourse.usuarios.Buscas
api.add_resource(Index,'/') # resourse.usuarios.Buscas.index

# Antes da primeira requisição, cria o banco
@app.before_first_request
def cria_banco():
    db.create_all()

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)    
    app.run(debug=True)