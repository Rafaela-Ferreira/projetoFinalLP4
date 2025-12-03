# Sistema de Tarefas – Trabalho de LP4
Rafaela Ferreira Dos Santos - CP3026353


Aplicação para gerenciamento de tarefas com usuários e categorias.  
Inclui **API REST em Flask** e uma **interface HTML simples** consumindo a API.

---

## 📌 Objetivo
Implementar um sistema capaz de:

- Criar e gerenciar usuários
- Criar categorias
- Criar, listar, atualizar e excluir tarefas
- Expor todos os recursos via API REST
- Consumir a API através de uma página HTML/JS

---

## 🧰 Tecnologias Utilizadas

### Backend
- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PyMySQL
- python-dotenv

### Banco de Dados
- MySQL ou MariaDB

### Frontend
- HTML + JavaScript (fetch API)

---

## 🔗 Endpoints Principais

### Usuários
- `POST /usuarios` – criar usuário  
- `GET /usuarios` – listar  
- `GET /usuarios/<id>` – obter  
- `PUT /usuarios/<id>` – atualizar  
- `DELETE /usuarios/<id>` – remover  

### Categorias
- `POST /categorias`  
- `GET  /categorias`  
- `PUT  /categorias/<id>`  
- `DELETE /categorias/<id>`  

### Tarefas
- `POST /tarefas`  
- `GET /tarefas?usuario_id=&status=`  
- `GET /tarefas/<id>`  
- `PUT /tarefas/<id>`  
- `DELETE /tarefas/<id>`  

---

## 🚀 Como rodar o projeto localmente (Windows)

### 1️⃣ Criar e ativar o ambiente virtual

Caso ainda não tenha um venv:

```bash
"C:\Users\Rafaela\AppData\Local\Programs\Python\Python314\python.exe" -m venv venv

```

## Ativar o ambiente:

venv\Scripts\activate


## Instalar dependências

pip install flask flask_sqlalchemy flask_migrate werkzeug
pip install python-dotenv
pip install pymysql


## Altere a senha do banco de dados
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:senha@localhost:3306/tarefas_db")

## Rodar o servidor Flask

python app.py

## A API ficará disponível em:

http://127.0.0.1:5000
