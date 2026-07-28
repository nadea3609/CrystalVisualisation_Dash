import numpy as np

# from cif_read_site_cols import read_site_line


# def read_cif(filepath):
#     """This function reads and extracts information from an input CIF file"""
#     out = {
#         "Author": [],
#         "Title": "",
#         "Journal": "",
#         "Year": "",
#         "Code": "",
#         "Formula": "",
#         "Name": "",
#         "Cell_lengths": [],
#         "Cell_angles": [],
#         "Atom_sites": None
#     }
#     author_flag = False
#     title_flag = False
#     title_parts = []
#     atom_site_flag = False
#     site_cols = []
#     site_dict = {}
#     with open(filepath, 'r') as cif:
#         for line in cif:
#             if "_publ_section_title" in line:
#                 title_flag = True
#             elif "_atom_site" in line:
#                 atom_site_flag = True
#             if author_flag:
#                 if "_" in line:
#                     author_flag = False
#                     continue
#                 author = line.strip("' \n")
#                 out["Author"].append(author)
#             if title_flag:
#                 if ";" in line and not title_parts:
#                     continue
#                 elif not title_parts:
#                     part = line.strip(" \n")
#                     if part[-1] == "-":
#                         title_parts.append(part)
#                     else:
#                         part = part + " "
#                         title_parts.append(part)
#                 elif ";" not in line:
#                     part = line.strip(" \n")
#                     if part[-1] == "-":
#                         title_parts.append(part)
#                     else:
#                         part = part + " "
#                         title_parts.append(part)
#                 elif ";" in line and len(title_parts) >= 1:
#                     title_flag = False
#                     full_title = ""
#                     for part in title_parts:
#                         full_title = full_title + part
#                     out["Title"] = full_title.rstrip()
#             if atom_site_flag:
#                 if "_" in line and not site_dict:
#                     split = line.split("_")
#                     split.pop(0)
#                     split.pop(1)
#                     joined = ""
#                     for word in split:
#                         stripped = word.strip(" \n")
#                         if not joined:
#                             joined = stripped
#                         else:
#                             joined = joined + " " + stripped
#                     joined.strip()
#                     site_cols.append(joined)
#                 elif "_" not in line and not site_dict:
#                     for col in site_cols:
#                         site_dict[col] = []
#                     site_dict = read_site_line(line, site_dict, site_cols)
#                 elif "_" not in line and len(site_cols) >= 1:
#                     site_dict = read_site_line(line, site_dict, site_cols)
#                 elif "_" in line and len(site_cols) == len(site_dict):
#                     atom_site_flag = False
#                     site_df = pd.DataFrame(site_dict)
#                     out['Atom_sites'] = site_df
#             if "#" in line:
#                 continue
#             elif "_publ_author_name" in line:
#                 author_flag = True
#                 continue
#             elif "_journal_name_full" in line:
#                 split = line.split(maxsplit=1)
#                 j_name = split[1].strip(" '\n")
#                 out["Journal"] = j_name
#             elif "_journal_year" in line:
#                 split = line.split(maxsplit=1)
#                 year = split[1].strip(" \n")
#                 out['Year'] = year
#             elif "_chemical_formula_sum" in line:
#                 split = line.split(maxsplit=1)
#                 formula = split[1].strip(" '\n")
#                 out["Formula"] = formula
#             elif "_chemical_name_mineral" in line:
#                 split = line.split(maxsplit=1)
#                 name = split[1].strip(" '\n")
#                 out["Name"] = name
#             elif "_cell_length" in line:
#                 split = line.split(maxsplit=1)
#                 split2 = split[1].split("(")
#                 length = split2[0].strip(" ")
#                 out["Cell_lengths"].append(float(length))
#             elif "_cell_angle" in line:
#                 split = line.split(maxsplit=1)
#                 split2 = split[1].split("(")
#                 angle = split2[0].strip(" ")
#                 out["Cell_angles"].append(float(angle))
#             elif "_cod_database_code" in line:
#                 split = line.split(maxsplit=1)
#                 code = split[1].strip(" '\n")
#                 out['Code'] = int(code)
#     return out


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
    dict["v0"][0] = -1 * dict["v1"][0] + -1 * dict["v2"][0]
    dict["v0"][1] = -1 * dict["v1"][1] + -1 * dict["v2"][1]

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
    r12 = np.sqrt(-1 * np.dot(plane_dict["v1"], plane_dict["v2"]))
    r01 = np.sqrt(-1 * np.dot(plane_dict["v0"], plane_dict["v1"]))
    r02 = np.sqrt(-1 * np.dot(plane_dict["v0"], plane_dict["v2"]))
    size = r12 + r01 + r02
    out = {
        'p12': np.round((r12 / size), 4),
        'p01': np.round((r01 / size), 4),
        'p02': np.round((r02 / size), 4)
        }
    return out


def pinv_coords(inv_dict):
    """
    takes the projected invatiants and outputs 
    the x and y co-ordiantes of the lattice on the QT
    """
    return (
            (float(np.round(inv_dict['p02'] - inv_dict['p01'], 3))),
            float(np.round((3 * inv_dict['p12']), 3))
            )


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
        # err_flag = False
        # for value in pl_dict[plane].values():
        #     if not isinstance(value, float):
        #         check = value.any(where=-1)
        #         if check:
        #             err_flag = True
        #     else:
        #         if value == -1:
        #             err_flag = True
        # if err_flag:
        #     continue
        pi_dict = create_pinv(pl_dict[plane])
        coords = pinv_coords(pi_dict)
        out_coords.append(coords)
    return out_coords


# files = []
# f_path = "CIF_files"
# with os.scandir(f_path) as it:
#     for entry in it:
#         if ".cif" in entry.name and entry.is_file():
#             files.append(entry.name)
# for path in files:
#     filepath = f"CIF_files/{path}"
#     test_coords = map_crystal(filepath)
#     print(test_coords)
