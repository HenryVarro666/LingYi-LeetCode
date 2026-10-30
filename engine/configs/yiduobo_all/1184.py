def _win(S):
    a, b = S.get('start'), S.get('destination')
    if a is None or b is None or a > b or a == b:
        return None
    return (a, b - 1)


def _color(S, i, v):
    a, b = S.get('start'), S.get('destination')
    if a is None or b is None or a > b:
        return None
    return 'green' if a <= i < b else 'orange'


def _text(S):
    s = S.get('s')
    if not s or len(s) < len(S['distance']) + 1:
        return '前缀和 `s[k]` = 前 k 条边的距离之和，区间和 = `s[右] − s[左]`'
    if 'res' not in S:
        return f'`s[-1] = {s[-1]}` 是整圈的总长'
    a, b, r = S['start'], S['destination'], S['res']
    return f'顺时针 `s[{b}] − s[{a}] = {s[b]} − {s[a]} = {r}`；逆时针 `{s[-1]} − {r} = {s[-1] - r}`'


CONFIG = dict(
    num=1184, title='公交站间的距离', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='前缀和 · 静态区间和',
    code='''
class Solution(object):
    def distanceBetweenBusStops(self, distance, start, destination):

        s = [0]
        for index in range(len(distance) - 1):
            s.append(s[-1] + distance[index])
        s.append(s[-1] + distance[-1])

        if start > destination:
            start, destination = destination, start

        res = s[destination] - s[start]
        return min(res, s[-1] - res)
''',
    call='Solution().distanceBetweenBusStops([1,2,3,4,5,6], 5, 1)',
    expect=7,
    views=[
        dict(type='text', fn=_text, h=70, size=26),
        dict(type='array', var='distance', label='distance（绿 = start→destination 顺时针段，橙 = 另一边）',
             cell=90, color=_color, window=('start', 'destination-1'), h=210),
        dict(type='array', var='s', label='s：前缀和数组', cell=90,
             pointers={'start': 'blue', 'destination': 'pink'}, h=220),
    ],
    watch=[('start', 'start', 'blue'), ('destination', 'destination', 'pink'), ('res', 'res', 'green')],
    captions={
        's = [0]': '前缀数组 `s`，`s[0] = 0` 表示前 0 条边的和',
        'for index': lambda S, B, r: (f'`index = {S.index}`：把第 `{S.index}` 条边加进前缀和' if S.index != B.get('index')
                                      else '循环到 `n-2` 结束，最后一条边留到循环外加'),
        's.append(s[-1] + distance[index])': '`s[{index + 1}] = s[{index}] + distance[{index}]` = =={s[-1]}==',
        's.append(s[-1] + distance[-1])': '最后一条边单独加：`s[-1] = {s[-1]}` 就是==整圈总长==',
        'if start > destination': lambda S, B, r: (f'`start = {S.start} > destination = {S.destination}`：不妨设 start 较小，交换'
                                                   if S.start > S.destination else f'`start = {S.start} ≤ destination = {S.destination}`，不用交换'),
        'start, destination =': '交换后 `start = {start}`，`destination = {destination}`',
        'res = ': '顺时针 `s[{destination}] − s[{start}] = {s[destination]} − {s[start]}` = =={res}==',
        'return min': '逆时针走过剩余所有边：`s[-1] − res = {s[-1]} − {res} = {s[-1] - res}`，取较小值 → =={ret}==',
    },
    cards=dict(
        one_liner='静态区间和：前缀数组一减，另一个方向用总长减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['环形公交线路，`distance[i]` 是相邻两站间的距离',
                 '求 `start` 到 `destination` 的最短距离（顺时针或逆时针）',
                 '本视频：`[1,2,3,4,5,6]`，5 → 1 → `7`'],
        quote='静态区间和的问题，依然是利用前缀数组来解决。……逆时针的情况则是走过了剩余的所有边，因此是pre[-1] - (pre[destination] - pre[start])，取二者的较小值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['这是==静态区间和==，先建前缀数组 `s`',
              '设 `start < destination`，顺时针 = `s[destination] − s[start]`',
              '逆时针 = 整圈 `s[-1]` 减去顺时针'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`start > destination` 要先交换，否则区间和为负',
                 '前缀和 `s` 长度是 `n+1`，`s[-1]` 即整圈总长',
                 '对比灵神：灵神直接 `sum` 切片，`O(1)` 空间；这里建前缀和，适合多次询问'],
    ),
)
