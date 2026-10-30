import math


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = 6
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
    R = min(x1 - x0, y1 - y0) * 0.36
    cv.text((cx, y0 + 4), '把 6 拆成 6 个 1：每次拆分的代价 a×b = 两堆之间的「点对数」', 24, T['muted'], anchor='mt', bold=True)
    pts = [(cx + R * math.sin(2 * math.pi * k / n), cy - R * math.cos(2 * math.pi * k / n)) for k in range(n)]
    live = 'n' in S
    for a in range(n):
        for b in range(a + 1, n):
            cv.line([pts[a], pts[b]], T['cyan'] if live else T['border'], 3)
    for k, (px, py) in enumerate(pts):
        cv.rect((px - 20, py - 20, px + 20, py + 20), fill=T['blue'], r=20)
        cv.text((px, py), '1', 26, T['bg'], anchor='mm', bold=True)
    cv.rect((cx - 80, cy - 24, cx + 80, cy + 24), fill=T['bg'], r=10)
    cv.text((cx, cy), f'{n * (n - 1) // 2} 条边', 34, T['yellow'], anchor='mm', bold=True)
    cv.text((cx, y1 - 8), '每对「点」恰好在某一次拆分中被分开一次，总代价 = 点对数 C(n,2)', 22, T['muted'], anchor='mb')


CONFIG = dict(
    num=3958, title='拆分到 1 的最小总代价 II', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找规律 · O(1) 公式',
    code='''
class Solution(object):
    def minCost(self, n):
        
        return n * (n - 1) // 2
''',
    call='Solution().minCost(6)',
    expect=15,
    views=[
        dict(type='text', h=110, size=36, fn=lambda S: f"`n = {S['n']}`：总代价 = `n × (n − 1) // 2`" if 'n' in S else ''),
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', h=110, size=36, fn=lambda S: f"`{S['n']} × {S['n'] - 1} // 2` = ==`{S['n'] * (S['n'] - 1) // 2}`==" if 'n' in S else ''),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return n * (n - 1) // 2': '不论怎么拆，总代价都是 `n(n−1)/2`：`{n} × {n-1} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='不管怎么拆，总代价都固定是 n(n−1)/2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['一次操作把 `x` 拆成 `a + b`，代价 `a * b`',
                 '问把 `n` 拆成 `n` 个 1 的最小总代价，`n` 最大 5×10^7',
                 '本视频：`n = 6` → `15`'],
        quote='本题与之前的3857题题设相同，但是数据规模较大。不过之前已经通过找规律以及归纳法得到了O(1)的算法，直接沿用就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['3857 题 `n` 小，可以 DP；这题 `n` 太大，必须用公式',
              '之前找规律并归纳证明：总代价恒为 `n * (n - 1) // 2`',
              '直观理解：代价 `a*b` 是两堆之间的点对数，每对点只被分开一次'],
        after=[dict(heading='为什么不用拆法优化', lines=['每次拆分代价 = 被分开的点对数', '每对点只会被分开一次，共 `C(n,2)` 对', '所以所有拆法的总代价相同，没有「最小」之分']),
               dict(heading='小例子验证', lines=['`n = 3`：拆成 `1+2` 代价 2，再拆 `2` 代价 1，共 `3`', '公式 `3 × 2 // 2 = 3`，一致', '`n = 4`：`2+2` 代价 4，再各拆一次共 `6` = `4 × 3 // 2`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：必须用整数除法 `//`，`n` 大时用浮点会丢精度',
                 '本题没有灵神视频，灵神指向 3857 的同一结论',
                 '原文为 Python 2 写法，整数除法已是 `//`，无需改动'],
    ),
)
