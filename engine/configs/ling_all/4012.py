def _done(S):
    """当前累计时间 t 下，前缀和 <= t 的任务个数（仅在循环里有意义）"""
    if 't' not in S or 'i' not in S or S['_line'] < 11:
        return None
    return sum(1 for x in S['tasks'] if x <= S['t'])


def _txt(S):
    k = _done(S)
    if k is None:
        return '前缀和 `s` 单调递增 → 可以对它二分'
    n = len(S['tasks'])
    if k >= n:
        return f"累计时间 `t = {S['t']}` >= 总时长 `{S['tasks'][-1]}` → ==全部完成==，t 清零"
    return f"累计时间 `t = {S['t']}`：前缀和 `<= t` 的有 `{k}` 个 → 未完成 `{n} − {k}` = =={n - k}=="


CONFIG = dict(
    num=4012, title='统计每个班次结束后的未完成任务数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='前缀和 + 二分查找',
    tags=['二分查找', '进阶', '难度分 1736'],
    code='''
class Solution:
    def countTasks(self, tasks: list[int], shifts: list[int]) -> list[int]:
        n = len(tasks)
        # 原地计算 tasks 的前缀和
        for i in range(1, n):
            tasks[i] += tasks[i - 1]

        t = 0
        for i, shift in enumerate(shifts):
            t += shift
            if t >= tasks[-1]:  # 完成所有任务
                t = 0
                shifts[i] = 0
            else:
                shifts[i] = n - bisect_right(tasks, t)
        return shifts
''',
    call='Solution().countTasks([2,3,4,5], [4,3,6,20,3])',
    expect=[3, 2, 1, 0, 3],
    views=[
        dict(type='text', size=26, fn=_txt),
        dict(type='array', var='tasks', label='tasks（原地变成前缀和，绿 = 已完成的任务）', h=260,
             color=lambda S, i, v: 'green' if (_done(S) or 0) > i else None),
        dict(type='array', var='shifts', label='shifts（原地改写成答案 ans）', h=260,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] and S['_line'] >= 11 else ('yellow' if 'i' in S and i < S['i'] else None)),
    ],
    watch=[('t', 't', 'cyan'), ('i', 'i', 'blue'), ('shift', 'shift'), ('n', 'n')],
    captions={
        'tasks[i] += tasks[i - 1]': '前缀和：`tasks[{i}]` = {tasks[i]}，表示前 `{i + 1}` 个任务总共要这么多时间',
        't += shift': '这个班次有 `{shift}` 单位时间 → 累计 `t = {t}`（上一班没做完的进度保留在 t 里）',
        'if t >= tasks[-1]': lambda S, B, r: (f"`t = {S.t}` >= 总时长 `{S.tasks[-1]}`：这一班把任务全做完了" if S.t >= S.tasks[-1]
                                               else f"`t = {S.t}` < 总时长 `{S.tasks[-1]}`：还有任务没做完"),
        'shifts[i] = 0': '全部完成 → 本班答案 `0`；剩余时间丢弃，==下一班重新从第 0 个任务开始==',
        't = 0': lambda S, B, r: ('累计时间清零，下一班重新从头做' if S._line > 10 else '`t` 是当前「连续处理」的累计时间，从头开始计时'),
        'bisect_right(tasks, t)': lambda S, B, r: (f"二分找第一个 `> t = {S.t}` 的前缀和下标 `k' = {len(S.tasks) - S.shifts[S.i]}`"
                                                    f"：前 `k'` 个任务都完成 → 未完成 `{len(S.tasks)} − {len(S.tasks) - S.shifts[S.i]}` = =={S.shifts[S.i]}=="),
        'return shifts': '`shifts` 已被原地改写成每个班次后的未完成数：`{shifts}`',
    },
    cards=dict(
        one_liner='前缀和递增 → 二分查出累计时间 t 能完成几个任务',
        complexity='时间 `O(n + m log n)`，空间 `O(1)`（原地）',
        problem=['任务按顺序做，时间 `tasks[i]`；班次时间 `shifts[j]`，没做完的任务下一班继续',
                 '某班把所有任务做完 → 剩余时间丢弃，下一班从第 0 个任务重来',
                 '求每个班次结束后的未完成任务数',
                 '示例：`tasks=[1,4,4], shifts=[9,1,4]` → `[0,2,1]`'],
        quote='我们可以在有序数组 s 中二分查找最后一个 ≤ t 的数的下标 k，那么已完成的任务下标为 [0,k]，未完成的任务下标为 [k+1,n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从时刻 0 起累计时间 `t`，前缀和 `s` 表示「做完前 j 个任务」的总用时',
              '`t` 内能完成的任务数 = 前缀和 `<= t` 的个数 → ==`bisect_right`==',
              '`t >= 总时长` 时全部完成，`t` 清零重来'],
        summary=['时间 `O(n + m log n)`，空间 `O(n)` 或原地 `O(1)`',
                 '关键：不用管「做到哪个任务的哪一步」，累计时间 `t` 本身就记录了进度',
                 '易错：完成全部任务后必须把 `t` 清零；用 `bisect_right` 而不是 `bisect_left`',
                 '灵神题解还附有二分转化表：`>= x` 用 lowerBound(x)，`> x` 用 lowerBound(x+1)'],
    ),
)
