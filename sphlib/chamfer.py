import math


def rescale_chamfer(chamfer, modifier):
    # Cálculo do tamanho do chanfrado interno
    # ===
    # Altura do triangulo chanfrado (altura = cateto / raiz de 2)
    altura = chamfer / math.sqrt(2)

    # Altura do novo chanfrado (altura antiga + 1 borda, 1 diagonal do quadrado de bordas)
    altura_nova = altura + modifier - modifier * math.sqrt(2)

    # chanfrado interno é o cateto do triangulo com altura nova
    return altura_nova * math.sqrt(2)
