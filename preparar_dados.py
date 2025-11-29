import wikipedia
import re
import random
from nltk.tokenize import sent_tokenize
import nltk

# Configuração inicial
nltk.download('punkt_tab') # Necessário para separar sentenças em PT
wikipedia.set_lang("pt")
NUM_ARTIGOS = 50  # Aumente para 500+ para um modelo robusto "grande o suficiente" 

print(f"--- Iniciando download de {NUM_ARTIGOS} artigos da Wikipedia PT ---")

corpus_total = []

# 1. Coleta de Dados
try:
    # Pega títulos aleatórios
    titulos = wikipedia.random(pages=NUM_ARTIGOS)
    
    for titulo in titulos:
        try:
            print(f"Baixando: {titulo}")
            page = wikipedia.page(titulo)
            conteudo = page.content
            
            # 2. Limpeza e Normalização 
            # Remove cabeçalhos de seção (ex: == História ==)
            conteudo = re.sub(r'==.*?==+', '', conteudo)
            # Remove quebras de linha múltiplas
            conteudo = re.sub(r'\n+', '\n', conteudo)
            
            # 3. Tokenização de Sentenças
            # O SRILM funciona melhor com uma sentença por linha
            sentencas = sent_tokenize(conteudo, language='portuguese')
            
            for s in sentencas:
                # Limpeza extra: remover espaços extras e lowercase
                s_limpa = s.strip().lower()
                # Filtrar frases muito curtas (ruído)
                if len(s_limpa) > 10:
                    corpus_total.append(s_limpa)
                    
        except wikipedia.exceptions.DisambiguationError:
            continue
        except wikipedia.exceptions.PageError:
            continue
            
except Exception as e:
    print(f"Erro geral: {e}")

# Embaralhar para evitar viés de tópico
random.shuffle(corpus_total)

# 4. Split Treino/Teste (80/20) 
split_idx = int(len(corpus_total) * 0.8)
treino = corpus_total[:split_idx]
teste = corpus_total[split_idx:]

print(f"\nTotal de sentenças processadas: {len(corpus_total)}")
print(f"Sentenças de Treino: {len(treino)}")
print(f"Sentenças de Teste: {len(teste)}")

# Salvar arquivos
with open("treino.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(treino))
    
with open("teste.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(teste))

print("\n--- Arquivos 'treino.txt' e 'teste.txt' gerados com sucesso! ---")
