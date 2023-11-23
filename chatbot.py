from flask import Flask, jsonify, request
from flask_cors import CORS
import nltk
import json
import openai
from nltk.chat.util import Chat, reflections  # Adicione esta linha

app = Flask(__name__)
CORS(app)  # Adicionando CORS ao aplicativo Flask

# Pares de padrão e respostas para o chatbot
pares = [
    ['Oi', ['Olá, como você está se sentindo hoje?']],
    ['Estou me sentindo muito triste',['Sinto muito ouvir isso. Você quer falar mais sobre o que está te incomodando?']],
    # ... outros pares de perguntas e respostas
    ['adeus', ['Espero ter ajudado. Se cuide!']]
]

# Defina sua chave de API
chave_api = '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'

# Configurar a chave de API
openai.api_key = chave_api
# Função para iniciar o chat
def iniciar_chat():
    return Chat(pares, reflections)

chat = iniciar_chat()

# Rota para receber e responder às mensagens
@app.route('/responder', methods=['POST', 'OPTIONS'])
def responder():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        return response

    try:
        data = request.get_data().decode('utf-8', 'ignore')
        data = json.loads(data)
        mensagem = data['mensagem']

        # Utilize os recursos da OpenAI, como a criação de completions
        resposta_openai = openai.Completion.create(
            engine="text-davinci-003",
            prompt=mensagem,
            max_tokens=1000
        )

        resposta_chatbot = chat.respond(mensagem)  # Resposta do chatbot original
        resposta_openai_texto = resposta_openai.choices[0].text.strip()

        # Retorna uma resposta combinada do chatbot original e da OpenAI
        return jsonify({'resposta_chatbot': resposta_chatbot, 'resposta_openai': resposta_openai_texto})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    nltk.download('punkt')
    app.run(debug=True)
