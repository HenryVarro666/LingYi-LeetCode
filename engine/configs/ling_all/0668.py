def _tab(S):
    return [[a * b for b in range(1, S['n'] + 1)] for a in range(1, S['m'] + 1)]


def _x(S):
    return S.get('x', S.get('mid'))


def _color(S, i, j, v):
    x = _x(S)
    if x is None:
        return None
    if 'i' in S and S.get('cnt') is not None and S['_line'] is not None and i == S['i'] - 1 and v <= x:
        return 'green'
    return 'blue' if v <= x else None


def _txt(S):
    x = _x(S)
    if 'left' not in S:
        return '乘法表第 i 行都是 i 的倍数'
    if x is None:
        return f"二分猜答案，开区间 `({S['left']}, {S['right']})`"
    return f"猜 `x = {x}`：表里 `≤ x` 的数（蓝色）有 ==`{sum(v <= x for r in _tab(S) for v in r)}`== 个，要 `≥ k = {S['k']}`"


def _chk(S, B, r):
    return f'`cnt = {S.cnt}`，`≥ k = {S.k}` → ==返回 {S.cnt >= S.k}=='


CONFIG = dict(
    num=668, title='乘法表中第k小的数', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 按行计数',
    tags=[],
    code='''
class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        def check(x: int) -> bool:
            cnt = x // n * n
            for i in range(x // n + 1, m + 1):
                cnt += x // i
            return cnt >= k

        left, right = 0, m * n
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call='Solution().findKthNumber(3, 4, 6)',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='table', var=_tab, label='乘法表 m×n（蓝 = ≤ x，绿 = 当前行已数入）', color=_color, rows=lambda S: list(range(1, S['m'] + 1)), cols=lambda S: list(range(1, S['n'] + 1)), h=300),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', 'x', 'cnt', ('k', 'k', 'green')],
    captions={
        'cnt = x // n * n': '前 `x // n = {x // n}` 行的每个数 `i × j`（`j ≤ n`）都 `≤ x`，整行 `n` 个全算：`cnt = {cnt}`',
        'for i in range': '逐行往下：第 `i` 行只有 `x // i` 个数 `≤ x`（`i` 的倍数）',
        'cnt += x // i': '第 `{i}` 行有 `{x} // {i} = {x // i}` 个 `≤ {x}` 的倍数 → `cnt` = {cnt}',
        'return cnt >= k': _chk,
        'left, right = 0': '开区间 `(0, m·n)`：`0` 一定不满足（0 个 `< k`），`m·n` 一定满足',
        'while left + 1': lambda S, B, r: (f'`left + 1 < right`（{S.left} + 1 < {S.right}）：开区间还不空 → 继续' if S.left + 1 < S.right
                                           else f'`left + 1 == right`：开区间空了，`right = {S.right}` 就是答案'),
        'mid = (': '取中点 `mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：数一数乘法表里 `≤ {mid}` 的数有几个',
        'right = mid': '`≤ {mid}` 的数够 `k` 个 → `mid` 可能是答案，`right = mid = {right}`',
        'left = mid': '`≤ {mid}` 的数不够 `k` 个 → 答案一定更大，`left = mid = {left}`',
        'return right': '第 `k` 小 = 最小的满足 `cnt ≥ k` 的 `x` = =={right}=='
    },
    cards=dict(
        one_liner='第 k 小 = 最小的 x，使得 ≤ x 的数至少有 k 个',
        complexity='时间 `O(m log(mn))`，空间 `O(1)`',
        problem=['`m × n` 的乘法表，`mat[i][j] = i * j`（下标从 1 开始），求第 `k` 小的数',
                 '示例：`m=3, n=3, k=5` → `3`',
                 '本视频：`m=3, n=4, k=6` → `4`'],
        quote='第 k 小等价于：求最小的 x，满足 ≤ x 的数至少有 k 个。（注意是至少不是恰好）',
        quote_src='—— 灵茶山艾府题解',
        idea=['x 越大越容易凑够 k 个，有单调性 → ==二分猜答案==',
              '第 `i` 行都是 `i` 的倍数，`≤ x` 的有 `min(x // i, n)` 个',
              '优化：`i ≤ x // n` 的行整行都算，只需从 `x // n + 1` 行开始累加'],
        summary=['时间 `O(m log(mn))`；`m > n` 时交换可做到 `O(min(m,n) log(mn))`',
                 '开区间 `(0, mn)`：左端点不满足、右端点必满足',
                 '要的是「至少 k 个」而不是恰好，所以 `check` 用 `>=`',
                 '二分结束的 `right` 一定在表里（反证：否则 `check(right-1)` 也成立）',
                 '另一种写法：不优化直接累加 `min(x // i, n)`，或用 `bisect_left` 库函数'],
    ),
)
