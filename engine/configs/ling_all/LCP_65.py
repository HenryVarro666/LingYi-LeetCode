def _jx(S):
    return S['_inner'].get('j')


def _ok(S):
    return 'j' in S['_inner'] and 'x' in S and S['dis'] != inf


def _txt(S):
    if 'x' not in S or 'f' not in S:
        return '`pre[j]` = 折线最右端点离最低点 j 时，最大值−最小值的最小值'
    x, j = S['x'], S['_inner'].get('j')
    if j is None or 'dis' not in S['_inner'] or S['_inner']['dis'] == inf:
        return f'第 `x = {x}` 条指令：每个有效的 `j` 都试 ==正号 / 负号== 两种走法'
    dis = S['_inner']['dis']
    if j >= x:
        return f'`j = {j}`，`dis = {dis}`：正号 → 到 `{j + x}`；负号 → 到 `{j - x}`'
    return f'`j = {j} < x`：负号会 ==穿过最低点==，新最低点，`f[0] = {dis} − {j} + {x}`'


CONFIG = dict(
    num='LCP 65', title='舒适的湿度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='折线图 · 到下界的距离 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def unSuitability(self, operate: List[int]) -> int:
        mx = max(operate) * 2
        pre = [0] + [inf] * mx
        for x in operate:
            f = [inf] * (mx + 1)
            for j, dis in enumerate(pre):
                if dis == inf: continue  # 无效的长度（无法组成）
                if j + x <= mx: f[j + x] = min(f[j + x], max(dis, j + x))
                if j >= x: f[j - x] = min(f[j - x], dis)
                else: f[0] = min(f[0], dis - j + x)
            pre = f
        return min(pre)
''',
    call='Solution().unSuitability([5, 3, 7])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='operate', label='operate（逐个决定正负号）', cell=64, h=130,
             color=lambda S, i, v: 'blue' if 'x' in S and i == S['operate'].index(S['x']) else None),
        dict(type='array', var='pre', label='pre[j]：上一轮，j = 最右端点到最低点的距离', cell=52, h=170,
             pointers={_jx: 'pink'}, pointer_labels={_jx: 'j'},
             color=lambda S, i, v: 'cyan' if v != inf else None, dim=lambda S, i, v: v == inf),
        dict(type='array', var='f', label='f[j]：这一轮（取 min 更新，绿 = 有效）', cell=52, h=170,
             color=lambda S, i, v: 'green' if v != inf else None, dim=lambda S, i, v: v == inf),
    ],
    watch=['mx', 'x', ('j', "_inner.get('j')" and (lambda S: S['_inner'].get('j')), 'pink'), ('dis', lambda S: S['_inner'].get('dis'), 'cyan')],
    captions={
        'mx = max': '`mx = 2 × max(operate) = {mx}`：按「前缀和正负交替」构造，折线极差不会超过它，所以 `j ≤ mx`',
        'pre = [0]': '`pre[0] = 0`：还没放数，折线只有起点；其余距离 ==无法到达== = inf',
        'f = [inf]': '新一轮 `f` 全部先设为 inf；下面只枚举 `pre` 里==有效==的距离 `j`（inf 的直接跳过），`dis` = 此时折线的最大值 − 最小值',
        'if j + x <= mx': lambda S, B, r: (f'取 ==正号==：折线往上走，最右端点离最低点 `{S.j + S.x}`；极差变成 `max({S.dis}, {S.j + S.x})`，`f[{S.j + S.x}] = {S.f[S.j + S.x]}`'
                                        if S.j + S.x <= S.mx else f'正号：`j + x = {S.j + S.x} > mx = {S.mx}`，超过上界，不转移（反正更差）'),
        'if j >= x': lambda S, B, r: (f'取 ==负号==，向下走 `{S.x}` 没穿过最低点：距离变 `{S.j - S.x}`，极差不变 `f[{S.j - S.x}] = {S.f[S.j - S.x]}`'
                                   if S.j >= S.x else f'`j = {S.j} < x = {S.x}`：向下会 ==穿过最低点==，转到 else'),
        'else: f[0]': '负号穿过最低点：最右端点成为新的最低点，距离归 0；极差增加 `x − j`：`f[0] = {f[0]}`',
        'pre = f': '一轮结束：滚动数组 `pre = f`',
        'return min': '最后一个数放完，`min(pre)` = ==最小的极差== = `{ret}`',
    },
    skip=['for j, dis', 'if dis == inf'],
    max_steps=80,
    cards=dict(
        one_liner='把前缀和画成折线，问题变成：最小化 最高点 − 最低点',
        complexity='时间 `O(nU)`，空间 `O(U)`',
        problem=['每个 `operate[i]` 可以取正或取负，所有连续段之和的绝对值取最大，叫「整体不适宜度」',
                 '求所有正负号方案中，它的 ==最小值==',
                 '示例：`[5,3,7]` → `8`，方案 `[5,3,-7]`'],
        quote='画折线图，问题转换成最小化折线图中最大值与最小值的差。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]`：前 `i` 个数，折线最右端离最低点 `j` 时，极差的最小值（`j` 是相对距离，不是坐标）',
              '正号：`f[j+x] = max(f[j], j+x)`；负号没穿底：`f[j-x] = f[j]`；穿底：`f[0] = f[j] − j + x`',
              '用滚动数组 `pre → f`，只保留一行'],
        summary=['时间 `O(nU)`，空间 `O(U)`，`U = max(operate)`',
                 '`j` 是到下界的距离，不是坐标：这样状态只和 `mx = 2U` 有关',
                 '穿过最低点时极差要加 `x − j`，别忘了 `j < x` 才进 else',
                 '对比 yiduobo：他二分答案 + 判定，这里直接 DP 求极差'],
    ),
)
