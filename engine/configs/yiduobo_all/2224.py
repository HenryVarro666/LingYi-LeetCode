CONFIG = dict(
    num=2224, title='转化时间需要的最少操作数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='贪心 · 60/15/5/1 依次填充',
    tags=[],
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
        dict(type='string', var='current', label='current', cell=70, h=120),
        dict(type='string', var='correct', label='correct', cell=70, h=120),
        dict(type='array', var='delta_list', label='delta_list（每次可加的分钟数，黄 = 当前 delta）', cell=96, h=160,
             color=lambda S, i, v: 'yellow' if S.get('delta') == v and S['_line'] in (10, 11, 12) else None),
        dict(type='text', h=110, size=32, fn=lambda S: (
            f"差值 `now` = =={S['now']}== 分钟，已用 `res` = =={S['res']}== 次" if 'now' in S and 'res' in S
            else (f"`m1` = =={S['m1']}==，`m2` = =={S['m2']}==" if 'm2' in S else ''))),
    ],
    watch=[('m1', 'm1', 'blue'), ('m2', 'm2', 'pink'), ('delta', 'delta', 'yellow'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'm1 = ': '`{current}` 换成分钟：`{current[:2]}×60 + {current[3:]}` = =={m1}==',
        'm2 = ': '`{correct}` 换成分钟：`{correct[:2]}×60 + {correct[3:]}` = =={m2}==',
        'now = m2 - m1': '问题变成：凑出 `{m2} − {m1}` = =={now}== 分钟，用的次数最少',
        'res = 0': '`res` 记录操作次数',
        'delta_list = [': '60、15、5、1 后一个都整除前一个 → 可以==贪心==，大的优先',
        'for delta in delta_list': '轮到 `delta = {delta}`',
        'res += now // delta': '还剩 `{B.now}` 分钟，能放 `{B.now} // {delta}` = =={B.now // delta}== 个 `{delta}` → `res = {res}`',
        'now %= delta': '放完剩下 `{B.now} % {delta}` = =={now}== 分钟，交给更小的面额',
        'return res': '剩余为 0，共 `{res}` 次操作',
    },
    cards=dict(
        one_liner='60、15、5、1 互为倍数，大面额优先就是最优',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每步可加 `1`、`5`、`15`、`60` 分钟，求 `current` 变成 `correct` 的最少步数',
                 '示例：`"02:30"` → `"04:35"`，答案 `3`',
                 '本视频：同示例，差 125 分钟'],
        quote='乍一看似乎是背包问题，但是实际上由于60、15、5、1之间具有倍数关系，因此在这里可以使用贪心。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把两个时间都换成分钟，作差得到要凑的分钟数',
              '依次用 60、15、5、1 去填：能放几个放几个',
              '放不下的余数留给下一个更小的数'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '能贪心是因为面额两两整除；一般的硬币问题要用 DP',
                 '易错：先转成分钟再相减，不要分别处理时和分',
                 '原文为 Python 2 写法，`res += now / delta` 已改为 `//`（整数除法）'],
    ),
)
