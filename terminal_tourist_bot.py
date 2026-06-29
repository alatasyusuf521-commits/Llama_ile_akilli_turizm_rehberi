#import libraries
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory

#ortam değişkenlerini tanımla (GROQ API KEY tanımla)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Llama model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,  # 0'a yakınsa garanti cevap verir, 1'e yakınsa daha yaratıcı/çeşitli cevap verir, 1'e yaklaştıkça halüsinasyon riski artar
    groq_api_key=GROQ_API_KEY
)

#Hafıza Ekleme, konuşma geçmişi takip etme
memory = ConversationBufferMemory(return_messages=True)

SYSTEM_PROMPT = (
    "Sen bir akıllı turizm rehberisin. Kullanıcıya gezilecek yerler, tatil önerileri, "
    "ulaşım bilgileri ve yöresel yemekler gibi konularda yardımcı olmalısın."
)

#Flask uygulamasını oluştur
app = Flask(__name__)


@app.route("/")
def index():
    # templates/index.html dosyasını render eder
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Mesaj boş olamaz."}), 400

        # Kullanıcının mesajını hafızaya kaydet
        memory.chat_memory.add_user_message(user_input)

        # Model için gerekli olan tüm mesajları oluştur: sistem + geçmiş + yeni mesaj
        messages = (
            [SystemMessage(content=SYSTEM_PROMPT)]
            + memory.load_memory_variables({})["history"]
            + [HumanMessage(content=user_input)]
        )

        # Modelden yanıt al
        response = llm.invoke(messages)

        # Modelin cevabını hafızaya ekle
        memory.chat_memory.add_ai_message(response.content)

        return jsonify({"response": response.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)