from flask import Flask, request, jsonify
from flask_cors import CORS

import os #For reading files
import cv2 #For image processing
import numpy as np
from deepface import DeepFace #For face recognition

app = Flask(__name__)
CORS(app)  # Isso habilitará o CORS para todos os domínios

diretorio = "./uploads/"
def check_face(image):
    global face_match

    # Read all images on the folder "users"
    imagens = os.listdir(diretorio)
    teste = False
    for imagem in imagens:
        # Read the image
        reference_img = cv2.imread(diretorio + imagem)

        # Compare the image with the reference image
        try:
            if DeepFace.verify(image, reference_img.copy())['verified']:
                teste = True
        except ValueError:
            continue # Continua sem parar.
    return teste

@app.route("/")
def home():
    return "Home"

@app.route("/register", methods=["POST"])
def register_image():
    # Verifique se a requisição contém a parte 'image'
    if 'image' not in request.files:
        return jsonify({"message": "No image part"}), 400
    print('chega aqui')
    file = request.files['image']
    name = request.form['name']  # acessa o nome da parte do formulário

    # Se o usuário não selecionar um arquivo, o navegador também
    # enviará um campo de arquivo vazio sem nome de arquivo.
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    # Use o nome fornecido para salvar o arquivo
    file.save(os.path.join("uploads", f"{name}.jpg"))  # Supondo que seja uma imagem JPEG

    return jsonify({"message": "Image received!"}), 200


@app.route("/verify", methods=["POST"])
def verify_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image part"}), 400
    file = request.files['image']

    temp_dir = "temporary"
    os.makedirs(temp_dir, exist_ok=True)  # Cria o diretório temporário se não existir

    image_path = os.path.join(temp_dir, "verify.jpg")
    file.save(image_path)  # Salvar a imagem temporariamente

    match = check_face(image_path)  # Passa o caminho do arquivo, não os bytes da imagem

    os.remove(image_path)  # Apagar a imagem temporária

    if match:
        return jsonify({"message": "MATCH!"}), 200
    else:
        return jsonify({"message": "NO MATCH!"}), 200


if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('temporary', exist_ok=True)
    app.run(debug=True)