from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config

app = Flask(__name__)
app.config.from_object(config)
mysql = MySQL(app)

# LISTAR (Read)
@app.route('/clientes')
def listar_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('clientes.html', clientes=clientes)

# ALTA (Create)
@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        telefono = request.form['telefono'].strip()
        direccion = request.form['direccion'].strip()

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO clientes (nombre, apellido, telefono, direccion)
                       VALUES (%s, %s, %s, %s)""",
                    (nombre, apellido, telefono, direccion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_clientes'))

    return render_template('form_cliente.html', cliente=None)

# MODIFICACIÓN (Update)
@app.route('/clientes/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        telefono = request.form['telefono'].strip()
        direccion = request.form['direccion'].strip()

        cur.execute("""UPDATE clientes SET nombre=%s, apellido=%s,
                       telefono=%s, direccion=%s WHERE idclientes=%s""",
                    (nombre, apellido, telefono, direccion, id_cliente))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_clientes'))

    cur.execute("SELECT * FROM clientes WHERE idclientes=%s", (id_cliente,))
    cliente = cur.fetchone()
    cur.close()
    return render_template('form_cliente.html', cliente=cliente)

# BAJA (Delete)
@app.route('/clientes/eliminar/<int:id_cliente>')
def eliminar_cliente(id_cliente):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clientes WHERE idclientes=%s", (id_cliente,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_clientes'))

# LISTAR motos (Read)
@app.route('/motos')
def listar_motos():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT motos.idmotos, motos.marca, motos.modelo, motos.patente,
                          motos.ano, clientes.nombre, clientes.apellido, motos.idclientes
                   FROM motos
                   JOIN clientes ON motos.idclientes = clientes.idclientes""")
    motos = cur.fetchall()
    cur.close()
    return render_template('motos.html', motos=motos)

# ALTA moto (Create)
@app.route('/motos/nueva', methods=['GET', 'POST'])
def nueva_moto():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idclientes = request.form['idclientes']
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        patente = request.form['patente'].strip()
        ano = request.form['ano']

        cur.execute("""INSERT INTO motos (idclientes, marca, modelo, patente, ano)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (idclientes, marca, modelo, patente, ano))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_motos'))

    cur.execute("SELECT idclientes, nombre, apellido FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('form_moto.html', moto=None, clientes=clientes)

# MODIFICACIÓN moto (Update)
@app.route('/motos/editar/<int:id_moto>', methods=['GET', 'POST'])
def editar_moto(id_moto):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idclientes = request.form['idclientes']
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        patente = request.form['patente'].strip()
        ano = request.form['ano']

        cur.execute("""UPDATE motos SET idclientes=%s, marca=%s, modelo=%s,
                       patente=%s, ano=%s WHERE idmotos=%s""",
                    (idclientes, marca, modelo, patente, ano, id_moto))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_motos'))

    cur.execute("SELECT * FROM motos WHERE idmotos=%s", (id_moto,))
    moto = cur.fetchone()

    cur.execute("SELECT idclientes, nombre, apellido FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('form_moto.html', moto=moto, clientes=clientes)

# BAJA moto (Delete)
@app.route('/motos/eliminar/<int:id_moto>')
def eliminar_moto(id_moto):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM motos WHERE idmotos=%s", (id_moto,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_motos'))

# LISTAR reparaciones (Read)
@app.route('/reparaciones')
def listar_reparaciones():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT reparaciones.idreparacion, reparaciones.Descripcion,
                          reparaciones.fecha_ingreso, reparaciones.fecha_salida,
                          reparaciones.costo, reparaciones.estado,
                          motos.marca, motos.modelo, motos.patente, motos.idmotos
                   FROM reparaciones
                   JOIN motos ON reparaciones.idmotos = motos.idmotos""")
    reparaciones = cur.fetchall()
    cur.close()
    return render_template('reparaciones.html', reparaciones=reparaciones)

# ALTA reparación (Create)
@app.route('/reparaciones/nueva', methods=['GET', 'POST'])
def nueva_reparacion():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idmotos = request.form['idmotos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""INSERT INTO reparaciones (idmotos, Descripcion, fecha_ingreso,
                       fecha_salida, costo, estado)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (idmotos, descripcion, fecha_ingreso, fecha_salida, costo, estado))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones'))

    # Para el formulario, necesitamos la lista de motos existentes
    cur.execute("""SELECT motos.idmotos, motos.marca, motos.modelo, motos.patente
                   FROM motos""")
    motos = cur.fetchall()
    cur.close()
    return render_template('form_reparacion.html', reparacion=None, motos=motos)

# MODIFICACIÓN reparación (Update)
@app.route('/reparaciones/editar/<int:id_reparacion>', methods=['GET', 'POST'])
def editar_reparacion(id_reparacion):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idmotos = request.form['idmotos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""UPDATE reparaciones SET idmotos=%s, Descripcion=%s,
                       fecha_ingreso=%s, fecha_salida=%s, costo=%s, estado=%s
                       WHERE idreparacion=%s""",
                    (idmotos, descripcion, fecha_ingreso, fecha_salida, costo,
                     estado, id_reparacion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones'))

    cur.execute("SELECT * FROM reparaciones WHERE idreparacion=%s", (id_reparacion,))
    reparacion = cur.fetchone()

    cur.execute("SELECT idmotos, marca, modelo, patente FROM motos")
    motos = cur.fetchall()
    cur.close()
    return render_template('form_reparacion.html', reparacion=reparacion, motos=motos)

# BAJA reparación (Delete)
@app.route('/reparaciones/eliminar/<int:id_reparacion>')
def eliminar_reparacion(id_reparacion):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reparaciones WHERE idreparacion=%s", (id_reparacion,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_reparaciones'))

if __name__ == '__main__':
    app.run(debug=True)