CONFIG = dict(
    num=2644, title='找出可整除性得分最大的整数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举除数，并列取小', tags=[],
    code='''
class Solution:
    def maxDivScore(self, nums: List[int], divisors: List[int]) -> int:
        max_cnt, ans = -1, 0
        for d in divisors:
            cnt = sum(1 for x in nums if x % d == 0)
            if cnt > max_cnt or cnt == max_cnt and d < ans:
                max_cnt, ans = cnt, d
        return ans
''',
    call='Solution().maxDivScore([2,9,15,50], [5,3,7,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 能被 d 整除）', h=140,
             color=lambda S, i, v: 'green' if 'd' in S and 'cnt' in S and v % S['d'] == 0 else None),
        dict(type='array', var='divisors', label='divisors（蓝 = 当前 d，绿 = 当前最优）', h=140,
             color=lambda S, i, v: 'blue' if v == S.get('d') else ('green' if v == S.get('ans') and S.get('max_cnt', -1) >= 0 else None)),
    ],
    watch=[('d', 'd', 'blue'), ('cnt', 'cnt', 'orange'), ('max_cnt', 'max_cnt', 'green'), ('ans', 'ans', 'green')],
    captions={
        'max_cnt, ans = -1': '`max_cnt = -1`：保证第一个 d 一定能更新',
        'cnt = sum': '`nums` 里能被 `{d}` 整除的有 `{cnt}` 个',
        'if cnt > max_cnt': lambda S, B, r: (f'`{S.cnt} > {S.max_cnt}`：得分更高 → 更新' if S.cnt > S.max_cnt
                                              else f'得分相同 `{S.cnt}`，比较 `d = {S.d}` 与 `ans = {S.ans}`：更小 → 更新' if S.cnt == S.max_cnt and S.d < S.ans
                                              else f'`cnt = {S.cnt}` 不比 `max_cnt = {S.max_cnt}` 强，也没有更小的 d → 不更新'),
        'max_cnt, ans = cnt': '更新：`max_cnt = {max_cnt}`，`ans = {ans}`',
        'return ans': '得分最大且最小的除数是 `{ans}`',
    },
    cards=dict(
        one_liner='枚举每个除数算得分，得分相同取更小的',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['`divisors[i]` 的得分 = `nums` 中能被它整除的个数',
                 '返回得分最大的除数，并列取数值最小的',
                 '示例：`[2,9,15,50]`、`[5,3,7,2]` → `2`'],
        quote='遍历 d=divisors[i]，暴力枚举 nums 中的数，统计能被 d 整除的数的个数 cnt。取 cnt 最大的 d 作为答案。如果有多个最大的 cnt，取其中最小的 d。',
        quote_src='—— 灵茶山艾府题解（优化前）',
        idea=['`max_cnt` 记最高得分，`ans` 记对应的除数',
              '更新条件：`cnt` 更大，或 `cnt` 相同且 `d` 更小'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '==并列时要比较 d 的大小==，因为 divisors 没排序',
                 '`max_cnt` 初值 `-1`，这样得分为 0 的 d 也能被选中',
                 '原文还有两个优化：nums 降序后遇到 `x < d` 就 break；divisors 排序后按上界提前退出'],
    ),
)
