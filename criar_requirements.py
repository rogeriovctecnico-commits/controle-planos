import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🔧 Criando requirements.txt automaticamente...")
    
    # Verificar se estamos em ambiente virtual
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("❌ Ambiente virtual não está ativo!")
        print("💡 Ative primeiro: .\.venv\Scripts\Activate.ps1")
        return
    
    try:
        # Executar pip freeze
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'freeze'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        packages = result.stdout.strip()
        
        if packages:
            # Criar arquivo requirements.txt
            with open('requirements.txt', 'w', encoding='utf-8') as f:
                f.write(packages)
            
            print(f"✅ requirements.txt criado com sucesso!")
            print(f"📦 {len(packages.split())} pacotes encontrados")
            
            # Mostrar primeiros pacotes
            lines = packages.split('\n')[:5]
            print("📋 Primeiros pacotes:")
            for line in lines:
                if line.strip():
                    print(f"  {line}")
            
            if len(packages.split('\n')) > 5:
                print(f"  ... e mais {len(packages.split()) - 5} pacotes")
                
        else:
            print("⚠️ Nenhum pacote instalado no ambiente virtual")
            # Criar arquivo vazio
            with open('requirements.txt', 'w', encoding='utf-8') as f:
                f.write("# Nenhum pacote instalado\n")
            print("📄 Arquivo requirements.txt vazio criado")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar pip freeze: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()