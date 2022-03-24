# API REST com Flask e Postgres
 
## API para manipulação de usuários - CRUD

### Estrutura da Ferramenta

#### Pasta do Projeto <br>
----- <b> models </b> <br>
--------- <i>usuarios.py </i><br>
----- <b> resourse </b> <br>
--------- <i>usuarioregistro.py </i> <br>
--------- <i>usuarios.py </i> <br>
----- <i>app.py </i> <br>

### O que é API REST?

API REST, também chamada de API RESTful, é uma interface de programação de aplicações (API ou API web) que está em conformidade com as restrições do estilo de arquitetura REST, permitindo a interação com serviços web RESTful. <br>
REST significa Representational State Transfer ou tansferência de estado representacional. <br>
<br>
Utilizei no framework Flask a extenção <b>flask_restful</b> que possui suporte para construção rápida de APIs REST.
<br>
### Exemplo mínimo de uma aplicação Flask utilizando Flask-RESTful.<br>
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
&nbsp;&nbsp;def get(self):
&nbsp;&nbsp;&nbsp;&nbsp;return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
&nbsp;&nbsp;app.run(debug=True)


