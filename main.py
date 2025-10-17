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
    pdf.cell(0, 5, "POLÍCIA MILITAR DO PARANÁ", ln=True, align='C')
    pdf.cell(0, 5, "4º COMANDO REGIONAL", ln=True, align='C')
    pdf.cell(0, 5, "27º BATALHÃO DE POLÍCIA MILITAR", ln=True, align='C')
    pdf.ln(4)
    pdf.set_font("Arial", 'BU', 12)
    pdf.cell(0, 7, "FICHA DE INFORMAÇÃO E AVALIAÇÃO DE CONCEITO DE PRAÇA", ln=True, align='C')
    pdf.ln(4)

    # Começo da nova tabela (3 colunas x 2 linhas) - largura dinâmica do NOME
    page_width = pdf.w - 2 * pdf.l_margin
    default_font_size = 12
    pdf.set_font("Arial", 'B', default_font_size)
    # calcula largura necessária para o nome (com pequena margem)
    name_width_needed = pdf.get_string_width(str(nome)) + 6
    max_name_frac = 0.7  # no máximo 70% da largura da página para o nome
    max_name_w = page_width * max_name_frac

    # reduz fonte se o nome for muito longo
    font_size = default_font_size
    pdf.set_font("Arial", 'B', font_size)
    while name_width_needed > max_name_w and font_size > 6:
        font_size -= 1
        pdf.set_font("Arial", 'B', font_size)
        name_width_needed = pdf.get_string_width(str(nome)) + 6

    # define larguras das colunas
    name_col_w = min(name_width_needed, max_name_w)
    remaining = page_width - name_col_w
    col2_w = col3_w = remaining / 2
    row_height = 6

    # Cabeçalhos da tabela
    pdf.set_font("Arial", 'B', font_size)
    headers = ["NOME/CPF", "GRADUAÇÃO", "COMPORTAMENTO"]
    widths = [name_col_w, col2_w, col3_w]
    for i, h in enumerate(headers):
        pdf.cell(widths[i], row_height, txt=h, border=1)
    pdf.ln(row_height)

    # Conteúdo da linha (ajusta fonte normal)
    pdf.set_font("Arial", size=font_size)
    cells = [f"{nome}", f"{graduacao}", f"{comportamento}"]
    for i, c in enumerate(cells):
        pdf.cell(widths[i], row_height, txt=c, border=1)
    pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela

    # Começo da nova tabela (2 colunas x 2 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 2  # largura da página menos margens dividida por 3
    row_height = 6
    
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
    row_height = 6
    
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
    row_height = 6
    
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

    pdf.set_font("Arial", 'BU', 12)
    pdf.cell(0, 8, "Observações importantes: ", ln=True)

    if len(conceitos) >= 5 and all(str(c).strip().upper() == 'EXCELENTE' for c in conceitos):
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 5, "Segue anexo cópia da FICHA DISCIPLINAR INDIVIDUAL devidamente autenticada pelo Oficial Chefe da SJD da unidade.")
        pdf.multi_cell(0, 5, "Segue também anexo, a justificativa circunstanciada considerando o conceito EXCELENTE atribuído ao militar.")

    pdf.set_font("Arial", 'B', 12)
    hoje = datetime.today().strftime('%d/%m/%Y')
    pdf.cell(0, 8, f"Data: {hoje}", ln=True)
    pdf.ln(8)
    pdf.cell(0, 5, "_____________________________________________", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 5, "Ten.- Cel. QOEM PM Luiz Antonio Ferreira Junior,", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 5, "Comandante do 27º BPM/4º CRPM", ln=True, align='C')

    # Começo da nova tabela
    col_width = (pdf.w - 2 * pdf.l_margin)  # largura da página menos margens dividida por 3
    row_height = 6
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["Situação Processual"],
        ["Está SUB-JUDICE  (  ) 		NADA CONSTA   ( X )"],
        ["Observações: "],
    ]

    # Imprime a tabela
    pdf.set_font("Times", 'B', size=12)  # Mudando para Times New Roman
    for i, row in enumerate(table_data):
        for cell in row:
            if i == 0:  # Primeira linha
                pdf.cell(col_width, row_height, txt=cell, border='TLR', align='C')  # Centralizado
            elif i == len(table_data)-1:  # Última linha
                pdf.cell(col_width, row_height, txt=cell, border='BLR')
            else:  # Linhas do meio
                pdf.cell(col_width, row_height, txt=cell, border='LR', align='C')  # Centralizado
        pdf.ln(row_height)

    pdf.ln(5)  # Espaço após tabela


    # Começo da nova tabela
    col_width = (pdf.w - 2 * pdf.l_margin)  # largura da página menos margens dividida por 3
    row_height = 6
    
    # Dados da tabela (3 col x 2 lin)
    table_data = [
        ["ESTÁ RESPONDENDO A CONSELHO DE DISCIPLINA OU CONSELHO DE JUSTIFICAÇÃO?"],
        ["SIM (  )		NÃO (  X   )"],
    ]

    # Imprime a tabela
    pdf.set_font("Times", 'B', size=10)  # Mudando para Times New Roman
    for i, row in enumerate(table_data):
        for cell in row:
            if i == 0:  # Primeira linha
                pdf.cell(col_width, row_height, txt=cell, border='TLR', align='C')  # Centralizado
            elif i == len(table_data)-1:  # Última linha
                pdf.cell(col_width, row_height, txt=cell, border='BLR', align='C')  # Centralizado
        pdf.ln(row_height)

    pdf.ln(5)  # Espaço após tabela

    pdf.set_font("Arial", 'B', 12)
    hoje = datetime.today().strftime('%d/%m/%Y')
    pdf.cell(0, 8, f"Data: {hoje}", ln=True)
    pdf.ln(8)
    pdf.cell(0, 8, "_____________________________________________", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 5, "1º Ten. QOEM PM Alaor Elias de Faria Junior,", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 5, "Resp. p/ Chefia da SJD do 27º BPM/4º CRPM", ln=True, align='C')

    pdf.ln(6)

    # segunda folha (anexo de justificativa) — somente se todos os conceitos forem "EXCELENTE"
    if len(conceitos) >= 5 and all(str(c).strip().upper() == 'EXCELENTE' for c in conceitos):
        pdf.add_page()
        pdf.set_font("Arial", 'BU', 12)
        pdf.cell(0, 5, "ANEXO A FICHA DE INFORMAÇÃO E AVALIAÇÃO DE CONCEITO", ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 5, f"({nome})", ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "JUSTIFICATIVA QUANTO AO CONCEITO EXCELENTE:", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 5, "Excelente Policial Militar dedicado e comprometido com a função que exerce, possui senso de responsabilidade, é disciplinado e educado, além de pontual. Apresenta iniciativa para as atividades inerentes ao bom andamento do serviço, busca soluções para os problemas quando apresentados. Demonstra-se sempre pronto para o serviço, preocupando-se em bem executá-lo. Dentro das suas funções, demonstra habilidade e eficiência. Possui postura ilibada na sociedade em que convive, representando bem a PMPR.")
    
        pdf.ln(6)
    
        MESES = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
    
        hoje = datetime.today()
        data_formatada = f"União da Vitória, {hoje.day} de {MESES[hoje.month]} de {hoje.year}."
    
        pdf.cell(0, 8, f"{data_formatada}", ln=True, align='C')
        pdf.ln(8)
        pdf.cell(0, 5, "_____________________________________________", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 5, "Ten.- Cel. QOEM PM Luiz Antonio Ferreira Junior,", ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 5, "Comandante do 27º BPM/4º CRPM", ln=True, align='C')


    # Salva PDF
    filename = f"fichas/ficha_{nome.replace(' ','_')}.pdf"
    pdf.output(filename)

print("PDFs gerados no padrão solicitado!")
