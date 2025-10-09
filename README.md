# Fichas de Avaliação de Militares - Automação Python

Projeto para gerar automaticamente fichas individuais de avaliação em PDF para militares, a partir de uma planilha Excel, facilitando o processamento em lote e a personalização do modelo de ficha.

## Estrutura

- **dados.xlsx:** Arquivo de entrada com dados dos militares.
- **main.py:** Script Python principal responsável pela leitura dos dados e geração dos PDFs.
- **/venv:** Ambiente virtual Python (não versionado).
- **ficha_nome.pdf:** Arquivos de saída gerados para cada militar.

## Requisitos

- Python 3.8 ou superior
- pip
- Pandas, Openpyxl, FPDF (instalados via pip)

## Instalação

```
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

## Uso

1. Coloque o arquivo `dados.xlsx` na raiz do projeto.
2. Execute o script principal:
    ```
    python main.py
    ```
3. Os PDFs individuais serão gerados para cada militar usando os dados das colunas de interesse da planilha.

## Personalização

O modelo de saída inicial é básico (informações em lista).
Para modificar o layout ou incluir novos campos, ajuste a estrutura do PDF no script `main.py`.

## Observações

- Versão inicial para testes. Futuramente será possível adaptar o modelo do PDF conforme o padrão institucional.
- O arquivo `dados.xlsx` pode ser substituído por outro com a mesma estrutura de cabeçalho.
- Os PDFs são gerados no mesmo diretório.

