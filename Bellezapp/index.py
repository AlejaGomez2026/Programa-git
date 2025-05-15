from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configurar la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def _repr_(self):
        return f'<User {self.username}>'

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            try:
                # Crear una nueva instancia de usuario
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('about'))  # Redirigir al inicio de sesión después del registro
            except IntegrityError:
                db.session.rollback()
                return render_template('register.html', error="El nombre de usuario o el correo electrónico ya están en uso.")
        else:
            return render_template('register.html', error="Las contraseñas no coinciden")

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        return redirect(url_for('start'))
    else:
        return redirect(url_for('home', error="Nombre de usuario o contraseña incorrectos"))

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/cortes')
def cortes():
    return render_template('cortes.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')



if __name__ == '__main__':
    app.run(debug=True)