from flask import Flask, render_template, request, send_file, redirect, url_for, session
import fitz  # PyMuPDF
import io
from datetime import date
from num2words import num2words

app = Flask(__name__)
app.secret_key = "segredo_seguro"

# --- Logins fixos ---
USUARIOS = {
    "admraul@gmail.com": "Summer@100",
    "leoneves@gmail.com": "KarateKid2025",
    "gustavo7@gmail.com": "777@123"
}

@app.route('/')
def index():
    if "usuario" in session:
        return redirect(url_for('formulario'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if email in USUARIOS and USUARIOS[email] == senha:
        session["usuario"] = email
        return redirect(url_for('formulario'))
    else:
        return render_template('login.html', erro="E-mail ou senha incorretos")

@app.route('/logout')
def logout():
    session.pop("usuario", None)
    return redirect(url_for('index'))

@app.route('/form')
def formulario():
    if "usuario" not in session:
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    if "usuario" not in session:
        return redirect(url_for('index'))

    print("📨 Recebi o formulário!")

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

    # --- Valor por extenso com parênteses e maiúscula ---
    try:
        valor_num = float(dados["valor"].replace(".", "").replace(",", "."))
        valor_extenso = num2words(valor_num, lang='pt_BR', to='currency').title()
        valor_extenso = f"({valor_extenso})"
    except:
        valor_extenso = "(Valor Inválido)"

    # --- Abre o modelo PDF ---
    modelo = "Alvara_Liberacao_Base1.pdf"
    pdf = fitz.open(modelo)
    page = pdf[0]

    # --- Coordenadas fixas ---
    campos = {
        "credor": (117, 270),
        "cpf": (138, 284),
        "advogado": (150, 298),
        "processo": (146, 325),
        "valor": (170, 522),
        "cumprimento": (264, 383),
        "assunto": (127, 425),
        "situacao": (130, 440),
        "valor_extenso": (216, 522),  # coordenada fixa para o texto por extenso
        "data": (70, 690)
    }

    # --- Inserção dos campos ---
    page.insert_text(campos["credor"], dados["credor"], fontsize=11)
    page.insert_text(campos["cpf"], dados["cpf"], fontsize=11)
    page.insert_text(campos["advogado"], dados["advogado"], fontsize=11)
    page.insert_text(campos["processo"], dados["processo"], fontsize=11)
    page.insert_text(campos["valor"], dados["valor"], fontsize=11, fontname="helv", render_mode=2)  # negrito
    page.insert_text(campos["cumprimento"], dados["cumprimento"], fontsize=11)
    page.insert_text(campos["assunto"], "Decisão Favorável", fontsize=11)
    page.insert_text(campos["situacao"], "AUTORIZADO", fontsize=11)
    page.insert_text(campos["valor_extenso"], valor_extenso, fontsize=10, fontname="helv", render_mode=2)  # negrito e parênteses
    page.insert_text(campos["data"], dados["data"], fontsize=11)

    # --- Salvar PDF ---
    output = io.BytesIO()
    pdf.save(output)
    output.seek(0)
    pdf.close()

    nome_arquivo = f"Alvara_Liberacao_{dados['credor'].replace(' ', '_')}.pdf"
    return send_file(output, as_attachment=True, download_name=nome_arquivo, mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
