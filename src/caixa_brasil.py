from ocp_vscode import show

from build123d import (
    Vector,
    extrude,
    import_svg,
    make_face,
    offset,
    scale,  
)

parede, altura, largura, tolerancia = 1, 5, 55, 0.1

edges = import_svg("./src/assets/mapa.svg")
face = make_face(edges)
face = scale(objects=face, by=largura / face.bounding_box().size.X)
box = extrude(to_extrude=face, amount=altura)
inner_face = offset(face, amount=-parede)
inner_box = extrude(inner_face, amount=altura - parede)
box = box.cut(inner_box)

face = face.translate(vector=Vector(largura * 1.1, 0, 0))
inner_face = offset(face, amount=-parede - tolerancia) 

lid = extrude(to_extrude=face, amount=parede)
inner_lid = extrude(inner_face, amount=parede * 2)
lid = lid.fuse(inner_lid)

show([box, lid])
print(box.bounding_box().size)

box.export_stl("library/caixa_brasil/box.stl")
lid.export_stl("library/caixa_brasil/lid.stl")
