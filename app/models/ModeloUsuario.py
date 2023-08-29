from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario

class ModeloUsuario():

    @classmethod
    def login(self, connection, usuario):
        try:
            cursor = connection.cursor()
            sql="SELECT id, usuario, password FROM usuario WHERE usuario ='{0}'".format(usuario.usuario)
            cursor.execute(sql)
            data=cursor.fetchone()
            if data != None:
                coincide = Usuario.verificar_password('pbkdf2:sha256:600000$eBLv77JpJaLlHPrp$eb4fcc2a2bb204738f124a838b2f96005f72e0adfd70fbd82b8d9b300055583c',usuario.password)
                if coincide:
                    usuario_logueado = Usuario(data[0],data[1], None, None)
                    return usuario_logueado
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def obtener_por_id(self, connection, id):
        try:
            cursor = connection.cursor()
            sql="""SELECT USU.id, USU.usuario, TIP.id, TIP.nombre FROM usuario USU JOIN tipousuario TIP 
            ON USU.tipousuario_id = TIP.id WHERE USU.id ={0}""".format(id)
            cursor.execute(sql)
            data=cursor.fetchone()
            tipousuario = TipoUsuario(data[2],data[3])
            usuario_logueado = Usuario(data[0], data[1], None, tipousuario)
            return usuario_logueado
        except Exception as ex:
            raise Exception(ex)
        
