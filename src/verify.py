import sys

def fail(msg):
    print(msg)
    sys.exit(0)


def readInput():
    raw = sys.stdin.read()
    if raw.strip() == "":
        fail("INVALID: empty input")

    lines = raw.splitlines()
    clean = []
    i = 0
    while i < len(lines):
        if lines[i].strip() != "":
            clean.append(lines[i].strip())
        i = i + 1
    return clean



def parsePref(line, n):
    parts = line.split()
    if len(parts) != n:
        fail("INVALID: preference line wrong length")

    seen = [False] * n
    row = []
    i = 0
    while i < len(parts):
        p = parts[i]
        if not p.lstrip("-").isdigit():
            fail("INVALID: non-integer in preferences")

        x = int(p) - 1
        if x < 0 or x >= n:
            fail("INVALID: preference out of range")

        if seen[x]:
            fail("INVALID: duplicate in preference list")

        seen[x] = True
        row.append(x)
        i = i + 1

    return row


def loadPrefs(lines):
    if len(lines) < 1:
        fail("INVALID: missing n")

    if not lines[0].lstrip("-").isdigit():
        fail("INVALID: n not integer")

    n = int(lines[0])
    if n < 0:
        fail("INVALID: n negative")

    if n == 0:
        return 0, [], []

    if len(lines) < (1 + 2 * n):
        fail("INVALID: not enough preference lines")

    hospital = []
    student = []

    i = 1
    while i < 1 + n:
        hospital.append(parsePref(lines[i], n))
        i = i + 1

    j = 1 + n
    while j < 1 + 2 * n:
        student.append(parsePref(lines[j], n))
        j = j + 1

    return n, hospital, student


def loadMatching(path, n):
    try:
        text =open(path, "r").read()
    except:
        fail("INVALID: cannot open matching file")

    rawLines = text.splitlines()
    lines = []
    i = 0
    while i < len(rawLines):
        if rawLines[i].strip() != "":
            lines.append(rawLines[i].strip())
        i = i + 1

    if n == 0:
        if len(lines) != 0:
            fail("INVALID: expected empty matching for n=0")
        return [], []

    if len(lines) != n:
        fail("INVALID: matching does not have exactly n lines")

    matchH = [-1] * n
    matchS = [-1] * n
    usedH = [False] * n
    usedS = [False] * n

    k = 0
    while k < len(lines):
        parts = lines[k].split()
        if len(parts) != 2:
            fail("INVALID: matching line must have 2 integers")

        a = parts[0]
        b = parts[1]

        if not a.lstrip("-").isdigit() or not b.lstrip("-").isdigit():
            fail("INVALID: non-integer in matching")

        h = int(a) - 1
        s = int(b) - 1

        if h < 0 or h >= n or s < 0 or s >= n:
            fail("INVALID: matching out of range")

        if usedH[h]:
            fail("INVALID: duplicate hospital in matching")
        if usedS[s]:
            fail("INVALID: duplicate student in matching")

        usedH[h] = True
        usedS[s] = True
        matchH[h] = s
        matchS[s] = h

        k = k + 1

    i = 0
    while i < n:
        if matchH[i] == -1:
            fail("INVALID: hospital unmatched")
        i = i + 1

    j = 0
    while j < n:
        if matchS[j] == -1:
            fail("INVALID: student unmatched")
        j = j + 1

    return matchH, matchS


def buildRanks(hospital, student, n):
    hospitalRank = []
    i = 0
    while i < n:
        rank = [0] * n
        j = 0
        while j < n:
            s = hospital[i][j]
            rank[s] = j
            j = j + 1
        hospitalRank.append(rank)
        i = i + 1

    studentRank = []
    i = 0
    while i < n:
        rank = [0] * n
        j = 0
        while j < n:
            h = student[i][j]
            rank[h] = j
            j = j + 1
        studentRank.append(rank)
        i = i + 1

    return hospitalRank, studentRank


def checkStable(matchH, matchS, hospitalRank, studentRank, n):
    h = 0
    while h < n:
        assigned = matchH[h]
        cutoff = hospitalRank[h][assigned]

        s = 0
        while s < n:
            if hospitalRank[h][s] < cutoff:
                curH = matchS[s]
                if studentRank[s][h] < studentRank[s][curH]:
                    fail("UNSTABLE: blocking pair (" + str(h + 1) + ", " + str(s + 1) + ")")
            s = s + 1

        h = h + 1

    print("VALID STABLE")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify.py < preferences.in matching.out")
        sys.exit(0)

    lines = readInput()
    n, hospital, student = loadPrefs(lines)

    matchH, matchS = loadMatching(sys.argv[1], n)

    if n == 0:
        print("VALID STABLE")
        return

    hospitalRank, studentRank = buildRanks(hospital, student, n)
    checkStable(matchH, matchS, hospitalRank, studentRank, n)


if __name__ == "__main__":
    main()
