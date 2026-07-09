
def read_site_line(line, dict, col_labels):
    """function for adding each part of the atom site column to the dictionary"""
    split = line.split()
    for i, label in zip(range(0, (len(col_labels))), col_labels):
        if "atom fract" in label:
            split_fract = split[i].split("(")
            dict[label].append(float(split_fract[0]))
        else:
            dict[label].append(split[i])
    return dict
