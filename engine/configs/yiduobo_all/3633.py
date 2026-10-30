CONFIG = dict(
    num=3633, title='最早完成陆地和水上游乐设施的时间 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='枚举先玩哪一类 · 先玩最早结束的', tags=[],
    code='''
class Solution(object):
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
        
        def calc(first_start, first_duration, second_start, second_duration):
            t = min([s + d for s, d in zip(first_start, first_duration)])
            res = None
            for s, d in zip(second_start, second_duration):
                if s > t:
                    finish = s + d
                else:
                    finish = t + d
                if res is None or res > finish:
                    res = finish
            return res

        return min(calc(landStartTime, landDuration, waterStartTime, waterDuration), calc(waterStartTime, waterDuration, landStartTime, landDuration))
''',
    call='Solution().earliestFinishTime([2,8,5], [4,1,6], [6,1], [3,10])',
    expect=9,
    views=[
        dict(type='array', var=lambda S: S.get('first_start', S['landStartTime']), label='先玩一类：开放时间', h=130, cell=64, pointers={}),
        dict(type='array', var=lambda S: S.get('first_duration', S['landDuration']), label='先玩一类：时长', h=130, cell=64, pointers={}),
        dict(type='array', var=lambda S: S.get('second_start', S['waterStartTime']), label='再玩一类：开放时间（粉箭头 = 当前 s）', h=190, cell=64,
             pointers={'second_start.index(s)': 'pink'}, pointer_labels={'second_start.index(s)': 's'}),
        dict(type='array', var=lambda S: S.get('second_duration', S['waterDuration']), label='再玩一类：时长', h=130, cell=64, pointers={}),
    ],
    watch=['t', 'res', 'finish'],
    captions={
        'return min(calc': '分别算「先陆地再水上」和「先水上再陆地」，取较小值',
        't = min(': '先玩的一类里挑 `s + d` 最小的，最早结束时刻 `t` = =={t}==',
        'res = None': '`res` 记录后玩一类的最早结束时间',
        'if s > t': lambda S, B, r: (f'`s = {S.s} > t = {S.t}`：设施还没开放，得等到 `s` 才能开始' if S.s > S.t
                                      else f'`s = {S.s} ≤ t = {S.t}`：结束时已经开放，立刻就能玩'),
        'finish = s + d': '要等待：`finish = s + d = {s} + {d}` = =={finish}==',
        'finish = t + d': '不用等：`finish = t + d = {t} + {d}` = =={finish}==',
        'if res is None': lambda S, B, r: (f'第一个候选 `{S.finish}`，直接记下' if S.res is None
                                           else f'`res = {S.res}` 与 `finish = {S.finish}`：{"更早，更新" if S.res > S.finish else "不更好，保留"}'),
        'res = finish': '`res` 更新为 =={res}==',
        'return res': '这一类先玩的最早完成时间：=={res}==',
    },
    cards=dict(
        one_liner='先玩哪类各算一遍：先玩的选结束最早的，后玩的枚举取最小',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['陆地、水上设施各玩恰好一个，顺序不限',
                 '设施 `s` 之后才开放，开始于 `t` 则结束于 `t + duration`',
                 '求完成两个设施的最早时间'],
        quote='无论是先玩哪一边，都应该玩结束时间最早的那个游乐设施',
        quote_src='—— yiduobo 题解原文',
        idea=['先玩一类：选 `s + d` 最小的，结束时刻 `t`',
              '再玩另一类：开始于 `max(s, t)`，结束于 `max(s, t) + d`',
              '陆地先、水上先各算一次，取较小值'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '易错点：到了 `t` 若设施还没开放，要等到 `s` 才能开始',
                 '两个方向都要算，不能只算先陆地',
                 '原文代码无需改动，直接 Python 3 运行'],
    ),
)
