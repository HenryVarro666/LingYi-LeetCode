def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st, tg = S.get('start'), S.get('target')
    if st is None:
        return
    cs = min(62, (y1 - y0 - 70) / 8, (x1 - x0 - 60) / 8)
    bx = x0 + ((x1 - x0) - cs * 8) / 2
    by = y0 + 44
    cv.text((bx, y0 + 6), '棋盘（浅格 x+y 为偶，深格为奇；蓝框 = 起点，粉框 = 终点）', 22, T['muted'], bold=True)
    for x in range(8):
        for y in range(8):
            X, Y = bx + x * cs, by + (7 - y) * cs
            fill = (92, 100, 112) if (x + y) % 2 == 0 else (52, 58, 68)
            cv.rect((X, Y, X + cs, Y + cs), fill=fill)
    for name, p, c in (('起点', st, T['blue']), ('终点', tg, T['pink'])):
        X, Y = bx + p[0] * cs, by + (7 - p[1]) * cs
        cv.rect((X + 2, Y + 2, X + cs - 2, Y + cs - 2), outline=c, width=5, r=6)
        cv.text((X + cs / 2, Y + cs / 2), f'{p[0] + p[1]}', 26, c, anchor='mm', bold=True)


CONFIG = dict(
    num=3996, title='偶数次骑士移动', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='格子颜色奇偶',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1260'],
    code='''
class Solution:
    def canReach(self, start: list[int], target: list[int]) -> bool:
        return (start[0] + start[1]) % 2 == (target[0] + target[1]) % 2
''',
    call='Solution().canReach([1, 1], [2, 2])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"起点 `x+y = {S['start'][0] + S['start'][1]}` → 颜色 =={(S['start'][0] + S['start'][1]) % 2}==；终点 `x+y = {S['target'][0] + S['target'][1]}` → 颜色 =={(S['target'][0] + S['target'][1]) % 2}==" if 'start' in S else ''),
    ],
    watch=[('start', 'start', 'blue'), ('target', 'target', 'pink')],
    captions={
        'return': '起点颜色 `({start[0]} + {start[1]}) % 2 = {(start[0] + start[1]) % 2}`，终点颜色 `({target[0]} + {target[1]}) % 2 = {(target[0] + target[1]) % 2}`：颜色相同 → 偶数步一定到得了，返回 =={ret}==',
    },
    cards=dict(
        one_liner='马每走一步换一次格子颜色，偶数步颜色不变',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘上，问骑士能否用 ==偶数== 次移动从 `start` 走到 `target`',
                 '示例：`[1,1]` → `[2,2]`，答案 `true`',
                 '示例：`[4,5]` → `[6,6]`，答案 `false`'],
        quote='马走奇数步，格子颜色会变；走偶数步，格子颜色不变。所以 start 和 target 的格子颜色必须相同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['马走一步，颜色必变；走两步，颜色变回来',
              '马走两步能到周围任意同色格子 → 偶数步能走遍所有同色格',
              '颜色用 `(x+y) % 2` 区分：同一条斜线颜色相同'],
        before=[dict(heading='先观察：一步会发生什么', lines=['骑士走「日」字，每步横纵各动 1 格和 2 格', '坐标和 `x+y` 一步变化 `±1` 或 `±3`，==一定是奇数==', '所以走一步，`x+y` 的奇偶翻转，格子颜色也翻转'])],
        after=[dict(heading='为什么偶数步够用', lines=['必要：偶数步 = 翻转偶数次 → 颜色必须不变', '充分：走两步可以到曼哈顿距离为 2 的同色格', '8×8 的棋盘足够大，同色格之间两步两步总能连通', '所以 ==颜色相同 ⇔ 偶数步可达=='])],
        summary=['时间、空间都是 `O(1)`，一行搞定',
                 '必要性：偶数步颜色不变；充分性：走两步可到曼哈顿距离 2 的同色格',
                 '易错点：别去写 BFS 数步数，只问奇偶',
                 '同类题：脑筋急转弯 · 奇偶性分析'],
    ),
)
