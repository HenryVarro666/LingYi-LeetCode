def _zone(t):
    if t == 0:
        return '==Green==（timer == 0）'
    if t == 30:
        return '==Orange==（timer == 30）'
    if 30 < t <= 90:
        return '==Red==（30 < timer <= 90）'
    return '==Invalid==（都不满足）'


def _text(S):
    if 'timer' not in S:
        return '依次输入 `0`、`30`、`60`、`5`，看每个落在哪个区间'
    return f"`timer = {S['timer']}` → 区间：{_zone(S['timer'])}"


def _cond(S, B, ret):
    t = S['timer']
    return t


CONFIG = dict(
    num=3894, title='交通信号灯的颜色', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='按题意模拟', tags=[],
    code='''
class Solution:
    def trafficSignal(self, timer: int) -> str:
        if timer == 0:
            return "Green"
        if timer == 30:
            return "Orange"
        if 30 < timer <= 90:
            return "Red"
        return "Invalid"
''',
    call='[Solution().trafficSignal(t) for t in (0, 30, 60, 5)]',
    expect=['Green', 'Orange', 'Red', 'Invalid'],
    views=[
        dict(type='text', fn=_text, size=34, h=90),
        dict(type='array', var=lambda S: [0, 30, '31~90', '其他'], label='四种情况（对应 Green / Orange / Red / Invalid）', cell=150,
             color=lambda S, i, v: ('green' if i == 0 else 'orange' if i == 1 else 'pink' if i == 2 else 'purple') if 'timer' in S and ((i == 0 and S['timer'] == 0) or (i == 1 and S['timer'] == 30) or (i == 2 and 30 < S['timer'] <= 90) or (i == 3 and not (S['timer'] in (0, 30) or 30 < S['timer'] <= 90))) else None,
             h=220),
    ],
    watch=[('timer', 'timer', 'blue')],
    captions={
        'if timer == 0': '`timer = {timer}`：是 `0` 吗？{"是 → 绿灯" if timer == 0 else "不是，往下看"}',
        'if timer == 30': '`timer = {timer}`：是 `30` 吗？{"是 → 橙灯" if timer == 30 else "不是，往下看"}',
        'if 30 < timer <= 90': '`30 < {timer} <= 90`：{"成立 → 红灯" if 30 < timer <= 90 else "不成立，三种情况都不满足"}',
        'return "Green"': '返回 `Green`',
        'return "Orange"': '`timer == 30` 只有这一个值是橙灯，返回 `Orange`',
        'return "Red"': '落在 `(30, 90]` 内，返回 `Red`',
        'return "Invalid"': '前三个条件都没命中，兜底返回 `Invalid`',
    },
    cards=dict(
        one_liner='题目怎么说，就怎么做：按规则逐条判断',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`timer` 是信号灯剩余秒数',
                 '`0` → Green，`30` → Orange，`(30, 90]` → Red，其余 Invalid',
                 '示例：`60` → `Red`，`5` → `Invalid`',
                 '本视频依次演示 `0`、`30`、`60`、`5`'],
        quote='题目怎么说，我们就怎么做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三条规则互不重叠，按顺序 `if` 判断即可',
              '都不满足时，最后一行统一返回 `Invalid`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：区间是 `30 < timer <= 90`，左开右闭，`30` 本身是 Orange',
                 'Python 支持链式比较 `30 < timer <= 90`，不用写 and'],
    ),
)
