# -*- coding: utf-8 -*-
import json, re, collections
from glossary import LING, LING_EXTRA, YIDUOBO, YIDUOBO_EXTRA

A = json.load(open('agg.json'))
S = json.load(open('style.json'))
CJ = json.load(open('concept.json'))
C = CJ['C']
I = json.load(open('idioms.json'))
L, Y = '灵茶山艾府', 'yiduobo'
NF = A['nfiles']
DF = A['df']


def pct(a, k):
    return f'{k / NF[a] * 100:.1f}%'


def top(a, key, k=3, min_count=2):
    cnt = C[a].get(key, {})
    items = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
    items = [(n, c) for n, c in items if c >= min_count][:k]
    if not items:
        return '—'
    return '、'.join(f'`{n}` {c}' for n, c in items)


def dfs_list(a, names):
    items = [(n, DF[a].get(n, 0)) for n in names]
    items = [x for x in items if x[1] > 0]
    items.sort(key=lambda x: (-x[1], x[0]))
    return '、'.join(f'`{n}` {c}' for n, c in items) or '—'


def idi(a, keys):
    return '、'.join(f'{label} {I[a].get(k, 0)}' for label, k in keys if I[a].get(k, 0)) or '—'


# type-suffix names
def suffix_stats(a):
    names = [n for n in DF[a] if re.search(r'_(dict|list|set|map|heap|stack|arr|cnt)$', n)]
    files = sum(DF[a][n] for n in names)
    top_ = sorted(names, key=lambda n: -DF[a][n])[:6]
    return len(names), files, top_


out = []
w = out.append

w('''---
title: 两位大神变量命名对照
tags: [leetcode, python, 命名, 代码风格]
---

# 两位大神变量命名对照

> 素材：**灵茶山艾府**（灵神，Python 3）和 **yiduobo**（Python 2 风格）的全部题解代码，与 [[Python 刷题函数从零讲解]]、[[两位大神差异对照]] 用的是同一批文件。
> 方法：用 Python 的 `ast` 把每段代码解析成语法树，找出每个被**赋值、当循环变量、当参数、当函数名**的名字，按“出现在多少篇题解里”统计；再按**语义**（返回的答案、栈、堆、BFS 队列、并查集……）归类，看同一个东西两人分别怎么叫。每个名字的含义都是对照真实代码写的，最后给出一般有良好编码习惯的人会怎么命名。
''')

# ---------------- 0. 口径
nL, nY = NF[L], NF[Y]
w(f'''## 0. 统计口径

- 能解析出 Python 代码的题解：灵神 **{nL}** 篇，yiduobo **{nY}** 篇（Python 2 的 `print x` 等先自动修复再解析）。
- **统计“作者自己起的名字”**：赋值目标、`for` / 推导式的循环变量、自己写的函数名和参数、`lambda` 参数、类名。
- **不统计题目给的名字**：力扣方法签名里的参数（`nums`、`s`、`target`、`grid`…）是题目定的，不算作者的风格。yiduobo 的签名里常见 `A`、`S`、`N`、`K` 这样的大写单字母（分别 {A['given'][Y].get('A', 0)}、{A['given'][Y].get('S', 0)}、{A['given'][Y].get('N', 0)}、{A['given'][Y].get('K', 0)} 篇），那是早期力扣题目的写法，也不是他起的。
- “篇”= 用到这个名字的题解文件数，同一篇用多次只算 1 篇；“占比”= 篇数 ÷ 该作者的题解总数。
- 风格指标（第 1 节）按“每篇题解 × 每个名字”计一次，灵神共 {S[L]['pairs']} 次，yiduobo 共 {S[Y]['pairs']} 次。
''')

# ---------------- 1. 总体风格
sL, sY = S[L], S[Y]
def p(x):
    return f'{x * 100:.1f}%' if x == 0 or x >= 0.001 else f'{x * 100:.2f}%'
