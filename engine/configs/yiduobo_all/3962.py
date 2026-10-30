
def _txt(S):
    if 'cnt' not in S or 's' not in S:
        return 'cnt = 已花掉的交换次数；s = 当前子数组和（已交换后）'
    return f'已用交换 `cnt = {S["cnt"]}` / `k = {S["k"]}`　子数组和 `s = {S["s"]}`　最优 `res = {S["res"]}`'


def _col(S, i, v):
    if 'start' not in S or 'index' not in S:
        return None
    if S['start'] <= i <= S['index']:
        return 'green'
    return None


CONFIG = dict(
    num=3962, title='至多 K 次交换后最大子数组和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举子数组 · 两个堆（外部元素 / 已换出元素）',
    tags=['常用数据结构', '难度分 2672'],
    code=r'''
class Solution(object):
    def maxSum(self, nums, k):
        
        mi = min(nums)
        res = max(nums)

        ori_heap = [(-v, index) for index, v in enumerate(nums)] + [(1 - mi, -1)]
        heapq.heapify(ori_heap)

        for start in range(len(nums)):
            rest_heap = ori_heap[:]
            rest_dict = {index: v for index, v in enumerate(nums)}
            swap_heap = [(1 - mi, -1)]
            swap_dict = {}

            now = nums[:]
            cnt = 0
            s = 0

            for index in range(start, len(nums)):
                v = now[index]
                if index in swap_dict:
                    cnt -= 1
                    swap_dict.pop(index)
                else:
                    rest_dict.pop(index)

                while len(rest_heap) > 1 and rest_dict.get(rest_heap[0][1], None) != -rest_heap[0][0]:
                    heapq.heappop(rest_heap)
                while len(swap_heap) > 1 and swap_dict.get(swap_heap[0][1], None) != -swap_heap[0][0]:
                    heapq.heappop(swap_heap)

                swap_v, swap_index = swap_heap[0]
                swap_v = -swap_v
                if swap_v > v:
                    now[index], now[swap_index] = now[swap_index], now[index]
                    heapq.heappop(swap_heap)
                    swap_dict.pop(swap_index)
                    heapq.heappush(swap_heap, (-v, swap_index))
                    swap_dict[swap_index] = v
                    v = swap_v
                
                rest_v, rest_index = rest_heap[0]
                rest_v = -rest_v
                if rest_v > v and cnt + 1 <= k:
                    now[index], now[rest_index] = now[rest_index], now[index]
                    heapq.heappop(rest_heap)
                    rest_dict.pop(rest_index)
                    heapq.heappush(swap_heap, (-v, rest_index))
                    swap_dict[rest_index] = v
                    v = rest_v
                    cnt += 1

                s += v
                res = max(res, s)

        return res
''',
    call='Solution().maxSum([1, -1, 2], 1)',
    expect=3,
    views=[
        dict(type='array', var='now', label='now（交换后的数组，绿框 = 当前子数组 [start, index]）', h=215,
             pointers={'start': 'blue', 'index': 'pink'}, window=('start', 'index')),
        dict(type='map', var='rest_dict', label='rest_dict：本来就在子数组外的元素（下标: 值）', h=105),
        dict(type='map', var='swap_dict', label='swap_dict：被换出去的元素（免费再换）', h=105),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('start', 'start', 'blue'), ('index', 'index', 'pink'), ('v', 'v', 'orange'), ('cnt', 'cnt', 'cyan'), ('s', 's', 'green'), ('res', 'res', 'orange')],
    skip=[4, 5, 7, 8, 11, 12, 13, 14, 16, 17, 18, 21, 28, 30, 33, 34, 37, 38, 39, 40, 41, 43, 44, 47, 48, 49, 50, 51, 24, 25, 23],
    captions={
        10: lambda S, B, r: ('起点都枚举完了' if B.get('start') == S.start else f'枚举起点 `start = {S.start}`：`rest` 装全部元素（都在子数组外），`swap` 为空，`cnt = s = 0`'),
        20: lambda S, B, r: ('这个起点的终点都扩完了' if B.get('index') == S.index else f'终点 `index = {S.index}`：子数组扩到 `[{S.start}, {S.index}]`，要处理 `now[{S.index}] = {S.now[S.index]}`'),
        22: lambda S, B, r: (f'`now[{S.index}]` 是之前被换进来的？' + ('是 → 它回到子数组了，之前那次交换不用付：`cnt` 减一' if S.index in S.swap_dict else '不是 → 它原本就在外面，从 `rest_dict` 里去掉')),
        26: '把 `index` 从 `rest_dict` 去掉（它进入了子数组）',
        29: '`rest_heap` 堆顶已失效（懒删除）→ 弹掉',
        31: '`swap_heap` 堆顶已失效 → 弹掉',
        35: lambda S, B, r: ('还没有被换出的元素，免费交换不可用' if S.swap_index == -1 else f'免费交换：被换出的最大值 `{S.swap_v}` 比 `v = {S.v}` 大吗？' + ('大 → 换' if S.swap_v > S.v else '不大')),
        36: '换！`v` 与 `swap_index` 位置的元素互换，==不花次数==，`v` 变成 {swap_v}',
        45: lambda S, B, r: ('外部已经没有元素可换' if S.rest_index == -1 else f'付费交换：外部最大值 `{S.rest_v}` 比 `v = {S.v}` 大，且 `cnt + 1 <= k`（`{S.cnt} + 1 <= {S.k}`）吗？' + ('可以换' if (S.rest_v > S.v and S.cnt + 1 <= S.k) else '不换')),
        46: '付费交换：`now[index]` 与外部最大值互换，被换出的 `v` 记入 `swap_heap`',
        52: '花了一次：`cnt` → {cnt}',
        54: '`s += v` → =={s}==：当前子数组（已交换）的和',
        55: '`res = max(res, s)` = =={res}==',
        58: '最大子数组和：`{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='换出去的元素再换回来不用再花次数：两个堆分开管',
        complexity='时间 `O(n^2 log n)`，空间 `O(n)`',
        problem=['最多交换 `k` 次（可交换任意两个下标），求交换后的最大子数组和',
                 '`n <= 1500`，可以枚举子数组起点，再向右延伸',
                 '本视频：`[1,-1,2]`，`k=1` → `3`'],
        quote='对于第一类的元素，本次的交换实际上是不需要代价的。……例如数组[2, 1, 5]，start为0：当index为0时，nums[index]为2，此时应该与外部的5进行交换，得到[5, 1, 2]，消耗了一次交换的代价',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举起点 `start`，终点 `index` 往右扩；每次想让 `nums[index]` 换成外面最大的数',
              '换的对象分两类：==之前被换出去的（免费）==；本来就在外面的（要花一次）',
              '`swap_heap` 管前一类，`rest_heap` 管后一类，`cnt` 记已花次数；用懒删除处理失效元素'],
        summary=['时间 `O(n^2 log n)`，空间 `O(n)`',
                 '`nums[index]` 如果本身是被换出去的，说明它回到子数组里：`cnt` 要减一（之前那次交换不用付了）',
                 '先看免费的 `swap_heap`，再看要付费的 `rest_heap`，且 `cnt + 1 <= k`',
                 '原文本身可在 Python 3 运行，未做修改；堆里放 `(-值, 下标)`，堆底放哨兵 `(1 - mi, -1)`',
                 '对照灵神：灵神只换「负数 ↔ 正数」并用树状数组算前 m 小之和；这里用贪心逐个扩展，用堆维护'],
    ),
)
