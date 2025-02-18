from flask import Flask, render_template
import MySQLdb

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    nombre = "Mundo"
    return render_template("index.html", nombre=nombre)

@app.route("/test_db")
def test_db():
    try:
        connection = MySQLdb.connect(
            host="172.17.0.2",
            user="root",
            passwd="root",
            db="ejercicio3"
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        results = cursor.fetchall()
        cursor.close()
        return f'<h1>Conexión exitosa a la base de datos.</h1><p>Las tablas disponibles son: {results}</p>'
    except Exception as e:
        return f'<h1>Error al conectar a la base de datos: {str(e)}</h1>'

if __name__ == "__main__":
    app.run(debug=True)

