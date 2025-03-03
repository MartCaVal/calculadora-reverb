from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML para la interfaz web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora de Reverb y Pre-delay</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        input, select { padding: 10px; margin: 10px; display: block; width: 100%; max-width: 200px; margin: auto; }
        label { display: block; margin-top: 10px; }
        table { width: 50%; margin: auto; border-collapse: collapse; }
        th, td { padding: 5px; border: 1px solid black; text-align: center; }
    </style>
</head>
<body>
    <h2>Calculadora de Reverb y Pre-delay</h2>
    <form method="POST">
        <label for="bpm">Introduce el BPM:</label>
        <input type="number" id="bpm" name="bpm" value="{{ bpm if bpm else '' }}" required>

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
    demisemifusa = negra / 32  # Pre-delay sigue igual basado en la demisemifusa
    pre_delay = demisemifusa  # Asignamos el valor correcto al pre-delay

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
