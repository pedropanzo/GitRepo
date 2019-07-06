#!/usr/bin/env python3
"""
🔄 CICLO AUTOMÁTICO DE SCRIPTS
Executa (tex.py → com.py) x20, depois dat.py x1
"""

import subprocess
import sys
import time
import os
import signal
import random
from datetime import datetime

# ──────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────
REP_MIN             = 5  # mínimo de repetições por ciclo
REP_MAX             = 30  # máximo de repetições por ciclo
PAUSA_ENTRE_SCRIPTS = 3   # segundos entre tex.py e com.py
PAUSA_ENTRE_CICLOS  = 4  # segundos entre cada ciclo completo
MAX_CICLOS          = 0   # 0 = infinito

TEX = {"arquivo": "tex.py", "nome": "Gerador de GUID",         "emoji": "🆔"}
COM = {"arquivo": "com.py", "nome": "Commit & Push Automático", "emoji": "📤"}
DAT = {"arquivo": "dat.py", "nome": "Alterador de Data +1",    "emoji": "📅"}

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
    print(f"  Ordem por ciclo:")
    print(f"    (tex.py -> com.py) x[{REP_MIN}~{REP_MAX} aleatorio]")
    print(f"    dat.py x1")
    print(f"  Pausa entre scripts : {PAUSA_ENTRE_SCRIPTS}s")
    print(f"  Pausa entre ciclos  : {PAUSA_ENTRE_CICLOS}s")
    print(f"  Max. ciclos         : {'inf' if MAX_CICLOS == 0 else MAX_CICLOS}")
    print(linha("═"))
    print("  Pressione Ctrl+C para parar\n")

def executar_script(script_info, label=""):
    arquivo = script_info["arquivo"]
    nome    = script_info["nome"]
    emoji   = script_info["emoji"]

    print(f"\n  {emoji}  [{hora()}]  {nome}{label}")
    print(f"  {linha('-', 48)}")

    if not os.path.exists(arquivo):
        print(f"  AVISO: Arquivo '{arquivo}' nao encontrado! Pulando...")
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

        if resultado.stdout:
            for ln in resultado.stdout.strip().splitlines():
                print(f"     {ln}")

        if resultado.stderr:
            print(f"  STDERR:")
            for ln in resultado.stderr.strip().splitlines():
                print(f"     {ln}")

        if resultado.returncode == 0:
            print(f"\n  OK  Concluido! (codigo {resultado.returncode})")
            return True
        else:
            print(f"\n  ERRO  Falhou! (codigo {resultado.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print(f"  Timeout! Script demorou mais de 60s.")
        return False
    except Exception as e:
        print(f"  Erro inesperado: {e}")
        return False

def aguardar(segundos, mensagem):
    for i in range(segundos, 0, -1):
        print(f"\r  {mensagem} ({i}s)... ", end="", flush=True)
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
            print(f"\nLimite de {MAX_CICLOS} ciclo(s) atingido. Encerrando.")
            break

        print(f"\n{'='*52}")
        print(f"  CICLO #{ciclo}   [{hora()}]")

        repeticoes = random.randint(REP_MIN, REP_MAX)
        print(f"  Repeticoes sorteadas: {repeticoes}")
        print(f"{'='*52}")

        resultados = []

        # ── Fase 1: (tex.py → com.py) repetido REPETICOES vezes ──
        for r in range(1, repeticoes + 1):
            if not executando:
                break

            print(f"\n  --- Repeticao {r}/{repeticoes} ---")

            # tex.py
            ok = executar_script(TEX, f"  [rep {r}/{repeticoes}]")
            resultados.append(ok)
            total_ok   += 1 if ok else 0
            total_fail += 0 if ok else 1

            if not executando:
                break

            aguardar(PAUSA_ENTRE_SCRIPTS, "Proximo em")

            # com.py
            ok = executar_script(COM, f"  [rep {r}/{repeticoes}]")
            resultados.append(ok)
            total_ok   += 1 if ok else 0
            total_fail += 0 if ok else 1

            if r < repeticoes and executando:
                aguardar(PAUSA_ENTRE_SCRIPTS, "Proxima repeticao em")

        # ── Fase 2: dat.py 1x ──
        if executando:
            print(f"\n  {linha('-', 48)}")
            ok = executar_script(DAT, "  [1x ao fim do ciclo]")
            resultados.append(ok)
            total_ok   += 1 if ok else 0
            total_fail += 0 if ok else 1

        # Resumo do ciclo
        ok_c   = sum(1 for r in resultados if r)
        fail_c = sum(1 for r in resultados if not r)
        print(f"\n  {linha('-', 48)}")
        print(f"  Ciclo #{ciclo} finalizado -- OK: {ok_c}  |  Falhas: {fail_c}")
        print(f"  {linha('-', 48)}")

        if not executando:
            break

        aguardar(PAUSA_ENTRE_CICLOS, f"Proximo ciclo (#{ciclo+1}) em")

    # Resumo final
    print(f"\n{'='*52}")
    print(f"  RESUMO FINAL")
    print(f"{'='*52}")
    print(f"  Ciclos executados : {ciclo}")
    print(f"  Execucoes OK      : {total_ok}")
    print(f"  Execucoes Falha   : {total_fail}")
    print(f"{'='*52}\n")

if __name__ == "__main__":
    main()
