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

# detecta colunas opcionais no Conceitos.csv
col_comportamento = None
col_just_ex = None
for c in df.columns:
    n = str(c).strip().lower()
    if n == 'comportamento':
        col_comportamento = c
    if n == 'justificativa se excelente' or n == 'justificativa_se_excellent' or n == 'justificativa_se_excelente':
        col_just_ex = c

# carrega dados do efetivo para preencher graduacao / data_promocao / funcao_atual
try:
    # CSV salvo a partir do Excel — usar latin-1 para preservar acentuação conservadora
    df_efetivo = pd.read_csv('Efetivo_Avancado.csv', dtype=str, encoding='latin-1')
    df_efetivo = df_efetivo.fillna('').copy()
except FileNotFoundError:
    print("Aviso: Efetivo_Avancado.csv não encontrado. Campos permanecerão com valores padrão.")
    df_efetivo = None

# monta lookup case-insensitive por 'Nome' (se possível)
lookup_efetivo = None
if df_efetivo is not None:
    def find_col(name):
        for c in df_efetivo.columns:
            if str(c).strip().lower() == name.lower():
                return c
        return None

    col_nome = find_col('Nome')
    col_posto = find_col('Posto/Grad')
    col_data = find_col('data promocao')
    col_funcao = find_col('funcao (atividade)')
    col_cpf = find_col('cpf')

    if col_nome is None:
        print("Aviso: coluna 'Nome' não encontrada em Efetivo_Avancado.csv — lookup desabilitado.")
    else:
        lookup_efetivo = {}
        for _, r in df_efetivo.iterrows():
            key = str(r[col_nome]).strip().casefold()
            lookup_efetivo[key] = {
                'graduacao': str(r[col_posto]).strip() if col_posto else '',
                'data_promocao': str(r[col_data]).strip() if col_data else '',
                'funcao_atual': str(r[col_funcao]).strip() if col_funcao else '',
                'cpf': str(r[col_cpf]).strip() if col_cpf else '',
            }

for idx, row in df_selected.iterrows():
    nome = row.iloc[0]
    conceitos = [row.iloc[i] for i in range(1, len(row))]

    # valores padrão (mantidos caso não encontre no CSV)
    graduacao = "não informada"
    comportamento = "não informado"
    data_promocao = "não informada"
    funcao_atual = "não informada"
    cpf = ""
    # justificativa padrão (usada se não houver coluna específica)
    justificativa_padrao = ("Justificativa não informada")
    justificativa_ex = justificativa_padrao

    # pega valores extras diretamente do df original (se as colunas existirem)
    # usamos df (com todas as colunas) e o índice idx correspondente
    try:
        orig_row = df.iloc[idx]
        if col_comportamento:
            comportamento = str(orig_row[col_comportamento]).strip() or comportamento
        if col_just_ex:
            j = str(orig_row[col_just_ex]).strip()
            if j:
                justificativa_ex = j
    except Exception:
        # se algo falhar, mantemos os padrões
        pass

    # tenta buscar no Efetivo_Avancado.csv (match case-insensitive)
    if lookup_efetivo is not None:
        info = lookup_efetivo.get(str(nome).strip().casefold())
        if info:
            graduacao = info.get('graduacao') or graduacao
            data_promocao = info.get('data_promocao') or data_promocao
            funcao_atual = info.get('funcao_atual') or funcao_atual
            cpf = info.get('cpf') or cpf

    # concatena NOME/CPF para exibição (se cpf vazio exibe só o nome)
    nome_cpf = f"{nome}/{cpf}" if cpf else str(nome)

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

    # Começo da nova tabela (3 colunas x 2 linhas) - largura dinâmica do NOME/CPF (ajusta com CPF)
    page_width = pdf.w - 2 * pdf.l_margin
    default_font_size = 12

    name_text = str(nome_cpf)
    # calcula largura necessária para o nome+cpf (com pequena margem)
    font_size = default_font_size
    pdf.set_font("Arial", 'B', font_size)
    name_width_needed = pdf.get_string_width(name_text) + 6
    max_name_frac = 0.60  # percentual máximo da largura da página para o nome (reduzido para dar espaço ao CPF)
    max_name_w = page_width * max_name_frac

    # reduz fonte se o nome for muito longo
    while name_width_needed > max_name_w and font_size > 6:
        font_size -= 1
        pdf.set_font("Arial", 'B', font_size)
        name_width_needed = pdf.get_string_width(name_text) + 6

    # se ainda não couber, trunca com reticências
    if name_width_needed > max_name_w:
        # corta até caber (mantendo algumas letras)
        truncated = name_text
        while pdf.get_string_width(truncated + '...') + 6 > max_name_w and len(truncated) > 4:
            truncated = truncated[:-1]
        name_text = truncated.rstrip() + '...'
        name_width_needed = pdf.get_string_width(name_text) + 6
        # mantém a fonte atual (mínima)

    # define larguras das colunas
    name_col_w = min(name_width_needed, max_name_w)
    remaining = page_width - name_col_w
    col2_w = col3_w = remaining / 2
    row_height = 6

    # Cabeçalhos da tabela
    pdf.set_font("Arial", 'B', font_size-1)
    headers = ["NOME/CPF", "GRADUAÇÃO", "COMPORTAMENTO"]
    widths = [name_col_w, col2_w, col3_w]
    for i, h in enumerate(headers):
        pdf.cell(widths[i], row_height, txt=h, border=1)
    pdf.ln(row_height)

    # Conteúdo da linha (ajusta fonte normal)
    pdf.set_font("Arial", size=max(font_size, 8))
    cells = [name_text, f"{graduacao}", f"{comportamento}"]
    for i, c in enumerate(cells):
        pdf.cell(widths[i], row_height, txt=c, border=1)
    pdf.ln(row_height)
    
    pdf.ln(5)  # Espaço após tabela

    # Começo da nova tabela (2 colunas x 2 linhas)
    col_width = (pdf.w - 2 * pdf.l_margin) / 2
    row_height = 6

    # Dados da tabela
    table_data = [
        ["DATA DA ÚLTIMA PROMOÇÃO", "FUNÇÃO QUE EXERCE ATUALMENTE"],
        [f"{data_promocao}", f"{funcao_atual}"],
    ]

    # helper para truncar texto com reticências até caber na largura
    def fit_text(text, pdf_obj, max_width, ellipsis='...'):
        text = str(text)
        if pdf_obj.get_string_width(text) <= max_width:
            return text
        # remove caracteres até caber com ellipsis
        # mantém ao menos alguns caracteres
        while pdf_obj.get_string_width(text + ellipsis) > max_width and len(text) > 3:
            text = text[:-1]
        return (text.rstrip() + ellipsis) if text else ellipsis

    pdf.set_font("Arial", size=11)
    padding = 4  # pequeno padding interno
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            # largura máxima utilizável para texto dentro da célula
            max_text_w = col_width - padding
            # aplica truncamento apenas no conteúdo (não nas células de cabeçalho)
            txt = fit_text(cell, pdf, max_text_w)
            pdf.cell(col_width, row_height, txt=txt, border=1)
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
        pdf.multi_cell(0, 5, justificativa_ex)
    
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
