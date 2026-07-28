import os
from glob import glob
import sqlite3 as sql


from cif_read import map_crystal

filepath = "D:/COD database/cif/branch batches/Batch 1/1/10"

result = [y for x in os.walk(filepath) for y in glob(os.path.join(x[0], '*.cif'))]
coords = []
for cif_path in result:
    out = map_crystal(cif_path)
    for coord_pair in out:
        coords.append(coord_pair)
print(coords)
con = sql.connect("testcod.db")
cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='codheatmap'")
if not res.fetchone():
    cur.execute("CREATE TABLE codheatmap(RowNo, ColNo)")
cur.executemany("INSERT INTO codheatmap VALUES(?,?)", coords)
con.commit()
