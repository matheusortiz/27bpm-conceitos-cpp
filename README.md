# 27BPM - Geração de Fichas de Conceito (versão 1.2.0)

Resumo
- Script em Python que lê um arquivo `Conceitos.csv` e um arquivo `Efetivo_Avancado.csv` e gera PDFs por militar em `fichas/`.
- Gera a ficha principal e, quando aplicável, uma segunda página de justificativa.

Principais funcionalidades (versão atual)
- Leitura de `Conceitos.csv` com colunas selecionadas para nome e 5 conceitos.
- Leitura de `Efetivo_Avancado.csv` para preencher:
  - graduacao
  - data_promocao
  - funcao_atual
  - cpf
- Busca por nome para fazer lookup entre os dois arquivos.
- Campo NOME/CPF: concatena Nome (do `Conceitos.csv`) + "/" + CPF (do `Efetivo_Avancado.csv`) quando disponível.
- Suporte a colunas opcionais no `Conceitos.csv`:
  - `Comportamento` → substitui a variável comportamento exibida na ficha.
  - `Justificativa SE EXCELENTE` → texto usado na segunda folha quando TODOS os 5 conceitos forem "EXCELENTE".
- Gera segunda página (anexo de justificativa) somente se os cinco conceitos forem "EXCELENTE".
- PDFs salvos em `fichas/ficha_{nome_com_underscores}.pdf`.

Requisitos
- Python 3.8+
- Bibliotecas:
  - pandas
  - fpdf
- Instalação rápida:
  - pip install pandas fpdf

Arquivos esperados e formato
- Conceitos.csv
  - Deve conter, na ordem usada, a coluna de Nome e 5 colunas de conceito (o script já seleciona índices; ajuste `selected_cols` se necessário).
  - Colunas opcionais reconhecidas (case-insensitive): `Comportamento`, `Justificativa SE EXCELENTE`.
- Efetivo_Avancado.csv
  - Deve conter colunas com cabeçalhos (case-insensitive): `Nome`, `Posto/Grad`, `data promocao`, `funcao (atividade)`, `cpf`.
  - Encoding recomendado: latin-1 (padrão no script). Troque para utf-8 se seu CSV estiver assim.

Como executar
- Coloque `Conceitos.csv` e `Efetivo_Avancado.csv` na raiz do projeto.
- Execute:
  - python3 main.py
- Os PDFs serão gerados dentro de `fichas/`.

Observações e notas
- Nomes são comparados ignorando maiúsculas/minúsculas; acentuação é mantida (não há normalização automática de acentos).
- Se uma coluna não existir, o script usa valores padrão e imprime um aviso quando relevante.
- Arquivos gerados e a pasta `fichas/` estão listados no `.gitignore` para não versionar os PDFs.
- Para alterar o comportamento (por exemplo, permitir que o nome quebre em múltiplas linhas em vez de truncar), solicite ajuste no código (posicionamento X/Y com MultiCell).

Changelog sucinto
- v0.2
  - Adicionada concatenação Nome/CPF e ajuste dinâmico da largura da coluna.
  - Suporte às colunas opcionais `Comportamento` e `Justificativa SE EXCELENTE`.
  - Truncamento com reticências em campos longos (nome/cpf e função atual).
  - Segunda folha de justificativa condicionada a todos os conceitos serem "EXCELENTE".

Contato
- Use o repositório para abrir issues / solicitar ajustes no layout ou regras de truncamento.