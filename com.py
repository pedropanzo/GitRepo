#!/usr/bin/env python3
import subprocess
import sys
import os
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

def obter_alteracoes():
    """Obtém lista de arquivos alterados"""
    stdout, _, _ = executar_comando("git status --porcelain")
    if not stdout:
        return []
    return stdout.split('\n')

def fazer_commit(mensagem):
    """Realiza o commit com a mensagem fornecida"""
    print("\n📦 Adicionando arquivos...")
    executar_comando("git add .")
    
    print("💾 Realizando commit...")
    stdout, stderr, code = executar_comando(f'git commit -m "{mensagem}"')
    
    if code == 0:
        print("✅ Commit realizado com sucesso!")
        print(f"📝 Mensagem: {mensagem}")
        return True
    else:
        print(f"❌ Erro ao fazer commit: {stderr}")
        return False

def commit_com_mensagem_personalizada():
    """Commit com mensagem personalizada"""
    print("\n=== COMMIT PERSONALIZADO ===\n")
    
    # Mostrar status atual
    stdout, _, _ = executar_comando("git status --short")
    if stdout:
        print("📁 Arquivos a serem commitados:")
        print(stdout)
    else:
        print("⚠️  Nenhum arquivo alterado para commit!")
        return
    
    # Solicitar mensagem
    mensagem = input("\n✏️  Digite a mensagem do commit: ").strip()
    
    if not mensagem:
        print("❌ Mensagem não pode estar vazia!")
        return
    
    fazer_commit(mensagem)

def commit_com_mensagem_automatica():
    """Commit com mensagem automática baseada na data/hora"""
    print("\n=== COMMIT AUTOMÁTICO ===\n")
    
    # Gerar mensagem automática
    agora = datetime.now()
    mensagem = f"Update automático - {agora.strftime('%d/%m/%Y %H:%M:%S')}"
    
    print(f"📝 Mensagem gerada: {mensagem}")
    fazer_commit(mensagem)

def commit_com_tipo():
    """Commit com tipos convencionais (Conventional Commits)"""
    tipos = {
        "1": ("feat", "✨ Nova funcionalidade"),
        "2": ("fix", "🐛 Correção de bug"),
        "3": ("docs", "📚 Documentação"),
        "4": ("style", "💎 Estilo (formatação, etc)"),
        "5": ("refactor", "♻️  Refatoração"),
        "6": ("test", "✅ Testes"),
        "7": ("chore", "🔧 Manutenção")
    }
    
    print("\n=== COMMIT CONVENCIONAL ===\n")
    print("Escolha o tipo de commit:")
    for key, (tipo, emoji) in tipos.items():
        print(f"  {key}. {emoji} {tipo}")
    
    opcao = input("\nDigite o número (1-7): ").strip()
    
    if opcao not in tipos:
        print("❌ Opção inválida!")
        return
    
    tipo, emoji = tipos[opcao]
    escopo = input("Escopo (opcional, pressione Enter para pular): ").strip()
    descricao = input("Descrição curta: ").strip()
    
    if not descricao:
        print("❌ Descrição não pode estar vazia!")
        return
    
    if escopo:
        mensagem = f"{tipo}({escopo}): {descricao}"
    else:
        mensagem = f"{tipo}: {descricao}"
    
    print(f"\n📝 Mensagem: {mensagem}")
    fazer_commit(mensagem)

def commit_com_push():
    """Commit e push automático"""
    if fazer_commit(input("📝 Mensagem do commit: ").strip()):
        print("\n📤 Enviando para o repositório remoto...")
        stdout, stderr, code = executar_comando("git push")
        
        if code == 0:
            print("✅ Push realizado com sucesso!")
        else:
            print(f"❌ Erro no push: {stderr}")

def main():
    if not verificar_git():
        sys.exit(1)
    
    while True:
        print("\n" + "="*50)
        print("🤖 SCRIPT DE COMMIT GIT")
        print("="*50)
        print("1. 📝 Commit com mensagem personalizada")
        print("2. 🤖 Commit com mensagem automática")
        print("3. 📚 Commit convencional (feat, fix, docs...)")
        print("4. 🚀 Commit + Push")
        print("5. 👀 Ver status do repositório")
        print("6. 📋 Ver histórico de commits")
        print("7. ❌ Sair")
        print("="*50)
        
        opcao = input("\nEscolha uma opção (1-7): ").strip()
        
        if opcao == "1":
            commit_com_mensagem_personalizada()
        elif opcao == "2":
            commit_com_mensagem_automatica()
        elif opcao == "3":
            commit_com_tipo()
        elif opcao == "4":
            commit_com_push()
        elif opcao == "5":
            executar_comando("git status")
        elif opcao == "6":
            executar_comando("git log --oneline --graph --decorate -10")
        elif opcao == "7":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()