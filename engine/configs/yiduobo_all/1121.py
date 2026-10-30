CONFIG = dict(
    num=1121, title='将数组分成几个递增序列', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='最大频次 n，长度 ÷ n',
    code='''
class Solution(object):
    def canDivideIntoSubsequences(self, nums, k):

        last = nums[0]
        cnt = 1
        n = 1
        for num in nums[1:]:
            if num == last:
                cnt += 1
            else:
                n = max(n, cnt)
                last = num
                cnt = 1
        
        n = max(n, cnt)
        return len(nums) // n >= k
''',
    call='Solution().canDivideIntoSubsequences([1,2,2,3,3,4,4], 3)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"最长的一段相同值 = `n` = =={S['n']}==（至少要拆成 n 个序列）" if 'n' in S else ''),
        dict(type='array', var='nums', h=200, label='nums（已排序，相同值连成一段）',
             color=lambda S, i, v: ('green' if v == S['last'] else None) if 'last' in S else None),
        dict(type='text', fn=lambda S: (f"可得序列长度：`{len(S['nums'])} // {S['n']}` = =={len(S['nums'])//S['n']}==，与 `k = {S['k']}` 比较" if 'n' in S and S['_line'] is not None and S.get('_done') else '')),
    ],
    watch=['last', 'cnt', ('n', 'n', 'orange'), 'k'],
    captions={
        'last = nums[0]': '`last` 记录当前这一段的值，从第一个数开始：{last}',
        'cnt = 1': '`cnt` 是当前这一段已有几个，初始 1',
        'n = 1': '`n` 是目前见过的最长一段，至少为 1',
        'if num == last': lambda S, B, r: (f'`{S.num}` 和 `last = {S.last}` 相同 → 同一段，相同值不能放进同一个序列' if S.num == S.last
                                           else f'`{S.num}` 和 `last = {S.last}` 不同 → 上一段结束了'),
        'cnt += 1': '同一段又多一个：`cnt` → {cnt}',
        'n = max(n, cnt)': '这一段出现 `{cnt}` 次，至少要 `{cnt}` 个序列来分：`n = max({B.n}, {cnt}) = {n}`',
        'last = num': '开始新的一段：`last` → {last}',
        'cnt = 1': '当前这一段已有 1 个：`cnt = 1`',
        'return': '最优分配下各序列长度最接近，最短的长度是 `{len(nums)} // {n}` = {len(nums)//n}；`>= {k}` → =={ret}==',
    },
    cards=dict(
        one_liner='相同的数必须分开，最大频次 n 就是序列数；均分后看最短长度够不够 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个非递减的整数数组 `nums` 和整数 `k`',
                 '问能否把它分成一个或多个不相交的==严格递增子序列==，且每个长度都 `>= k`',
                 '示例：`[1,2,2,3,3,4,4]`，`k = 3` → `True`（拆成 `1,2,3,4` 和 `2,3,4`）'],
        quote='相同的值不能放在同一个序列中，从而得到了拆分序列数量的下限，也就是数组中每种数出现频率的最大值，在这里将其记为n。',
        quote_src='—— yiduobo 题解原文',
        idea=['序列越少越长，所以只拆 ==n 个==（最大频次）',
              '从小到大把每种数轮流分给各序列，长度会尽量接近',
              '不用真分配：最短序列长度就是 `len(nums) // n`，与 `k` 比较'],
        summary=['时间 `O(n)`，空间 `O(1)`，一趟统计每段相同值的长度',
                 '循环结束后还要再做一次 `n = max(n, cnt)`，最后一段没有触发更新',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去类型文档字符串',
                 '数组本身有序，相同值一定连续，所以不需要哈希表'],
    ),
)
