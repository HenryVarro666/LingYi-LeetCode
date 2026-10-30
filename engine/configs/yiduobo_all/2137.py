def _axis(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    hi = max(S['buckets']) * 1.0
    cv.text((x0 + 18, y0 + 4), '最终水量的候选区间 [left, right]（蓝 left，粉 right，黄 mid）', 22, T['muted'], bold=True)
    ax0, ax1 = x0 + 50, x1 - 50
    ya = y0 + 105

    def X(v):
        return ax0 + (ax1 - ax0) * v / hi
    cv.line([(ax0, ya), (ax1, ya)], T['border'], 4)
    for t in range(int(hi) + 1):
        cv.line([(X(t), ya - 8), (X(t), ya + 8)], T['dim'], 2)
        cv.text((X(t), ya + 14), t, 20, T['dim'], anchor='mt', mono=True)
    if 'left' not in S or 'right' not in S:
        return
    l, r = S['left'], S['right']
    cv.rect((X(l), ya - 12, max(X(r), X(l) + 3), ya + 12), fill=T['blue'], alpha=120, r=6)
    cv.tri_up(X(l), ya + 48, 10, T['blue'])
    cv.text((X(l) - 10, ya + 64), f'left={l:.5f}', 20, T['blue'], anchor='la', bold=True)
    cv.tri_up(X(r), ya + 48, 10, T['pink'])
    cv.text((X(r) + 10, ya + 92), f'right={r:.5f}', 20, T['pink'], anchor='ra', bold=True)
    if 'mid' in S and S.get('_line', 0) >= 10:
        m = S['mid']
        cv.line([(X(m), ya - 40), (X(m), ya + 12)], T['yellow'], 5)
        cv.text((X(m), ya - 46), f'mid={m:.5f}', 22, T['yellow'], anchor='mb', bold=True)


def _buckets(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    bs = S['buckets']
    n = len(bs)
    cv.text((x0 + 18, y0 + 4), f"buckets（虚线 = mid，多出的水倒出，不够的补满；补水要 ×100/(100−{S['loss']})）", 22, T['muted'], bold=True)
    cell = min(130, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    base, top = y1 - 60, y0 + 100
    scale = (base - top) / max(bs)
    mid = S['mid'] if 'mid' in S else None
    cur = S.get('v') if 'cnt' in S and S.get('_line', 0) >= 12 else None
    for i, v in enumerate(bs):
        Xl = sx + i * cell
        col = T['panel2']
        fill = (125, 133, 145)
        if mid is not None and cur is not None and v == cur and i == [j for j, w in enumerate(bs) if w == cur][0]:
            fill = T['orange'] if v > mid else T['cyan']
        cv.rect((Xl + 12, base - v * scale, Xl + cell - 12, base), fill=fill, r=6)
        cv.text((Xl + cell / 2, base - v * scale - 4), v, 24, T['text'], anchor='mb', bold=True)
        cv.text((Xl + cell / 2, base + 8), i, 18, T['dim'], anchor='mt', mono=True)
        if mid is not None and v > mid:
            cv.rect((Xl + 12, base - v * scale, Xl + cell - 12, base - mid * scale), fill=T['orange'], alpha=140, r=4)
        elif mid is not None and v < mid:
            cv.rect((Xl + 12, base - mid * scale, Xl + cell - 12, base - v * scale), outline=T['cyan'], width=3, r=4)
    if mid is not None:
        cv.dashed((sx, base - mid * scale), (sx + n * cell, base - mid * scale), T['yellow'], 3)
    cv.line([(sx, base), (sx + n * cell, base)], T['border'], 2)


def _cnt_text(S):
    if 'cnt' not in S:
        return ''
    c = S['cnt']
    return f"盈余 `cnt = {c:.4f}`：" + ('==还够用，水量可以更高==' if c >= 0 else '==亏空，水量要降低==')


CONFIG = dict(
    num=2137, title='通过倒水操作让所有的水桶所含水量相等', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 浮点二分',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def equalizeWater(self, buckets, loss):

        left = 0.0
        right = max(buckets) * 1.0
        eps = 10 ** -5

        while left < right - eps:
            mid = (left + right) / 2.0
            cnt = 0.0
            for v in buckets:
                if v > mid:
                    cnt += v - mid
                else:
                    cnt -= (mid - v) * 100 / (100 - loss)

            if cnt >= 0:
                left = mid
            else:
                right = mid
        
        return left
''',
    call='Solution().equalizeWater([1,2,7], 80)',
    expect=1.9999990463256836,
    views=[
        dict(type='text', fn=_cnt_text, size=26),
        dict(type='custom', draw=_axis, h=250),
        dict(type='custom', draw=_buckets, h=330),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'orange'), ('loss', 'loss', 'cyan')],
    captions={
        'left = 0.0': '最终水量最少是 `0`：`left = 0`',
        'right = max': '最终水量不会超过最大的桶：`right = {right}`',
        'eps = ': '精度要求 `10^-5`：区间小于它就停',
        'while left < right': lambda S, B, r: (f'区间宽 `{S.right - S.left:.5f}` > eps → 继续二分' if S.left < S.right - S.eps
                                               else f'区间宽 `{S.right - S.left:.6f}` ≤ eps → 结束'),
        'mid = (left': '猜每个桶最终都有 `mid = {mid:.5f}` 的水',
        'cnt = 0.0': '`cnt` 记录总盈余：多出的加进来，缺的从里面扣',
        'if v > mid': lambda S, B, r: (f'桶 `{S.v}` > `mid`：比目标多 → 要往外倒' if S.v > S.mid
                                       else f'桶 `{S.v}` ≤ `mid`：比目标少 → 要从盈余里补'),
        'cnt += v - mid': '多出 `{v} − {mid:.4f}`，全部进入盈余：`cnt = {cnt:.4f}`',
        'cnt -= (mid': '补 `{mid:.4f} − {v}`，但倒水会漏掉 `loss%`，所以要从盈余扣 ==×100/(100−loss)==：`cnt = {cnt:.4f}`',
        'if cnt >= 0': lambda S, B, r: (f'`cnt = {S.cnt:.4f} ≥ 0`：水够用，`mid` 可行 → 成立' if S.cnt >= 0
                                        else f'`cnt = {S.cnt:.4f} < 0`：水不够补，`mid` 太高'),
        'left = mid': '`mid` 可行，试试更高：`left = {left:.5f}`',
        'right = mid': '`mid` 不可行：`right = {right:.5f}`',
        'return left': '区间已小于 eps，`left = {left:.5f}` 就是最大水量',
    },
    skip=['for v in buckets', 'eps = '],
    max_steps=52,
    cards=dict(
        one_liner='二分「最终每个桶的水量」，一趟扫描算盈亏',
        complexity='时间 `O(n log(M/eps))`，空间 `O(1)`',
        problem=['有若干水桶 `buckets[i]`，可以把水从一个桶倒到另一个桶，倒水会损失 `loss` 百分比',
                 '求最终让所有桶水量相等时，==最大的水量==（误差 `10^-5` 内）',
                 '示例：`buckets = [1,2,7], loss = 80` → 约 `2.0`'],
        quote='每次二分最终各水桶的水量。对于当前二分到的水量mid，只需一趟遍历，使用一个变量cnt记录多出的水量。',
        quote_src='—— yiduobo 题解原文',
        idea=['水量越高越难凑齐：==单调==，所以能二分最终水量 `mid`',
              '大于 `mid` 的桶多出水，加到 `cnt`；小于 `mid` 的桶要补水，从 `cnt` 里扣',
              '补水有损耗：补 `d` 要消耗 `d × 100 / (100 − loss)`',
              '最后 `cnt ≥ 0` 说明够用，抬高下界，否则降低上界'],
        summary=['时间 `O(n log(M/eps))`，空间 `O(1)`',
                 '浮点二分用 `eps` 终止，每次 `left = mid` / `right = mid`，不加减 1',
                 '损耗系数是 `100 / (100 − loss)`：补 1 升要耗更多，别写成 `(100 − loss) / 100`',
                 '原文已是 Python 3 可运行的写法（`/` 都是浮点除法），未做修改',
                 '同类题：2226、1891（二分答案 + 一趟检查）'],
    ),
)