sufL, sufY = suffix_stats(L), suffix_stats(Y)
w('## 1. 总体风格：一张表看差异\n')
w('| 指标 | 灵神 | yiduobo | 怎么理解 |')
w('|---|---|---|---|')
w(f'| 不同的名字个数 | {len(DF[L])} | {len(DF[Y])} | yiduobo 题解更多，名字也更杂 |')
w(f'| 名字平均长度（字符） | {sL["mean_len"]:.2f} | {sY["mean_len"]:.2f} | 灵神更短 |')
w(f'| 名字长度中位数 | {sL["median_len"]:.0f} | {sY["median_len"]:.0f} | |')
w(f'| 单字母名占比 | {p(sL["len1"])} | {p(sY["len1"])} | 灵神将近一半是单字母：`i`、`x`、`f`、`g`、`s` |')
w(f'| 2–3 个字母 | {p(sL["len2_3"])} | {p(sY["len2_3"])} | `ans`、`cnt`、`res`、`now` 这类缩写 |')
w(f'| 4 个字母以上 | {p(sL["len4p"])} | {p(sY["len4p"])} | yiduobo 爱写全词：`index`、`stack`、`heap`、`char` |')
w(f'| 含下划线的 snake_case | {p(sL["kinds"].get("snake_case", 0))} | {p(sY["kinds"].get("snake_case", 0))} | yiduobo 爱加类型后缀：`cnt_dict`、`num_list` |')
w(f'| 全大写常量 | {p(sL["kinds"].get("UPPER", 0))} | {p(sY["kinds"].get("UPPER", 0))} | 灵神的常量全大写：`MOD`、`MX`、`DIRS`；yiduobo 写小写 `mod` |')
w(f'| camelCase | {p(sL["kinds"].get("camelCase", 0))} | {p(sY["kinds"].get("camelCase", 0))} | 两人都几乎不用（灵神的多半是复用力扣方法名） |')
w(f'| 带类型后缀的名字（`_dict` / `_list` / `_set` …） | {sufL[0]} 个 | {sufY[0]} 个 | yiduobo 最常见：' + '、'.join(f'`{n}`' for n in sufY[2][:5]) + ' |')
shL = '、'.join(f'`{n}` {c}' for n, c in sL['shadow'][:4])
shY = '、'.join(f'`{n}` {c}' for n, c in sY['shadow'][:4])
w(f'| 遮蔽内置名的题解 | {sL["shadow_files"]} 篇（{shL}） | {sY["shadow_files"]} 篇（{shY}） | 灵神多是刻意的卡常；yiduobo 多是 `next` 当邻居 |')
w(f'| 用 `l` 当变量的题解 | {sL["amb"].get("l", 0)} 篇 | {sY["amb"].get("l", 0)} 篇 | PEP 8 明确不建议（`l` 像 `1`） |')
w('')
w(f'''**一句话画像**

- **灵神：数学记号式。** 名字尽量短，和题解正文里的公式一一对应：元素叫 `x`，邻居叫 `y`，DP 数组叫 `f`，图叫 `g`，前缀和叫 `s`，答案叫 `ans`。常量全大写（`MOD`、`MX`、`DIRS`），预处理表的上限 `MX` 一般放在类外。名字短，但含义靠**固定搭配**撑着：`for y in g[x]`、`dfs(x, fa)`、`f[i]` 就是 `dfs(i)`。
- **yiduobo：口语描述式。** 他会写全词（`index`、`stack`、`heap`、`char`），会给容器加类型后缀（`cnt_dict`、`num_list`、`pos_dict`），而“当前的东西”一律叫 `now`。答案叫 `res`，最大最小叫 `ma` / `mi`，布尔标志叫 `flag`。另外有 Python 2 时代的痕迹：没有 `nonlocal`，所以用 `res[0]` / `self.res` 在递归里改答案；BFS 多用 list 加 `head, tail`（或 `l, r`）指针，很少用 `deque`。
- **两人共同的竞赛习惯：** DP 都叫 `f`（几乎没人写 `dp`：灵神 {DF[L].get("dp", 0)} 篇，yiduobo {DF[Y].get("dp", 0)} 篇），图都叫 `g`，并查集父数组都叫 `fa`（father），计数都叫 `cnt`，访问标记叫 `vis`，规模是 `n` / `m`，递归函数叫 `dfs`。这些缩写在国内算法竞赛圈很普遍，读多了就是“行话”。

**为什么他们敢用这么短的名字？** 因为题解正文先定义了含义。灵神有 {I[L].get("@cache", 0)} 篇用了 `@cache` 记忆化，他讲 DP 的固定套路是“先写记忆化搜索，再 1:1 翻译成递推”，原文写的是“$f[i][j]$ 的定义和 $dfs(i,j)$ 的定义是一样的”。yiduobo 的正文里有 246 篇写了“f[i]表示……”或“f[i][j]表示……”。**脱离了正文，`f`、`g`、`s` 就看不懂了**。面试、工程代码里没有这段正文，所以要用说明含义的名字。
''')

