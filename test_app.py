from cif_read import read_cif, cif_read_lattice, create_plane_groups
import numpy as np


def test_cif_code():
    filepath = "COMP702/app_latices/CIF_files/1000047.cif"
    test_out = read_cif(filepath)
    assert test_out["Code"] == 1000047


def test_cif_title():
    filepath = "COMP702/app_latices/CIF_files/1100509.cif"
    test_out = read_cif(filepath)
    assert test_out['Title'] == "New Homochiral Ligands Bearing Nonstereogenic Chirotopic Centers. Lithiated N,N'-Dialkylureas as Chiral Bases and Sterically Crowded Phosphines for Asymmetric Catalysis"


def test_cif_planes():
    files = ["1000047", "1100509", "1544392", "1544359"]
    tests = []
    for path in files:
        filepath = f"COMP702/app_latices/CIF_files/{path}.cif"
        lat_dict = cif_read_lattice(filepath)
        pl_dict = create_plane_groups(lat_dict)
        for plane in pl_dict.keys():
            vectors = []
            for vect in pl_dict[plane].values():
                if len(vectors) == 3:
                    continue
                else:
                    vectors.append(vect)
            vect_lens = []
            for v in vectors:
                vect_lens.append(np.sqrt(v[0] ** 2 + v[1] ** 2))
            if vect_lens[0] <= vect_lens[1] and vect_lens[1] <= vect_lens[2]:
                tests.append(True)
            else:
                tests.append(False)
    assert all(tests)
