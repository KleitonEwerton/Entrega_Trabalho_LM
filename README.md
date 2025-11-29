# Modelos de Linguagem com SRILM - Experimentos e Análise

Este repositório contém os scripts e logs dos experimentos realizados para a disciplina de Modelos de Linguagem. O projeto foca na análise do impacto de diferentes métodos de suavização (Smoothing) em corpora esparsos de língua portuguesa.

**Aluno:** Kleiton Ewerton
**Data:** Novembro/2025

## 📂 Estrutura do Projeto

* `src/` (ou raiz): Scripts Python para ETL e avaliação.
* `imagens/`: Prints do terminal utilizados no relatório para comprovar a execução.
* `results/`: Logs de saída do SRILM e prints comprobatórios.
* `treino.txt` / `teste.txt`: Corpus gerado a partir da Wikipedia PT.

## 🛠️ Pré-requisitos

1. **SRILM Toolkit:** Deve estar instalado e configurado no PATH.
   * Compilado com `MACHINE_TYPE=i686-m64`.
2. **Python 3.8+**
3. **Dependências Python:**
   ```bash
   pip install -r requirements.txt
## 🚀 Como Executar

Abaixo estão as instruções para reproduzir o pipeline de dados, treinamento e avaliação.

### 1. Preparação dos Dados (ETL)
O script baixa artigos da Wikipedia, normaliza o texto e realiza o *split* rigoroso (80/20). Se desejar gerar novos dados:

```bash
python3 preparar_dados.py
```

### 2. Experimentos de Perplexidade (SRILM)
Exemplos de comandos utilizados para treinar modelos e avaliar a Perplexidade (PPL).

Baseline (Sem suavização):

```bash
ngram-count -text treino.txt -order 3 -addsmooth 0 -lm baseline.lm
```
ngram -lm baseline.lm -ppl teste.txt
Melhor Modelo (Kneser-Ney):

```bash
ngram-count -text treino.txt -order 3 -kndiscount -lm kneser.lm
ngram -lm kneser.lm -ppl teste.txt
```
### 3. Scripts de Avaliação Empírica
Visualização de Shannon (Geração de Frases): Gera sentenças aleatórias baseadas nas probabilidades de n-grams do modelo treinado.

```bash
python3 shannon_viz.py
```
Teste de Acurácia (Good vs Bad Sentences): Verifica se o modelo atribui menor perplexidade (maior probabilidade) a frases gramaticalmente corretas em comparação a frases sem sentido.

```bash
python3 avaliacao_empirica.py
```
Classificador de Tópicos (Extra): Demonstração de classificação de texto (Esporte vs. Música) via comparação de Perplexidade.

```bash
python3 classificador_topicos.py
```
## 📦 Conteúdo do Pacote de Entrega
A estrutura deste diretório de entrega está organizada da seguinte forma:

### Scripts Python (.py):

 - preparar_dados.py: ETL e limpeza de dados.

 - shannon_viz.py: Gerador de texto.

 - avaliacao_empirica.py: Validação de acurácia.

 - classificador_topicos.py: Experimento extra de classificação.

### Configuração:

 - requirements.txt: Lista de dependências Python (instalar com pip install -r requirements.txt).

 - README.md: Este arquivo de documentação.

 - Evidências e Logs (.txt):

 - resultado_*.txt: Logs contendo as saídas do terminal com valores de Perplexidade e ZeroProbs.

### Figuras:

Prints do terminal utilizados no relatório para comprovar a execução.

### Documentação Final:

Relatorio.pdf: Relatório técnico completo (gerado via LaTeX/Overleaf).
