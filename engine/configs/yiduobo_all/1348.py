def _lst(S):
    d = S.get('self.time_dict')
    if not d:
        return None
    k = S.get('tweetName') or next(iter(d))
    return [f'{t}×{c}' for t, c in d.get(k, [])]


def _info(S):
    if 'freq' not in S or 'res' not in S:
        return ''
    if 'left' in S and 'right' in S:
        return f"区间 `[{S['startTime']}, {S['endTime']}]` 对应下标 `[{S['left']}, {S['right']})`，每 `{S['freq']}` 秒一桶"
    return f"每 `{S['freq']}` 秒一桶，共 `{len(S['res'])}` 桶"


CONFIG = dict(
    num=1348, title='推文计数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按时间有序列表 + 手写二分',
    tags=['设计'],
    code='''
class TweetCounts(object):

    def __init__(self):
        self.time_dict = {}

    def bSearch(self, tweetName, time):
        l = 0
        r = len(self.time_dict[tweetName])
        while l < r:
            mid = (l + r) // 2
            if self.time_dict[tweetName][mid][0] < time:
                l = mid + 1
            else:
                r = mid
        
        return l

    def recordTweet(self, tweetName, time):
        if tweetName not in self.time_dict:
            self.time_dict[tweetName] = [[time, 1]]
        else:
            if time > self.time_dict[tweetName][-1][0]:
                self.time_dict[tweetName].append([time, 1])
            elif time < self.time_dict[tweetName][0][0]:
                self.time_dict[tweetName] = [[time, 1]]+ self.time_dict[tweetName]
            else:
                p = self.bSearch(tweetName, time)
                
                if self.time_dict[tweetName][p][0] == time:
                    self.time_dict[tweetName][p][1] += 1
                else:
                    self.time_dict[tweetName] = self.time_dict[tweetName][:p] + [[time, 1]] + self.time_dict[tweetName][p:]

    def getTweetCountsPerFrequency(self, freq, tweetName, startTime, endTime):
        delta = endTime - startTime + 1
        if freq == 'minute':
            freq = 60
        elif freq == 'hour':
            freq = 3600
        else:
            freq = 86400

        n = delta // freq
        if delta % freq != 0:
            n += 1
        res = [0] * n

        if startTime > endTime:
            return res
        
        if tweetName not in self.time_dict:
            return res

        if startTime > self.time_dict[tweetName][-1][0] or endTime < self.time_dict[tweetName][0][0]:
            return res
        
        if startTime <= self.time_dict[tweetName][0][0]:
            left = 0
        else:
            left = self.bSearch(tweetName, startTime)
        
        if endTime >= self.time_dict[tweetName][-1][0]:
            right = len(self.time_dict[tweetName])
        else:
            right = self.bSearch(tweetName, endTime)

        for index in range(left, right):
            delta = self.time_dict[tweetName][index][0] - startTime
            p = delta // freq
            res[p] += self.time_dict[tweetName][index][1]
        
        return res
''',
    call="""t = TweetCounts()
t.recordTweet('tweet3', 0)
t.recordTweet('tweet3', 60)
t.recordTweet('tweet3', 10)
[t.getTweetCountsPerFrequency('minute', 'tweet3', 0, 59), t.getTweetCountsPerFrequency('minute', 'tweet3', 0, 119)]""",
    expect=[[2], [2, 1]],
    skip=['freq = 3600', 'freq = 86400', 'self.time_dict = {}', 'if startTime > endTime', 'if delta % freq'],
    max_steps=90,
    views=[
        dict(type='array', var=_lst, label="time_dict['tweet3']：按时间排序的 时间×条数（黄 = 刚改动）", cell=110, h=190,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow', 'p': 'purple'},
             window=('left', 'right - 1'), window_color='green'),
        dict(type='array', var='res', label='res：每个时间桶里的推文数', cell=100, h=170,
             pointers={'index': 'orange'}, color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_info, size=26, h=80),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('p', 'p', 'purple'),
           ('left', 'left', 'green'), ('right', 'right', 'green'), ('freq', 'freq', 'cyan')],
    captions={
        'l = 0': '二分区间 `[l, r)`：`l = 0`',
        'r = len': '`r = {r}`：开区间右端，答案可以是末尾',
        'while l < r': lambda S, B, ret: ('`l < r`，继续二分' if S.l < S.r else '`l == r`，找到位置 `{}`'.format(S.l)),
        'mid = ': '取中点 `mid = ({B.l} + {B.r}) // 2 = {mid}`',
        'if self.time_dict[tweetName][mid][0] < time': lambda S, B, ret: (
            '`{}` < `{}` → 目标在右半，`l = mid + 1`'.format(S.time_dict_val, S.time) if False else
            ('第 `mid` 条时间 `{}` < `{}`：太早了，往右找'.format(S['self.time_dict'][S.tweetName][S.mid][0], S.time)
             if S['self.time_dict'][S.tweetName][S.mid][0] < S.time
             else '第 `mid` 条时间 `{}` ≥ `{}`：可能就是它，往左收'.format(S['self.time_dict'][S.tweetName][S.mid][0], S.time))),
        'l = mid + 1': '`l = {l}`',
        'r = mid': '`r = {r}`',
        'return l': '第一个时间 ≥ `{time}` 的下标是 `{l}`',
        'tweetName not in self.time_dict': lambda S, B, ret: ('第一条推文：直接建一个列表' if 'time' in S and S.tweetName not in S['self.time_dict'] else '这个账号已有记录，继续往下查'),
        'time > self.time_dict[tweetName][-1][0]': lambda S, B, ret: ('比最后一条还晚 → ==直接追加到末尾==' if S.time > S['self.time_dict'][S.tweetName][-1][0]
                                                                  else '不比最后一条晚，再看是不是最早的'),
        'time < self.time_dict[tweetName][0][0]': lambda S, B, ret: ('比第一条还早 → ==插到最前面==' if S.time < S['self.time_dict'][S.tweetName][0][0]
                                                                 else '落在中间 → 要二分找位置'),
        'p = self.bSearch': '二分得到插入位置 `p = {p}`',
        '[p][0] == time': lambda S, B, ret: ('这个时间已有记录 → 只把条数 +1' if S['self.time_dict'][S.tweetName][S.p][0] == S.time else '没有这个时间 → 在 `p` 处插入新记录'),
        '[p][1] += 1': '同一时间的条数 +1',
        '[:p] + [[time, 1]]': '把新记录拼在 `p` 位置：`前半 + [[time, 1]] + 后半`',
        'delta = endTime': '查询区间长度 `delta = {endTime} - {startTime} + 1 = {delta}`',
        "freq = 60": "`minute` 对应的桶宽：60 秒（`hour` 3600，`day` 86400）",
        'n = delta // freq': '桶数 = `{delta} // {freq}` = {n}（不能整除时还要 +1 补一个不满的桶）',
        'if delta % freq': lambda S, B, ret: ('不能整除 → 多一个不满的桶，`n += 1`' if S.delta % S.freq else '刚好整除，不用补桶'),
        'res = [0] * n': '准备 `{n}` 个桶，全是 0',
        'if startTime <= self.time_dict[tweetName][0][0]': lambda S, B, ret: ('起点不晚于最早的推文 → `left = 0`' if S.startTime <= S['self.time_dict'][S.tweetName][0][0] else '起点在中间 → 二分找 `left`'),
        'left = self.bSearch': '`left` = 第一个时间 ≥ `startTime` 的下标 = {left}',
        'if endTime >= self.time_dict[tweetName][-1][0]': lambda S, B, ret: ('终点不早于最晚的推文 → `right` = 列表长度' if S.endTime >= S['self.time_dict'][S.tweetName][-1][0] else '终点在中间 → 二分找 `right`'),
        'right = len': '`right = {right}`：全部取到末尾',
        'right = self.bSearch': '`right` = 第一个时间 ≥ `endTime` 的下标 = {right}（右开）',
        'for index in range(left, right)': lambda S, B, ret: ('遍历 `[{}, {})` 内的每条记录'.format(S.left, S.right) if 'index' not in B else '看下一条记录（没有了就结束循环）'),
        'delta = self.time_dict[tweetName][index][0] - startTime': '离起点 `delta = {delta}` 秒',
        'p = delta // freq': '落进第 `{delta} // {freq}` = ==第 {p} 桶==',
        'res[p] +=': '第 `{p}` 桶加上这个时间的条数：`res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每个账号存一个按时间排好序的列表，查询时二分出区间再分桶',
        complexity='记录 `O(n)`（插入要搬数据），查询 `O(log n + k)`',
        problem=['`recordTweet(name, time)` 记录一条推文',
                 '`getTweetCountsPerFrequency(freq, name, start, end)`：按分钟/小时/天分桶，统计 `[start, end]` 内每桶的推文数',
                 '示例：时间 0、60、10，查 `[0,59]` 得 `[2]`，查 `[0,119]` 得 `[2,1]`'],
        quote='高级一点的做法应该是以时间为key，使用平衡二叉树来储存。我在这里采用的低配的做法，即按时间从小到大储存一个list。',
        quote_src='—— yiduobo 题解原文',
        idea=['新推文：先看是不是最晚 / 最早（常见情况免二分），否则二分找插入位置，同一时间只加条数',
              '查询：二分出 `[left, right)`，这一段就是区间内的所有记录',
              '桶下标 = `(time - startTime) // freq`，桶数 = 区间长度向上取整'],
        summary=['记录用手写二分找位置，列表插入 `O(n)`；换平衡树（有序集合）可到 `O(log n)`',
                 '易错：`right` 是开区间端点；`endTime` 包含在内，桶数要向上取整',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`mid`、桶数 `n`、桶下标 `p`）',
                 '两端的边界情况（起点早于最早、终点晚于最晚）直接用 `0` / `len`，省掉二分'],
    ),
)
