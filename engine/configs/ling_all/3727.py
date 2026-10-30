CONFIG = dict(
    num=3727, title='最大交替平方和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='平方后排序 + 小的减、大的加',
    tags=['灵神题单', '难度分 1455'],
    code='''
class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        nums = sorted(x * x for x in nums)  # 原地写法见另一份代码

        m = len(nums) // 2
        # 交替和：减去小的，加上大的
        return sum(nums[m:]) - sum(nums[:m])
''',
    call='Solution().maxAlternatingSum([1,-1,2,-2,3,-3,4])',
    expect=32,
    views=[
        dict(type='text', fn=lambda S: (f"前 `m = {S['m']}` 个小的 ==减去==，后 `{len(S['nums'])-S['m']}` 个大的 ==加上==" if 'm' in S else '先把每个数平方，再排序')),
        dict(type='array', var='nums', h=300, label='nums（平方后升序）',
             color=lambda S, i, v: ('pink' if i < S['m'] else 'green') if 'm' in S and 'nums' in S and len(S['nums']) == 7 else None),
    ],
    watch=['m', ('减去的和', lambda S: sum(S['nums'][:S['m']]) if 'm' in S else 0, 'pink'),
           ('加上的和', lambda S: sum(S['nums'][S['m']:]) if 'm' in S else 0, 'green')],
    captions={
        'nums = sorted': '==每项先平方再升序排序==：符号不影响平方，只看绝对值大小。`nums = {nums}`',
        'm = len': '奇数项（被减）有 `n // 2 = {m}` 个，其余 `{len(nums) - m}` 个是偶数项（被加）',
        'return sum': '贪心：==前 {m} 小的当被减项，其余大的当加项==。`{sum(nums[m:])} - {sum(nums[:m])}` = =={ret}==',
    },
    cards=dict(
        one_liner='平方后排序：最小的一半减，最大的一半加',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums` 可以任意重排，交替得分 `arr[0]² - arr[1]² + arr[2]² - ...`',
                 '求重排后能得到的最大交替得分',
                 '示例：`[1,-1,2,-2,3,-3]` → `16`；本视频：`[1,-1,2,-2,3,-3,4]` → `32`'],
        quote='把 nums 每一项平方，然后从小到大排序。设 m = floor(n/2)。贪心地，把前 m 小作为奇数项（减去），后 n-m 大作为偶数项（加上），这样算出来的交替和是最大的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['得分只与每个数的平方有关，先把所有数平方',
              '加号位有 `n - m` 个，减号位有 `m` 个（`m = n // 2`）',
              '大的放加号位、小的放减号位，总和最大'],
        summary=['时间 `O(n log n)`，瓶颈在排序；原地写法空间 `O(1)`',
                 '易错：`n` 为奇数时加号位比减号位多一个，所以 `m = n // 2` 而不是 `(n+1)//2`',
                 '快速选择找第 m 小可以做到 `O(n)`',
                 '同类：贪心 §1.1 从最小/最大开始贪心'],
    ),
)
