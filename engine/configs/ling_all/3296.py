CONFIG = dict(
    num=3296, title='移山所需的最少秒数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='最小堆模拟',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1850'],
    code='''
class Solution:
    def minNumberOfSeconds(self, mountainHeight: int, workerTimes: List[int]) -> int:
        h = [(t, t, t) for t in workerTimes]
        heapify(h)

        for _ in range(mountainHeight):
            # 工作后总用时，当前工作（山高度降低 1）用时，workerTimes[i]
            total, cur, base = h[0]
            heapreplace(h, (total + cur + base, cur + base, base))
        return total  # 最后一个出堆的 total 即为答案
''',
    call='Solution().minNumberOfSeconds(4, [2, 1, 1])',
    expect=3,
    views=[
        dict(type='array', var='workerTimes', label='workerTimes（每个工人降低 1 米要的秒数 base）', h=170),
        dict(type='heap', var='h', label='h：(总用时, 当前一米用时, base)',
             fmt=lambda x: f'{x[0]},{x[1]},{x[2]}', h=330),
        dict(type='text', h=110, fn=lambda S: (
            f"本轮选中堆顶：`total = {S['total']}`，干完这一米后他的总用时变成 ==`{S['total'] + S['cur'] + S['base']}`==，下一米要 `{S['cur'] + S['base']}` 秒"
            if 'cur' in S and 'base' in S else '')),
    ],
    watch=[('total', 'total', 'green'), 'cur', 'base'],
    skip=['h = [(t'],
    captions={
        'heapify': '堆元素 `(total, cur, base)`：`h` = =={h}==；按 `total` 排序，堆顶是「谁干完下一米最早」',
        'for _ in range': '山还有一米要降：选「干完这一米后总用时最短」的工人（按事件发生顺序模拟）',
        'total, cur, base = h[0]': '看堆顶：这个工人干完这一米时，全队已经过了 ==`{total}`== 秒（`cur = {cur}`，`base = {base}`）',
        'heapreplace': '他降下这一米后，下一米更慢：`cur` 变成 `{B.cur} + {B.base} = {B.cur + B.base}`，总用时变成 `{B.total + B.cur + B.base}`；`heapreplace` 弹出旧堆顶并压入新值',
        'return total': '最后一次弹出的 `total` = ==`{total}`==：山降到 0 的那一刻就是答案（所有人同时干活，取事件发生的时刻）',
    },
    cards=dict(
        one_liner='工人同时干活：每一米交给「最早干完」的人，按事件顺序模拟',
        complexity='时间 `O(mountainHeight log n)`，空间 `O(n)`',
        problem=['`workerTimes[i]` = 工人 i 降 1 米要的秒数，降 `x` 米要 `t·(1+2+…+x)` 秒',
                 '所有人同时开工，总时间 = 最慢的那个人，求把山降到 0 的最少秒数',
                 '示例：`mountainHeight = 4, workerTimes = [2,1,1]` → `3`'],
        quote='循环 mountainHeight 次，每次选一个「工作后总用时」最短的工人，把山的高度降低 1。注意工人们是同时工作的，这个算法不是贪心，是按照事件发生顺序的模拟。',
        quote_src='—— 灵茶山艾府题解 方法一',
        idea=['堆里存 `(总用时, 当前一米用时, base)`，堆顶就是下一个完成工作的人',
              '每次完成一米，该工人的下一米要多花 `base` 秒：`cur + base`',
              '山降到 0 的那一刻，最后弹出的 `total` 就是答案'],
        summary=['时间 `O(mountainHeight log n)`，空间 `O(n)`',
                 '不是贪心：是按事件发生顺序模拟，不用「把活平均分」',
                 '`heapreplace` 比 pop + push 更快；返回的是最后一次取出的 `total`',
                 '灵神方法二：二分答案 + 开平方算每人最多降几米，`O(n log U)`，山很高时更快'],
    ),
)
