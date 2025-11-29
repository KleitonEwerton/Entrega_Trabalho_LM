# Modelos de Linguagem com SRILM - Experimentos e Análise

Este repositório contém os scripts e logs dos experimentos realizados para a disciplina de Modelos de Linguagem. O projeto foca na análise do impacto de diferentes métodos de suavização (Smoothing) em corpora esparsos de língua portuguesa.

**Aluno:** Kleiton Ewerton
**Data:** Novembro/2025

## 📂 Estrutura do Projeto

* `src/` (ou raiz): Scripts Python para ETL e avaliação.
* `results/`: Logs de saída do SRILM e prints comprobatórios.
* `treino.txt` / `teste.txt`: Corpus gerado a partir da Wikipedia PT.

## 🛠️ Pré-requisitos

1. **SRILM Toolkit:** Deve estar instalado e configurado no PATH.
   * Compilado com `MACHINE_TYPE=i686-m64`.
2. **Python 3.8+**
3. **Dependências Python:**
   ```bash
   pip install -r requirements.txt