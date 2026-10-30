def _text(S):
    if 'timer' not in S:
        return '依次输入 `0`、`30`、`45`、`100`'
    t = S['timer']
    z = '==Green==' if t == 0 else '==Orange==' if t == 30 else '==Red==' if 30 < t <= 90 else '==Invalid=='
    return f'`timer = {t}` → {z}'


CONFIG = dict(
    num=3894, title='交通信号灯的颜色', difficulty='Easy', category='模拟',
    author='yiduobo', technique='if 逐条判断', tags=[],
    code='''
class Solution(object):
    def trafficSignal(self, timer):
        
        if timer == 0:
            return "Green"
        if timer == 30:
            return "Orange"
        if 30 < timer <= 90:
            return "Red"
        return "Invalid"
''',
    call='[Solution().trafficSignal(t) for t in (0, 30, 45, 100)]',
    expect=['Green', 'Orange', 'Red', 'Invalid'],
    views=[
        dict(type='text', fn=_text, size=34, h=90),
        dict(type='array', var=lambda S: ['0', '30', '31~90', '其他'], label='规则：Green / Orange / Red / Invalid', cell=150,
             color=lambda S, i, v: ('green' if i == 0 else 'orange' if i == 1 else 'pink' if i == 2 else 'purple') if 'timer' in S and ((i == 0 and S['timer'] == 0) or (i == 1 and S['timer'] == 30) or (i == 2 and 30 < S['timer'] <= 90) or (i == 3 and not (S['timer'] in (0, 30) or 30 < S['timer'] <= 90))) else None,
             h=220),
    ],
    watch=[('timer', 'timer', 'blue')],
    captions={
        'if timer == 0': '`timer = {timer}`，等于 `0` 吗？{"是，绿灯" if timer == 0 else "否，继续判断"}',
        'if timer == 30': '`timer = {timer}`，等于 `30` 吗？{"是，橙灯" if timer == 30 else "否，继续判断"}',
        'if 30 < timer <= 90': '`30 < {timer} <= 90`？{"成立，红灯" if 30 < timer <= 90 else "不成立，没有任何规则命中"}',
        'return "Green"': '返回 `Green`',
        'return "Orange"': '返回 `Orange`',
        'return "Red"': '返回 `Red`',
        'return "Invalid"': '以上条件均不满足，返回 `Invalid`',
    },
    cards=dict(
        one_liner='比较基础的题目：照着题目要求 if 判断',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给一个整数 `timer`，表示信号灯剩余秒数',
                 '`0` 绿，`30` 橙，`30 < timer <= 90` 红，其余 Invalid',
                 '本视频演示 `0`、`30`、`45`、`100`'],
        quote='比较基础的题目，直接按照题目要求if判断一下就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['规则互斥，没有先后依赖：从上到下逐条判断',
              '全部不满足就落到最后一行，返回 `Invalid`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`timer = 30` 属于 Orange，不属于 Red（红灯区间左开）',
                 '原文为 Python 2 风格，除类型说明外无需改动'],
    ),
)
