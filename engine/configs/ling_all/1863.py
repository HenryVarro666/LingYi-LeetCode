from itertools import combinations

NUMS = [5, 1, 6]


def _subs():
    out = []
    for r in range(len(NUMS) + 1):
        for c in combinations(NUMS, r):
            x = 0
            for v in c:
                x ^= v
            out.append((c, x))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    cv.text((x0 + 18, y0 + 4), '每个比特位独立：只要这一位上有 1，贡献就是 2^(n-1) × 位权', 24, T['muted'], bold=True)
    cell, gx = 92, x0 + 230
    top = y0 + 64
    for k in range(3):
        cv.text((gx + k * cell + cell / 2, top), f'2^{2 - k}', 22, T['dim'], anchor='mm', mono=True)
    for r, v in enumerate(NUMS):
        y = top + 28 + r * 62
        cv.text((gx - 20, y + 25), f'nums[{r}] = {v}', 24, T['text'], anchor='rm', mono=True)
        for k in range(3):
            bit = (v >> (2 - k)) & 1
            cv.rect((gx + k * cell + 4, y, gx + (k + 1) * cell - 4, y + 52),
                    fill=(T['blue'] if bit else (30, 36, 46)), r=8)
            cv.text((gx + k * cell + cell / 2, y + 26), bit, 30, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    yo = top + 28 + n * 62 + 8
    cv.line([(gx, yo - 4), (gx + 3 * cell, yo - 4)], T['border'], 2)
    orv = 0
    for v in NUMS:
        orv |= v
    cv.text((gx - 20, yo + 29), f'OR = {orv}', 24, T['green'], anchor='rm', mono=True, bold=True)
    for k in range(3):
        bit = (orv >> (2 - k)) & 1
        cv.rect((gx + k * cell + 4, yo + 4, gx + (k + 1) * cell - 4, yo + 56), fill=T['green'] if bit else (30, 36, 46), r=8)
        cv.text((gx + k * cell + cell / 2, yo + 30), bit, 30, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((gx + 3 * cell + 30, yo + 30),
            f'= {orv} × 2^{n - 1} = {orv} << {n - 1} = {orv << (n - 1)}', 26, T['yellow'], anchor='lm', bold=True, mono=True)
    ys = yo + 90
    cv.text((x0 + 18, ys), '对照：8 个子集的异或和', 22, T['muted'], bold=True)
    tot = 0
    for i, (c, xv) in enumerate(_subs()):
        tot += xv
        col, row = i % 4, i // 4
        cx = x0 + 24 + col * 250
        cy = ys + 38 + row * 40
        cv.text((cx, cy), f"{list(c)} → {xv}", 22, T['text'], mono=True)
    cv.text((x0 + 24, ys + 38 + 2 * 40 + 6), f'0 + 5 + 1 + 6 + 4 + 3 + 7 + 2 = {tot}', 24, T['green'], bold=True, mono=True)


CONFIG = dict(
    num=1863, title='找出所有子集的异或总和再求和', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='拆位 / 贡献法 · or << (n-1)',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1372'],
    setup='from functools import reduce\nfrom operator import or_',
    code='''
class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        return reduce(or_, nums) << (len(nums) - 1)
''',
    call='Solution().subsetXORSum([5, 1, 6])',
    expect=28,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('n', 'len(nums)'), ('OR', lambda S: 7, 'green')],
    captions={
        'return reduce': '`reduce(or_, nums)` = 5 | 1 | 6 = ==7==（每一位上只要有一个 1，结果这一位就是 1）；再 `<< (3 - 1)` = ×4 → ==28==',
    },
    cards=dict(
        one_liner='每个出现过的比特位，贡献都是 2^(n-1) 倍：or << (n-1)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 的每个子集的异或总和（空集为 0），求这些值之和',
                 '相同元素的不同子集要多次计数',
                 '示例：`[5,1,6]` 共 8 个子集 → `28`'],
        before=[dict(heading='提示 1：只看一个比特位', lines=[
            '先想 `nums` 只有 0 和 1：子集里 1 的个数为奇数，异或和才为 1',
            '拿出一个 1，剩下 `n-1` 个数随便选或不选，共 `2^(n-1)` 种',
            '选了偶数个 1 → 放入拿出的那个 1；选了奇数个 → 不放',
            '==恰好 `2^(n-1)` 个子集异或和为 1==，与 1 的个数无关']),
            dict(heading='提示 2：推广到多个比特位', lines=[
                '各比特位互相独立，第 `i` 位有 1 就贡献 `2^i · 2^(n-1)`',
                '哪些位上有 1？==算所有元素的 OR==，它恰好是 `Σ 2^i`',
                '答案 = `or × 2^(n-1)`']),
        ],
        quote='所有元素的 OR，就是上例中的 2^0 + 2^1 + 2^3。设 nums 所有元素的 OR 为 or，nums 的所有子集的异或和的总和为 or · 2^(n-1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['“从特殊到一般”：先解 0/1 数组，再按位推广',
              '位的贡献与有几个 1 无关，只与“有没有 1”有关',
              '一行 `reduce(or_, nums) << (n - 1)` 搞定'],
        result='`7 << 2 = 28` ✓ 与 8 个子集逐一相加的结果一致',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`reduce(or_, nums)` 需要 `from functools import reduce`、`from operator import or_`（LeetCode 已预置）',
                 '易错：不是 `or × n` 也不是 `or × 2^n`，是 `2^(n-1)`',
                 '灵神还附了定理：大小为 m 的集合有 `2^(m-1)` 个奇数大小子集（双射 / 二项式两种证法）',
                 '变形：改成连续子数组、异或和的异或和等，见「灵茶八题」'],
    ),
)
