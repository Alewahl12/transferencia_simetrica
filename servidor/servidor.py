from flask import Flask, request, render_template
from cryptography.fernet import Fernet
import requests
import io
import json

app = Flask(__name__)

rota_final = "http://localhost:5001/receber_mensagem"

# Chave simétrica (gerada previamente)
with open('chave_simetrica.json', 'r') as file:
    data = json.load(file)
    chave_carregada = data['chave']

chave_simetrica = Fernet(chave_carregada)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    mensagem = request.form.get('mensagem')
    if mensagem is not None:
        mensagem_criptografada = chave_simetrica.encrypt(mensagem.encode("utf-8"))
        string_para_enviar = mensagem_criptografada
        dados = string_para_enviar
        dados_post = {'file': io.BytesIO(dados)}
        requests.post(rota_final, files=dados_post)
        return "Mensagem enviada"
    else:
        # Handle the case where 'mensagem' is missing
        return "Error: Missing 'mensagem' data in request"


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

#curl -X POST http://localhost:5000/encrypt -d mensagem="Hello, World!"

#curl -X POST http://localhost:5000/decrypt -d mensagem_criptografada=gAAAAABmIAJ_Hy9FhpzR6XCdXbcHBkJPhMNOQ5-uvYHHEBgRsj-xhsqLyq2QnzK4WaP6uRhOvGA4yc1A-OVrGR7iD09jd0f8xA==
