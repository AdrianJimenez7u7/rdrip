from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from modelo.Dao import Usuario, db, Producto, Departamento, MetodoPago, Carrito
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta

from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/empresa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#inicio de metodos
#metodos de sesion
@app.route('/')
def inicio():
    return redirect(url_for('menuPrincipal'))
#gestion de usuarios
app.secret_key='Cl4v3'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"


@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

# Urls definidas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))# nombre de la vista o 

#metodos de usuarios
@app.route('/login', methods=['POST','get'])
def login():
    if request.method == 'POST':
        #recibimos el formulario
        user = Usuario()
        correo = request.form['correo']
        contra = request.form['contrasena']
        #validamos
        user=user.validar(correo, contra)
        if user != None:
            login_user(user)
            return redirect(url_for('menuPrincipal'))
    return render_template('login.html',  is_login_page=True)

@app.route('/registroUsuarios', methods=['POST','GET'])
def RegistroUsuarios():
    if request.method =='POST':
        user = Usuario()
        user.username = request.form['nombre']
        user.email = request.form['correo']
        user.passw = request.form['contraseña']
        user.role = "Cliente"
        user.agregar() #no asignamos foto por que aun no se ve en clases
        return redirect(url_for('login'))
    return render_template('RegistrarUsuario.html', is_register_page =True)

@login_required
@app.route('/usuarios')
def mostrarUsuarios():
    usuario = Usuario()
    usuario = usuario.consultaGeneral()
    return render_template('usuarios.html', usuario = usuario)



@login_required
@app.route('/actualizarUsuario/<int:idUsuario>', methods=['POST','GET'])
def actualizarUsuario(idUsuario):
    if (current_user.idUsuario == idUsuario or current_user.role == 'Administrador'):
        userA = Usuario()
        if request.method =='POST':
            username = request.form['nombre']
            email = request.form['correo']
            passw = request.form['contraseña']
            userA.idUsuario = idUsuario
            userA.username = username
            userA.email = email
            userA.passw = passw
            userA.actualizar()
            if(current_user.role == 'Administrador'):
                return redirect(url_for('mostrarUsuarios'))
            else:
                return redirect(url_for('menuPrincipal'))
        userA = userA.consultaIndividual(idUsuario)
        metodos_pago = MetodoPago().consultMetodosCliente(idUsuario)
        return render_template('actualizarUsuario.html', usuario = userA, meto = metodos_pago)
    else:
        return redirect(url_for('login'))
    
@app.route('/hacerAdmin/<int:idUsuario>', methods=['POST','GET'])
def hacerAdministrador(idUsuario):
    usera=Usuario().consultaIndividual(idUsuario)
    usera.tipo='Administrador'
    usera.actualizar()
    return redirect(url_for('mostrarUsuarios'))

@app.route('/hacerCliente/<int:idUsuario>')
def hacerCliente(idUsuario):
    user=Usuario()
    user=user.consultaIndividual(idUsuario)
    user.tipo='Cliente'
    user.actualizar()
    return redirect(url_for('mostrarUsuarios'))

@login_required
@app.route('/eliminarMetodo/<int:metodo>', methods=['post','get'])
def deleteMetodo(metodo):
    Metodop = MetodoPago()
    Metodop = Metodop.consultaIndividual(metodo)
    Metodop.eliminar()
    return redirect(url_for("actualizarUsuario"))

@login_required
@app.route('/registroPago', methods=['POST','GET'])
def RegistroPago():
    if request.method =='POST':
        metodo = MetodoPago()
        usuario = current_user.idUsuario
        metodo.idUsuario = usuario
        metodo.empresa = request.form['empresa']
        metodo.numero = int(request.form['numero'])
        metodo.tipo = request.form['tipo']
        metodo.agregar()
        return redirect(url_for('actualizarUsuario', idUsuario = current_user.idUsuario))
    return render_template('crearMetodoPago.html')

#metodos para departamento
@login_required
@app.route('/registroDepartamento', methods=['POST','GET'])
def RegistroDepartamento():
    if (current_user.is_authenticated or current_user.role == 'Administrador'):
        if request.method =='POST':
            departame = Departamento()
            departame.nombre = request.form['nombre']
            departame.estado = request.form['estado']
            departame.agregar()
            return redirect(url_for('mostrarDepartamentos'))
        return render_template('crearDepartamento.html')
    else: 
        return redirect(url_for('login'))


@login_required
@app.route('/departamentos')
def mostrarDepartamentos():
    if (current_user.is_authenticated or current_user.role == 'Administrador'):
        departamento = Departamento()
        departamento = departamento.consultaGeneral()
        return render_template('departamentos.html', departamento = departamento)
    else: 
        return redirect(url_for('login'))
    
@login_required
@app.route('/actualizarDepartamento/<int:idDepartamento>', methods=['POST','GET'])
def actualizarDepartamento(idDepartamento):
    if (current_user.is_authenticated or current_user.role == 'Administrador'):
        departame = Departamento().consultaIndividual(idDepartamento)
        if request.method =='POST':
            
            departame.idDepartamento = idDepartamento
            departame.nombre = request.form['nombre']
            departame.estado = request.form['estado']
            departame.actualizar()
            return redirect(url_for('mostrarDepartamentos'))
        return render_template('actualizarDepartamento.html', dep = departame)
    else: 
        return redirect(url_for('login'))
    
