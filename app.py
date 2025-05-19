from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'  # Cambia esto si tienes contraseña
app.config['MYSQL_DB'] = 'asn'
app.config['MYSQL_PORT'] = 2345  # Puerto por defecto de MySQL, cámbialo si usas otro

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleado')
    empleados = cur.fetchall()
    cur.close()
    return render_template('index.html', empleados=empleados)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        salario = request.form['salario']
        area = request.form['area']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO empleado (nombre, salario, area) VALUES (%s, %s, %s)', (nombre, salario, area))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        salario = request.form['salario']
        area = request.form['area']
        cur.execute('UPDATE empleado SET nombre=%s, salario=%s, area=%s WHERE id=%s', (nombre, salario, area, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM empleado WHERE id=%s', (id,))
    empleado = cur.fetchone()
    cur.close()
    return render_template('edit.html', empleado=empleado)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleado WHERE id=%s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
