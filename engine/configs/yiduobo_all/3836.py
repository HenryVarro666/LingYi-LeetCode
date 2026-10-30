def _layer(t):
    def fn(S):
        f = S.get('f')
        if f is None:
            return None
        return [[row[t] if t < len(row) else None for row in plane] for plane in f]
    return fn


def _rows(S):
    return ['-'] + [str(v) for v in S['nums1']]


def _cols(S):
    return ['-'] + [str(v) for v in S['nums2']]


def _color(T):
    def fn(S, r, c, v):
        i, j, t, ln = S.get('i'), S.get('j'), S.get('t'), S.get('_line')
        if i is None or j is None or t is None or ln not in (18, 20, 22):
            return None
        if T == t and (r, c) == (i, j):
            return 'yellow'
        if ln == 18 and T == t - 1 and (r, c) == (i - 1, j - 1):
            return 'green'
        if ln == 20 and T == t and (r, c) == (i - 1, j):
            return 'blue'
        if ln == 22 and T == t and (r, c) == (i, j - 1):
            return 'blue'
        return None
    return fn


def _formula(S):
    i, j, t, ln = S.get('i'), S.get('j'), S.get('t'), S.get('_line')
    if i is None or j is None or t is None or ln not in (18, 20, 22):
        return '`f[i][j][t]`：`nums1` 前 `i` 个、`nums2` 前 `j` 个里选 `t` 对的最大得分（`t=0` 层全是 0）'
    a, b = S['nums1'][i - 1], S['nums2'][j - 1]
    if ln == 18:
        return f'先假设用最后一对：`f[{i - 1}][{j - 1}][{t - 1}] + {a}×{b}` = =={S["f"][i][j][t]}=='
    if ln == 20:
        return f'不选 nums1[{i - 1}]：`f[{i - 1}][{j}][{t}]` = {S["f"][i - 1][j][t]}，与当前取大'
    return f'不选 nums2[{j - 1}]：`f[{i}][{j - 1}][{t}]` = {S["f"][i][j - 1][t]}，与当前取大'


