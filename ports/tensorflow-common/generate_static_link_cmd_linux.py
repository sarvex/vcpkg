import re
import sys

params_path = sys.argv[2]
version = sys.argv[3]
lib_suffix = "" if len(sys.argv) < 5 else sys.argv[4]

with open(sys.argv[1], "r") as f_in:
    with open("static_link.sh", "w") as f_out:
        p_cd = re.compile(r"^\((cd .*) && \\$")
        p_linker = re.compile(fr"^\s*(.+)gcc.+(@bazel-out\S+libtensorflow{lib_suffix}\.so\.\d+\.\d+\.\d+-2\.params).*")
        f_out.write("#!/bin/bash\n# note: ar/binutils version 2.27 required to support output files > 4GB\n")
        env = []
        for line in f_in:
            if line.startswith("(cd"):
                # new command, reset
                env = [line]
            elif m1 := p_linker.match(line):
                m2 = p_cd.match(env[0])
                f_out.write(m2[1] + "\n")
                line = f'"{m1[1]}ar" rcs {m1[2][1:-9].replace(".so", ".a")} {m1[2].replace(".so", ".a")}\n'
                f_out.write(line)
            else:
                env.append(line)
