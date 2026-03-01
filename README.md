# Exercício de agente

## Requisitos:

```
python 3.12
```

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Depois, copie o arquivo `.env.sample` para `.env` para configurar seu ambiente local. No arquivo `.env`, coloque sua chave de acesso a API (OpenAI, Gemini, etc). Além disso, indique `BASE_PATH` que será o caminho base e isso serve para criar uma espécie de sandbox e garantir que o agente modifique apenas o que estiver a partir de `BASE_PATH`. Um exemplo:
```
BASE_PATH="/home/joaozinho/minha_pasta_descartavel"
```
No exemplo acima, apenas arquivos e diretórios dentro de `minha_pasta_descartavel` serão manipulados. Você também pode rodar a aplicação num container Docker, é mais seguro.

## Para rodar

```
python main.py
```

## Execução

Caso queira ver a aplicação rodando, veja [o vídeo com um teste](./sample.webm).

## Estrutura

A pasta `project/.hidden-folder` simula umm diretório que deve ser ignorado. Dessa forma, quando for pedido ao agente para listar os arquivos de uma pasta, `.hidden-folder` não deve aparecer.
