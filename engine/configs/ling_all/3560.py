def _bar(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, m, k = S['n'], S['m'], S['k']
    cv.text((x0 + 18, y0 + 4), f'两根木材（灰线 = 载重 k = {k}，超出部分要切掉）', 24, T['muted'], bold=True)
    mx = max(n, m, k) * 1.05
    W = x1 - x0 - 120
    for r, (name, L, c) in enumerate((('n', n, T['blue']), ('m', m, T['pink']))):
        y = y0 + 90 + r * 120
        cv.text((x0 + 20, y + 24), f'{name}={L}', 26, c, anchor='lm', bold=True)
        bx = x0 + 130
        cut = min(L, k)
        cv.rect((bx, y, bx + W * cut / mx, y + 48), fill=c, r=6)
        if L > k:
            cv.rect((bx + W * k / mx, y, bx + W * L / mx, y + 48), fill=T['red'], r=6)
            cv.text((bx + W * (k + L) / 2 / mx, y + 24), f'{L-k}', 26, T['bg'], anchor='mm', bold=True)
    kx = x0 + 130 + W * k / mx
    cv.line([(kx, y0 + 60), (kx, y0 + 290)], T['muted'], 3)


CONFIG = dict(
    num=3560, title='木材运输的最小成本', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='至多切一次 · 抛物线取端点 O(1)',
    tags=[],
    code='''
class Solution:
    def minCuttingCost(self, n: int, m: int, k: int) -> int:
        return max(k * (max(n, m) - k), 0)
''',
    call='Solution().minCuttingCost(10, 4, 6)',
    expect=24,
    views=[
        dict(type='custom', draw=_bar, h=330),
        dict(type='text', h=120, size=32,
             fn=lambda S: f"较长的木材 `max(n, m) = {max(S['n'], S['m'])}`，超出载重 `k = {S['k']}` 的部分是 `{max(S['n'], S['m']) - S['k']}`"),
        dict(type='text', h=120, size=32,
             fn=lambda S: f"成本 `k × (max(n, m) − k) = {S['k']} × {max(S['n'], S['m']) - S['k']}` = =={S['k'] * (max(S['n'], S['m']) - S['k'])}=="),
    ],
    watch=['n', 'm', 'k'],
    captions={
        'return max': '较长的那根 `max(n, m) = {max(n, m)}`，切成 `k = {k}` 和 `{max(n, m) - k}`：成本 `{k} × {max(n, m) - k}` = =={k * (max(n, m) - k)}==；若为负说明不用切，取 `0`。返回 `{ret}`',
    },
    cards=dict(
        one_liner='三辆车两根木，至多切一刀，且只会切较长的那根',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两根木材长 `n`、`m`，三辆卡车，每辆最多装一根长度不超过 `k` 的木材',
                 '把长 `x` 切成 `a` 和 `x−a`，成本 `a × (x−a)`，求最小总成本',
                 '示例：`n=6, m=5, k=5` → `5`；本视频：`10, 4, 6` → `24`'],
        quote='两根木材，三辆车，每辆车只能装一根木材，所以==至多切一次==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['成本 `x(n−x) = −x² + nx` 是开口向下的抛物线',
              '`n−k ≤ x ≤ k` 的范围内，最小值在端点 `x = k`，成本 `k(n−k)`',
              '题目保证有解，所以只有较长的那根可能要切：`max(k·(max(n,m)−k), 0)`'],
        after=[dict(heading='用示例验算', lines=['示例 1：`n=6, m=5, k=5`，切 `6 → 1 + 5`，成本 `1×5 = 5`','公式：`5 × (6−5) = 5`，与手算一致','示例 2：`4, 4, 6`：`max(6×(4−6), 0) = 0`，不用切'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '不用 `if`：`max(…, 0)` 统一处理不需要切割的情况',
                 '易错点：只取 `max(n, m)`，因为保证另一根 `≤ k`',
                 '两根都不超过 `k` 时答案为 `0`'],
    ),
)
