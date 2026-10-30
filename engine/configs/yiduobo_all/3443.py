S0 = 'NSWWEW'
K = 3


def _idx(S):
    t = S['north'] + S['south'] + S['east'] + S['west']
    return t - 1 if S.get('_line') in (8, 10, 12, 14, 16) else t


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '前缀里四个方向的次数（成对看：南北一对、东西一对）', 22, T['muted'], bold=True)
    names = [('north', 'N 北', 'south', 'S 南', 'blue'), ('east', 'E 东', 'west', 'W 西', 'orange')]
    unit = 42
    for r, (a, an, b, bn, col) in enumerate(names):
        y = y0 + 60 + r * 160
        va, vb = S.get(a, 0), S.get(b, 0)
        mn = min(va, vb)
        for row, (nm, v, c) in enumerate(((an, va, T[col]), (bn, vb, T['pink'] if col == 'blue' else T['cyan']))):
            yy = y + row * (unit + 10)
            cv.text((x0 + 40, yy + unit / 2), f'{nm} = {v}', 24, T['text'], anchor='lm', bold=True)
            for j in range(v):
                X = x0 + 220 + j * (unit + 8)
                cancel = j < mn
                cv.rect((X, yy, X + unit, yy + unit), fill=c, alpha=90 if cancel else 255, r=8,
                        outline=T['yellow'] if cancel else None, width=3)
        if mn:
            cv.text((x0 + 40, y + 2 * (unit + 10) + 6), f'黄框 = 较少的 {mn} 个，可改成另一边 → 抵消反向', 20, T['yellow'], anchor='lm', bold=True)
    if 'north' in S:
        d = abs(S['north'] - S['south']) + abs(S['east'] - S['west'])
        m = min(min(S['north'], S['south']) + min(S['east'], S['west']), S['k'])
        cv.text((x0 + 40, y1 - 40), f"不改距离 {d}；可改 min(…, k) = {m} 次，每次 +2 → {d + 2 * m}", 24, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=3443, title='K 次修改后的最大曼哈顿距离', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='四方向计数 + 成对抵消',
    tags=['灵神题单', '难度分 1856'],
    code='''
class Solution(object):
    def maxDistance(self, s, k):

        north, south, east, west = 0, 0, 0, 0
        res = 0
        for c in s:
            if c == 'N':
                north += 1
            elif c == 'S':
                south += 1
            elif c == 'E':
                east += 1
            else:
                west += 1

            res = max(res, abs(north - south) + abs(east - west) + min(min(north, south) + min(east, west), k) * 2)

        return res
''',
    call=f'Solution().maxDistance({S0!r}, {K})',
    expect=6,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符）', h=140, cell=80,
             color=lambda S, k, v: 'blue' if 'c' in S and k == _idx(S) else None),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('north', 'north', 'blue'), ('south', 'south', 'pink'), ('east', 'east', 'orange'), ('west', 'west', 'cyan'),
           ('res', 'res', 'green')],
    captions={
        'north, south, east, west = 0': '四个变量分别统计当前前缀里 `N/S/E/W` 出现的次数',
        'res = 0': '`res` 记录所有前缀里最远的曼哈顿距离',
        'for c in s': lambda S, B, r: ('所有字符都处理完，循环结束' if S.north + S.south + S.east + S.west == len(S.s) else f'下一个字符 `{S.c}`，把它计入前缀'),
        "if c == 'N'": lambda S, B, r: ('`N`：向北，north 加 1' if S.c == 'N' else '不是 `N`，看下一个分支'),
        "elif c == 'S'": lambda S, B, r: ('`S`：向南，south 加 1' if S.c == 'S' else '不是 `S`，看下一个分支'),
        "elif c == 'E'": lambda S, B, r: ('`E`：向东，east 加 1' if S.c == 'E' else '不是 `E`，其余只剩 `W`'),
        'north += 1': '`north` → {north}',
        'south += 1': '`south` → {south}',
        'east += 1': '`east` → {east}',
        'west += 1': '`west` → {west}',
        'res = max': '不改：`|{north}-{south}| + |{east}-{west}|` = `{abs(north-south)+abs(east-west)}`；可抵消 `min(…, k)` = `{min(min(north, south) + min(east, west), k)}` 次，每次 +2 → `res` = =={res}==',
        'return res': '最远的曼哈顿距离 =={ret}==',
    },
    cards=dict(
        one_liner='把少的一边改成多的一边，每改一次距离 +2',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 由 `N/S/E/W` 组成，表示向北南东西各走 1 格',
                 '最多改 `k` 个字符，求过程中离原点的最大曼哈顿距离',
                 '示例：`s = "NSWWEW", k = 3` → `6`'],
        quote='将N和S中出现次数较少的那个尽量修改成另一个，对于E和W也是同样的处理方式。',
        quote_src='—— yiduobo 题解原文',
        idea=['横、竖互不相关：分别看 `N/S` 和 `E/W` 的差',
              '抵消次数 = `min(north,south) + min(east,west)`，但不超过 `k`',
              '每改一次抵消一次反向、多一次同向，距离 `+2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '要对每个前缀都算一次，最后取最大',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串',
                 '对比灵神：他用 `min(|x|+|y|+2k, i+1)` 一个式子，不用四个计数'],
    ),
)