# ---------------- 2. concept table
w('## 2. 同一个东西，两人怎么叫\n')
w('数字 = 篇数。“推荐命名”是面试 / 工程里更易读的写法。\n')
w('| 概念 | 灵神 | yiduobo | 推荐命名 |')
w('|---|---|---|---|')
rows = [
    ('最后被 `return` 的答案', top(L, '返回的答案变量'), top(Y, '返回的答案变量'), '按含义：`max_len`、`total`、`min_cost`；实在没有就用 `result`'),
    ('`range` 循环下标', top(L, 'range 循环下标', 4), top(Y, 'range 循环下标', 4), '`i`、`j`、`k`；不用的写 `_`'),
    ('`enumerate` 的（下标, 元素）', top(L, 'enumerate 的 (下标, 元素)', 4), top(Y, 'enumerate 的 (下标, 元素)', 4), '`i, num`、`i, ch`、`i, row`'),
    ('直接遍历输入时的元素', top(L, '直接遍历输入的元素', 4), top(Y, '直接遍历输入的元素', 4), '容器名的单数：`for num in nums`、`for word in words`'),
    ('“当前”节点 / 值', dfs_list(L, ['cur', 'now']), dfs_list(Y, ['now', 'cur']), '`cur` / `node`，或说清是什么：`cur_sum`'),
    ('打擂台求最大', top(L, '打擂台 max(变量, ...)', 4), top(Y, '打擂台 max(变量, ...)', 4), '`max_len`、`best`、`max_val`'),
    ('打擂台求最小', top(L, '打擂台 min(变量, ...)', 4), top(Y, '打擂台 min(变量, ...)', 4), '`min_cost`、`min_val`'),
    ('计数表 `Counter` / `defaultdict(int)`', 'Counter：' + top(L, '计数器 Counter', 2) + '；defaultdict(int)：' + top(L, '计数器 defaultdict(int)', 2), top(Y, '计数器 Counter', 2) + '（他更常用普通 dict，见下一行）', '`count`、`freq`、`char_count`'),
    ('普通 dict `{}`', top(L, '空字典 {}', 3), top(Y, '空字典 {}', 5), '说清“键 → 值”：`index_of`、`count_by_char`'),
    ('dict 计数的写法', idi(L, [('`cnt[x] += 1`', 'cnt[x] += 1')]), idi(Y, [('`d[k] = d.get(k, 0) + 1`', 'x.get(k, 0) + 1')]), '`Counter` 或 `defaultdict(int)` 最清楚'),
    ('栈（`append` + `[-1]` + `pop()`）', top(L, '栈 (append + [-1] + pop)', 1), top(Y, '栈 (append + [-1] + pop)', 1), '`stack`；单调栈可叫 `mono_stack`'),
    ('堆', top(L, '堆', 3), top(Y, '堆', 3), '`heap`、`min_heap`、`max_heap`'),
    ('`deque` 队列', top(L, '队列 (deque)', 3), top(Y, '队列 (deque)', 3), '`queue`'),
    ('BFS 一层一层走', idi(L, [('`tmp = q; q = []` 换层', 'BFS: tmp = q; q = []'), ('`popleft()`', 'BFS: .popleft()')]), idi(Y, [('`head, tail = tail, len(q)`', 'BFS: head, tail = tail, len(q)'), ('`l, r = r, len(q)`', 'BFS: l, r = r, len(q)')]), '`deque` + `for _ in range(len(queue))`'),
    ('访问标记', dfs_list(L, ['vis', 'seen', 'visited', 'used']), dfs_list(Y, ['used', 'vis', 'seen', 'visited']), '`visited`；回溯里“用过没有”叫 `used`'),
    ('邻接表 `[[] for _ in range(n)]`', top(L, '邻接表 [[] for _ in range(n)]', 3), top(Y, '邻接表 [[] for _ in range(n)]', 3) + '（也常用 `g = {}`）', '`graph`、`adj`'),
    ('遍历邻居', top(L, '遍历邻居', 2), top(Y, '遍历邻居', 4), '`neighbor`、`child`；**别用 `next`**（遮蔽内置函数）'),
    ('树 DFS 的父节点参数', idi(L, [('`dfs(x, fa)`', 'tree dfs(x, fa)')]), idi(Y, [('`dfs(now, fa)`', 'tree dfs(now, fa)')]), '`dfs(node, parent)`'),
    ('并查集父数组', top(L, '并查集父节点数组', 2), top(Y, '并查集父节点数组', 2) + '；根叫 `fa_x` / `fa_y`', '`parent`；根叫 `root_x` / `root_y`'),
    ('网格方向', top(L, '四方向/八方向数组', 2, 3) + '，或直接写 `for x, y in (i, j-1), (i, j+1), ...`', top(Y, '方向分量数组 (dx/dy 分开写)', 2), '一个模块级常量 `DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))`'),
    ('网格里当前格 → 邻居格', '`i, j` → `x, y`（22 篇）；少数题反过来（3 篇）', '`nowx, nowy` → `x, y`（`= nowx + dx[d]` 60 篇）', '`r, c` → `nr, nc`（或 `cur_x` → `next_x`）'),
    ('网格行数、列数', f'`m, n = len(grid), len(grid[0])` {C[L].get("网格的行数, 列数", {}).get("m, n", 0)}', f'`m = len(grid)` {A["inits"][Y]["m"].get("len(grid)", 0)}、`n = len(grid[0])` {A["inits"][Y]["n"].get("len(grid[0])", 0)}', '`rows, cols`（`m, n` 也普遍接受）'),
    ('取模常数 1e9+7', top(L, '取模常数 1e9+7', 2) + '（`1_000_000_007`）', top(Y, '取模常数 1e9+7', 2) + '（`10 ** 9 + 7`）', '`MOD`（常量全大写）'),
    ('二分中点', top(L, '二分的中点', 2), top(Y, '二分的中点', 2), '`mid`'),
    ('二分 / 双指针左右端', top(L, '二分的左右边界', 2), top(Y, '二分的左右边界', 2), '`left, right` 或 `lo, hi`；不要用 `l`'),
    ('DP 数组', dfs_list(L, ['f', 'dp', 'memo']), dfs_list(Y, ['f', 'dp', 'memo']), '`dp`，或按状态含义：`max_profit`'),
    ('记忆化搜索', idi(L, [('`@cache`', '@cache')]) + '；函数名 ' + top(L, '记忆化搜索函数名', 2), idi(Y, [('`f = [None] * n` 手写备忘录', 'f = [None]*')]), '`@cache` + 说明返回值的函数名'),
    ('前缀和数组', top(L, '前缀和数组', 3), '`s` ' + str(C[Y]['前缀和数组'].get('s', 0)) + '（`s.append(s[-1] + x)`）、`f` ' + str(C[Y]['前缀和数组'].get('f', 0)), '`prefix_sum` / `prefix`'),
    ('布尔标志', top(L, '布尔标志位', 3), top(Y, '布尔标志位', 3), '说清楚是什么：`found`、`is_valid`、`has_zero`'),
    ('链表哨兵', top(L, '链表哨兵节点', 1, 5), top(Y, '链表哨兵节点', 3), '`dummy`'),
    ('有序集合 `SortedList`', top(L, '有序集合 SortedList', 1, 3), '—（Python 2 时代没有）', '`sorted_list` 或按用途：`window`'),
    ('嵌套辅助函数名', top(L, '嵌套辅助函数名', 4), top(Y, '嵌套辅助函数名', 4), '动词短语：`count_paths`、`can_finish(speed)`'),
    ('递归里修改外层答案', idi(L, [('`nonlocal`', 'nonlocal')]), idi(Y, [('`res[0]`', 'res[0] mutable'), ('`self.res`', 'self.res')]), '`nonlocal ans`，或让函数直接返回结果'),
]
for r in rows:
    w('| ' + ' | '.join(r) + ' |')
