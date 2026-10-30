CONFIG = dict(
    num=1629, title='按键持续时间最长的键', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟扫描 · 维护最长',
    code='''
class Solution(object):
    def slowestKey(self, releaseTimes, keysPressed):
        res = keysPressed[0]
        max_time = releaseTimes[0]
        for index in range(1, len(releaseTimes)):
            delta_time = releaseTimes[index] - releaseTimes[index - 1]
            if delta_time > max_time or (delta_time == max_time and keysPressed[index] > res):
                max_time = delta_time
                res = keysPressed[index]
        
        return res
''',
    call="Solution().slowestKey([12,23,36,46,62], 'spuda')",
    expect='a',
    views=[
        dict(type='array', var='releaseTimes', pointers={'index': 'blue'}, h=200, cell=90, label='releaseTimes（松开时间）'),
        dict(type='string', var='keysPressed', pointers={'index': 'blue'}, h=200, cell=90, label='keysPressed（按下的键）',
             color=lambda S, i, v: 'green' if 'res' in S and 'index' in S and False else None),
        dict(type='text', fn=lambda S: (f"最长持续 `{S['max_time']}`，对应键 =={S['res']}==" if 'max_time' in S and 'res' in S else ''), size=28),
    ],
    watch=[('index', 'index', 'blue'), 'delta_time', ('max_time', 'max_time', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = keysPressed[0]': '先假设第 0 个键最长：`res = {res!r}`',
        'max_time = releaseTimes[0]': '第 0 个键从 0 时刻按下，持续时间就是松开时间 `{max_time}`',
        'for index in range': '看第 `{index}` 个键 `{keysPressed[index]!r}`',
        'delta_time = ': '持续时间 = 本次松开 - 上次松开 = `{releaseTimes[index]} - {releaseTimes[index - 1]}` = =={delta_time}==',
        'if delta_time > max_time': lambda S, B, r: (f'`{S.delta_time} > {S.max_time}`：更久 → 更新' if S.delta_time > S.max_time else (f'时间相同 `{S.delta_time}`，比字典序：`{S.keysPressed[S.index]!r} > {S.res!r}` → 更大则更新' if S.delta_time == S.max_time and S.keysPressed[S.index] > S.res else (f'时间相同，但 `{S.keysPressed[S.index]!r}` 不比 `{S.res!r}` 大 → 不更新' if S.delta_time == S.max_time else f'`{S.delta_time} < {S.max_time}`：更短 → 不更新'))),
        'max_time = delta_time': '最长持续时间更新为 `{max_time}`',
        'res = keysPressed[index]': '答案键更新为 `{res!r}`',
        'return res': '最长持续的键是 `{ret!r}`',
    },
    cards=dict(
        one_liner='每个键的持续时间 = 相邻松开时间之差，打擂台取最长',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`releaseTimes[i]` 是第 `i` 个键松开的时刻，`keysPressed[i]` 是该键',
                 '第 `i` 个键持续时间 = `releaseTimes[i] - releaseTimes[i-1]`（第 0 个从 0 开始）',
                 '返回持续时间最长的键；并列取字典序最大的',
                 '示例：`[12,23,36,46,62]`，`"spuda"` → `"a"`'],
        quote='初始化答案为第0个键，并记录当前最长持续时间为第0个键的松开时间，然后从第1个键开始向后扫描，每次计算当前键松开时间与上一个键松开时间的差值，根据这个差值与当前最长持续时间的大小来更新答案以及当前最长持续时间即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 0 个键直接作为初始答案',
              '从第 1 个键起，用相邻松开时间做差得到持续时间',
              '更久就替换；一样久时比较字符，大的获胜'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：并列时要取字典序更大的键，不是先出现的键',
                 '第 0 个键的持续时间就是 `releaseTimes[0]`',
                 '`index` 从 1 开始才能访问 `index - 1`'],
    ),
)
