A, Bv = [2, 1, 3], [10, 2, 5, 0]


def _x(a):
    r = 0
    for v in a:
        r ^= v
    return r


def _txt(S):
    if 'm' not in S or 'n' not in S:
        return '展开 `m×n` 个数：`nums1` 的每个数各出现 `n` 次，`nums2` 的每个数各出现 `m` 次'
    return (f'`n = {S["n"]}` 是{"奇" if S["n"] % 2 else "偶"}数 → nums1 =={"保留" if S["n"] % 2 else "消去"}==；'
            f'`m = {S["m"]}` 是{"奇" if S["m"] % 2 else "偶"}数 → nums2 =={"保留" if S["m"] % 2 else "消去"}==')


CONFIG = dict(
    num=2425, title='所有数对的异或和', difficulty='Medium', category='位运算',
    author='yiduobo', technique='异或抵消 · 看长度奇偶',
    tags=['灵神题单·位运算', '难度分 1622'],
    code='''
class Solution(object):
    def xorAllNums(self, nums1, nums2):

        m = len(nums1)
        n = len(nums2)

        res = 0
        if n % 2 == 1:
            for num in nums1:
                res ^= num

        if m % 2 == 1:
            for num in nums2:
                res ^= num

        return res
''',
    call=f'Solution().xorAllNums({A}, {Bv})',
    expect=_x([a ^ b for a in A for b in Bv]),
    views=[
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='array', var='nums1', label='nums1（长度 m）', h=190, cell=96,
             color=lambda S, i, v: 'green' if S.get('_line') in (9, 10) and S.get('num') == v else None),
        dict(type='array', var='nums2', label='nums2（长度 n）', h=190, cell=96,
             color=lambda S, i, v: 'green' if S.get('_line') in (13, 14) and S.get('num') == v else None),
    ],
    watch=[('res', 'res', 'green'), 'm', 'n', 'num'],
    captions={
        'm = len(nums1)': '`m = {m}`：nums1 的长度',
        'n = len(nums2)': '`n = {n}`：nums2 的长度。每个 nums1 的数出现 `n` 次',
        'if n % 2 == 1': '`n = {n}` {"是奇数" if n % 2 else "是偶数"}：nums1 的每个数出现 {n} 次，x ^ x = 0 {"，成对消去后还剩 1 个 → 要异或" if n % 2 else "，全部消去 → 跳过"}',
        'if m % 2 == 1': '`m = {m}` {"是奇数" if m % 2 else "是偶数"}：nums2 的每个数出现 {m} 次 {"，剩 1 个 → 要异或" if m % 2 else "，全部消去 → 跳过"}',
        'res ^= num': '`res ^= {num}` → =={res}==',
    },
    cards=dict(
        one_liner='x ^ x = 0：成对出现的数自己消掉',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['`nums1`、`nums2` 两两取异或得到新数组，求新数组全部元素的异或。',
                 '示例：`[2,1,3]`、`[10,2,5,0]` → 13。'],
        quote='观察可以发现，nums1中的数每个都出现了n次，而nums2中的数则出现了m次。由于异或满足交换律，那么在计算最终结果时完全可以先将相同的数放在一起异或。',
        quote_src='—— yiduobo 题解',
        idea=['把 `m×n` 个数列出来：nums1 的数每个出现 `n` 次。',
              '异或满足交换律，同一个数放一起：偶数次 = 0，奇数次 = 它自己。',
              '所以按 `n`、`m` 的奇偶，决定要不要把对应数组异或进答案。'],
        summary=['时间 `O(m+n)`，空间 `O(1)`。',
                 '易错：`n` 奇偶决定的是 ==nums1==，`m` 才决定 nums2。'],
    ),
)
