def _nl(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    num, t = S['num'], S['t']
    hi = num + 2 * t
    n = t + 1
    cw = min(120, (x1 - x0 - 80) / n)
    sx = x0 + ((x1 - x0) - cw * n) / 2
    top = y0 + 50
    cv.text((x0 + 18, y0 + 4), '每一步：x 减 1，num 加 1，两数逐步靠拢', 24, T['muted'], bold=True)
    for k in range(n):
        X = sx + k * cw + cw / 2
        yv = top + 40 + k * 60
        cv.text((X, top), f'第 {k} 步', 20, T['dim'], anchor='mm')
        cv.text((X, top + 50), f'x={hi - k}', 28, T['green'], anchor='mm', bold=True)
        cv.text((X, top + 100), f'num={num + k}', 28, T['blue'], anchor='mm', bold=True)
    cv.text((x0 + 18, top + 160), f'走 t = {t} 步后相遇：x = num + t + t = {num} + {t} + {t} = {hi}', 28, T['yellow'])


CONFIG = dict(
    num=2769, title='找出最大的可达成数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='每步 x 减 1、num 加 1',
    tags=[],
    code='''
class Solution(object):
    def theMaximumAchievableX(self, num, t):
        return num + t + t
''',
    call='Solution().theMaximumAchievableX(4, 3)',
    expect=10,
    views=[
        dict(type='custom', draw=_nl, h=360),
        dict(type='text', fn=lambda S: f"答案：`num + t + t = {S['num']} + {S['t']} + {S['t']}` = =={S['num'] + 2 * S['t']}==", size=34, h=160),
    ],
    watch=[('num', 'num', 'blue'), ('t', 't', 'pink')],
    captions={
        'return num + t + t': '每步 `x` 减 1、`num` 加 1，`t` 步后相遇 → `num + t + t = {num} + {t} + {t}` = =={num + t + t}==',
    },
    cards=dict(
        one_liner='每一步都让答案减 1、num 加 1，答案就是 num + t + t',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['一次操作：`x` 加或减 `1`，同时可选让 `num` 加或减 `1`',
                 '不超过 `t` 次操作后 `x == num`，求最大的 `x`',
                 '示例：`num=4, t=1` → `6`；本视频用 `num=4, t=3` → `10`'],
        quote='为了使得答案最大，那么每一步都应该是让答案减去1，然后让num加上1，最终使得二者相等，而对应的答案就应该是num + t + t。',
        quote_src='—— yiduobo 题解原文',
        idea=['想让 `x` 最大，就让它每步往 `num` 靠 1，`num` 也往它靠 1',
              '`t` 步后，`x` 少了 `t`，`num` 多了 `t`',
              '二者相等：`x − t = num + t`，所以 `x = num + t + t`'],
        after=[dict(heading='验证示例', lines=['`num=4, t=1`：x 6→5，num 4→5，一步相遇，答案 `4+1+1 = 6`', '`num=3, t=2`：x 7→6→5，num 3→4→5，答案 `3+2+2 = 7`', '若 x 再大 1：差距 `2t+1`，每步最多缩 2，追不上'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '一次操作能让两数的差缩小 `2`，所以最大差是 `2t`',
                 '代码与原文一致，无需改动',
                 '对比灵神：灵神写成 `num + t * 2`，并分别讲「只加 num」「只减 x」两条路线'],
    ),
)
