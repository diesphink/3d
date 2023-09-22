from ocp_vscode import show

from build123d import (
    Axis,
    BuildLine,
    BuildPart,
    BuildSketch,
    Mode,
    Plane,
    Rectangle,
    Vector,
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
        make_face(import_svg("./src/assets/path6858.svg"))
        scale(by=largura / mapa.sketch.bounding_box().size.X)
        mirror(about=Plane.XZ, mode=Mode.REPLACE)
    print(mapa.sketch.location)
    extrude(amount=altura)
    
    inner_map = offset(mapa.sketch, amount=-parede)
    extrude(to_extrude=inner_map, amount=altura - parede, mode=Mode.SUBTRACT)
    

show(box)

# face = make_face(edges)
# face = scale(objects=face, by=largura / face.bounding_box().size.X)
# box = extrude(to_extrude=face, amount=altura)
# inner_face = offset(face.sketch, amount=-parede)



# inner_box = extrude(inner_face, amount=altura - parede)
# box = box.cut(inner_box)

# face = face.translate(vector=Vector(largura * 1.1, 0, 0))
# inner_face = offset(face, amount=-parede - tolerancia) 

# lid = extrude(to_extrude=face, amount=parede)
# inner_lid = extrude(inner_face, amount=parede * 2)
# lid = lid.fuse(inner_lid)

# show([box, lid])
# print(box.bounding_box().size)

# box.export_stl("library/caixa_brasil/box.stl")
# lid.export_stl("library/caixa_brasil/lid.stl")
