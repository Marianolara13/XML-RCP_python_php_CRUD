from xmlrpc.server import SimpleXMLRPCServer


def llenar():
    sql = "select * from datos"
    return sql


def insert():
    sql = "insert into datos(nombre, apellidoP, apellidoM) values (%s,%s,%s)"
    return sql


def eliminar():
    sql = "delete from datos where id = %s"
    return sql


def actualizar():
    sql = "update datos set nombre=%s, apellidoP=%s, apellidoM=%s where id=%s"
    return sql


server = SimpleXMLRPCServer(("localhost", 8001))
server.register_function(eliminar, "eliminar")
server.register_function(insert, "insert")
server.register_function(actualizar, "actualizar")
server.register_function(llenar, "llenar")
server.serve_forever()
