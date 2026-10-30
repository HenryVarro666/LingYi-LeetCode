def _t(S):
    if 'g' not in S:
        return '`x` 能整除 numsDivide 的所有元素 ⇔ `x` 整除它们的最大公因数 `g`'
    g = S['g']
    ns = S['nums']
    bad = sum(1 for x in ns if g % x)
    return f'`g = {g}`：nums 里能整除 g 的数（绿色）才合格，排序后第一个合格的下标 = 要删的个数'


CONFIG = dict(
    num=2344, title='使数组可以被整除的最少删除次数', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='GCD + 排序找第一个因子',
    tags=['灵神题单', '数学算法', '难度分 1641'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], numsDivide: List[int]) -> int:
        g = gcd(*numsDivide)
        nums.sort()
        return next((i for i, x in enumerate(nums) if g % x == 0), -1)
''',
    call='Solution().minOperations([2,3,2,4,3], [9,6,9,3,15])',
    expect=2,
    views=[
        dict(type='array', var='numsDivide', h=170, label='numsDivide'),
        dict(type='array', var='nums', h=190, label='nums（排序后）',
             color=lambda S, i, v: ('green' if 'g' in S and S['g'] % v == 0 else None)),
        dict(type='text', fn=_t, h=120),
    ],
    watch=['g', 'nums'],
    captions={
        'g = gcd': '`g = gcd(*numsDivide) = {g}`：numsDivide 所有元素的最大公因数。==x 能整除每个元素 ⇔ x 整除 g==',
        'nums.sort': '排序：`nums = {nums}`。最小元素最先考察，比第一个合格元素小的都得删',
        'return next': lambda S, B, r: f'从小到大找第一个满足 `g % x == 0` 的元素，它的下标 `{r}` 就是前面要删的个数' if r != -1 else '没有任何元素能整除 g → 返回 `-1`',
    },
    cards=dict(
        one_liner='能整除所有数 ⇔ 能整除它们的最大公因数',
        complexity='时间 `O(m + log U + n log n)`，空间 `O(1)`（排序不计）',
        problem=['给两个正整数数组 `nums` 和 `numsDivide`，可以从 `nums` 删任意个元素',
                 '要使 `nums` 的==最小元素==能整除 `numsDivide` 的所有元素，求最少删几个，不行返回 `-1`',
                 '示例：`[2,3,2,4,3]`，`[9,6,9,3,15]` → `2`'],
        quote='元素 x 若能整除 numsDivide 的所有元素，等价于 x 是所有 numsDivide[i] 的因子，这也等价于 x 是 numsDivide 所有元素的最大公因数 g 的因子。',
        quote_src='—— 灵茶山艾府题解（提示 1）',
        idea=['先把 numsDivide 压成一个数：最大公因数 `g`',
              '问题变成：`nums` 里哪个最小的数是 `g` 的因子',
              '排序后从小到大扫，第一个满足 `g % x == 0` 的下标，就是它前面必须删除的个数'],
        summary=['时间 `O(m + log U + n log n)`，空间 `O(1)`',
                 '`next(..., -1)`：找不到时返回默认值 `-1`',
                 '易错：不是整除 `numsDivide` 的每个数都要检查，只要整除 `g`',
                 '题解还给了不排序的写法：先找最小的合格元素 `mn`，再数比 `mn` 小的个数，`O(m + log U + n)`'],
    ),
)