CONFIG = dict(
    num=3836, title='恰好 K 个下标对的最大得分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三维 DP · f[i][j][t]',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1988'],
    code='''
class Solution(object):
    def maxScore(self, nums1, nums2, k):
        
        n = len(nums1)
        m = len(nums2)

        f = [[[None] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]
        f[0][0][0] = 0
        for i in range(1, n + 1):
            f[i][0][0] = 0
        for j in range(1, m + 1):
            f[0][j][0] = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                f[i][j][0] = 0
                for t in range(1, min(i, j, k) + 1):
                    f[i][j][t] = f[i - 1][j - 1][t - 1] + nums1[i - 1] * nums2[j - 1]
                    if f[i - 1][j][t] is not None:
                        f[i][j][t] = max(f[i][j][t], f[i - 1][j][t])
                    if f[i][j - 1][t] is not None:
                        f[i][j][t] = max(f[i][j][t], f[i][j - 1][t])
        
        return f[-1][-1][k]
''',
    call='Solution().maxScore([1, 3, 2], [4, 5], 2)',
    expect=22,
    skip=[8, 9, 10, 11, 12, 16],
    max_steps=90,
    views=[
        dict(type='text', fn=_formula, size=22, h=70),
        dict(type='table', var=_layer(1), label='t = 1 层：选 1 对', h=250, cell=56, rows=_rows, cols=_cols, color=_color(1)),
        dict(type='table', var=_layer(2), label='t = 2 层：选 2 对（黄 = 正在算，绿 = 上一层左上，蓝 = 不选的来源）', h=250, cell=56, rows=_rows, cols=_cols, color=_color(2)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('t', 't', 'cyan'), ('f[i][j][t]', 'f[i][j][t]', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'm = len': '`m = {m}`',
        'f = [[[None]': '`f[i][j][t]`：共 `{n + 1} × {m + 1} × {k + 1}` 格，先全设为 `None`（还不存在）；随后把 `t = 0` 的边界都设成 0：什么都不选，得分 0',
        14: lambda S, B, r: (f'第 `{S.i}` 个 `nums1[{S.i - 1}] = {S.nums1[S.i - 1]}`' if S.i != B.get('i') else '`nums1` 都处理完了'),
        15: lambda S, B, r: (f'`j = {S.j}`：`nums2[{S.j - 1}] = {S.nums2[S.j - 1]}`' if S.j != B.get('j') else '这一行 `j` 都处理完'),
        17: lambda S, B, r: (f'`t = {S.t}`：最多选 `min(i, j, k) = {min(S.i, S.j, S.k)}` 对' if S.f[S.i][S.j][S.t] is None else '`t` 都枚举完'),
        'f[i][j][t] = f[i - 1][j - 1][t - 1]': '用最后一对 `nums1[{i - 1}]×nums2[{j - 1}]` = {nums1[i - 1] * nums2[j - 1]}，加上 `f[{i - 1}][{j - 1}][{t - 1}]` = {f[i - 1][j - 1][t - 1]} → =={f[i][j][t]}==',
        'if f[i - 1][j][t] is not None': lambda S, B, r: ('`f[i-1][j][t]` 存在（前置状态必须存在）→ 可以比较' if S.f[S.i - 1][S.j][S.t] is not None else '`f[i-1][j][t]` 是 `None`：这个状态不可达，跳过'),
        'f[i][j][t] = max(f[i][j][t], f[i - 1][j][t])': '不选 `nums1[{i - 1}]`：`max({B.f[i][j][t]}, {f[i - 1][j][t]})` → =={f[i][j][t]}==',
        'if f[i][j - 1][t] is not None': lambda S, B, r: ('`f[i][j-1][t]` 存在 → 可以比较' if S.f[S.i][S.j - 1][S.t] is not None else '`f[i][j-1][t]` 是 `None`：不可达，跳过'),
        'f[i][j][t] = max(f[i][j][t], f[i][j - 1][t])': '不选 `nums2[{j - 1}]`：`max({B.f[i][j][t]}, {f[i][j - 1][t]})` → =={f[i][j][t]}==',
        'return f[-1][-1][k]': '`f[{n}][{m}][{k}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j][t]：前 i、前 j 个里选 t 对，三种取最大',
        complexity='时间 `O(nmk)`，空间 `O(nmk)`',
        problem=['两数组各选==恰好 `k` 对==下标，要求下标严格递增，得分是每对乘积之和',
                 '示例：`[1,3,2]`、`[4,5,1]`、`k=2` → `22`',
                 '本视频：`[1,3,2]`、`[4,5]`、`k=2` → `22`（`3×4 + 2×5`）'],
        quote='令f[i][j][t]表示从nums1的前i个数，nums2的前j个数中选出t组可以得到的最大得分……需要注意，这里有一个前提是前置状态必须是存在的。',
        quote_src='—— yiduobo 题解原文',
        idea=['保留 `nums1[i]`、`nums2[j]` 配成一对：`f[i-1][j-1][t-1] + a×b`',
              '不保留 `nums1[i]`：`f[i-1][j][t]`；不保留 `nums2[j]`：`f[i][j-1][t]`',
              '三者取最大；`t` 只枚举到 `min(i, j, k)`，选不出来的状态保持 `None`',
              '先造好 `t = 0` 的边界：什么都不选得分为 0'],
        summary=['时间 `O(nmk)`，空间 `O(nmk)`',
                 '易错：用 `None` 表示不存在，取 max 前要先判断是否为 `None`',
                 '易错：`nums1[i - 1]` 的下标比 `i` 小 1（`f` 下标从 1 开始计数）',
                 '对比灵神：灵神用 `-inf` 表示无解并压成两层滚动；这里直接开三维数组',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
