def _np(v):
    return v < 2 or any(v % d == 0 for d in range(2, v))


def _txt(S):
    if 'nums' not in S or 'i' not in S:
        return '`not_prime[x]` = ==True== 表示 x 不是质数（合数或 1）'
    nums = S['nums']
    i, j = S.get('i'), S.get('j')
    if j is None:
        v = nums[i]
        return f'从左往右：`nums[{i}] = {v}` → ' + ('==合数/1，继续右移==' if _np(v) else '==是质数，第一个质数找到==')
    v = nums[j]
    return f'从右往左：`nums[{j}] = {v}` → ' + ('==合数/1，继续左移==' if _np(v) else '==是质数，最后一个质数找到==')


CONFIG = dict(
    num=3115, title='质数的最大距离', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理筛质数 + 两端找质数',
    tags=['灵神题单·数学算法', '难度分 1294'],
    code='''
not_prime = [False] * 101
not_prime[1] = True
for i in 2, 3, 5, 7:
    for j in range(i * i, 101, i):
        not_prime[j] = True

class Solution:
    def maximumPrimeDifference(self, nums: List[int]) -> int:
        i = 0
        while not_prime[nums[i]]:
            i += 1
        j = len(nums) - 1
        while not_prime[nums[j]]:
            j -= 1
        return j - i
''',
    call='Solution().maximumPrimeDifference([4, 1, 9, 2, 8, 6, 3, 8, 9])',
    expect=3,
    skip=['for j in range(i * i', 'for i in 2, 3, 5, 7', 'not_prime[j] = True'],
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 左指针 i，粉 = 右指针 j）', cell=84, h=240,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'green' if not _np(v) else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'not_prime = [False] * 101': '先预处理 `0..100`：`not_prime[x]` 为真表示 ==x 不是质数==',
        'not_prime[1] = True': '`1` 不是质数',
        'i = 0': '从左往右找第一个质数：`i = 0`',
        'while not_prime[nums[i]]': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}`，`not_prime` = {_np(S.nums[S.i])} → ' + ('不是质数，继续' if _np(S.nums[S.i]) else '是质数，停下')),
        'i += 1': '不是质数，`i` 右移到 {i}',
        'j = len(nums) - 1': '再从右往左找最后一个质数：`j = {j}`',
        'while not_prime[nums[j]]': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]}`，`not_prime` = {_np(S.nums[S.j])} → ' + ('不是质数，继续' if _np(S.nums[S.j]) else '是质数，停下')),
        'j -= 1': '不是质数，`j` 左移到 {j}',
        'return j - i': '最远的两个质数下标 `{j}` 和 `{i}`，距离 `{j} − {i}` = =={ret}==',
    },
    cards=dict(
        one_liner='最远的两个质数 = 最左的质数 和 最右的质数',
        complexity='时间 `O(n)`（忽略预处理），空间 `O(1)`',
        problem=['给整数数组 `nums`，求两个（可以是同一个）质数下标的==最大距离==',
                 '`1 <= nums[i] <= 100`，保证至少有一个质数',
                 '示例：`[4,2,9,5,3]` → `3`；`[4,8,2,8]` → `0`'],
        quote='遍历 10 以内的质数 2,3,5,7，标记其倍数为合数。注意标记 i 的倍数时，只需从 j = i² 开始，因为小于 i² 的合数 j 一定有一个小于 i 的质因子。',
        quote_src='—— 灵茶山艾府题解（方法二：筛质数）',
        idea=['值域只有 100：先筛一遍，查表 `O(1)` 判质数',
              '距离最大 = ==从左数第一个质数、从右数第一个质数==，下标相减',
              '从两边向中间找，随机数据下很快就能碰到质数'],
        summary=['时间 `O(n)`，空间 `O(1)`（预处理 `O(U log log U)` 忽略）',
                 '易错：==1 不是质数==，要手动标记 `not_prime[1] = True`',
                 '只有一个质数时 `i == j`，答案为 0',
                 '灵神还给了两种写法：方法一每个数试除到 `isqrt(n)`；方法三把 100 以内质数压成一个位掩码 `PRIME_MASK`'],
    ),
)
