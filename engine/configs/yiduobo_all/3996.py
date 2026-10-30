def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st, tg = S.get('start'), S.get('target')
    if st is None:
        return
    cs = min(62, (y1 - y0 - 70) / 8, (x1 - x0 - 60) / 8)
    bx = x0 + ((x1 - x0) - cs * 8) / 2
    by = y0 + 44
    cv.text((bx, y0 + 6), '棋盘（格内数字 = x+y；蓝框 = start，粉框 = target）', 22, T['muted'], bold=True)
    for x in range(8):
        for y in range(8):
            X, Y = bx + x * cs, by + (7 - y) * cs
            fill = (92, 100, 112) if (x + y) % 2 == 0 else (52, 58, 68)
            cv.rect((X, Y, X + cs, Y + cs), fill=fill)
            cv.text((X + cs / 2, Y + cs / 2), x + y, 16, T['dim'], anchor='mm')
    for name, p, c in (('start', st, T['blue']), ('target', tg, T['pink'])):
        X, Y = bx + p[0] * cs, by + (7 - p[1]) * cs
        cv.rect((X + 2, Y + 2, X + cs - 2, Y + cs - 2), outline=c, width=5, r=6)
        cv.text((X + cs / 2, Y + cs / 2), f'{p[0] + p[1]}', 26, c, anchor='mm', bold=True)


CONFIG = dict(
    num=3996, title='偶数次骑士移动', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='坐标和奇偶',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1260'],
    code='''
class Solution(object):
    def canReach(self, start, target):
        
        return (sum(target) + sum(start)) % 2 == 0
''',
    call='Solution().canReach([4, 5], [6, 6])',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: f"`sum(start) = {sum(S['start'])}`，`sum(target) = {sum(S['target'])}`，差为 =={abs(sum(S['target']) - sum(S['start']))}==" if 'start' in S else ''),
    ],
    watch=[('start', 'start', 'blue'), ('target', 'target', 'pink')],
    captions={
        'return': '`sum(target) + sum(start) = {sum(target)} + {sum(start)} = {sum(target) + sum(start)}`，是{"偶" if (sum(target) + sum(start)) % 2 == 0 else "奇"}数 → 差为{"偶" if (sum(target) + sum(start)) % 2 == 0 else "奇"}数，返回 =={ret}==',
    },
    cards=dict(
        one_liner='每跳一步坐标和变奇数，偶数步后坐标和差必为偶数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘，骑士一次走「日」字：一个方向两格，垂直方向一格',
                 '问能否 ==偶数次== 移动从 `start` 到 `target`',
                 '示例：`[4,5]` → `[6,6]`，答案 `false`'],
        quote='对于每次跳跃操作，相对于跳跃的起点，坐标之和的变化必然为奇数。进行了偶数次跳跃后，坐标之和的变化为偶数，反之则为奇数。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一点：8×8 棋盘上马可以到任意格子，不存在到不了的情况',
              '第二点：一步变化 1±2 或 2±1，和的变化是奇数',
              '所以看坐标和之差的奇偶：偶 → 可以，奇 → 不行'],
        before=[dict(heading='先看一步跳跃', lines=['马从 `(x, y)` 跳到 `(x±1, y±2)` 或 `(x±2, y±1)`', '坐标和变化量是 `±1` 或 `±3`', '==每跳一步，坐标和的奇偶性翻转=='])],
        after=[dict(heading='把两点合起来看', lines=['第一点：棋盘够大，任意两格都能跳到，不会无解', '第二点：偶数步 → 和的变化为偶数；奇数步 → 为奇数', '所以只要判断 `start` 与 `target` 的和之差是否为偶数'])],
        summary=['时间、空间都是 `O(1)`',
                 '`sum(target) + sum(start)` 与差同奇偶，用和代替差更省事',
                 '原文为 Python 2 风格，无需改动代码',
                 '对比灵神：灵神从格子颜色讲，yiduobo 从坐标和变化讲，本质同为奇偶'],
    ),
)
