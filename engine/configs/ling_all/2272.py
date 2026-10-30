S0 = 'aababbb'


def _col(S, i, v):
    a, b = S.get('a'), S.get('b')
    if a is None:
        return None
    if v == a:
        return 'green'
    if v == b:
        return 'pink'
    return None


def _dim(S, i, v):
    a, b = S.get('a'), S.get('b')
    return a is not None and v not in (a, b)


def _fmt(x):
    return '−∞' if x == float('-inf') else str(x)


def _text(S):
    a, b = S.get('a'), S.get('b')
    if a is None:
        return '枚举两个字母：`a` 当「最多」记 +1，`b` 当「最少」记 −1，其余记 0，然后求最大子数组和'
    f0, f1 = S.get('f0'), S.get('f1')
    if f0 is None:
        return f'这一对：`a = {a}`（+1），`b = {b}`（−1）'
    return f'`f0` = 以当前位置结尾的最大和 ==({_fmt(f0)})==；`f1` = 其中==一定含 b== 的最大和 ==({_fmt(f1)})=='


CONFIG = dict(
    num=2272, title='最大波动的子字符串', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='枚举字母对 + 状态机 DP（最大子数组和）',
    tags=['灵神题单', '动态规划', '难度分 2516'],
    setup="ascii_lowercase = 'ab'  # 演示用：示例串只含 a、b，字母表缩成 2 个字母，只枚举 (a,b)、(b,a) 两对",
    code='''
class Solution:
    def largestVariance(self, s: str) -> int:
        ans = 0
        for a, b in permutations(ascii_lowercase, 2):  # 枚举所有小写字母对
            f0, f1 = 0, -inf
            for ch in s:
                if ch == a:
                    f0 = max(f0, 0) + 1
                    f1 += 1
                elif ch == b:
                    f1 = f0 = max(f0, 0) - 1
                # else: f0 = max(f0, 0) 可以留到 ch 等于 a 或者 b 的时候计算，f1 不变
                ans = max(ans, f1)
        return ans
''',
    call=f'Solution().largestVariance({S0!r})',
    expect=3,
    max_steps=70,
    skip=['for ch in s', 'elif ch == b', 'ans = 0'],
    views=[
        dict(type='string', var=lambda S: S0, label='s（绿 = a，+1；粉 = b，−1；灰 = 其他，记 0）', h=190, cell=84,
             color=_col, dim=_dim),
        dict(type='text', fn=_text, size=24, h=90),
    ],
    watch=['a', 'b', ('ch', 'ch', 'yellow'), ('f0', 'f0', 'blue'), ('f1', 'f1', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录最大波动，初值 0',
        'for a, b in permutations': lambda S, B, r: ('字母对都枚举完了' if S.get('a') is not None and S.a == B.get('a') and S.b == B.get('b') else f'枚举字母对：`a = {S.a!r}` 当「出现最多」（每个记 +1），`b = {S.b!r}` 当「出现最少」（每个记 −1）'),
        'f0, f1 = 0, -inf': '`f0`：以当前位置结尾的最大子数组和（含不含 b 都行）；`f1`：==一定含 b== 的最大和，一开始不存在 → `−∞`',
        'if ch == a': lambda S, B, r: (f'`ch = {S.ch!r}` 就是 a（+1）' if S.ch == S.a else f'`ch = {S.ch!r}` 不等于 `a = {S.a!r}`'),
        'f0 = max(f0, 0) + 1': '`a` 记 +1：前面的和为负就丢掉（`max(f0, 0)`），再 +1 → `f0 = {f0}`',
        'f1 += 1': lambda S, B, r: (f'`f1` 还是 `−∞`：前面没有 b，接上 a 也不算数' if S.f1 == float('-inf')
                                     else f'`f1` 已经含 b，再接一个 a → `f1 = {S.f1}`'),
        'elif ch == b': lambda S, B, r: (f'`ch = {S.ch!r}` 是 b（−1）' if S.ch == S.b else f'`ch = {S.ch!r}` 既不是 a 也不是 b，`f0`、`f1` 都不变'),
        'f1 = f0 = max(f0, 0) - 1': '`ch = {ch!r}` 就是 b（−1）：`f0 = max({B.f0}, 0) − 1 = {f0}`；这个子数组必含 b，所以 `f1` 也等于它 → `f1 = {f1}`',
        'ans = max(ans, f1)': lambda S, B, r: (f'`f1 = −∞`（还没出现 b），不更新：`ans = {S.ans}`' if S.f1 == float('-inf')
                                               else f'只用「==含 b==」的 `f1` 更新答案：`ans = max({B.ans}, {S.f1}) = {S.ans}`（只含 a 的子串波动是 0，不能用 `f0`）'),
        'return ans': '所有字母对都试过，最大波动 =={ans}==',
    },
    cards=dict(
        one_liner='枚举「最多」和「最少」两个字母，转成最大子数组和',
        complexity='时间 `O(n·|Σ|²)`，空间 `O(1)`',
        problem=['波动 = 子串里出现最多的字符次数 − 出现最少的字符次数，求所有子串的最大波动',
                 '示例：`s = "aababbb"` → `3`（子串 `babbb`：4 个 b − 1 个 a）',
                 '演示把字母表缩成 `a`、`b` 两个，只枚举 2 对字母'],
        quote='最大波动值只由 s 中的两种字母决定……设出现次数最多的字母为 a，出现次数最少的字母为 b。把 a 视作 1，b 视作 -1，其余字母视作 0，最大波动值就等同于 53. 最大子数组和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举有序字母对 `(a, b)`：`a` 记 +1，`b` 记 −1，子数组和 = a 的个数 − b 的个数',
              '和 53 题的区别：`b` 必须在子串里。多一个状态 `f1` 表示「一定含 b」',
              '`f1` 初值 `−∞`，遇到 b 才「落地」成 `f0`，答案只取 `f1`'],
        summary=['复杂度 `O(n·|Σ|²)`，`|Σ| = 26`；灵神还给了「只遍历 s 一次、更新 26×26 矩阵」的 `O(n·|Σ|)` 优化写法',
                 '易错：不能用 `f0` 更新答案，只含 a 的子串波动其实是 0',
                 '易错：`f1` 初值是 `−inf`，不是 0，否则「没有 b」也会被当成合法',
                 '为了演示清晰，`setup` 里把 `ascii_lowercase` 缩成 `ab`（只影响枚举的字母对数，算法不变）'],
    ),
)
