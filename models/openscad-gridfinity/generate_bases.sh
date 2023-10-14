#!/bin/bash

# Set the path to the OpenSCAD executable
OPENSCAD=/usr/bin/openscad

# Set the path to the directory where the STL files will be saved
STL_DIR=/home/sphink/devel/3d/library/gridfinity/bases

generate_bases() {

    local getopt_results
    getopt_results=$(getopt -s bash -o 'x:y:z:' -l 'divx:,divy:,nolip,nozsnap,custom_z,scoop,tab' -- "$@")
    eval set -- "$getopt_results"
    gridz_define=0
    enable_scoop='false'
    enable_lip='true'
    enable_zsnap='true'
    style_tab=5
    divx=1
    divy=1

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
    -o "$STL_DIR/${filename}" "Bins - kennetek.scad"
}

generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2
generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2 --scoop
generate_bases -x 4 -y 2 -z 6 --divx 2 --divy 2 --tab
generate_bases -x 3 -y 5 -z 15 --divx 4 --divy 1 --tab
generate_bases -x 1 -y 1 -z 3 
generate_bases -x 1 -y 1 -z 3 --tab
generate_bases -x 1 -y 1 -z 3 --nolip
