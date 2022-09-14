import json

with open("packages.json", "r") as f:
  pkgs = json.load(f)

totalpkgs = len(pkgs)

revs = {}


for pkg in pkgs:
  revs[pkg] = []
  for pkg2 in pkgs:
    if pkg in pkgs[pkg2]:
      revs[pkg].append(pkg2)

with open("rev_packages.json", "w") as f:
    f.write(json.dumps(revs, indent=4))


def add_all_dependencies(pkg):
    mygroup = []
    deplist = pkgs.pop(pkg)
    revlist = revs.pop(pkg)
    mygroup.append(pkg)
    mygroup.extend(deplist)
    mygroup.extend(revlist)
    for pkg2 in deplist:
      if pkg2 in list(pkgs):
        mygroup.extend(add_all_dependencies(pkg2))
    for pkg2 in revlist:
      if pkg2 in list(revs):
        mygroup.extend(add_all_dependencies(pkg2))
    return mygroup

groups = {}

keylist = list(pkgs.keys())

for pkg in keylist:
  if pkg in list(pkgs) and len(pkgs[pkg]) == 0:
    mygroup = []
    mykey = ""
    for key in groups:
      if pkg in groups.get(key,[]):
        mykey = key
        mygroup = groups[key]
    if not mykey:
      mykey = pkg
    mygroup.extend(add_all_dependencies(pkg))
    groups[mykey] = list(set(mygroup))

total = 0

for g in groups:
  total += len(groups[g])
  print(len(groups[g]))

if total == totalpkgs:
  print(f"Successfully groups {total} packages in {len(groups)} groups.")
else:
  print(f"Total number of packages in groups {total} is different than total number of packages {totalpkgs}")

