import pandas as pd

from cif_read_site_cols import read_site_line


def read_cif(filepath):
    """This function reads and extracts information from an input CIF file"""
    out = {
        "Author": [],
        "Title": "",
        "Journal": "",
        "Year": "",
        "Code": "",
        "Formula": "",
        "Name": "",
        "Cell_lengths": [],
        "Atom_sites": None
    }
    author_flag = False
    title_flag = False
    title_parts = []
    atom_site_flag = False
    site_cols = []
    site_dict = {}
    atom_type_flag = False
    with open(filepath, 'r') as cif:
        for line in cif:
            if "_publ_section_title" in line:
                title_flag = True
            elif "_atom_site" in line:
                atom_site_flag = True
            elif "_atom_type" in line:
                atom_type_flag = True
            if author_flag:
                if "_" in line:
                    author_flag = False
                    continue
                author = line.strip("' \n")
                out["Author"].append(author)
            if title_flag:
                if ";" in line and not title_parts:
                    continue
                elif not title_parts:
                    part = line.strip(" \n")
                    if part[-1] == "-":
                        title_parts.append(part)
                    else:
                        part = part + " "
                        title_parts.append(part)
                elif ";" not in line:
                    part = line.strip(" \n")
                    if part[-1] == "-":
                        title_parts.append(part)
                    else:
                        part = part + " "
                        title_parts.append(part)
                elif ";" in line and len(title_parts) >= 1:
                    title_flag = False
                    full_title = ""
                    for part in title_parts:
                        full_title = full_title + part
                    out["Title"] = full_title.rstrip()
            if atom_site_flag:
                if "_" in line and not site_dict:
                    split = line.split("_")
                    split.pop(0)
                    split.pop(1)
                    joined = ""
                    for word in split:
                        stripped = word.strip(" \n")
                        if not joined:
                            joined = stripped
                        else:
                            joined = joined + " " + stripped
                    joined.strip()
                    site_cols.append(joined)
                elif "_" not in line and not site_dict:
                    for col in site_cols:
                        site_dict[col] = []
                    site_dict = read_site_line(line, site_dict, site_cols)
                elif "_" not in line and len(site_cols) >= 1:
                    site_dict = read_site_line(line, site_dict, site_cols)
                elif "_" in line and len(site_cols) == len(site_dict):
                    atom_site_flag = False
                    site_df = pd.DataFrame(site_dict)
                    out['Atom_sites'] = site_df
            if "#" in line:
                continue
            elif "_publ_author_name" in line:
                author_flag = True
                continue
            elif "_journal_name_full" in line:
                split = line.split(maxsplit=1)
                j_name = split[1].strip(" '\n")
                out["Journal"] = j_name
            elif "_journal_year" in line:
                split = line.split(maxsplit=1)
                year = split[1].strip(" \n")
                out['Year'] = year
            elif "_chemical_formula_sum" in line:
                split = line.split(maxsplit=1)
                formula = split[1].strip(" '\n")
                out["Formula"] = formula
            elif "_chemical_name_mineral" in line:
                split = line.split(maxsplit=1)
                name = split[1].strip(" '\n")
                out["Name"] = name
            elif "_cell_length" in line:
                split = line.split(maxsplit=1)
                split2 = split[1].split("(")
                length = split2[0].strip(" ")
                out["Cell_lengths"].append(float(length))
            elif "_cod_database_code" in line:
                split = line.split(maxsplit=1)
                code = split[1].strip(" '\n")
                out['Code'] = int(code)
    return out


def split_fract_coords(cif_dict):
    """
    This function splits the fractional x, y and z co-ordinates of the atoms in the cif file into
    three pairs of co-ordinates for three key sides of the unit cell
    """
    df = cif_dict["Atom_sites"]
    fract_x = []
    fract_y = []
    fract_z = []
    for idx, row in df.iterrows():
        fract_x.append(row['atom fract x'])
        fract_y.append(row['atom fract y'])
        fract_z.append(row['atom fract z'])
    out_dict = {
        'xy': dict(x=fract_x, y=fract_y),
        'yz': dict(y=fract_y, z=fract_z),
        'xz': dict(x=fract_x, z=fract_z)
    }
    return out_dict


filepath = "COMP702/app_latices/CIF_files/1000047.cif"
dict = read_cif(filepath)
print(dict)
