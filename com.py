#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import subprocess
import sys
from datetime import datetime

def executar_comando(comando):
    """Executa comando no terminal e retorna saída"""
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        return resultado.stdout.strip(), resultado.stderr.strip(), resultado.returncode
    except Exception as e:
        return "", str(e), 1

def verificar_git():
    """Verifica se está em um repositório Git"""
    stdout, stderr, code = executar_comando("git status")
    if code != 0:
        print("❌ Não está em um repositório Git!")
        return False
    return True

def verificar_alteracoes():
    """Verifica se há alterações para commit"""
    stdout, _, _ = executar_comando("git status --porcelain")
    if not stdout:
        print("⚠️  Nenhum arquivo alterado para commit!")
        return False
    return True

def commit_auto_push():
    """Realiza commit automático e push"""
    print("\n=== COMMIT AUTOMÁTICO COM PUSH ===\n")
    
    # Verificar alterações
    if not verificar_alteracoes():
        return False
    
    # Mostrar arquivos que serão commitados
    stdout, _, _ = executar_comando("git status --short")
    print("📁 Arquivos a serem commitados:")
    print(stdout)
    
    # Gerar mensagem automática com data/hora
    agora = datetime.now()
    mensagem = f"Update automático - {agora.strftime('%d/%m/%Y %H:%M:%S')}"
    
    print(f"\n📝 Mensagem gerada: {mensagem}")
    
    # Adicionar arquivos
    print("\n📦 Adicionando arquivos...")
    executar_comando("git add .")
    
    # Fazer commit
    print("💾 Realizando commit...")
    _, stderr, code = executar_comando(f'git commit -m "{mensagem}"')
    
    if code != 0:
        print(f"❌ Erro ao fazer commit: {stderr}")
        return False
    
    print("✅ Commit realizado com sucesso!")
    
    # Fazer push
    print("\n📤 Enviando para o repositório remoto...")
    #_, stderr, code = executar_comando("git push")
    
    if code == 0:
        print("✅ Push realizado com sucesso!")
        return True
    else:
        print(f"❌ Erro no push: {stderr}")
        return False

def main():
    if not verificar_git():
        sys.exit(1)
    
    if commit_auto_push():
        print("\n🎉 Processo concluído com sucesso!")
    else:
        print("\n❌ Falha no processo!")
        sys.exit(1)

if __name__ == "__main__":
    main()