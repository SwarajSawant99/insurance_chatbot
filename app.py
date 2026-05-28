from flask import Flask, render_template, request, jsonify
from rag.retriever import Retriever
from rag.generator import GroqGenerator
import os

app = Flask(__name__)

# =========================
# ENV VARIABLES
# =========================

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

    try:

        data = request.get_json()

        query = data.get("query")
        insurance_type = data.get("insurance_type")

        print("===================================")
        print("Question:", query)
        print("Insurance Type:", insurance_type)

        # =========================
        # LOAD RETRIEVER
        # =========================

        print("Loading retriever...")

        if insurance_type == "health":

            retriever = Retriever(
                os.path.join(BASE_DIR, "output", "health.index"),
                os.path.join(BASE_DIR, "output", "health_chunks.json")
            )

        elif insurance_type == "car":

            retriever = Retriever(
                os.path.join(BASE_DIR, "output", "car.index"),
                os.path.join(BASE_DIR, "output", "car_chunks.json")
            )

        else:

            return jsonify({
                "answer": "Invalid insurance type selected."
            })

        print("Retriever loaded successfully")

        # =========================
        # LOAD GENERATOR
        # =========================

        print("Loading generator...")

        generator = GroqGenerator(API_KEY)

        print("Generator loaded successfully")

        # =========================
        # SEARCH DOCUMENT
        # =========================

        print("Searching document...")

        results = retriever.search(query)

        print("Search completed")

        # =========================
        # GENERATE ANSWER
        # =========================

        print("Generating answer...")

        answer = generator.generate_answer(
            query,
            results
        )

        print("Answer generated successfully")

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("===================================")
        print("BACKEND ERROR:")
        print(str(e))
        print("===================================")

        return jsonify({
            "answer": str(e)
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