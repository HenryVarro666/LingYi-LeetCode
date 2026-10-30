def _info(S):
    if 'n' not in S or 'target' not in S:
        return ''
    d = S['s'] - S['target']
    if d < 0:
        tail = '还没到终点'
    elif d % 2:
        tail = '相距奇数，反向步只能改偶数'
    else:
        tail = '相距偶数，可反向若干步恰好到达'
    return f"不回头走 {S['n']} 步：s = =={S['s']}==，s − target = =={d}==（{tail}）"


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S or 'target' not in S:
        return
    s, t, n = S['s'], S['target'], S['n']
    hi = max(s, t, 1)
    ax0, ax1 = x0 + 50, x1 - 120
    k = (ax1 - ax0) / hi
    y = y0 + 150
    cv.text((x0 + 18, y0 + 4), '数轴：青色 = 一路向右走到的位置 s，橙色 = 终点 target', 22, T['muted'], bold=True)
    cv.line([(ax0, y), (ax1, y)], T['border'], 3)
    pos = 0
    for step in range(1, n + 1):
        nx = pos + step
        cv.rect((ax0 + pos * k + 1, y - 34, ax0 + nx * k - 1, y - 6), fill=T['cyan'], alpha=170 if step < n else 255, r=4)
        if (nx - pos) * k > 22:
            cv.text(((ax0 + pos * k + ax0 + nx * k) / 2, y - 20), step, 18, T['bg'], anchor='mm', bold=True)
        pos = nx
    cv.tri_up(ax0 + t * k, y + 8, 12, T['orange'])
    cv.text((ax0 + t * k, y + 26), f'target = {t}', 24, T['orange'], anchor='mt', bold=True)
    cv.tri_up(ax0, y + 8, 10, T['dim'])
    cv.text((ax0, y + 26), '0', 22, T['dim'], anchor='mt', bold=True)
    if s != t:
        cv.text((ax0 + s * k, y - 44), f's = {s}', 24, T['cyan'], anchor='mb', bold=True)
    if s > t:
        cv.rect((ax0 + t * k, y + 70, ax0 + s * k, y + 100), outline=T['pink'], width=3, r=6)
        cv.text(((ax0 + t * k + ax0 + s * k) / 2, y + 112), f'越过 {s - t}', 22, T['pink'], anchor='mt', bold=True)


CONFIG = dict(
    num=754, title='到达终点数字', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='先不回头走，再反向某些步', tags=['灵神题单', '难度分 2000'],
    code='''
class Solution:
    def reachNumber(self, target: int) -> int:
        target = abs(target)
        s = n = 0
        while s < target or (s - target) % 2:  # 没有到达（越过）终点，或者相距奇数
            n += 1
            s += n
        return n
''',
    call='Solution().reachNumber(-2)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=30),
        dict(type='custom', h=300, draw=_draw),
    ],
    watch=['target', ('n', 'n', 'blue'), ('s', 's', 'cyan')],
    captions={
        'target = abs': '`target = |{B.target}| = {target}`：终点对称，取绝对值不影响答案',
        's = n = 0': '`s` 是走 `n` 步后的步长之和，一开始都是 0',
        'while s < target': lambda S, B, r: (f'`s = {S.s}`，`target = {S.target}`：' + (f'还没到（越过）终点 → 继续' if S.s < S.target
                                              else (f'已越过终点，但相距 `{S.s - S.target}` 是奇数，反向步只能改偶数 → 继续' if (S.s - S.target) % 2
                                                    else f'已越过终点，相距 `{S.s - S.target}` 是偶数 → 把步长和为 `{(S.s - S.target)//2}` 的若干步反向即可，停'))),
        'n += 1': '再走一步，第 `{n}` 步步长为 `{n}`',
        's += n': '`s = {B.s} + {n} = {s}`',
        'return n': '最少 `{n}` 步：`s − target = {s - target}` 是偶数，反向若干步即可',
    },
    cards=dict(
        one_liner='一直往终点走，越过后看距离奇偶：偶数就能反向凑齐',
        complexity='时间 `O(√|target|)`，空间 `O(1)`',
        problem=['在数轴 0 处，第 `i` 次移动走 `i` 步，方向可选左或右',
                 '求到达 `target` 的最少移动次数',
                 '示例：`target=2` → `3`；`target=3` → `2`'],
        quote='如果不回头地往终点走 n 步，并恰好能走到终点，那么答案就是 n。如果无法恰好走到终点，就需要仔细讨论了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`target` 取绝对值（对称）',
              '先不回头走 `n` 步，直到 `s >= target`',
              '距离 `s - target` 为偶数：把和为一半的若干步反向，恰好到终点',
              '为奇数：继续多走（一两步），直到变成偶数'],
        summary=['时间 `O(√|target|)`；题解还给了公式写法 `O(1)`：`n + 1 + n % 2`',
                 '易错：不要只判断 `s >= target`，还要 `(s - target) % 2 == 0`',
                 '反向若干步总能凑出：`[1,s]` 内每个数都能由不同的 `[1,n]` 内数相加得到（归纳）',
                 '本视频演示循环写法，公式写法见题解'],
    ),
)
