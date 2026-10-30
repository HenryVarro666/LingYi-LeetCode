CONFIG = dict(
    num=1953, title='你可以工作的最大周数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='相邻不同 · 最大值 vs 其余和',
    tags=['灵神题单', '难度分 1804'],
    code='''
class Solution:
    def numberOfWeeks(self, milestones: List[int]) -> int:
        s = sum(milestones)
        m = max(milestones)
        return min(s, (s - m) * 2 + 1)
''',
    call='Solution().numberOfWeeks([5,2,1])',
    expect=7,
    views=[
        dict(type='text', size=30, fn=lambda S: "把阶段任务看成小球：项目 i 有 `milestones[i]` 个球，相邻不能同色"),
        dict(type='bars', var='milestones', label='milestones（每个项目的任务数）', h=300,
             color=lambda S, i, v: 'orange' if 'm' in S and v == S['m'] and i == S['milestones'].index(S['m']) else None),
        dict(type='text', size=32, fn=lambda S: (
            f"总数 `s = {S['s']}`（序列长度上界）" if 's' in S else '')),
        dict(type='text', size=32, fn=lambda S: (
            f"最大 `m = {S['m']}` 与 其余之和加一 `{S['s']-S['m']+1}`" if 'm' in S else '')),
    ],
    watch=[('s', 's', 'blue'), ('m', 'm', 'orange')],
    captions={
        's = sum': '任务总数 `s = {s}`：每周做一个，最多工作 `{s}` 周',
        'm = max': '最多的项目 `m = {m}`：它要被别的任务隔开，其余任务共 `{s - m}` 个',
        'return min': lambda S, B, r: (f'`m = {S.m} <= s-m+1 = {S.s-S.m+1}`：能排成相邻不同的序列，工作 `s` 周 → =={r}=='
                                       if S.m <= S.s - S.m + 1 else
                                       f'`m = {S.m} > s-m+1 = {S.s-S.m+1}`：只能把 m 放奇偶间隔，长度 `(s-m)*2+1` → =={r}=='),
    },
    cards=dict(
        one_liner='相邻不同：最大的那堆不能超过其余之和加一',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每周完成某个项目的恰好一个阶段任务，连续两周不能是同一项目',
                 '无法继续时停止，求最多工作几周',
                 '示例：`[5,2,1]` → `7`'],
        quote='相当于给你一些小球，颜色为 x 的小球有 milestones[x] 个。你需要选择一些小球，排成一排，使得所有相邻小球的颜色都不同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设和为 `s`，最大值为 `m`；`s` 是序列长度的上界',
              '`m <= s - m + 1`：一定能排满，答案 `s`',
              '`m > s - m + 1`：`m` 只能放偶数位，其余放奇数位，长度 `2*(s-m)+1`'],
        after=[dict(heading='两个例子', lines=['`[1,2,3]`：`m = 3 <= 4`，工作 `6` 周', '`[5,2,1]`：`m = 5 > 4`，只能 `2*3+1 = 7` 周', '`[3,1]`：`s-m = 1`，`2*1+1 = 3` 周，多出的一个 0 放不下'])],
        summary=['时间 `O(n)`，空间 `O(1)`，一次遍历求和与最大值',
                 '易错点：别漏掉 `+1`，序列长度可以是奇数',
                 '同类题：「相邻不同」类贪心（题单 §1.8），如 2856、3785'],
    ),
)
