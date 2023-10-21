# Based on work by jdegs
# https://www.printables.com/@jdegs
# https://www.printables.com/model/202054-divided-gridfinity-boxes-with-finger-scoops-cadque

# reimplementation of scooped divided gridfinity box design by Zack Freedman
# this revision is dated 2022-05-10 adds finger scoops
# designed in CadQuery and CQ-Editor both checked out from github on 2022-04-13
from build123d import BasePartObject
import cadquery as cq
import math
from cadquery import exporters
from random import randrange as rrr
import build123d as b3d

from ocp_vscode import show_object


class GridfinityBox(BasePartObject):
    def __init__(
        self,
        x_grid_number=1,
        y_grid_number=7,
        unit_height=6,
        x_divider_number=0,
        y_divider_number=2,
        disable_mholes=False,
        disable_scoops=False,
        **kwargs
    ):
        # # adjust these three variables to change the grid size
        # x_grid_number = 1  # CHANGEME! 1+ number of x units of gridfinity size
        # y_grid_number = 2  # CHANGEME! 1+ number of y units of gridfinity size
        # unit_height = 3  # CHANGME! 2+ number of units -- unitless in integer

        # # adjust these variables to change the number of divider walls
        # x_divider_number = 0  # CHANGEME! number of divider walls
        # y_divider_number = 2  # CHANGEME!
        # # ^ for this scooped version, recommend, x_divs is fixed at zero
        # # and y_divs is adjusted as desired

        # disable_mholes = True  # disable magnet/bolt holes in container

        # disable_scoops = False  # use this to switch scoops on/off,
        # # ^scoops are only on face perp. to x-axis and on one side
        # # ^scoops do not take into account divider walls
        # # by default they are the max allowable size

        # # box stackability is implemented!
        # # boxes are always 0.5mm shy of the unit_width*42mm, and
        # # that is independent of number of units

        ############################################
        # shouldn't need to adjust anything below here
        box_wd = 42.0  # mm, distance between major straight walls
        box_maj_wd = box_wd  # mm, x,y width of box to add
        b2b_clear = 0.5  # mm, box to box clearance applied only once to each x and y
        c_rad = 4  # mm, corner radius of outer box
        socket_ht = 5  # mm, overall socket height
        ov_ht = 3.8 + 7 * unit_height  # mm, overall height for a Z-unit box
        vw_ht = ov_ht - socket_ht  # mm, height of vertical walls
        wall_th = 1.0  # mm, wall thickness, don't adjust as it will break top-socket compat
        div_wall_th = 1.0  # mm, divider wall thickness should be adjustable
        div_ht = (
            ov_ht - 2 * socket_ht
        )  # mm, divider wall height should be adjustable as long as it it doesn't interfere with socket

        # for magnet/bolt holes
        mag_diam = 6.5  # mm
        mag_dep = 2.4  # mm
        bolt_diam = 3.0  # mm
        bolt_dep = 3.6 + mag_dep  # mm, total depth of entire hole includng 3.6mm for the bolt itself
        mag_dist0 = 26 / 2  # mm, distance from holes to zero-axis (26mm between holes total)

        bot_th = 2.0 + bolt_dep - socket_ht  # mm, bottom thickness of box interior
        # bot_th was revised to account for bolt_dep since it is longer than socket_ht
        # the revision ensures that there is 2.0mm of bottom thickness above the top of the bolt holes

        # actual hypotenuse of t_chm is 3.39mm
        # actual exterior hypotenuse of t_chm is 3.04mm due to cropping

        # for socket only
        b_chm_ht = 1.13 / math.sqrt(2)  # mm, base chamfer height
        strt_ht = 1.8  # mm, straight wall height
        t_chm_ht = socket_ht - b_chm_ht - strt_ht  # top chamfer height

        # create 2D sketch with rounded corners, for the bottom of the socket
        s3a = (
            cq.Sketch().rect(box_wd + 0.001, box_wd + 0.001).vertices().fillet(c_rad)
        )  # ensure boxes overlap with small add

        # take s3a sketch and create one socket for the bottom of box
        f2 = (
            cq.Workplane("XY")
            .placeSketch(s3a)
            .extrude(t_chm_ht * math.sqrt(2), taper=45)
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(strt_ht)
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(b_chm_ht * math.sqrt(2), taper=45)
            .mirror(mirrorPlane="XY")  # flip upside down
        )

        # create sketch for exterior box walls
        box_wd_xwall = box_wd * x_grid_number - b2b_clear  # 0.5mm for clearance btwn boxes
        box_wd_ywall = box_wd * y_grid_number - b2b_clear

        s4 = cq.Sketch().rect(box_wd_xwall, box_wd_ywall).vertices().fillet(c_rad)

        # define x,y positions of the exterior walls
        wall_xpos = (box_wd) * (x_grid_number - 1) / 2
        wall_ypos = (box_wd) * (y_grid_number - 1) / 2

        # create exterior box walls
        f7 = (
            cq.Workplane("XY").placeSketch(s4).extrude(vw_ht).translate((wall_xpos, wall_ypos, 0))
        )  # vertical wall height

        # create divider walls
        s1 = (
            cq.Sketch()
            .rect(box_wd_xwall, div_wall_th)  # create x-wall rect
            .rect(div_wall_th, box_wd_ywall)  # create y-wal rect
        )

        f1 = cq.Workplane("XY")  # basic workplane object
        f1b = (  # these are the "x-walls" used to create walls perpendicular to x-axis
            cq.Workplane("XY").rect(div_wall_th, box_wd_ywall).extrude(div_ht)
        )

        f1c = (  # these are the "y-walls" used to create walls perpendicular to y-axis
            cq.Workplane("XY").rect(box_wd_xwall, div_wall_th).extrude(div_ht)
        )

        # divx_pts is the locations of the x divider boxes, the math for placing these automatically is fairly complicated
        divx_pts = [
            (
                box_wd_xwall / (x_divider_number + 1) * (x + 1 / x_grid_number * 2)
                + box_wd_xwall / x_grid_number * ((x_grid_number - 2) / (x_divider_number + 1) - 1 / 2),
                box_wd_ywall / 2 - box_wd / 2 + b2b_clear / 2,
            )
            for x in range(0, x_divider_number)
        ]

        # divy_pts is the locations of the y divider boxes
        divy_pts = [
            (
                box_wd_xwall / 2 - box_wd / 2 + b2b_clear / 2,
                box_wd_ywall / (y_divider_number + 1) * (y + 1 / y_grid_number * 2)
                + box_wd_ywall / y_grid_number * ((y_grid_number - 2) / (y_divider_number + 1) - 1 / 2),
            )
            for y in range(0, y_divider_number)
        ]

        # f1x iterates through divx_pts and creates all the x divider boxes, f1y is y-equiv
        f1x = f1.pushPoints(divx_pts).eachpoint(lambda loc: f1b.val().moved(loc), combine="a")
        f1y = f1.pushPoints(divy_pts).eachpoint(lambda loc: f1c.val().moved(loc), combine="a")

        # create tool to trim off excess socket underhang
        f11 = (
            cq.Workplane("XY")
            .placeSketch(s4)
            .extrude(-socket_ht - 1)  # socket is below XY-plane
            .translate((wall_xpos, wall_ypos, 1 / 2))
        )

        c_rad_in = c_rad - wall_th  # mm, corner radius of inner box (f(wall_th))

        # create sketch for box interior that is later swept
        # straight/chamfered to create top socket for stackability
        s5 = (
            cq.Sketch()
            # should NOT be a f(wall_th) to ensure compatibility, but could create other issues
            .rect(box_wd_xwall - 2 * wall_th, box_wd_ywall - 2 * wall_th)
            .vertices()
            .fillet(c_rad_in)
        )

        # for top socket of box walls that allows stacking
        # ordered vars from lowest to highest in a spatial sense
        wall_strt_ht1 = vw_ht - 6.5 - bot_th  # main straight interior
        wall_chm_ht1 = 2.33 / math.sqrt(2)  # 45-deg section to support socket w/o supports
        wall_strt_ht2 = 1.2
        wall_chm_ht2 = 0.98 / math.sqrt(2)
        wall_strt_ht3 = 1.8
        wall_chm_ht3 = 1.59 / math.sqrt(2) + 0.1  # add a little extra to make sure it clears the top face

        # create tool to later subtract inside of box
        # includes fillets on the bottom interior
        # and chamfered walls that enable stacking
        f9 = (
            cq.Workplane("XY")
            .placeSketch(s5)
            .extrude(wall_strt_ht1)  # vertical wall height
            .translate((wall_xpos, wall_ypos, bot_th))  # REVISED, to make sure bot_th is correct
            # .faces("<Z").edges("|X").chamfer(3) #skip for swoopies
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(wall_chm_ht1 * math.sqrt(2), taper=45)  # "overhang" chamfer"
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(wall_strt_ht2)  # short straight section
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(wall_chm_ht2 * math.sqrt(2), taper=-45)  # 1st part of socket interface
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(wall_strt_ht3)  # next short straight section for socket interface
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(wall_chm_ht3 * math.sqrt(2), taper=-45)  # last part of socket interface
        )

        # create sketch for box interior that is later used
        # for finger scoops inside the box

        # scoop_fillet = min((box_wd*x_grid_number/2-2*wall_th),wall_strt_ht1-1)
        scoop_fillet = min((box_wd * x_grid_number - 3 * wall_th), wall_strt_ht1 - 0.001)
        # log((box_wd * x_grid_number - 3 * wall_th))
        # log(wall_strt_ht1)
        s5rect = cq.Sketch().rect(box_wd_xwall - 2 * wall_th, box_wd_ywall - 2 * wall_th)

        scoop_xtr = wall_chm_ht1 / math.sqrt(2) + wall_th / 2

        f9_scoops_neg = (
            cq.Workplane("XY")
            .rect(box_wd_xwall - 2 * wall_th, box_wd_ywall - 2 * wall_th)
            .extrude(wall_strt_ht1 + wall_chm_ht1 + wall_strt_ht2)  # vertical wall height
            .faces("<Z")
            .edges("|Y")  # select two sides
            .edges("<X")  # select one side
            .fillet(scoop_fillet)  # vertical wall height
            .translate((wall_xpos + scoop_xtr, wall_ypos, bot_th))  # REVISED, to make sure bot_th is correct
        )
        f9_scoops_pos = (
            cq.Workplane("XY")
            .placeSketch(s5rect)
            .extrude(wall_strt_ht1 + wall_chm_ht1 + wall_strt_ht2)
            .translate((wall_xpos, wall_ypos, bot_th))
            .edges("|Z")
            .chamfer(wall_th / 2)  # cut off corners that stick through
            .cut(f9_scoops_neg)
        )

        # pts is the locations of each grid position for each box
        # only used for socket base(s)
        pts = [(x * box_maj_wd, y * box_maj_wd) for x in range(0, x_grid_number) for y in range(0, y_grid_number)]
        pts.pop(0)  # remove first element as not to duplicate existing socket
        f2a = f2.pushPoints(pts).eachpoint(lambda loc: f2.val().moved(loc), combine="a")  # join all sockets
        f4 = f11.intersect(f2a)  # trim excess socket overhang, approx 0.25mm all sides
        f3 = f7.union(f4)  # join trimmed sockets with walls
        f8 = f3.cut(f9)  # remove box interior

        if not disable_scoops:
            f8 = f8.union(f9_scoops_pos)  # add swoopy doops

        # add the dividers to final part
        if x_divider_number != 0:  # dont union any xwalls if set to zero
            f8 = f8.union(f1x)
        if y_divider_number != 0:  # dont union any ywalls if set to zero
            f8 = f8.union(f1y)

        # hole_pts is center locations of ALL the magnet/bolt holes
        # BEWARE that the coordinate system is inverted in the y-direction hence the -1*
        # this is why you should not use cboreHole, because it cant do inverted holes!
        hole_pts = [
            ((x * box_maj_wd - mag_dist0 * (1 - 2 * i)), -1 * (y * box_maj_wd - mag_dist0 * (1 - 2 * j)))
            for x in range(0, x_grid_number)
            for y in range(0, y_grid_number)
            for i in [0, 1]
            for j in [0, 1]
        ]

        # "counterbore" all the magnet/bolt hole locations
        if disable_mholes == False:
            f8 = f8.faces("<Z").workplane().pushPoints(hole_pts).cboreHole(bolt_diam, mag_diam, mag_dep, depth=bolt_dep)

        # f8 is the final complete part
        def rnco():
            return rrr(10, 100), rrr(10, 100), rrr(10, 100)  # random color, dont want too bright

        # show_object(f8, options={"alpha": 0.10, "color": (10, 14, 10)})
        # show_object(f9_scoops_pos,options={"alpha":0.10, "color": rnco()})
        # show_object(f1y,options={"alpha":0.10, "color": (165, 94, 55)})

        filename = (
            "divided box "
            + str(x_grid_number)
            + "x"
            + str(y_grid_number)
            + "x"
            + str(unit_height)
            + "-hi and "
            + str(x_divider_number)
            + "x"
            + str(y_divider_number)
            + "-divs with finger scoops.stl"
        )
        # log(filename)
        # exporters.export(f8, filename, tolerance=0.99, angularTolerance=0.5)

        b3d_solid = b3d.Solid.make_box(1, 1, 1)
        b3d_solid.wrapped = f8.objects[0].wrapped

        super().__init__(part=b3d_solid)


show_object(GridfinityBox(x_grid_number=4, y_grid_number=4, unit_height=5, x_divider_number=0, y_divider_number=0))
