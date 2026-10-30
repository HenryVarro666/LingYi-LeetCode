NUMS = [4, 1, 2, 1, 2]


def _draw(cv, S, B, box, T):
    """reduce 只有一步：把整条异或链和“两两抵消”画成一张静态图"""
    x0, y0, x1, y1 = box
    nums = S.get('nums') or NUMS
    pal = {4: T['green'], 1: T['pink'], 2: T['blue']}
    cv.text((x0 + 18, y0 + 4), 'reduce(xor, nums)：把所有数异或起来', 24, T['muted'], bold=True)
    n, cell, gap = len(nums), 112, 40
    total = n * cell + (n - 1) * gap
    sx = x0 + (x1 - x0 - total) / 2
    y = y0 + 52
    for k, v in enumerate(nums):
        X = sx + k * (cell + gap)
        cv.rect((X, y, X + cell, y + 84), fill=pal.get(v, T['panel2']), r=12)
        cv.text((X + cell / 2, y + 42), str(v), 42, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y + 100), f'{v:03b}', 30, T['text'], anchor='mt', mono=True)
        if k:
            cv.text((X - gap / 2, y + 42), '⊕', 34, T['muted'], anchor='mm')
    # 按位统计
    yb = y + 168
    cv.line([(sx, yb), (sx + total, yb)], T['border'], 2)
    res = 0
    for v in nums:
        res ^= v
    cv.text((sx, yb + 18), '按二进制位看：每一位上 1 的个数', 24, T['muted'])
    for b in range(2, -1, -1):
        ones = sum(v >> b & 1 for v in nums)
        X = sx + (2 - b) * 230
        cv.rect((X, yb + 58, X + 210, yb + 118), fill=T['panel2'], r=10)
        cv.text((X + 105, yb + 88), f'第{b}位：{ones} 个 → {ones % 2}', 26,
                T['yellow'] if ones % 2 else T['text'], anchor='mm', bold=True)
    yc = yb + 150
    cv.rich(sx, yc, '`4 ⊕ 1 ⊕ 2 ⊕ 1 ⊕ 2`', 900, size=30)
    cv.rich(sx, yc + 52, '= `4 ⊕ (1 ⊕ 1) ⊕ (2 ⊕ 2)`　交换律 + 结合律', 900, size=30, accent=T['orange'])
    cv.rich(sx, yc + 104, f'= `4 ⊕ 0 ⊕ 0` = =={res}==（二进制 `{res:03b}`）', 900, size=30, accent=T['orange'])


CONFIG = dict(
    num=136, title='只出现一次的数字', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='异或 · reduce',
    code='''
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)
''',
    call=f'Solution().singleNumber({NUMS})',
    expect=4,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('nums', 'nums')],
    captions={
        'return reduce': '`reduce(xor, nums)` 从第一个数开始依次异或：成对的数 `a ⊕ a = 0` ==全部抵消==，返回 =={ret}==',
    },
    cards=dict(
        one_liner='相同的数异或为 0，把所有数异或起来就只剩落单的那个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['非空数组 `nums` 中，除了某个元素只出现一次，其余每个元素都出现==两次==',
                 '找出只出现一次的元素；要求==线性时间、常量空间==',
                 '示例：`[4,1,2,1,2]` → `4`'],
        before=[dict(heading='异或 ⊕ 的三条性质', lines=[
            '`a ⊕ a = 0`：自己和自己异或，每一位都相同 → 全是 0',
            '`0 ⊕ a = a`：和 0 异或不改变它',
            '==交换律== `a⊕b = b⊕a`，==结合律== `(a⊕b)⊕c = a⊕(b⊕c)`'])],
        quote='利用异或运算 a⊕a=0 的性质，我们可以用异或来「消除」所有出现了两次的元素，最后剩下的一定是只出现一次的元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把所有元素异或：用交换律、结合律把相同的数挪到一起',
              '`4⊕1⊕2⊕1⊕2 = 4⊕(1⊕1)⊕(2⊕2) = 4⊕0⊕0 = 4`',
              '代码一行：`reduce(xor, nums)`，相当于从第一个数开始和其他数依次异或'],
        result='整条异或链只剩 `4` → 返回 `4` ✓',
        after=[dict(heading='reduce 展开：逐个异或', lines=[
            '`4 ⊕ 1 = 5`：`100 ⊕ 001 = 101`',
            '`5 ⊕ 2 = 7`：`101 ⊕ 010 = 111`',
            '`7 ⊕ 1 = 6`：`111 ⊕ 001 = 110`（第二个 1 把第 0 位消掉）',
            '`6 ⊕ 2 = 4`：`110 ⊕ 010 = 100`（第二个 2 把第 1 位消掉）'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '写成循环：`ans = 0`，`for x in nums: ans ^= x`（`0 ⊕ a = a`）',
                 '异或与顺序无关，所以重复元素不用相邻',
                 '相似题：137（其余出现三次）、260（两个数只出现一次）'],
    ),
)
