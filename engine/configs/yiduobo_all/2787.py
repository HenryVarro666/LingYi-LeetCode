def _fcolor(S, i, v):
    p, vv = S.get('i'), S.get('v')
    if p is None or vv is None or S.get('_line') not in (17, 18, 19):
        return None
    if i == p:
        return 'yellow'
    if i == p - vv:
        return 'blue'
    return None


def _formula(S):
    v = S.get('v')
    if S.get('_line') in (17, 18, 19) and S.get('i') is not None and 'f' in S and v is not None and 'candidate' in S and 'mod' in S:
        i = S['i']
        return f'`f[{i}] += f[{i}-{v}]`：加上「已经凑出 {i - v} 的方案」再放一个 `{v}`'
    if 'mod' in S:
        return '`f[i]` = 组成 `i` 的方案数；`candidate` 里每个幂只能用一次'
    return '先找出所有不超过 `n` 的 `b^x`，放进 `candidate`'


CONFIG = dict(
    num=2787, title='将一个数字表示成幂的和的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='先列幂，再 0-1 背包',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1818'],
    code='''
class Solution(object):
    def numberOfWays(self, n, x):

        candidate = []
        b = 1
        while True:
            v = b ** x
            if v > n:
                break
            candidate.append(v)
            b += 1
        
        f = [0] * (n + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for v in candidate:
            for i in range(n, v - 1, -1):
                f[i] += f[i - v]
                if f[i] >= mod:
                    f[i] -= mod
        
        return f[n]
''',
    call='Solution().numberOfWays(5, 1)',
    expect=3,
    max_steps=90,
    skip=['b += 1', 'if f[i] >= mod', 'f[i] -= mod'],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='candidate', label='candidate：所有 ≤ n 的幂（物品）', h=150, cell=80,
             color=lambda S, i, v: 'purple' if v == S.get('v') and S.get('f') is not None else None),
        dict(type='array', var='f', label='f[i]：组成 i 的方案数（黄 = 正在更新，蓝 = f[i-v]）', h=240, cell=90,
             color=lambda S, i, v: _fcolor(S, i, v)),
    ],
    watch=[('b', 'b', 'blue'), ('v', 'v', 'purple'), ('i', 'i', 'yellow'), ('f[n]', 'f[n]', 'green')],
    captions={
        'candidate = []': '`candidate` 收集所有不超过 `n` 的幂',
        'v = b ** x': '`v = {b}^{x} = =={v}==`',
        'if v > n': lambda S, B, r: (f'`{S.v} > {S.n}`：再大的幂也装不下 → 停止' if S.v > S.n else f'`{S.v} ≤ {S.n}`，可以作为物品'),
        'break': '幂已经超过 `n`，后面只会更大 → 跳出，候选收集完毕',
        'candidate.append': '`{v}` 加入候选：`candidate = {candidate}`',
        'f = [0] * (n + 1)': '`f[i]` 表示组成 `i` 的方案数',
        'f[0] = 1': '组成 0 的方案数为 1（什么都不选）',
        'mod = ': '取模常数 `mod`',
        'for v in candidate': '依次考虑每个幂 `v = {v}`，它只能用一次',
        'for i in range': '`i` 从 `n` ==倒序==到 `v`：本轮算出的新值不会被本轮再次使用',
        'f[i] += f[i - v]': '`f[{i}] += f[{i - v}]`：多一种「最后放 `{v}`」的方案 → ==`{f[i]}`==',
        'if f[i] >= mod': '`f[{i}] = {f[i]}`，没超过 `mod` 就不用减',
        'return f[n]': '`f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='先把能用的幂列出来，再倒序做 0-1 背包',
        complexity='时间 `O(n·n^(1/x))`，空间 `O(n)`',
        problem=['把正整数 `n` 表示成若干 ==互不相同== 正整数的 `x` 次幂之和',
                 '返回方案数，对 `10^9 + 7` 取模',
                 '示例：`n = 4, x = 1` → `2`；本视频：`n = 5, x = 1` → `3`'],
        quote='首先遍历所有可用的幂v，接下来从f[n]倒序遍历到f[v]，使用f[i] += f[i - v]进行更新。这里倒序遍历的理由是每种幂只能使用一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 不大，先一趟循环算出所有 `≤ n` 的幂放进数组',
              '问题变成「从这些数里选一些凑成 `n`」，是经典背包',
              '一维 `f[i]`，必须倒序，防止同一个幂被重复使用'],
        summary=['时间 `O(n·n^(1/x))`，空间 `O(n)`',
                 '易错：倒序遍历；正序会变成完全背包',
                 '每次加法后立刻判断 `>= mod` 再减，避免数字过大',
                 '对比灵神：灵神最后才取模，不用边算边减'],
    ),
)
