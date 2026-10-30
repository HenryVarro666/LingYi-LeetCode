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
    cv.text((x0 + 18, y0 + 6), '按二进制位竖着看：每一列独立，答案该位 = 这一列 1 的个数 的奇偶', 24, T['muted'], bold=True)
    for b in range(w):
        cv.text((sx + b * cw + cw / 2, top - 10), f'2^{w - 1 - b}', 18, T['dim'], anchor='mb', mono=True)
    for r, v in enumerate(nums):
        y = top + r * rh
        cv.text((x0 + 30, y + rh / 2), f'nums[{r}]={v}', 24, T['text'], anchor='lm', mono=True)
        for b in range(w):
            bit = (v >> (w - 1 - b)) & 1
            X = sx + b * cw
            cv.rect((X + 4, y + 4, X + cw - 4, y + rh - 4), fill=(T['panel2'] if bit == 0 else T['blue']), r=8, alpha=(255 if bit else 160))
            cv.text((X + cw / 2, y + rh / 2), bit, 28, T['dim'] if bit == 0 else T['bg'], anchor='mm', bold=True, mono=True)
    yc = top + n * rh + 14
    cv.line([(x0 + 30, yc - 6), (sx + w * cw, yc - 6)], T['border'], 2)
    cv.text((x0 + 30, yc + rh / 2), '1 的个数 y', 24, T['muted'], anchor='lm')
    cv.text((x0 + 30, yc + rh * 1.5), '答案各位', 24, T['green'], anchor='lm', bold=True)
    res = 0
    for b in range(w):
        cnt = sum((v >> (w - 1 - b)) & 1 for v in nums)
        bit = cnt % 2
        res = res * 2 + bit
        X = sx + b * cw
        cv.text((X + cw / 2, yc + rh / 2), cnt, 28, T['yellow'] if bit else T['muted'], anchor='mm', bold=True, mono=True)
        cv.rect((X + 4, yc + rh + 4, X + cw - 4, yc + rh * 2 - 4), fill=(T['green'] if bit else T['panel2']), r=8)
        cv.text((X + cw / 2, yc + rh * 1.5), bit, 28, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((sx + w * cw + 30, yc + rh * 1.5), f'= {res}', 34, T['green'], anchor='lm', bold=True, mono=True)
    cv.text((sx + w * cw + 30, yc + rh / 2), '奇数个 → 该位为 1', 22, T['yellow'], anchor='lm')


CONFIG = dict(
    num=2527, title='查询数组异或美丽值', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='对称性化简 · 全体异或',
    tags=['灵神题单', '位运算', '难度分 1550'],
    code='''
class Solution:
    def xorBeauty(self, nums: List[int]) -> int:
        return reduce(xor, nums)
''',
    call='Solution().xorBeauty([3, 5, 12, 9])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: '`reduce(xor, nums)` = `3 ^ 5 ^ 12 ^ 9` = ==3==' if S.get('_line') == 3 else '三元组 `(i, j, k)` 的有效值：`(nums[i] | nums[j]) & nums[k]`', size=30),
    ],
    watch=[('答案', 'reduce(xor, nums)', 'green')],
    captions={
        'def xorBeauty': '把 `nums = [3, 5, 12, 9]` 交给函数：先别枚举 `n^3` 个三元组，找对称性',
        'return reduce': '`i≠j` 成对抵消，`i=j≠k` 也成对抵消，只剩 `i=j=k`，有效值就是 `nums[i]` 自己 → 全部异或 = =={ret}==。看下方的列：每一位 1 的个数是奇数，该位就是 1',
    },
    cards=dict(
        result='每一位上 1 的个数是奇数，答案该位就是 1 → 全体异或 ==3== ✓',
        one_liner='三元组成对抵消，只剩 i=j=k：答案就是全体异或',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有效值 `(nums[i] | nums[j]) & nums[k]`，对所有 `n^3` 个下标三元组 `(i, j, k)` 求异或',
                 '求这个异或美丽值',
                 '示例：`[1,4]` → `5`；本视频用 `[3,5,12,9]` → `3`'],
        quote='如果 i≠j，那么 (i,j,k) 和 (j,i,k) 的有效值相等。由于两个相等的数的异或结果为 0，所以 i≠j 的情况对答案无贡献。',
        quote_src='—— 灵茶山艾府题解 思路一',
        idea=['`i≠j`：交换 i、j 有效值不变，成对异或为 0',
              '`i=j≠k`：`(i,i,k)` 和 `(k,k,i)` 的有效值相等，也成对抵消',
              '只剩 `i=j=k`：`(x | x) & x = x`，所以答案 = ==nums 的异或和=='],
        after=[dict(heading='思路二：拆位法（更通用）', lines=[
            '或、与按位定义，每一位互相独立 → 拆成每一位单独算',
            '某位有 `y` 个 1、`x = n−y` 个 0：有效值为 1 的有 `(n²−x²)·y = 2ny²−y³` 个',
            '`2ny²` 是偶数，只看 `y³` 的奇偶，也就是 ==y 的奇偶==，仍然是异或和',
            '若改成「有效值的和」，就用 `total · 2^i` 累加']),
        ],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先找对称性：把「三重循环」化成「一重异或」',
                 '`reduce(xor, nums)` 一行，`xor` 来自 `operator`',
                 '易错：不要真的去枚举 `n^3` 个三元组，`n=10^5` 会超时',
                 '拆位法是通用做法：改成「求和」就能直接套用'],
    ),
)
