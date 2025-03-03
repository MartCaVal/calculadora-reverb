from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ""
    if request.method == 'POST':
        tipo_instrumento = request.form['tipo_instrumento']
        tiempo = request.form['tiempo']
        resultado = f"Cálculo para {tipo_instrumento} con tiempo {tiempo} ms"
    
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculadora de Reverb</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            h1 {{ font-size: 2em; }}
            label {{ font-size: 1.5em; display: block; margin-top: 20px; }}
            select, input {{ font-size: 1.5em; padding: 10px; width: 300px; margin-top: 10px; }}
            button {{ background-color: green; color: white; font-size: 2em; padding: 10px 20px; border: none; cursor: pointer; margin-top: 20px; }}
            button:hover {{ background-color: darkgreen; }}
            p {{ font-size: 1.5em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Calculadora de Reverb</h1>
        <form method="post">
            <label for="tipo_instrumento">Selecciona tipo de instrumento:</label>
            <select name="tipo_instrumento" id="tipo_instrumento">
                <option value="Percusión">Percusión</option>
                <option value="Melodía">Melodía</option>
            </select>
            <br>
            <label for="tiempo">Introduce tiempo (ms):</label>
            <input type="number" name="tiempo" id="tiempo" required>
            <br>
            <button type="submit">Calcular</button>
        </form>
        <p>{resultado}</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)