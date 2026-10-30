CONFIG = dict(
    num=3282, title='到达数组末尾的最大得分', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='DP 推导 · 中继点选更大值',
    tags=['灵神题单', '贪心与思维', '难度分 1772'],
    code='''
class Solution(object):
    def findMaximumScore(self, nums):

        now = 0
        res = 0
        for index in range(1, len(nums)):
            if index == len(nums) - 1 or nums[index] > nums[now]:
                res += (index - now) * nums[now]
                now = index
        
        return res
''',
    call='Solution().findMaximumScore([2,5,3,6,1,4])',
    expect=24,
    views=[
        dict(type='text', fn=lambda S: (f"当前起跳点 `now = {S['now']}`（值 {S['nums'][S['now']]}）；累计 `res = {S['res']}`" if 'res' in S else '从下标 0 出发，只往右跳'), h=90),
        dict(type='array', var='nums', h=300, label='nums',
             pointers={'now': 'blue', 'index': 'pink'},
             color=lambda S, i, v: 'blue' if 'now' in S and i == S['now'] else ('pink' if 'index' in S and i == S['index'] else None)),
    ],
    watch=[('now', 'now', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'now = 0': '起跳点 `now = 0`，先从 0 号出发',
        'res = 0': '`res` 累计得分',
        'if index == len': '`index = {index}`：{\"是终点，必须跳过去收尾\" if index == len(nums) - 1 else \"nums[index] = %d %s nums[now] = %d\" % (nums[index], \">\" if nums[index] > nums[now] else \"<=\", nums[now]) + (\" → 更大，换它当中继点\" if nums[index] > nums[now] else \" → 不更大，继续用 now 往后\")}',
        'res += ': '从 `{now}` 跳到 `{index}`：`({index} − {now}) × {nums[now]}` → `res = {res}`',
        'now = index': '`now = {index}`：以后从这个更大的位置起跳',
        'return res': '最后一跳也跳完了，总得分 ==res = {res}==',
    },
    cards=dict(
        one_liner='对比两个中继点：较大的 nums 更优，一路跳向更大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从下标 0 跳到 `n-1`，只能往右；从 `i` 跳到 `j` 得分 `(j-i)*nums[i]`',
                 '求到达末尾的最大总得分',
                 '本视频：`[2,5,3,6,1,4]` → `24`'],
        quote='可以发现，上面两个式子可以约掉前面的所有项，只剩下最后的(i - k) * (nums[k] - nums[j])。也就是说，在这里应该选择nums较大的那个位置作为中继点进行跳跃。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到 `f[i]` 的 `O(n^2)` DP：枚举从哪个下标 `j` 跳到 `i`',
              '比较中继点 `j<k`：把 `f[k]` 看作先跳到 `j` 再补一步，差值是 `(i-k)*(nums[k]-nums[j])`',
              '所以 ==nums 更大的下标当中继点更优==：从 `now` 一直跳到下一个更大的数，最后一跳到终点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '终点 `index == len(nums) - 1` 要无条件跳，否则最后一段没算',
                 '判断用严格大于 `>`：相等的数没必要换起跳点',
                 '原文为 Python 2 风格，代码未做改动',
                 '对比灵神：灵神用矩形面积看成前缀最大值累加；这里是 DP 推导后的“跳到更大值”'],
    ),
)
