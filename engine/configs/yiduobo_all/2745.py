def _seq(x, y, z):
    m = min(x, y)
    if y > x:
        s = ['BB'] + ['AA', 'BB'] * m
        return s[:1] + ['AB'] * z + s[1:]
    if x > y:
        s = ['AA', 'BB'] * m + ['AA']
        return s[:2] + ['AB'] * z + s[2:] if m else ['AB'] * z + s
    s = ['AA', 'BB'] * m
    return s[:2] + ['AB'] * z + s[2:]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y, z = S['x'], S['y'], S['z']
    cv.text((x0 + 18, y0 + 4), '一种可行的构造（蓝 = BB，粉 = AA，绿 = AB）', 24, T['muted'], bold=True)
    seq = _seq(x, y, z)
    n = len(seq)
    cell = min(110, (x1 - x0 - 40) / max(n, 1))
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    top = y0 + 80
    col = {'AA': T['pink'], 'BB': T['blue'], 'AB': T['green']}
    for i, s in enumerate(seq):
        X = sx + i * cell
        cv.rect((X + 3, top, X + cell - 3, top + 90), fill=col[s], r=8, alpha=200)
        cv.text((X + cell / 2, top + 45), s, 34, T['bg'], anchor='mm', bold=True)
    cv.text(((x0 + x1) / 2, top + 130), ''.join(seq), 30, T['text'], anchor='mm', mono=True, bold=True)
    cv.text(((x0 + x1) / 2, top + 180), f'{n} 个字符串 × 2 = {2 * n} 个字符', 26, T['muted'], anchor='mm')


CONFIG = dict(
    num=2745, title='构造最长的新字符串', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='AB 不受影响 · 比较 x 与 y 分三类',
    tags=['贪心与思维', '难度分 1607'],
    code='''
class Solution(object):
    def longestString(self, x, y, z):
        if x > y:
            return (y + y + 1 + z) * 2
        elif x == y:
            return (x + y + z) * 2
        else:
            return (x + x + 1 + z) * 2
''',
    call='Solution().longestString(2, 5, 1)',
    expect=12,
    views=[
        dict(type='text', fn=lambda S: f'`x = {S["x"]}` 个 AA，`y = {S["y"]}` 个 BB，`z = {S["z"]}` 个 AB', size=30, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: 'BB 只能接在 AA 后面；AB 自带一个 B，又需要前导 B → 不改变可用的前导 B', size=24, h=60),
    ],
    watch=['x', 'y', 'z'],
    captions={
        'if x > y': lambda S, B, r: (f'比较 `x = {S.x}` 和 `y = {S.y}`：AA 更多 → ==AA 多于 BB== 的情况' if S.x > S.y
                                     else f'`x = {S.x} > y = {S.y}` 不成立，继续看别的情况'),
        'elif x == y': lambda S, B, r: (f'`x = y = {S.x}`：数量相同 → ==全都要==' if S.x == S.y
                                        else f'`x = {S.x}` ≠ `y = {S.y}`，不是相等的情况'),
        'return (y + y + 1 + z)': 'AA 必须接在 BB 或 AB 后，前导 B 只有 `y` 个，最多用 `y + 1` 个 AA：`(y+y+1+z)×2`',
        'return (x + y + z)': '`x = y`：去掉最开头的 BB，AA、BB 刚好全用上：`({x}+{y}+{z})×2` = =={ret}==',
        'return (x + x + 1 + z)': 'BB 只能接在 AA 后，AA 有 `{x}` 个，最多用 `x + 1` 个 BB：`({x}+{x}+1+{z})×2` = =={ret}==，最后接上 ABAB…',
    },
    cards=dict(
        one_liner='AB 不影响接法，只比较 x 和 y 的大小',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`x` 个 `"AA"`、`y` 个 `"BB"`、`z` 个 `"AB"`，选一部分按顺序连接',
                 '结果不能含 `"AAA"` 或 `"BBB"`，求最长长度',
                 '示例：`x=2, y=5, z=1` → `12`'],
        quote='AB的存在对另外两种字符串的接法不会产生任何影响，那么在这里就只需要考虑AA和BB的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['AB 需要前导 B，自己又提供一个 B → 对 AA、BB 的接法没有影响，全部都能用',
              '`y > x`：BB 被 x 个 AA 隔开，最多 `x+1` 个 → `x+x+1+z`',
              '`x = y` 全都要；`x > y`：最多 `y+1` 个 AA → `y+y+1+z`；最后都 `×2`'],
        result='`x=2 < y=5`：`(2+2+1+1)×2 = 12`',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：多的一方只能多用 1 个；相等时恰好全用',
                 '构造：先 `BBAABB…`，再接 `ABAB…`；或先 `ABAB…` 再接 `AABB…AA`',
                 '代码原样照搬，Python 3 直接可运行',
                 '对比灵神：灵神合成一个公式 `min(x,y)*2+(x!=y)+z`，yiduobo 分三类讨论'],
    ),
)
