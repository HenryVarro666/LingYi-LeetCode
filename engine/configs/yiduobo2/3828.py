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
    cv.text((sx, y), '① 极端情况：Alice 第一轮就结束 → 答案下界', 24, T['green'], bold=True)
    _row(cv, T, sx, y + 40, nums, 54, small=True,
         color=lambda i, v: 'blue' if i == 0 else None, cross=lambda i, v: i > 0)
    cv.text((sx + n * 54 + 20, y + 64), f'删 [1, n-1] → 剩 {a}', 22, T['text'], anchor='lm')
    _row(cv, T, sx, y + 104, nums, 54, small=True,
         color=lambda i, v: 'pink' if i == n - 1 else None, cross=lambda i, v: i < n - 1)
    cv.text((sx + n * 54 + 20, y + 128), f'删 [0, n-2] → 剩 {b}', 22, T['text'], anchor='lm')
    cv.text((sx, y + 176), f'→ 下界 = max({a}, {b}) = {best}', 24, T['green'], bold=True)
    # ---- 情况二：Alice 想留中间更大的数
    y = y0 + 380
    mids = [(nums[j], j) for j in range(1, n - 1)]
    if not mids:
        cv.text((sx, y), '② 只有两个数：没有“中间的数”可留', 24, T['orange'], bold=True)
        cv.text((sx, y + 44), f'Alice 删掉较小的那个，直接剩 {best}', 22, T['text'])
        return
    x, i = max(mids)
    cv.text((sx, y), f'② Alice 不结束（想留中间的 {x}）→ Bob 第二轮结束', 24, T['orange'], bold=True)
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
    author='yiduobo', technique='从极端情况入手 · 先找下界',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def finalElement(self, nums):
        return max(nums[0], nums[-1])
''',
    call=f'''
s = Solution()
[s.finalElement(a) for a in {CASES}]
''',
    expect=[2, 7, 6, 5],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('nums[0]', 'nums[0]', 'blue'), ('nums[-1]', 'nums[-1]', 'pink'),
           ('下界', 'max(nums[0], nums[-1])', 'green')],
    captions={
        'return max': lambda S, B, ret: (
            f'下界 `max({S.nums[0]}, {S.nums[-1]}) = {ret}`；'
            + ('只有两个数，Alice 删掉小的就结束' if len(S.nums) == 2 else
               'Alice 不结束的话 Bob 就结束，结果不会更好')
            + f' → 返回 =={ret}=='),
    },
    cards=dict(
        one_liner='先看极端：Alice 能直接结束游戏，下界就是答案',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['Alice、Bob 轮流删一个子数组（==不能全选==），只剩一个数时结束',
                 'Alice 想让剩下的数最大，Bob 想让它最小，Alice 先手',
                 '示例：`[1,5,2]` → `2`；`[3,7]` → `7`'],
        quote='alice是有能力直接结束游戏的，此时剩下的要么是nums[0]，要么是nums[-1]，也就是说，最终答案的下界就是max(nums[0], nums[-1])。',
        quote_src='—— yiduobo 题解原文',
        idea=['乍一看没思路 → ==从极端情况入手==：Alice 第一轮就结束',
              '下界：`max(nums[0], nums[-1])`',
              'Alice 若不结束，Bob 第二轮就能结束，留下==较小的一端=='],
        result='4 组输入的答案都是下界 `max(两端)`：`[2, 7, 6, 5]` ✓',
        before=[dict(heading='Alice 不结束会怎样？', lines=[
            'Alice 操作后，剩下数组的一端必然是 `max(nums[0], nums[-1])`',
            '另一端必须 `≥` 它，否则 Bob 直接留下较小的一端',
            '所以 Bob 的最优选择：==本轮结束==，留下 `max(nums[0], nums[-1])`',
            '结论：怎么走都拿不到比下界更好的结果']),
        ],
        summary=['时间、空间 `O(1)`',
                 '思路：先找 Alice 能保证的下界，再说明 Bob 能把结果压回下界',
                 '易错：“不能全选”意味着每轮都能删到只剩一个端点',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用反证法严格证明“大于号取不到”'],
    ),
)
