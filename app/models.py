from app import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.Enum('admin', 'empleado'), default='empleado')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.id_usuario)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

class Gelatina(db.Model):
    __tablename__ = 'gelatinas'
    id_gelatina = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(255))
    categoria = db.relationship('Categoria', backref='gelatinas')

class Stock(db.Model):
    __tablename__ = 'stock'
    id_stock = db.Column(db.Integer, primary_key=True)
    id_gelatina = db.Column(db.Integer, db.ForeignKey('gelatinas.id_gelatina'))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    gelatina = db.relationship('Gelatina', backref='stock')

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'))
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado'), default='pendiente')
    total = db.Column(db.Numeric(10, 2))
    cliente = db.relationship('Cliente', backref='pedidos')

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'))
    id_gelatina = db.Column(db.Integer, db.ForeignKey('gelatinas.id_gelatina'))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    pedido = db.relationship('Pedido', backref='detalles')
    gelatina = db.relationship('Gelatina', backref='detalles')