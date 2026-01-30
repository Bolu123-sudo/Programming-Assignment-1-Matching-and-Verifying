import sys

#reads the input
reading = sys.stdin.read()
if reading.strip() == "":
    exit()
inp = reading.splitlines()
count = int(inp[0])

#some edge cases
if count == 0:
    exit()
if len(inp) < (1+count+count):
    exit()



#create arrays for hospitals and students
hospital = []
student = []


def parse(x):
    nums = x.split()
    row = []
    j = 0
    while j < len(nums):
        row.append(int(nums[j]) - 1)
        j = j + 1
    return row

i =1
while i < (1 + count):
    hospital.append(parse(inp[i]))
    i = i+1

j = 1 + count
while j < (1 + count + count):
    student.append(parse(inp[j]))
    j = j+1

#student rank
studentRank = []
for i in range(count):
    rank = [0] * count
    for j in range(count):
        stu = student[i][j]
        rank[stu] = j
    studentRank.append(rank)

#algo
tracker = [0] * count
hospitalMatch = [-1] * count
studentMatch = [-1] * count
while True:
    hos = -1
    i = 0
    while i < count:
        if hospitalMatch[i] == -1:
            if(tracker[i] < count):
                hos = i
                break
        i = i + 1
    if hos == -1:
        break
    stu = hospital[hos][tracker[hos]]
    tracker[hos] = tracker[hos] + 1

    if studentMatch[stu] == -1:
        studentMatch[stu] = hos
        hospitalMatch[hos] = stu
    else:
        cur = studentMatch[stu]
        if studentRank[stu][hos] < studentRank[stu][cur]:
            studentMatch[stu] = hos
            hospitalMatch[hos] = stu
            hospitalMatch[cur] = -1

for i in range(count):
    print(i + 1, hospitalMatch[i] + 1)
