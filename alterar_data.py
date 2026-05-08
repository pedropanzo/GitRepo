import subprocess
import sys
import os
from datetime import datetime

def alterar_data_windows(nova_data):
    """Altera a data no Windows"""
    try:
        # Formato: DD-MM-AAAA
        data_formatada = nova_data.strftime("%d-%m-%Y")
        subprocess.run(f'date {data_formatada}', shell=True, check=True)
        print(f"Data alterada para: {data_formatada}")
        return True
    except subprocess.CalledProcessError:
        print("Erro ao alterar data. Execute como administrador.")
        return False

def alterar_data_linux(nova_data):
    """Altera a data no Linux/macOS"""
    try:
        # Formato: AAAA-MM-DD
        data_formatada = nova_data.strftime("%Y-%m-%d")
        subprocess.run(f'sudo date -s "{data_formatada}"', shell=True, check=True)
        print(f"Data alterada para: {data_formatada}")
        return True
    except subprocess.CalledProcessError:
        print("Erro ao alterar data. Execute como sudo.")
        return False

def main():
    print("=== ALTERADOR DE DATA DO SISTEMA ===")
    print("Formato: DD/MM/AAAA ou DD-MM-AAAA")
    
    data_input = input("Digite a nova data: ")
    
    # Tentar diferentes formatos
    for formato in ["%d/%m/%Y", "%d-%m-%Y"]:
        try:
            nova_data = datetime.strptime(data_input, formato)
            break
        except ValueError:
            continue
    else:
        print("Formato inválido! Use DD/MM/AAAA ou DD-MM-AAAA")
        sys.exit(1)
    
    # Detectar sistema operacional
    sistema = sys.platform
    
    if sistema == "win32":
        if not alterar_data_windows(nova_data):
            print("Dica: Execute o script como administrador!")
    elif sistema in ["linux", "darwin"]:  # darwin = macOS
        if not alterar_data_linux(nova_data):
            print("Dica: Execute com: sudo python script.py")
    else:
        print(f"Sistema não suportado: {sistema}")

if __name__ == "__main__":
    main()