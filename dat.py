#!/usr/bin/env python3
"""
Script que pega a data atual do computador, adiciona +1 dia e define como nova data
"""

import subprocess
import sys
from datetime import datetime, timedelta
import platform

def get_data_atual():
    """Obtém a data atual do sistema"""
    return datetime.now()

def adicionar_um_dia(data):
    """Adiciona 1 dia à data"""
    return data + timedelta(days=1)

def alterar_data_windows(nova_data):
    """Altera a data no Windows"""
    try:
        # Formato: DD-MM-AAAA
        data_formatada = nova_data.strftime("%d-%m-%Y")
        comando = f'date {data_formatada}'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"✅ Data alterada para: {data_formatada}")
            return True
        else:
            print(f"❌ Erro: {resultado.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao alterar data: {e}")
        return False

def alterar_data_linux(nova_data):
    """Altera a data no Linux/macOS"""
    try:
        # Formato: AAAA-MM-DD
        data_formatada = nova_data.strftime("%Y-%m-%d")
        
        # Para Linux, também podemos manter a mesma hora
        hora_atual = datetime.now().strftime("%H:%M:%S")
        data_hora = f"{data_formatada} {hora_atual}"
        
        comando = f'sudo date -s "{data_hora}"'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"✅ Data alterada para: {data_formatada}")
            return True
        else:
            print(f"❌ Erro: {resultado.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao alterar data: {e}")
        return False

def desativar_sincronizacao_windows():
    """Desativa sincronização automática no Windows"""
    try:
        # Desativar serviço de hora do Windows
        subprocess.run('net stop w32time', shell=True, capture_output=True)
        print("⚠️  Sincronização automática desativada")
        return True
    except:
        return False

def desativar_sincronizacao_linux():
    """Desativa sincronização automática no Linux"""
    try:
        subprocess.run('sudo timedatectl set-ntp false', shell=True, capture_output=True)
        print("⚠️  Sincronização automática desativada")
        return True
    except:
        return False

def main():
    print("="*50)
    print("📅 ALTERADOR DE DATA +1 DIA")
    print("="*50)
    
    # Detectar sistema operacional
    sistema = platform.system()
    print(f"🖥️  Sistema detectado: {sistema}")
    
    # Obter data atual
    data_atual = get_data_atual()
    print(f"\n📆 Data atual: {data_atual.strftime('%d/%m/%Y')}")
    
    # Adicionar 1 dia
    nova_data = adicionar_um_dia(data_atual)
    print(f"➕ Data +1 dia: {nova_data.strftime('%d/%m/%Y')}")
    
    # Confirmar com usuário
    confirmar = 's'
    
    if confirmar.lower() != 's':
        print("❌ Operação cancelada!")
        sys.exit(0)
    
    # Desativar sincronização automática (opcional)
    if sistema == "Windows":
        desativar_sincronizacao_windows()
        sucesso = alterar_data_windows(nova_data)
        if sucesso:
            print("\n💡 Dica: Reative a sincronização automática em:")
            print("   Configurações > Hora e Idioma > Sincronizar agora")
    elif sistema in ["Linux", "Darwin"]:  # Darwin = macOS
        desativar_sincronizacao_linux()
        sucesso = alterar_data_linux(nova_data)
        if sucesso:
            print("\n💡 Dica: Para reativar NTP, execute: sudo timedatectl set-ntp true")
    else:
        print(f"❌ Sistema não suportado: {sistema}")
        sys.exit(1)
    
    if sucesso:
        print("\n🎉 Data alterada com sucesso!")
        
        # Verificar nova data
        nova_data_sistema = datetime.now()
        print(f"📆 Nova data do sistema: {nova_data_sistema.strftime('%d/%m/%Y')}")
    else:
        print("\n❌ Falha ao alterar data!")
        print("   Execute o script como administrador/root!")
        sys.exit(1)

if __name__ == "__main__":
    main()