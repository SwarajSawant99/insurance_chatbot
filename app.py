from flask import Flask, render_template, request, jsonify
from rag.retriever import Retriever
from rag.generator import GroqGenerator
import os
from dotenv import load_dotenv

app = Flask(__name__)

# =========================
# ENV VARIABLES
# =========================
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# CHAT PAGE
# =========================

@app.route("/chat/<insurance_type>")
def chat(insurance_type):

    return render_template(
        "chat.html",
        insurance_type=insurance_type
    )


# =========================
# ASK ROUTE
# =========================

@app.route("/ask", methods=["POST"])
def ask():

    print("ASK ROUTE HIT")

    return jsonify({
        "answer": "Backend is working correctly"
    })
    


# =========================
# RUN FLASK APP
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )