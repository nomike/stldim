import os
import re

import stl
from stl import mesh


def sanitize_filename(stlfile):
    """
    Replace every non-alphanumeric character with an underscore
    """
    return re.sub(r'\W', '_', os.path.basename(stlfile)).lower()


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

    stl_dimensions['minx'], stl_dimensions['maxx'], stl_dimensions['miny'], stl_dimensions[
        'maxy'], stl_dimensions['minz'], stl_dimensions['maxz'] = find_mins_maxs(main_body)

    stl_dimensions['minx'] = round(stl_dimensions['minx'], 3)
    stl_dimensions['maxx'] = round(stl_dimensions['maxx'], 3)
    stl_dimensions['miny'] = round(stl_dimensions['miny'], 3)
    stl_dimensions['maxy'] = round(stl_dimensions['maxy'], 3)
    stl_dimensions['minz'] = round(stl_dimensions['minz'], 3)
    stl_dimensions['maxz'] = round(stl_dimensions['maxz'], 3)

    stl_dimensions['xsize'] = round(
        stl_dimensions['maxx']-stl_dimensions['minx'], 3)
    stl_dimensions['ysize'] = round(
        stl_dimensions['maxy']-stl_dimensions['miny'], 3)
    stl_dimensions['zsize'] = round(
        stl_dimensions['maxz']-stl_dimensions['minz'], 3)

    stl_dimensions['midx'] = round(stl_dimensions['xsize']/2, 3)
    stl_dimensions['midy'] = round(stl_dimensions['ysize']/2, 3)
    stl_dimensions['midz'] = round(stl_dimensions['zsize']/2, 3)

    return stl_dimensions
