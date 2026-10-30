CONFIG = dict(
    num=2400, title='恰好移动 k 步到达某一位置的方法数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索（剩余步数剪枝）',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1751'],
    code='''
class Solution:
    def numberOfWays(self, startPos: int, endPos: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        @cache
        def f(x: int, left: int) -> int:
            if abs(x - endPos) > left: return 0
            if left == 0: return 1  # 成功到达终点，算一种方案
            return (f(x - 1, left - 1) + f(x + 1, left - 1)) % MOD
        return f(startPos, k)
''',
    call='Solution().numberOfWays(1, 2, 3)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: list(range(-2, 6)), label='数轴（蓝 = 当前位置 x，绿 = 终点 endPos）', cell=70, h=170,
             pointers={'endPos + 2': 'green', "_inner.get('x', -99) + 2": 'blue'},
             pointer_labels={'endPos + 2': 'end', "_inner.get('x', -99) + 2": 'x'},
             color=lambda S, i, v: 'blue' if i - 2 == S['_inner'].get('x') else 'green' if i - 2 == S.get('endPos') else None),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"距终点 `|{S['_inner']['x']} − {S['endPos']}|` = =={abs(S['_inner']['x'] - S['endPos'])}==，还剩 `{S['_inner']['left']}` 步"
                           if 'x' in S['_inner'] else '`f(x, left)`：在 x，还剩 left 步，走到终点的方案数')),
        dict(type='calls', h=300),
    ],
    watch=[('endPos', 'endPos', 'green'), ('x', "_inner.get('x')", 'blue'), ('left', "_inner.get('left')", 'pink')],
    captions={
        'MOD = ': '答案可能很大，最后对 `10^9 + 7` 取余',
        '@cache': '加缓存：相同的 `(x, left)` 只算一次，递归树变成 DP 状态图',
        'abs(x - endPos) > left': lambda S, B, r: (f"`|x − endPos| = {abs(S.x - S.endPos)} > left = {S.left}`：剩下的步数走不到终点 → ==剪枝返回 0=="
                                                  if abs(S.x - S.endPos) > S.left else
                                                  f"`|x − endPos| = {abs(S.x - S.endPos)} ≤ left = {S.left}`：还有希望，继续"),
        'left == 0': lambda S, B, r: ('步数用完，且恰好站在终点 → ==算一种方案，返回 1==' if S.left == 0 else '还有剩余步数，继续枚举下一步'),
        'return (f(x - 1': '`f({B.x}, {B.left})` = 往左 `f({B.x - 1}, {B.left - 1})` + 往右 `f({B.x + 1}, {B.left - 1})`，==先进入下一层==，回来再相加取模',
        'return f(startPos, k)': '从 `startPos = {startPos}` 出发、共 `k = {k}` 步，调用 `f({startPos}, {k})`',
    },
    cards=dict(
        one_liner='f(x, left)：枚举往左还是往右，走不到终点就剪枝',
        complexity='时间 `O(k^2)`，空间 `O(k^2)`',
        problem=['在无限数轴上从 `startPos` 出发，每步向左或向右走 1',
                 '求==恰好走 k 步==到达 `endPos` 的不同走法数，结果对 `10^9 + 7` 取余',
                 '示例：`startPos=1, endPos=2, k=3` → `3`'],
        quote='定义 f(x, left) 表示当前在 x，还剩 left 步时，走到终点的方案数。枚举下一步往左或者往右，累加即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `(x, left)`：位置和剩余步数；下一步往左或往右，变成规模更小的子问题',
              '==剪枝==：`|x − endPos| > left` 时一定走不到，直接返回 0',
              '`left == 0` 且没被剪掉，说明恰好站在终点，算 1 种方案'],
        summary=['状态数 `O(k^2)`（x 只会在 startPos ± k 范围内），单个状态 `O(1)`',
                 '易错：先判断剪枝再判断 `left == 0`，否则会把没到终点的情况算成 1',
                 '灵神视频还讲了组合数学做法：往左走 b 步，答案是 `C(k, b)`'],
    ),
)
