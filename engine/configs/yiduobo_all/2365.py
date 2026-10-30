CONFIG = dict(
    num=2365, title='任务调度器 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记录不可用时间',
    tags=[],
    code='''
class Solution(object):
    def taskSchedulerII(self, tasks, space):

        disable = {}
        now = 1
        for t in tasks:
            if disable.get(t, 0) < now:
                disable[t] = now + space
                now += 1
            else:
                now = disable[t] + 2
                disable[t] += space + 1
        
        return now - 1
''',
    call='Solution().taskSchedulerII([1,2,1,2,3,1], 3)',
    expect=9,
    views=[
        dict(type='array', var='tasks', label='tasks（蓝 = 当前任务的同类型）', h=170,
             color=lambda S, i, v: 'blue' if 't' in S and v == S['t'] else None),
        dict(type='map', var='disable', label='disable：每种任务最晚的不可用时间', h=260),
        dict(type='text', h=90, fn=lambda S: f"下一个可用时间戳 now = =={S['now']}==" if 'now' in S else ''),
    ],
    watch=['t', ('now', 'now', 'green'), 'space'],
    captions={
        'disable = {}': '`disable[t]`：任务 t 在这个时间戳及以前都不可用',
        'now = 1': '`now` 是当前时间戳，从 1 开始',
        'if disable.get': lambda S, B, r: (f'`disable[{B.t}] = {B.disable.get(B.t, 0)} < now = {B.now}` → 已经可用，直接执行'
                                           if B.disable.get(B.t, 0) < B.now
                                           else f'`disable[{B.t}] = {B.disable[B.t]} >= now = {B.now}` → 还在冷却，要等'),
        'disable[t] = now + space': '执行后接下来 `space` 个单位不可用：`disable[{t}] = {now} + {space}` = {disable[t]}',
        'now += 1': '`now` → {now}',
        'now = disable[t] + 2': '等到 `disable[t] + 1` 才能开始执行，执行完时间戳是 `disable[t] + 2`：`now = {now}`',
        'disable[t] += space + 1': '任务 `{t}` 又执行了一次，不可用时间再顺延 `space + 1`：`disable[{t}] = {disable[t]}`',
        'return now - 1': '`now` 是下一个时间戳，所以答案是 `now - 1 = {now-1}`',
    },
    cards=dict(
        one_liner='哈希表记下每种任务的不可用时间，一趟顺序执行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['任务必须按顺序执行，每天做一个或休息',
                 '同类型任务之间至少隔 `space` 天，求最少总天数',
                 '示例：`tasks=[1,2,1,2,3,1], space=3` → `9`'],
        quote='可以使用哈希表disable记录每种任务最晚的不可用时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 大于 `disable[t]`：直接执行，并令 `disable[t] = now + space`、`now += 1`',
              '否则必须等到 `disable[t] + 1` 才能开始，`now = disable[t] + 2`',
              '遍历完 `now` 是下一个时间戳，所以答案 `now - 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`now` 从 1 开始，返回 `now - 1`',
                 '等待分支里 `disable[t]` 要加 `space + 1`，不是 `now + space`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
