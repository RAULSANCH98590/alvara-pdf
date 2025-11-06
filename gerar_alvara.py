from flask import Flask, render_template, request, send_file, Response
import fitz  # PyMuPDF
import io
from datetime import date
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    try:
        print("📨 Recebi o formulário!")  # Log no terminal

        # --- Dados vindos do formulário ---
        dados = {
            "credor": request.form.get('credor', ''),
            "cpf": request.form.get('cpf', ''),
            "advogado": request.form.get('advogado', ''),
            "processo": request.form.get('processo', ''),
            "valor": request.form.get('valor', ''),
            "cumprimento": request.form.get('cumprimento', ''),
            "data": date.today().strftime("%d/%m/%Y")
        }

        # --- Campos fixos ---
        assunto_fixo = "Decisão Favorável"
        situacao_fixa = "AUTORIZADO"

        # --- Abre o PDF modelo ---
        modelo = "Alvara_Liberacao_Base1.pdf"
        doc = fitz.open(modelo)
        page = doc[0]

        # --- Coordenadas dos campos ---
        campos = {
            "credor": (117, 270),
            "cpf": (138, 284),
            "advogado": (150, 298),
            "processo": (146, 325),
            "valor": (173, 522),
            "cumprimento": (264, 383),
            "assunto": (127, 425),
            "situacao": (130, 440),
            "data": (95, 610)
        }

        # --- Função auxiliar para escrever com fallback de fonte/negrito ---
        def escrever(pos, texto, fontsize=11, bold=False):
            x, y = pos
            # tenta primeiro usar fonte padrão bold se bold=True
            try:
                if bold:
                    # Times-Bold é geralmente suportada
                    page.insert_text((x, y), texto, fontsize=fontsize, fontname="Times-Bold")
                else:
                    page.insert_text((x, y), texto, fontsize=fontsize, fontname="Times-Roman")
                return
            except Exception:
                # fallback: tentar render_mode que aumenta espessura do traço
                try:
                    if bold:
                        page.insert_text((x, y), texto, fontsize=fontsize, render_mode=2)
                    else:
                        page.insert_text((x, y), texto, fontsize=fontsize)
                    return
                except Exception:
                    # último recurso: inserir sem opções
                    page.insert_text((x, y), texto, fontsize=fontsize)

        # --- Inserção dos textos ---
        escrever(campos["credor"], dados["credor"])
        escrever(campos["cpf"], dados["cpf"])
        escrever(campos["advogado"], dados["advogado"])
        escrever(campos["processo"], dados["processo"])
        escrever(campos["valor"], dados["valor"], bold=True)  # valor em negrito (fallback incluso)
        escrever(campos["cumprimento"], dados["cumprimento"])

        # --- Campos fixos (apenas valores, pois o template já tem os rótulos) ---
        escrever(campos["assunto"], assunto_fixo)
        escrever(campos["situacao"], situacao_fixa)

        # --- Data ---
        escrever(campos["data"], dados["data"], fontsize=11)

        # --- Salva o novo PDF ---
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        doc.close()

        nome_arquivo = f"Alvara_Liberacao_{dados['credor'].replace(' ', '_')}.pdf"
        return send_file(output, as_attachment=True, download_name=nome_arquivo, mimetype='application/pdf')

    except Exception as e:
        # imprime o traceback completo no terminal para diagnosticarmos
        tb = traceback.format_exc()
        print("===== ERRO NA GERAÇÃO DO PDF =====")
        print(tb)
        print("==================================")
        # retorna erro simples ao navegador (você verá também no terminal)
        return Response("Erro ao gerar PDF. Verifique o terminal para detalhes.", status=500)

if __name__ == '__main__':
    app.run(debug=True)
