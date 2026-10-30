def _fmt(S):
    if 'res' in S and 's2' in S and S.get('_line', 0) < 8:
        return f'两边各留至多 `{S["n"] // 2}` 个不同数，相加上限 `res = {S["res"]}`'
    if 'res' in S:
        return f'`res = {S["res"]}` 是上限；合并后不同数只有 `{len(S["s1"])}` 个 → 取小 =={min(len(S["s1"]), S["res"])}=='
    if 'n' in S:
        return f'每个数组只能留 `n/2 = {S["n"] // 2}` 个元素'
    return '集合 `s1`、`s2` = 各数组去重后的结果'


CONFIG = dict(
    num=3002, title='移除后集合的最多元素数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='去重 + 上限取小',
    tags=['贪心与思维', '难度分 1917'],
    code='''
class Solution(object):
    def maximumSetSize(self, nums1, nums2):

        n = len(nums1)
        s1 = set(nums1)
        s2 = set(nums2)
        res = min(len(s1), n // 2) + min(len(s2), n // 2)
        s1.update(s2)
        return min(len(s1), res)
''',
    call='Solution().maximumSetSize([1,2,1,2,3,3], [1,1,4,4,5,5])',
    expect=5,
    views=[
        dict(type='array', var='nums1', label='nums1', h=130, cell=70),
        dict(type='array', var='nums2', label='nums2', h=130, cell=70),
        dict(type='set', var='s1', label='s1（最后会并入 s2）', fmt=lambda x: str(x), h=100),
        dict(type='set', var='s2', label='s2', fmt=lambda x: str(x), h=100),
        dict(type='text', h=110, size=28, fn=_fmt),
    ],
    watch=['n', 'res', ('len(s1)', 'len(s1)', 'cyan')],
    captions={
        'n = len': '`n = {n}`：每个数组要删掉一半，只能剩下 `n // 2 = {n // 2}` 个',
        's1 = set': '`s1` 是 `nums1` 去重后的结果：`{sorted(s1)}`，`{len(s1)}` 种',
        's2 = set': '`s2` 是 `nums2` 去重后的结果：`{sorted(s2)}`，`{len(s2)}` 种',
        'res = min': '单个数组剩余不同数：既不超过 `n/2`，也不超过原有种数。`min({len(s1)}, {n // 2}) + min({len(s2)}, {n // 2})` = =={res}==，这是答案上限',
        's1.update': '两边合并：`s1` 变成并集，只剩 `{len(s1)}` 种不同的数（重复的合并了）',
        'return min': '上限 `res = {res}`，并集大小 `{len(s1)}` → 取小 = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么要取两次较小', lines=['第一次：每边最多留 `n/2` 个，且不能比自己的种数多', '第二次：两边加起来后，相同的数在集合里只算一个', '所以最终答案 = `min(并集大小, 两边上限之和)`'])],
        one_liner='每边留 n/2 种，加起来再被并集大小卡住',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个长为偶数 `n` 的数组，各移除 `n/2` 个元素',
                 '剩下的元素放进集合，求集合最多有多少个元素',
                 '示例：`[1,2,1,2]`、`[1,1,1,1]` → `2`'],
        quote='单个数组中剩余不重复元素的上限显然就是n除以2，但是单个数组中可能有很多重复的元素',
        quote_src='—— yiduobo 题解',
        idea=['单个数组：剩余不同数 ≤ `n/2`，也 ≤ 原来的不同数个数，取较小',
              '两个数组的上限相加，是答案的上限',
              '但两边合并后还有重复，所以再和合并后的不同数个数取较小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两个「取较小」缺一不可：每边 `n/2` 的限制，和合并去重的限制',
                 '`s1.update(s2)` 会改掉 `s1`，之后 `len(s1)` 是并集大小',
                 '原文代码已是 Python 3 写法，无需修改'],
    ),
)
