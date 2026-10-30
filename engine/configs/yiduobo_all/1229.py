CONFIG = dict(
    num=1229, title='安排会议日程', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='差分思想 · 起点x2 终点x2+1',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minAvailableDuration(self, slots1, slots2, duration):

        timepoints = []
        for x, y in slots1:
            timepoints.append(x + x)
            timepoints.append(y + y + 1)

        for x, y in slots2:
            timepoints.append(x + x)
            timepoints.append(y + y + 1)

        timepoints.sort()

        cnt = 0
        start = 0
        for t in timepoints:
            if t % 2 == 0:
                cnt += 1
                if cnt == 2:
                    start = t // 2
            else:
                cnt -= 1
                if cnt == 1:
                    if t // 2 - start >= duration:
                        return [start, start + duration]

        return []
''',
    call='Solution().minAvailableDuration([[10,50],[60,120],[140,210]], [[0,15],[60,70]], 8)',
    expect=[60, 68],
    views=[
        dict(type='array', var='timepoints', label='timepoints（偶数 = 区间起点 2x，奇数 = 终点 2y+1）', h=200, cell=90,
             color=lambda S, i, v: ('blue' if 't' in S and 'cnt' in S and v == S['t'] else None)),
        dict(type='text', size=32, h=90, fn=lambda S: (
            f"当前时间点 `{S['t']}` → {'起点' if S['t'] % 2 == 0 else '终点'}，真实时刻 `{S['t'] // 2}`；cnt = =={S['cnt']}== 人有空"
            if 't' in S and 'cnt' in S else '')),
        dict(type='text', size=30, h=80, fn=lambda S: (
            f"两人同时空闲的起点 start = ==`{S['start']}`==，要求至少 `{S['duration']}` 分钟" if 'start' in S and 'duration' in S else '')),
    ],
    watch=[('t', 't', 'blue'), ('cnt', 'cnt', 'orange'), ('start', 'start', 'green'), 'duration'],
    captions={
        'timepoints = []': '把所有区间端点放进 `timepoints`，像差分数组一样扫描',
        'timepoints.append(x + x)': '起点 `{x}` 记成 `{x+x}`（偶数）',
        'timepoints.append(y + y + 1)': '终点 `{y}` 记成 `{y+y+1}`（奇数）：同一时刻==起点排在终点前==，刚好首尾相接的区间也算重叠',
        'timepoints.sort()': '按时间排序，起点和终点混在一起扫',
        'cnt = 0': '`cnt` = 当前有几个人空闲（0、1、2）',
        'start = 0': '`start` 记录最近一次两人同时空闲的起点',
        'for t in timepoints': '扫到时间点 `{t}`',
        'if t % 2 == 0': lambda S, B, r: f'`{S.t} % 2 == 0` → ' + ('偶数，是区间起点，有人空出来' if S.t % 2 == 0 else '奇数，是区间终点，有人忙起来'),
        'cnt += 1': '一个人开始空闲：`cnt` = {cnt}',
        'if cnt == 2': lambda S, B, r: ('`cnt == 2`：两个人都空闲了，从这里开始' if S.cnt == 2 else f'`cnt = {S.cnt}`，还没到两人同时空闲'),
        'start = t // 2': '两人共同空闲从 `{t} // 2 = {start}` 开始',
        'cnt -= 1': '一个人不再空闲：`cnt` = {cnt}',
        'if cnt == 1': lambda S, B, r: ('`cnt` 从 2 回落到 1：共同空闲段结束了' if S.cnt == 1 else f'`cnt = {S.cnt}`，不是从两人同时空闲落下来的，跳过'),
        'if t // 2 - start >= duration': lambda S, B, r: f'共同空闲 `{S.t // 2} − {S.start} = {S.t // 2 - S.start}`，{">=" if S.t // 2 - S.start >= S.duration else "<"} `{S.duration}` → ' + ('够长，答案就是它' if S.t // 2 - S.start >= S.duration else '不够长，继续扫'),
        'return [start': '最早的够长时段：`[{start}, {start + duration}]`',
        'return []': '扫完都没有够长的时段，返回空',
    },
    cards=dict(
        one_liner='把端点排序成一条时间线，cnt 数到 2 才是两人都有空',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个人各有一组互不重叠的空闲时间段 `slots1`、`slots2`',
                 '找出最早的、两人都空闲且长度至少 `duration` 的时间段，返回 `[start, start+duration]`，没有则返回空',
                 '示例：`slots1=[[10,50],[60,120],[140,210]]`，`slots2=[[0,15],[60,70]]`，`duration=8` → `[60,68]`'],
        quote='使用一个变量cnt记录当前空闲的人数，接下来遍历所有出现的时间点。若当前遍历到的是一个区间的起点，那么就将cnt加上1，否则将cnt减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['单人的空闲段互不重叠，所以 `cnt` 最多是 2',
              '起点 `x` 记成 `2x`，终点 `y` 记成 `2y+1`，排序后同一时刻起点在前',
              '`cnt` 到 2 记下 start，从 2 回落到 1 时检查这一段够不够长'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '原文为 Python 2 写法，`t / 2` 是整数除法，已改为 `t // 2`',
                 '返回的是 `[start, start + duration]`，不是共同空闲段的终点',
                 '同一个人的区间不重叠，`cnt == 2` 才一定是两个人各一个'],
    ),
)
