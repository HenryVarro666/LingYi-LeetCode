CONFIG = dict(
    num=3326, title='使数组非递减的最少除法操作次数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='倒序贪心 · 试除求最小质因子',
    tags=['灵神题单', '难度分 1864'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        res = 0
        now = nums[-1]
        prime = {}
        for index in range(len(nums) - 2, -1, -1):
            if nums[index] <= now:
                now = nums[index]
            else:
                if nums[index] not in prime:
                    p = 2
                    while p * p <= nums[index]:
                        if nums[index] % p == 0:
                            break
                        p += 1
                
                    if nums[index] % p == 0:
                        prime[nums[index]] = p
                    else:
                        return -1

                if  prime[nums[index]] <= now:
                    now = prime[nums[index]]
                    res += 1
                else:
                    return -1
        
        return res
''',
    call='Solution().minOperations([3, 9, 25, 8, 49])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = index；右侧绿色已定）', pointers={'index': 'blue'}, cell=110, h=230,
             color=lambda S, i, v: ('green' if 'index' in S and i > S['index'] else None)),
        dict(type='map', var='prime', label='prime（缓存：数 → 最小质因子）', fmt=lambda k, v: f'{k}: {v}', h=130, font=34),
        dict(type='text', h=90, size=32, fn=lambda S: (f"右侧已定的最小值 `now = {S['now']}`" if 'now' in S else '')),
    ],
    watch=['index', ('now', 'now', 'cyan'), 'p', ('res', 'res', 'green')],
    captions={
        'now = nums[-1]': '最后一个数保留不动，`now = {now}` 是右边==当前的上界==',
        'for index in range': '从倒数第二个往前扫，当前数不能超过 `now`',
        'if nums[index] <= now': lambda S, B, r: (
            f"`{S.nums[S.index]} <= now = {S.now}`：不用操作，==更新 now==（保留尽量大的值）" if S.nums[S.index] <= S.now
            else f"`{S.nums[S.index]} > now = {S.now}`：太大，只能操作"),
        'now = nums[index]': '不操作：`now` 变为 `{now}`，让更左边的数有更大选择空间',
        'if nums[index] not in prime': '先查缓存里有没有它的最小质因子',
        'p = 2': '从 2 开始试除，找 `nums[index]` 的最小质因子',
        'while p * p <= nums[index]': lambda S, B, r: (f'`p = {S.p}`：`p*p <= {S.nums[S.index]}` 继续试除' if S.p * S.p <= S.nums[S.index]
                                                      else f'`p*p > {S.nums[S.index]}`：试除结束'),
        'p += 1': '`p` 不是因子，试下一个：`p` → {p}',
        'prime[nums[index]] = p': '找到最小质因子：`prime[{nums[index]}] = {p}`',
        'return -1': '==无解==：质数没法变小，或最小质因子仍大于 `now`',
        'if  prime[nums[index]] <= now': lambda S, B, r: (
            f"最小质因子 `{S.prime[S.nums[S.index]]} <= now = {S.now}` → 操作后可行" if S.prime[S.nums[S.index]] <= S.now
            else f"最小质因子 `{S.prime[S.nums[S.index]]} > now = {S.now}` → 变小也不够"),
        'now = prime[nums[index]]': '操作一次：`now` 变为 `{now}`（最小质因子）',
        'res += 1': '`res` → =={res}==',
        'return res': '一共操作 =={res}== 次',
    },
    cards=dict(
        one_liner='能不操作就不操作：这样次数少，保留的值还大',
        complexity='时间 `O(n√U)`，空间 `O(n)`',
        problem=['一次操作：把一个数除以它的==最大真因数==',
                 '求让数组非递减的最少操作次数，不能就返回 `-1`',
                 '示例：`[25,7]` → `1`；`[7,7,6]` → `-1`'],
        quote='如果从后往前看，对于每个元素能不执行操作就不应该执行操作，因为这样一来既使得操作的总数最小，又可以保留尽量大的元素值，让前面的元素有更大的选择空间。',
        quote_src='—— yiduobo 题解原文',
        idea=['除以最大真因数 = 合数变成它的==最小质因子==，质数无法操作',
              '原文给了 DP（f/g 表示操作与否）和贪心两种，本视频演示贪心',
              '倒着扫，用 `now` 记右侧上界；用试除法求最小质因子并缓存'],
        summary=['时间 `O(n√U)`（每个数试除到根号），空间 `O(n)`',
                 '与灵神的筛法不同：这里按需试除，并用字典 `prime` 缓存',
                 '质数试除到 `p*p > x` 仍无因子 → 无法变小 → 直接返回 `-1`',
                 '原文还介绍了 DP（f[i]/g[i]）解法，视频只演示贪心'],
    ),
)
