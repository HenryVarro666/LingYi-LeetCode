import time as _t


def _fmt(t):
    return _t.strftime('%Y:%m:%d:%H:%M:%S', _t.localtime(t))


def _range_txt(S):
    if 'st' in S and 'et' in S:
        return f"补齐后的区间：`{_fmt(S['st'])}` ~ `{_fmt(S['et'])}`"
    if 'p' in S:
        return f"granularity = `{S['granularity']}` → 保留前 `{S['p'] + 1}` 段，后面起点补最小、终点补最大"
    return '日志按时间戳比较；区间两端先按 granularity 补齐'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    logs = S.get('self.log_list', [])
    cv.text((x0 + 18, y0 + 4), 'log_list（绿 = 区间内，红 = 区间外，黄 = 正在比较）', 22, T['muted'], bold=True)
    st, et = S.get('st'), S.get('et')
    cur = S.get('t') if 'res' in S else None
    cur_id = S.get('id') if 'res' in S else None
    res = S.get('res', [])
    rh = 74
    y = y0 + 56
    for t, i in logs:
        inr = st is not None and et is not None and st <= t <= et
        fill = T['panel2']
        out = T['border']
        if cur is not None and t == cur and i == cur_id and S.get('_line') in range_lines:
            out = T['yellow']
        elif st is not None and et is not None and 'res' in S and i in res:
            out = T['green']
        elif st is not None and et is not None and 'res' in S and cur is not None and S.get('_line') in range_lines:
            out = T['border']
        cv.rect((x0 + 24, y, x1 - 24, y + rh - 10), fill=fill, r=10, outline=out, width=4 if out != T['border'] else 2)
        cv.text((x0 + 48, y + (rh - 10) / 2), f'id = {i}', 28, T['text'], anchor='lm', bold=True, mono=True)
        cv.text((x0 + 220, y + (rh - 10) / 2), _fmt(t), 28, T['green'] if (st is not None and 'res' in S and inr) else (T['red'] if (st is not None and 'res' in S) else T['text']), anchor='lm', mono=True)
        if st is not None and 'res' in S:
            cv.text((x1 - 48, y + (rh - 10) / 2), '在区间内' if inr else '不在区间内', 24, T['green'] if inr else T['red'], anchor='rm', bold=True)
        y += rh
    if not logs:
        cv.text((x0 + 30, y0 + 70), '（还没有日志）', 26, T['dim'])
    if 'res' in S:
        cv.text((x0 + 30, y + 14), f"res = {res}", 30, T['green'], bold=True, mono=True)


range_lines = (38, 39, 40)

