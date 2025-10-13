import json, re, csv

with open("/Users/sanjeevchoubey/Downloads/Redis-Enterprisev7_22-SBOM-cyclonedx.json") as f:
    data = json.load(f)

deps = set()

# 1. Extract from components (most reliable: has name+version)
components = data.get("components", [])
for comp in components:
    name = comp.get("name")
    version = comp.get("version")
    if name and version:
        deps.add((name, version))

# 2. Extract from dependencies (ref/dependsOn package URLs)
dependencies = data.get("dependencies", [])
for dep in dependencies:
    for field in ["ref"] + dep.get("dependsOn", []):
        m = re.search(r"pkg:[^/]+/([^@]+)@([^?]+)", field)
        if m:
            deps.add((m.group(1), m.group(2)))

# Write to CSV
with open("/Users/sanjeevchoubey/Downloads/deps.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["dependency", "version"])
    writer.writerows(sorted(deps))