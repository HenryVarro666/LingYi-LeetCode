CONFIG = dict(
    num=2332, title='坐上公交的最晚时间', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 二路归并 + 向前避让',
    tags=['灵神题单', '难度分 1841'],
    code='''
class Solution(object):
    def latestTimeCatchTheBus(self, buses, passengers, capacity):

        buses.sort()
        passengers.sort()

        passengers_set = set(passengers)

        p = 0
        for t in buses:
            cnt = 0
            while p < len(passengers) and cnt < capacity and passengers[p] <= t:
                cnt += 1
                p += 1

        if cnt < capacity:
            res = buses[-1]
        else:
            res = passengers[p - 1] - 1
        
        while res in passengers_set:
            res -= 1
        
        return res
''',
    call='Solution().latestTimeCatchTheBus([20,30,10], [19,13,26,4,25,11,21], 2)',
    expect=20,
    views=[
        dict(type='array', var='buses', label='buses（发车时间）', h=190,
             color=lambda S, i, v: 'orange' if S.get('t') == v else None),
        dict(type='array', var='passengers', label='passengers（绿 = 已上车）', h=250,
             pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if i < S.get('p', 0) and 'res' not in S else None),
        dict(type='set', var='passengers_set', label='passengers_set（已被占用的时刻）', h=170, fmt=lambda x: str(x)),
    ],
    watch=['t', 'cnt', ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'buses.sort()': '车按发车时间排序',
        'passengers.sort()': '人按到达时间排序，接下来像二路归并那样对齐',
        'passengers_set = set': '把到达时刻放进集合，后面可以 `O(1)` 判断某时刻有没有人',
        'for t in buses': '下一班车，发车时间 `t = {t}`',
        'cnt = 0': '这班车已载 0 人',
        'while p < len': lambda S, B, r: (f'乘客 `{S.passengers[S.p]}` ≤ `{S.t}` 且还有座位（`{S.cnt}` < `{S.capacity}`）→ ==上车=='
                                          if S.p < len(S.passengers) and S.cnt < S.capacity and S.passengers[S.p] <= S.t
                                          else '车满了，或下一位乘客来不及 → 这班车发车'),
        'cnt += 1': '车上多一人：`cnt = {cnt}`',
        'p += 1': '`p` 指向下一位乘客：{p}',
        'if cnt < capacity': lambda S, B, r: (f'最后一班 `cnt = {S.cnt}` < `{S.capacity}`，没坐满 → 理想时刻是发车时间'
                                              if S.cnt < S.capacity else f'最后一班坐满了 `{S.cnt}` = `{S.capacity}` → 要挤掉最后上车的人'),
        'res = buses[-1]': '没坐满：最理想是==正好发车时==到，`res = {res}`',
        'res = passengers[p - 1] - 1': '坐满了：在最后上车乘客（`{passengers[p - 1]}`）==前一刻==到，`res = {res}`',
        'while res in': lambda S, B, r: (f'`res = {S.res}` 已被别的乘客占用 → 继续往前' if S.res in S.passengers_set
                                         else f'`res = {S.res}` 没人占用 → 就是它'),
        'res -= 1': '让出这个时刻，前一刻：`res = {res}`',
        'return res': '最晚到站时间 `{res}`',
    },
    cards=dict(
        one_liner='理想时刻若被占就往前退，直到没人为止',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['给出各车发车时间、各乘客到达时间和每车容量，先到先上车',
                 '求自己赶上车的最晚到达时刻，不能和别人同时到',
                 '示例：`[20,30,10]`，`[19,13,26,4,25,11,21]`，`capacity=2` → `20`'],
        quote='若最后一趟车没有坐满，那么最理想的情况就是在最后一趟车开车的时间点到达。若最后一趟车坐满了，那么最理想的情况则是恰好把最后一趟车上的最后一名乘客挤下去。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序，用类似二路归并的方式算出每位乘客坐哪班车',
              '看最后一班：没满取发车时刻，满了取最后上车者前一刻',
              '理想时刻可能已有人，所以用集合判断，被占就一直减一'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(m)`（集合）',
                 '乘客时刻 ≥ 2，往前退必然能找到空时刻，不会退到 0 以下',
                 '`cnt` 在每班车开始时清零，循环结束后保存的是最后一班的人数',
                 '对比灵神：灵神用 `j` 边退边比较，不建集合，空间 `O(1)`；本文用集合判重'],
    ),
)
