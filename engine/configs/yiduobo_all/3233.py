L, R = 4, 20


def _isp(v):
    return v >= 2 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _rng(S):
    return list(range(0, R + 1))


def _col(S, i, v):
    sq = [p * p for p in range(2, 5) if _isp(p) and L <= p * p <= R]
    if v in sq:
        k = (R - L + 1) - S['res'] if 'res' in S else 0
        return 'yellow' if sq.index(v) < k else 'blue'
    return None


def _txt(S):
    if 'x' not in S:
        return f'`[l, r] = [{L}, {R}]`：特殊数字只能是质数的平方，只需检查 `x` 从 `√l` 到 `√r`'
    x = S['x']
    return f'检查 `x = {x}`：`x * x = {x * x}`；当前 `res` = =={S["res"]}=='


CONFIG = dict(
    num=3233, title='统计不是特殊数字的数字数量', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='反面计数 · 枚举 √l..√r 判质数',
    tags=['灵神题单·数学算法', '难度分 1509'],
    code='''
class Solution(object):
    def nonSpecialCount(self, l, r):

        res = r - l + 1
        for x in range(int(sqrt(l)), int(sqrt(r)) + 1):
            if x < 2:
                continue
            y = 2
            prime = True
            while y * y <= x:
                if x % y == 0:
                    prime = False
                    break
                y += 1
            
            if prime and l <= x * x <= r:
                res -= 1
        
        return res
''',
    call=f'Solution().nonSpecialCount({L}, {R})',
    expect=15,
    setup='from math import sqrt',
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=_rng, color=_col, cell=46, h=300,
             label=f'区间 0..{R}（粉箭头 = x²；蓝 = 区间里的质数平方，黄 = 已减掉的）',
             pointers={'x * x': 'pink'}),
    ],
    watch=['l', 'r', ('x', 'x', 'blue'), ('y', 'y', 'pink'), 'prime', ('res', 'res', 'green')],
    captions={
        'res = r - l + 1': '先假设区间里的数全都不是特殊数字：`res = {r} − {l} + 1 = {res}`',
        'for x in range': lambda S, B, r: ('`x` 枚举完了，剩下的就是答案' if 'x' in B and B.x == S.x
                                           else f'枚举 `x = {S.x}`：若它是质数，`{S.x * S.x}` 就是候选特殊数字'),
        'if x < 2': lambda S, B, r: f'`x = {S.x} < 2`：1 不是质数（0 也不是），跳过' if S.x < 2 else f'`x = {S.x} >= 2`：继续判是不是质数',
        'continue': '直接换下一个 `x`',
        'y = 2': '试除从 `y = 2` 开始',
        'prime = True': '先假设 `{x}` 是质数',
        'while y * y <= x': lambda S, B, r: (f'`{S.y}×{S.y} = {S.y*S.y} <= {S.x}`：还要试除' if S.y * S.y <= S.x
                                              else f'`{S.y}×{S.y} = {S.y*S.y} > {S.x}`：试除完了，没找到因子'),
        'if x % y == 0': lambda S, B, r: (f'`{S.x} % {S.y} = 0`：有因子 → 合数' if S.x % S.y == 0 else f'`{S.x} % {S.y} = {S.x % S.y}`：不整除'),
        'prime = False': '`{x}` 不是质数',
        'break': '已经知道不是质数，停止试除',
        'y += 1': '`y` → {y}',
        'if prime and': lambda S, B, r: (f'`{S.x}` 是质数，且 `l <= {S.x*S.x} <= r` 成立 → `{S.x*S.x}` 是特殊数字' if S.prime and S.l <= S.x * S.x <= S.r
                                          else (f'`{S.x}` 是质数，但 `{S.x*S.x}` 不在 `[l, r]` 内，不算' if S.prime else f'`{S.x}` 不是质数，`{S.x*S.x}` 不是特殊数字')),
        'res -= 1': '特殊数字不计入答案：`res` → {res}',
        'return res': '剩下 `{res}` 个不是特殊数字',
    },
    cards=dict(
        one_liner='特殊数字必是质数的平方，反过来数一数',
        complexity='时间 `O(√r · r^(1/4))`，空间 `O(1)`',
        problem=['恰有两个真因数的数叫特殊数字；求 `[l, r]` 里 ==不是== 特殊数字的个数',
                 '示例：`l = 4, r = 16` → `11`',
                 f'本视频：`l = {L}`，`r = {R}`'],
        quote='所有的特殊数字必然是某个质数的平方。',
        quote_src='—— yiduobo 题解原文',
        idea=['合数 `x` 若是特殊数字，除 1 和自身外只能有一个因子 `p`',
              '`p` 必是质数，且 `p == x / p`，所以 `x = p²`',
              '枚举 `x` 从 `√l` 到 `√r`，判质数，`x²` 在区间内就减 1'],
        summary=['原文为 Python 2 写法，本题无需修改，直接运行',
                 '易错：`x < 2` 要跳过（1 不是质数）',
                 '易错：`x*x` 也要落在 `[l, r]` 内（`int(sqrt(l))` 取整会偏小）',
                 '对比灵神：灵神预处理质数前缀和，查询 `O(1)`；这里每次现判质数'],
    ),
)
