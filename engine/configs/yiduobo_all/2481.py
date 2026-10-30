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
    if n % 2 == 0:
        for k in range(n // 2):
            a = math.pi * k / (n // 2)
            cv.line([(cx - R * math.cos(a), cy - R * math.sin(a)), (cx + R * math.cos(a), cy + R * math.sin(a))], T['green'], 4)
    else:
        for k in range(n):
            a = 2 * math.pi * k / n
            cv.line([(cx, cy), (cx + R * math.cos(a), cy + R * math.sin(a))], T['pink'], 4)


CONFIG = dict(
    num=2481, title='分割圆的最少切割次数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='观察规律 · 奇偶分类',
    tags=[],
    code='''
class Solution(object):
    def numberOfCuts(self, n):

        if n == 1:
            return 0
        elif n & 1:
            return n
        else:
            return n >> 1
''',
    call='[Solution().numberOfCuts(k) for k in (1, 3, 6)]',
    expect=[0, 3, 3],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=120, size=32,
             fn=lambda S: (f"`n = {S['n']}`：{'奇数，只能用半径' if S['n'] % 2 else '偶数，可以用直径'}" if S['n'] > 1 else 'n = 1：不用切') if 'n' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('n & 1', 'n & 1', 'yellow')],
    captions={
        'if n == 1': '`n = {n}`：{"整个圆已经是 1 等分，不用切" if n == 1 else "不是 1，继续判断奇偶"}',
        'elif n & 1': '`n & 1 = {n & 1}`：{"最低位是 1 → 奇数，必须用半径" if n & 1 else "最低位是 0 → 偶数，可以用直径"}',
        'return n >> 1': '偶数用直径，每条切出两块：`n >> 1 = {n} / 2` = =={ret}==',
        'return n\n': '奇数：返回 `n`',
    },
    cards=dict(
        one_liner='n 为奇数必须用半径，否则可以用直径一次切两块',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['切割是过圆心的线段（直径或半径），把圆切成相等的 `n` 等分',
                 '求最少切割次数',
                 '示例：`n=4` → `2`；`n=3` → `3`'],
        quote='当n为奇数时，必须使用半径来进行切割，否则就可以使用直径来进行切分，因此当n为奇数时，答案为n，否则为n / 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['观察样例找规律：`n=4` 两刀，`n=3` 三刀',
              '偶数能用直径，一刀产生两条边界；奇数不行，每个边界一刀',
              '特别注意 `n = 1`：不用切，答案 0'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：先判断 `n == 1`，否则会被当成奇数返回 1',
                 '`n & 1` 判奇偶，`n >> 1` 即 `n // 2`',
                 '对比灵神：灵神从扇形对称性解释，yiduobo 从样例观察规律'],
    ),
)
