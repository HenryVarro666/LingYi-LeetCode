CONFIG = dict(
    num=976, title='三角形的最大周长', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='排序后从大到小枚举长边',
    tags=['滑动窗口与双指针', '贪心与思维', '难度分 1341'],
    code='''
class Solution(object):
    def largestPerimeter(self, nums):

        nums = sorted(nums)

        for i in range(len(nums) - 1, 1, -1):
            if nums[i] < nums[i - 1] + nums[i - 2]:
                return nums[i] + nums[i - 1] + nums[i - 2]
        
        return 0
''',
    call='Solution().largestPerimeter([1,2,1,10,4,7,20,3])',
    expect=21,
    views=[
        dict(type='text', fn=lambda S: (f"长边 `{S['nums'][S['i']]}` 对 两短边之和 `{S['nums'][S['i']-1]} + {S['nums'][S['i']-2]} = {S['nums'][S['i']-1]+S['nums'][S['i']-2]}`" if 'i' in S and S['i'] >= 2 else '')),
        dict(type='array', var='nums', h=300, cell=100,
             pointers={'i': 'pink'},
             color=lambda S, i, v: ('pink' if i == S['i'] else 'blue' if i in (S['i'] - 1, S['i'] - 2) else None) if 'i' in S else None),
    ],
    watch=[('i', 'i', 'pink')],
    captions={
        'nums = sorted': '先排序得到 `{nums}`，才能方便地找「仅次于长边」的两条边',
        'for i in range': '从大到小枚举长边 `nums[i]`',
        'if nums[i] <': '两短边之和 `{nums[i-1]}+{nums[i-2]} = {nums[i-1]+nums[i-2]}` 与长边 `{nums[i]}`：{"大于长边，能组成三角形" if nums[i] < nums[i-1]+nums[i-2] else "不大于，更小的短边更不可能，换下一个长边"}',
        'return nums[i] +': '这三条边是当前最大的合法组合，之后只会更小 → 直接返回 =={ret}==',
        'return 0': '枚举结束都没有合法三角形 → 返回 0',
    },
    cards=dict(
        one_liner='三角形：两短边之和大于长边，从大到小找第一组',
        complexity='时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新列表）',
        problem=['给定若干边长，选三条组成面积不为零的三角形，求最大周长',
                 '示例：`[1,2,1,10]` → `0`；本视频：`[1,2,1,10,4,7,20,3]` → `21`'],
        quote='若可以，那么当前这三条边形成的答案显然要大于之后继续枚举得到的答案，因此直接返回三边之和即可，否则剩余的短边更加不可能与长边形成三角形。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序，再从大到小枚举长边',
              '对长边，取长度仅次于它的两条边去试，试成功就是最大周长',
              '试失败：更短的边之和更小，同样不行，换下一个长边'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`range(len-1, 1, -1)` 保证 `i-2 >= 0`',
                 '无解返回 `0`',
                 '对比灵神：灵神原地 `sort`，这里用 `sorted` 复制一份'],
    ),
)
