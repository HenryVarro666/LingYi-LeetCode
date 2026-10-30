A, Bv = [2, 1, 3], [10, 2, 5, 0]


def _x(a):
    r = 0
    for v in a:
        r ^= v
    return r


def _txt(S):
    n, m = len(S['nums1']), len(S['nums2'])
    return (f'`nums1` 每个数出现 `m = {m}` 次 → =={"奇数次，留下" if m % 2 else "偶数次，抵消成 0"}==；'
            f'`nums2` 每个数出现 `n = {n}` 次 → =={"奇数次，留下" if n % 2 else "偶数次，抵消成 0"}==')


CONFIG = dict(
    num=2425, title='所有数对的异或和', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='贡献法 · 奇偶性',
    tags=['灵神题单·位运算', '难度分 1622'],
    code='''
class Solution:
    def xorAllNums(self, nums1: List[int], nums2: List[int]) -> int:
        ans = 0
        if len(nums2) % 2: ans ^= reduce(xor, nums1)
        if len(nums1) % 2: ans ^= reduce(xor, nums2)
        return ans
''',
    call=f'Solution().xorAllNums({A}, {Bv})',
    expect=_x([a ^ b for a in A for b in Bv]),
    views=[
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='array', var='nums1', label='nums1（每个数要和 nums2 的每个数异或一次）', h=190, cell=96),
        dict(type='array', var='nums2', label='nums2', h=190, cell=96),
    ],
    watch=[('ans', 'ans', 'green'), ('n = len(nums1)', 'len(nums1)'), ('m = len(nums2)', 'len(nums2)')],
    captions={
        'ans = 0': '答案是一大堆数的异或和 → 用==贡献法==：看每个数出现几次',
        'if len(nums2) % 2': '`nums1[i]` 要和 `nums2` 的每个元素配对，共出现 `m = {len(nums2)}` 次；{"奇数次 → 偶数个相同的数异或为 0，剩 1 个，把 nums1 全部异或进答案" if len(nums2) % 2 else "偶数次 → x ^ x = 0 全部抵消"}：`ans = {ans}`',
        'if len(nums1) % 2': '`nums2[j]` 同理出现 `n = {len(nums1)}` 次；{"奇数次 → 留下，把 nums2 全部异或进答案" if len(nums1) % 2 else "偶数次 → 全部抵消"}：`ans = {ans}`',
    },
    cards=dict(
        one_liner='数一数每个数出现几次：偶数次抵消，奇数次留下',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组，`nums1` 和 `nums2` 中所有数对都异或一次，得到 `nums3`。',
                 '返回 `nums3` 所有数的异或和。示例：`[2,1,3]`、`[10,2,5,0]` → 13。'],
        quote='由于答案是一大堆数字的异或和，根据贡献法的思想，我们可以讨论每个数字在这一大堆数字中出现了多少次，对答案的贡献是多少。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums1[i]` 会和 `nums2` 的每个数配对，一共出现 `m` 次。',
              '一个数异或自己等于 0：`m` 为偶数贡献 0，为奇数贡献 `nums1[i]` 本身。',
              '`nums2` 的元素同理，出现 `n` 次。所以只看两个长度的奇偶。'],
        after=[dict(heading='举例：为什么偶数次会消失', lines=[
            '`nums2` 有 4 个数，所以 `nums1[0] = 2` 在 `nums3` 里出现 4 次。',
            '`2 ^ 2 ^ 2 ^ 2 = 0`，`nums1` 的三个数都消失了。',
            '`nums1` 有 3 个数，`nums2` 的每个数出现 3 次，`x ^ x ^ x = x`，全部留下。',
            '所以答案就是 `10 ^ 2 ^ 5 ^ 0 = 13`。'])],
        summary=['时间 `O(n+m)`，空间 `O(1)`。',
                 '易错：`nums1` 的出现次数由 ==nums2 的长度== 决定，别写反。',
                 '两个长度都是偶数时答案为 0。',
                 '同类：拆位 / 贡献法（位运算题单第四节）。'],
    ),
)
