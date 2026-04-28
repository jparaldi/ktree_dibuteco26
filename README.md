# ktree_dibuteco26

## TP1 - Geometria Computacional (KD-Tree)

Um repositório para o trabalho prático de Algoritmos II - UFMG 2026/1.

## Sobre o trabalho

Este projeto foi desenvolvido para a disciplina de **Algoritmos 2 (DCC207 - UFMG)**.

O objetivo é implementar um sistema interativo para visualização de bares participantes do *Comida di Buteco 2026* em Belo Horizonte.

O sistema permite:

* Buscar bares a partir de um endereço informado pelo usuário
* Definir uma região retangular de interesse
* Filtrar os bares dentro dessa região
* Ordenar os resultados por distância
* Visualizar os bares em um mapa interativo

A estrutura de dados principal utilizada é uma **árvore k-dimensional (k-d tree)**, aplicada para realizar buscas espaciais eficientes.

---

## Tecnologias utilizadas

* Python
* KD-Tree (implementação própria)
* Dash + Dash Leaflet (visualização)
* OpenStreetMap (geocoding)
* Pandas (manipulação de dados)

---

## Gerenciamento de dependências com uv

Este projeto utiliza o **uv** para gerenciamento de ambiente e dependências.

### Instalação do ambiente

Após clonar o repositório:

```bash
uv sync
```

Isso irá:

* Criar o ambiente virtual automaticamente
* Instalar todas as dependências com base no arquivo `uv.lock`

## Status

Projeto em desenvolvimento.

## Pipeline pra Organização

Bloco 1 — Dados

Objetivo: transformar CSV cru → dados utilizáveis

 Implementar csv_loader.py
 Ler CSV com sep=';'
 Limpar strings (espaços, etc.)
 Garantir que não tem linhas quebradas
 Criar estrutura intermediária (dict ou lista)

Bloco 2 — Geocoding

Objetivo: endereço → coordenadas

 Implementar geocoding.py
 Integrar com OpenStreetMap (geopy)
 Converter endereços em lat/lon
 Salvar bares_geocoded.csv
 Tratar erros (endereço inválido)

Bloco 3 — KD-Tree

Objetivo: estrutura de dados

 Implementar Node
 Construção da árvore
 Implementar busca ortogonal (retângulo)
 Testar com dados pequenos

Bloco 4 — Distância e ordenação
 Implementar cálculo de distância
 Ordenar resultados por proximidade

Bloco 5 — Integração
 Conectar dados → kd-tree
 Executar busca com dados reais
 Validar resultados

Bloco 6 — Interface
 Criar app com Dash
 Input de endereço
 Renderizar mapa (Leaflet)
 Mostrar tabela
 Sincronizar mapa + tabela

Bloco 7 — Extra (se sobrar tempo)
 Busca circular (raio)
 Melhorias visuais
