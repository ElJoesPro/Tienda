from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_wtf.csrf import CSRFProtect
import psycopg2 
from psycopg2 import sql
from flask_login import LoginManager,login_user, logout_user, login_required, current_user

from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario
from .models.ModeloCompra import ModeloCompra

from .models.entities.Usuario import Usuario
from .models.entities.Libro import Libro
from .models.entities.Compra import Compra

from .const import *

app = Flask(__name__)

csrf = CSRFProtect()

# Configura los detalles de la conexión a la base de datos
db_config = {
    'host': 'trumpet.db.elephantsql.com',
    'dbname': 'feoyzkea',
    'user': 'feoyzkea',
    'password': 'VQhRV53_-iD9-PdhHtOcKtpG5fQfOpQk',
    'port': '5432'  # Puerto predeterminado de PostgreSQL
}


# Establece la conexión a la base de datos
connection = psycopg2.connect(**db_config)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    print(id)
    return ModeloUsuario.obtener_por_id(connection,id)


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos= ModeloLibro.listar_libros_vendidos(connection)
                data = {
                    'titulo':'Libros Vendidos',
                    'libros_vendidos':libros_vendidos
                }
                return render_template('index.html',data=data)
            except Exception as ex:
                return render_template('errores/error.html',mensaje = format(ex))   
        else:
            try:
                compras= ModeloCompra.listar_compras_usuario(connection, current_user)
                data = {
                    'titulo':'Mis compras',
                    'compras':compras
                }
                return render_template('index.html',data=data)
            except Exception as ex:
                    return render_template('errores/error.html',mensaje = format(ex))
        
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    #CSRF (Cross-site Request Forgery): Solicitud de falsificación entre sitios
    if(request.method == 'POST'):
        #print(request.form['usuario'])
        #print(request.form['password'])
        usuario = Usuario(None, request.form['usuario'],request.form['password'],None)
        usuario_logueado = ModeloUsuario.login(connection,usuario)
        if usuario_logueado != None:
            login_user(usuario_logueado)
            flash(MENSAJE_BIENVENIDA, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS, 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

"""
@app.route('/contra/<password>')
def contra(password):
    hash = generate_password_hash(password)
    valor = check_password_hash(hash, password)
    return "{0},{1}".format(hash,valor)
"""


# Ruta de prueba para verificar la conexión
@app.route('/libros')
@login_required
def listar_libros():
    try:
        libros = ModeloLibro.listar_libros(connection)
        data = {
            'titulo':'Listado de libros',
            'libros':libros
        }
        return render_template('listado_libros.html', data = data)
    except Exception as ex:
        return render_template('errores/error.html',mensaje = format(ex))

def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def pagina_no_autorizada(error):
    return redirect(url_for('login'))

@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()
    data={}
    try:
        libro=Libro(data_request['isbn'],None,None,None,None)
        compra = Compra(None, libro, current_user)
        data['exito'] = ModeloCompra.registrar_compra(connection, compra)
    except Exception as ex:
        data['mensaje']=format(ex)
        data['exito']=False
    return jsonify(data)

def create_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    #print(app.config['PORT'])
    app.register_error_handler(401, pagina_no_autorizada)
    app.register_error_handler(404, pagina_no_encontrada)
    return app.run(port=app.config['PORT'])
