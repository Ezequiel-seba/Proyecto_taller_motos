from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import config
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(config)
mysql = MySQL(app)
bcrypt = Bcrypt(app)
from functools import wraps
UPLOAD_FOLDER = 'static/uploads/motos'
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extension_valida(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'correo' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada

# LISTAR (Read)
@app.route('/clientes')
@login_requerido
def listar_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('clientes.html', clientes=clientes)

# ALTA (Create)
@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_requerido
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
@login_requerido
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
@login_requerido
def eliminar_cliente(id_cliente):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clientes WHERE idclientes=%s", (id_cliente,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_clientes'))

# LISTAR motos (Read)
@app.route('/motos')
@login_requerido
def listar_motos():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT motos.idmotos, motos.marca, motos.modelo, motos.patente,
                          motos.ano, clientes.nombre, clientes.apellido, motos.foto
                   FROM motos
                   JOIN clientes ON motos.idclientes = clientes.idclientes""")
    motos = cur.fetchall()
    cur.close()
    return render_template('motos.html', motos=motos)

# ALTA moto (Create)
@app.route('/motos/nueva', methods=['GET', 'POST'])
@login_requerido
def nueva_moto():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idclientes = request.form['idclientes']
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        patente = request.form['patente'].strip()
        ano = request.form['ano']

        nombre_foto = None
        archivo = request.files.get('foto')
        if archivo and archivo.filename != '' and extension_valida(archivo.filename):
            nombre_foto = secure_filename(f"{patente}_{archivo.filename}")
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto))

        cur.execute("""INSERT INTO motos (idclientes, marca, modelo, patente, ano, foto)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (idclientes, marca, modelo, patente, ano, nombre_foto))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_motos'))

    cur.execute("SELECT idclientes, nombre, apellido FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('form_moto.html', moto=None, clientes=clientes)

# MODIFICACIÓN moto (Update)
@app.route('/motos/editar/<int:id_moto>', methods=['GET', 'POST'])
@login_requerido
def editar_moto(id_moto):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        idclientes = request.form['idclientes']
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        patente = request.form['patente'].strip()
        ano = request.form['ano']

        cur.execute("SELECT foto FROM motos WHERE idmotos=%s", (id_moto,))
        foto_actual = cur.fetchone()[0]
        nombre_foto = foto_actual

        archivo = request.files.get('foto')
        if archivo and archivo.filename != '' and extension_valida(archivo.filename):
            nombre_foto = secure_filename(f"{patente}_{archivo.filename}")
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto))

        cur.execute("""UPDATE motos SET idclientes=%s, marca=%s, modelo=%s,
                       patente=%s, ano=%s, foto=%s WHERE idmotos=%s""",
                    (idclientes, marca, modelo, patente, ano, nombre_foto, id_moto))
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
@login_requerido
def eliminar_moto(id_moto):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM motos WHERE idmotos=%s", (id_moto,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_motos'))

