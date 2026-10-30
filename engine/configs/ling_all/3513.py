def _txt(S):
    if 'n' not in S:
        return '先看 n，再决定能异或出多少种值'
    n = S['n']
    if n <= 2:
        return f'n = {n} ≤ 2：答案就是 =={n}=='
    L = n.bit_length()
    return f'n = `{n}` = 二进制 `{n:b}`，长度 L = {L}；能得到 `0 ~ 2^{L} − 1` 共 =={1 << L}== 个'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    nums = S['nums']
    cv.text((x0 + 18, y0 + 4), '异或值的取值范围（0 ~ 2^L−1）', 24, T['muted'], bold=True)
    if n is None or n <= 2:
        return
    L = n.bit_length()
    tot = 1 << L
    cell = min(64, (x1 - x0 - 40) / tot)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * tot) / 2
    y = y0 + 90
    for v in range(tot):
        X = sx + v * cell
        if v == 0:
            c = T['purple']
        elif v <= n:
            c = T['blue']
        else:
            c = T['green']
        cv.rect((X + 2, y, X + cell - 2, y + cell - 6), fill=c, r=6)
        cv.text((X + cell / 2, y + cell / 2 - 3), v, 22, T['bg'], anchor='mm', bold=True)
    ly = y + cell + 30
    lx = x0 + 24
    cv.text((lx, ly), '紫 = 0：选 1, 2, 3', 20, T['purple'], bold=True)
    cv.text((lx, ly + 32), '蓝 = 1 ~ n：选三个相同的数 a', 20, T['blue'], bold=True)
    cv.text((lx, ly + 64), '绿 = n+1 ~ 2^L−1：选 最高位, a^最高位^1, 1', 20, T['green'], bold=True)
    cv.text((lx, ly + 100), f'大于 {tot - 1} 的数：nums 里没有数的第 {L + 1} 位以上是 1，得不到', 20, T['muted'])


CONFIG = dict(
    num=3513, title='不同 XOR 三元组的数目 I', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='构造 · 二进制长度',
    tags=['贪心算法', '构造题', '难度分 1663'],
    code='''
class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        n = len(nums)
        return n if n <= 2 else 1 << n.bit_length()
''',
    call='Solution().uniqueXorTriplets([3,1,5,2,4])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', h=170, label='nums（排列）'),
        dict(type='custom', draw=_draw, h=300),
    ],
    watch=['n'],
    captions={
        'n = len': '`n = len(nums) = {n}`：nums 是 1~n 的排列，包含 [1, n] 所有整数',
        'return': lambda S, B, ret: (f'n = {S.n} ≤ 2 → 直接返回 `n`' if S.n <= 2 else
                                      f'n = {S.n} > 2：二进制长度 `n.bit_length() = {S.n.bit_length()}` → `1 << {S.n.bit_length()}` = =={ret}==，能得到 0 ~ {ret - 1} 的任意值'),
    },
    cards=dict(
        one_liner='i≤j≤k 不重要，就是任选三个数；n≥3 时能凑出 0 ~ 2^L−1 的全部值',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums` 是 `1~n` 的排列，选 `i ≤ j ≤ k`，求 `nums[i] ^ nums[j] ^ nums[k]` 有多少种不同取值',
                 '示例：`[3,1,2]` → `4`（0、1、2、3）',
                 '本视频：`[3,1,5,2,4]` → `8`（0 ~ 7）'],
        quote='因为异或运算满足交换律，实际上我们可以随意选。所以本质上，这题就是从 nums 中（可重复地）选三个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n ≤ 2`：鸽巢原理，三个数里有两个相等，异或为 0，剩下 1 或 2 → 答案 `n`',
              '`n ≥ 3`：能得到 `0 ~ 2^L−1` 全部，更大的得不到 → 答案 ==2^L==，`L = n.bit_length()`'],
        after=[dict(heading='为什么 n ≥ 3 全都能凑出', lines=['`0`：选 `1, 2, 3`，`1^2^3 = 0`',
                                                    '`[1, n]` 中的 `a`：选三个 `a`，`a^a^a = a`',
                                                    '`[n+1, 2^L−1]` 中的 `a`：选 `最高位, a^最高位^1, 1`',
                                                    '特例 `a = 2^(L-1)+1`：改选 `最高位, 3, 2`'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：`n ≤ 2` 要单独判断，此时凑不出 0',
                 '`a = 2^(L-1)+1` 时 `a^最高位^1 = 0`，要改选 `最高位, 3, 2`',
                 '`1 << n.bit_length()` 就是 `2^L`，不是 `2^n`'],
    ),
)
