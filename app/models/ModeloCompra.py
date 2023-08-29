from .entities.Compra import Compra
from .entities.Libro import Libro

class ModeloCompra():
    @classmethod
    def registrar_compra(self,connection,compra):
        try:
            cursor = connection.cursor()
            query = """INSERT INTO compra (uuid, libro_isbn, usuario_id) 
                    VALUES (uuid_generate_v4(), '{0}','{1}')""".format(compra.libro.isbn,compra.usuario.id)
            #print(compra.libro.isbn,compra.usuario.id)
            cursor.execute(query)
            connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def listar_compras_usuario(self, connection, usuario):
        try:
            cursor = connection.cursor()
            query = """SELECT COM.fecha, LIB.isbn, LIB.titulo, LIB.precio 
                    FROM compra COM JOIN libro LIB on COM.libro_isbn = LIB.isbn
                    WHERE COM.usuario_id = {0}""".format(usuario.id)
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            compras = []
            for row in data:
                lib = Libro(row[1],row[2],None,None,row[3])
                com = Compra(None, lib, usuario, row[0])
                compras.append(com)
            return compras
        except Exception as ex:
            raise Exception(ex)
