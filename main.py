import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Garante a pasta fichas
os.makedirs('fichas', exist_ok=True)

df = pd.read_csv('Conceitos.csv', skiprows=1)

# Indique os índices das colunas relevantes no seu csv:
# nome, conceito1, conceito2, conceito3, conceito4, conceito5, conceito6
selected_cols = [0, 4, 8, 12, 16, 20]
col_names = df.columns[selected_cols]
df_selected = df.iloc[:, selected_cols]

# Dados “fixos” ou fictícios para o exemplo do cabeçalho/assinatura  (ajuste conforme preciso)
graduacao = "Sd. QP PM"
comportamento = "EXCEPCIONAL"
data_promocao = "XX/XX/XXXX"
funcao_atual = ""

for idx, row in df_selected.iterrows():
    nome = row.iloc[0]
    conceitos = [row.iloc[i] for i in range(1, len(row))]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cabeçalho
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "POLÍCIA MILITAR DO PARANÁ", ln=True, align='C')
    pdf.cell(0, 8, "4º COMANDO REGIONAL", ln=True, align='C')
    pdf.cell(0, 8, "27º BATALHÃO DE POLÍCIA MILITAR", ln=True, align='C')
    pdf.ln(4)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "FICHA DE INFORMAÇÃO E AVALIAÇÃO DE CONCEITO DE PRAÇA", ln=True, align='C')
    pdf.ln(4)
    pdf.set_font("Arial", '', 10)
    # Dados do militar
    pdf.cell(0, 8, f"NOME: {nome}", ln=True)
    pdf.cell(0, 8, f"GRADUAÇÃO: {graduacao}", ln=True)
    pdf.cell(0, 8, f"COMPORTAMENTO: {comportamento}", ln=True)
    pdf.cell(0, 8, f"DATA DA ÚLTIMA PROMOÇÃO: {data_promocao}", ln=True)
    pdf.cell(0, 8, f"FUNÇÃO QUE EXERCE ATUALMENTE: {funcao_atual}", ln=True)
    pdf.ln(6)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "CONCEITOS:", ln=True)
    pdf.set_font("Arial", '', 10)
    for i, conceito in enumerate(conceitos):
        pdf.cell(0, 8, f"{col_names[i+1]}: {conceito}", ln=True)
    pdf.ln(6)

    # Observações finais / assinatura modelo
    pdf.set_font("Arial", '', 9)
    hoje = datetime.today().strftime('%d/%m/%Y')
    pdf.cell(0, 8, f"Data: {hoje}", ln=True)
    pdf.ln(12)
    pdf.cell(0, 8, "_____________________________________________", ln=True)
    pdf.cell(0, 5, "Ten.- Cel. QOEM PM Luiz Antonio Ferreira Junior", ln=True)
    pdf.cell(0, 5, "Comandante do 27º BPM/4º CRPM", ln=True)

    # Salva PDF
    filename = f"fichas/ficha_{nome.replace(' ','_')}.pdf"
    pdf.output(filename)

print("PDFs gerados no padrão solicitado!")
