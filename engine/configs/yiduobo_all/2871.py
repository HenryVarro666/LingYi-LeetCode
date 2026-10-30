CONFIG = dict(
    num=2871, title='将数组分割成最多数目的子数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='先定最小分数 · 为 0 就划分',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def maxSubarrays(self, nums):

        res = 0
        now = None
        for v in nums:
            if now is None:
                now = v
            else:
                now &= v
            
            if now == 0:
                res += 1
                now = None
        
        if res == 0:
            res = 1
        
        return res
''',
    call='Solution().maxSubarrays([1,0,2,0,1,2])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums'),
        dict(type='text', fn=lambda S: (f"当前子数组的分数 `now = {S['now']}`　已划分 `res = {S['res']}` 段" if 'now' in S else ''), size=38),
    ],
    watch=[('v', 'v', 'blue'), ('now', 'now', 'purple'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录分数为 0 的子数组个数',
        'now = None': '`now` 是当前子数组的分数，`None` 表示还没开始',
        'for v in nums': '取下一个数 `v = {v}`',
        'if now is None': lambda S, B, r: ('当前没有子数组 → 这个数作为新子数组的开头' if B.now is None else f'当前子数组分数是 `{B.now}`，把 `v = {S.v}` 并进来'),
        'now = v': '新子数组从 `{v}` 开始，`now = {now}`',
        'now &= v': '按位与是越算越小：`now` AND `{v}` → {now}',
        'if now == 0': lambda S, B, r: ('`now == 0`：分数已经到 0 → ==立刻划分==，后面的数留给下一段' if S.now == 0 else f'`now = {S.now}` 不为 0，继续累积'),
        'res += 1': '划出一段分数为 0 的子数组：`res` → {res}',
        'now = None': lambda S, B, r: ('划分后清空 `now`，重新开始' if S['_line'] != 5 else '`now` 是当前子数组的分数，`None` 表示还没开始'),
        'if res == 0': lambda S, B, r: ('`res = 0`：整个数组的 AND 都不为 0，只能不划分' if S.res == 0 else f'`res = {S.res}`，已经划出分数为 0 的段'),
        'res = 1': '整体分数大于 0，划分越多总分越大 → 整个数组算 1 段',
        'return res': '最多可分 `{ret}` 段（末尾不为 0 的数合并进最后一段）',
    },
    cards=dict(
        one_liner='分数为正就别分；能到 0 就切，切得越早剩得越多',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组切成连续子数组，每段分数 = 段内所有数的按位与',
                 '总分数要最小，且在此前提下段数最多',
                 '示例：`[1,0,2,0,1,2]` → `3`'],
        quote='当子数组的分数为正数时，分得越多分数和就越大，这也就意味着只有当分数为0时才需要尽量多分，而分数大于0时不进行任何划分才能让分数之和最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小总分 = 整个数组的 AND：不为 0 就答案 1',
              '为 0 时从头往后算当前段分数，一到 0 就划走',
              '末尾分数不为 0 的零头并入最后一段，段数不变'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用 `None` 表示还没开始的段，比用 0 安全（0 本身就是目标分数）',
                 '`res == 0` 时要改成 1：整个数组 AND 大于 0，只能一段',
                 '对比灵神：灵神用 `-1` 全 1 当 AND 的单位元，省掉 `None` 判断'],
    ),
)
