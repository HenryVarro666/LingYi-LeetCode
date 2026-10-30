CONFIG = dict(
    num=2466, title='统计构造好字符串的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 边算边累加',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1694'],
    code='''
class Solution(object):
    def countGoodStrings(self, low, high, zero, one):

        f = [1]
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, high + 1):
            f.append(0)
            if index >= zero:
                f[-1] += f[index - zero]
                if f[-1] >= mod:
                    f[-1] -= mod
            if index >= one:
                f[-1] += f[index - one]
                if f[-1] >= mod:
                    f[-1] -= mod
        
            if index >= low:
                res += f[-1]
                if res >= mod:
                    res -= mod
        
        return res
''',
    call='Solution().countGoodStrings(3, 6, 1, 2)',
    expect=29,
    views=[
        dict(type='array', var='f', pointers={'index': 'blue'}, h=250, label='f[i]：长度为 i 的好字符串方案数',
             color=lambda S, i, v: 'green' if 'low' in S and i >= S['low'] else None),
        dict(type='text', size=28, fn=lambda S: (f"累加区间 `[{S['low']}, {S['high']}]`（绿色格）：`res` = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=['low', 'high', 'zero', 'one', ('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：空串，什么都不做也是一种方案',
        'res = 0': '`res` 用来累加长度在 `[low, high]` 内的 `f`',
        'for index': lambda S, B, r: (f'计算长度 `{S.index}` 的方案数 `f[{S.index}]`' if B.get('index') != S.index or 'f' not in B or len(B.f) < S.index + 1 else '`index` 走到 `high`，循环结束'),
        'f.append(0)': '先给 `f[{index}]` 占位 0，再累加两类来源',
        'if index >= zero': lambda S, B, r: (f'`index = {S.index} ≥ zero = {S.zero}`：末尾能放 `zero` 个 0，要加 `f[{S.index - S.zero}]`' if S.index >= S.zero else f'`index = {S.index} < zero = {S.zero}`：放不下，跳过'),
        'f[-1] += f[index - zero]': '`f[{index}] += f[{index - zero}]` → `{f[-1]}`',
        'if index >= one': lambda S, B, r: (f'`index = {S.index} ≥ one = {S.one}`：末尾能放 `one` 个 1，要加 `f[{S.index - S.one}]`' if S.index >= S.one else f'`index = {S.index} < one = {S.one}`：放不下，跳过'),
        'f[-1] += f[index - one]': '`f[{index}] += f[{index - one}]` → `{f[-1]}`',
        'if f[-1] >= mod': '`f[{index}] = {f[-1]}` 没超过 `mod`，不用减',
        'if index >= low': lambda S, B, r: (f'`index = {S.index} ≥ low = {S.low}`：长度合法，顺便累加进答案' if S.index >= S.low else f'`index = {S.index} < low = {S.low}`：长度太短，不计入答案'),
        'res += f[-1]': '`res += f[{index}]` → `res = {res}`',
        'if res >= mod': '`res = {res}` 没超过 `mod`，不用减',
        'return res': '`f[low]` 到 `f[high]` 累加完毕，答案 `{res}`',
    },
    cards=dict(
        one_liner='f[i] = f[i-zero] + f[i-one]，算到哪儿顺手累加到哪儿',
        complexity='时间 `O(high)`，空间 `O(high)`',
        problem=['每步在末尾放 `zero` 个 `0` 或 `one` 个 `1`，求长度在 `[low, high]` 的不同字符串数',
                 '结果对 `10^9+7` 取余',
                 '本视频：`low=3, high=6, zero=1, one=2` → `29`'],
        quote='令f[i]表示构造长度为i的好字符串的方案数，那么就有f[0] = 1，表示空串……由于题目要求的是长度在low到high之间的好字符串数目，那么在计算的过程中顺便统计f[low]到f[high]之间的累加和即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 先置 0；`i ≥ zero` 就加 `f[i-zero]`，`i ≥ one` 就加 `f[i-one]`',
              '最后一次放 0 还是放 1 互不重复，方案数直接相加',
              '长度进入 `[low, high]` 后，把 `f[i]` 边算边累加到 `res`'],
        summary=['时间 `O(high)`，空间 `O(high)`',
                 '易错点：==`f[0] = 1`==（空串）；`f` 与 `res` 每次加完都要取模',
                 '用 `if x >= mod: x -= mod` 取模，加法只会超过一次 `mod`',
                 '对比灵神：灵神还用 GCD 缩小规模；这里是最朴素的线性递推',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
