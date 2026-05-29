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

        print("Creating retriever...")

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

        print("RETRIEVER CREATED")

        # =========================
        # LOAD GENERATOR
        # =========================

        print("Creating generator...")

        generator = GroqGenerator(API_KEY)

        print("GENERATOR CREATED")

        # =========================
        # SEARCH
        # =========================

        print("Starting search...")

        results = retriever.search(query)

        print("SEARCH COMPLETED")
        print(f"Retrieved {len(results)} chunks")

        # =========================
        # GENERATE ANSWER
        # =========================

        print("Generating answer...")

        answer = generator.generate_answer(
            query,
            results
        )

        print("ANSWER GENERATED")
        print("RETURNING RESPONSE")

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("===================================")
        print("BACKEND ERROR:")
        print(repr(e))
        print("===================================")

        return jsonify({
            "answer": f"Backend Error: {str(e)}"
        }), 500


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