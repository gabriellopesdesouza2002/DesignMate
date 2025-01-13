from designmate.utils.utils import *


class Flask:
    def __init__(self, project_name):
        """
        Inicializa a estrutura de um projeto Flask.

        Args:
            project_name (str): Nome do projeto. Será usado como nome do diretório raiz.
        """
        self.PROJECT_NAME = project_name
        self.app = f'{self.PROJECT_NAME}/app'
        self.models = f'{self.PROJECT_NAME}/app/models'
        self.routes = f'{self.PROJECT_NAME}/app/routes'
        self.services = f'{self.PROJECT_NAME}/app/services'
        self.utils = f'{self.PROJECT_NAME}/app/utils'
        self.extensions = f'{self.PROJECT_NAME}/app/extensions'
        
        self.tests = f'{self.PROJECT_NAME}/tests'
        
        self.migrations = f'{self.PROJECT_NAME}/migrations'

        self.paths = [self.app, self.models, self.routes, self.services, self.utils, self.extensions, self.tests, self.migrations, self.PROJECT_NAME]
        

    def create(self):
        """
Cria a estrutura de diretórios e arquivos para um projeto Flask seguindo o padrão modular.

### Estrutura Criada:

- *PROJECT_NAME/*
  - *app/*
    - *__init__.py*: Inicializa a aplicação Flask e registra blueprints.
    - *models/*
      - *user.py*: Modelo de usuário com campos básicos.
    - *routes/*
      - *user_routes.py*: Rotas para o recurso "usuário".
    - *services/*
      - *user_service.py*: Serviços para manipulação de usuários.
    - *utils/*
      - *validators.py*: Funções de validação para email e username.
    - *config.py*: Configurações da aplicação para diferentes ambientes.
    - *extensions.py*: Inicializa extensões do Flask, como SQLAlchemy.
    - *errors.py*: Handlers de erros personalizados.
  - *tests/*
    - *test_user_routes.py*: Testes para as rotas de usuário.
    - *conftest.py*: Configurações para pytest (fixtures, etc.).
  - *migrations/*: Pasta para migrações do banco de dados (se usar Flask-Migrate).
  - *requirements.txt*: Lista de dependências do projeto.
  - *.env*: Variáveis de ambiente (usando python-dotenv).
  - *.gitignore*: Arquivos e pastas ignorados pelo Git.
  - *run.py*: Script para rodar a aplicação.
  - *README.md*: Documentação do projeto.

    Como Executar:
    1. Crie o ambiente virtual:
       ```bash
       python -m venv venv
       ```
    2. Ative o ambiente virtual:
       - No Linux/Mac:
         ```bash
         source venv/bin/activate
         ```
       - No Windows:
         ```bash
         venv\Scripts\activate
         ```
    3. Instale as dependências:
       ```bash
       pip install -r requirements.txt
       ```
    4. Execute a aplicação:
       ```bash
       python run.py
       ```
    5. Teste as rotas:
       - Listar usuários:
         ```bash
         curl http://127.0.0.1:5000/api/users/
         ```
       - Criar usuário:
         ```bash
         curl -X POST -H "Content-Type: application/json" -d '{"username": "test", "email": "test@example.com"}' http://127.0.0.1:5000/api/users/
         ```

    Observação:
    - O banco de dados SQLite é configurado por padrão.
    - Para migrações de banco de dados, instale o Flask-Migrate e execute `flask db init`, `flask db migrate`, e `flask db upgrade`.
        """
        print(f'Criando diretórios para projeto Flask... {self.PROJECT_NAME}')
        cria_diretorio_no_local_do_projeto(self.PROJECT_NAME)
        
        for path in self.paths:
            cria_diretorio_no_local_do_projeto(path)
            
        print('Criando arquivos!')
        with open(f'{self.app}/__init__.py', 'w') as f:
            f.write("""from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Banco de dados SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões
    db.init_app(app)

    # Registra blueprints (rotas)
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app""")
        
        with open(f'{self.app}/extensions.py', 'w') as f:
            f.write("""from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()""")



        with open(f'{self.app}/extensions.py', 'w') as f:
            f.write("""""")
            
        with open(f'{self.models}/user.py', 'w') as f:
            f.write("""from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'""")
            
            
            
        with open(f'{self.routes}/user_routes.py', 'w') as f:
            f.write("""from flask import Blueprint, jsonify, request
from app.models.user import User
from app.extensions import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201""")
            
            
            
        with open(f'{self.services}/user_service.py', 'w') as f:
            f.write("""from app.models.user import User

def get_all_users():
    return User.query.all()

def create_user(username, email):
    new_user = User(username=username, email=email)
    return new_user""")
            
        with open(f'{self.utils}/validators.py', 'w') as f:
            f.write("""def validate_email(email):
    return '@' in email

def validate_username(username):
    return len(username) >= 3""")
            
        with open(f'{self.app}/config.py', 'w') as f:
            f.write("""class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/prod_db'
    DEBUG = False""")
            
        with open(f'{self.app}/errors.py', 'w') as f:
            f.write("""from flask import jsonify

def handle_not_found_error(e):
    return jsonify({"error": "Resource not found"}), 404

def handle_bad_request_error(e):
    return jsonify({"error": "Bad request"}), 400""")
            
        with open(f'{self.tests}/test_user_routes.py', 'w') as f:
            f.write("""import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert response.json == []

def test_create_user(client):
    response = client.post('/api/users/', json={'username': 'test', 'email': 'test@example.com'})
    assert response.status_code == 201
    assert response.json['username'] == 'test'
    assert response.json['email'] == 'test@example.com'""")
        with open(f'{self.PROJECT_NAME}/requirements.txt', 'w') as f:
            f.write("""Flask==2.3.2
Flask-SQLAlchemy==3.0.5
pytest==7.4.0""")
        with open(f'{self.PROJECT_NAME}/run.py', 'w') as f:
            f.write("""from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)""")
        with open(f'{self.PROJECT_NAME}/.env', 'w') as f:
            f.write("""FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key""")
        with open(f'{self.PROJECT_NAME}/.gitignore', 'w') as f:
            f.write("""__pycache__/
venv/
.env
*.sqlite3""")
        with open(f'{self.PROJECT_NAME}/README.md', 'w') as f:
            f.write("""# Flask API

Esta é uma API Flask para gerenciar usuários.

## Instalação

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Ative o ambiente virtual:
   - No Linux/Mac: `source venv/bin/activate`
   - No Windows: `venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`.
5. Execute a aplicação: `python run.py`.

## Rotas

- `GET /api/users/`: Retorna todos os usuários.
- `POST /api/users/`: Cria um novo usuário.""")
        with open(f'{self.extensions}/extensions.py', 'w') as f:
            f.write("""from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()""")
        
        
    def delete(self):
        for path in self.paths:
            if os.path.exists(path):
                shutil.rmtree(path)