w('')

# ---------------- 3. side by side
w('''## 3. 同一道题对照，再给一个“规范命名”版

下面三题两人用的是同一个算法，差别只在命名。代码摘自原题解（`...` 处有省略），`#` 注释是本文加的。规范版都用随机数据和原版对拍过，结果一致。

### 3.1 994. 腐烂的橘子（多源 BFS）

灵神：

```py
m, n = len(grid), len(grid[0])
fresh = 0
q = []
for i, row in enumerate(grid):
    for j, x in enumerate(row):        # x 是格子的值
        if x == 1:
            fresh += 1
        elif x == 2:
            q.append((i, j))
ans = 0
while q and fresh:
    ans += 1
    tmp = q                             # tmp：当前层
    q = []                              # q：下一层
    for x, y in tmp:                    # x, y 变成了坐标
        for i, j in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):   # i, j 变成了邻居
            if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
                fresh -= 1
                grid[i][j] = 2
                q.append((i, j))
return -1 if fresh else ans
```

yiduobo：

```py
q = []
m = len(grid)
n = len(grid[0])
cnt = 0                                 # cnt：新鲜橘子数
...
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
l, r = 0, len(q)                        # q[l:r] 是当前层
step = 0
while l < r:
    step += 1
    for now_x, now_y in q[l: r]:        # now_ = 当前格子
        for index in range(4):          # index = 方向编号
            x = now_x + dx[index]       # x, y = 新格子
            y = now_y + dy[index]
            ...
    l, r = r, len(q)
```

规范命名版：

```python
from collections import deque
from typing import List

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        fresh_count = 0
        rotten = deque()
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == 1:
                    fresh_count += 1
                elif cell == 2:
                    rotten.append((r, c))

        minutes = 0
        while rotten and fresh_count:
            minutes += 1
            for _ in range(len(rotten)):          # 只处理当前这一层
                r, c = rotten.popleft()
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        rotten.append((nr, nc))
        return -1 if fresh_count else minutes
```

要点：
- 灵神这段里 `x` 先是“格子的值”，后来又是“当前坐标”；`i, j` 先是外层下标，后来又是邻居坐标（他更常见的写法是当前格 `i, j`、邻居 `x, y`，这题正好反过来）。**同一函数里一个名字换了含义**，这是短名字最容易出事的地方。
- yiduobo 的 `l, r` 在这里是“队列的一段”，在二分题里又是“搜索区间”，同一个名字要看上下文才知道。
- 规范版给每样东西一个固定的名字：`rotten`（队列里装的是什么）、`fresh_count`、`minutes`（答案的单位）、`r, c` / `nr, nc`（当前格 / 邻居格）、`DIRECTIONS`（模块级常量，全大写）。

### 3.2 739. 每日温度（单调栈）

| 灵神 | yiduobo |
|---|---|
| `ans = [0] * n`、`st = []`、`for i, t in enumerate(temperatures)`、`j = st.pop()` | `res = [0] * len(T)`、`stack = [0]`、`for index in range(1, len(T))` |

规范命名版：

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        days_to_wait = [0] * len(temperatures)
        pending = []  # 单调栈：还没等到更高温度的日子（存下标）
        for day, temp in enumerate(temperatures):
            while pending and temp > temperatures[pending[-1]]:
                prev_day = pending.pop()
                days_to_wait[prev_day] = day - prev_day
            pending.append(day)
        return days_to_wait
```

要点：`st` / `stack` 只说了“这是个栈”，`pending` 说的是**栈里装的是什么**（还在等更高温度的日子）。答案也用它的含义 `days_to_wait` 命名，而不是 `ans` / `res`。

### 3.3 3. 无重复字符的最长子串（滑动窗口）

| 灵神 | yiduobo |
|---|---|
| `ans = left = 0`、`cnt = defaultdict(int)`、`for right, c in enumerate(s)` | `left = 0`、`res = 0`、`for right, char in enumerate(s)`、`pos = s.find(char, left, right)` |

规范命名版：

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_len = left = 0
        char_count = {}
        for right, ch in enumerate(s):
            char_count[ch] = char_count.get(ch, 0) + 1
            while char_count[ch] > 1:          # 窗口里有重复字符，收缩左端
                char_count[s[left]] -= 1
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len
```

要点：`left` / `right` 两人都用全名，这是最常见、最好懂的写法。答案改成 `max_len`，读者看名字就知道求的是“最大长度”。
''')

