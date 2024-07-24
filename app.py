from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re


app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sistema_de_login.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class Sistema(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    
    def __init__(self, email, senha):
        self.email = email
        self.senha = generate_password_hash(senha)
        
    def verficar_senha(self, pwd):
        return check_password_hash(self.senha, pwd)
        

def EmailInvalido(email):
    remail = r'\b[A-Ba-z0-9._%+-]+@[a-z0-9.-]+\.[\com]'
    if email != remail:
        return flash('Email Inválido, por favor digite um Email Válido')
    else:
        email = re.match(email)

@app.route('/LoginFinalizado')
def LoginFinalizado():
    message = 'ParabÉns'
    return render_template('parabens.html', message=message)
 
@app.route('/', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')
        system = Sistema.query.filter_by(email=email).first()
        
        if not system or not system.verficar_senha(senha):
            flash('Deu Errado, Por Favor, digite um Email ou Senha Corretos')
        else: 
            return redirect(url_for('LoginFinalizado'))
    return render_template('index.html')

@app.route('/Cadastro', methods=['POST', 'GET'])
def Cadastro():
    email = request.form.get('email')
    senha = request.form.get('password')
    
    if request.method == 'POST':
        if not email or not senha:
            flash('Você preencheu tudo ou nada, por favor preencha')
        elif EmailInvalido(email=email):
            flash('Email Inválido, por favor digite um Email Válido')
        else:
            sistema = Sistema(email, senha)
            db.session.add(sistema)
            db.session.commit()
            flash('Parabens você fez o Cadastro, agora retorne e faça o Login!')
    return render_template('cadastro.html')
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    with app.app_context():
        db.create_all()
    app.run(debug=True)