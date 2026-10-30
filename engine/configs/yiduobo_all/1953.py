CONFIG = dict(
    num=1953, title='你可以工作的最大周数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='最大任务量与其余之和比较',
    tags=['灵神题单', '难度分 1804'],
    code='''
class Solution(object):
    def numberOfWeeks(self, milestones):

        s = sum(milestones)
        max_n = max(milestones)

        if max_n > s - max_n + 1:
            return s - max_n + s - max_n + 1
        
        return s
''',
    call='Solution().numberOfWeeks([5,2,1])',
    expect=7,
    views=[
        dict(type='bars', var='milestones', label='milestones（每个项目的任务数）', h=320,
             color=lambda S, i, v: 'orange' if 'max_n' in S and v == S['max_n'] and i == S['milestones'].index(S['max_n']) else None),
        dict(type='text', size=32, fn=lambda S: (
            f"总数 `s = {S['s']}`" if 's' in S else '')),
        dict(type='text', size=32, fn=lambda S: (
            f"`max_n = {S['max_n']}`  vs  `s - max_n + 1 = {S['s']-S['max_n']+1}`" if 'max_n' in S else '')),
    ],
    watch=[('s', 's', 'blue'), ('max_n', 'max_n', 'orange')],
    captions={
        's = sum': '任务总数 `s = {s}`，是最多能工作的周数上限',
        'max_n = max': '最大任务数 `max_n = {max_n}`，其余任务共 `{s - max_n}` 个',
        'if max_n >': lambda S, B, r: (f'`{S.max_n} > {S.s-S.max_n}+1`：最大项目的任务太多，其余项目不够隔开 → 进入 if'
                                       if S.max_n > S.s - S.max_n + 1 else
                                       f'`{S.max_n} <= {S.s-S.max_n}+1`：能做完所有任务，不进 if'),
        'return s - max_n': '尽量多安排最大项目：`({s}-{max_n})*2+1` = =={ret}== 周',
        'return s': '所有任务都能做完 → =={ret}==',
    },
    cards=dict(
        one_liner='最大项目任务不超过其余之和加一，就能全做完',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每周完成某个项目的恰好一个阶段任务，连续两周不能是同一项目',
                 '求最多工作几周',
                 '本视频：`[5,2,1]` → `7`'],
        quote='设数组中的最大值为max_n，总和为s，那么若max_n <= s - max_n + 1，就可以全部完成，答案为s，否则答案为是(s - max_n) * 2 + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到 n = 3 的简化版题，结论一样',
              '`m[0] = m[1]` 时按前 k 个相等的任务轮流做，一直做完',
              '`m[0] > m[1]` 时用别的任务去隔开任务 0，隔不完就多出任务 0 放弃'],
        after=[dict(heading='作者的推导', lines=['m 从大到小排序，分 `m[0]=m[1]` 与 `m[0]>m[1]` 两种', '后者用任务 0 与最小的任务交替消耗，直到 `m[0]=m[1]+1`', '消耗不完时，任务 0 最多安排 `s-m[0]+1` 次', '总数为 `(s-m[0])*2+1`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：条件里的 `+1`，最大项目可以放首尾',
                 '这份写法不需要排序，只要 sum 与 max',
                 '对比灵神：灵神写成 `min(s, 2(s-m)+1)`，这里拆成 if 判断，等价'],
    ),
)
