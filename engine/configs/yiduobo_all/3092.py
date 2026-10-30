CONFIG = dict(
    num=3092, title='最高频率的 ID', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 + 堆 · remove 计数懒删除',
    tags=['难度分 1793'],
    code='''
class Solution(object):
    def mostFrequentIDs(self, nums, freq):

        heap = []
        res = []
        freq_dict = Counter()
        remove_dict = Counter()
        for v, f in zip(nums, freq):
            if freq_dict[v] > 0:
                remove_dict[(-freq_dict[v], v)] += 1

            while heap and remove_dict[heap[0]] > 0:
                remove_dict[heap[0]] -= 1
                heapq.heappop(heap)

            freq_dict[v] += f
            heapq.heappush(heap, (-freq_dict[v], v))
            if heap:
                res.append(-heap[0][0])
            else:
                res.append(0)
        
        return res
''',
    call='Solution().mostFrequentIDs([2,3,2,1], [3,2,-3,1])',
    expect=[3, 3, 2, 2],
    views=[
        dict(type='map', var='freq_dict', label='freq_dict（ID → 当前频率）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='heap', var='heap', label='heap（小根堆，元素 = (−频率, ID)）', fmt=lambda t: f'{t[0]},{t[1]}', h=180),
        dict(type='map', var='remove_dict', label='remove_dict（待删记录 → 次数）',
             fmt=lambda k, v: f'{k} × {v}', h=150, font=26),
        dict(type='array', var='res', label='res', h=130),
    ],
    watch=['v', 'f', ('堆顶', 'heap[0] if heap else None', 'pink'), ('res', 'res', 'green')],
    captions={
        'freq_dict = Counter': '`freq_dict`：每个 ID 当前的频率',
        'remove_dict = Counter': '`remove_dict`：登记「堆里哪些记录已作废、各作废几条」',
        'for v, f in zip': lambda S, B, r: ('所有操作处理完了' if len(S.res) == len(S.nums) else f'第 {len(S.res)+1} 步：ID `{S.v}` 频率变化 `{S.f}`'),
        'heap = []': '`heap`：小根堆，存 `(-频率, ID)`',
        'res = []': '`res` 收集每步的答案',
        'if freq_dict[v] > 0': lambda S, B, r: (
            f'`{S.v}` 之前频率是 `{S.freq_dict[S.v]}` > 0，堆里有它的旧记录，等会儿要作废'
            if S.freq_dict[S.v] > 0 else f'`{S.v}` 之前频率是 `{S.freq_dict[S.v]}`，堆里没有有效旧记录'),
        'remove_dict[(-freq_dict[v], v)] += 1': '只做登记：旧记录 `({-freq_dict[v]}, {v})` 作废，不去堆里找它',
        'while heap and remove_dict': lambda S, B, r: (
            f'堆顶 `{S.heap[0]}` 已被登记作废 → 弹出' if S.heap and S.remove_dict[S.heap[0]] > 0
            else '堆为空或堆顶没被登记作废 → 堆顶有效，停止'),
        'remove_dict[heap[0]] -= 1': '作废登记用掉一次：`remove_dict[{B.heap[0]}]` = {remove_dict[B.heap[0]]}',
        'heapq.heappop': '弹出作废的旧记录',
        'freq_dict[v] += f': '`{v}` 的频率变成 =={freq_dict[v]}==',
        'heapq.heappush': '新记录 `({-freq_dict[v]}, {v})` 入堆（取负，小根堆堆顶=最高频）',
        'if heap:': lambda S, B, r: ('堆非空：取堆顶' if S.heap else '堆为空：集合里没有元素'),
        'res.append(-heap[0][0])': '堆顶 `{heap[0]}`，取负得最高频率 =={-heap[0][0]}==',
        'res.append(0)': '集合为空，答案 `0`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先登记「谁作废了」，等它浮到堆顶再弹',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每步操作增减某个 ID 的个数，问操作后出现最多的 ID 的次数',
                 '集合为空时答案为 `0`',
                 '示例：`[2,3,2,1]`，`[3,2,-3,1]` → `[3,3,2,2]`'],
        quote='如果操作的id之前出现过，那么就需要先将之前的记录从堆中删掉再将新的记录加入到堆中，为了保证复杂度，在删除时就需要用到懒删除的技巧。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表管频率，堆管最大值',
              '同一个 ID 的新记录入堆前，先在 `remove_dict` 里给旧记录计数 +1',
              '每步入堆前，把堆顶已登记作废的记录弹光，之后堆顶即最高频'],
        summary=['每条记录至多入堆、出堆一次，`O(n log n)`',
                 '堆存 `(-频率, ID)`，靠取负变成大根堆',
                 '对比灵神：灵神直接拿 `cnt` 校验堆顶；这里用 `remove_dict` 显式登记作废记录',
                 '原文为 Python 3 可运行写法，无需修改'],
    ),
)
