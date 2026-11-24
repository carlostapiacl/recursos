#!/usr/bin/env python3
# Line survival by week of writing.
# https://github.com/carlostapiacl/recursos/tree/master/intermedio/supervivencia-de-codigo
# Usage: python3 survival.py <repo> <branch> <since YYYY-MM-DD> [--with-tests] [--exclude REGEX]
import collections, datetime as dt, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

repo, branch, since = sys.argv[1], sys.argv[2], dt.date.fromisoformat(sys.argv[3])
with_tests = "--with-tests" in sys.argv
EXCLUDE = re.compile(sys.argv[sys.argv.index("--exclude") + 1]) if "--exclude" in sys.argv else None  # generated files
CODE = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".kt", ".rb",
          ".php", ".dart", ".vue", ".swift", ".c", ".cpp", ".cs", ".sh", ".sql"}
TEST = re.compile(r"(^|/)(tests?|__tests__|spec)/|_test\.|\.test\.|\.spec\.|Test\.php$")

def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, errors="replace").stdout
def counts(f): return (os.path.splitext(f)[1] in CODE and (with_tests or not TEST.search(f))
                       and not (EXCLUDE and EXCLUDE.search(f)))
def monday(d): return d - dt.timedelta(days=d.weekday())

def snapshot(sunday):
    sha = git("rev-list", "-1", "--first-parent", f"--before={sunday}T23:59:59", branch).strip()
    week, added, sha_c = {}, collections.Counter(), None
    for l in git("log", sha, f"--since={since}", "--numstat", "--format=@%H %ad", "--date=short").splitlines():
        if l.startswith("@"):
            sha_c, d = l[1:].split(); week[sha_c] = monday(dt.date.fromisoformat(d))
        elif l.count("\t") == 2 and l.split("\t")[0].isdigit() and counts(l.split("\t")[2]):
            added[sha_c] += int(l.split("\t")[0])
    def blame(f):
        return collections.Counter(l[:40] for l in git("blame", "--line-porcelain", sha, "--", f).splitlines()
                                   if re.match(r"[0-9a-f]{40} \d+ \d+", l))
    alive = collections.Counter()
    files = [f for f in git("ls-tree", "-r", "--name-only", sha).splitlines() if counts(f)]
    with ThreadPoolExecutor(8) as ex:
        for c in ex.map(blame, files): alive.update(c)
    table = collections.defaultdict(lambda: [0, 0])
    for c, n in added.items():
        table[week[c]][0] += n; table[week[c]][1] += min(alive[c], n)
    return table

sundays, d = [], monday(since) + dt.timedelta(days=6)
while d <= dt.date.today(): sundays.append(d); d += dt.timedelta(days=7)
snaps = {d: snapshot(d) for d in sundays}

print("week,lines," + ",".join(f"wk{k}" for k in range(1, len(sundays) + 1)))
for i, s in enumerate(monday(d) for d in sundays):
    row = [snaps[d][s] for d in sundays[i:] if snaps[d][s][0]]
    if row:
        print(f"{s},{row[-1][0]}," + ",".join(f"{v / a:.1%}" for a, v in row))
