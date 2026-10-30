_APP = 25  # f.append 所在行号


def _cur(S):
    f = S['f']
    return len(f) - 2 if S['_line'] >= _APP else len(f) - 1


def _books(S):
    return [f'{t}×{h}' for t, h in S['books']]


def _col(S, i, v):
    if 'bound' not in S or 'now' not in S:
        return None
    c = _cur(S)
    if S['bound'] <= i <= c:
        return 'blue'
    return None


def _dim(S, i, v):
    return 'bound' in S and i < S['bound']


def _q(S):
    return [f"{k}:高{S['books'][k][1]}" for k in S['q'][S['l']:S['r']]]


def _txt(S):
    if 'now' not in S or 'bound' not in S:
        return ''
    c = _cur(S)
    return f"窗口 `books[{S['bound']}..{c}]`：厚度和 `now` = =={S['now']}== / {S['shelf_width']}"


CONFIG = dict(
    num=1105, title='填充书架', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='DP + 滑动窗口 + 单调队列',
    tags=[],
    code='''
class Solution(object):
    def minHeightShelves(self, books, shelf_width):

        n = len(books)
        bound = 0
        now = 0
        f = [0]
        q = []
        l = 0
        r = 0
        for index in range(n):
            now += books[index][0]
            while now > shelf_width:
                now -= books[bound][0]
                if l < r and q[l] == bound:
                    l += 1
                bound += 1
            
            while r > l and books[q[-1]][1] < books[index][1]:
                q.pop()
                r -= 1
            q.append(index)
            r += 1

            f.append(f[bound] + books[q[l]][1])
            for index in range(l, r - 1):
                f[-1] = min(f[-1], f[q[index] + 1] + books[q[index + 1]][1])

        return f[-1]
''',
    call='Solution().minHeightShelves([[1,1],[2,3],[2,3],[1,2]], 4)',
    expect=6,
    views=[
        dict(type='array', var=_books, label='books（厚度×高度），蓝 = 滑动窗口 = 最后一层可放的书', pointers={'bound': 'blue'},
             color=_col, dim=_dim, h=200),
        dict(type='text', fn=_txt, size=28, h=80),
        dict(type='array', var=lambda S: list(S['f']), label='f[k]：前 k 本书的最小高度', h=190),
        dict(type='array', var=_q, label='单调队列 q：下标:高度（从前到后高度递减）', h=190),
    ],
    watch=[('index', 'index', 'pink'), ('bound', 'bound', 'blue'), ('now', 'now', 'cyan')],
    captions={
        'bound = 0': '`bound`：滑动窗口左边界，也就是最后一层能放的第一本书',
        'now = 0': '`now`：窗口里书的厚度之和',
        'f = [0]': '`f[k]` = 前 `k` 本书的最小高度，`f[0] = 0`',
        'q = []': '`q` 是单调队列（存下标，高度递减），`l`、`r` 是它的有效范围 `[l, r)`',
        'now += ': '第 `{index}` 本书入窗：厚度 `{books[index][0]}` → `now = {now}`',
        'while now > shelf_width': lambda S, B, r: (f'`now = {S.now} > {S.shelf_width}`：这层放不下了 → ==左边界右移==' if S.now > S.shelf_width else f'`now = {S.now} ≤ {S.shelf_width}`：窗口合法'),
        'now -= books[bound][0]': '把 `books[{bound}]` 移出窗口：`now = {now}`',
        'if l < r and q[l] == bound': lambda S, B, r: ('队首正是被移出的这本书 → 队首失效，`l += 1`' if S.l < S.r and S.q[S.l] == S.bound else '队首不是它，队列不用动'),
        'l += 1': '队首出队：`l = {l}`',
        'bound += 1': '窗口左边界 → `bound = {bound}`',
        'while r > l and books': lambda S, B, r: ((f'队尾书高 `{S.books[S.q[-1]][1]}` < 新书高 `{S.books[S.index][1]}` → 队尾被新书挡住，==弹出==') if S.r > S.l and S.books[S.q[-1]][1] < S.books[S.index][1] else '队尾不比新书矮（或队列为空）→ 不用再弹'),
        'q.pop()': '弹出队尾：它矮又靠前，不可能再是更优的最高书',
        'r -= 1': '`r` → {r}',
        'q.append(index)': '新书下标 `{index}` 入队尾',
        'r += 1': '`r` → {r}',
        'f.append': '候选 1：`f[bound] + 窗口最高书` = `{f[bound]} + {books[q[l]][1]}` → `f[{index+1}]` 先取 =={f[-1]}==',
        'for index in range(l, r - 1)': '再看队列里相邻的候选：前一本作为最后一层起点的分界',
        'f[-1] = min': '候选：`f[{q[index]+1}] + 高{books[q[index+1]][1]}` = {f[q[index]+1] + books[q[index+1]][1]}，和现有值取最小 → `f[{len(f)-1}]` = =={f[-1]}==',
        'return f[-1]': '最后一个 `f` 就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='窗口维护「最后一层能放哪些书」，单调队列只留有用的最高书',
        complexity='时间 `O(n^2)` 最坏，空间 `O(n)`',
        problem=['按顺序把书放进宽 `shelf_width` 的书架，每层厚度和不超过它，层高 = 该层最高的书',
                 '求书架总高度的最小值',
                 '本视频：`[[1,1],[2,3],[2,3],[1,2]]`，宽度 `4`'],
        quote='这里是一个经典的滑动窗口问题，那么可以在动态规划的过程中使用滑动窗口维护j的左边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 表示前 i 本书的最小高度，最后一层放第 j 到 i 本，`f[j-1] + 最高的书`',
              '厚度之和有上限 → `bound` 随 `index` 右移，是一个滑动窗口',
              '窗口里被更高的书挡住的书不用枚举 → 用单调队列只保留递减的高度'],
        summary=['时间最坏 `O(n^2)`，空间 `O(n)`；原文也说这个优化改变不了极限复杂度',
                 '`f[-1]` 先取 `f[bound] + 窗口最高`，再枚举队列里相邻的候选',
                 '内层循环复用了变量名 `index`，下一轮外层 for 会重新赋值',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