# ---------------- 4/5 dictionaries
def dict_table(a, entries, title, extra=False):
    rows_ = []
    for names, meaning, usage, rec in entries:
        counts = [(n, DF[a].get(n, 0)) for n in names]
        mx = max(c for _, c in counts)
        if len(names) == 1:
            label = f'`{names[0]}`'
            cnt = f'{counts[0][1]}（{pct(a, counts[0][1])}）'
        else:
            label = ' / '.join(f'`{n}`' for n in names)
            cnt = ' / '.join(str(c) for _, c in counts)
        rows_.append((mx, label, cnt, meaning, usage, rec))
    if not extra:
        rows_.sort(key=lambda r: -r[0])
    w(title + '\n')
    w('| 变量 | 篇数 | 在他代码里的含义 | 典型写法 | 规范命名建议 |')
    w('|---|---|---|---|---|')
    for _, label, cnt, meaning, usage, rec in rows_:
        w(f'| {label} | {cnt} | {meaning} | {usage} | {rec} |')
    w('')

w('## 4. 灵神变量词典\n')
w(f'按出现篇数从高到低，共 {len(LING)} 条（多个名字一行的，篇数按顺序对应）。灵神共 {nL} 篇。\n')
dict_table(L, LING, '### 4.1 高频名')
dict_table(L, LING_EXTRA, '### 4.2 特色低频名（数位 DP、线段树、滑窗模板里的固定写法）', extra=True)

