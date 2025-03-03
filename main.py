from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML con diseño mejorado y fondo de rejilla metálica
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora de Reverb</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: url('https://www.transparenttextures.com/patterns/black-linen.png'); /* Fondo de rejilla metálica */
            color: white;
        }
        h2 { font-size: 3vw; }
        label { font-size: 2.5vw; display: block; margin-top: 20px; }
        input, select {
            font-size: 2.5vw;
            padding: 10px;
            width: 80%;
            max-width: 400px;
            margin-top: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid white;
        }
        button {
            background-color: green;
            color: white;
            font-size: 3vw;
            padding: 15px 30px;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover { background-color: darkgreen; }
        table {
            width: 90%;
            max-width: 600px;
            margin: 20px auto;
            border-collapse: collapse;
            font-size: 2vw;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
        }
        th, td { border: 1px solid white; padding: 15px; text-align: center; }

        .tap-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            margin-top: 20px;
        }

        .tap-button {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background-color: red;
            color: white;
            font-size: 4vw;
            font-weight: bold;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            touch-action: manipulation;
        }
        .tap-button:active {
            background-color: darkred;
        }

        @media (max-width: 600px) {
            h2 { font-size: 6vw; }
            label, input, select, button { font-size: 5vw; }
            table { font-size: 4vw; }
            .tap-button { width: 150px; height: 150px; font-size: 6vw; }
        }
    </style>
</head>
<body>
    <h2>Calculadora de Reverb</h2>
    <form method="POST">
        <label for="bpm">Introduce el BPM:</label>
        <input type="number" id="bpm" name="bpm" value="{{ bpm if bpm else '' }}" required>
        <br>

        <div class="tap-container">
            <button type="button" class="tap-button" onclick="tapBPM()">TAP</button>
        </div>

        <label for="instrumento">Selecciona tipo de Instrumento:</label>
        <select id="instrumento" name="instrumento">
            <option value="percusion" {% if instrumento == 'percusion' %}selected{% endif %}>Percusión</option>
            <option value="melodia" {% if instrumento == 'melodia' %}selected{% endif %}>Melodía</option>
        </select>

        <button type="submit">Calcular</button>
    </form>

    {% if resultados %}
    <h3>Resultados:</h3>
    <table>
        <tr><th>Parámetro</th><th>Tiempo (ms)</th></tr>
        {% for tipo, tiempo in resultados.items() %}
        <tr><td>{{ tipo }}</td><td>{{ tiempo }} ms</td></tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""

def calcular_reverb(BPM, instrumento):
    negra = 60000 / BPM
    demifusa = negra / 16  # Demifusa
    pre_delay = demifusa * 1.5  # Demifusa con puntillo

    if instrumento == "percusion":
        decay = (negra * 1) * 1.1  # Una negra + 10%
    else:
        decay = (negra * 2) * 1.1  # Dos negras + 10%

    return {
        "Pre-delay recomendado": round(pre_delay, 2),
        "Tiempo de Reverb (Decay)": round(decay, 2)
    }

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = None
    bpm = None
    instrumento = "percusion"
    if request.method == "POST":
        bpm = request.form.get("bpm", type=int)
        instrumento = request.form.get("instrumento")
        if bpm and bpm > 0:
            resultados = calcular_reverb(bpm, instrumento)
    return render_template_string(HTML_TEMPLATE,
                                  resultados=resultados,
                                  bpm=bpm,
                                  instrumento=instrumento)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
