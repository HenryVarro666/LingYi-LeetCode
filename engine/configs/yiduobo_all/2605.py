CONFIG = dict(
    num=2605, title='从两个数字数组里生成最小数字', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='枚举一位数 · 拼接最小值',
    tags=[],
    code='''
class Solution(object):
    def minNumber(self, nums1, nums2):

        for v in range(1, 10):
            if v in nums1 and v in nums2:
                return v
        
        mi1 = min(nums1)
        mi2 = min(nums2)
        return min(mi1, mi2) * 10 + max(mi1, mi2)
''',
    call='Solution().minNumber([4, 1, 3], [5, 7])',
    expect=15,
    views=[
        dict(type='array', var='nums1', label='nums1', h=150,
             color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] else ('green' if 'mi1' in S and v == S['mi1'] else None)),
        dict(type='array', var='nums2', label='nums2', h=150,
             color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] else ('green' if 'mi2' in S and v == S['mi2'] else None)),
        dict(type='text', fn=lambda S: (f"枚举到 `v = {S['v']}`：nums1 里{'有' if S['v'] in S['nums1'] else '没有'}，nums2 里{'有' if S['v'] in S['nums2'] else '没有'}" if 'v' in S and 'mi1' not in S else ('1 到 9 都不是公共数字，改拼两位数' if 'mi1' in S else '')), size=32),
    ],
    watch=['v', 'mi1', 'mi2'],
    captions={
        'for v in range': lambda S, B, r: ('`1` 到 `9` 都枚举完了，没有公共数字 → 往下拼两位数' if getattr(B, 'v', None) == 9 else f'从小到大枚举一位数 `v = {S.v}`'),
        'if v in nums1': lambda S, B, r: (f'`{S.v}` 在 nums1 里：{S.v in S.nums1}，在 nums2 里：{S.v in S.nums2}' + (' → ==两边都有，一位数就够了==' if S.v in S.nums1 and S.v in S.nums2 else ' → 不是公共数字，枚举下一个')),
        'mi1 = min': '没有公共数字：取 nums1 的最小值 `mi1 = {mi1}` 作为一个数位',
        'mi2 = min': '取 nums2 的最小值 `mi2 = {mi2}`',
        'return min(mi1': '较小的放十位、较大的放个位：`{min(mi1, mi2)}` × 10 + `{max(mi1, mi2)}` = =={ret}==',
    },
    cards=dict(
        one_liner='先找一位数公共数字，找不到就拼两个最小值',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组，元素是 1 到 9 的互不相同数字',
                 '求最小的数，使两个数组都至少含它的某个数位',
                 '示例：`nums1=[4,1,3], nums2=[5,7]` → `15`'],
        quote='首先从1到9遍历所有的1位数，若当前遍历到的数同时出现在两个数组中，那么直接返回这个数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 1 到 9 依次枚举：第一个同时出现在两数组的就是最小的公共数字',
              '一个都没有：各取数组最小值 `mi1`、`mi2`',
              '较小的作十位、较大的作个位，拼出两位数'],
        summary=['时间 `O(n+m)`：枚举 9 个数，每次在长度 ≤ 9 的数组里找',
                 '易错点：不能先拼两位数，一位数公共数字永远更小',
                 '原文为 Python 2 风格，无需改动，直接运行',
                 '对比灵神：灵神用集合求交，这里直接枚举 1 到 9'],
    ),
)