w('## 5. yiduobo 变量词典\n')
w(f'按出现篇数从高到低，共 {len(YIDUOBO)} 条。yiduobo 共 {nY} 篇。\n')
dict_table(Y, YIDUOBO, '### 5.1 高频名')
dict_table(Y, YIDUOBO_EXTRA, '### 5.2 特色写法（类型后缀、拓扑、状压等）', extra=True)

# ---------------- 6. rules
w('''## 6. 好名字的规则（以及刷题时可以放宽到哪）

**PEP 8（Python 官方风格指南）**
1. 变量、函数用小写加下划线 `snake_case`：`max_len`、`count_paths`。两人都基本遵守；yiduobo 的 `quickPow`、`nowx`（没分词）是例外。
2. 常量全大写：`MOD`、`MAX_N`、`DIRECTIONS`。灵神这样写，yiduobo 写成小写 `mod`。
3. 类名用 CapWords：`UnionFind`、`SegmentTree`。两人都遵守。
4. **不要用 `l`、`O`、`I` 当单字母名**（在一些字体里和 `1`、`0` 分不清），想用 `l` 时用 `L`。两人都大量用 `l`，这一条两人都没守。
5. 名字和关键字撞了就在末尾加下划线：`in_`、`class_`。灵神的 `in_, out` 正是这个用法。

**Google Python 风格指南**
1. 名字要能说明含义；避免缩写，尤其不要用项目外的人看不懂的缩写，**也不要靠删掉单词中间的字母来缩写**。按这一条，`cnt`（count）、`nxt`（next）、`mx`（max）、`tmp`（temporary）这类删字母的缩写都不合格；`st`、`vis` 这类截断也属于“避免缩写”。
2. 单字母名只在这些情况可以用：计数器 / 迭代器（`i`、`j`、`k`、`v`）、`except` 里的 `e`、`with` 里的文件句柄 `f`，以及**和参考论文或算法里的记号一致的名字**。灵神的 `f[i]`、`x`、`y` 能算最后这一类：前提是正文里写了公式。
3. 名字的描述性要和它的作用域成正比：5 行循环里的 `i` 没问题，跨好几层嵌套的 `i` 就太含糊了。

**再补几条常见共识**
- 不要遮蔽内置名：`next`、`sum`、`max`、`min`、`id`、`type`、`list`、`dict`、`str`。遮蔽后这个作用域里就调不了原函数了（函数里只要出现 `for next in g[now]`，整个函数内的 `next` 都是局部变量，调用 `next()` 会报错）。
- 名字说**内容**，不说**类型**：`num_list` → `nums`，`cnt_dict` → `count`，`pos_dict` → `index_of`。类型交给类型注解。
- 布尔值用 `is_` / `has_` / `can_` 开头：`flag` → `found` / `is_valid`；判定函数 `check(mid)` → `can_ship(capacity)`。
- 容器用复数，元素用单数：`for word in words`、`for row in grid`。
- 一个名字在一个函数里只表示一样东西（见 3.1 节的反例）。
- `tmp`、`res`、`ans`、`now`、`flag` 这类“万能名”要换成具体含义；作用域只有两三行的除外。

**刷题、面试、工程怎么取舍**

| 场景 | 建议 |
|---|---|
| 比赛、自己刷题 | 两位大神的写法完全可以照搬，打字快，配上固定搭配（`for y in g[x]`、`f[i]` ↔ `dfs(i)`）就够了 |
| 面试白板 / 共享编辑器 | 中间档：`i`、`j`、`n`、`m`、`left`、`right`、`mid` 保留；容器写全名 `stack`、`queue`、`heap`、`graph`、`visited`、`parent`、`dp`；答案按含义命名 |
| 工程代码 | 全部按上面的规则，再加类型注解 |

## 7. 缩写速查

| 缩写 | 全称 | 谁在用 | 推荐写法 |
|---|---|---|---|
| `ans` / `res` / `ret` | answer / result / return value | 灵神 / yiduobo / yiduobo | 按含义，或 `result` |
| `cnt` | count | 两人 | `count` / `freq` |
| `vis` | visited | 两人 | `visited` |
| `fa` | father（父节点） | 两人 | `parent` |
| `g` | graph | 两人 | `graph` / `adj` |
| `f` | function（数学里的函数，即 DP 数组） | 两人 | `dp` |
| `dis` | distance | 两人 | `dist` |
| `st` | stack（偶尔是 set） | 灵神 | `stack` |
| `h` | heap | 灵神 | `heap` |
| `q` | queue | 两人 | `queue` |
| `mx` / `ma` | max | 灵神 / yiduobo | `max_val` |
| `mn` / `mi` | min | 灵神 / yiduobo | `min_val` |
| `pre` | previous 或 prefix | 两人 | `prev` / `prefix` 分开用 |
| `suf` | suffix | 灵神 | `suffix` |
| `cur` / `now` | current | 灵神 / yiduobo | `cur` / `curr` |
| `nxt` | next | 两人 | `next_node` / `neighbor` |
| `idx` | index | 灵神 | `index_of` / `i` |
| `ind` | in-degree（入度） | yiduobo | `in_degree` |
| `deg` | degree | 灵神 | `degree` |
| `sz` | size | 灵神 | `size` |
| `tot` | total | yiduobo | `total` |
| `tmp` | temporary | 两人 | 具体含义 |
| `MOD` / `mod` | modulus | 灵神 / yiduobo | `MOD` |
| `MX` | max（预处理上限） | 灵神 | `MAX_N` |
| `DIRS` | directions | 灵神 | `DIRECTIONS` |
| `dx` / `dy` | delta x / delta y | 两人 | `DIRECTIONS` 里的 `dr, dc` |
| `sl` | SortedList | 灵神 | `sorted_list` |
| `o` | 线段树节点（node） | 灵神 | `node` |
| `ql` / `qr` | query left / right | 灵神 | 保留或写全 |
| `lo` / `hi` | low / high | 两人 | 保留 |
| `u` | universe（全集掩码）或边端点 | 灵神 | `full_mask` / `u` |
| `w` | weight / width | 两人 | `weight` / `width` |
| `f0` / `f1` | 状态 0 / 状态 1 | 灵神 | 状态名，如 `not_hold` / `hold` |
''')

