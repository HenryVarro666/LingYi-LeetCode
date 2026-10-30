def _fc(S, k, v):
    i = S.get('i')
    if i is None or S.get('_line') not in (5, 6, 7, 8):
        return 'green' if v else None
    if k == i:
        return 'yellow'
    if S.get('_line') == 8 and 'x' in S and k == i + S['x'] ** 2:
        return 'green'
    return 'green' if v else None


CONFIG = dict(
    num=1510, title='石子游戏 IV', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='博弈 DP · 刷表法（必败态推出必胜态）',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1787'],
    code='''
class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        f = [False] * (n + 1)
        for i in range(n):
            if f[i]:
                continue
            for x in range(1, isqrt(n - i) + 1):
                f[i + x * x] = True
        return f[n]
''',
    call='Solution().winnerSquareGame(13)',
    expect=True,
    skip=['for x in range'],
    views=[
        dict(type='array', var='f', label='f[i]：剩 i 颗石子时先手是否必胜（绿 = 必胜 True，灰 = 必败 False）', h=300, cell=64,
             pointers={'i': 'blue'}, color=_fc),
        dict(type='text', size=26, h=70,
             fn=lambda S: (f"必败态 `f[{S['i']}]` = False：先手拿 `{S['x']}^2 = {S['x']**2}`，对手面对 `{S['i']}` → `f[{S['i'] + S['x']**2}]` ==必胜=="
                           if S.get('_line') == 8 and 'x' in S else '`i` 是必败态，才能把 `i + x^2` 推成必胜' if 'i' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('f[i]', 'f[i]', 'yellow')],
    captions={
        'f = [False]': '`f[i]` = 有 `i` 颗石子时先手能否必胜；==初始全部 False==（0 颗石子先手必败）',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：看剩 `{S.i}` 颗时先手的结局' if S.get('i') != B.get('i') else '所有 `i` 都处理完了'),
        'if f[i]': lambda S, B, r: (f'`f[{S.i}]` 是 True：必胜态不会影响后面，==跳过==' if S.f[S.i]
                                    else f'`f[{S.i}]` 是 False：先手必败，对手面对它就输 → 可以拿它去推别的状态'),
        'continue': '必胜态直接 `continue`',
        'f[i + x * x] = True': '从 `{i}` 出发拿 `x^2 = {x*x}`：谁面对 `{i + x*x}` 颗，先拿 `{x*x}` 颗留 `{i}` 给对手必输 → `f[{i + x*x}] = True`',
        'return f[n]': '`f[{n}] = {f[n]}` → =={ret}==',
    },
    cards=dict(
        one_liner='谁面对必败态谁输：从必败态往外「刷」出所有必胜态',
        complexity='时间 `O(n√n)`，空间 `O(n)`',
        problem=['Alice、Bob 轮流从 `n` 颗石子里拿走任意非零==平方数==颗，Alice 先手',
                 '没石子可拿的人输。双方都最优，Alice 赢返回 `true`',
                 '示例：`n = 1` → `true`；`n = 7` → `false`；本视频：`n = 13`'],
        quote='如果 f[i] = false，那么枚举 x^2，更新 f[i+x^2] 为 true，其中 i+x^2 ≤ n。对于 f[i] = true 的状态，由于不影响后续状态，直接 continue。',
        quote_src='—— 灵茶山艾府题解（刷表法）',
        idea=['`dfs(i)`：有 `i` 颗石子先手能否必胜；只要某个 `dfs(i−x^2)` 为 False，就必胜',
              '反过来看：`i` 颗必败，那么 `i + x^2` 颗时先拿 `x^2`，对手就面对必败 → 必胜',
              '必败态很少（`10^5` 内仅 2.8%），刷表比查表快得多'],
        summary=['时间 `O(n√n)`，空间 `O(n)`；实际只枚举必败态，更快',
                 '易错：`f[0] = False` 是边界，所以初始全 False，且 `i` 从 0 开始',
                 '易错：内层上界 `isqrt(n - i)`，保证 `i + x^2 <= n`',
                 '题解主线是记忆化搜索 `@cache` + 1:1 翻译成递推（查表法），这里选最后的刷表法',
                 '同类：博弈 DP 题单，如 486、1690、877'],
    ),
)
