from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configuración de la base de datos
def get_db_connection():
    return MySQLdb.connect(
        host="172.17.0.2",  # Dirección IP de tu contenedor o servidor MySQL
        user="root",
        passwd="root",
        db="ejercicio3"
    )

# Página principal con 5 logros
@app.route('/')
def index():
    portfolio = [
        {"id": 1, "title": "Creación OpenVPN", "description": "Creación de OpenVPN con Certtificados de forma Manual.", "image": "cloud_project.jpg"},
        {"id": 2, "title": "Crackeador de contraseñas", "description": "Cómo crackear contraseñas con PowerShell.", "image": "devops_pipeline.jpg"},
        {"id": 3, "title": "Planificación de redes", "description": "Creación ficticia de una estructura de red para una compañía.", "image": "network_security.jpg"},
        {"id": 4, "title": "Seguridad de redes informáticas", "description": "Creación de servicio DHCP.", "image": "db_optimization.jpg"},
        {"id": 5, "title": "Paquetes en base de datos", "description": "Creación de base de datos con el metodo de paquetes.", "image": "flask_web.jpg"},
    ]
    return render_template("index.html", portfolio=portfolio)

# Página de cada logro
@app.route('/logro/<int:logro_id>')
def logro(logro_id):
    logros = {
        1: "Detalles sobre el proyecto en OpenVPN...",
        2: "Detalles sobre el crackeo de contraseñas...",
        3: "Detalles sobre la planificación de redes...",
        4: "Detalles sobre la seguridad de redes informáticas...",
        5: "Detalles sobre el desarrollo de base de datos con paquetes...",
    }
    return render_template("logro.html", logro_id=logro_id, description=logros.get(logro_id, "No encontrado"))

# Página de búsqueda en la base de datos y el portafolio
@app.route('/test_db', methods=['GET'])
def test_db():
    query = request.args.get('q', '')
    results = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if query:
            # Si el término de búsqueda está en el portafolio, busca en el título y descripción
            found_in_portfolio = False
            portfolio = [
                {"id": 1, "title": "Creación OpenVPN", "description": "Creación de OpenVPN con Certtificados de forma Manual.", "image": "cloud_project.jpg"},
                {"id": 2, "title": "Crackeador de contraseñas", "description": "Cómo crackear contraseñas con PowerShell.", "image": "devops_pipeline.jpg"},
                {"id": 3, "title": "Planificación de redes", "description": "Creación ficticia de una estructura de red para una compañía.", "image": "network_security.jpg"},
                {"id": 4, "title": "Seguridad de redes informáticas", "description": "Creación de servicio DHCP.", "image": "db_optimization.jpg"},
                {"id": 5, "title": "Paquetes en base de datos", "description": "Creación de base de datos con el metodo de paquetes.", "image": "flask_web.jpg"},
            ]
            for item in portfolio:
                if query.lower() in item["title"].lower() or query.lower() in item["description"].lower():
                    results.append(f'<a href="{url_for("logro", logro_id=item["id"])}">La palabra "{query}" está en el portafolio en el logro: {item["title"]}</a>')
                    found_in_portfolio = True

            if not found_in_portfolio:
                results.append(f'No se encontró "{query}" en el portafolio.')

            # Si la búsqueda es sobre la base de datos, consulta en la tabla persona
            cursor.execute("SELECT * FROM persona WHERE nombre LIKE %s OR ciudad LIKE %s", (f"%{query}%", f"%{query}%"))
            db_results = cursor.fetchall()
            if db_results:
                results.append(f'Resultados en la base de datos:')
                for row in db_results:
                    results.append(f"Nombre: {row[1]}, Edad: {row[2]}, Ciudad: {row[3]}, Experiencia: {row[4]}, Trabajo actual: {row[5]}")
            else:
                results.append(f'No se encontraron resultados para "{query}" en la base de datos.')

        cursor.close()
        connection.close()

        return render_template("test_db.html", tables=tables, query=query, results=results)
    except Exception as e:
        return f'<h1>Error al conectar a la base de datos: {str(e)}</h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
