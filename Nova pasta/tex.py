#!/usr/bin/env python3
"""
Script para escrever GUID automaticamente em arquivo "Arq"
"""

import uuid

def escrever_arquivo(nome_arquivo, conteudo):
    """Escreve conteúdo no arquivo (substitui se já existir)"""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        print(f"✅ Conteúdo escrito em '{nome_arquivo}' com sucesso!")
        print(f"📝 GUID gerado: {conteudo}")
        return True
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")
        return False

# Gerar GUID automaticamente
def gerar_guid():
    """Gera um GUID único"""
    return str(uuid.uuid4())

# Exemplo de uso automático
if __name__ == "__main__":
    # Nome fixo do arquivo
    nome = "Arq"
    
    # Gerar GUID automaticamente
    guid = gerar_guid()
    
    print(f"🔧 Gerando GUID para o arquivo '{nome}'...")
    print(f"🆔 GUID: {guid}")
    
    # Escrever o GUID no arquivo
    escrever_arquivo(nome, guid)