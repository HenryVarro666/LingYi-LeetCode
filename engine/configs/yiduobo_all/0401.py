def _text(S):
    if 'hour' not in S:
        return '手表有 4 位小时灯、6 位分钟灯：枚举所有时间，用 lowbit 数二进制里 1 的个数'
    s = f"小时 `{S['hour']}` = `{S['hour']:04b}`"
    if 'hour_cnt' in S and S.get('_line', 0) >= 6:
        s += f"（{S['hour_cnt']} 盏）"
    if 'minute' in S and S.get('_line', 0) >= 14:
        s += f"，分钟 `{S['minute']}` = `{S['minute']:06b}`"
    return s


def _lowbit(S):
    if 'tmp' not in S:
        return ''
    t = S['tmp']
    return f"`tmp = {t:b}`：lowbit = `tmp & -tmp` = {t & -t:b}，减掉它就少一个 1" if t else '`tmp = 0`：1 都数完了'


CONFIG = dict(
    num=401, title='二进制手表', difficulty='Easy', category='位运算',
    author='yiduobo', technique='枚举时间 + lowbit 计数',
    tags=[],
    code='''
class Solution(object):
    def readBinaryWatch(self, num):

        res = []
        for hour in range(12):
            hour_cnt = 0
            tmp = hour
            while tmp:
                tmp -= tmp & -tmp
                hour_cnt += 1
            if hour_cnt > num:
                continue
            for minute in range(60):
                minute_cnt = 0
                tmp = minute
                while tmp:
                    tmp -= tmp & - tmp
                    minute_cnt += 1
                if minute_cnt + hour_cnt == num:
                    res.append('%d:%02d' % (hour, minute))

        return res
''',
    call='Solution().readBinaryWatch(1)',
    expect=["0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"],
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='text', fn=_lowbit, h=70),
        dict(type='array', var=lambda S: [int(c) for c in format(S['tmp'], '06b')] if 'tmp' in S else [0] * 6,
             label='tmp 的二进制（每次去掉最低位的 1）', cell=90,
             color=lambda S, i, v: 'yellow' if v else None, h=190),
        dict(type='array', var='res', label='res（已找到的时间）', cell=100, h=150),
    ],
    watch=[('hour', 'hour', 'yellow'), ('minute', 'minute', 'cyan'), ('hour_cnt', 'hour_cnt', 'pink'),
           ('minute_cnt', 'minute_cnt', 'orange')],
    skip=['while tmp', 'hour_cnt = 0', 'minute_cnt = 0'],
    max_steps=70,
    captions={
        'res = []': '`res` 收集合法时间',
        'for hour in range': '枚举小时 `hour = {hour}`',
        'hour_cnt = 0': '`hour_cnt`：这个小时需要亮几盏灯',
        'tmp = hour': '`tmp` 复制一份 `hour`，用来逐个去掉最低位的 1',
        'tmp -= tmp & -tmp': lambda S, B, r: f"`tmp & -tmp` 取出最低位的 1（`{B.tmp & -B.tmp}`），减掉后 `tmp = {S['tmp']}`",
        'hour_cnt += 1': '去掉了一个 1，`hour_cnt` → {hour_cnt}',
        'while tmp': lambda S, B, r: (f"`tmp = {S['tmp']}` 还有 1，继续" if S['tmp'] else "`tmp = 0`：1 数完了"),
        'if hour_cnt > num': lambda S, B, r: (f"`hour_cnt = {S['hour_cnt']} > num = {S['num']}`：光小时就亮多了 → 跳过整个小时" if S['hour_cnt'] > S['num']
                                              else f"`hour_cnt = {S['hour_cnt']} ≤ num = {S['num']}`：还有机会，继续枚举分钟"),
        'continue': '跳过这个小时的所有分钟（剪枝）',
        'for minute in range': '枚举分钟 `minute = {minute}`',
        'minute_cnt = 0': '`minute_cnt` 重新数',
        'tmp = minute': '`tmp = minute`',
        'tmp -= tmp & - tmp': lambda S, B, r: f"`tmp & -tmp` 取出最低位的 1（`{B.tmp & -B.tmp}`），减掉后 `tmp = {S['tmp']}`",
        'minute_cnt += 1': '`minute_cnt` → {minute_cnt}',
        'while tmp:': lambda S, B, r: (f"`tmp = {S['tmp']}` 还有 1，继续" if S['tmp'] else "`tmp = 0`：1 数完了"),
        'if minute_cnt + hour_cnt': lambda S, B, r: (f"`{S['minute_cnt']} + {S['hour_cnt']} = {S['minute_cnt'] + S['hour_cnt']}` "
                                                    + ('== num → 记下' if S['minute_cnt'] + S['hour_cnt'] == S['num'] else f"≠ num = {S['num']} → 跳过")),
        'res.append': "格式化为 `{hour}:{minute:02d}`：分钟补成两位",
        'return res': '一共 `{len(ret)}` 个时间：`{ret}`',
    },
    cards=dict(
        one_liner='不做 DFS：直接枚举所有时间，反推需要亮几盏灯',
        complexity='时间 `O(1)`（常数次枚举），空间 `O(1)`',
        problem=['二进制手表：4 盏灯表示小时（0–11），6 盏灯表示分钟（0–59）',
                 '给定亮灯数 `num`，返回所有可能的时间；分钟必须两位',
                 '示例：`num = 1` → `["0:01","0:02","0:04","0:08","0:16","0:32","1:00","2:00","4:00","8:00"]`'],
        quote='这里可以用dfs去做，不过我的做法是直接枚举可能的所有时间，然后反推出led的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个合法的 hour 或 minute，二进制里 `1` 的数量就是亮灯数',
              '用 lowbit：`tmp & -tmp` 取出最低位的 1，`tmp -= lowbit`，减几次就有几个 1',
              '小时的灯数已经超过 `num` 就整个跳过，省掉 60 次分钟枚举'],
        after=[dict(heading='动画里没演示的部分', lines=['720 次枚举太多，动画只演示了 `hour = 0` 的前面几个分钟，其余快进', '`hour = 3, 5, 6, 7, 9, 10, 11` 灯数 > 1，直接剪枝；`hour = 1, 2, 4, 8` 只有 `minute = 0` 满足', '最终 10 个时间：分钟 1,2,4,8,16,32 加上 `1:00,2:00,4:00,8:00`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：分钟用 `%02d` 补零，小时用 `%d` 不补',
                 '`tmp & -tmp` 就是最低位的 1，是位运算常用技巧',
                 '原文本身是 Python 2/3 通用写法，代码一字未改',
                 '对比灵神：灵神直接 `bit_count()`；yiduobo 手写 lowbit 数 1，并给小时加了剪枝'],
    ),
)
