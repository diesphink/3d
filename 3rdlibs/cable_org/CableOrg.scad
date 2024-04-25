// ------------------
// Dec 2023 - Cubic8
// ------------------

/* [Cable Details] */

// Diameter of the cable in mm
cable_diameter = 3.0; // [1:0.1:6]

// Maximum loops of the cable that the clip is to hold
cable_max_loops = 4; // [2:1:20]

/* [Clip Dimentions] */

// Overall height of the clip in mm (ie. when printed on its edge)
clip_height = 10.0; // [1:1:50]

// Maximum outer width of clip in mm (ie. across the loops of cable). The depth will be adjusted to fit your required loops.
max_width = 30; // [20:0.5:80]

// Check if using flex filament. The cable gap will be smaller, and walls thicker.
using_flex = false;

// Check if the central space is to be a clip to grip onto the cable.
cable_grip = false;

/* [Hidden] */

// Thickness of walls in mm
// FLEX needs thicker walls
base_thickness = using_flex ? 2.0: 1.0;

// Add extra if we have a bigger clip
wall_thickness = base_thickness 
    + round(0.5 
        + (cable_diameter * cable_max_loops) / 50.0
    );
echo("wall_thickness", wall_thickness);

// Depth is calculated from cable size and loops needed
loop_num_bottom = max(2, round(0.5 + 
       (max_width/2 - wall_thickness * 1.5) /
        cable_diameter
    ));

internal_depth = (round(0.5 +(cable_max_loops / loop_num_bottom)) + 1)
       * cable_diameter;
       
outer_depth = internal_depth + wall_thickness*2;

// No-Corner dimentions
depth_nc = internal_depth - cable_diameter;
half_width_nc = (max_width/2 - wall_thickness * 1.5) - cable_diameter; 
top_half_width_nc = 
    using_flex ? 
        half_width_nc - cable_diameter/4 :
        half_width_nc - cable_diameter;

echo("loop_num_bottom", loop_num_bottom);
echo("internal_depth", internal_depth);
echo("outer_depth", outer_depth);
echo("depth_nc", depth_nc);
echo("half_width_nc", half_width_nc);
echo("top_half_width_nc", top_half_width_nc);

$fn = 60;

assert(loop_num_bottom > 1, "Expect bottom width to be over 1 mm");
assert(half_width_nc > 0, "Must be able to fit one cable dia across bottom.  Increase Max-Width");
assert(top_half_width_nc > 0, "Must have enough width to fit cable through. Increase Max-Width");

module corner_section(r)
{
    rotate([0,0,r])
    {
        intersection()
        {
            difference()
            {
                circle(cable_diameter/2 + wall_thickness);
                circle(cable_diameter/2);
            }
            square(cable_diameter/2 + wall_thickness);
        }
    }
}

module end_section(r)
{
    rotate([0,0,r])
    {
        intersection()
        {
            circle(wall_thickness/2);
            translate([wall_thickness/2,0,0])
                square(wall_thickness, center=true);
        }
    }
}

module half_section_squ()
{
    corneradj = (cable_diameter+wall_thickness)/2;
    
    translate([0,-half_width_nc-wall_thickness/2-cable_diameter/2,0])
    {
        translate([-corneradj,-corneradj,0])
        {
            translate([-depth_nc,0,0])
            {
                translate([-corneradj,corneradj,0])
                {
                    translate([0,half_width_nc,0])
                    {
                        translate([
                            (depth_nc+cable_diameter+wall_thickness)/2,
                            corneradj,
                            0
                        ])
                        {
                            square([depth_nc, wall_thickness], center = true);
                            translate([depth_nc/2,0,0]) end_section(0);
                            translate([
                                -depth_nc/2,
                                -corneradj,
                                0]) corner_section(90);
                        }
                        
                        translate([0,-half_width_nc/2,0])
                        {
                            square([wall_thickness, half_width_nc], center = true);
                        }
                    }
                    translate([corneradj,0,0]){
                        corner_section(180);
                    }
                }
                translate([depth_nc/2,0,0])
                {
                    square([depth_nc, wall_thickness], center = true);
                }
            }
            translate([0,corneradj,0])
            {
                corner_section(270);
            }
        }
        translate([0, top_half_width_nc/2, 0])
        {
            square([wall_thickness, top_half_width_nc], center = true);
        }
        translate([0,top_half_width_nc,0]) end_section(90);
    }
}

linear_extrude(clip_height)
{
    if (cable_grip)
    {
        grip_scale = [1,using_flex ? 1.3 : 1,1];
        grip_indent_factor = 0.15;
        offset = (cable_diameter + wall_thickness)/2;
        translate([0,-offset,0])
        {   
            half_section_squ();
            translate([-cable_diameter,cable_diameter*grip_indent_factor,0])
                scale(grip_scale)
                    end_section(90);
        }
        mirror([0,1,0]) translate([0,-offset,0])
        {
            half_section_squ();
            translate([-cable_diameter,cable_diameter*grip_indent_factor,0])
                scale(grip_scale)
                    end_section(90);
        }
        translate([-internal_depth,0,0])
        {
            corner_section(180);
            corner_section(90);
        }
        
    }
    else
    {
        half_section_squ();
        mirror([0,1,0]) half_section_squ();
    }
}
