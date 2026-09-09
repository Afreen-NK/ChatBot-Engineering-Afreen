"""
app.py - Flask Web Server and API for CareerCompass FAQ Chatbot

Endpoints:
- GET  /                : Renders interactive web chat UI
- POST /chat            : Main chatbot query endpoint (TF-IDF + Cosine Matching)
- GET  /api/categories  : Returns available engineering FAQ categories
- GET  /api/faqs        : Returns FAQ questions, optionally filtered by category
- GET  /api/health      : Health check and engine statistics
"""

import logging
from flask import Flask, jsonify, render_template, request
from chatbot import CareerCompassBot

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CareerCompassApp")

# Instantiate CareerCompass bot engine
bot = CareerCompassBot(faq_path="faq_data.json", similarity_threshold=0.25)


@app.route("/")
def index():
    """Renders the single-page chat user interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles user chat messages.
    Expects JSON payload: {"message": "User query string", "debug": false}
    Returns JSON matching response.
    """
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({
                "answer": "Invalid request format. Please provide a JSON object with a 'message' field.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True
            }), 400

        user_message = data.get("message", "")

        # Input type check
        if not isinstance(user_message, str):
            return jsonify({
                "answer": "Invalid message format. The 'message' field must be text.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True
            }), 400

        # Input length safety check (max 1000 characters)
        if len(user_message) > 1000:
            return jsonify({
                "answer": "Your message is too long. Please ask a concise question (under 1000 characters).",
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True
            }), 400

        # Empty or whitespace message check
        if not user_message.strip():
            return jsonify({
                "answer": "Please type a question first.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None,
                "fallback": True
            }), 200

        # Query CareerCompass engine
        result = bot.get_response(user_message)

        # Structure response for UI (omitting raw debug vectors unless requested)
        include_debug = data.get("debug", False) or request.args.get("debug") == "true"
        response_data = {
            "answer": result["answer"],
            "confidence": result["confidence"],
            "matched_question": result["matched_question"],
            "category": result["category"],
            "fallback": result["fallback"],
        }

        if include_debug:
            response_data["top_matches"] = result.get("top_matches", [])

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error handling /chat request: {e}", exc_info=True)
        return jsonify({
            "answer": "An unexpected server error occurred. Please try asking again in a moment.",
            "confidence": 0.0,
            "matched_question": None,
            "category": None,
            "fallback": True
        }), 500


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Returns all FAQ categories with count of available FAQs."""
    try:
        categories = bot.get_categories()
        category_counts = {}
        for cat in categories:
            faqs = bot.get_faqs_by_category(cat)
            category_counts[cat] = {
                "name": cat,
                "count": len(faqs),
                "sample_questions": [f["question"] for f in faqs[:3]]
            }
        return jsonify({
            "status": "success",
            "categories": category_counts
        }), 200
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/faqs", methods=["GET"])
def get_faqs():
    """Returns FAQ entries, optionally filtered by category."""
    try:
        category = request.args.get("category")
        if category:
            faqs = bot.get_faqs_by_category(category)
        else:
            faqs = bot.faqs

        simplified = [
            {
                "id": f["id"],
                "category": f["category"],
                "question": f["question"],
                "answer": f["answer"]
            }
            for f in faqs
        ]
        return jsonify({
            "status": "success",
            "total": len(simplified),
            "faqs": simplified
        }), 200
    except Exception as e:
        logger.error(f"Error fetching FAQs: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint providing engine metadata."""
    return jsonify({
        "status": "healthy",
        "faq_count": len(bot.faqs),
        "categories_count": len(bot.get_categories()),
        "similarity_threshold": bot.similarity_threshold,
        "model": "TF-IDF + Cosine Similarity (NLTK Lemmatizer)"
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "HTTP method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CareerCompass — Engineering Student FAQ Chatbot")
    print("  Running locally at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
