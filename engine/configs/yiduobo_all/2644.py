CONFIG = dict(
    num=2644, title='找出可整除性得分最大的整数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='双重循环计数，ma/res 擂台更新', tags=[],
    code='''
class Solution(object):
    def maxDivScore(self, nums, divisors):

        ma = 0
        res = 10 ** 9 + 1
        for d in divisors:
            cnt = 0
            for v in nums:
                if v % d == 0:
                    cnt += 1
            
            if ma < cnt or (ma == cnt and d < res):
                ma = cnt
                res = d
        
        return res
''',
    call='Solution().maxDivScore([2,9,15,50], [5,3,7,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 能被当前 d 整除）', h=140,
             color=lambda S, i, v: 'green' if 'd' in S and v % S['d'] == 0 else None),
        dict(type='array', var='divisors', label='divisors（蓝 = 当前 d）', h=140,
             color=lambda S, i, v: 'blue' if v == S.get('d') else ('green' if v == S.get('res') else None)),
    ],
    watch=[('d', 'd', 'blue'), ('v', 'v', 'pink'), ('cnt', 'cnt', 'orange'), ('ma', 'ma', 'green'), ('res', 'res', 'green')],
    captions={
        'ma = 0': '`ma` 记最大得分，初值 0',
        'res = 10': '`res` 记答案，初值取一个比任何 d 都大的数 `10^9 + 1`',
        'cnt = 0': '换一个除数 `d = {d}`，计数清零',
        'if v % d == 0': lambda S, B, r: (f'`{S.v} % {S.d} == 0` → 整除，计一个' if S.v % S.d == 0
                                          else f'`{S.v} % {S.d} = {S.v % S.d}` ≠ 0 → 不整除'),
        'cnt += 1': '`cnt` → {cnt}',
        'if ma < cnt': lambda S, B, r: (f'`ma = {S.ma} < cnt = {S.cnt}`：得分更高 → 更新' if S.ma < S.cnt
                                        else f'得分相同 `{S.cnt}`，且 `d = {S.d} < res = {S.res}` → 更新' if S.ma == S.cnt and S.d < S.res
                                        else f'`cnt = {S.cnt}` 没有超过 `ma = {S.ma}`，d 也不更小 → 不更新'),
        'ma = cnt': '最大得分 `ma` → {ma}',
        'res = d': '答案 `res` → {res}',
        'return res': '最大得分里最小的除数：`{res}`',
    },
    cards=dict(
        one_liner='对每个除数数一遍整除个数，按题意擂台更新',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['`divisors[i]` 的得分 = `nums` 中被它整除的个数',
                 '返回得分最大的除数，并列取最小',
                 '示例：`[4,7,9,3,9]`、`[5,2,3]` → `3`'],
        quote='直接遍历divisors中的所有整数，对于当前遍历到的整数d，遍历nums，计算nums中可以整除d的个数cnt，然后按照题目要求使用cnt和d更新最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举 `d`，内层数 `nums` 里整除的个数 `cnt`',
              '`ma < cnt` 得分更高就换；`ma == cnt` 时 `d` 更小也换',
              '`res` 初值设成大于任何 d 的数，让并列比较有意义'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '`ma = 0` 时，得分为 0 的 d 靠 `ma == cnt and d < res` 选出最小的',
                 '`res` 初值必须大于所有 divisors（`10^9 + 1`）',
                 '对比灵神：灵神用 `sum(1 for ...)` 并把 max_cnt 设为 -1'],
    ),
)
