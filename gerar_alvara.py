from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import io
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    print("📨 Recebi o formulário!")  # Log

    # --- Dados vindos do formulário ---
    dados = {
        "credor": request.form['credor'],
        "cpf": request.form['cpf'],
        "advogado": request.form['advogado'],
        "processo": request.form['processo'],
        "valor": request.form['valor'],
        "cumprimento": request.form['cumprimento'],
        "data": date.today().strftime("%d/%m/%Y")
    }

    # --- Campos fixos (não vêm do formulário) ---
    assunto_fixo = "Decisão Favorável"
    situacao_fixa = "AUTORIZADO"

    # --- Abre o PDF modelo ---
    modelo = "Alvara_Liberacao_Base1.pdf"
    pdf = fitz.open(modelo)
    page = pdf[0]

    # --- Coordenadas dos campos ---
    campos = {
        "credor": (120, 173),
        "cpf": (143, 187),
        "advogado": (150, 202),
        "processo": (145, 245),
        "valor": (163, 429),
        "cumprimento": (313, 300),
        "assunto": (120, 329),  # posição após o rótulo “Assunto:”
        "situacao": (123, 344),  # posição após o rótulo “Situação:”
        "data": (110, 610)
    }

    # --- Inserção dos textos ---
    page.insert_text(campos["credor"], f"{dados['credor']}", fontsize=11)
    page.insert_text(campos["cpf"], f"{dados['cpf']}", fontsize=11)
    page.insert_text(campos["advogado"], f"{dados['advogado']}", fontsize=11)
    page.insert_text(campos["processo"], f"{dados['processo']}", fontsize=11)
    page.insert_text(campos["valor"], f"R$ {dados['valor']}", fontsize=11)
    page.insert_text(campos["cumprimento"], f"{dados['cumprimento']}", fontsize=11)

    # --- Campos fixos: imprimem apenas os valores ---
    page.insert_text(campos["assunto"], f"{assunto_fixo}", fontsize=11)
    page.insert_text(campos["situacao"], f"{situacao_fixa}", fontsize=11)

    # --- Data ---
    page.insert_text(campos["data"], f"{dados['data']}", fontsize=11)

    # --- Salva o novo PDF ---
    output = io.BytesIO()
    pdf.save(output)
    output.seek(0)
    pdf.close()

    nome_arquivo = f"Alvara_Liberacao_{dados['credor'].replace(' ', '_')}.pdf"
    return send_file(output, as_attachment=True, download_name=nome_arquivo, mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
