from packaging.version import parse as Version

v = Version("1!1.0.0dev1")
v2 = Version("2!1.0.0dev1")

print(v.base_version)
print(v.dev)
print(v.epoch)
print(v.major)
print(v.minor)
print(v.micro)
print(v.post)
print(v.pre)

print(v <= v2)
