def _water(h):
    n = len(h)
    pre = [0] * n
    suf = [0] * n
    for i in range(n):
        pre[i] = max(pre[i - 1] if i else 0, h[i])
    for i in range(n - 1, -1, -1):
        suf[i] = max(suf[i + 1] if i < n - 1 else 0, h[i])
    return [min(p, s) - x for p, s, x in zip(pre, suf, h)]


def _just(S, B):
    """index whose water was added in this step (ans changed), else None"""
    if 'ans' not in B or S['ans'] == B['ans']:
        return None
    return S['left'] if S['pre_max'] < S['suf_max'] else S['right']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    h = S['height']
    n = len(h)
    cv.text((x0 + 18, y0 + 4), 'height（蓝 = 已确定的接水量，黄 = 这一步刚算出的）', 24, T['muted'], bold=True)
    cell = min(96, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    base, top = y1 - 96, y0 + 70
    scale = (base - top) / max(h)
    water = _water(h)
    live = 'left' in S and 'right' in S
    just = _just(S, B) if live else None
    for i, v in enumerate(h):
        X = sx + i * cell
        bw = cell * 0.7
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        settled = live and (i < S['left'] or i > S['right'])
        wet = (settled or i == just) and water[i] > 0
        if wet:
            wc = T['yellow'] if i == just else T['water']
            cv.rect((X + 1, base - (v + water[i]) * scale, X + cell - 1, base - v * scale), fill=wc, alpha=170)
            cv.text((X + cell / 2, base - (v + water[i] / 2) * scale), f'+{water[i]}', 24, T['bg'], anchor='mm', bold=True)
        dimmed = live and not (S['left'] <= i <= S['right'])
        fill = (70, 76, 86) if dimmed else (125, 133, 145)
        if live and i == S['left']:
            fill = T['blue']
        elif live and i == S['right']:
            fill = T['pink']
        cv.rect((bx0, base - max(3, v * scale), bx1, base), fill=fill, r=4)
        if not wet:
            cv.text((X + cell / 2, base - v * scale - 4), v, 24, T['muted'] if dimmed else T['text'], anchor='mb', bold=True)
        elif v * scale > 34:
            cv.text((X + cell / 2, base - v * scale + 6), v, 22, T['text'], anchor='mt', bold=True)
        cv.text((X + cell / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if not live:
        return
    l, r = S['left'], S['right']
    if S['pre_max'] > 0:
        y = base - S['pre_max'] * scale
        cv.dashed((sx, y), (sx + (l + 1) * cell, y), T['blue'], 3)
        cv.text((sx - 8, y), f"pre_max={S['pre_max']}", 20, T['blue'], anchor='rm', bold=True)
    if S['suf_max'] > 0:
        y = base - S['suf_max'] * scale
        cv.dashed((sx + r * cell, y), (sx + n * cell, y), T['pink'], 3)
        cv.text((sx + n * cell + 8, y), f"suf_max={S['suf_max']}", 20, T['pink'], anchor='lm', bold=True)
    for name, idx, c in (('left', l, T['blue']), ('right', r, T['pink'])):
        X = sx + idx * cell + cell / 2
        dy = 0 if name == 'left' or l != r else 26
        cv.tri_up(X, base + 32, 10, c)
        cv.text((X, base + 48 + dy), name, 22, c, anchor='mt', bold=True)


def _cmp(S, B, ret):
    p, s = S.pre_max, S.suf_max
    if p < s and S.left > 0:
        return f'`{p} < {s}` → 可以确定 ==left== 处的接水量'
    if p >= s and S.right < len(S.height) - 1:
        return f'`{p} ≥ {s}` → 可以确定 ==right== 处的接水量'
    if p < s:
        return f'`pre_max = {p} < suf_max = {s}`：left 的真实后缀最大 ≥ `{s}` > `{p}` → left 的水位就是 ==pre_max=='
    return f'`pre_max = {p} ≥ suf_max = {s}`：right 的真实前缀最大 ≥ `{p}` ≥ `{s}` → right 的水位就是 ==suf_max=='


CONFIG = dict(
    num=42, title='接雨水', difficulty='Hard', category='双指针',
    author='灵茶山艾府', technique='相向双指针（前后缀最大值）',
    code='''
class Solution:
    def trap(self, height: List[int]) -> int:
        ans = pre_max = suf_max = 0
        left, right = 0, len(height) - 1
        while left < right:
            pre_max = max(pre_max, height[left])  # 前缀最大值
            suf_max = max(suf_max, height[right])  # 后缀最大值
            if pre_max < suf_max:  # 可以确定 left 处的接水量
                ans += pre_max - height[left]
                left += 1  # 搞定了 left，现在问题缩小到 [left+1, right]
            else:  # 可以确定 right 处的接水量
                ans += suf_max - height[right]
                right -= 1  # 搞定了 right，现在问题缩小到 [left, right-1]
        return ans
''',
    call='Solution().trap([3,0,2,0,4,1,2])',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('pre_max', 'pre_max', 'blue'),
           ('suf_max', 'suf_max', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = pre_max = suf_max = 0': '`ans` 累计水量；`pre_max`、`suf_max` 是已遍历的前缀、后缀最大值',
        'left, right = 0': '`left = 0`，`right = {right}`：中间的柱子还不知道多高',
        'pre_max = max(': lambda S, B, r: (f'前缀 `[0, {S.left}]` 的最大高度：`pre_max = max({B.pre_max}, {S.height[S.left]}) = {S.pre_max}`'
                                           if B.pre_max == 0 else f'`pre_max = max({B.pre_max}, {S.height[S.left]}) = {S.pre_max}`'),
        'suf_max = max(': lambda S, B, r: (f'后缀 `[{S.right}, n−1]` 的最大高度：`suf_max = max({B.suf_max}, {S.height[S.right]}) = {S.suf_max}`'
                                           if B.suf_max == 0 else f'`suf_max = max({B.suf_max}, {S.height[S.right]}) = {S.suf_max}`'),
        'if pre_max < suf_max': _cmp,
        'ans += pre_max - height[left]': '`left = {left}` 处接水 `{pre_max} − {height[left]} = {pre_max - height[left]}`，`ans` = {ans}',
        'left += 1': '搞定了 left，问题缩小到 `[{left}, {right}]`',
        'ans += suf_max - height[right]': '`right = {right}` 处接水 `{suf_max} − {height[right]} = {suf_max - height[right]}`，`ans` = {ans}',
        'right -= 1': '搞定了 right，问题缩小到 `[{left}, {right}]`',
        'while left < right': lambda S, B, r: ('判断 `left < right` → 成立，继续' if S.left < S.right
                                               else f'`left == right == {S.left}`：相遇处是最高的柱子，接不了水 → 结束'),
        'return ans': '一共接水 `{ans}`',
    },
    cards=dict(
        one_liner='谁小移动谁：较小一侧的最大值，就是这一侧桶的水位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`height[i]` 是宽为 1 的柱子高度，求下雨后能接多少水',
                 '把每个位置看成宽 1 的水桶：水量 = `min(左边最高, 右边最高) − height[i]`',
                 '示例：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`；本视频：`[3,0,2,0,4,1,2]` → `8`'],
        quote='……left 处的接水量就是 preMax[left] − height[left]。这意味着，==在没有遍历完 height 数组的情况下，也能算出接水量==。',
        quote_src='—— 灵茶山艾府题解「方法二」',
        idea=['`pre_max < suf_max`：left 的后缀最大 ≥ `suf_max` > `pre_max` → 水位是 `pre_max`',
              '反之：right 的真实前缀最大 ≥ `pre_max` ≥ `suf_max` → 水位是 `suf_max`',
              '每一步确定一个桶，指针往中间收缩'],
        summary=['时间 `O(n)`，空间 `O(1)`：一次遍历',
                 '`while` 不加等号：相遇位置一定是最高的柱子，接不了水',
                 '方法一：前后缀分解，先算 `pre_max`、`suf_max` 数组，空间 `O(n)`',
                 '方法三：单调栈"横着"算：找上一个更大元素，在找的过程中填坑'],
    ),
)
