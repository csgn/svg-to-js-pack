import os
import sys
import re

def usage():
    print("USAGE:\n\tpython svg.py <source_path> <destination_path>")
    sys.exit(1)


def main(source, destination):
    icons = [i for i in os.listdir(source) if ".svg" in i]
    comps = {}
    new_comps = []

    for i in icons:
        with open(f'{source}/{i}', "r") as f:
            comps[i] = f.read()

    for k, v in comps.items():
        new_v = re.sub("stroke+([\-]?)*([\w]*)+([\=]?)+\"+\W*\w*\"", " ", v)
        x, y = k.split('.')
        l = "Icon" + "".join([ i.capitalize() for i in x.split('-') ])

        c = {
            "file_name": k,
            "component_name": l,
            "content": new_v
        }

        new_comps.append(c)

    js_pack = []
    for i in new_comps:
        x, y, z = i.items()

        if not os.path.exists(destination + '/assets'):
            os.mkdir(destination + '/assets/')

        dest = destination + '/assets/' + i[x[0]]

        with open(dest, "w") as f:
            print(i[y[0]], "[OK]")
            try:
                f.write(i[z[0]])
            except:
                continue
        
        o = f"export {{ ReactComponent as {i[y[0]]} }} from \'./assets/{i[x[0]]}';"
        js_pack.append(o)

    with open(destination + '/index.js', "w") as f:
        for i in js_pack:
            f.write(i + '\n')
        
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    source = sys.argv[1]
    destination = sys.argv[2]

    if not os.path.exists(source):
        usage()

    if not os.path.exists(destination):
        os.mkdir(destination)

    main(source, destination)
   
