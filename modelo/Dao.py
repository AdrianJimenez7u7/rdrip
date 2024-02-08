from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Departamento(db.Model):
    __tablename__ = 'departamento'
    idDepartamento = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True)
    estado = Column(String)

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Departamento.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

# Tabla proveedor
class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    idProveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    correo = db.Column(db.String(30))
    direccion = db.Column(db.String(30))
    telefono = db.Column(db.Integer)

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Producto.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

class Producto(db.Model):
    __tablename__ = 'producto'
    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    precio = Column(Float)
    idDepartamento = Column(Integer, ForeignKey('departamento.idDepartamento'))
    departamento = relationship('Departamento', backref='productos', lazy='select')
    existencia = Column(Integer)
    foto = Column(LargeBinary)

    def consultarImagen(self, id):
        return Producto.query.get(id).foto

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Producto.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def productosDepartamento(self, idD):
        return Producto.query.filter_by(idDepartamento = idD).all()

class Carrito(db.Model):
    __tablename__ = 'carrito'
    idCarrito = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    idProducto = Column(Integer, ForeignKey('producto.idProducto'))
    producto = relationship('Producto', backref='carritos')
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    usuario = relationship('Usuario', backref='carritos')

    def consultarImagen(self, id):
        return Carrito.query.get(id).foto

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Carrito.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def carritoCliente(self, idC):
        return Carrito.query.filter_by(idUsuario = idC).all()

class MetodoPago(db.Model):
    __tablename__ = 'metodoPago'
    idMetodo = Column(Integer, primary_key=True)
    tipo = Column(String(30))
    empresa = Column(String(30))
    numero = Column(BigInteger, unique=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    usuario = relationship('Usuario', backref='metodosPago', lazy='select')


    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return MetodoPago.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultMetodosCliente(self, idC):
        return MetodoPago.query.filter_by(idUsuario = idC).all()


# Tabla usuarios
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    idUsuario = Column(Integer, primary_key=True)
    username = Column(String(30))
    email = Column(String(50), unique=True)
    passw = Column(String(30))
    foto = Column(LargeBinary)
    role = Column(String(20))

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Usuario.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def validar(self, email, contra):
        user = Usuario.query.filter(Usuario.email==email).first()
        if user!= None and user.passw == contra:
            return user
        return None
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

# Tabla pedido
