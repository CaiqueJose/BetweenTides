import json
import os

ARQUIVO_RECORDES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recordes.json")

NOMES_GENERICOS = {
    "Lenda dos Mares",
    "Navegador Mestre",
    "Lobo do Mar",
    "Explorador Naval",
    "Sobrevivente",
}

RECORDES_PADRAO = []

_CACHE_RECORDES = None
_ULTIMA_POSICAO = None


def carregar_recordes():
    """Carrega a lista de melhores pontuacoes cadastradas no arquivo JSON."""
    global _CACHE_RECORDES
    if os.path.exists(ARQUIVO_RECORDES):
        try:
            with open(ARQUIVO_RECORDES, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    # Filtrar quaisquer nomes genericos residuais
                    dados_filtrados = [
                        r for r in dados
                        if isinstance(r, dict) and r.get("nome") not in NOMES_GENERICOS
                    ]
                    _CACHE_RECORDES = dados_filtrados
                    return _CACHE_RECORDES
        except Exception as e:
            print(f"Erro ao ler recordes: {e}")

    _CACHE_RECORDES = []
    return _CACHE_RECORDES


def salvar_recordes(recordes):
    """Salva a lista de recordes no arquivo JSON."""
    try:
        # Nao salvar a flag transitoria 'atual' no arquivo persistido
        dados_salvar = []
        for r in recordes[:5]:
            item = {"nome": r.get("nome", "Naufrago"), "pontos": int(r.get("pontos", 0))}
            dados_salvar.append(item)
        with open(ARQUIVO_RECORDES, "w", encoding="utf-8") as f:
            json.dump(dados_salvar, f, indent=2)
    except Exception as e:
        print(f"Erro ao salvar recordes: {e}")


def registrar_pontuacao(pontos, nome="Naufrago (Voce)"):
    """Registra uma nova pontuacao, reordena o ranking e salva."""
    global _CACHE_RECORDES, _ULTIMA_POSICAO
    recordes = carregar_recordes()

    # Limpar flags anteriores de 'atual'
    for r in recordes:
        r["atual"] = False

    novo = {"nome": nome, "pontos": int(pontos), "atual": True}
    recordes.append(novo)

    # Ordenar por pontuacao decrescente
    recordes.sort(key=lambda x: x["pontos"], reverse=True)

    # Identificar posicao do jogador (1-indexado)
    posicao = None
    for idx, r in enumerate(recordes):
        if r.get("atual"):
            posicao = idx + 1
            break

    # Manter top 5
    recordes = recordes[:5]
    _CACHE_RECORDES = recordes
    _ULTIMA_POSICAO = posicao

    salvar_recordes(recordes)
    return recordes, posicao


def obter_recordes():
    """Retorna a lista atual de recordes e a ultima posicao registrada."""
    global _CACHE_RECORDES, _ULTIMA_POSICAO
    if _CACHE_RECORDES is None:
        _CACHE_RECORDES = carregar_recordes()
    return _CACHE_RECORDES, _ULTIMA_POSICAO

