import random
import time
import csv

# Generate random preference lists
def randomizer(n):
    row = list(range(n))
    random.shuffle(row)
    return row

def generate(n):
    hospital = []
    student = []
    for i in range(n):
        hospital.append(randomizer(n))

    for i in range(n):
        student.append(randomizer(n))

    return hospital, student


# Gale–Shapley matcher from Part A
def galeshapley(hospital, student, n):
    studentRank = []
    i = 0
    while i < n:
        rank = [0] * n
        j = 0
        while j < n:
            rank[student[i][j]] = j
            j = j + 1
        studentRank.append(rank)
        i = i + 1
    tracker = [0] * n
    hospitalMatch = [-1] * n
    studentMatch = [-1] * n

    while True:
        hos = -1
        i = 0
        while i < n:
            if hospitalMatch[i] == -1 and tracker[i] < n:
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
    return hospitalMatch

def main():
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    data = []

    for n in sizes:
        h, s = generate(n)
        start = time.perf_counter()
        galeshapley(h, s, n)
        end = time.perf_counter()
        t = end - start
        data.append((n, t))
        print(n, t)

    out = open("matcher_times.csv", "w", newline="")
    w = csv.writer(out)
    w.writerow(["n", "time"])
    for d in data:
        w.writerow(d)
    out.close()

if __name__ == "__main__":
    main()