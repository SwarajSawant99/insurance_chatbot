from flask import Flask, render_template, request, jsonify
from rag.retriever import Retriever
from rag.generator import GroqGenerator
import os

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# generator
generator = GroqGenerator(API_KEY)

# load retrievers ONCE
print("Loading health retriever...")
health_retriever = Retriever(
    os.path.join(BASE_DIR, "output", "health.index"),
    os.path.join(BASE_DIR, "output", "health_chunks.json")
)

print("Loading car retriever...")
car_retriever = Retriever(
    os.path.join(BASE_DIR, "output", "car.index"),
    os.path.join(BASE_DIR, "output", "car_chunks.json")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat/<insurance_type>")
def chat(insurance_type):
    return render_template("chat.html", insurance_type=insurance_type)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        query = data["query"]
        insurance_type = data["insurance_type"]

        print("Question:", query)

        # choose retriever
        if insurance_type == "health":
            retriever = health_retriever
        else:
            retriever = car_retriever

        # search
        results = retriever.search(query)

        # generate
        answer = generator.generate_answer(query, results)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "answer": f"Backend Error: {str(e)}"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)