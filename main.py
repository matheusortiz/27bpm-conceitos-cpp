import pandas as pd
from fpdf import FPDF

# Carregar a planilha, pular cabeçalho (duas primeiras linhas)
df = pd.read_excel('dados.xlsx', skiprows=2)

# Selecionar as colunas relevantes (A, E, I, M, Q, U são índices 0, 4, 8, 12, 16, 20)
selected_cols = [0, 4, 8, 12, 16, 20]
col_names = df.columns[selected_cols]
df_selected = df.iloc[:, selected_cols]

for idx, row in df_selected.iterrows():
    nome = row.iloc[0]  # Coluna A
    # Montar conteúdo lista
    conteudo = [f"{col_names[i]}: {row.iloc[i]}" for i in range(1, len(row))]
    conteudo_str = "\n".join(conteudo)
    
    # Gerar PDF simples
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ficha de Avaliação: {nome}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for line in conteudo:
        pdf.cell(0, 10, txt=line, ln=True)
    pdf.output(f"ficha_{nome.replace(' ','_')}.pdf")

print("PDFs gerados.")
