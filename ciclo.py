#!/usr/bin/env python3
"""
🔄 CICLO AUTOMÁTICO DE SCRIPTS
Executa tex.py → dat.py → com.py em loop contínuo
"""

import subprocess
import sys
import time
import os
import signal
from datetime import datetime

# ──────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────
SCRIPTS = [
    {"arquivo": "tex.py",  "nome": "Gerador de GUID",        "emoji": "🆔"},
    {"arquivo": "dat.py",  "nome": "Alterador de Data +1",   "emoji": "📅"},
    {"arquivo": "com.py",  "nome": "Commit & Push Automático","emoji": "📤"},
]

PAUSA_ENTRE_SCRIPTS = 3   # segundos entre cada script
PAUSA_ENTRE_CICLOS  = 10  # segundos entre cada ciclo completo
MAX_CICLOS          = 0   # 0 = infinito

# ──────────────────────────────────────────────
# CONTROLE DE INTERRUPÇÃO
# ──────────────────────────────────────────────
executando = True

def sinal_encerrar(sig, frame):
    global executando
    print("\n\n⛔  Interrompido pelo usuário. Encerrando após ciclo atual...\n")
    executando = False

signal.signal(signal.SIGINT, sinal_encerrar)

# ──────────────────────────────────────────────
# UTILITÁRIOS
# ──────────────────────────────────────────────
def linha(char="─", n=52):
    return char * n

def hora():
    return datetime.now().strftime("%H:%M:%S")

def cabecalho():
    print("\n" + linha("═"))
    print("  🔄  CICLO AUTOMÁTICO DE SCRIPTS")
    print(linha("═"))
    print(f"  Scripts configurados : {len(SCRIPTS)}")
    print(f"  Pausa entre scripts  : {PAUSA_ENTRE_SCRIPTS}s")
    print(f"  Pausa entre ciclos   : {PAUSA_ENTRE_CICLOS}s")
    print(f"  Máx. ciclos          : {'∞' if MAX_CICLOS == 0 else MAX_CICLOS}")
    print(linha("═"))
    print("  Pressione Ctrl+C para parar\n")

def executar_script(script_info, numero):
    arquivo = script_info["arquivo"]
    nome    = script_info["nome"]
    emoji   = script_info["emoji"]

    print(f"\n  {emoji}  [{hora()}] Script {numero}/{len(SCRIPTS)}: {nome}")
    print(f"  {linha('-', 48)}")

    if not os.path.exists(arquivo):
        print(f"  ⚠️   Arquivo '{arquivo}' não encontrado! Pulando...")
        return False

    try:
        resultado = subprocess.run(
            [sys.executable, arquivo],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

        # Exibir saída com indentação
        if resultado.stdout:
            for linha_saida in resultado.stdout.strip().splitlines():
                print(f"     {linha_saida}")

        if resultado.stderr:
            print(f"  ⚠️   STDERR:")
            for linha_err in resultado.stderr.strip().splitlines():
                print(f"     {linha_err}")

        if resultado.returncode == 0:
            print(f"\n  ✅  Concluído com sucesso! (código {resultado.returncode})")
            return True
        else:
            print(f"\n  ❌  Falhou! (código {resultado.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print(f"  ⏱️   Timeout! Script demorou mais de 60s.")
        return False
    except Exception as e:
        print(f"  ❌  Erro inesperado: {e}")
        return False

def aguardar(segundos, mensagem):
    """Aguarda com contagem regressiva visível"""
    for i in range(segundos, 0, -1):
        print(f"\r  ⏳  {mensagem} ({i}s)... ", end="", flush=True)
        time.sleep(1)
        if not executando:
            break
    print()

# ──────────────────────────────────────────────
# LOOP PRINCIPAL
# ──────────────────────────────────────────────
def main():
    cabecalho()

    ciclo      = 0
    total_ok   = 0
    total_fail = 0

    while executando:
        ciclo += 1

        if MAX_CICLOS > 0 and ciclo > MAX_CICLOS:
            print(f"\n🏁  Limite de {MAX_CICLOS} ciclo(s) atingido. Encerrando.")
            break

        print(f"\n{'═'*52}")
        print(f"  🔁  CICLO #{ciclo}   [{hora()}]")
        print(f"{'═'*52}")

        resultados = []

        for i, script in enumerate(SCRIPTS, start=1):
            if not executando:
                break

            sucesso = executar_script(script, i)
            resultados.append(sucesso)

            if sucesso:
                total_ok += 1
            else:
                total_fail += 1

            # Pausa entre scripts (exceto após o último)
            if i < len(SCRIPTS) and executando:
                aguardar(PAUSA_ENTRE_SCRIPTS, f"Próximo script em")

        # Resumo do ciclo
        ok   = sum(1 for r in resultados if r)
        fail = sum(1 for r in resultados if not r)
        print(f"\n  {linha('─', 48)}")
        print(f"  📊  Ciclo #{ciclo} finalizado: ✅ {ok} ok  |  ❌ {fail} falhas")
        print(f"  {linha('─', 48)}")

        if not executando:
            break

        # Pausa entre ciclos
        aguardar(PAUSA_ENTRE_CICLOS, f"Próximo ciclo (#{ciclo+1}) em")

    # Resumo final
    print(f"\n{'═'*52}")
    print(f"  📈  RESUMO FINAL")
    print(f"{'═'*52}")
    print(f"  Ciclos executados : {ciclo}")
    print(f"  Scripts ✅ ok     : {total_ok}")
    print(f"  Scripts ❌ falha  : {total_fail}")
    print(f"{'═'*52}\n")

if __name__ == "__main__":
    main()
