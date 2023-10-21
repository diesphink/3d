from ocp_vscode import show

from build123d import (
    BuildPart,
    BuildSketch,
    Mode,
    Plane,
    extrude,
    import_svg,
    make_face,
    mirror,
    offset,
    scale,
)

parede, altura, largura, tolerancia = 2, 10, 100, 0.1
with BuildPart() as box:
    with BuildSketch() as mapa:
        make_face(import_svg("./assets/path6858.svg"))
        scale(by=largura / mapa.sketch.bounding_box().size.X)
        mirror(about=Plane.XZ, mode=Mode.REPLACE)
    print(mapa.sketch.location)
    extrude(amount=altura)

    inner_map = offset(mapa.sketch, amount=-parede)
    extrude(to_extrude=inner_map, amount=altura - parede, mode=Mode.SUBTRACT)


show(box)
