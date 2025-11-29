import random
import math

def carregar_modelo_arpa(arquivo_lm):
    """Lê um arquivo .lm (ARPA format) e carrega unigramas e bigramas simples."""
    modelo = {}
    lendo_secao = None
    
    print(f"Carregando {arquivo_lm}...")
    with open(arquivo_lm, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            linha = linha.strip()
            if linha == '\\1-grams:': lendo_secao = 1; continue
            if linha == '\\2-grams:': lendo_secao = 2; continue
            if linha == '\\3-grams:': lendo_secao = 3; continue
            if linha.startswith('\\end\\'): break
            if not linha or linha.startswith('\\'): continue

            partes = linha.split('\t')
            if len(partes) < 2: continue
            
            log_prob = float(partes[0])
            termo = partes[1]
            
            # Converter Log10 para Probabilidade real
            prob = 10 ** log_prob
            
            if lendo_secao == 1:
                # Unigramas: termo -> prob
                if 'unigrams' not in modelo: modelo['unigrams'] = []
                modelo['unigrams'].append((termo, prob))
            elif lendo_secao == 2:
                # Bigramas: palavra_anterior -> [(proxima_palavra, prob), ...]
                palavras = termo.split()
                if len(palavras) == 2:
                    contexto, proxima = palavras[0], palavras[1]
                    if contexto not in modelo: modelo[contexto] = []
                    modelo[contexto].append((proxima, prob))
    return modelo

def gerar_frase(modelo, inicio=None, max_len=20):
    frase = []
    
    # 1. Escolher palavra inicial
    if inicio:
        atual = inicio
        frase.append(atual)
    else:
        # Começa com <s> (início de sentença)
        atual = '<s>'
    
    for _ in range(max_len):
        if atual == '</s>': break
        
        # Tenta achar continuacoes baseadas no bigrama (Markov Chain)
        candidatos = modelo.get(atual)
        
        if candidatos:
            palavras = [c[0] for c in candidatos]
            probs = [c[1] for c in candidatos]
            # Normalizar probabilidades para somar 1 (simplificação para amostragem)
            total = sum(probs)
            probs_norm = [p/total for p in probs]
            
            proxima = random.choices(palavras, weights=probs_norm, k=1)[0]
        else:
            # Backoff simplificado: se não tem bigrama, pega um unigrama aleatório
            # (Numa implementação completa, usaria os pesos de backoff do arquivo)
            proxima = random.choice(modelo['unigrams'])[0]
        
        if proxima == '</s>':
            break
        if proxima != '<s>':
            frase.append(proxima)
        atual = proxima
        
    return " ".join(frase)

# --- Execução ---
# Use o modelo Kneser-Ney (melhor resultado)
arquivo_modelo = 'kneser.lm' 
modelo = carregar_modelo_arpa(arquivo_modelo)

print("\n--- Visualização de Shannon (Gerador de Frases) ---")
print("Gerando 5 frases aleatórias:")
for i in range(5):
    print(f"{i+1}. {gerar_frase(modelo)}")

print("\nGerando frases com início forçado ('o', 'a', 'foi'):")
for s in ['o', 'a', 'foi']:
    print(f"Início '{s}': {gerar_frase(modelo, inicio=s)}")
