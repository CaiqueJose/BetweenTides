class Inventario:
    """Sistema de inventario do jogador."""

    def __init__(self):
        self.recursos = {
            "madeira": 0,
            "cipo": 0,
            "pedra": 0,
            "corda": 0,
            "chave": 0,
            "espada": 0,
        }
        self.pontuacao = 0

    def adicionar(self, tipo, quantidade=1):
        if tipo in self.recursos:
            self.recursos[tipo] += quantidade

    def quantidade(self, tipo):
        return self.recursos.get(tipo, 0)

    def possui(self, tipo, quantidade):
        return self.recursos.get(tipo, 0) >= quantidade

    def copiar(self):
        novo = Inventario()
        novo.recursos = self.recursos.copy()
        novo.pontuacao = self.pontuacao
        return novo

    def restaurar(self, outro):
        self.recursos = outro.recursos.copy()
        self.pontuacao = outro.pontuacao

    def resetar(self):
        for chave in self.recursos:
            self.recursos[chave] = 0
