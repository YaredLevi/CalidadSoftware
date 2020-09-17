from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Clave secreta para extra protección
app.secret_key = 'lavidasimplemente'

# Conexió a la base de datos
app.config['MYSQL_HOST'] = 'server' 
app.config['MYSQL_USER'] = 'usuario'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'base de datos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

print ("Comexión a MySQL, exitosa!!")

# Inicializamos MYSQL
mysql = MySQL(app)

# Página de login, se necesitan las llamadas GET y POST
@app.route('/', methods=['GET', 'POST'])
def login():
    # Mensaje si algo falla...
    msg = ''
    # Verifica si "username" y "password" de la llmada POST exiten
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Crea las variables
        username = request.form['username']
        password = request.form['password']
        # Verifica si la cuenta existe en MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USUARIOS WHERE username = %s AND password = %s', (username, password,))
        # Seleeciona un registro y lo trae
        account = cursor.fetchone()
        # si la cuenta existe en los registros de la tabla de la base de datos
        if account:
            # Crea la sesión
            session['loggedin'] = True
            session['id'] = account['ID_USUARIOS']
            session['username'] = account['USERNAME']
            # Redirecciona a la página home
            # Despliega 'Acceso Exitoso!'
            return redirect(url_for('home'))
        else:
            # Si la cuenta no existe o el username/password son incorrectos
            msg = 'Incorrecto username/password!'
    # Muestra el formulario de logín con el mensaje
    return render_template('index.html', msg=msg)

# Página de logout
@app.route('/logout')
def logout():
    # Remueve los datos de la sesión
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirecciona a la página de login
   return redirect(url_for('login'))

# Página de registro, se necesitan las llamadas GET y POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Mensaje si algo va mal...
    msg = ''
    # Verifica "username", "password" y "email" en la llamada POST
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Crea las variables
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['username']
        email = request.form['email']
        rol = "Cliente"

        # Verifica que la cuenta existe
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USUARIOS WHERE USERNAME = %s', (username,))
        account = cursor.fetchone()
        # Si la cuenta existe muestra errores de validación
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección email incorrecta!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username sólo debe contener caracteres y números!'
        elif not username or not password or not email:
            msg = 'Por favor, llene el formulario!'
        else:
            # La cuenta no existe y los datos son válidos, se insertan los datos en la tabla
            cursor.execute('INSERT INTO USUARIOS VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, nombre, email, rol))
            mysql.connection.commit()
            msg = 'Se ha registrado exitosamente!'

    elif request.method == 'POST':
        # El formulario está vacío... (no hay datos en el POST)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# Página home, sólo para usuarios validados
@app.route('/home')
def home():
    # Verifica el loggedin
    if 'loggedin' in session:
        #Consulta a la base de datos
        cur = mysql.connection.cursor()
        cur.execute('''SELECT ARTICULOS.NOMBRE, ARTICULOS.PRECIO, ARTICULOS.STOCK,ARTICULOS.IMAGEN, CATEGORIAS.NOMBRE FROM ARTICULOS INNER JOIN CATEGORIAS ON ARTICULOS.ID_CATEGORIAS = CATEGORIAS.ID_CATEGORIAS''')
        articulos = cur.fetchall()
        # Test de recepción correcta de elementos, muestra los datos en la consola
        print(articulos)
        # Usuario loggedin, se muestra la página home.
        # Y pasamos los datos al template
        return render_template('home.html', username=session['username'], articulos = articulos)
    # Usuario sin loggedin se redireciona a la página login
    return redirect(url_for('login'))

# Página de perfil, sólo para usuarios validados
@app.route('/profile')
def profile():
    # Verifica al usuario loggedin
    if 'loggedin' in session:
        # Seleccionamos la información del usuario validado
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USUARIOS WHERE ID_USUARIOS = %s', (session['id'],))
        account = cursor.fetchone()
        # Se muestra la información de la cuenta
        return render_template('profile.html', account=account)
    # Usuario no validado. se redireciona a la ágina login
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)