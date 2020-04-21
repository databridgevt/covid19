import yaml

from pyprojroot import here

with open(here("environment.yml")) as file:
    env = yaml.load(file, Loader=yaml.FullLoader)

deps = env["dependencies"]
pip = deps.pop(-1)["pip"]

deps.remove('make=4.3')
deps.remove('python=3.8.2')

deps_eql = map(lambda x: x.replace("=", "=="), deps)

all_deps = list(deps_eql) + pip

print(all_deps)

with open(here('requirements.txt'), 'w') as f:
    for py_pkg in all_deps:
        f.write(f"{py_pkg}\n")
