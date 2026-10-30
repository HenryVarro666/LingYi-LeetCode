def _fc(S, k, v):
    num = S.get('num')
    if num is None:
        return 'green' if v else None
    if k == num:
        return 'yellow'
    if S.get('x') and k == num - S['x'] ** 2 and S.get('_line') in (8, 9, 10):
        return 'pink' if not v else 'blue'
    return 'green' if v else None


CONFIG = dict(
    num=1510, title='石子游戏 IV', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='博弈 DP · 枚举平方根',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1787'],
    code='''
class Solution(object):
    def winnerSquareGame(self, n):

        f = [False] * (n + 1)
        for num in range(1, n + 1):
            x = 1
            while x * x <= num:
                if not f[num - x * x]:
                    f[num] = True
                    break

                x += 1
        
        return f[-1]
''',
    call='Solution().winnerSquareGame(13)',
    expect=True,
    skip=['x = 1'],
    views=[
        dict(type='array', var='f', label='f[i]（绿 = 先手必胜；黄 = 正在算；粉 = 拿完后对手面对的必败态）', h=220, cell=64,
             pointers={'num': 'blue'}, color=_fc),
        dict(type='text', size=26, h=70,
             fn=lambda S: (f"拿 `{S['x']}×{S['x']} = {S['x']**2}` 颗 → 对手面对 `{S['num'] - S['x']**2}` 颗：`f[{S['num'] - S['x']**2}]` = {S['f'][S['num'] - S['x']**2]}"
                           if 'x' in S and 'num' in S and S['num'] - S['x'] ** 2 >= 0 and S.get('_line') in (8, 9, 10) else '')),
    ],
    watch=[('num', 'num', 'blue'), ('x', 'x', 'pink'), ('x*x', 'x*x', 'orange'), ('f[num]', 'f[num]', 'green')],
    captions={
        'f = [False]': '`f[i]` = 剩 `i` 颗时先手是否必胜；先全设 False，`f[0]` 先手无石可拿必败',
        'for num in range': lambda S, B, r: (f'`num = {S.num}`：先手面对 `{S.num}` 颗石子，枚举平方数' if S.get('num') != B.get('num')
                                             else '`f[1..n]` 都算完了'),
        'while x * x <= num': lambda S, B, r: (f'`x*x = {S.x*S.x} <= {S.num}`：这个平方数可以拿' if S.x * S.x <= S.num
                                               else f'`x*x = {S.x*S.x} > {S.num}`：再没有可拿的平方数 → `f[{S.num}]` 保持 ==False=='),
        'if not f[num - x * x]': lambda S, B, r: (f'拿 `{S.x*S.x}` 颗，对手面对 `{S.num - S.x*S.x}`：`f[{S.num - S.x*S.x}]` 是 False（必败）→ 成立' if not S.f[S.num - S.x*S.x]
                                                  else f'拿 `{S.x*S.x}` 颗，对手面对 `{S.num - S.x*S.x}`：`f[{S.num - S.x*S.x}]` 是 True（对手必胜）→ 这招不行'),
        'f[num] = True': '找到让对手必败的拿法 → `f[{num}] = True`（先手必胜）',
        'break': '已经必胜，不用再枚举了',
        'x += 1': '`x` → {x}，试下一个平方数 `{x*x}`',
        'return f[-1]': '`f[{n}] = {f[-1]}` → =={ret}==',
    },
    cards=dict(
        one_liner='枚举平方根：能把对手送进必败态，自己就必胜',
        complexity='时间 `O(n√n)`，空间 `O(n)`',
        problem=['Alice、Bob 轮流从 `n` 颗石子里拿走非零==完全平方数==颗，Alice 先手',
                 '无石可拿者输，双方最优，Alice 赢返回 `true`',
                 '示例：`n = 7` → `false`；`n = 4` → `true`；本视频：`n = 13`'],
        quote='没想到博弈论的做法，只好老老实实用动态规划来做。令f[i]表示剩余i颗式子的时候先手是否必胜……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：剩 `i` 颗时先手是否必胜；`f[0]` 为 False',
              '枚举平方根 `x`（`x*x <= i`）：若 `f[i - x*x]` 为假，先手拿走它就必胜',
              '一旦找到就 `break`；枚举完都没有则 `f[i]` 保持 False'],
        summary=['时间 `O(n√n)`，空间 `O(n)`',
                 '`f[0] = False` 是边界，`num` 从 1 开始',
                 '找到必胜拿法要 `break`，省去后面的枚举',
                 '本题代码本身是 Python 3 可运行的，未做修改',
                 '对比灵神：灵神有「刷表法」，只用必败态向外推；yiduobo 是对每个 `num` 向前查'],
    ),
)
