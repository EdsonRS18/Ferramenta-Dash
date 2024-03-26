from flask import Flask, render_template
from app import app  # Importe sua aplicação Dash

# Crie uma instância do aplicativo Flask
flask_app = Flask(__name__)

# Roteamento Flask: adicione uma rota para sua aplicação Dash
@flask_app.route('/')
def index():
    return render_template(r'C:\Users\Edson\Documents\TCC\versao-dividida\index.html')

# Inicialize a aplicação Dash dentro do aplicativo Flask
app.init_app(flask_app)

if __name__ == '__main__':
    flask_app.run(debug=True)
