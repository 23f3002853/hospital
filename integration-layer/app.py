from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated VXML → Conversational AI connector
@app.route("/vxml/request", methods=["POST"])
def vxml_request():
    data = request.json
    user_input = data.get("speech", "")

    # Simulated conversational AI response
    if "appointment" in user_input.lower():
        response = "Your appointment request is registered."
    else:
        response = "Please say appointment booking or doctor availability."

    return jsonify({
        "ivr_response": response
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
