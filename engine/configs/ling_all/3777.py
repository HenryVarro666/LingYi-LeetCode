S0 = 'AABAB'
QS = [[2, 0, 4], [1, 2], [2, 0, 4], [2, 1, 3]]


def _tree(S):
    v = S.get('self.tree')
    if isinstance(v, list):
        return v
    t = S.get('t')
    v = getattr(t, 'tree', None)
    return v if isinstance(v, list) else None


def _s(S):
    s = S.get('s')
    return list(s) if s is not None else None


def _b(S):
    s = _s(S)
    if not s:
        return None
    return [0] + [1 if s[k - 1] == s[k] else 0 for k in range(1, len(s))]


def _txt(S):
    q = S.get('q')
    if q is None:
        return '`b[i] = 1` 表示 `s[i-1] == s[i]`（删掉右边那个）；子串 `[l,r]` 的答案 = `b[l+1..r]` 的和'
    if q[0] == 1:
        return f'翻转 `s[{q[1]}]`：只影响 `b[{q[1]}]` 和 `b[{q[1] + 1}]`，各 +1 或 -1'
    return f'查询 `[{q[1]}, {q[2]}]`：`b[{q[1] + 1}..{q[2]}]` 的和 = `pre({q[2]}) − pre({q[1]})`'


CONFIG = dict(
    num=3777, title='使子字符串变交替的最少删除次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='差分标记 b[i] + 树状数组',
    tags=['灵神题单', '常用数据结构', '难度分 2202'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res += t[i]
            i &= i - 1
        return res

    # 计算区间和 a[l] + ... + a[r]
    # 1 <= l <= r <= n
    # 时间复杂度 O(log n)
    def query(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.pre(r) - self.pre(l - 1)

class Solution:
    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        t = FenwickTree(n - 1)
        for i in range(1, n):
            if s[i - 1] == s[i]:  # 删除 i
                t.update(i, 1)

        s = list(s)
        ans = []
        for q in queries:
            if q[0] == 2:
                ans.append(t.query(q[1] + 1, q[2]))
                continue

            i = q[1]

            if i > 0:
                t.update(i, 1 if s[i - 1] != s[i] else -1)
            if i < n - 1:
                t.update(i + 1, 1 if s[i] != s[i + 1] else -1)

            s[i] = 'A' if s[i] == 'B' else 'B'  # A 变成 B，B 变成 A

        return ans
''',
    call=f'Solution().minDeletions({S0!r}, {QS})',
    expect=[1, 3, 2],
    views=[
        dict(type='text', fn=_txt, h=80, size=27),
        dict(type='array', var=_s, label='s（A/B 字符，翻转会改它）', cell=84, h=190,
             color=lambda S, i, v: 'cyan' if v == 'A' else 'purple', pointers={'i': 'blue'}),
        dict(type='array', var=_b, label='b[i]（1 = s[i-1] == s[i]，下标从 1 开始）', cell=84, h=170,
             color=lambda S, i, v: 'orange' if v == 1 and i > 0 else None),
        dict(type='array', var=_tree, label='树状数组 tree（和 b 对应，管辖区间的和）', cell=84, h=170),
        dict(type='array', var='ans', label='ans', cell=84, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('val', 'val', 'orange'), ('res', 'res', 'green'), ('ans', 'ans', 'green')],
    skip=['self.tree = [0]', 'while i', 'i += i & -i', 'i &= i - 1', 'n = len(s)', 'ans = []', 't = self.tree', 'res = 0', 'for q in queries', 'continue'],
    max_steps=90,
    captions={
        't = FenwickTree(n - 1)': '`b` 只有 `n−1` 个位置（下标 1 到 n−1），建一棵空树状数组',
        'if s[i - 1] == s[i]': lambda S, B, r: (f'`s[{B.i - 1}] = {B.s[B.i - 1]}`，`s[{B.i}] = {B.s[B.i]}`：' + ('相等 → 规定删右边的 `s[%d]`，`b[%d] = 1`' % (B.i, B.i) if B.s[B.i - 1] == B.s[B.i] else '不等 → 不用删，`b[%d] = 0`' % B.i)),
        't.update(i, 1)': '`b[{i}] = 1`：树状数组下标 `{i}` 加 1',
        's = list(s)': '字符串不能改，转成列表',
        'if q[0] == 2': lambda S, B, r: (f'`q = {B.q}`：类型 2 → 查询' if B.q[0] == 2 else f'`q = {B.q}`：类型 1 → 翻转 `s[{B.q[1]}]`'),
        'ans.append': '`[{q[1]}, {q[2]}]` 的最少删除数 = `b[{q[1]+1}..{q[2]}]` 的区间和，交给 `query` 去算（下标 +1 是因为 `b` 从 1 开始）',
        'i = q[1]': '要翻转的下标 `i = {i}`',
        't.update(i, 1 if s[i - 1] != s[i] else -1)': lambda S, B, r: (f'`b[{B.i}]`：原来 `s[{B.i-1}] {"≠" if B.s[B.i-1] != B.s[B.i] else "="} s[{B.i}]`，翻转后必然' + ('相等 → `b[%d]` 从 0 变 1，加 1' % B.i if B.s[B.i-1] != B.s[B.i] else '不等 → `b[%d]` 从 1 变 0，减 1' % B.i)),
        't.update(i + 1, 1 if s[i] != s[i + 1] else -1)': lambda S, B, r: (f'`b[{B.i+1}]`：原来 `s[{B.i}] {"≠" if B.s[B.i] != B.s[B.i+1] else "="} s[{B.i+1}]`，翻转后必然' + ('相等 → `b[%d]` 从 0 变 1，加 1' % (B.i+1) if B.s[B.i] != B.s[B.i+1] else '不等 → `b[%d]` 从 1 变 0，减 1' % (B.i+1))),
        's[i] = ': '翻转 `s[{i}]` → `{s[i]}`（先更新树状数组，再改字符）',
        't[i] += val': '树状数组节点 `{B.i}` 加 `{val}` → {t[B.i]}，随后 `i` 跳到 `i + lowbit(i)`',
        'res += t[i]': '累加节点 `{B.i}` 管辖的和 `{t[B.i]}` → `res = {res}`，随后 `i` 去掉最低位',
        'if r < l': '区间 `[{l}, {r}]` 合法才算，否则是 0',
        'return self.pre(r) - self.pre(l - 1)': '区间和 = `pre({r}) − pre({l - 1})`',
        'return res': lambda S, B, r: f'前缀和 `{r}`',
        'return ans': '全部查询的答案：`{ans}`',
    },
    cards=dict(
        one_liner='相邻相等就删右边：把“相等对”标成 1，区间和就是答案',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含 `A/B`；`[1, j]` 翻转 `s[j]`，`[2, l, r]` 问 `s[l..r]` 变成交替串（无相邻相等）最少删几个',
                 '示例（本视频）：`s = "AABAB"`，`queries = [[2,0,4],[1,2],[2,0,4],[2,1,3]]` → `[1,3,2]`'],
        quote='如果发现 s[i-1]≠s[i]，人为规定删除右边的 s[i]。这启发我们定义长为 n-1 的数组 b（下标从 1 到 n-1）。子串 [l,r] 的删除次数，等于 b 的子数组 [l+1,r] 中的 1 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`b[i] = 1` 当且仅当 `s[i-1] == s[i]`，每个 1 对应删掉右边那个字符',
              '子串 `[l, r]` 的删除数 = `b[l+1..r]` 的和（`s[l]` 左边的对不算）',
              '翻转 `s[i]` 只改 `b[i]` 和 `b[i+1]`，各自 0↔1 翻转，用树状数组做单点加、区间和'],
        after=[dict(heading='原文的其他写法', lines=['方法一：线段树，每个节点存左端字母、右端字母、最少删除数，`merge` 时端点相同多删 1',
                                                      '方法二写法一：先撤销旧的 `b[i]`、`b[i+1]`，翻转后再加新的；本视频用的写法二直接按“相等↔不等”加减 1',
                                                      '附：用 `SortedList` 维护需要删除的下标，二分求个数'])],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '易错：区间和是 `b[l+1..r]`，下标从 `l+1` 起，不含 `b[l]`',
                 '易错：树状数组下标从 1 开始，`b` 只有 `n-1` 个位置，所以建 `FenwickTree(n-1)`',
                 '翻转后相等/不等一定取反，所以每次只要 ±1，不必先撤销再添加'],
    ),
)
