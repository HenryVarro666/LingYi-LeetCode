CONFIG = dict(
    num=2206, title='将数组划分成相等数对', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 奇偶判断',
    tags=[],
    code='''
class Solution(object):
    def divideArray(self, nums):

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        for cnt in num_dict.values():
            if cnt % 2 == 1:
                return False

        return True
''',
    call='Solution().divideArray([3,2,3,2,2,2,5,5])',
    expect=True,
    views=[
        dict(type='array', var='nums', pointers={}, h=150,
             color=lambda S, i, v: 'yellow' if 'num' in S and S['_line'] <= 7 and v == S['num'] else None),
        dict(type='map', var='num_dict', h=220, label='num_dict：数字 → 出现次数'),
        dict(type='text', h=60, fn=lambda S: (f"次数 `{S['cnt']}` 是 =={'奇数' if S['cnt'] % 2 else '偶数'}==" if 'cnt' in S else '')),
    ],
    watch=['num', 'cnt'],
    captions={
        'num_dict = {}': '`num_dict` 统计每种数出现的次数',
        'for num in nums': '取出 `num = {num}`',
        'num_dict[num] =': '`{num}` 的次数 +1 → =={num_dict[num]}==',
        'for cnt in num_dict.values()': '检查一种数的出现次数 `cnt = {cnt}`',
        'if cnt % 2 == 1': '`{cnt} % 2 = {cnt % 2}` → {"奇数：多出一个配不上对 → 直接返回 False" if cnt % 2 else "偶数：能两两配对，继续看下一种"}',
        'return False': '有一种数出现奇数次 → 不能划分',
        'return True': '每种数的次数都是偶数 → ==可以划分==',
    },
    cards=dict(
        one_liner='每种数出现偶数次，才能两两配成相等数对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 有 `2n` 个数，要分成 `n` 对，每对里两个数相等',
                 '能划分返回 `true`，否则 `false`',
                 '示例：`[3,2,3,2,2,2]` → `true`；本视频用 `[3,2,3,2,2,2,5,5]`'],
        quote='当每种数出现的次数都为偶数次时，就可以完成划分，否则就不能。',
        quote_src='—— yiduobo 题解原文',
        idea=['相等的数才能成对，所以每种数自己内部配对',
              '某种数出现奇数次，必然多出一个没法配',
              '一趟遍历计数，再检查每个次数是否为偶数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '提示里数值 ≤ 500，也可以用长 501 的数组计数',
                 '易错：不能只看总个数是偶数，必须每种数都是偶数次'],
    ),
)
