from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/celulares1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar los modelos después de inicializar db
from models import Marca, Equipo, Celulares, Fabricantes, Caracteristica, Stock, Accesorios, Proveedor

@app.route("/")
def index():
    celulares = Celulares.query.all()
    return render_template('index.html', celulares=celulares)

@app.route("/celulares_list.html", methods=['POST', 'GET'])
def celulares_list():
    if request.method == 'POST':
        marca = request.form['marca']
        equipo = request.form['equipo']
        celular_nuevo = Celulares(marca=marca, equipo=equipo)
        db.session.add(celular_nuevo)
        db.session.commit()
        return redirect(url_for('celulares_list'))
    
    celulares = Celulares.query.all()
    return render_template('celulares_list.html', celulares=celulares)

@app.route("/equipo_list.html")
def equipo_list():
    equipos = Equipo.query.all()
    return render_template('equipo_list.html', equipos=equipos)

@app.route("/marca_list.html", methods=['POST', 'GET'])
def marca_list():
    marcas = Marca.query.all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('marca_list'))
    return render_template('marca_list.html', marcas=marcas)

@app.route("/marca/<int:id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marca_list'))
    return render_template("marca_edit.html", marca=marca)

@app.route('/equipos', methods=['GET', 'POST'])
def equipos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        nuevo_equipo = Equipo(nombre=nombre)
        db.session.add(nuevo_equipo)
        db.session.commit()
        return redirect(url_for('equipos'))
    equipos = Equipo.query.all()
    return render_template('equipo_list.html', equipos=equipos)

@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    if request.method == 'POST':
        equipo.nombre = request.form.get('nombre')
        db.session.commit()
        return redirect(url_for('equipos'))
    return render_template('editar_equipo.html', equipo=equipo)

@app.route('/equipos/eliminar/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for('equipos'))

@app.route('/crear_marca', methods=['POST'])
def crear_marca():
    nombre_marca = request.form['nombre']
    nueva_marca = Marca(nombre=nombre_marca)
    db.session.add(nueva_marca)
    db.session.commit()
    return redirect(url_for('marca_list'))

# Rutas para Características
@app.route('/caracteristicas_list.html', methods=['GET', 'POST'])
def caracteristicas_list():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        nueva_caracteristica = Caracteristica(tipo=tipo, descripcion=descripcion)
        db.session.add(nueva_caracteristica)
        db.session.commit()
        return redirect(url_for('caracteristicas_list'))
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas_list.html', caracteristicas=caracteristicas)

@app.route('/caracteristicas/editar/<int:id>', methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    if request.method == 'POST':
        caracteristica.tipo = request.form.get('tipo')
        caracteristica.descripcion = request.form.get('descripcion')
        db.session.commit()
        return redirect(url_for('caracteristicas_list'))
    return render_template('caracteristicas_edit.html', caracteristica=caracteristica)

@app.route('/caracteristicas/eliminar/<int:id>', methods=['POST'])
def eliminar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return redirect(url_for('caracteristicas_list'))

# Rutas para Stock
@app.route('/stock_list.html', methods=['GET', 'POST'])
def stock_list():
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        ubicacion = request.form['ubicacion']
        nuevo_stock = Stock(cantidad=cantidad, ubicacion=ubicacion)
        db.session.add(nuevo_stock)
        db.session.commit()
        return redirect(url_for('stock_list'))
    stock = Stock.query.all()
    return render_template('stock_list.html', stock=stock)

@app.route('/stock/editar/<int:id>', methods=['GET', 'POST'])
def editar_stock(id):
    stock = Stock.query.get_or_404(id)
    if request.method == 'POST':
        stock.cantidad = request.form.get('cantidad')
        stock.ubicacion = request.form.get('ubicacion')
        db.session.commit()
        return redirect(url_for('stock_list'))
    return render_template('stock_edit.html', stock=stock)

@app.route('/stock/eliminar/<int:id>', methods=['POST'])
def eliminar_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(url_for('stock_list'))

# Rutas para Proveedores
@app.route('/proveedores_list.html', methods=['GET', 'POST'])
def proveedores_list():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        nuevo_proveedor = Proveedor(nombre=nombre, contacto=contacto)
        db.session.add(nuevo_proveedor)
        db.session.commit()
        return redirect(url_for('proveedores_list'))
    proveedores = Proveedor.query.all()
    return render_template('proveedores_list.html', proveedores=proveedores)

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        proveedor.nombre = request.form.get('nombre')
        proveedor.contacto = request.form.get('contacto')
        db.session.commit()
        return redirect(url_for('proveedores_list'))
    return render_template('proveedor_edit.html', proveedor=proveedor)

@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    return redirect(url_for('proveedores_list'))

# Rutas para Fabricantes
@app.route('/fabricantes_list.html', methods=['GET', 'POST'])
def fabricantes_list():
    if request.method == 'POST':
        nombre = request.form['nombre']
        pais = request.form['pais']
        nuevo_fabricante = Fabricantes(nombre=nombre, pais=pais)
        db.session.add(nuevo_fabricante)
        db.session.commit()
        return redirect(url_for('fabricantes_list'))
    fabricantes = Fabricantes.query.all()
    return render_template('fabricantes_list.html', fabricantes=fabricantes)

@app.route('/fabricantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_fabricante(id):
    fabricante = Fabricantes.query.get_or_404(id)
    if request.method == 'POST':
        fabricante.nombre = request.form.get('nombre')
        fabricante.pais = request.form.get('pais')
        db.session.commit()
        return redirect(url_for('fabricantes_list'))
    return render_template('fabricante_edit.html', fabricante=fabricante)

@app.route('/fabricantes/eliminar/<int:id>', methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricantes.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    return redirect(url_for('fabricantes_list'))

# Rutas para Accesorios
@app.route('/accesorios', methods=['GET', 'POST'])
def accesorios_list():
    if request.method == 'POST':
        tipo = request.form['tipo']
        compatible_con = request.form['compatible_con']
        nuevo_accesorio = Accesorios(tipo=tipo, compatible_con=compatible_con)
        db.session.add(nuevo_accesorio)
        db.session.commit()
        return redirect(url_for('accesorios_list'))
    accesorios = Accesorios.query.all()
    return render_template('accesorios_list.html', accesorios=accesorios)

@app.route('/accesorios/editar/<int:id>', methods=['GET', 'POST'])
def editar_accesorio(id):
    accesorio = Accesorios.query.get_or_404(id)
    if request.method == 'POST':
        accesorio.tipo = request.form.get('tipo')
        accesorio.compatible_con = request.form.get('compatible_con')
        db.session.commit()
        return redirect(url_for('accesorios_list'))
    return render_template('accesorios_edit.html', accesorio=accesorio)

@app.route('/accesorios/eliminar/<int:id>', methods=['POST'])
def eliminar_accesorio(id):
    accesorio = Accesorios.query.get_or_404(id)
    db.session.delete(accesorio)
    db.session.commit()
    return redirect(url_for('accesorios_list'))

if __name__ == "__main__":
    app.run(debug=True)
