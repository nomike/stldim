#!/usr/bin/env python3
"""
    stldim - Get dimensions of an STL file
    Usage:
        stldim.py [options] <stlfile>

    Options:
        -h --help       Show this screen.
        --version       Show version.
        --name=<name>   Name of the object [defaults to the filename with non alpha-numeric characters replaced with underscores].
"""

import argparse
import os
import re
import sys
import stldim._version

import stl
from stl import mesh


def sanitize_filename(args):
    """
    Replace every non-alphanumeric character with an underscore
    """
    return re.sub(r'\W', '_', os.path.basename(args.stlfile)).lower()


def get_varname(args):
    if args.name:
        return args.name
    else:
        return sanitize_filename(args)


def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

def get_stl_dimensions(stlfile):
    # find the max dimensions, so we can know the bounding box, getting the height,
    # width, length (because these are the step size)...
    stl_dimensions = {}

    main_body = mesh.Mesh.from_file(stlfile)

    stl_dimensions['minx'], stl_dimensions['maxx'], stl_dimensions['miny'], stl_dimensions['maxy'], stl_dimensions['minz'], stl_dimensions['maxz'] = find_mins_maxs(main_body)

    stl_dimensions['minx'] = round(stl_dimensions['minx'], 3)
    stl_dimensions['maxx'] = round(stl_dimensions['maxx'], 3)
    stl_dimensions['miny'] = round(stl_dimensions['miny'], 3)
    stl_dimensions['maxy'] = round(stl_dimensions['maxy'], 3)
    stl_dimensions['minz'] = round(stl_dimensions['minz'], 3)
    stl_dimensions['maxz'] = round(stl_dimensions['maxz'], 3)

    stl_dimensions['xsize'] = round(stl_dimensions['maxx']-stl_dimensions['minx'], 3)
    stl_dimensions['ysize'] = round(stl_dimensions['maxy']-stl_dimensions['miny'], 3)
    stl_dimensions['zsize'] = round(stl_dimensions['maxz']-stl_dimensions['minz'], 3)

    stl_dimensions['midx'] = round(stl_dimensions['xsize']/2, 3)
    stl_dimensions['midy'] = round(stl_dimensions['ysize']/2, 3)
    stl_dimensions['midz'] = round(stl_dimensions['zsize']/2, 3)

    return stl_dimensions

def main():
    parser = argparse.ArgumentParser(prog="stldim",
        description="Get dimensions of an STL file")

    parser.add_argument("stlfile", type=str, help="Path to the STL file")
    parser.add_argument("--version", action="version", help="Show version", version=stldim._version.__str__)
    parser.add_argument("--name", type=str, default=None,
                        help="Name of the object (defaults to filename with special characters replaced by underscores")

    args = parser.parse_args()

    if not os.path.exists(args.stlfile):
        sys.exit(f'ERROR: file args.stlfile was not found!')
    varname = get_varname(args)

    stl_dimensions = get_stl_dimensions(args.stlfile)


# the logic is easy from there

    print("// File:", args.stlfile)
    lst = ['obj =("', args.stlfile, '");']
    obj = ['\t\timport("', args.stlfile, '");']

    print("// X size:", stl_dimensions['xsize'])
    print(f"{varname}_xsize = {stl_dimensions['xsize']};")
    print("// Y size:", stl_dimensions['ysize'])
    print(f"{varname}_ysize = {stl_dimensions['ysize']};")
    print("// Z size:", stl_dimensions['zsize'])
    print(f"{varname}_zsize = {stl_dimensions['zsize']};")
    print("// X position:", stl_dimensions['minx'])
    print(f"{varname}_xposition = {stl_dimensions['minx']};")
    print("// Y position:", stl_dimensions['miny'])
    print(f"{varname}_yposition = {stl_dimensions['miny']};")
    print("// Z position:", stl_dimensions['minz'])
    print(f"{varname}_zposition = {stl_dimensions['minz']};")

    # --------------------
    print("NE=1; NW=2; SW=3; SE=4; CTR=5; CTRXY=6;")

    print(f"module {varname}_obj2origin (where) {{")
    print("\tif (where == NE) {")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == NW) {")
    print("\t\ttranslate([", -stl_dimensions['xsize'], ",", 0, ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == SW) {")
    print("\t\ttranslate([", -stl_dimensions['xsize'], ",", -stl_dimensions['ysize'], ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == SE) {")
    print("\t\ttranslate([", 0, ",", -stl_dimensions['ysize'], ",", 0, ",", "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == CTR) {")
    print("\ttranslate([", -stl_dimensions['midx'], ",", -stl_dimensions['midy'], ",", -stl_dimensions['midz'], "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == CTRXY) {")
    print("\ttranslate([", -stl_dimensions['midx'], ",", -stl_dimensions['midy'], ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("}")
    print("")

    print(f"module {varname}_objNE () {{")
    print("\ttranslate([", -stl_dimensions['minx'], ",", -stl_dimensions['miny'], ",", -stl_dimensions['minz'], "])")
    print("".join(obj))
    print("}")


if __name__ == '__main__':
    main()
