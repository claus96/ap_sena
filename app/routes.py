from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app.models import Usuario, Gelatina, Categoria, Stock, Cliente, Pedido, DetallePedido
from app import db
import bcrypt
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)
csrf = CSRFProtect()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    gelatinas = Gelatina.query.all()
    return render_template('index.html', gelatinas=gelatinas)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = Usuario.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password, user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    gelatinas = Gelatina.query.all()
    stocks = Stock.query.all()
    
    # Convertir objetos Gelatina a diccionarios
    gelatinas_data = [
        {
            'id_gelatina': gelatina.id_gelatina,
            'nombre': gelatina.nombre,
            'id_categoria': gelatina.id_categoria,
            'precio': float(gelatina.precio),
            'descripcion': gelatina.descripcion
        } for gelatina in gelatinas
    ]
    
    # Convertir objetos Stock a diccionarios
    stocks_data = [
        {
            'id_stock': stock.id_stock,
            'id_gelatina': stock.id_gelatina,
            'cantidad': stock.cantidad,
            'fecha_actualizacion': stock.fecha_actualizacion.isoformat() if stock.fecha_actualizacion else None
        } for stock in stocks
    ]
    
    return render_template('dashboard.html', gelatinas=gelatinas_data, stocks=stocks_data)

@bp.route('/gelatinas', methods=['GET', 'POST'])
@login_required
def gelatinas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_categoria = request.form['id_categoria']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        imagen = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                imagen = filename
        gelatina = Gelatina(nombre=nombre, id_categoria=id_categoria, precio=precio, descripcion=descripcion, imagen=imagen)
        db.session.add(gelatina)
        db.session.commit()
        stock = Stock(id_gelatina=gelatina.id_gelatina, cantidad=0)
        db.session.add(stock)
        db.session.commit()
        flash('Gelatina agregada con éxito', 'success')
        return redirect(url_for('main.gelatinas'))
    gelatinas = Gelatina.query.all()
    categorias = Categoria.query.all()
    return render_template('gelatinas.html', gelatinas=gelatinas, categorias=categorias)

@bp.route('/gelatinas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_gelatina(id):
    gelatina = Gelatina.query.get_or_404(id)
    if request.method == 'POST':
        gelatina.nombre = request.form['nombre']
        gelatina.id_categoria = request.form['id_categoria']
        gelatina.precio = request.form['precio']
        gelatina.descripcion = request.form['descripcion']
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                gelatina.imagen = filename
        db.session.commit()
        flash('Gelatina actualizada con éxito', 'success')
        return redirect(url_for('main.gelatinas'))
    categorias = Categoria.query.all()
    return render_template('gelatinas_editar.html', gelatina=gelatina, categorias=categorias)

@bp.route('/gelatinas/eliminar/<int:id>', methods=['GET'])
@login_required
def eliminar_gelatina(id):
    gelatina = Gelatina.query.get_or_404(id)
    # Eliminar registros relacionados en stock y detalles_pedido
    Stock.query.filter_by(id_gelatina=id).delete()
    DetallePedido.query.filter_by(id_gelatina=id).delete()
    db.session.delete(gelatina)
    db.session.commit()
    flash('Gelatina eliminada con éxito', 'success')
    return redirect(url_for('main.gelatinas'))

@bp.route('/categorias', methods=['GET', 'POST'])
@login_required
def categorias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría agregada con éxito')
        return redirect(url_for('main.categorias'))
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@bp.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    if request.method == 'POST':
        id_gelatina = request.form['id_gelatina']
        cantidad = request.form['cantidad']
        stock = Stock.query.filter_by(id_gelatina=id_gelatina).first()
        if stock:
            stock.cantidad = cantidad
            stock.fecha_actualizacion = datetime.utcnow()
        else:
            stock = Stock(id_gelatina=id_gelatina, cantidad=cantidad)
            db.session.add(stock)
        db.session.commit()
        flash('Stock actualizado con éxito')
        return redirect(url_for('main.stock'))
    stocks = Stock.query.all()
    gelatinas = Gelatina.query.all()
    return render_template('stock.html', stocks=stocks, gelatinas=gelatinas)

@bp.route('/pedidos')
@login_required
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

@bp.route('/pedido', methods=['GET', 'POST'])
def pedido():
    if request.method == 'POST':
        try:
            cliente = Cliente(
                nombre=request.form['nombre'],
                email=request.form['email'],
                telefono=request.form['telefono'],
                direccion=request.form['direccion']
            )
            db.session.add(cliente)
            db.session.flush()

            total = 0
            pedido = Pedido(id_cliente=cliente.id_cliente, total=0)
            db.session.add(pedido)
            db.session.flush()

            gelatinas = request.form.getlist('gelatinas[]')
            cantidades = request.form.getlist('cantidades[]')
            for id_gelatina, cantidad in zip(gelatinas, cantidades):
                cantidad = int(cantidad)
                gelatina = Gelatina.query.get(id_gelatina)
                if not gelatina:
                    raise Exception("Gelatina no encontrada")
                stock = Stock.query.filter_by(id_gelatina=id_gelatina).first()
                if not stock or stock.cantidad < cantidad:
                    raise Exception(f"Stock insuficiente para {gelatina.nombre}")
                subtotal = gelatina.precio * cantidad
                total += subtotal
                detalle = DetallePedido(
                    id_pedido=pedido.id_pedido,
                    id_gelatina=id_gelatina,
                    cantidad=cantidad,
                    precio_unitario=gelatina.precio,
                    subtotal=subtotal
                )
                db.session.add(detalle)
                stock.cantidad -= cantidad
                stock.fecha_actualizacion = datetime.utcnow()

            pedido.total = total
            db.session.commit()
            return render_template('pedido.html', mensaje="Pedido registrado con éxito", gelatinas=Gelatina.query.all())
        except Exception as e:
            db.session.rollback()
            return render_template('pedido.html', error=str(e), gelatinas=Gelatina.query.all())
    gelatinas = Gelatina.query.all()
    return render_template('pedido.html', gelatinas=gelatinas)