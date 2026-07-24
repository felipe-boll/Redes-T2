import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Usa a URL do Postgres se estiver no Docker, caso contrário cria um banco SQLite local
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///local_db.db")
db = SQLAlchemy(app)


# Tabela 'messages' mapeada para armazenar os avisos de achados e perdidos
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)   # Nome/Contato de quem publicou
    text = db.Column(db.Text, nullable=False)          # Descrição do objeto e local
    ip_client = db.Column(db.String(45), nullable=True)  # IP do dispositivo do usuário (informado no payload)
    ip_origin = db.Column(db.String(45), nullable=True)  # IP de origem do roteamento na rede Docker
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


with app.app_context():
    db.create_all()


@app.get("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})


# Endpoint para listar os avisos cadastrados
@app.get("/messages")
def list_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "text": m.text,
            "ip_client": m.ip_client,
            "ip_origin": m.ip_origin,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ])


# Endpoint para criar um novo aviso de achado/perdido
@app.post("/messages")
def create_message():
    data = request.get_json()
    # Valida se os campos obrigatórios foram enviados: name (contato) e text (descrição do objeto)
    if not data or not data.get("name") or not data.get("text"):
        return jsonify({"error": "campos 'name' (nome) e 'text' (objeto/local) são obrigatórios"}), 400
    
    msg = Message(
        name=data["name"],        # Nome do usuário
        text=data["text"],        # Descrição do objeto e local
        ip_client=data.get("ip_client"),  # IP do dispositivo que postou
        ip_origin=request.remote_addr,    # IP real de onde o pedido chegou no Docker
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"id": msg.id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
