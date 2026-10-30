def _txt(S):
    if 'ans' not in S or 'i' not in S:
        return '把每个 limit 与 `n-1` 取小，再从小到大排序'
    if S['i'] >= S['j']:
        return '`i` 与 `j` 相遇，所有 `j` 都处理完了'
    return f'窗口 `[i, j-1]` 的和 `s` = =={S["s"]}==；`a[i] + a[j] = {S["a"][S["i"]] + S["a"][S["j"]]}`，`n = {S["n"]}`'


CONFIG = dict(
    num=3802, title='给纸张涂色的方式数量', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针 + 区间和',
    tags=[],
    code='''
class Solution:
    def numberOfWays(self, n: int, a: List[int]) -> int:
        MOD = 1_000_000_007
        for i in range(len(a)):
            a[i] = min(a[i], n - 1)
        a.sort()

        ans = 0
        s = sum(a)
        i, j = 0, len(a) - 1
        while i < j:
            if a[i] + a[j] < n:
                s -= a[i]
                i += 1
            else:
                s -= a[j]
                ans += s - (n - a[j] - 1) * (j - i)
                j -= 1
        return ans * 2 % MOD
''',
    call='Solution().numberOfWays(5, [3,6,2,4,1])',
    expect=34,
    views=[
        dict(type='text', h=70, size=30, fn=_txt),
        dict(type='array', var='a', label='a = limit（取小并排序后）；框 = 下标 [i, j-1]', pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j - 1'), h=300, cell=100,
             dim=lambda S, i, v: 'j' in S and i > S['j']),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'a[i] = min': '`a[{i}]` 与 `n-1 = {n-1}` 取小：必须恰好用两种颜色，所以一种颜色最多涂 `n-1` 张',
        'a.sort()': '从小到大排序：`{a}`，下面用相向双指针',
        'ans = 0': '`ans` 先只数 `i<j` 的方案，最后乘 2（对称）',
        's = sum(a)': '`s` 维护下标 `[i, j]` 的元素和（还没去掉 `a[j]`）：`{s}`',
        'i, j = 0': '`i` 在最小处，`j` 在最大处',
        'while i < j': lambda S, B, r: ('`i < j`，继续枚举' if S.i < S.j else f'`i = {S.i} ≥ j = {S.j}`：结束'),
        'if a[i] + a[j] < n': lambda S, B, r: (
            f'`{S.a[S.i]} + {S.a[S.j]} = {S.a[S.i] + S.a[S.j]} < {S.n}`：`a[i]` 连最大的 `a[j]` 都配不上'
            if S.a[S.i] + S.a[S.j] < S.n else
            f'`{S.a[S.i]} + {S.a[S.j]} = {S.a[S.i] + S.a[S.j]} ≥ {S.n}`：`a[j]` 能和 `a[i..j-1]` 全部配对'),
        's -= a[i]': '`a[i]` 与其他更小的 `a[j]` 也无法满足要求，没用了：`s` 去掉它 → {s}',
        'i += 1': '`i` 右移到 {i}',
        's -= a[j]': '把 `a[j]` 从和里去掉，`s` 变成 `[i, j-1]` 的和 = {s}',
        'ans += s': lambda S, B, r: (
            f'每个 `a[k]` 贡献 `a[k] − (n−a[j]−1)` 种 x：`{S.s} − ({S.n}−{S.a[S.j]}−1)×({S.j}−{S.i})` = '
            f'{S.s - (S.n - S.a[S.j] - 1) * (S.j - S.i)} → `ans` = =={S.ans}=='),
        'j -= 1': '`a[j]` 算完了，`j` 左移到 {j}',
        'return ans': '只数了 `i<j`，乘 2 再取模：`{ans} × 2` = =={ret}==',
    },
    cards=dict(
        one_liner='排序后相向双指针：每个 a[j] 一次算出它与 [i,j-1] 的全部方案',
        complexity='时间 `O(m log m)`，空间 `O(1)`',
        problem=['`n` 张纸，每种颜色 `k` 有上限 `limit[k]`',
                 '恰好用两种颜色，各涂连续的一段，涂的张数不超过上限，求方案数（模 `10^9+7`）',
                 '本视频：`n=5`，`limit=[3,6,2,4,1]` → `34`'],
        quote='如果 a[i]+a[j]<n，那么 a[i] 与其他更小的 a[j] 也无法满足要求，所以 a[i] 没用，去掉，把 i 加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选下标不同的 `(a_i, a_j)`，再选 `x+y=n`，`x ≤ a_i`，`y ≤ a_j`',
              '`x` 的个数 = `a_i − (n−a_j−1)`；对 `[i, j-1]` 求和：窗口和 − `(n−a_j−1)·(j−i)`',
              '先算 `i<j` 再乘 2；窗口和 `s` 随指针移动同步维护'],
        summary=['时间 `O(m log m)`，瓶颈在排序；空间 `O(1)`',
                 '先把 `limit` 与 `n-1` 取小，避免一种颜色涂满整张纸',
                 '`s` 要在算答案前先减去 `a[j]`，因为窗口是 `[i, j-1]`',
                 '只算 `i<j`，对称性乘 2；中途取模不影响结果',
                 '类似：两数之和 II / 三数之和（排序 + 相向双指针）'],
    ),
)
