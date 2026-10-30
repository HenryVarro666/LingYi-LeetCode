INF = float('inf')


def _s(v):
    return '∞' if v == INF else '−∞' if v == -INF else str(v)


def _rng(S):
    return list(range(S.i - 2, max(S.i - S.k - 2, -1), -1))


def _info(S):
    if S.get('k') is None or S.get('i') is None:
        return '`f[i]`：以 `a[i]` ==不替换==、且前缀可行时，最长的「没被替换」序列长度'
    i, k, a, b = S['i'], S['k'], S['a'], S['b']
    if 'j' in S and S.get('_line') in (12, 13, 14, 15) and 0 <= S.get('j', -1) < i - 1 and S['j'] >= max(i - k - 1, 0):
        j = S['j']
        return f'`a[{j + 1}..{i - 1}]` 共 {i - j - 1} 个 → 换成 `b[{k - (i - j - 1)}..{k - 1}]`，最小的 `b[{k - (i - j - 1)}] = {b[k - (i - j - 1)]}` 要 `> a[{j}] = {_s(a[j])}`'
    return f'`b` 里比 `a[{i}] = {_s(a[i])}` 小的有 `k = {k}` 个：`a[{i}]` 左边最多能换 {k} 个数'


CONFIG = dict(
    num=1187, title='使数组严格递增', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='枚举选哪个 · 递推（LIS 变形）',
    tags=['灵神题单·动态规划', '难度分 2316'],
    code='''
class Solution:
    def makeArrayIncreasing(self, arr1: List[int], b: List[int]) -> int:
        a = arr1 + [inf]  # 简化代码逻辑
        b = sorted(set(b))  # 去重+排序
        n = len(a)  # 注意 a 已经添加了一个元素
        f = [0] * n  # 这里初始化成任何值都行
        for i, x in enumerate(a):
            k = bisect_left(b, x)
            res = 0 if k >= i else -inf  # 小于 a[i] 的数全部替换
            if i and a[i - 1] < x:  # 无替换
                res = max(res, f[i - 1])
            for j in range(i - 2, max(i - k - 2, -1), -1):
                if b[k - (i - j - 1)] > a[j]:
                    # a[j+1] 到 a[i-1] 替换成 b[k-(i-j-1)] 到 b[k-1]
                    res = max(res, f[j])
            f[i] = res + 1  # 把 +1 移到这里，表示 a[i] 不替换
        return -1 if f[-1] < 0 else n - f[-1]  # 注意 a 已经添加了一个元素
''',
    call='Solution().makeArrayIncreasing([1,5,3,6,7], [1,3,2,4])',
    expect=1,
    skip=['for j in range', 'n = len(a)'],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='array', var='a', label='a = arr1 + [inf]（蓝 = i，粉 = j）', h=215, cell=90, pointers={'i': 'blue', 'j': 'pink'}, min_slots=6,
             color=lambda S, i, v: 'blue' if i == S.get('i') else None),
        dict(type='array', var='b', label='b（去重排序；k = 第一个 ≥ a[i] 的位置）', h=215, cell=90, pointers={'k': 'yellow'}, min_slots=6),
        dict(type='array', var='f', label='f[i]：a[i] 不替换时，最多保留几个没被替换的数', h=170, cell=90,
             color=lambda S, i, v: 'green' if (S.get('i') is not None and i < S['i'] and v > 0) else None),
    ],
    watch=[('i', 'i', 'blue'), ('k', 'k', 'yellow'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'a = arr1': '`a` 末尾加个 ∞：这样最后一个数不用替换，答案就是 `n − f[n]`',
        'b = sorted': '`b` 去重（保证替换的数互不相同）并排序，替换时才能取连续的几个',
        'n = len(a)': '`n = {n}`（含末尾的 ∞）',
        'f = [0] * n': '`f[i]`：以 `a[i]` ==没被替换==结尾的最长序列长度；==不可行==时是负数',
        'for i, x in enumerate': lambda S, B, r: (f'枚举没被替换的 `a[{S.i}] = {_s(S.x)}`' if S.get('i') != B.get('i') or B.get('i') is None else '所有位置都算完了'),
        'k = bisect_left': lambda S, B, r: f'`b` 里小于 `{_s(S.x)}` 的有 `k = {S.k}` 个：`a[{S.i}]` 左边最多能换 `{S.k}` 个（取 `b[k-1]` 往前连续取）',
        'res = 0 if k >= i': lambda S, B, r: (f'`k = {S.k} >= i = {S.i}`：左边 {S.i} 个数全换掉也够 → 可行，`res = 0`' if S.k >= S.i
                                              else f'`k = {S.k} < i = {S.i}`：`b` 里小的数不够把左边全换掉 → `res = −∞`'),
        'if i and a[i - 1] < x': lambda S, B, r: (f'`a[{S.i - 1}] = {_s(S.a[S.i - 1])} < {_s(S.x)}`：相邻已经递增，==一个都不换==，可以接在 `f[{S.i - 1}]` 后' if S.i and S.a[S.i - 1] < S.x
                                                  else ('`i = 0`：左边没有数' if S.i == 0 else f'`a[{S.i - 1}] = {_s(S.a[S.i - 1])} ≥ {_s(S.x)}`：相邻不递增 → `a[{S.i - 1}]` 必须换掉，不能直接接')),
        'res = max(res, f[i - 1])': '`res = max(.., f[{i - 1}])` = =={res}==',
        'if b[k - (i - j - 1)] > a[j]': lambda S, B, r: (f'枚举 `j = {S.j}`：中间 `{S.i - S.j - 1}` 个换成 `b` 的最大几个，最小的 `b[{S.k - (S.i - S.j - 1)}] = {S.b[S.k - (S.i - S.j - 1)]} > a[{S.j}] = {_s(S.a[S.j])}` → ==可行==' if S.b[S.k - (S.i - S.j - 1)] > S.a[S.j]
                                                         else f'枚举 `j = {S.j}`：中间 `{S.i - S.j - 1}` 个换成 `b` 的最大几个，最小的 `b[{S.k - (S.i - S.j - 1)}] = {S.b[S.k - (S.i - S.j - 1)]} ≤ a[{S.j}] = {_s(S.a[S.j])}` → ==不行=='),
        'res = max(res, f[j])': '`a[{j + 1}..{i - 1}]` 全部换掉：`res = max(.., f[{j}])` = =={res}==',
        'f[i] = res + 1': lambda S, B, r: (f'`f[{S.i}] = res + 1` = =={S.f[S.i]}==：把 `a[{S.i}]` 自己算上' if S.res >= 0
                                           else f'`res` 为负：`a[{S.i}]` 不能被保留，`f[{S.i}] = {_s(S.f[S.i])}`'),
        'return -1 if f[-1]': '`f[-1] = {f[-1]}`：保留 `{f[-1] - 1}` 个原数，其余要替换，答案 `{n} − {f[-1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='盯住「没被替换」的数：最长保留序列 = n − 最少操作',
        complexity='时间 `O(n(log m + min(n, m)))`，空间 `O(n)`',
        problem=['`arr1[i] = arr2[j]` 可任意次替换，使 `arr1` ==严格递增==',
                 '求最少替换次数；做不到返回 `-1`',
                 '示例：`[1,5,3,6,7]`，`[1,3,2,4]` → `1`（5 换成 2）'],
        quote='我们把重点放在 lis 上，关注哪些 a[i] ==没有被替换==，那么答案就是 n−length(lis)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `a[i]` 左边最近没被替换的 `a[j]`，中间 `i−j−1` 个都要换成 `b` 的数',
              '`b[k−1]` 是比 `a[i]` 小的最大数，往前取连续的：最小的是 `b[k−(i−j−1)]`，它要 `> a[j]`',
              '末尾补 `∞` 当哨兵；`f[i]` 为负表示不可行'],
        after=[dict(heading='灵神的另一种写法', lines=['方法一「选或不选」：`dfs(i, pre)` + 哈希表记忆化', '复杂度 `O(nm log m)`，这里用的是方法二（只有 `O(n)` 个状态）'])],
        summary=['时间 `O(n(log m + min(n, m)))`，空间 `O(n)`',
                 '`b` 必须 `set` 去重：同一个数不能替换两处并保持严格递增',
                 '`j` 的下界 `i−k−1`：`b` 里比 `a[i]` 小的只有 `k` 个',
                 '`-inf` 表示不可行，`f[-1] < 0` 才返回 `-1`'],
    ),
)
