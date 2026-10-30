CASES = [[1, 5, 2], [3, 7], [4, 9, 1, 6], [5, 1, 8, 2, 3]]


def _row(cv, T, x, y, vals, cell, color=None, cross=None, small=False):
    for i, v in enumerate(vals):
        X = x + i * cell
        c = color(i, v) if color else None
        crossed = cross and cross(i, v)
        fill = T[c] if c else T['panel2']
        if crossed:
            fill = (40, 45, 53)
        cv.rect((X + 3, y, X + cell - 3, y + cell - 6), fill=fill, r=8, outline=T['border'], width=1)
        cv.text((X + cell / 2, y + (cell - 6) / 2), v, 24 if small else 30,
                T['dim'] if crossed else (T['bg'] if c else T['text']), anchor='mm', bold=True, mono=True)
        if crossed:
            cv.line([(X + 8, y + 6), (X + cell - 8, y + cell - 12)], T['red'], 3)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        cv.text((x0 + 18, y0 + 4), '依次演示 4 组输入', 22, T['muted'], bold=True)
        return
    n = len(nums)
    a, b = nums[0], nums[-1]
    best = max(a, b)
    k = next((j for j in range(len(CASES)) if CASES[j] == list(nums)), 0)
    cv.text((x0 + 18, y0 + 4), f'第 {k + 1} 组：nums（蓝 = nums[0]，粉 = nums[-1]）', 22, T['muted'], bold=True)
    sx = x0 + 40
    _row(cv, T, sx, y0 + 44, nums, 76,
         color=lambda i, v: 'blue' if i == 0 else ('pink' if i == n - 1 else None))
    # ---- 情况一：Alice 第一轮直接结束
    y = y0 + 150
    cv.text((sx, y), '① Alice 第一轮就结束游戏', 24, T['green'], bold=True)
    _row(cv, T, sx, y + 40, nums, 54, small=True,
         color=lambda i, v: 'blue' if i == 0 else None, cross=lambda i, v: i > 0)
    cv.text((sx + n * 54 + 20, y + 64), f'删 [1, n-1] → 剩 {a}', 22, T['text'], anchor='lm')
    _row(cv, T, sx, y + 104, nums, 54, small=True,
         color=lambda i, v: 'pink' if i == n - 1 else None, cross=lambda i, v: i < n - 1)
    cv.text((sx + n * 54 + 20, y + 128), f'删 [0, n-2] → 剩 {b}', 22, T['text'], anchor='lm')
    cv.text((sx, y + 176), f'→ Alice 至少能拿到 max({a}, {b}) = {best}', 24, T['green'], bold=True)
    # ---- 情况二：Alice 想留中间更大的数
    y = y0 + 380
    mids = [(nums[j], j) for j in range(1, n - 1)]
    if not mids:
        cv.text((sx, y), '② 只有两个数：没有“中间的数”可留', 24, T['orange'], bold=True)
        cv.text((sx, y + 44), f'Alice 删掉较小的那个，直接剩 {best}', 22, T['text'])
        return
    x, i = max(mids)
    cv.text((sx, y), f'② Alice 想留中间的 {x}？只能删它一侧的一段', 24, T['orange'], bold=True)
    left_part = i <= n - 1 - i
    # Alice 删掉 x 左边（或右边）的一段 → 另一端还在
    keep = list(range(i, n)) if left_part else list(range(0, i + 1))
    _row(cv, T, sx, y + 40, nums, 54, small=True,
         color=lambda j, v: 'orange' if j == i else ('pink' if j == n - 1 and left_part else
                                                     ('blue' if j == 0 and not left_part else None)),
         cross=lambda j, v: j not in keep)
    end_v = b if left_part else a
    cv.text((sx + n * 54 + 20, y + 64), f'Alice 删{"左" if left_part else "右"}侧 → {"右" if left_part else "左"}端 {end_v} 还在',
            22, T['text'], anchor='lm')
    _row(cv, T, sx, y + 104, nums, 54, small=True,
         color=lambda j, v: ('pink' if j == n - 1 else None) if left_part else ('blue' if j == 0 else None),
         cross=lambda j, v: j != (n - 1 if left_part else 0))
    cv.text((sx + n * 54 + 20, y + 128), f'Bob 立刻结束 → 剩 {end_v} ≤ {best}', 22, T['red'], anchor='lm')


CONFIG = dict(
    num=3828, title='删除子数组后的最终元素', difficulty='Medium', category='数学',
    author='灵茶山艾府', technique='脑筋急转弯 · 反证法',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def finalElement(self, nums: List[int]) -> int:
        return max(nums[0], nums[-1])
''',
    call=f'''
s = Solution()
[s.finalElement(a) for a in {CASES}]
''',
    expect=[2, 7, 6, 5],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('nums[0]', 'nums[0]', 'blue'), ('nums[-1]', 'nums[-1]', 'pink')],
    captions={
        'return max': lambda S, B, ret: (
            f'`nums = {S.nums}`：Alice 一步结束能拿 `max({S.nums[0]}, {S.nums[-1]})`，'
            + ('只有两个数，没得选' if len(S.nums) == 2 else
               f'想留中间的 `{max(S.nums[1:-1])}` 会被 Bob 截胡')
            + f' → 返回 =={ret}=='),
    },
    cards=dict(
        one_liner='Alice 第一回合就结束游戏：答案是两端的较大值',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['Alice、Bob 轮流删一个子数组（不能删光），只剩一个数时结束',
                 'Alice 想让剩下的数==最大==，Bob 想让它==最小==，Alice 先手',
                 '示例：`[1,5,2]` → `2`；`[3,7]` → `7`'],
        quote='假设答案严格大于 max(nums[0], nums[n−1])……Bob 可以删除其他数，最终剩下 nums[0] 或 nums[n−1]。矛盾。',
        quote_src='—— 灵茶山艾府题解（反证法）',
        idea=['Alice 删 `[1,n−1]` 或 `[0,n−2]` → 答案 ==≥ max(两端)==',
              '反证：若最后剩中间的 `x` 更大，Alice 第一轮只能删 `x` 一侧',
              '另一端还在 → Bob 第二轮直接留下它，==矛盾== → 答案就是 `max(两端)`'],
        result='4 组输入都等于两端较大值：`[2, 7, 6, 5]` ✓',
        before=[dict(heading='反证法的关键', lines=[
            '设最终剩下 `x = nums[i]` 且 `x > max(nums[0], nums[n−1])`',
            '那么 `x` 不在两端：`1 ≤ i ≤ n−2`',
            'Alice 不能删 `x`，删完后==至少剩下一个端点==，游戏也没结束',
            'Bob 只要删掉端点以外的数，就能让结果 `≤ max(两端)`']),
        ],
        summary=['时间、空间都是 `O(1)`：只看两端',
                 '下界：Alice 一步结束；上界：反证法说明拿不到更大的',
                 '易错：别被“博弈”吓到去写 DP / 区间 DP',
                 '同类：灵神题单「脑筋急转弯」「博弈论」'],
    ),
)
