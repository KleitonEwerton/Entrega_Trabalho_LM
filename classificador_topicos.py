import wikipedia
import subprocess
import os
import nltk
from nltk.tokenize import sent_tokenize

# Configuração
nltk.download('punkt_tab')
wikipedia.set_lang("pt")

topicos = {
    "esporte": ["Futebol", "Vôlei", "Basquete", "Olimpíadas", "Neymar", "Ginástica"],
    "musica": ["Rock", "Jazz", "Mozart", "Guitarra", "Beatles", "Sinfonia"]
}

def preparar_lm_topico(nome, keywords):
    print(f"\n[Treinando] Coletando dados para: {nome.upper()}...")
    texto_completo = []
    for key in keywords:
        try:
            p = wikipedia.page(key)
            sents = sent_tokenize(p.content.lower())
            texto_completo.extend(sents)
        except: continue
    
    arquivo_txt = f"{nome}.txt"
    arquivo_lm = f"{nome}.lm"
    
    with open(arquivo_txt, "w") as f:
        f.write("\n".join(texto_completo))
        
    # Treinar LM (usando SRILM via subprocess)
    # Usando add-one smoothing para ser rápido e evitar zeros
    cmd = f"ngram-count -text {arquivo_txt} -order 3 -addsmooth 1 -lm {arquivo_lm}"
    subprocess.run(cmd, shell=True, check=True)
    print(f"Modelo {arquivo_lm} gerado com {len(texto_completo)} frases.")
    return arquivo_lm

def classificar_frase(frase, lm_a, lm_b, nome_a, nome_b):
    with open("temp_class.txt", "w") as f: f.write(frase.lower())
    
    def get_ppl(lm):
        cmd = f"ngram -lm {lm} -ppl temp_class.txt"
        try:
            res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
            import re
            m = re.search(r'ppl= ([0-9.]+)', res)
            return float(m.group(1)) if m else float('inf')
        except: return float('inf')

    ppl_a = get_ppl(lm_a)
    ppl_b = get_ppl(lm_b)
    
    vencedor = nome_a if ppl_a < ppl_b else nome_b
    return vencedor, ppl_a, ppl_b

# --- Main ---
lm_esporte = preparar_lm_topico("esporte", topicos["esporte"])
lm_musica = preparar_lm_topico("musica", topicos["musica"])

print("\n--- Teste do Classificador ---")
frases_teste = [
    "O jogador chutou a bola no gol",      # Esperado: Esporte
    "O guitarrista tocou um solo incrível", # Esperado: Musica
    "A orquestra sinfônica se apresentou",  # Esperado: Musica
    "O juiz apitou o final da partida"      # Esperado: Esporte
]

for f in frases_teste:
    classe, pa, pb = classificar_frase(f, lm_esporte, lm_musica, "Esporte", "Música")
    print(f"Frase: '{f}'")
    print(f"   PPL Esporte: {pa:.2f} | PPL Música: {pb:.2f} -> Classificado como: {classe.upper()}")
