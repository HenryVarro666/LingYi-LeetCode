def _t(S):
    if 'sv' not in S or 'dv' not in S or 'x' not in S:
        if 's' in S and 'd' in S and 'res' in S:
            return f"不删点：s 极差 `{S['s'][-1]} − {S['s'][0]}` = {S['s'][-1]-S['s'][0]}，d 极差 `{S['d'][-1]} − {S['d'][0]}` = {S['d'][-1]-S['d'][0]}"
        return ''
    return f"删掉点 `({S['x']}, {S['y']})`：s 差 =={S['sv']}==，d 差 =={S['dv']}== → 最大距离 =={max(S['sv'], S['dv'])}=="


def _cs(S, i, v):
    if 'x' in S and 'y' in S and 'sv' in S and S['_line'] >= 17:
        if v == S['x'] + S['y'] and i in (0, len(S['s']) - 1):
            return 'pink'
    return None


def _cd(S, i, v):
    if 'x' in S and 'y' in S and 'sv' in S and S['_line'] >= 17:
        if v == S['x'] - S['y'] and i in (0, len(S['d']) - 1):
            return 'pink'
    return None


CONFIG = dict(
    num=3102, title='最小化曼哈顿距离', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='开绝对值 · 最大最小与次大次小',
    tags=['灵神题单·数学算法', '难度分 2216'],
    code='''
class Solution(object):
    def minimumDistance(self, points):

        s = sorted([x + y for x, y in points])
        d = sorted([x - y for x, y in points])
        
        res = max(s[-1] - s[0], d[-1] - d[0])
        for x, y in points:
            if x + y == s[0]:
                sv = s[-1] - s[1]
            elif x + y == s[-1]:
                sv = s[-2] - s[0]
            else:
                sv = s[-1] - s[0]
            
            if x - y == d[0]:
                dv = d[-1] - d[1]
            elif x - y == d[-1]:
                dv = d[-2] - d[0]
            else:
                dv = d[-1] - d[0]
            
            res = min(res, max(sv, dv))

        return res
''',
    call='Solution().minimumDistance([[3,10],[5,15],[10,2],[4,4]])',
    expect=12,
    views=[
        dict(type='text', fn=_t, size=30, h=90),
        dict(type='text', fn=lambda S: 'points = ' + ' '.join(f'({a},{b})' for a, b in S['points']), size=28, h=70),
        dict(type='array', var='s', label='s = 排序后的 x+y（粉 = 被删点正好是端点）', color=_cs, h=190),
        dict(type='array', var='d', label='d = 排序后的 x−y', color=_cd, h=190),
    ],
    watch=[('res', 'res', 'green'), 'x', 'y', 'sv', 'dv'],
    captions={
        's = sorted': '`s` = 每个点的 `x+y`，排序：==最大 − 最小== 就是 s 方向的最大距离，得 `{s}`',
        'd = sorted': '`d` = 每个点的 `x−y`，排序，得 `{d}`',
        'res = max(s[-1]': '不删点时最大曼哈顿距离 = `max(s 极差, d 极差)` = `max({s[-1]-s[0]}, {d[-1]-d[0]})` = =={res}==，先当作答案上界',
        'for x, y in points': '枚举要删的点 `({x}, {y})`：`x+y = {x+y}`，`x−y = {x-y}`',
        'if x + y == s[0]': lambda S, B, r: (f'`x+y = {S.x+S.y}` 恰是最小的 s → 删掉后 s 的最小值变成次小 `{S.s[1]}`' if S.x + S.y == S.s[0] else f'`x+y = {S.x+S.y}` ≠ 最小 s `{S.s[0]}`，继续看是不是最大'),
        'elif x + y == s[-1]': lambda S, B, r: (f'`x+y = {S.x+S.y}` 恰是最大的 s → 删掉后最大值变成次大 `{S.s[-2]}`' if S.x + S.y == S.s[-1] else f'`x+y = {S.x+S.y}` 既不是最大也不是最小，s 极差不变'),
        'sv = s[-1] - s[1]': '删掉最小 s：`sv = {s[-1]} − {s[1]}` = =={sv}==',
        'sv = s[-2] - s[0]': '删掉最大 s：`sv = {s[-2]} − {s[0]}` = =={sv}==',
        'sv = s[-1] - s[0]': 's 的端点没动：`sv = {s[-1]} − {s[0]}` = =={sv}==',
        'if x - y == d[0]': lambda S, B, r: (f'`x−y = {S.x-S.y}` 恰是最小的 d → 删掉后看次小 `{S.d[1]}`' if S.x - S.y == S.d[0] else f'`x−y = {S.x-S.y}` ≠ 最小 d `{S.d[0]}`，继续看是不是最大'),
        'elif x - y == d[-1]': lambda S, B, r: (f'`x−y = {S.x-S.y}` 恰是最大的 d → 删掉后看次大 `{S.d[-2]}`' if S.x - S.y == S.d[-1] else f'`x−y = {S.x-S.y}` 既不是最大也不是最小，d 极差不变'),
        'dv = d[-1] - d[1]': '删掉最小 d：`dv = {d[-1]} − {d[1]}` = =={dv}==',
        'dv = d[-2] - d[0]': '删掉最大 d：`dv = {d[-2]} − {d[0]}` = =={dv}==',
        'dv = d[-1] - d[0]': 'd 的端点没动：`dv = {d[-1]} − {d[0]}` = =={dv}==',
        'res = min(res, max(sv, dv))': '删掉 `({x}, {y})` 后最大距离 = `max({sv}, {dv})` = {max(sv, dv)}；`res = min({B.res}, {max(sv, dv)})` = =={res}==',
        'return res': '删哪个点最优：最小的最大距离 = =={ret}==',
    },
    cards=dict(
        one_liner='开绝对值：最大曼哈顿距离 = x+y 的极差 与 x−y 的极差 的较大者',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['删掉恰好一个点，使剩下点两两曼哈顿距离的==最大值最小==',
                 '示例：`[[3,10],[5,15],[10,2],[4,4]]` → `12`（删第 2 个点）'],
        quote='最大的曼哈顿距离一定是某两个s之差或者某两个d之差。……若当前点的x与y之和与最大的s或者最小的s相同，那么就需要选取次大的s或者次小的s重新计算s之差的部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['`|dx|+|dy|` 拆成四种符号，合并后只剩 `s=x+y` 与 `d=x−y` 两类差',
              '所以最大距离 = `max(max s − min s, max d − min d)`',
              '删一个点：只有它恰是 s 或 d 的端点时才要换成次大/次小'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`s`、`d` 各排序一次，之后每个点 `O(1)` 判断',
                 '易错：端点值重复时（多个点同一 s）次大次小等于端点，结果仍正确',
                 '同类：1131 绝对值表达式的最大值（同样是拆绝对值）',
                 '原文已是 Python 3 可运行，未做修改'],
    ),
)
