from flask import Flask, jsonify, request, abort, render_template
from config import Config
from models import db, Usuario, Categoria, Tarefa
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def home():
        #return {"message": "API rodando!"}
        return render_template("index.html")

    @app.route("/usuarios", methods=["POST"])
    def criar_usuario():
        data = request.get_json()
        if not data or not data.get("nome") or not data.get("email") or not data.get("senha"):
            return jsonify({"erro":"dados incompletos"}), 400
        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"erro":"email já cadastrado"}), 409
        senha_hash = generate_password_hash(data["senha"])
        u = Usuario(nome=data["nome"], email=data["email"], senha_hash=senha_hash)
        db.session.add(u); db.session.commit()
        return jsonify(u.to_dict()), 201

    @app.route("/usuarios", methods=["GET"])
    def listar_usuarios():
        usuarios = Usuario.query.all()
        return jsonify([u.to_dict() for u in usuarios])

    @app.route("/usuarios/<int:id>", methods=["GET"])
    def obter_usuario(id):
        u = Usuario.query.get_or_404(id)
        return jsonify(u.to_dict())

    @app.route("/usuarios/<int:id>", methods=["PUT"])
    def atualizar_usuario(id):
        u = Usuario.query.get_or_404(id)
        data = request.get_json()
        if data.get("nome"): u.nome = data["nome"]
        if data.get("email"): u.email = data["email"]
        if data.get("senha"): u.senha_hash = generate_password_hash(data["senha"])
        db.session.commit()
        return jsonify(u.to_dict())

    @app.route("/usuarios/<int:id>", methods=["DELETE"])
    def deletar_usuario(id):
        u = Usuario.query.get_or_404(id)
        db.session.delete(u); db.session.commit()
        return jsonify({"msg":"deletado"}), 204

    # --- Categorias (CRUD) ---
    @app.route("/categorias", methods=["POST"])
    def criar_categoria():
        data = request.get_json()
        if not data or not data.get("nome"):
            return jsonify({"erro":"nome requerido"}), 400
        if Categoria.query.filter_by(nome=data["nome"]).first():
            return jsonify({"erro":"categoria existente"}), 409
        c = Categoria(nome=data["nome"], descricao=data.get("descricao"))
        db.session.add(c); db.session.commit()
        return jsonify(c.to_dict()), 201

    @app.route("/categorias", methods=["GET"])
    def listar_categorias():
        cats = Categoria.query.all()
        return jsonify([c.to_dict() for c in cats])

    @app.route("/categorias/<int:id>", methods=["PUT"])
    def atualizar_categoria(id):
        c = Categoria.query.get_or_404(id)
        data = request.get_json()
        if data.get("nome"): c.nome = data["nome"]
        if "descricao" in data: c.descricao = data["descricao"]
        db.session.commit()
        return jsonify(c.to_dict())

    @app.route("/categorias/<int:id>", methods=["DELETE"])
    def deletar_categoria(id):
        c = Categoria.query.get_or_404(id)
        db.session.delete(c); db.session.commit()
        return jsonify({"msg":"deletado"}), 204

    # --- Tarefas (CRUD) ---
    @app.route("/tarefas", methods=["POST"])
    def criar_tarefa():
        data = request.get_json()
        required = ["titulo", "usuario_id"]
        if not data or not all(k in data for k in required):
            return jsonify({"erro":"dados incompletos: titulo e usuario_id são obrigatórios"}), 400
        # checar usuario existente
        if not Usuario.query.get(data["usuario_id"]):
            return jsonify({"erro":"usuario não encontrado"}), 404
        if data.get("categoria_id") and not Categoria.query.get(data["categoria_id"]):
            return jsonify({"erro":"categoria não encontrada"}), 404
        t = Tarefa(
            titulo=data["titulo"],
            descricao=data.get("descricao"),
            status=data.get("status","pendente"),
            data_vencimento=data.get("data_vencimento"),
            usuario_id=data["usuario_id"],
            categoria_id=data.get("categoria_id")
        )
        db.session.add(t); db.session.commit()
        return jsonify(t.to_dict()), 201

    @app.route("/tarefas", methods=["GET"])
    def listar_tarefas():
        q = Tarefa.query
        usuario_id = request.args.get("usuario_id")
        status = request.args.get("status")
        if usuario_id: q = q.filter_by(usuario_id=int(usuario_id))
        if status: q = q.filter_by(status=status)
        tarefas = q.all()
        return jsonify([t.to_dict() for t in tarefas])

    @app.route("/tarefas/<int:id>", methods=["GET"])
    def obter_tarefa(id):
        t = Tarefa.query.get_or_404(id)
        return jsonify(t.to_dict())

    @app.route("/tarefas/<int:id>", methods=["PUT"])
    def atualizar_tarefa(id):
        t = Tarefa.query.get_or_404(id)
        data = request.get_json()
        for k in ("titulo","descricao","status","data_vencimento","categoria_id"):
            if k in data:
                setattr(t, k, data[k])
        db.session.commit()
        return jsonify(t.to_dict())

    @app.route("/tarefas/<int:id>", methods=["DELETE"])
    def deletar_tarefa(id):
        t = Tarefa.query.get_or_404(id)
        db.session.delete(t); db.session.commit()
        return jsonify({"msg":"deletado"}), 204

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro":"não encontrado"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
