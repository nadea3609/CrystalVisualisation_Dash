import numpy as np


def cif_read_lattice(filepath):
    """
    This function reads only the lattice information from the input CIF file
    if there is an error in either the cell lengths or the cell angles, it sets them to -1,
    which will be interpreted as an error value by later functions
    """
    out = {
        "Cell_lengths": [],
        "Cell_angles": []
    }
    with open(filepath, 'r') as cif:
        for line in cif:
            if "#" in line:
                continue
            elif "_cell_length" in line:
                split = line.split(maxsplit=1)
                split2 = split[1].split("(")
                length = split2[0].strip(" ")
                try:
                    out["Cell_lengths"].append(float(length))
                except ValueError:
                    out["Cell_lengths"].append(-1)
            elif "_cell_angle" in line:
                split = line.split(maxsplit=1)
                split2 = split[1].split("(")
                angle = split2[0].strip(" ")
                try:
                    out["Cell_angles"].append(float(angle))
                except ValueError:
                    out["Cell_angles"].append(-1)
            else:
                continue
    return out


def compare(dict, val1, val2):
    """function to compare two vectors of a 2D unit cell and insert them into a dictionary"""
    checks = (val1 == -1, val2 == -1, dict["ang"] == -1)
    if any(checks):
        dict["v1"] = -1
        dict["v2"] = -1
        dict["v0"] = -1
        dict["ang"] = -1
        return dict
    if val1 >= val2 and dict["ang"] == 90:
        dict["v1"][0] = val2
        dict["v2"][1] = val1
    elif val1 >= val2 and dict["ang"] > 90:
        dict["v1"][0] = val2
        dict["v2"][1] = val1 * np.sin(dict["ang"] * (np.pi/180))
        dict["v2"][0] = val1 * np.cos(dict["ang"] * (np.pi/180))
    elif val2 >= val1 and dict["ang"] == 90:
        dict["v1"][0] = val1
        dict["v2"][1] = val2
    elif val2 >= val1 and dict["ang"] > 90:
        dict["v1"][0] = val1
        dict["v2"][1] = val2 * np.sin(dict["ang"] * (np.pi/180))
        dict["v2"][0] = val2 * np.cos(dict["ang"] * (np.pi/180))
    elif val1 >= val2 and dict["ang"] < 90:
        ang_corr = 180 - dict["ang"]
        dict["v1"][0] = val2
        dict["v2"][1] = val1 * np.sin(ang_corr * (np.pi/180))
        dict["v2"][0] = val1 * np.cos(ang_corr * (np.pi/180))
    elif val2 >= val1 and dict["ang"] < 90:
        ang_corr = 180 - dict["ang"]
        dict["v1"][0] = val1
        dict["v2"][1] = val2 * np.sin(ang_corr * (np.pi/180))
        dict["v2"][0] = val2 * np.cos(ang_corr * (np.pi/180))
    dict["v0"] = -(dict["v1"] + dict["v2"])
    return dict


def create_plane_groups(in_dict):
    """
    This function extracts the side lengths and angles for the three key planes of the unit cell
    """
    out_dict = {
        'ab': dict(v1=np.zeros(2, dtype=float),
                   v2=np.zeros(2, dtype=float),
                   v0=np.zeros(2, dtype=float),
                   ang=in_dict["Cell_angles"][2]),
        'bc': dict(v1=np.zeros(2, dtype=float),
                   v2=np.zeros(2, dtype=float),
                   v0=np.zeros(2, dtype=float),
                   ang=in_dict["Cell_angles"][0]),
        'ac': dict(v1=np.zeros(2, dtype=float),
                   v2=np.zeros(2, dtype=float),
                   v0=np.zeros(2, dtype=float),
                   ang=in_dict["Cell_angles"][1])
    }
    length_a = in_dict["Cell_lengths"][0]
    length_b = in_dict["Cell_lengths"][1]
    length_c = in_dict["Cell_lengths"][2]    
    out_dict["ab"] = compare(out_dict["ab"], length_a, length_b)
    out_dict["bc"] = compare(out_dict["bc"], length_b, length_c)
    out_dict["ac"] = compare(out_dict["ac"], length_a, length_c)
    return out_dict


def create_pinv(plane_dict):
    """
    This function calculates the root and subsequently the projected invariants
    of a given 2D lattice
    """
    r12 = np.sqrt(-np.dot(plane_dict["v1"], plane_dict["v2"]))
    r01 = np.sqrt(-np.dot(plane_dict["v0"], plane_dict["v1"]))
    r02 = np.sqrt(-np.dot(plane_dict["v0"], plane_dict["v2"]))
    rsort = sorted([r12, r01, r02])
    out = {
            'r12': np.round(rsort[0], 4),
            'r01': np.round(rsort[1], 4),
            'r02': np.round(rsort[2], 4)
            }
    return out


def pinv_coords(inv_dict):
    """
    takes the projected invatiants and outputs 
    the x and y co-ordiantes of the lattice on the QT
    """
    size = inv_dict['r12'] + inv_dict['r01'] + inv_dict['r02']
    x = float(np.round((inv_dict['r02'] - inv_dict['r01'])/ size, 3))
    y = float(np.round((3 * inv_dict['r12']) / size, 3))
    # if x > 1 or y > 1:
    #     raise ValueError("Error with calculation of projected invariant coordiantes")
    return (x, y)


def map_crystal(filepath):
    """performs cif_read_lattice, create_plane_groups, create_pinv and pinv_coords in bulk"""
    try:
        cif_dict = cif_read_lattice(filepath)
    except ValueError as ev:
        cif_name = filepath.split("/")
        return f"Error with reading {cif_name[-1]}, {ev}"
    except IndexError as ei:
        cif_name = filepath.split("/")
        return f"Error with reading {cif_name[-1]}, {ei}"
    try:
        pl_dict = create_plane_groups(cif_dict)
    except ValueError as ev:
        cif_name = filepath.split("/")
        return f"Error with processing {cif_name[-1]}, {ev}"
    except IndexError as ei:
        cif_name = filepath.split("/")
        return f"Error with processing {cif_name[-1]}, {ei}"
    out_coords = []
    for plane in pl_dict.keys():
        pi_dict = create_pinv(pl_dict[plane])
        try:
            coords = pinv_coords(pi_dict)
        except ValueError as e:
            cif_name = filepath.split("/")
            print(f"Error encountered with {cif_name[-1]}, {e}")
        else:
            out_coords.append(coords)
    return out_coords
