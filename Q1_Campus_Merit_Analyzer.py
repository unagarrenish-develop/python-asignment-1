"""Q1: Campus Merit Analyzer
Run: python Q1_Campus_Merit_Analyzer.py < input.txt
Input: n k m, followed by n records: enrollment name semester cpi and m marks.
"""
import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    try:
        n, k, m = int(next(it)), int(next(it)), int(next(it))
        if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
            raise ValueError("n, k, or m is outside the allowed range")
        students = []
        for _ in range(n):
            enrollment = next(it)
            name = next(it)
            semester = int(next(it))
            cpi = float(next(it))
            marks = tuple(int(next(it)) for _ in range(m))
            if not (1 <= semester <= 8 and 0 <= cpi <= 10 and all(0 <= x <= 100 for x in marks)):
                raise ValueError("Invalid semester, CPI, or marks")
            students.append({"enrollment": enrollment, "name": name, "semester": semester,
                             "cpi": cpi, "marks": marks, "average": sum(marks) / m})
        groups = {}
        for student in students:
            groups.setdefault(student["semester"], []).append(student)
        for semester in sorted(groups):
            ranked = sorted(groups[semester],
                            key=lambda s: (-s["cpi"], -s["average"], s["enrollment"]))
            print(f"Semester {semester}:", *[s["enrollment"] for s in ranked[:k]])
        for j in range(m):
            highest = max(s["marks"][j] for s in students)
            toppers = sorted(s["enrollment"] for s in students if s["marks"][j] == highest)
            print(f"S{j + 1}:", *toppers)
    except (StopIteration, ValueError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
