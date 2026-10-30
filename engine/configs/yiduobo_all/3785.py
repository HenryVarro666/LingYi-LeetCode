CONFIG = dict(
    num=3785, title='避免禁用值的最小交换次数', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='鸽笼判无解 · 非法位置计数',
    tags=['灵神题单', '难度分 2052'],
    code='''
class Solution(object):
    def minSwaps(self, nums, forbidden):
        
        bad = {}
        tot = {}
        forbid = {}

        for v, f in zip(nums, forbidden):
            tot[v] = tot.get(v, 0) + 1
            forbid[f] = forbid.get(f, 0) + 1
            if v == f:
                bad[v] = bad.get(v, 0) + 1
        
        for v in tot:
            if tot[v] + forbid.get(v, 0) > len(nums):
                return -1
        
        if not bad:
            return 0
        
        return max(max(bad.values()), (sum(bad.values()) + 1) // 2)
''',
    call='Solution().minSwaps([4,6,6,5], [4,6,5,5])',
    expect=2,
    views=[
        dict(type='grid', var=lambda S: [S['nums'], S['forbidden']], label='nums 与 forbidden（红 = 非法位置）', h=190,
             rows=['nums', 'forb'], cols=lambda S: list(range(len(S['nums']))),
             color=lambda S, i, j, v: 'red' if S['nums'][j] == S['forbidden'][j] else None),
        dict(type='map', var='tot', label='tot：v 在 nums 里的次数', h=120),
        dict(type='map', var='forbid', label='forbid：v 在 forbidden 里的次数', h=120),
        dict(type='map', var='bad', label='bad：v 处于非法位置的次数', h=120),
    ],
    watch=['v', 'f'],
    captions={
        'bad = {}': '`bad`：每种数在非法位置（`nums[i] == forbidden[i]`）上的次数',
        'tot = {}': '`tot[v]`：`v` 在 nums 里出现几次',
        'forbid = {}': '`forbid[v]`：`v` 在 forbidden 里出现几次',
        'for v, f in zip': lambda S, B, r: ('四列都看完了：`tot`、`forbid`、`bad` 统计完毕' if B.get('v') == S.v and B.get('f') == S.f else f'看下一列：`nums = {S.v}`，`forbidden = {S.f}`'),
        'tot[v] =': '`tot[{v}]` = {tot[v]}',
        'forbid[f] =': '`forbid[{f}]` = {forbid[f]}',
        'if v == f': lambda S, B, r: (f'`{S.v} == {S.f}`：这一列是非法位置' if S.v == S.f else f'`{S.v} != {S.f}`：这一列已经合法'),
        'bad[v] =': '`bad[{v}]` = {bad[v]}：记下一个非法位置',
        'for v in tot': lambda S, B, r: ('每种数都检查过，没有无解的数' if B.get('v') == S.v else f'检查每种数能不能被安置：`v = {S.v}`'),
        'if tot[v]': lambda S, B, r: (f'`tot[{S.v}] + forbid[{S.v}] = {S.tot[S.v] + S.forbid.get(S.v, 0)}` > n：鸽笼原理，无法安置 → -1'
                                      if S.tot[S.v] + S.forbid.get(S.v, 0) > len(S.nums) else
                                      f'`tot[{S.v}] + forbid[{S.v}] = {S.tot[S.v] + S.forbid.get(S.v, 0)}` <= n = {len(S.nums)}：{S.v} 可以安置'),
        'if not bad': '`bad` 非空：有非法位置，需要交换',
        'return max': '`max({max(bad.values())}, ({sum(bad.values())}+1)//2)` = =={ret}==：取「最大值」与「成对次数」中较大者',
    },
    cards=dict(
        one_liner='非法位置两两互换最省，最多的数配不完就按它算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个等长数组 `nums`、`forbidden`，每次交换 `nums` 里两个下标的值',
                 '要让每个 `nums[i]` 都不等于 `forbidden[i]`，求最少交换次数，无解返回 -1',
                 '本视频：`[4,6,6,5]`, `[4,6,5,5]` → `2`'],
        quote='对于任意元素，只要其在nums中出现的次数小于等于forbidden中不等于该元素的下标的数量，那么就一定有办法可以安置这种元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['先判无解：`tot[v] + forbid[v] > n` 时由鸽笼原理必无解',
              '换位按交换环路看：`m` 个元素成 `k` 个环要 `m - k` 次，环越多越好',
              '最理想是两两成环：交换次数 `ceil(总数/2)`',
              '某个 v 的非法位置多于其余之和：多出的 v 去和合法位置的数换，次数为 `max(bad)`'],
        after=[dict(heading='为什么 max', lines=['`bad` 中最大值不超过总数的一半：可两两配对，次数 `ceil(sum/2)`', '`bad` 中最大值超过一半：多出的必须和合法位置的数换', '无解检查已保证合法位置足够，所以答案是最大值'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 风格，本题写法无需改动（`//` 本来就是整除）',
                 '易错点：先判 -1，再判 `bad` 为空返回 0',
                 '对比灵神：灵神用 Counter 相加判无解，只数坏列；这里用三个字典手动计数'],
    ),
)