CONFIG = dict(
    num=635, title='设计日志存储系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='暴力扫描 + 按粒度补齐时间',
    tags=[],
    code='''
import time

class LogSystem(object):

    def __init__(self):
        self.log_list = []
        self.small_month = set(['04', '06', '09', '11'])
        self.cut_pos = {'Year': 0, 'Month': 1, 'Day': 2, 'Hour': 3, 'Minute': 4, 'Second': 5}

    def put(self, id, timestamp):
        t = time.mktime(time.strptime(timestamp, '%Y:%m:%d:%H:%M:%S'))
        self.log_list.append([t, id])

    def retrieve(self, start, end, granularity):

        start_parts = start.split(':')
        end_parts = end.split(':')

        min_list = ['01', '01', '00', '00', '00']
        max_list = ['12', '31', '23', '59', '59']

        if end_parts[1] == '02':
            y = int(end_parts[0])
            if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
                max_list[1] = '29'
            else:
                max_list[1] = '28'
        elif end_parts[1] in self.small_month:
            max_list[1] = '30'

        p = self.cut_pos[granularity]

        st = time.mktime(time.strptime(':'.join(start_parts[:p + 1] + min_list[p:]), '%Y:%m:%d:%H:%M:%S'))
        et = time.mktime(time.strptime(':'.join(end_parts[:p + 1] + max_list[p:]), '%Y:%m:%d:%H:%M:%S'))
        

        res = []
        for t, id in self.log_list:
            if st <= t <= et:
                res.append(id)
        return res
        
''',
    call='''l = LogSystem()
l.put(1, "2017:01:01:23:59:59")
l.put(2, "2017:01:01:22:59:59")
l.put(3, "2016:01:01:00:00:00")
out = [l.retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Year"), l.retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Hour")]
out''',
    expect=[[1, 2, 3], [1, 2]],
    views=[
        dict(type='text', fn=_range_txt, size=26, h=80),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=['granularity', 'p', ('res', 'res', 'green')],
    max_steps=110,
    captions={
        6: '日志列表：每条存 `[时间戳, id]`',
        7: '30 天的月份：4、6、9、11 月',
        8: '粒度 → 要保留前几段：`Year` 保留 1 段，`Second` 保留 6 段',
        11: '`{timestamp}` 转成时间戳 `{int(t)}`，以后直接比大小',
        'self.log_list.append': '存入 `[时间戳, {id}]`',
        'start_parts = start.split': '起点拆成 6 段：`{start_parts}`',
        'end_parts = end.split': '终点拆成 6 段：`{end_parts}`',
        'min_list =': '起点补齐用最小值：月 01、日 01、时分秒 00',
        'max_list =': '终点补齐用最大值：月 12、日 31、时 23、分秒 59',
        "if end_parts[1] == '02'": lambda S, B, r: '终点是 2 月：日的最大值取决于是否闰年' if S.end_parts[1] == '02' else '终点不是 2 月 → 先不用考虑闰年',
        'y = int': '年份 `{y}`',
        'if y % 400': '闰年判定：被 400 整除，或被 4 整除但不被 100 整除',
        "max_list[1] = '29'": '闰年 2 月最多 29 天',
        "max_list[1] = '28'": '平年 2 月最多 28 天',
        'elif end_parts[1] in': lambda S, B, r: ('终点月份 `{}` 是小月：最大日改成 30'.format(S.end_parts[1]) if S.end_parts[1] in S['self.small_month']
                                                 else '`{}` 月是大月，最大日保持 31'.format(S.end_parts[1])),
        "max_list[1] = '30'": '小月最多 30 天',
        'p = self.cut_pos': '粒度 `{granularity}` → `p = {p}`：保留前 `{p + 1}` 段',
        33: lambda S, B, r: '起点：前 {} 段不变，后面补最小值 → `{}`'.format(S.p + 1, _fmt(S.st)),
        34: lambda S, B, r: '终点：前 {} 段不变，后面补最大值 → `{}`'.format(S.p + 1, _fmt(S.et)),
        'res = []': '结果列表，从头扫描所有日志',
        'for t, id in self.log_list': lambda S, B, r: '取一条日志：`id = {}`，时间 `{}`'.format(S.id, _fmt(S.t)),
        'if st <= t <= et': lambda S, B, r: ('`{}` 落在区间内 → 命中'.format(_fmt(S.t)) if S.st <= S.t <= S.et
                                             else '`{}` 超出区间 → 跳过'.format(_fmt(S.t))),
        'res.append(id)': '`id {id}` 加入结果：`{res}`',
        'return res': lambda S, B, r: '返回命中的 id：`{}`'.format(r),
    },
    cards=dict(
        one_liner='按粒度把区间两端补齐成完整时间，再逐条比时间戳',
        complexity='`put` 为 `O(1)`，`retrieve` 为 `O(n)`',
        problem=['`put(id, timestamp)` 存日志，时间格式 `Year:Month:Day:Hour:Minute:Second`',
                 '`retrieve(start, end, granularity)`：只比较到该粒度，返回区间内日志 id',
                 '示例：粒度 `Year` 会忽略月日时分秒，整年都算'],
        quote='在确定了精确到哪一级之后，可以将 start_time 在这一级之后的时间都置为最小时间，将 end_time 在这一级之后的时间都置为最大时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，直接 `O(n)` 暴力扫描，不必上平衡树',
              '起点补最小（`01 01 00 00 00`），终点补最大（`12 31 23 59 59`）',
              '终点日期的最大值要看月份：小月 30 天，2 月看闰年'],
        summary=['`put` `O(1)`，`retrieve` `O(n)`，空间 `O(n)`',
                 '易错：粒度之后的段，起点补最小、终点补最大，别搞反',
                 '易错：终点是 2 月要判闰年，小月（4、6、9、11）最大日是 30',
                 '时间戳用 `time.mktime` 转换，比较就是比数字'],
    ),
)
