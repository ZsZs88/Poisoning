from random import randint
import sys

IDX = int(sys.argv[1])

with open("random", "r") as f:
    already_in = list(map(lambda x : int(x), f.readline().strip().split(" ")))
new = []

i = 0
while i < IDX:
    random_int = randint(0, 199)
    if random_int not in already_in:
        already_in.append(random_int)
        new.append(random_int)
        i += 1
already_in.sort()
new.sort()
with open("random", "w") as f:
    f.write(" ".join(list(map(lambda x: str(x), already_in))))
print(" ".join(list(map(lambda x: str(x), new))))
