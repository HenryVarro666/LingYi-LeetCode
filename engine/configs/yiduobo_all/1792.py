def _total(S):
    h = S.get('heap')
    if not h or 'index' not in S and S.get('_line', 0) < 8:
        return ''
    t = sum(x[1] * 1.0 / x[2] for x in h)
    return f'堆里各班通过率之和 = `{t:.4f}`，堆顶 = ==提升最大==的班级 `{h[0][1]}/{h[0][2]}`'


CONFIG = dict(
    num=1792, title='最大平均通过率', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 + 堆（先推导提升递减）',
    tags=['堆（优先队列）', '难度分 1818'],
    code='''
class Solution(object):
    def maxAverageRatio(self, classes, extraStudents):

        heap = []
        for p, t in classes:
            heap.append([-((p + 1.0) / (t + 1.0) - p * 1.0 / t), p, t])
        heapq.heapify(heap)
        for index in range(extraStudents):
            rate, p, t = heapq.heappop(heap)
            p += 1
            t += 1
            heapq.heappush(heap, [-((p + 1.0) / (t + 1.0) - p * 1.0 / t), p, t])
 
        s = 0
        for rate, p, t in heap:
            s += p * 1.0 / t
        return s / len(heap)
''',
    call='Solution().maxAverageRatio([[2,4],[3,9],[4,5],[2,10]], 4)',
    expect=0.53485,
    result_fn=lambda r: round(r, 5),
    views=[
        dict(type='text', fn=_total, h=70),
        dict(type='heap', var='heap', fmt=lambda x: f'{x[1]}/{x[2]}', label='heap（格内 = 通过/总数；按「−提升」排序）', h=200),
    ],
    watch=[('p', 'p', 'blue'), ('t', 't', 'pink'), ('rate', 'rate', 'orange'), ('s', 's', 'green')],
    captions={
        'for p, t in classes': '逐个班级算出「再加 1 个学生」的提升，准备入堆',
        'heap.append': '提升 = `(p+1)/(t+1) − p/t`，==取负数==存入，让最小堆的堆顶成为提升最大的班级',
        'heapq.heapify': '堆化：堆顶 = 当前提升最大的班级',
        'for index in range': '每个额外学生都要选一个班：==提升最大的那个==（同班提升越来越小，所以不会有「先铺垫再暴涨」）',
        'heappop': '弹出堆顶：班级 `{p}/{t}` 提升最大（−提升 = `{rate:.4f}`），这个学生就分给它',
        'p += 1': '分来一个必过学生：`p` → {p}',
        't += 1': '`t` → {t}，该班变成 `{p}/{t}`',
        'heappush': '重新算它的下一次提升（比刚才小），==压回堆里==，堆自动重排',
        's += p': '累加通过率：`s` = {s:.4f}',
        'return s': '平均通过率 = `{s:.4f} / {len(heap)}` = =={ret:.5f}==',
    },
    cards=dict(
        one_liner='提升越来越小 → 每个学生贪心地给「提升最大」的班',
        complexity='时间 `O((n + k) log n)`，空间 `O(n)`',
        problem=['每个班 `[通过人数, 总人数]`，再来 `extraStudents` 个必过学生，任意分配',
                 '求平均通过率的最大值',
                 '示例：`[[2,4],[3,9],[4,5],[2,10]]`，4 人 → ==0.53485=='],
        quote='对于同一个班级而言，越往里面加入学生，对通过率的提升率是越小的。……每次都选择一个学生，加入到通过率提升最大的那个班级。',
        quote_src='—— yiduobo 题解原文',
        idea=['设一个班 `x/y`：加 1 人提升 `(y−x)/(y(y+1))`，再加 1 人提升 `(y−x)/((y+1)(y+2))`',
              '前者分母更小 → ==提升严格递减==，所以贪心成立',
              '用堆维护各班当前提升：弹出最大 → 加人 → 重算 → 压回'],
        summary=['时间 `O((n + k) log n)`，k = extraStudents',
                 '提升取负数入堆：`heapq` 是最小堆',
                 '`1.0` 强制浮点除法，防止整数除法截断（Python 2 的坑）；Python 3 里写法无需修改',
                 '对比灵神：灵神每步用 `heapreplace`，并给出不用浮点数的交叉相乘比较；这里是 pop + push'],
    ),
)
