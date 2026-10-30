CONFIG = dict(
    num=1480, title='一维数组的动态和', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='原地递推前缀和', tags=[],
    code='''
class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]
        return nums
''',
    call='Solution().runningSum([3,1,2,10,1,4])',
    expect=[3, 4, 6, 16, 17, 21],
    views=[
        dict(type='text', fn=lambda S: (f"`nums[{S['i']}]` = `nums[{S['i']-1}]` + 原值 → =={S['nums'][S['i']]}==" if 'i' in S and S['i'] >= 1 and S['_line'] != 3 else '动态和 = 前一个位置的动态和 + 当前数'), h=70),
        dict(type='array', var='nums', label='nums（原地变成动态和）', pointers={'i': 'blue'}, cell=100, h=230,
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
    ],
    watch=[('i', 'i', 'blue')],
    captions={
        'for i in range': lambda S, B, r: ('`i` 已到末尾，循环结束' if B.get('i') == S.get('i') and 'i' in B else f"`i = {S.i}`：从下标 1 开始，`nums[0]` 本身就是动态和，不用动"),
        'nums[i] += nums[i - 1]': '`nums[{i}]` 加上前一项 `nums[{i-1}]`（已是前缀和）→ =={nums[i]}==',
        'return nums': '`nums` 已经全部变成动态和，直接返回',
    },
    cards=dict(
        one_liner='runningSum[i] = runningSum[i-1] + nums[i]，一个循环搞定',
        complexity='时间 `O(n)`，空间 `O(1)`（原地）',
        problem=['`runningSum[i] = nums[0] + … + nums[i]`，返回动态和数组',
                 '示例：`[1,2,3,4]` → `[1,3,6,10]`',
                 '本视频：`[3,1,2,10,1,4]` → `[3,4,6,16,17,21]`'],
        quote='对于 runningSum[2] = 1+2+3 的计算，不需要写个循环，而是将其拆开成 (1+2)+3，前面的 1+2 我们已经算出来了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前面的和已经算好了，==不用重新累加==，只加一个新数',
              '把递推式 `rs[i] = rs[i-1] + nums[i]` 直接写回 `nums[i]`，省掉新数组'],
        summary=['时间 `O(n)`，原地修改所以空间 `O(1)`',
                 '循环从 1 开始：`nums[0]` 不变',
                 '方法一另开 `running_sum` 数组（空间 `O(n)`），Python 还可以 `list(accumulate(nums))`',
                 '进阶：303 题区域和检索，用前缀和回答区间和'],
    ),
)
