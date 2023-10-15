#!/bin/bash

# Set the path to the OpenSCAD executable
#OPENSCAD=/usr/bin/openscad
OPENSCAD=/home/sphink/Downloads/OpenSCAD-2023.10.11.ai16515-x86_64.AppImage

# Set the path to the directory where the STL files will be saved
STL_DIR=/home/sphink/devel/3d/library/gridfinity
project_name="bases"

generate_bases() {

    local getopt_results
    getopt_results=$(getopt -s bash -o 'x:y:z:' -l 'divx:,divy:,nolip,nozsnap,custom_z,scoop,tab,lite' -- "$@")
    eval set -- "$getopt_results"
    gridz_define=0
    enable_scoop='false'
    enable_lip='true'
    enable_zsnap='true'
    style_tab=5
    divx=1
    divy=1

    scad_file="Bins - kennetek.scad"

    while true; do
        case "$1" in
            -x) gridx="$2"; shift 2;;
            -y) gridy="$2"; shift 2;;
            -z) gridz="$2"; shift 2;;
            --divx) divx="$2"; shift 2;;
            --divy) divy="$2"; shift 2;;
            --nolip) enable_lip="false"; shift 1;;
            --nozsnap) enable_zsnap="false"; shift 1;;
            --custom_z) gridz_define="2"; shift 1;;
            --scoop) enable_scoop="true"; shift 1;;
            --tab) style_tab="1"; shift 1;;
            --lite) scad_file="Lite Bins - kennetek.scad"; shift 1;;
            --) shift; break;;
            *) echo "Error: Invalid argument $1"; exit 1;;
        esac
    done

    filename="${gridx}x${gridy}x${gridz}"
    if [ "$gridz_define" -ne 0 ]; then
        $filename=$filename"cm"
    fi
    
    if [ "$divx" -ne 1 ] || [ "$divy" -ne 1 ]; then
        filename="${filename}_div${divx}x${divy}"
    fi

    if [ "$enable_scoop" = "true" ]; then
        filename="${filename}_scoop"
    fi

    if [ "$enable_lip" = "false" ]; then
        filename="${filename}_nolip"
    fi

    if [ "$enable_zsnap" = "false" ]; then
        filename="${filename}_nozsnap"
    fi

    if [ "$style_tab" -ne 5 ]; then
        filename="${filename}_tab"
    fi

    # Check if there's argument on $1
    if [ -n "$1" ]; then
        filename="${filename}_${1}"
    fi

    filename="${filename}.stl"

    echo Generating $filename...

    $OPENSCAD \
    -D gridx=$gridx \
    -D gridy=$gridy \
    -D gridz=$gridz \
    -D divx=$divx \
    -D divy=$divy \
    -D gridz_define=$gridz_define \
    -D style_hole=0 \
    -D enable_scoop=$enable_scoop \
    -D enable_lip=$enable_lip \
    -D enable_zsnap=$enable_zsnap \
    -D style_tab=$style_tab \
    -o "$STL_DIR/${project_name}/${filename}" "${scad_file}"
}

project() {
    # Check if contains only one argument
    if [ "$#" -ne 1 ]; then
        echo "Error: Invalid number of arguments"
        exit 1
    fi

    # Remove folder with project name if it exists
    if [ -d "${STL_DIR}/${1}" ]; then
        rm -r "${STL_DIR}/${1}"
    fi
        
    # Recreate project folder
    mkdir "${STL_DIR}/${1}"
    # set global variable project_name
    project_name="$1"
}

project screws

# generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2
# generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2 --scoop
# generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2 --tab
# generate_bases -x 3 -y 5 -z 15 --divx 4 --divy 1 --tab
# generate_bases -x 1 -y 1 -z 3 
# generate_bases -x 1 -y 1 -z 3 --tab
# generate_bases -x 1 -y 1 -z 3 --nolip

#generate_bases -x 3 -y 2 -z 2 --divx 5 --divy 2 --tab --scoop 
#generate_bases -x 3 -y 2 -z 4 --divx 6 --divy 2 --tab --scoop

# m3x16 + m3x12
generate_bases -x 2 -y 1 -z 4 --divx 2 --lite --tab "m316+m312"

# m3x20
generate_bases -x 1 -y 2 -z 6 --divy 2 --tab --scoop "m320"

# m3 nuts
generate_bases -x 1 -y 1 -z 6 "m3nuts"

# m3 assorted
generate_bases -x 2 -y 1 -z 2 --divx 3 --lite "m3assorted" 

# m1.6
# generate_bases -x "2.5" -y 1 -z 3 --divx 6 --divy 1 --tab --scoop "m1.6"

# m2
# generate_bases -x 3 -y 1 -z 3 --divx 6 --divy 1 --tab --scoop "m2"

# m2 + m1.6
generate_bases -x 2 -y 3 -z 3 --divx 4 --divy 3 --tab --scoop "m2+m1.6"

# m2.5
generate_bases -x 2 -y 3 -z 3 --divx 2 --divy 3 --tab --scoop "m2.5"
