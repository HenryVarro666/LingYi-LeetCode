def _fmt(S):
    if 'c2' in S:
        return f'`c1 + c2 = {S["c1"]} + {S["c2"]} = {S["c1"] + S["c2"]}`（各取一半的上限） 与 `|set1 ∪ set2| = {len(S["set1"] | S["set2"])}`（并集大小）取小 → =={min(len(S["set1"] | S["set2"]), S["c1"] + S["c2"])}=='
    if 'c1' in S:
        return f'nums1 最多留 `c1 = {S["c1"]}` 个不同数；nums2 还没算'
    if 'n' in S:
        return f'每个数组只能留 `n/2 = {S["n"] // 2}` 个元素，所以不同数最多 `n/2` 种'
    return '集合 = 去重：每种数最多留一个'


CONFIG = dict(
    num=3002, title='移除后集合的最多元素数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='集合 + 取小',
    tags=['贪心与思维', '难度分 1917'],
    code='''
class Solution:
    def maximumSetSize(self, nums1: List[int], nums2: List[int]) -> int:
        set1 = set(nums1)
        set2 = set(nums2)
        n = len(nums1)
        c1 = min(len(set1), n // 2)
        c2 = min(len(set2), n // 2)
        return min(len(set1 | set2), c1 + c2)
''',
    call='Solution().maximumSetSize([1,2,3,4,5,6], [2,3,2,3,2,3])',
    expect=5,
    views=[
        dict(type='array', var='nums1', label='nums1（留一半）', h=130, cell=70),
        dict(type='array', var='nums2', label='nums2（留一半）', h=130, cell=70),
        dict(type='set', var='set1', label='set1 = set(nums1)', fmt=lambda x: str(x), h=100),
        dict(type='set', var='set2', label='set2 = set(nums2)', fmt=lambda x: str(x), h=100),
        dict(type='text', h=110, size=28, fn=_fmt),
    ],
    watch=['n', 'c1', 'c2'],
    captions={
        'set1 = set': '`nums1` 去重：`set1 = {sorted(set1)}`，有 `{len(set1)}` 种不同的数',
        'set2 = set': '`nums2` 去重：`set2 = {sorted(set2)}`，有 `{len(set2)}` 种不同的数',
        'n = len': '`n = {n}`：每个数组要移除 `n/2 = {n // 2}` 个，只剩 `n/2` 个',
        'c1 = min': 'nums1 最多留 `min(不同数 {len(set1)}, n/2 = {n // 2})` = =={c1}== 个不同的数',
        'c2 = min': 'nums2 最多留 `min(不同数 {len(set2)}, n/2 = {n // 2})` = =={c2}== 个不同的数',
        'return min': '两部分没交集时是 `c1 + c2 = {c1 + c2}`；有交集就只能是并集大小 `{len(set1 | set2)}`，取小 = =={ret}==',
    },
    cards=dict(
        one_liner='各留一半、尽量不同；答案受「并集大小」封顶',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个长为偶数 `n` 的数组，各移除 `n/2` 个元素',
                 '把剩下的元素放进集合 `s`，求 `s` 最多有多少个元素',
                 '示例：`[1,2,3,4,5,6]` 和 `[2,3,2,3,2,3]` → `5`'],
        quote='从 nums1 中选择不超过 n/2 个元素，并让这些元素尽量与 nums2 没有交集。这可以选 c1 = min(n1, n/2) 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换个角度：不是「移除」，而是「各选 `n/2` 个留下」',
              '每个数组最多选 `min(不同数个数, n/2)` 个：`c1`、`c2`',
              '两部分无交集答案是 `c1 + c2`；有交集则不超过并集大小，两者取小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '灵神还给了「从移除角度」和「c1 + c2 + common」两种写法，本题选最简洁的一种',
                 '易错点：不能忘记并集上限，也不能忘记每边 `n/2` 的上限',
                 '核心：把「移除」转成「选择」，再用集合去重'],
    ),
)