w('''## 数据与脚本

脚本和汇总数据在同目录 `变量命名统计/`。`extract.py` 在 `Leetcode` 库根目录运行，其余脚本在 `变量命名统计/` 目录里按顺序运行（`collect.py`、`concept.py` 会用到上一级 `census.py` 里的解析函数）：

1. `extract.py`：从两个题解文件夹抽出 Python 代码块 → `allcode.json`
2. `collect.py`：逐篇解析，记录每个名字和它的角色（赋值 / 循环变量 / 参数 / 函数名…）→ `uses.json`
3. `agg.py`、`style.py`、`concept.py`、`idioms.py`：按作者汇总、风格指标、按语义归类、惯用写法计数
4. `glossary.py`：本文第 4、5 节的人工释义；`build_md.py`：生成本文
5. `ctx.py`、`grepn.py`：查看某个名字在真实代码里的上下文（写释义时用的）
6. `test_rewrites.py`：第 3 节三个规范命名版与原版的随机对拍

`varnames_stats.json` 是汇总结果（每个名字的篇数、角色分布、最常见的初始化写法、语义归类）。

## 参考

- [PEP 8 – Style Guide for Python Code · Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions)
- [Google Python Style Guide · Naming](https://google.github.io/styleguide/pyguide.html#316-naming)
''')

open('两位大神变量命名对照.md', 'w').write('\n'.join(out))
print('written', sum(1 for _ in open('两位大神变量命名对照.md')), 'lines')
