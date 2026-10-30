CONFIG = dict(
    num=3392, title='统计符合条件长度为 3 的子数组数目', difficulty='Easy', category='模拟',
    author='yiduobo', technique='从下标 2 开始遍历第三个元素',
    tags=[],
    code='''
class Solution(object):
    def countSubarrays(self, nums):
        
        res = 0
        for index in range(2, len(nums)):
            if (nums[index] + nums[index - 2]) * 2 == nums[index - 1]:
                res += 1
                
        return res
''',
    call='Solution().countSubarrays([1,2,1,4,1,3,1])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 当前子数组，黄 = 中间数）', h=300, pointers={'index': 'pink'},
             window=('index-2', 'index'),
             color=lambda S, k, v: 'yellow' if 'index' in S and k == S['index'] - 1 else None),
        dict(type='text', fn=lambda S: f"已找到 ==res== 个符合条件的子数组：`{S['res']}`" if 'res' in S else '', size=26),
    ],
    watch=[('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计符合条件的子数组个数',
        'for index in range': lambda S, B, r: (
            f'`index = {S.index}` 当作第三个元素，子数组是 `nums[{S.index-2}..{S.index}]`' if B.get('index') != S.index or 'index' not in B
            else '下标遍历完了'),
        'if (nums[index]': lambda S, B, r: (
            f'`({S.nums[S.index]} + {S.nums[S.index-2]}) × 2 = {(S.nums[S.index]+S.nums[S.index-2])*2}`，中间数 `{S.nums[S.index-1]}` → '
            + ('==相等=='if (S.nums[S.index]+S.nums[S.index-2])*2 == S.nums[S.index-1] else '不相等，跳过')),
        'res += 1': '符合条件，`res` → {res}',
        'return res': '一共 `{res}` 个',
    },
    cards=dict(
        one_liner='下标 2 起遍历第三个元素，检查前两个位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `nums` 里数长度为 3 的子数组个数',
                 '条件：第一个数与第三个数之和==恰好是中间数的一半==',
                 '示例：`[1,2,1,4,1]` → `1`'],
        quote='直接从下标2开始向后遍历子数组中的第三个元素，对于当前遍历到的下标index，检测nums[index]与nums[index - 2]之和的两倍是否恰好等于nums[index - 1]即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['以第三个元素的下标 `index` 定位子数组，从 2 开始',
              '“和 = 中间数的一半” 等价于 “和的两倍 = 中间数”',
              '满足就 `res += 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`index` 从 2 起，保证 `index - 2` 不越界',
                 '用乘 2 代替除 2，避免小数',
                 '代码原样照搬，没有 Python 2 专有写法'],
    ),
)
