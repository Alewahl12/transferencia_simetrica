from flask import Flask, request, render_template
from cryptography.fernet import Fernet
import json


# Chave simétrica (gerada previamente)
with open('chave_simetrica.json', 'r') as file:
    data = json.load(file)
    chave_carregada = data['chave']

def decrypt(mensagem_criptografada):
  
    chave_simetrica = Fernet(chave_carregada)
    return chave_simetrica.decrypt(mensagem_criptografada)

app = Flask(__name__)

@app.route('/receber_mensagem', methods=['POST'])
def receber():
  # Check if a file is included in the request
  if 'file' in request.files:
    # This approach assumes the data is sent as a single file named 'file'
    received_data = request.files['file'].read().decode("utf-8")
    print(f"Received data: {received_data}")
    mensagem_descriptografada = decrypt(received_data)
    print(mensagem_descriptografada)
    return "Mensagem recebida!"
  else:
    # Handle the case where no file is sent
    return "Error: No data received"

if __name__ == '__main__':
  app.run(host='localhost', port=5001)





        
    


