NUMS = [3, 9, 6, 1, 4]
K = 5


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if nums is None:
        return
    cv.text((x0 + 18, y0 + 4), 'nums（蓝色虚框 = 把窗口里的数都变成 x 需要的操作次数）', 24, T['muted'], bold=True)
    n = len(nums)
    vmax = max(nums)
    cell = min(130, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    base, top = y1 - 90, y0 + 80
    scale = (base - top) / vmax
    live = all(k in S for k in ('left', 'right', 'x')) and S.get('_line', 0) >= 6
    L, R, X = (S['left'], S['right'], S['x']) if live else (None, None, None)
    if live and S.get('_line') == 8:
        L += 1  # s 已经减去 nums[left]，left 下一步才右移：按移出后的窗口画
    if live and L <= R:
        yX = base - X * scale
        cv.dashed((sx + L * cell, yX), (sx + (R + 1) * cell, yX), T['orange'], 3)
        cv.text((sx + (R + 1) * cell + 6, yX), f'x = {X}', 22, T['orange'], anchor='lm', bold=True)
    for i, v in enumerate(nums):
        bx0, bx1 = sx + i * cell + cell * 0.18, sx + (i + 1) * cell - cell * 0.18
        inwin = live and L <= i <= R
        later = live and i > R
        if inwin and i == R:
            fill = T['orange']
        elif inwin:
            fill = T['cyan']
        elif later:
            fill = (52, 58, 68)
        else:
            fill = (110, 120, 132)
        if live and not inwin and i < L:
            fill = (70, 76, 86)
        cv.rect((bx0, base - v * scale, bx1, base), fill=fill, r=5)
        if inwin and v < X:
            cv.rect((bx0, base - X * scale, bx1, base - v * scale), fill=T['water'], alpha=90)
            cv.rect((bx0, base - X * scale, bx1, base - v * scale), outline=T['water'], width=2)
            if (X - v) * scale >= 40:
                cv.text(((bx0 + bx1) / 2, base - (X + v) / 2 * scale), f'+{X - v}', 24, T['text'], anchor='mm', bold=True)
            else:
                cv.text(((bx0 + bx1) / 2, base - X * scale - 6), f'+{X - v}', 24, T['blue'], anchor='mb', bold=True)
        if inwin and v < X:
            cv.text(((bx0 + bx1) / 2, base - v * scale + 6), v, 24, T['bg'], anchor='mt', bold=True)
        else:
            cv.text(((bx0 + bx1) / 2, base - v * scale - 6), v, 26, T['dim'] if later else T['text'], anchor='mb', bold=True)
        cv.text(((bx0 + bx1) / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if live:
        L0 = S['left']
        for name, idx, c, row in (('left', L0, T['green'], 0), ('right', R, T['pink'], 1 if L0 == R else 0)):
            X_ = sx + idx * cell + cell / 2
            cv.tri_up(X_, base + 32, 10, c)
            cv.text((X_, base + 48 + row * 26), name, 22, c, anchor='mt', bold=True)


def _text(S):
    if not all(k in S for k in ('left', 'right', 'x', 's')) or S.get('_line', 0) < 6:
        return '操作次数 = 矩形面积 `(right − left + 1) · x` − 窗口和 `s`'
    L, R, X, s = S['left'], S['right'], S['x'], S['s']
    if S.get('_line') == 8:
        return f'移出 `nums[{L}]` 后窗口是 `[{L + 1}, {R}]`，`s = {s}`'
    c = (R - L + 1) * X - s
    ok = '≤' if c <= K else '>'
    return f'操作次数 `{R - L + 1} × {X} − {s} = {c}` {ok} `k = {K}`'


def _cap_while(S, B, ret):
    w = B.right - B.left + 1
    c = w * B.x - B.s
    if c > B.k:
        return f'`{w} × {B.x} − {B.s} = {c} > k = {B.k}`：操作次数不够 → ==缩短窗口=='
    return f'`{w} × {B.x} − {B.s} = {c} ≤ k`：窗口里的数都能变成 `{B.x}`'


def _cap_for(S, B, ret):
    if 'right' in B and B.right == S.right:
        return '枚举结束'
    return f'枚举 `x = nums[{S.right}] = {S.x}` 作为最终的最高频元素（窗口右端点）'


CONFIG = dict(
    num=1838, title='最高频元素的频数', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='排序 + 不定长滑动窗口',
    tags=['字节30天'],
    code='''
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = s = left = 0
        for right, x in enumerate(nums):
            s += x
            while (right - left + 1) * x - s > k:
                s -= nums[left]
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().maxFrequency({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'pink'), ('x', 'x', 'orange'), 's', 'k', ('ans', 'ans', 'yellow')],
    captions={
        'nums.sort()': '排序：要变大的数就是 `x` 左边==一段连续的子数组==',
        'ans = s = left = 0': '`s` 是窗口 `[left, right]` 的元素和',
        'for right, x': _cap_for,
        's += x': '`x` 进入窗口：`s = {s}`',
        'while (right - left + 1)': _cap_while,
        's -= nums[left]': '最小的 `nums[{B.left}] = {B.nums[B.left]}` 离 x 最远，最费操作 → 移出：`s = {s}`',
        'left += 1': '`left` → {left}',
        'ans = max': '窗口长度 `{right - left + 1}` 就是 `x` 能达到的频数 → `ans = {ans}`',
        'return ans': '最大频数 =={ret}==',
    },
    cards=dict(
        one_liner='排序后枚举 x，窗口内的数都补到 x，操作次数 = 面积 − 和',
        complexity='时间 `O(n log n)`（瓶颈是排序），空间 `O(1)`',
        problem=['每次操作把某个元素 `+1`，最多 `k` 次',
                 '求操作后数组中==最高频元素的最大频数==',
                 '示例：`[1,2,4]`，`k = 5` → `3`（都变成 4）',
                 '演示：`[3,9,6,1,4]`，`k = 5` → `3`（`3,4` 补到 `6`，共 `3 + 2 = 5` 次）'],
        quote='排序后，要变大的数就是一段连续的子数组了。子数组越长，需要的操作次数越多，越无法实现；子数组越短，需要的操作次数越少，越可以实现。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `[1,4,1,2]` 都变成 3 没意义，变成 2 更省 → 最高频元素==一定等于某个 nums[i]==',
              '枚举 `x = nums[right]`，优先把离 x 近的（左边紧挨着的）变大',
              '操作次数 = 矩形 `(right − left + 1) · x` − 子数组和 `s`；大于 `k` 就移动 `left`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（忽略排序栈开销）',
                 '易错：别忘了先排序；乘积可能很大，Java/C++ 要用 long',
                 '缩窗时扔掉的是最小的数——它离 x 最远，最费操作',
                 '同类：不定长滑动窗口（越短越合法），答案在缩完窗后更新'],
    ),
)
