from flask import Flask, request, render_template_string, jsonify
import time

app = Flask(__name__)

# HTML con diseño mejorado y botón TAP para calcular BPM
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora de Reverb</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        h2 { font-size: 3vw; } /* Se adapta al tamaño de pantalla */
        label { font-size: 2.5vw; display: block; margin-top: 20px; }
        input, select { font-size: 2.5vw; padding: 10px; width: 80%; max-width: 400px; margin-top: 10px; }
        button { background-color: green; color: white; font-size: 3vw; padding: 15px 30px; border: none; cursor: pointer; margin-top: 20px; }
        button:hover { background-color: darkgreen; }
        table { width: 90%; max-width: 600px; margin: 20px auto; border-collapse: collapse; font-size: 2vw; }
        th, td { border: 1px solid black; padding: 15px; text-align: center; }

        /* Botón TAP circular */
        .tap-button {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background-color: red;
            color: white;
            font-size: 2vw;
            font-weight: bold;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }
        .tap-button:active {
            background-color: darkred;
        }

        /* Ajustes para pantallas pequeñas */
        @media (max-width: 600px) {
            h2 { font-size: 6vw; }
            label, input, select, button { font-size: 5vw; }
            table { font-size: 4vw; }
            .tap-button { width: 100px; height: 100px; font-size: 5vw; }
        }
    </style>
    <script>
        let tapTimes = [];

        function tapBPM() {
            let now = new Date().getTime();
            tapTimes.push(now);
            
            if (tapTimes.length > 1) {
                let intervals = [];
                for (let i = 1; i < tapTimes.length; i++) {
                    intervals.push(tapTimes[i] - tapTimes[i - 1]);
                }
                let avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
                let bpm = Math.round(60000 / avgInterval);
                document.getElementById("bpm").value = bpm;
            }

            if (tapTimes.length > 4) {
                tapTimes.shift();
            }
        }
    </script>
</head>
<body>
    <h2>Calculadora de Reverb</h2>
    <form method="POST">
        <label for="bpm">Introduce el BPM:</label>
        <input type="number" id="bpm" name="bpm" value="{{ bpm if bpm else '' }}" required>
        <br>
        <button type="button" class="tap-button" onclick="tapBPM()">TAP</button>

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
    demisemifusa = negra / 32  # Pre-delay basado en la demisemifusa
    pre_delay = demisemifusa  

    # Ajuste del tiempo de Decay según el instrumento
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
