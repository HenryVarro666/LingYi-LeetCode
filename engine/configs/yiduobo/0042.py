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
    """index whose water was added in this step (res changed), else None"""
    if 'res' not in B or S['res'] == B['res']:
        return None
    return S['left'] if S['highest_left'] < S['highest_right'] else S['right']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    h = S['height']
    n = len(h)
    cv.text((x0 + 18, y0 + 4), 'height（蓝 = 已算好的水，黄 = 这一步刚算出的）', 24, T['muted'], bold=True)
    cell = min(96, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    base, top = y1 - 96, y0 + 70
    scale = (base - top) / max(h)
    water = _water(h)
    live = 'left' in S and 'right' in S and 'res' in S
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
        dimmed = settled
        fill = (70, 76, 86) if dimmed else (125, 133, 145)
        if live and i == S['left'] and S['left'] <= S['right']:
            fill = T['cyan']
        elif live and i == S['right'] and S['left'] <= S['right']:
            fill = T['orange']
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
    if S['highest_left'] > 0:
        y = base - S['highest_left'] * scale
        cv.dashed((sx, y), (sx + min(l, n) * cell, y), T['cyan'], 3)
        cv.text((sx - 8, y), f"highest_left={S['highest_left']}", 19, T['cyan'], anchor='rm', bold=True)
    if S['highest_right'] > 0:
        y = base - S['highest_right'] * scale
        cv.dashed((sx + max(r + 1, 0) * cell, y), (sx + n * cell, y), T['orange'], 3)
        cv.text((sx + n * cell + 8, y), f"highest_right={S['highest_right']}", 19, T['orange'], anchor='lm', bold=True)
    for name, idx, c, row in (('left', l, T['blue'], 0), ('right', r, T['pink'], 1 if l == r else 0)):
        if 0 <= idx < n:
            X = sx + idx * cell + cell / 2
            cv.tri_up(X, base + 32, 10, c)
            cv.text((X, base + 48 + row * 26), name, 22, c, anchor='mt', bold=True)


def _side(S, B, ret):
    hl, hr = S.highest_left, S.highest_right
    if hl < hr and S.left > 0:
        return f'`{hl} < {hr}` → 计算 ==left=='
    if hl >= hr and S.right < len(S.height) - 1:
        return f'`{hl} ≥ {hr}` → 计算 ==right=='
    if hl < hr:
        return f'`highest_left = {hl} < highest_right = {hr}`：答案取决于矮的一侧 → ==计算 left=='
    return f'`highest_left = {hl} ≥ highest_right = {hr}`：右侧更矮（或相等）→ ==计算 right=='


def _lq(S, B, ret):
    h, hl = S.height[S.left], S.highest_left
    if h < hl:
        return f'`height[{S.left}] = {h} < {hl}`：比左侧最高矮 → 能接 `{hl} − {h} = {hl - h}`'
    return f'`height[{S.left}] = {h} ≥ {hl}`：接不了水，它成为新的左侧最高'


def _rq(S, B, ret):
    h, hr = S.height[S.right], S.highest_right
    if h < hr:
        return f'`height[{S.right}] = {h} < {hr}`：比右侧最高矮 → 能接 `{hr} − {h} = {hr - h}`'
    return f'`height[{S.right}] = {h} ≥ {hr}`：接不了水，它成为新的右侧最高'


CONFIG = dict(
    num=42, title='接雨水', difficulty='Hard', category='双指针',
    author='yiduobo', technique='左右双指针 · 只算矮的一侧',
    code='''
class Solution(object):
    def trap(self, height):
        left = 0
        right = len(height) - 1
        highest_left = 0
        highest_right = 0
        res = 0

        while left <= right:
            if highest_left < highest_right:
                if height[left] < highest_left:
                    res += highest_left - height[left]
                else:
                    highest_left = height[left]
                left += 1
            else:
                if height[right] < highest_right:
                    res += highest_right - height[right]
                else:
                    highest_right = height[right]
                right -= 1

        return res
''',
    call='Solution().trap([3,0,2,0,4,1,2])',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('highest_left', 'highest_left', 'cyan'),
           ('highest_right', 'highest_right', 'orange'), ('res', 'res', 'green')],
    captions={
        'highest_left = 0': '`highest_left`：left ==左侧==最高的柱子（不含 left 自己）',
        'left = 0': '左右双指针往内扫描：`left = 0`',
        'right = len': '`right = {right}`',
        'highest_right = 0': '`highest_right`：right ==右侧==最高的柱子',
        'res = 0': '`res` 累计水量',
        'while left <= right': lambda S, B, r: ('`left <= right`，继续' if S.left <= S.right
                                                else f'`left = {S.left} > right = {S.right}`：每根柱子都算过了 → 结束'),
        'if highest_left < highest_right': _side,
        'if height[left] < highest_left': _lq,
        'res += highest_left - height[left]': '`res` += `{highest_left} − {height[left]}` → {res}',
        'highest_left = height[left]': '`highest_left` 更新为 `{highest_left}`',
        'left += 1': '`left` → {left}',
        'if height[right] < highest_right': _rq,
        'res += highest_right - height[right]': '`res` += `{highest_right} − {height[right]}` → {res}',
        'highest_right = height[right]': '`highest_right` 更新为 `{highest_right}`',
        'right -= 1': '`right` → {right}',
        'return res': '一共接水 `{res}`',
    },
    cards=dict(
        one_liner='水量取决于左右最高中较矮的一侧：哪边矮就算哪边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`height[i]` 是宽为 1 的柱子高度，求下雨后能接多少水',
                 '示例：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`',
                 '本视频：`[3,0,2,0,4,1,2]` → `8`'],
        quote='在这个柱子上方能接的水取决于这个柱子左侧最高的柱子highest_left以及右侧最高的柱子highest_right中==较矮的那一个==。',
        quote_src='—— yiduobo 题解原文',
        idea=['柱高 `h`：两侧最高的较小值 `> h` 才能接水，接 `min(…) − h`',
              '和第 11 题一样，答案取决于==矮的一侧== → 左右双指针往内扫',
              '`highest_left < highest_right` 就算 left，否则算 right'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while left <= right`：相遇的那根柱子也要处理一次',
                 '`highest_left` 不含当前柱子：先判断能否接水，接不了才更新最高值',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神先用当前柱子更新 pre/suf_max 再算水；yiduobo 接不了水时才更新最高'],
    ),
)
