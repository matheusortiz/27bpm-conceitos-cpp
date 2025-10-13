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
graduacao = "Mango . QP PM"
comportamento = "TESTE"
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
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "FICHA DE INFORMAÇÃO E AVALIAÇÃO DE CONCEITO DE PRAÇA", ln=True, align='C')
    pdf.ln(4)

    # Começo da nova tabela (3 colunas x 2 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 3  # largura da página menos margens dividida por 3
    row_height = 10
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["NOME/CPF", "GRADUAÇÃO", "COMPORTAMENTO"],
        [f"{nome}", f"{graduacao}", f"{comportamento}"],
    ]
    
    # Imprime a tabela
    pdf.set_font("Arial", size=12)
    for row in table_data:
        for cell in row:
            pdf.cell(col_width, row_height, txt=cell, border=1)
        pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela

    # Começo da nova tabela (2 colunas x 2 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 2  # largura da página menos margens dividida por 3
    row_height = 10
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["DATA DA ÚLTIMA PROMOÇÃO", "FUNÇÃO QUE EXERCE ATUALMENTE"],
        [f"{data_promocao}", f"{funcao_atual}"],
    ]
    
    # Imprime a tabela
    pdf.set_font("Arial", size=12)
    for row in table_data:
        for cell in row:
            pdf.cell(col_width, row_height, txt=cell, border=1)
        pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela

    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 5, "O presente documento visa atender as exigências do Art. 26, inciso III, § 1º e 2º, da Lei Estadual nº 5.940/1969 (Lei de Promoção de Praças) sendo os conceitos classificados em:")

    
    # Começo da nova tabela (4 colunas x 1 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 4  # largura da página menos margens dividida por 3
    row_height = 10
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["EXCELENTE", "BOM", "REGULAR", "INSUFICIENTE"],
    ]
    
    # Imprime a tabela
    pdf.set_font("Arial", size=12)
    for row in table_data:
        for cell in row:
            pdf.cell(col_width, row_height, txt=cell, border=1)
        pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela

    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 5, "O presente conceito está sendo emitindo considerando:")

    # Começo da nova tabela (2 colunas x 5 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 2  # largura da página menos margens dividida por 3
    row_height = 10
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["CARÁTER, CONDUTA MILITAR E CIVIL", f"{conceitos[0]}"],
        ["ESPÍRITO MILITAR E POLICIAL", f"{conceitos[1]}"],
        ["CULTURA POLICIAL MILITAR E GERAL", f"{conceitos[2]}"],
        ["APTIDÃO PROFISSIONAL", f"{conceitos[3]}"],
        ["DEDICAÇÃO AO TRABALHO", f"{conceitos[4]}"],
    ]
    # Imprime a tabela
    pdf.set_font("Arial", size=12)
    for row in table_data:
        for cell in row:
            pdf.cell(col_width, row_height, txt=cell, border=1)
        pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela


    pdf.ln(6)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "CONCEITOS:", ln=True)
    pdf.set_font("Arial", '', 12)
    for i, conceito in enumerate(conceitos):
        pdf.cell(0, 8, f"{col_names[i+1]}: {conceito}", ln=True)
    pdf.ln(6)

    # Observações finais / assinatura modelo
    pdf.set_font("Arial", '', 12)
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
