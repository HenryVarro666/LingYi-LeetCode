CONFIG = dict(
    num=1705, title='吃苹果的最大数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='堆 + 过期日期 + 批量吃',
    tags=['灵神题单', '难度分 1930'],
    code='''
class Solution(object):
    def eatenApples(self, apples, days):

        heap = []
        n = len(apples)
        res = 0
        for index in range(n):
            date = index + 1
            if apples[index] > 0:
                heapq.heappush(heap, [days[index] + date, apples[index]])

            while heap and heap[0][0] <= date:
                heapq.heappop(heap)

            if heap:
                day, apple = heapq.heappop(heap)
                res += 1
                apple -= 1
                if apple > 0:
                    heapq.heappush(heap, [day, apple])

        date = n + 1
        while heap:
            while heap and heap[0][0] <= date:
                heapq.heappop(heap)

            if heap:
                day, apple = heapq.heappop(heap)
                if date + apple - 1 < day:
                    res += apple
                    date += apple
                else:
                    res += day - date
                    date = day

        return res
''',
    call='Solution().eatenApples([1,2,3,5,2], [3,2,1,4,2])',
    expect=7,
    views=[
        dict(type='array', var='apples', pointers={'index': 'blue'}, label='apples（下标 index = 第 index+1 天）', h=170),
        dict(type='heap', var='heap', fmt=lambda x: f'第{x[0]}天过期×{x[1]}', h=200),
        dict(type='text', fn=lambda S: f"现在是第 `{S['date']}` 天，已吃 ==`{S['res']}`== 个" if 'date' in S and 'res' in S else '', h=70),
    ],
    max_steps=90,
    watch=[('date', 'date', 'blue'), ('res', 'res', 'green'), ('堆大小', 'len(heap)', 'yellow')],
    captions={
        'date = index + 1': '下标 `{index}` 对应第 `{date}` 天（天数从 1 开始）',
        'if apples[index] > 0': '第 `{date}` 天 `apples[{index}] = {apples[index]}`，有新苹果才入堆',
        'heapq.heappush(heap, [days[index] + date': '入堆 `[过期日={days[index] + date}, 个数={apples[index]}]`：==过期日早的先吃==',
        'while heap and heap[0][0] <= date': lambda S, B, r: (f'堆顶过期日 `{S.heap[0][0]}` ≤ 今天 `{S.date}` → 已过期，弹出' if S.heap and S.heap[0][0] <= S.date
                                                              else '堆顶没过期（或堆空）→ 不再弹'),
        'if heap:': lambda S, B, r: ('堆不空 → 今天能吃一个' if S.heap else '堆空 → 今天吃不到'),
        'day, apple = heapq.heappop(heap)': '取出堆顶：过期日 `{day}`，剩 `{apple}` 个',
        'res += 1': '吃一个，`res` → =={res}==',
        'apple -= 1': '这批剩 `{apple}` 个',
        'if apple > 0': lambda S, B, r: ('还有剩 → 重新放回堆' if S.apple > 0 else '这批吃完了 → 不放回'),
        'heapq.heappush(heap, [day, apple])': '放回 `[{day}, {apple}]`',
        'date = n + 1': '处理完 `n` 天，没有新苹果了。==堆顶吃完或过期前不用管其他批==，所以可以==一批一批吃==，从第 `{date}` 天起',
        'while heap:': '堆不空就继续',
        'if date + apple - 1 < day': lambda S, B, r: (f'吃完要到第 `{S.date + S.apple - 1}` 天 < 过期日 `{S.day}` → 来得及全吃' if S.date + S.apple - 1 < S.day
                                                       else f'吃完要到第 `{S.date + S.apple - 1}` 天 ≥ 过期日 `{S.day}` → 有些来不及吃'),
        'res += apple': '全吃：`res` += {apple} → =={res}==',
        'date += apple': '日期推进 `{apple}` 天 → 第 `{date}` 天',
        'res += day - date': '只能吃到过期前一天：`day − date` = {B.day - B.date} 个，`res` → =={res}==',
        'date = day': '直接跳到过期日：`date` → {date}',
        'return res': '堆空，一共吃了 `{ret}` 个',
    },
    cards=dict(
        one_liner='先吃过期最早的：堆里放 [过期日, 个数]',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['第 `i` 天长出 `apples[i]` 个苹果，保质期 `days[i]` 天；每天最多吃一个',
                 '求最多吃几个，`n` 天后还可以接着吃',
                 '示例：`apples=[1,2,3,5,2]`，`days=[3,2,1,4,2]` → `7`'],
        quote='由于题目中的苹果都是由保质期的，为了吃到最多的苹果，显然应该先吃掉过期时间最早的苹果，那么一个自然的想法就是使用一个堆来维护当前剩下的苹果。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐天：新苹果入堆 → 弹掉过期的 → 吃堆顶一个，还有剩就放回',
              '`n` 天后不再有新苹果：堆顶吃完或过期之前，==不用考虑其他批==',
              '一批最多吃 `apple` 个；来不及就只吃 `day − date` 个，直接跳到过期日'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '天数从 1 开始：`date = index + 1`，过期日 = `days + date`，过期日当天已不能吃（`<=`）',
                 '`n` 天后的两种情况：来得及全吃，或吃到过期前一天',
                 '对比灵神：灵神原地改堆顶个数；这里弹出再放回'],
    ),
)
