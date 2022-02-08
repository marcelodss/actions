# Referência: https://docs.python.org/3/library/pathlib.html

from pathlib import Path

pergunta = 'Deletar arquivos cache e os da pasta migrations? S/N:'
separador = ' '.join('*' * len(pergunta))
resposta = input('\n' + separador + '\nDeletar arquivos cache e os da pasta migrations? S/N\n' + separador + '\n')

caminho = Path(__file__).resolve().parent.parent 

if resposta.upper() == 'S':
    for arquivo in Path(caminho).glob("**/*.py"):
        diretorio = Path(arquivo).resolve().parent
        if Path(diretorio).name == 'migrations' and Path(arquivo).name != '__init__.py':
            if Path(arquivo).exists():
                Path(arquivo).unlink(missing_ok=False)
                print(f'\n{Path(arquivo).name} DELETADO\nde {diretorio}')

    for arquivo in Path(caminho).glob("**/*.pyc"):
        diretorio = Path(arquivo).resolve().parent
        if Path(diretorio).name == '__pycache__':
            if Path(arquivo).exists():
                Path(arquivo).unlink(missing_ok=False)
                print(f'\n{Path(arquivo).name} DELETADO\nde {diretorio}')

