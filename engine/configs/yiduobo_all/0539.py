CONFIG = dict(
    num=539, title='最小时间差', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='转分钟 + 集合扫描',
    code='''
class Solution(object):
    def findMinDifference(self, timePoints):

        time_set = set()
        for time in timePoints:
            hour, minute = time.split(':')
            tmp = int(hour) * 60 + int(minute)
            if tmp in time_set:
                return 0
            time_set.add(tmp)

        first_time = 0
        while first_time not in time_set:
            first_time += 1
        
        now = first_time
        res = 1440
        for time in range(first_time + 1, 1441):
            if time in time_set:
                res = min(res, time - now)
                now = time

        return min(res, first_time + 1440 - now)
''',
    call="Solution().findMinDifference(['23:59', '00:00', '12:30', '06:10'])",
    expect=1,
    views=[
        dict(type='array', var='timePoints', label='timePoints', h=170, cell=110),
        dict(type='set', var='time_set', label='time_set（分钟数）', h=190, fmt=lambda x: str(x)),
        dict(type='text', size=32, h=120, fn=lambda S: (f"扫描 `time` = {S['time']}，上一个时间 `now` = {S['now']}，当前最小差 `res` = =={S['res']}==" if 'res' in S and 'now' in S and isinstance(S.get('time'), int) else '')),
    ],
    watch=['tmp', 'first_time', 'now', ('res', 'res', 'green'), 'time'],
    captions={
        'hour, minute': '拆出时分：`{hour}` 时 `{minute}` 分',
        'tmp = int(hour)': '换算成分钟：`{hour}×60 + {minute}` = =={tmp}==（一天最多 1440 种）',
        'if tmp in time_set': '`{tmp}` 已出现过？{"是 → 有两个相同时间，差为 0" if tmp in time_set else "没有，继续"}',
        'return 0': '出现重复时间，最小差直接是 `0`',
        'time_set.add': '`{tmp}` 加入集合',
        'while first_time not in time_set': '从 0 开始找最早的时间：`first_time` = {first_time}，在集合里吗？{"是，停" if first_time in time_set else "否，继续加 1"}',
        'first_time += 1': '`{first_time - 1}` 不在集合，试 `{first_time}`',
        'now = first_time': '最早的时间是 `{first_time}`，作为“上一个时间” `now`',
        'res = 1440': '`res` 初值设成一天的分钟数 1440',
        'if time in time_set': '`{time}` 在集合里吗？{"是 → 和上一个时间比较" if time in time_set else "否，下一个"}',
        'res = min(res, time - now)': '和前一个时间的差 `{time} − {now}` = {time - now}，`res` 取较小 → =={res}==',
        'now = time': '`now` 更新为 `{time}`，继续往后',
        'return min': '还要比较跨天：最晚 `{now}` 和第二天最早 `{first_time}+1440` 的差 `{first_time + 1440 - now}`，取小 → =={ret}==',
    },
    skip=['time_set = set()', 'for time in range(first_time'],
    max_steps=70,
    cards=dict(
        one_liner='一天只有 1440 分钟，转成数字后线性扫描相邻差',
        complexity='时间 `O(n + 1440)`，空间 `O(n)`',
        problem=['给一组 `"HH:MM"` 时间，求任意两个时间的最小分钟差',
                 '时间是循环的：`23:59` 与次日 `00:00` 差 1 分钟',
                 '本视频：`["23:59","00:00","12:30","06:10"]` → `1`'],
        quote='用hour * 60 + minute来表示hour:minute这个时间，将timePoints中的所有时间转换为这个形式，用一个set储存起来。在转换的过程中，如果发现有相同的时间出现，那么直接返回0即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['最多 1440 个不同时间，用集合去重，重复直接返回 0',
              '从 0 往后扫，相邻两个时间之差取最小',
              '最后别忘了头尾：最大时间到次日最小时间，差为 `first + 1440 − now`'],
        summary=['时间 `O(n + 1440)`，空间 `O(n)`',
                 '易错：忘记跨天比较，会漏掉 `23:59` 与 `00:00`',
                 '`n > 1440` 时必有重复，会在第一个循环里提前返回 0',
                 '原文本身是 Python 3 可运行的，代码未改动'],
    ),
)
