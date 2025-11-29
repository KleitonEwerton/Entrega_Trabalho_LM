import subprocess

# Defina pares de frases (Correta vs Errada)
pares_teste = [
    ("o menino jogou a bola", "bola menino a jogou o"), # Gramática quebrada
    ("a vida é bela", "a vida é cadeira"),              # Semântica quebrada
    ("hoje o dia está lindo", "lindo está dia o hoje"), # Ordem inversa
    ("eu gosto de programar em python", "python de em gosto programar eu")
]

modelo = "kneser.lm" # Seu melhor modelo

print(f"--- Avaliação Empírica: Acurácia do Modelo {modelo} ---")
acertos = 0

for i, (frase_boa, frase_ruim) in enumerate(pares_teste):
    # Criar arquivos temporários para o SRILM ler
    with open("temp_boa.txt", "w") as f: f.write(frase_boa)
    with open("temp_ruim.txt", "w") as f: f.write(frase_ruim)
    
    # Função auxiliar para pegar PPL
    def get_ppl(arquivo):
        cmd = f"ngram -lm {modelo} -ppl {arquivo}"
        resultado = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        # Parsear o valor de ppl= X
        import re
        match = re.search(r'ppl= ([0-9.]+)', resultado)
        return float(match.group(1)) if match else float('inf')

    try:
        ppl_boa = get_ppl("temp_boa.txt")
        ppl_ruim = get_ppl("temp_ruim.txt")
        
        # O modelo acerta se PPL(Boa) < PPL(Ruim)
        venceu = ppl_boa < ppl_ruim
        if venceu: acertos += 1
        
        print(f"\nPar {i+1}:")
        print(f"  [Boa] '{frase_boa}' -> PPL: {ppl_boa}")
        print(f"  [Ruim] '{frase_ruim}' -> PPL: {ppl_ruim}")
        print(f"  Resultado: {'ACERTOU' if venceu else 'ERROU'}")
        
    except Exception as e:
        print(f"Erro ao processar par {i}: {e}")

acuracia = (acertos / len(pares_teste)) * 100
print(f"\n>>> Acurácia Final: {acuracia}%")
