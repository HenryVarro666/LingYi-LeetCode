def _info(S):
    if 's' not in S or 'i' not in S:
        return '枚举回文数的左半边，补上右半边得到整个回文数'
    n, k = S['n'], S['k']
    s = S['s']
    if len(s) != n:
        return f'左半边 `{S["i"]}`，补成回文数还差一步'
    v = int(s)
    st = f'回文数 `{s}`，`{s} % {k} = {v % k}`' + ('，能整除' if v % k == 0 else '，不能整除 → 跳过')
    if 'res' in S and S['_line'] >= 17:
        st += f'；本类排列数 `res = {S["res"]}`'
    return st


CONFIG = dict(
    num=3272, title='统计好整数的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举回文数 + 多重集排列数',
    tags=['组合数学', '难度分 2382'],
    code='''
class Solution:
    def countGoodIntegers(self, n: int, k: int) -> int:
        fac = [factorial(i) for i in range(n + 1)]
        ans = 0
        vis = set()
        base = 10 ** ((n - 1) // 2)
        for i in range(base, base * 10):  # 枚举回文数左半边
            s = str(i)
            s += s[::-1][n % 2:]
            if int(s) % k:  # 回文数不能被 k 整除
                continue

            sorted_s = ''.join(sorted(s))
            if sorted_s in vis:  # 不能重复统计
                continue
            vis.add(sorted_s)

            cnt = Counter(sorted_s)
            res = (n - cnt['0']) * fac[n - 1]
            for c in cnt.values():
                res //= fac[c]
            ans += res
        return ans
''',
    setup='from math import factorial',
    call='Solution().countGoodIntegers(4, 3)',
    expect=84,
    skip=['continue', 'fac = [', 'base = 10', 'for c in cnt.values()', 'res //= fac[c]', 's = str(i)', 's += s[::-1]', 'for i in range'],
    max_steps=54,
    views=[
        dict(type='string', var='s', label='s：当前的回文数', h=130, cell=70),
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='set', var='vis', label='vis：已经统计过的「排序后的数位」', h=170, fmt=lambda x: str(x)),
        dict(type='map', var='cnt', label='cnt：各数位出现次数', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('res', 'res', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计好整数个数，`fac[i] = i!` 备用',
        'vis = set()': '`vis` 记录排序后的数位串，防止重复统计',
        'if int(s) % k': lambda S, B, r: (f'左半边 `{S.i}` → 回文数 `{S.s}`：`% {S.k} = {int(S.s) % S.k}`'
                                          + ('，不能被 k 整除 → 不是 k 回文数，跳过' if int(S.s) % S.k else '，能整除 → ==是 k 回文数==')),
        'sorted_s = ': '把数位排序得到 `{sorted_s}`：能互相重排的数，排序后都一样',
        'if sorted_s in vis': lambda S, B, r: (f'`{S.sorted_s}` 已在 vis 中 → 它的所有排列之前已经算过，==跳过==' if S.sorted_s in S.vis
                                                else f'`{S.sorted_s}` 第一次出现 → 要统计'),
        'vis.add': '记下 `{sorted_s}`',
        'cnt = Counter': '统计每个数位出现几次：`{dict(cnt)}`',
        'res = (n - cnt': '最高位不能是 0：有 `{n - cnt["0"]}` 种填法；其余 `{n - 1}` 位随便排 `{n - 1}!` = {fac[n - 1]} → `res` = =={res}==',
        'ans += res': lambda S, B, r: ('再除以每个数位个数的阶乘 `' + ' × '.join(f'{c}!' for c in S.cnt.values()) + f'` → `res` = {S.res}；`ans` = {B.ans} + {S.res} = =={S.ans}=='),
        'return ans': '一共 `{ret}` 个好整数',
    },
    cards=dict(
        one_liner='枚举所有 n 位回文数，排序去重，再数它们的排列个数',
        complexity='时间 `O(10^m · n log n)`，`m = (n-1)//2`',
        problem=['`k` 回文数：回文数且能被 `k` 整除',
                 '好整数：数位重排后能得到 `k` 回文数（任何时候不能有前导 0）',
                 '求 `n` 位好整数的个数；示例 `n=3, k=5` → `27`；本视频 `n=4, k=3`'],
        quote='考虑枚举所有长为 n 的回文数。首先，知道了回文数的左半边，就知道了回文数的右半边，所以可以枚举回文数的左半边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只枚举左半边：`10^m` 种；能被 `k` 整除才算 k 回文数',
              '把数位排序，排序后相同的回文数能生成同一批排列，用 `vis` 去重',
              '排列数 = 最高位非零的选法 `(n - cnt0)` × `(n-1)!` ÷ 各数位个数的阶乘'],
        summary=['时间 `O(10^m · n log n)`，空间约 `O(10^m · n)`',
                 '易错：最高位不能为 0，所以先乘 `n - cnt[0]`，其余 `n-1` 位再全排',
                 '易错：不去重会把 1221 和 2112 的排列重复算',
                 '`factorial` 来自 `math`，视频里在 setup 中导入'],
    ),
)