@login_required
@app.route('/eliminarDepartamento/<int:idDepartamento>', methods=['POST','GET'])
def eliminarDepartamento(idDepartamento):
    if (current_user.is_authenticated and current_user.role=='Administrador'):
        dep = Departamento()
        dep = dep.consultaIndividual(idDepartamento)
        productos =Producto().productosDepartamento(idDepartamento)
        for p in productos:
            p.eliminar()
        dep.eliminar()
        return redirect(url_for("mostrarDepartamentos"))
    else: 
        return redirect(url_for('login'))
#metodos para productos
@login_required
@app.route('/registroProducto', methods=['POST','GET'])
def registroProducto():
    if (current_user.role == 'Administrador'):
        deps = Departamento()
        deps = deps.consultaGeneral()
        if request.method =='POST':
            prod = Producto()
            prod.nombre = request.form['nombre']
            prod.precio = request.form['precio']
            prod.existencia = request.form['existencia']
            prod.idDepartamento = request.form['departamento']
            prod.foto = request.files['foto'].stream.read()
            prod.agregar()
            return redirect(url_for('mostrarProductos'))
        return render_template('registroProductos.html', deps = deps)
    else: 
        return redirect(url_for('login'))


@login_required
@app.route('/actualizarProducto/<int:idProducto>', methods=['post', 'get'])
def actProducto(idProducto):
    if (current_user.is_authenticated and current_user.role=='Administrador'):
        prodM = Producto()
        deps = Departamento().consultaGeneral()  # Directamente obtén la lista de departamentos

        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = request.form['precio']
            existencia = request.form['existencia']
            departamento = int(request.form['departamento'])  # Asegúrate de que sea un entero

            prodM.idProducto = idProducto
            prodM.nombre = nombre
            prodM.precio = precio
            prodM.existencia = existencia
            prodM.idDepartamento = departamento

            if 'foto' in request.files and request.files['foto']:
                foto = request.files['foto'].stream.read()
                prodM.foto = foto

            prodM.actualizar()
            return redirect(url_for('mostrarProductos'))

        prodM = prodM.consultaIndividual(idProducto)
        return render_template('actualizarProducto.html', producto=prodM, deps=deps)
    else: 
        return redirect(url_for('login'))

@login_required
@app.route('/eliminarProducto/<int:idProducto>', methods=['post','get'])
def deleteProducto(idProducto):
    if (current_user.is_authenticated and current_user.role=='Administrador'):
        productoE = Producto()
        productoE = productoE.consultaIndividual(idProducto)
        productoE.eliminar()
        return redirect(url_for("mostrarProductos"))
    else: 
        return redirect(url_for('login'))

@login_required
@app.route('/productos')
def mostrarProductos():
    if (current_user.is_authenticated and current_user.role=='Administrador'):
        producto = Producto()
        producto = producto.consultaGeneral()
        return render_template('productos.html', producto = producto)
    else: 
        return redirect(url_for("mostrarProductosCliente"))

@app.route('/productosCliente')
def mostrarProductosCliente():
    producto = Producto()
    producto = producto.consultaGeneral()
    deps = Departamento().consultaGeneral()
    return render_template('productosCliente.html', producto = producto, deps=deps)

@login_required
@app.route('/agregarCarrito/<int:idProducto>', methods=['post','get'])
def agregarProductoCarrito(idProducto):
    if (current_user.is_authenticated):
        carrito = Carrito()
        carrito.idProducto = idProducto
        carrito.idUsuario = current_user.idUsuario
        carrito.agregar()
        return redirect(url_for('carrito'))
    else: 
        return redirect(url_for('login'))

@login_required
@app.route('/Carrito', methods=['post','get'])
def carrito():
    if (current_user.is_authenticated):
        carrito = Carrito()
        productos = carrito.carritoCliente(current_user.idUsuario)
        metodo = MetodoPago().consultMetodosCliente(current_user.idUsuario)
        total = sum(p.producto.precio for p in productos)
        return render_template('carrito.html', producto=productos, total = total, metodo = metodo)
    else: 
        return redirect(url_for('login'))

@login_required
@app.route('/eliminarCarrito/<int:idCarrito>', methods=['post','get'])
def eliminarCarrito(idCarrito):
    carrito = Carrito()
    carrito = carrito.consultaIndividual(idCarrito)
    carrito.eliminar()
    return redirect(url_for('carrito'))

@app.route('/menuPrincipal')
def menuPrincipal():
    return render_template('menuPrincipal.html')


@app.route('/consultarImgProd/<int:idProd>')
def imgProd(idProd):
    prod=Producto()
    return prod.consultarImagen(idProd)

@login_required
@app.route('/carrito')
def mostrarCarrito():
    
    return render_template('carrito.html')


#fin de metodos
if __name__=='__main__':#python -m main
    db.init_app(app)
    app.run(debug=True) #hablilita el debug para modo depuracion activado, es para que sea sensible a cambios
