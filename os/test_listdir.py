import os

print(os.getcwd())

l = os.listdir()
print(l)
assert "test_listdir.py" in l
assert "os" in l
