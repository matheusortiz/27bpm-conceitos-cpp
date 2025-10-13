# Fichas de Avaliação de Militares - Automação Python

Projeto para gerar automaticamente fichas individuais de avaliação em PDF para militares, a partir de uma planilha CSV, permitindo processamento em lote e personalização do modelo da ficha.

## Estrutura

- **Conceitos.csv:** Arquivo de entrada (separado por vírgulas) com dados dos militares.
- **main.py:** Script Python responsável por ler os dados e gerar os PDFs.
- **/venv:** Ambiente virtual Python (não versionado).
- **/fichas:** Pasta na qual são gerados os PDFs individuais para cada militar.

## Requisitos

- Python 3.8 ou superior
- pip
- pandas, fpdf (instalados via pip)

## Instalação

```
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

pip install -r requirements.txt
```

## Uso

1. Coloque o arquivo `Conceitos.csv` na raiz do projeto. Certifique-se de que está separado por vírgulas e que as duas primeiras linhas correspondem ao cabeçalho.
2. Execute o script principal:
    ```
    python main.py
    ```
3. Os PDFs individuais serão gerados na pasta `fichas`, utilizando apenas o nome e os campos "conceito" das colunas A, E, I, M, Q e U do arquivo CSV.

## Personalização

O modelo inicial do PDF contém apenas o nome e os conceitos selecionados.
Para modificar o layout, adicionar ou remover campos, edite o script `main.py` conforme a necessidade.

## Observações

- Esta versão trabalha com CSV para maior portabilidade.
- O arquivo `Conceitos.csv` pode ser substituído por outro, desde que siga a mesma estrutura de cabeçalho.
- A pasta `fichas` será criada automaticamente pelo script, se não existir.
- Os PDFs são gerados automaticamente na pasta `fichas`.