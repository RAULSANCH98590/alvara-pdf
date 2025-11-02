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
    print("📨 Recebi o formulário!")  # Mostra no terminal se o POST chegou

    dados = {
        "credor": request.form['credor'],
        "cpf": request.form['cpf'],
        "advogado": request.form['advogado'],
        "processo": request.form['processo'],
        "valor": request.form['valor'],
        "cumprimento": request.form['cumprimento'],
        "assunto": request.form['assunto'],
        "situacao": request.form['situacao'],
        "data": date.today().strftime("%d/%m/%Y")
    }

    modelo = "Alvara_Liberacao_Base1.pdf"
    pdf = fitz.open(modelo)
    page = pdf[0]

    campos = {
        "credor": (120, 173),
        "cpf": (143, 187),
        "advogado": (150, 202),
        "processo": (145, 245),
        "valor": (163, 429),
        "cumprimento": (313, 300),
        "assunto": (125, 329),
        "situacao": (126, 344),
        "data": (110, 610)
    }

    # Insere os dados
    page.insert_text(campos["credor"], f"{dados['credor']}", fontsize=11)
    page.insert_text(campos["cpf"], f"{dados['cpf']}", fontsize=11)
    page.insert_text(campos["advogado"], f"{dados['advogado']}", fontsize=11)
    page.insert_text(campos["processo"], f"{dados['processo']}", fontsize=11)
    page.insert_text(campos["valor"], f"R$ {dados['valor']}", fontsize=11)
    page.insert_text(campos["cumprimento"], f"{dados['cumprimento']}", fontsize=11)
    page.insert_text(campos["assunto"], f"{dados['assunto']}", fontsize=11)
    page.insert_text(campos["situacao"], f"{dados['situacao']}", fontsize=11)
    page.insert_text(campos["data"], f"{dados['data']}", fontsize=11)

    output = io.BytesIO()
    pdf.save(output)
    output.seek(0)

    nome_arquivo = f"Alvara_Liberacao_{dados['credor'].replace(' ', '_')}.pdf"
    return send_file(output, as_attachment=True, download_name=nome_arquivo, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

