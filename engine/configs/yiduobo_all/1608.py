CONFIG = dict(
    num=1608, title='特殊数组的特征值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='排序 + 从大到小枚举答案',
    tags=[],
    code='''
class Solution(object):
    def specialArray(self, nums):

        nums = sorted(nums, reverse = True)
        now = 0
        cnt = 0
        for res in range(1000, -1, -1):
            while now < len(nums) and nums[now] >= res:
                cnt += 1
                now += 1

            if res == cnt:
                return res
        
        return -1
''',
    call='Solution().specialArray([0, 4, 3, 0, 4])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（从大到小排序；蓝 = now 指向下一个没统计的数；绿 = 已统计 ≥ res）', cell=90, h=230,
             pointers={'now': 'blue'},
             color=lambda S, i, v: 'green' if 'now' in S and i < S['now'] else None),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f'枚举 `res = {S["res"]}`：大于等于它的数有 `{S["cnt"]}` 个' + ('，==相等，找到答案==' if S['res'] == S['cnt'] else '')
                           if 'res' in S else '先排序，再从 1000 往下试 res')),
    ],
    watch=[('res', 'res', 'blue'), ('cnt', 'cnt', 'green'), ('now', 'now', 'orange')],
    captions={
        'nums = sorted': '从大到小排序：`{nums}`，这样「≥ res 的数」总是排在最前面',
        'now = 0': '`now` 指向下一个还没统计的数',
        'cnt = 0': '`cnt` 记录 ≥ res 的数的个数',
        'for res in range': lambda S, B, r: (f'枚举 `res = {S.res}`，从大往小，res 变小时 ≥ res 的数只会变多'
                                             if 'res' in S else '枚举结束'),
        'while now < len': lambda S, B, r: (f'`nums[{S.now}] = {S.nums[S.now]} >= {S.res}` → 它也 ≥ res，要计入'
                                            if S.now < len(S.nums) and S.nums[S.now] >= S.res else
                                            (f'已经没有更多的数 ≥ {S.res}，`cnt = {S.cnt}`' if S.now >= len(S.nums)
                                             else f'`nums[{S.now}] = {S.nums[S.now]} < {S.res}`，不计入，停止统计')),
        'cnt += 1': '`cnt` → {cnt}',
        'now += 1': '`now` → {now}，看下一个数',
        'if res == cnt': lambda S, B, r: (f'`res = {S.res}`，`cnt = {S.cnt}` ==相等== → 找到特征值'
                                          if S.res == S.cnt else f'`res = {S.res}` ≠ `cnt = {S.cnt}` → 继续试更小的 res'),
        'return res': '找到特征值 =={ret}==',
        'return -1': '所有 res 都不满足，返回 `-1`',
    },
    skip=[],
    max_steps=48,
    cards=dict(
        one_liner='数据规模小，从 1000 往下枚举，边枚举边统计 ≥ res 的个数',
        complexity='时间 `O(n log n + C)`（C = 1000），空间 `O(n)`',
        problem=['`nums` 中恰好有 `x` 个数大于等于 `x`，则 `x` 是特征值',
                 '`x` 不必在 `nums` 里，特征值唯一；没有则返回 `-1`',
                 '示例：`[0,4,3,0,4]` → `3`（有 3 个数 ≥ 3）'],
        quote='数据规模很小，我直接采用的暴力算法，先将nums从大到小进行排序，然后从1000开始向下枚举答案res，并判断当前数据中有多少数大于等于res。',
        quote_src='—— yiduobo 题解原文',
        idea=['降序排序后，≥ res 的数一定是排在前面的一段',
              'res 从大往小，满足条件的数只增不减 → `now` 指针不回头，`cnt` 累加',
              '每个 res 统计完看 `res == cnt`，相等就是答案'],
        summary=['时间 `O(n log n + C)`，C 为枚举范围 1000，空间 `O(n)`',
                 '易错：答案 `res` 可以是 0，所以 `range(1000, -1, -1)` 要包含 0',
                 '`now` 指针单调不回头，所以 `cnt` 不用重算',
                 '作者说明：数据规模放大时可用数据结构优化；原文为 Python 2 风格，本题无需改动'],
    ),
)
