from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    tarefas = db.relationship("Tarefa", backref="usuario", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "criado_em": self.criado_em.isoformat()}

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    tarefas = db.relationship("Tarefa", backref="categoria", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao, "criado_em": self.criado_em.isoformat()}

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.Enum('pendente','em_progresso','concluida', name="status_enum"), default='pendente')
    data_vencimento = db.Column(db.Date, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "data_vencimento": self.data_vencimento.isoformat() if self.data_vencimento else None,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "criado_em": self.criado_em.isoformat()
        }
