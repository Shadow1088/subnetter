import math

amount = int(input("\nEnter the amount of subnets you would like to be created: "))
iprange = int(input("\nShould all subnets have the same range for hosts? If so, type the number of max hosts, else write 0: "))
totalhosts = 0
ranges = []
masks = []

if iprange:
    for i in range(amount):
        n = (2**math.ceil(math.log2(iprange)))
        totalhosts = totalhosts+n
        ranges.append(n)
        masks.append(32-math.ceil(math.log2(iprange)))

else:
    for i in range(amount):
        n = 2**math.ceil(math.log2(int(input(f"\nEnter the range for the {i+1}. subnet: "))+2))
        totalhosts = totalhosts+n
        ranges.append(n)
        masks.append(int(32-math.log2(n)))


network = input("\nWhat private network IP class to use? (A=over a milion IPs; B=up to a milion; C=under 65k)\n")

if (totalhosts<65536) and (network=="C"):
    network="192.168.0.0"
elif (totalhosts<1_048_576) and ((network=="B") or (network=="C")):
    network="172.16.0.0"
elif network in "ABC":
    if network in "AB":
        print("Too many hosts for the IP class, picking class C...\n")
    network="10.0.0.0"
else:
    print("Something went wrong, maybe invalid input?")
print(f"Selected network: {network}")

sep = network.split(".")
binarysep = bin(int(sep[0])).zfill(10) + bin(int(sep[1])).zfill(10) + bin(int(sep[2])).zfill(10) + bin(int(sep[3])).zfill(10)

newbinarysep = ""
for i, j in enumerate(binarysep):
    if j=="b":
        newbinarysep = newbinarysep[:-1]
    else:
        newbinarysep+=j

for i in range(amount):
    chunks = []
    endchunks = []

    for j in range(0, len(newbinarysep), 8):
        chunks.append(str(int(newbinarysep[j:j+8],2)))


    print(f'Network address   of {i+1}. subnet: {".".join(chunks)}   /{masks[i]}')

    newbinarysep = (bin(int(newbinarysep, 2)+ranges[i]))[2:].zfill(32)
    endbinsep = bin(int(newbinarysep,2)-int("1",2))[2:].zfill(32)

    for j in range(0, len(endbinsep), 8):
        endchunks.append(str(int(endbinsep[j:j+8],2)))

    print(f'Broadcast address of {i+1}. subnet: {".".join(endchunks)} /{masks[i]}')
