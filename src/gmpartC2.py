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

# Gale–Shapley matcher
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

    return hospitalMatch, studentMatch

# Build rank tables for verifier
def buildRanks(hospital, student, n):
    hospitalRank = []
    i = 0
    while i < n:
        rank = [0] * n
        j = 0
        while j < n:
            rank[hospital[i][j]] = j
            j = j + 1
        hospitalRank.append(rank)
        i = i + 1

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

    return hospitalRank, studentRank

# Verify validity and stability
def verify(hospital, student, matchH, matchS, n):

    usedS = [False] * n
    i = 0
    while i < n:
        s = matchH[i]
        if s < 0 or s >= n:
            return False
        if usedS[s]:
            return False
        usedS[s] = True
        if matchS[s] != i:
            return False
        i = i + 1

    hospitalRank, studentRank = buildRanks(hospital, student, n)

    h = 0
    while h < n:
        assigned = matchH[h]
        cutoff = hospitalRank[h][assigned]
        s = 0
        while s < n:
            if hospitalRank[h][s] < cutoff:
                curH = matchS[s]
                if studentRank[s][h] < studentRank[s][curH]:
                    return False
            s = s + 1
        h = h + 1

    return True

def main():
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    data = []

    for n in sizes:
        hospital, student = generate(n)
        matchH, matchS = galeshapley(hospital, student, n)

        start = time.perf_counter()
        ok = verify(hospital, student, matchH, matchS, n)
        end = time.perf_counter()

        if not ok:
            print("Verifier failed at n =", n)

        t = end - start
        data.append((n, t))
        print(n, t)

    out = open("verifier_times.csv", "w", newline="")
    w = csv.writer(out)
    w.writerow(["n", "time"])
    for d in data:
        w.writerow(d)
    out.close()

if __name__ == "__main__":
    main()
