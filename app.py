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

# LISTAR servicios (Read)
@app.route('/servicios')
def listar_reparaciones_servicios():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT servicios.idservicios, servicios.Descripcion,
                          servicios.fecha_ingreso, servicios.fecha_salida,
                          servicios.costo, servicios.estado,
                          motos.marca, motos.modelo, motos.patente, motos.idmotos
                   FROM servicios
                   JOIN motos ON servicios.idmotos = motos.idmotos""")
    reparaciones = cur.fetchall()
    cur.close()
    return render_template('servicios.html', reparaciones=reparaciones)

# ALTA servicio (Create)
@app.route('/servicios/nueva', methods=['GET', 'POST'])
def nuevo_servicio():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idmotos = request.form['idmotos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""INSERT INTO servicios (idmotos, Descripcion, fecha_ingreso,
                       fecha_salida, costo, estado)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (idmotos, descripcion, fecha_ingreso, fecha_salida, costo, estado))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones_servicios'))

    cur.execute("""SELECT motos.idmotos, motos.marca, motos.modelo, motos.patente
                   FROM motos""")
    motos = cur.fetchall()
    cur.close()
    return render_template('form_servicio.html', reparacion=None, motos=motos)

# MODIFICACIÓN servicio (Update)
@app.route('/servicios/editar/<int:id_reparacion>', methods=['GET', 'POST'])
def editar_servicio(id_reparacion):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idmotos = request.form['idmotos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""UPDATE servicios SET idmotos=%s, Descripcion=%s,
                       fecha_ingreso=%s, fecha_salida=%s, costo=%s, estado=%s
                       WHERE idservicios=%s""",
                    (idmotos, descripcion, fecha_ingreso, fecha_salida, costo,
                     estado, id_reparacion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones_servicios'))

    cur.execute("SELECT * FROM servicios WHERE idservicios=%s", (id_reparacion,))
    reparacion = cur.fetchone()

    cur.execute("SELECT idmotos, marca, modelo, patente FROM motos")
    motos = cur.fetchall()
    cur.close()
    return render_template('form_servicio.html', reparacion=reparacion, motos=motos)

# BAJA servicio (Delete)
@app.route('/servicios/eliminar/<int:id_reparacion>')
def eliminar_servicio(id_reparacion):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM servicios WHERE idservicios=%s", (id_reparacion,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_reparaciones_servicios'))

# LISTAR mecánicos (Read)
@app.route('/mecanicos')
def listar_mecanicos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mecanicos")
    mecanicos = cur.fetchall()
    cur.close()
    return render_template('mecanicos.html', mecanicos=mecanicos)

# ALTA mecánico (Create)
@app.route('/mecanicos/nuevo', methods=['GET', 'POST'])
def nuevo_mecanico():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        documento = request.form['documento'].strip()
        telefono = request.form['telefono'].strip()
        direccion = request.form['direccion'].strip()

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO mecanicos (nombre, apellido, documento, telefono, direccion)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (nombre, apellido, documento, telefono, direccion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_mecanicos'))

    return render_template('form_mecanico.html', mecanico=None)

# MODIFICACIÓN mecánico (Update)
@app.route('/mecanicos/editar/<int:id_mecanico>', methods=['GET', 'POST'])
def editar_mecanico(id_mecanico):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        documento = request.form['documento'].strip()
        telefono = request.form['telefono'].strip()
        direccion = request.form['direccion'].strip()

        cur.execute("""UPDATE mecanicos SET nombre=%s, apellido=%s, documento=%s,
                       telefono=%s, direccion=%s WHERE idmecanicos=%s""",
                    (nombre, apellido, documento, telefono, direccion, id_mecanico))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_mecanicos'))

    cur.execute("SELECT * FROM mecanicos WHERE idmecanicos=%s", (id_mecanico,))
    mecanico = cur.fetchone()
    cur.close()
    return render_template('form_mecanico.html', mecanico=mecanico)

# BAJA mecánico (Delete)
@app.route('/mecanicos/eliminar/<int:id_mecanico>')
def eliminar_mecanico(id_mecanico):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mecanicos WHERE idmecanicos=%s", (id_mecanico,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_mecanicos'))

# HISTORIAL de una moto (todas sus reparaciones)
@app.route('/motos/historial/<int:id_moto>')
def historial_moto(id_moto):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM motos WHERE idmotos=%s", (id_moto,))
    moto = cur.fetchone()

    cur.execute("""SELECT * FROM servicios
                   WHERE idmotos=%s ORDER BY fecha_ingreso DESC""", (id_moto,))
    reparaciones = cur.fetchall()
    cur.close()

    return render_template('historial_moto.html', moto=moto, reparaciones=reparaciones)

if __name__ == '__main__':
    app.run(debug=True)