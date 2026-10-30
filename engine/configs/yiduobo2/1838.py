NUMS = [3, 9, 6, 1, 4]
K = 5


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if nums is None or 'l' not in S or 'r' not in S:
        cv.text((x0 + 18, y0 + 4), 'nums', 24, T['muted'], bold=True)
        return
    cv.text((x0 + 18, y0 + 4), 'nums（蓝框 = 变成 nums[r] 要花的操作，橙 = 目标 nums[r]）', 24, T['muted'], bold=True)
    n = len(nums)
    vmax = max(nums)
    cell = min(130, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    base, top = y1 - 90, y0 + 80
    scale = (base - top) / vmax
    l, r = S['l'], S['r']
    X = nums[r]
    yX = base - X * scale
    cv.dashed((sx + min(l, r) * cell, yX), (sx + (r + 1) * cell, yX), T['orange'], 3)
    for i, v in enumerate(nums):
        bx0, bx1 = sx + i * cell + cell * 0.18, sx + (i + 1) * cell - cell * 0.18
        inwin = l <= i <= r
        if i == r:
            fill = T['orange']
        elif inwin:
            fill = T['cyan']
        elif i > r:
            fill = (60, 66, 76)
        else:
            fill = (110, 120, 132)
        cv.rect((bx0, base - v * scale, bx1, base), fill=fill, r=5)
        if inwin and v < X:
            cv.rect((bx0, yX, bx1, base - v * scale), fill=T['water'], alpha=90)
            cv.rect((bx0, yX, bx1, base - v * scale), outline=T['water'], width=2)
            if (X - v) * scale >= 40:
                cv.text(((bx0 + bx1) / 2, base - (X + v) / 2 * scale), f'+{X - v}', 24, T['text'], anchor='mm', bold=True)
            else:
                cv.text(((bx0 + bx1) / 2, base - X * scale - 6), f'+{X - v}', 24, T['blue'], anchor='mb', bold=True)
        if inwin and v < X:
            cv.text(((bx0 + bx1) / 2, base - v * scale + 6), v, 24, T['bg'], anchor='mt', bold=True)
        else:
            cv.text(((bx0 + bx1) / 2, base - v * scale - 6), v, 26, T['dim'] if i > r else T['text'], anchor='mb', bold=True)
        cv.text(((bx0 + bx1) / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    for name, idx, c, row in (('l', l, T['green'], 0), ('r', r, T['pink'], 1 if l == r else 0)):
        X_ = sx + idx * cell + cell / 2
        cv.tri_up(X_, base + 32, 10, c)
        cv.text((X_, base + 48 + row * 26), name, 22, c, anchor='mt', bold=True)
    # 剩余预算
    kk = S.get('k', 0)
    cv.text((x1 - 24, y0 + 52), f'剩余 k = {kk}', 28, T['yellow'], anchor='ra', bold=True)


def _text(S):
    if 'r' not in S or 'l' not in S:
        return '把 `[l, r]` 都变成 `nums[r]`；剩下的操作次数记在 `k` 里'
    nums, l, r = S['nums'], S['l'], S['r']
    used = sum(nums[r] - nums[i] for i in range(l, r + 1)) if l <= r else 0
    return f'把 `[{l}, {r}]` 都变成 `{nums[r]}` 已花 `{used}` 次，还剩 `k = {S["k"]}`'


def _cap_outer(S, B, ret):
    if B.l > 0 and B.r > 0:
        return f'`l = {B.l}`，`r = {B.r}`：都没到左边界，以 `nums[{B.r}] = {B.nums[B.r]}` 为目标继续'
    return f'`l = {B.l}` 或 `r = {B.r}` 到达左边界 → 结束'


def _cap_inner(S, B, ret):
    l, r, nums, k = B.l, B.r, B.nums, B.k
    if l > 0 and nums[r] - nums[l - 1] <= k:
        d = nums[r] - nums[l - 1]
        return f'把 `nums[{l - 1}] = {nums[l - 1]}` 变成 `{nums[r]}` 要 `{d}` 次 ≤ `k = {k}` → 可以，往左扩'
    if l == 0:
        return '`l = 0`：左边没有数了'
    d = nums[r] - nums[l - 1]
    return f'把 `nums[{l - 1}] = {nums[l - 1]}` 变成 `{nums[r]}` 要 `{d}` 次 > `k = {k}` → ==不够了==，左边界停在 `{l}`'


def _cap_refund(S, B, ret):
    r, l, nums = B.r, B.l, B.nums
    if r - l == 0:
        return f'`r - l = 0`：没有可返还的操作，`k = {S.k}`'
    return (f'目标从 `{nums[r]}` 降到 `{nums[r - 1]}`：`[{l}, {r - 1}]` 这 `{r - l}` 个数各少花 `{nums[r] - nums[r - 1]}` 次'
            f' → 返还 `{(r - l) * (nums[r] - nums[r - 1])}`，`k = {S.k}`')


CONFIG = dict(
    num=1838, title='最高频元素的频数', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='排序 + 从右往左双指针（返还操作次数）',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maxFrequency(self, nums, k):
        nums = sorted(nums)
        r = len(nums) - 1
        l = r
        res = 1
        while l > 0 and r > 0:
            while l > 0 and nums[r] - nums[l - 1] <= k:
                k -= nums[r] - nums[l - 1]
                l -= 1

            res = max(res, r - l + 1)
            k += (r - l) * (nums[r] - nums[r - 1])
            r -= 1

        return res
''',
    call=f'Solution().maxFrequency({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('l', 'l', 'green'), ('r', 'r', 'pink'), ('k', 'k', 'yellow'), ('res', 'res', 'cyan')],
    skip=['l = r'],
    captions={
        'nums = sorted': '先排序：只能 `+1`，所以只有比 target 小的数才能变成 target，==优先选最接近的==',
        'r = len': '最终目标 target 设为 `nums[r]`，从最右边 `r = {r}` 开始（`l = r`）',
        'res = 1': '至少每个数自己就是频数 1',
        'while l > 0 and r > 0': _cap_outer,
        'while l > 0 and nums[r]': _cap_inner,
        'k -= nums[r]': '花掉 `{B.k - k}` 次：`k = {k}`',
        'l -= 1': '`l` → {l}',
        'res = max': '`[{l}, {r}]` 都能变成 `{nums[r]}`：频数 `{r - l + 1}` → `res = {res}`',
        'k += (r - l)': _cap_refund,
        'r -= 1': '目标换成 `nums[{r}] = {nums[r]}`；`l` ==不用回退==，从 `{l}` 接着往左找',
        'return res': '最大频数 =={ret}==',
    },
    cards=dict(
        one_liner='目标从大到小枚举，换目标时把多花的操作“退回”给 k',
        complexity='时间 `O(n log n)`（瓶颈是排序），空间 `O(n)`（`sorted` 新建列表）',
        problem=['每次操作把某个元素 `+1`，最多 `k` 次',
                 '求操作后数组中==最高频元素的最大可能频数==',
                 '示例：`[1,4,8,13]`，`k = 5` → `2`',
                 '演示：`[3,9,6,1,4]`，`k = 5` → `3`'],
        before=[dict(heading='yiduobo 的推导', lines=[
            '目标为 `nums[r]`、左边界为 `l` 时，总代价 `p = Σ (nums[r] − nums[i])`',
            '把 `[l, r-1]` 都变成 `nums[r-1]` 的代价 `p\'`，对比两式可以发现：',
            '`p\' = p − (nums[r] − nums[r-1]) × (r − l)`',
            '→ 换成目标 `r-1`，k ==补充== `(r − l) × (nums[r] − nums[r-1])`',
        ])],
        quote='朴素算法……枚举target的位置r。对于当前的r，从r - 1开始向左遍历，找到左边界l……这个朴素算法时间复杂度为O(n^2)……到了这里，很容易就想到==使用双指针==来快速求解了。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，从右往左枚举目标 `nums[r]`，`l` 尽量往左扩，`k` 记剩余操作数',
              '`r` 左移时，`[l, r-1]` 的目标变小，==返还==多花的操作',
              'k 得到补充后，`l` 可能还能继续往左扩 → `l` 永远不回退'],
        summary=['时间 `O(n log n)`：`l`、`r` 都只往左走；空间 `O(n)`',
                 '易错：返还量是 `(r − l) × (nums[r] − nums[r-1])`，不含 `r` 自己',
                 '`k` 被当成“剩余预算”直接修改，省去了窗口和 `s`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神从左往右枚举 x，用“矩形面积 − 窗口和”判断'],
    ),
)
