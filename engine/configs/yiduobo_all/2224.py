CONFIG = dict(
    num=2224, title='转化时间需要的最少操作数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='转分钟 + 贪心', tags=[],
    code='''
class Solution(object):
    def convertTime(self, current, correct):

        m1 = int(current[:2]) * 60 + int(current[3:])
        m2 = int(correct[:2]) * 60 + int(correct[3:])
        
        now = m2 - m1
        res = 0
        delta_list = [60, 15, 5, 1]
        for delta in delta_list:
            res += now // delta
            now %= delta
        
        return res
''',
    call='Solution().convertTime("02:30", "04:35")',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"{S['current']} → {S['correct']}") if 'current' in S else '', size=36, h=70),
        dict(type='array', var='delta_list', label='delta_list', pointers={'idx': 'blue'}, h=120),
        dict(type='text', fn=lambda S: (f"还差 ==`{S['now']}`== 分钟，已用 ==`{S['res']}`== 步") if 'now' in S and 'res' in S else (f"还差 ==`{S['now']}`== 分钟" if 'now' in S else ''), size=36, h=80),
    ],
    watch=['m1', 'm2', 'now', 'delta', ('res', 'res', 'green')],
    captions={
        'm1 =': '`current` 换算成分钟：`{current[:2]} × 60 + {current[3:]}` = `{m1}`',
        'm2 =': '`correct` 换算成分钟：`{correct[:2]} × 60 + {correct[3:]}` = `{m2}`',
        'now = m2 - m1': '要加的总分钟数：`{m2} − {m1}` = =={now}==',
        'res = 0': '`res` 记录操作次数',
        'delta_list =': '60、15、5、1 互为倍数 → 可以贪心，不必背包',
        'for delta in': '尝试面额 `delta = {delta}`',
        'res += now // delta': '`{B.now} // {delta}` = {B.now // delta} 个 `{delta}` → `res` = =={res}==',
        'now %= delta': '剩下的零头 `{now}` 留给更小的面额',
        'return res': '零头用完，一共 `{ret}` 步',
    },
    cards=dict(
        one_liner='先换算成分钟，再从大面额往下填',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['可加 `1`、`5`、`15`、`60` 分钟，求从 `current` 到 `correct` 的最少步数',
                 '本视频：`"02:30"` → `"04:35"` 差 `125` 分钟 → `3` 步'],
        quote='乍一看似乎是背包问题，但是实际上由于60、15、5、1之间具有倍数关系，因此在这里可以使用贪心。',
        quote_src='—— yiduobo 题解原文',
        idea=['`int(current[:2]) * 60 + int(current[3:])` 切出时和分',
              '差值先尽量用 `60` 填，填不了的再用 `15`、`5`、`1`',
              '倍数关系保证大面额多用不会让总步数变多'],
        summary=['原文为 Python 2 写法，其中整数除法 `now / delta` 已改为 `now // delta`',
                 '时间 `O(1)`，空间 `O(1)`',
                 '易错：`current <= correct`，不用处理跨天',
                 '贪心的前提是面额互为倍数'],
    ),
)
