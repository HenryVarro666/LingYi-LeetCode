CONFIG = dict(
    num=2365, title='任务调度器 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 模拟',
    tags=[],
    code='''
class Solution:
    def taskSchedulerII(self, tasks: List[int], space: int) -> int:
        ans, last = 0, {}
        for t in tasks:
            ans += 1  # 完成该任务，天数+1
            if t in last:
                ans = max(ans, last[t] + space + 1)  # 看看是否要间隔 space 天
            last[t] = ans  # 记录上一次完成时间
        return ans
''',
    call='Solution().taskSchedulerII([1,2,1,2,3,1], 3)',
    expect=9,
    views=[
        dict(type='array', var='tasks', label='tasks（蓝 = 当前任务的同类型）', h=170,
             color=lambda S, i, v: 'blue' if 't' in S and v == S['t'] else None),
        dict(type='map', var='last', label='last：每种任务上一次完成在第几天', h=260),
        dict(type='text', h=90, fn=lambda S: f"今天是第 =={S['ans']}== 天" if 'ans' in S else ''),
    ],
    watch=['t', ('ans', 'ans', 'green'), 'space'],
    captions={
        'ans, last = 0, {}': '`ans` 记录已经过的天数，`last` 记录每种任务上次完成的那一天',
        'ans += 1': '先假设今天就能做：天数 +1 → `ans = {ans}`',
        'if t in last': lambda S, B, r: (f'任务 `{B.t}` 以前做过（第 `{B.last[B.t]}` 天）→ 要检查间隔' if B.t in B.last
                                         else f'任务 `{B.t}` 第一次出现 → 不受限制'),
        'ans = max': '最早可做的日子是 `last[t] + space + 1 = {last[t]} + {space} + 1 = {last[t]+space+1}`，和今天 `{B.ans}` 取大 → `ans = {ans}`（比今天晚就要休息）',
        'last[t] = ans': '记下任务 `{t}` 完成于第 `{ans}` 天',
        'return ans': '全部做完，共 `{ans}` 天',
    },
    cards=dict(
        one_liner='按题意模拟：每个任务做完后，记下它完成的那一天',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['任务必须按顺序做，每天做一个任务或休息',
                 '同类型任务之间至少隔 `space` 天，求最少总天数',
                 '示例：`tasks=[1,2,1,2,3,1], space=3` → `9`'],
        quote='按照题意模拟，遍历 tasks 的同时维护答案，具体见注释。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ans` 就是“当前任务完成在第几天”',
              '先 `ans += 1`；若同类型任务做过，最早只能在 `last[t] + space + 1` 天',
              '两者取大，差出来的天数就是休息的天数'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希表按任务类型存）',
                 '易错：间隔是 `space` 天，所以下一次最早是 `last + space + 1`',
                 '不用真的模拟休息的每一天，直接让 `ans` 跳到那一天'],
    ),
)
