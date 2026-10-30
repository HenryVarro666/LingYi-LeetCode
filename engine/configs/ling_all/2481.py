import math


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    if n is None:
        return
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2 - 30
    N = 160
    pts = [(cx + R * math.cos(2 * math.pi * k / N), cy + R * math.sin(2 * math.pi * k / N)) for k in range(N + 1)]
    cv.line(pts, T['border'], 4)
    if n == 1:
        cv.text((cx, cy), '整圆，不用切', 34, T['green'], anchor='mm', bold=True)
        return
    col = T['green'] if n % 2 == 0 else T['pink']
    if n % 2 == 0:
        for k in range(n // 2):
            a = math.pi * k / (n // 2)
            cv.line([(cx - R * math.cos(a), cy - R * math.sin(a)), (cx + R * math.cos(a), cy + R * math.sin(a))], col, 4)
    else:
        for k in range(n):
            a = 2 * math.pi * k / n
            cv.line([(cx, cy), (cx + R * math.cos(a), cy + R * math.sin(a))], col, 4)
    cv.text((cx, cy), '', 20, T['text'], anchor='mm')


CONFIG = dict(
    num=2481, title='分割圆的最少切割次数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='对称性 · 奇偶分类',
    tags=[],
    code='''
class Solution:
    def numberOfCuts(self, n: int) -> int:
        return n if n > 1 and n % 2 else n // 2
''',
    call='[Solution().numberOfCuts(k) for k in (1, 3, 6)]',
    expect=[0, 3, 3],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=120, size=32,
             fn=lambda S: (f"n = `{S['n']}` 是偶数：每条直径切出 2 块，切 `{S['n']}/2` = =={S['n']//2}== 次" if S['n'] % 2 == 0
                           else f"n = `{S['n']}` 是奇数：没有对称，每块都要一条半径 → ==`{S['n']}`== 次") if 'n' in S else ''),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return n if': '`n = {n}`：{"n > 1 且是奇数 → 切 n 次" if (n > 1 and n % 2) else ("n = 1 → n // 2 = 0，不用切" if n == 1 else "偶数 → 直径对称，切 n // 2 次")}，返回 =={ret}==',
    },
    cards=dict(
        one_liner='偶数靠对称用直径，奇数没有对称只能用半径',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['切割只能是过圆心的线段：整条直径，或一条半径',
                 '求把圆切成面积相等的 `n` 块，最少切几次',
                 '示例：`n=4` → `2`；`n=3` → `3`'],
        quote='n 为偶数时，每一块扇形都有对称的扇形，所以是切割 n/2 次；n 为奇数时，不存在对称性，所以是切割 n 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶数：每块扇形都能找到关于圆心对称的另一块，一条直径同时切出两块',
              '奇数：不存在这样的配对，每块都得单独一条半径',
              '特判 `n = 1`：整个圆本身就是一块，无需切割'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：`n = 1` 时答案是 0，不是 1',
                 '一行写法：`n if n > 1 and n % 2 else n // 2`',
                 '视频依次演示 `n = 1, 3, 6`，答案 0、3、3'],
    ),
)