# LISTAR servicios (Read)
@app.route('/servicios')
@login_requerido
def listar_reparaciones_servicios():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT servicios.idservicios, servicios.Descripcion,
                          servicios.fecha_ingreso, servicios.fecha_salida,
                          servicios.costo, servicios.estado,
                          motos.marca, motos.modelo, motos.patente, motos.idmotos,
                          mecanicos.nombre, mecanicos.apellido
                   FROM servicios
                   JOIN motos ON servicios.idmotos = motos.idmotos
                   JOIN mecanicos ON servicios.idmecanicos = mecanicos.idmecanicos""")
    reparaciones = cur.fetchall()
    cur.close()
    return render_template('servicios.html', reparaciones=reparaciones)

# ALTA servicio (Create)
@app.route('/servicios/nueva', methods=['GET', 'POST'])
@login_requerido
def nuevo_servicio():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        idmotos = request.form['idmotos']
        idmecanicos = request.form['idmecanicos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""INSERT INTO servicios (idmotos, idmecanicos, Descripcion,
                       fecha_ingreso, fecha_salida, costo, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (idmotos, idmecanicos, descripcion, fecha_ingreso, fecha_salida, costo, estado))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones_servicios'))

    cur.execute("SELECT idmotos, marca, modelo, patente FROM motos")
    motos = cur.fetchall()
    cur.execute("SELECT idmecanicos, nombre, apellido FROM mecanicos")
    mecanicos = cur.fetchall()
    cur.close()
    return render_template('form_servicio.html', reparacion=None, motos=motos, mecanicos=mecanicos)

# MODIFICACIÓN servicio (Update)
@app.route('/servicios/editar/<int:id_reparacion>', methods=['GET', 'POST'])
@login_requerido
def editar_servicio(id_reparacion):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        idmotos = request.form['idmotos']
        idmecanicos = request.form['idmecanicos']
        descripcion = request.form['descripcion'].strip()
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] or None
        costo = request.form['costo']
        estado = request.form['estado']

        cur.execute("""UPDATE servicios SET idmotos=%s, idmecanicos=%s, Descripcion=%s,
                       fecha_ingreso=%s, fecha_salida=%s, costo=%s, estado=%s
                       WHERE idservicios=%s""",
                    (idmotos, idmecanicos, descripcion, fecha_ingreso, fecha_salida, costo,
                     estado, id_reparacion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_reparaciones_servicios'))

    cur.execute("SELECT * FROM servicios WHERE idservicios=%s", (id_reparacion,))
    reparacion = cur.fetchone()
    cur.execute("SELECT idmotos, marca, modelo, patente FROM motos")
    motos = cur.fetchall()
    cur.execute("SELECT idmecanicos, nombre, apellido FROM mecanicos")
    mecanicos = cur.fetchall()
    cur.close()
    return render_template('form_servicio.html', reparacion=reparacion, motos=motos, mecanicos=mecanicos)

# BAJA servicio (Delete)
@app.route('/servicios/eliminar/<int:id_reparacion>')
@login_requerido
def eliminar_servicio(id_reparacion):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM servicios WHERE idservicios=%s", (id_reparacion,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_reparaciones_servicios'))

# LISTAR mecánicos (Read)
@app.route('/mecanicos')
@login_requerido
def listar_mecanicos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mecanicos")
    mecanicos = cur.fetchall()
    cur.close()
    return render_template('mecanicos.html', mecanicos=mecanicos)

# ALTA mecánico (Create)
@app.route('/mecanicos/nuevo', methods=['GET', 'POST'])
@login_requerido
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
@login_requerido
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
@login_requerido
def eliminar_mecanico(id_mecanico):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mecanicos WHERE idmecanicos=%s", (id_mecanico,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_mecanicos'))

# HISTORIAL de una moto (todas sus reparaciones)
@app.route('/motos/historial/<int:id_moto>')
@login_requerido
def historial_moto(id_moto):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM motos WHERE idmotos=%s", (id_moto,))
    moto = cur.fetchone()

    cur.execute("""SELECT * FROM servicios
                   WHERE idmotos=%s ORDER BY fecha_ingreso DESC""", (id_moto,))
    reparaciones = cur.fetchall()
    cur.close()

    return render_template('historial_moto.html', moto=moto, reparaciones=reparaciones)

@app.route('/')
def index():
    return render_template('index.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
        usuario_db = cur.fetchone()
        cur.close()

        if usuario_db and bcrypt.check_password_hash(usuario_db[2], contrasena):
            session['correo'] = usuario_db[1]
            return redirect(url_for('listar_clientes'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos.")

    return render_template('login.html', error=None)

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('correo', None)
    return redirect(url_for('index'))

# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena']
        confirmar = request.form['confirmar']

        if contrasena != confirmar:
            return render_template('registro.html', error="Las contraseñas no coinciden.")

        cur = mysql.connection.cursor()
        cur.execute("SELECT idusuarios FROM usuarios WHERE correo=%s", (correo,))
        if cur.fetchone():
            cur.close()
            return render_template('registro.html', error="Ese correo ya está registrado.")

        hash_contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
        cur.execute("INSERT INTO usuarios (correo, contrasena) VALUES (%s, %s)",
                    (correo, hash_contrasena))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template('registro.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)