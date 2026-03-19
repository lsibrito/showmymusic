import pygame
import time
import os
import re
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# --- DICIONÁRIO CORRIGIDO ---
# O segredo aqui é o nome do arquivo ser IDÊNTICO ao que você tem na pasta
MUSICAS = {
    "1": {
        "titulo": "Happier Than Ever - Billie Eilish",
        "mp3": "Happier_Than_Ever-Billie_Eilish.mp3",
        "lrc": "happier_than_ever.lrc"
    },
    "2": {
        "titulo": "Fly Me To The Moon - Frank Sinatra",
        "mp3": "Fly_Me_To_The_Moon-Francis_Albert_Sinatra.mp3",  # Nome do arquivo que você enviou
        "lrc": "fly_me_to_the_moon.lrc"  # Verifique se o seu arquivo de letra tem esse nome!
    }
}


def carregar_letra(arquivo):
    letras = []
    if not os.path.exists(arquivo):
        return []
    padrao_tempo = r"\[(\d+):(\d+\.?\d*)\]"
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            resultado = re.search(padrao_tempo, linha)
            if resultado:
                minutos = int(resultado.group(1))
                segundos = float(resultado.group(2))
                total_segundos = minutos * 60 + segundos
                texto = linha[linha.find("]") + 1:].strip()
                letras.append((total_segundos, texto))
    letras.sort(key=lambda x: x[0])
    return letras


def gerar_conteudo(letras, indice_atual, titulo):
    conteudo = Text()
    if indice_atual > 0:
        conteudo.append(f"{letras[indice_atual - 1][1]}\n", style="dim white")
    else:
        conteudo.append("---\n", style="dim white")

    texto_atual = letras[indice_atual][1] if letras[indice_atual][1] else "..."
    conteudo.append(f"\n{texto_atual.upper()}\n\n", style="bold green")

    if indice_atual < len(letras) - 1:
        conteudo.append(f"{letras[indice_atual + 1][1]}", style="dim white")
    else:
        conteudo.append("---", style="dim white")

    return Panel(
        Align.center(conteudo, vertical="middle"),
        title=f"[bold green] {titulo} [/]",
        border_style="green",
        height=10
    )


def main():
    print("\n" + "=" * 30)
    print("      SPOTIFY TERMINAL")
    print("=" * 30)
    for chave, info in MUSICAS.items():
        print(f"{chave}. {info['titulo']}")

    escolha = input("\nEscolha o número da música: ").strip()

    if escolha not in MUSICAS:
        print("Opção inválida!")
        return

    dados = MUSICAS[escolha]

    # Verifica se os arquivos existem antes de tentar tocar
    if not os.path.exists(dados['mp3']):
        print(f"\n[ERRO] Arquivo de áudio não encontrado: {dados['mp3']}")
        return
    if not os.path.exists(dados['lrc']):
        print(f"\n[ERRO] Arquivo de letra não encontrado: {dados['lrc']}")
        return

    pygame.init()
    pygame.mixer.init()

    letra = carregar_letra(dados['lrc'])
    pygame.mixer.music.load(dados['mp3'])
    pygame.mixer.music.play()

    with Live(gerar_conteudo(letra, 0, dados['titulo']), refresh_per_second=10) as live:
        while pygame.mixer.music.get_busy():
            tempo_atual = pygame.mixer.music.get_pos() / 1000.0
            novo_indice = 0
            for i, (tempo, texto) in enumerate(letra):
                if tempo_atual >= tempo:
                    novo_indice = i
                else:
                    break
            live.update(gerar_conteudo(letra, novo_indice, dados['titulo']))
            time.sleep(0.1)

    pygame.quit()


if __name__ == "__main__":
    main()