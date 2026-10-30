CONFIG = dict(
    num=3512, title='使数组和能被 K 整除的最少操作次数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='求和后对 k 取余',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums, k):
        
        return sum(nums) % k
''',
    call='Solution().minOperations([3,9,7], 5)',
    expect=4,
    views=[
        dict(type='array', var='nums', h=240, label='nums'),
        dict(type='text', size=34, fn=lambda S: f"元素之和 = `{sum(S['nums'])}`" if 'nums' in S else ''),
        dict(type='text', size=34, fn=lambda S: f"余数 `{sum(S['nums'])} % {S['k']}` = =={sum(S['nums']) % S['k']}== 次操作" if 'nums' in S else ''),
    ],
    watch=['k', ('sum(nums)', 'sum(nums)', 'cyan'), ('操作次数', 'sum(nums) % k', 'green')],
    captions={
        'return sum': '先求和得 `{sum(nums)}`，再对 `{k}` 取模：余数就是需要的操作次数 =={ret}==',
    },
    cards=dict(
        one_liner='每次操作使和对 k 的余数减 1，余数多少就操作多少次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['可以把任意 `nums[index]` 替换为 `nums[index] - 1`，次数不限',
                 '问最少几次操作能使元素之和被 `k` 整除',
                 '本视频：`nums=[3,9,7], k=5` → `4`'],
        quote='每次操作都可以使得nums的元素之和对k的余数减少1，于是可以直接计算nums元素之和，对k取模即为需要的操作次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作的是总和对 `k` 的余数，每次减 1',
              '余数减到 0 就整除了，所以次数 = 余数',
              '一行代码：`sum(nums) % k`'],
        before=[dict(heading='为什么是余数', lines=['和 `s` 写成 `q×k + r`，`0 <= r < k`', '每次操作 `s` 减 1，`r` 也跟着减 1', '`r` 减到 0 时 `s` 刚好是 k 的倍数'])],
        after=[dict(heading='三个示例对照', lines=['`[3,9,7], k=5`：和 19，余数 4', '`[4,1,3], k=4`：和 8，余数 0，无需操作', '`[3,2], k=6`：和 5，余数 5，两个数都减成 0'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '余数已经是 0 时不需要操作（示例 2）',
                 '原文为 Python 2 写法，仅有类型说明注释，代码无需修改'],
    ),
)
