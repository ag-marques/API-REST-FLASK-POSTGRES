from werkzeug.security import generate_password_hash, check_password_hash
from sql_alchemy import db
import re

class UsuariosModel(db.Model):    
    __tablename__ = 'tb_users'

    cpf = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(80))
    pais = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    municipio = db.Column(db.String(60))
    cep = db.Column(db.String(20))  
    rua = db.Column(db.String(100))
    # numero str para receber s/n ou 10
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(10))
    pis = db.Column(db.String(20))
    senha = db.Column(db.String(128))

    def __init__(self, cpf, nome, email, pais, estado, municipio, cep, rua, numero, complemento, pis, senha):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.pais = pais
        self.estado = estado
        self.municipio = municipio
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.pis = pis
        self.senha = generate_password_hash(senha)
    
    def json(self):
        return {
            'cpf':self.cpf,
            'nome':self.nome,
            'email':self.email,
            'pais':self.pais,
            'estado':self.estado,
            'municipio':self.municipio,
            'cep':self.cep,
            'rua':self.rua,
            'numero':self.numero,
            'complemento':self.complemento,
            'pis':self.pis,
            'senha':self.senha
        }
    
    def save_usuario(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, cpf, nome, email, pais, estado, municipio, cep, rua, numero, complemento, pis):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.pais = pais
        self.estado = estado
        self.municipio = municipio
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.pis = pis

    @classmethod
    def find_by_cpf_pis(cls, num):        
        
        if re.search("^\d{3}[.]\d{5}[.]\d{2}[-]\d{1}$",num):
            user = cls.query.filter_by(pis=num).first()
        elif re.search("^\d{3}[.]\d{3}[.]\d{3}[-]\d{2}$",num):
            user = cls.query.filter_by(cpf=num).first()            

        if user:
            return user
        return None 

    @classmethod
    def find_by_nome(cls, nome):
        user = cls.query.filter(cls.nome.ilike(f'%{nome}%')).all()
        result = []
        if user:
            for linha in user:
                result.append(linha.json()) 
            return {'Resultado':result}
        return None

    @classmethod
    def find_by_login(cls, email, cpf, pis):
        if email:
            user = cls.query.filter_by(email=email).first() 
        elif cpf:    
            user = UsuariosModel.find_by_cpf_pis(cpf) 
        elif pis:    
            user = cls.query.filter_by(pis=pis).first() 
        if user:
            return user.json()
        return None             
    
    def delete_usuario(self):
        db.session.delete(self)
        db.session.commit()
