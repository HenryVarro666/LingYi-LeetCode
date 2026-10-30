CONFIG = dict(
    num=1488, title='避免洪水泛滥', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 · 堆维护最近泛滥时间',
    tags=['灵神题单', '常用数据结构', '难度分 1974'],
    code='''
class Solution(object):
    def avoidFlood(self, rains):

        n = len(rains)
        rain_dict = {}
        next_rain = [-1] * n
        for index, num in enumerate(rains):
            if num > 0:
                if num in rain_dict:
                    next_rain[rain_dict[num]] = index
                rain_dict[num] = index
        
        heap = []
        res = []
        rain_set = set()
        for index, num in enumerate(rains):
            if num == 0:
                if heap:
                    deal = heapq.heappop(heap)
                    rain_set.remove(rains[deal])
                    res.append(rains[deal])
                else:
                    res.append(1)
            else:
                res.append(-1)
                if num in rain_set:
                    return []
                if next_rain[index] != -1:
                    rain_set.add(num)
                    heapq.heappush(heap, next_rain[index])
        
        return res
''',
    call='Solution().avoidFlood([1,2,0,0,2,1])',
    expect=[-1, -1, 2, 1, -1, -1],
    views=[
        dict(type='array', var='rains', pointers={'index': 'blue'}, label='rains（黄 = 晴天）', h=170,
             color=lambda S, i, v: 'blue' if i == S.get('index') else ('yellow' if v == 0 else None)),
        dict(type='array', var='next_rain', label='next_rain（该湖下次下雨日，-1 = 不再下）', h=130),
        dict(type='heap', var='heap', fmt=lambda d: f'第{d}天', label='heap（下次下雨日，小的在堆顶）', h=150),
        dict(type='set', var='rain_set', label='rain_set（有水的湖）', h=90),
        dict(type='array', var='res', label='res', h=110, color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=['index', 'num', 'deal'],
    captions={
        'next_rain = [-1]': '先扫一遍，求出每次下雨之后，那个湖==下一次==下雨的日子',
        'next_rain[rain_dict[num]] = index': '湖 `{num}` 上次下雨在第 `{rain_dict[num]}` 天，下一次就是第 `{index}` 天：`next_rain[{rain_dict[num]}] = {index}`',
        'rain_dict[num] = index': '更新湖 `{num}` 最近一次下雨日为 `{index}`',
        'heap = []': '第二遍扫描。堆里放「有水湖的下次泛滥时间」，抽水总是抽==最快要泛滥==的',
        'if num == 0': lambda S, B, r: (f'第 `{S.index}` 天晴天，可以抽水' if S.num == 0 else f'第 `{S.index}` 天湖 `{S.num}` 下雨'),
        'if heap': lambda S, B, r: ('堆不空：有湖装着水，抽下次泛滥最近的那个' if S.heap else '堆是空的：没有湖有水，随便抽一个'),
        'deal = heapq.heappop': '弹出堆顶 `{deal}`：它对应湖 `rains[{deal}] = {rains[deal]}`，是最近要泛滥的',
        'rain_set.remove': '湖 `{rains[deal]}` 被抽干，从有水集合移除',
        'res.append(rains[deal])': '这天抽湖 `{rains[deal]}`：`res` 追加',
        'res.append(1)': '没有湖有水，抽湖 `1`（空湖抽了也无事发生）',
        'res.append(-1)': '雨天答案固定 `-1`',
        'if num in rain_set': lambda S, B, r: (f'湖 `{S.num}` 已经有水又下雨 → 洪水，返回空数组' if S.num in S.rain_set
                                               else f'湖 `{S.num}` 目前是空的，不会泛滥'),
        'if next_rain[index] != -1': lambda S, B, r: (f'`next_rain[{S.index}] = {S.next_rain[S.index]}`：以后还会再下雨，需要抽水'
                                                      if S.next_rain[S.index] != -1 else '以后不再下雨，不用抽它，也不放进堆'),
        'rain_set.add(num)': '湖 `{num}` 装满了水：加入有水集合',
        'heapq.heappush': '把「下次下雨日」`{next_rain[index]}` 压入堆，堆顶永远是最紧迫的',
        'return res': '没有洪水，方案 `{res}`',
    },
    cards=dict(
        one_liner='每次抽水，抽下一次泛滥时间最近的那个湖',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['下雨日湖会装满，已满再下雨即洪水；晴天可抽干任意一个湖',
                 '给出每天的操作 `res`（雨天 `-1`），无解返回 `[]`',
                 '示例：`[1,2,0,0,2,1]` → `[-1,-1,2,1,-1,-1]`'],
        quote='对于每次抽水，都应该抽一个泛滥时间最近的湖泊，于是可以使用一个堆来维护当前有水的湖泊下一次泛滥的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍算 `next_rain`：每个湖下一次下雨是哪天',
              '再扫一遍：雨天把「下次下雨日」入堆；晴天弹堆顶抽水',
              '雨天遇到集合里已有的湖就是洪水'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '不再下雨的湖不入堆，省得浪费抽水机会',
                 '堆里放的是==日期==，通过 `rains[日期]` 还原成湖号',
                 '对比灵神：他倒过来「每个要再下雨的湖找前面最早的空晴天」，yiduobo 是晴天时选最紧迫的湖',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
