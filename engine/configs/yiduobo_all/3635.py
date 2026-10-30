def _hl(name_s, name_d):
    def f(S, i, v):
        s = S.get('s')
        if s is None or 'second_start' not in S:
            return None
        return 'yellow' if S['second_start'][i] == s and S['second_duration'][i] == S['d'] else None
    return f


def _mode(S):
    if 'first_start' not in S:
        return '先分别算「先陆地后水上」「先水上后陆地」两种顺序'
    first = '陆地' if S['first_start'] == [2, 8] else '水上'
    second = '水上' if first == '陆地' else '陆地'
    t = S.get('t')
    if t is None:
        return f'当前顺序：先玩=={first}==，再玩=={second}=='
    return f'先玩{first}，最早 `t = {t}` 结束；逐个看{second}设施：开放时间 `s` 与 `t` 比大小'


CONFIG = dict(
    num=3635, title='最早完成陆地和水上游乐设施的时间 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='两种顺序 + 遍历另一边',
    tags=['贪心与思维', '难度分 1870'],
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
    call='Solution().earliestFinishTime([2,8], [4,1], [6,1], [3,2])',
    expect=7,
    views=[
        dict(type='array', var='first_start', label='先玩一边 · 开放时间', h=115, cell=76, index=False),
        dict(type='array', var='first_duration', label='先玩一边 · 时长', h=115, cell=76, index=False),
        dict(type='array', var='second_start', label='再玩一边 · 开放时间 s（黄 = 当前这个）', h=115, cell=76, index=False,
             color=_hl('second_start', 'second_duration')),
        dict(type='array', var='second_duration', label='再玩一边 · 时长 d', h=115, cell=76, index=False,
             color=_hl('second_start', 'second_duration')),
        dict(type='text', h=80, size=28, fn=_mode),
    ],
    watch=[('t', 't', 'blue'), ('s', 's', 'cyan'), ('d', 'd', 'cyan'), ('finish', 'finish', 'yellow'), ('res', 'res', 'green')],
    captions={
        't = min': '先玩的一边，挑==结束最早==的那个：`t = {t}`',
        'res = None': '`res` 记录「再玩另一边」的最早结束时间，先置空',
        'for s, d in': lambda S, B, ret: ('看另一边的设施：开放 `s = %s`，时长 `d = %s`' % (S['s'], S['d'])) if (B.get('s') != S['s'] or B.get('d') != S['d']) else '另一边的设施都看完了',
        'if s > t': '`s > t`？`{s} > {t}` → {"==是，要等它开放==" if s > t else "==否，已经开放，直接玩=="}',
        'finish = s + d': '还没开放，要等到 `s` 才开始：`finish = {s} + {d}` = =={finish}==',
        'finish = t + d': '已经开放，`t` 时刻接着玩：`finish = {t} + {d}` = =={finish}==',
        'if res is None': '`res` 为空或比 `finish` 大 → {"==更新答案==" if (B.res is None or B.res > finish) else "不更新"}',
        'res = finish': '更新：`res = {res}`',
        'return res': '这个顺序的最早结束时间 = =={ret}==',
        'return min(calc': '先算「先陆地、再水上」；另一种顺序紧接着算，最后取较小值',
    },
    cards=dict(
        one_liner='先玩一边挑结束最早的，再扫另一边，两种顺序取小',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['陆地、水上设施各玩一个，顺序不限；设施在开放时间之后才能开始',
                 '开始于 `t`，结束于 `t + duration`；求两个都玩完的最早时间',
                 '示例：陆地 `[2,8]/[4,1]`，水上 `[6]/[3]` → `9`'],
        quote='无论是先玩哪一边，都应该玩结束时间最早的那个游乐设施',
        quote_src='—— yiduobo 题解',
        idea=['分别算「先陆地再水上」和「先水上再陆地」，取较小值',
              '先玩的一边：一趟遍历找最早结束时间 `t`',
              '另一边每个设施：`s <= t` 则 `t + d`，否则等到 `s + d`'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '易错点：先玩的一边要选「结束最早」而不是开放最早',
                 '`s > t` 要等开放：结束时间是 `s + d`，不是 `t + d`',
                 '两种先后顺序都要算'],
    ),
)
