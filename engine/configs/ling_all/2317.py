def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    w = max(v.bit_length() for v in nums)
    n = len(nums)
    cw = 78
    rh = 62
    lw = 150
    sx = x0 + 30 + lw
    top = y0 + 92
    cv.text((x0 + 18, y0 + 6), '每一列：只要有 1，就留下一个 1（绿），其余改成 0（灰）→ 该列异或恰为 1', 24, T['muted'], bold=True)
    for b in range(w):
        cv.text((sx + b * cw + cw / 2, top - 10), f'2^{w - 1 - b}', 18, T['dim'], anchor='mb', mono=True)
    kept = {}
    for b in range(w):
        for r, v in enumerate(nums):
            if (v >> (w - 1 - b)) & 1:
                kept[b] = r
                break
    for r, v in enumerate(nums):
        y = top + r * rh
        cv.text((x0 + 30, y + rh / 2), f'nums[{r}]={v}', 24, T['text'], anchor='lm', mono=True)
        for b in range(w):
            bit = (v >> (w - 1 - b)) & 1
            X = sx + b * cw
            if bit and kept[b] == r:
                fill, tc = T['green'], T['bg']
            elif bit:
                fill, tc = T['panel2'], T['red']
            else:
                fill, tc = T['panel2'], T['dim']
            cv.rect((X + 4, y + 4, X + cw - 4, y + rh - 4), fill=fill, r=8, alpha=(255 if bit and kept[b] == r else 170))
            cv.text((X + cw / 2, y + rh / 2), bit, 28, tc, anchor='mm', bold=True, mono=True)
    yc = top + n * rh + 14
    cv.line([(x0 + 30, yc - 6), (sx + w * cw, yc - 6)], T['border'], 2)
    cv.text((x0 + 30, yc + rh / 2), '该列有 1 吗', 24, T['muted'], anchor='lm')
    cv.text((x0 + 30, yc + rh * 1.5), '最大异或和', 24, T['green'], anchor='lm', bold=True)
    res = 0
    for b in range(w):
        has = b in kept
        res = res * 2 + (1 if has else 0)
        X = sx + b * cw
        cv.text((X + cw / 2, yc + rh / 2), '有' if has else '无', 24, T['yellow'] if has else T['muted'], anchor='mm', bold=True)
        cv.rect((X + 4, yc + rh + 4, X + cw - 4, yc + rh * 2 - 4), fill=(T['green'] if has else T['panel2']), r=8)
        cv.text((X + cw / 2, yc + rh * 1.5), 1 if has else 0, 28, T['bg'] if has else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((sx + w * cw + 30, yc + rh * 1.5), f'= {res}', 34, T['green'], anchor='lm', bold=True, mono=True)
    cv.text((sx + w * cw + 30, yc + rh / 2), '= 所有数按位或', 22, T['yellow'], anchor='lm')


CONFIG = dict(
    num=2317, title='操作后的最大异或和', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='逐位构造 · 全体按位或',
    tags=['灵神题单', '位运算', '难度分 1679'],
    setup='from operator import or_',
    code='''
class Solution:
    def maximumXOR(self, nums: List[int]) -> int:
        return reduce(or_, nums)
''',
    call='Solution().maximumXOR([3, 2, 4, 6])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: '`reduce(or_, nums)` = `3 | 2 | 4 | 6` = ==7==' if S.get('_line') == 3 else '操作 `nums[i] & (nums[i] ^ x)`：只能把某些 1 改成 0，不能把 0 改成 1', size=30),
    ],
    watch=[('答案', 'reduce(or_, nums)', 'green')],
    captions={
        'def maximumXOR': '先别管操作长什么样，看它能做到什么：只能把 nums[i] 的某些位由 1 改成 0',
        'return reduce': '某一位只要有一个数是 1，就把其余的 1 改成 0，只留一个 → 这一位异或为 1。所以答案 = 所有数按位或 = =={ret}==',
    },
    cards=dict(
        result='每一位只要出现过 1 就能保留一个 → 按位或 ==7== ✓',
        one_liner='操作只能把 1 改成 0：每一位只要出现过 1，就能凑出 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：选非负整数 `x` 和下标 `i`，令 `nums[i] = nums[i] AND (nums[i] XOR x)`',
                 '可以操作任意次，求 `nums` 所有元素的最大逐位异或和',
                 '示例：`[3,2,4,6]` → `7`'],
        quote='nums[i] 逐位与任意非负整数，相当于把 nums[i] 的某些比特位的值，由 1 修改为 0，但是不能由 0 修改为 1。',
        quote_src='—— 灵茶山艾府题解 提示 2',
        idea=['提示 1：`nums[i]` 异或任意 `x` = 变成任意数；再与原值相与 = ==只能把 1 擦成 0==',
              '提示 3：某位有奇数个 1，异或为 1；有至少一个 1，就能只留一个 → ==异或也是 1==',
              '提示 4：「哪些位上有 1」就是按位或，同时也是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '关键是读懂操作的含义：`x & (x ^ y)` 只会擦掉 1',
                 '每一位独立：有 1 就能保证该位为 1，答案已经最大',
                 '`or_` 来自 `operator`，已在 setup 里导入',
                 '例：`[3,2,4,6]` 有 2^2、2^1、2^0 三列都出现过 1，所以答案是 `111` = 7',
                 '同类题：位运算里的「拆位」思想'],
    ),
)
