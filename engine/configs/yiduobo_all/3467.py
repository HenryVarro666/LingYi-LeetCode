CONFIG = dict(
    num=3467, title='将数组按照奇偶性转化', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历数偶数个数', tags=['灵神题单'],
    code='''
class Solution(object):
    def transformArray(self, nums):
        
        even = 0
        for v in nums:
            if v % 2 == 0:
                even += 1
        
        return [0] * even + [1] * (len(nums) - even)
''',
    call='Solution().transformArray([1,5,1,4,2,7,6])',
    expect=[0, 0, 0, 1, 1, 1, 1],
    views=[
        dict(type='array', var='nums', pointers={}, label='nums（蓝 = 偶数，粉 = 奇数）', h=260,
             color=lambda S, i, v: 'pink' if v % 2 else 'blue',
             dim=lambda S, i, v: 'v' in S and False),
        dict(type='text', size=30, fn=lambda S: (f"遍历到 `{S['v']}`：偶数已有 `{S['even']}` 个" if 'v' in S and 'even' in S else '')),
    ],
    watch=[('v', 'v', 'yellow'), ('even', 'even', 'blue')],
    captions={
        'even = 0': '`even` 记录偶数的个数，先从 0 开始',
        'for v in nums': lambda S, B, r: (f'取出 `v = {S.v}`' if S.v != B.get('v') or B.get('v') is None else '遍历完毕，退出循环'),
        'if v % 2 == 0': lambda S, B, r: (f'`{S.v} % 2 == 0` 成立：偶数，会变成 0' if S.v % 2 == 0 else f'`{S.v}` 是奇数，会变成 1，不用数'),
        'even += 1': '又发现一个偶数：`even` → =={even}==',
        'return': '前面 `{even}` 个 0，后面 `{len(nums) - even}` 个 1：`{ret}`',
    },
    cards=dict(
        one_liner='替换后只剩 0 和 1，左边全是 0、右边全是 1',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['偶数换成 `0`，奇数换成 `1`，然后非递减排序',
                 '示例：`[1,5,1,4,2]` → `[0,0,1,1,1]`',
                 '本视频：`[1,5,1,4,2,7,6]` → `[0,0,0,1,1,1,1]`'],
        quote='最后得到的数组必然由左侧若干个0和右侧若干个1组成，其中0的数目为nums中偶数的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['非递减 + 只有 0/1 → ==左边一段 0，右边一段 1==',
              '0 的个数就是偶数的个数，数一遍即可',
              '剩下的都是奇数：`len(nums) - even` 个 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文只用一个计数器 `even`，奇数个数用总数减出来',
                 '无需真的替换再排序，排序结果可以直接构造'],
    ),
)
