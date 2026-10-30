CONFIG = dict(
    num=976, title='三角形的最大周长', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 倒序枚举最长边',
    tags=['滑动窗口与双指针', '贪心与思维', '难度分 1341'],
    code='''
class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        for i in range(len(nums) - 1, 1, -1):
            if nums[i - 2] + nums[i - 1] > nums[i]:
                return nums[i - 2] + nums[i - 1] + nums[i]
        return 0  # 无解
''',
    call='Solution().largestPerimeter([1,2,1,10,4,7,20,3])',
    expect=21,
    views=[
        dict(type='text', fn=lambda S: (f"最长边 `nums[{S['i']}] = {S['nums'][S['i']]}`，两短边 `{S['nums'][S['i']-2]} + {S['nums'][S['i']-1]} = {S['nums'][S['i']-2]+S['nums'][S['i']-1]}`" if 'i' in S and S['i'] >= 2 else '')),
        dict(type='array', var='nums', h=300, cell=100,
             pointers={'i': 'pink'},
             color=lambda S, i, v: ('pink' if i == S['i'] else 'blue' if i in (S['i'] - 1, S['i'] - 2) else None) if 'i' in S else None),
    ],
    watch=[('i', 'i', 'pink')],
    captions={
        'nums.sort()': '先从小到大排序：`{nums}`。这样==最大周长的三条边在数组里一定相邻==',
        'for i in range': '倒着枚举最长边 `c = nums[i]`，从最大的开始',
        'if nums[i - 2]': '只需检查 `a + b > c`：`{nums[i-2]} + {nums[i-1]} = {nums[i-2]+nums[i-1]}` 对 `{nums[i]}` → {"成立" if nums[i-2]+nums[i-1] > nums[i] else "不成立，换更小的最长边"}',
        'return nums[i - 2]': '找到的第一个就是最大周长：继续枚举只会更小 → `{nums[i-2]}+{nums[i-1]}+{nums[i]}` = =={ret}==',
        'return 0': '没有任何三条边能组成三角形，返回 0',
    },
    cards=dict(
        one_liner='排序后倒序枚举最长边，只看紧挨着的两条边',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给定边长数组，选三条边组成面积不为零的三角形，求最大周长',
                 '无法组成则返回 `0`',
                 '示例：`[2,1,2]` → `5`；本视频：`[1,2,1,10,4,7,20,3]` → `21`'],
        quote='枚举 c，由于 a 和 b 越大，周长 a+b+c 就越大，且 a+b>c 越能成立，所以最大周长的 a,b,c 在排序后的数组中是相邻的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `a<=b<=c`，另外两个不等式 `a+c>b`、`b+c>a` 必然成立，只剩 `a+b>c`',
              '固定 c，a、b 取==紧挨着它的两个最大值==：既最大又最容易成立',
              '倒序枚举，第一个满足的就是答案'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错：循环到 `i=2` 为止（`range(n-1, 1, -1)`），否则 `i-2` 越界',
                 '无解必须返回 `0`',
                 '思考题：最小周长，枚举中间边 + 背向双指针；同类题 611'],
    ),
)
