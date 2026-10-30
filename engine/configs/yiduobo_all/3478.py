CONFIG = dict(
    num=3478, title='选出和最大的 K 个元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 大小为 k 的小顶堆',
    tags=['堆（优先队列）', '难度分 1753'],
    code='''
class Solution(object):
    def findMaxSum(self, nums1, nums2, k):
        
        n = len(nums1)
        res = [0] * n
        heap = []
        s = 0

        info = sorted(enumerate(nums1), key=lambda d:d[1])
        p = 0
        while p < len(info):
            q = p
            while q < len(info) and info[p][1] == info[q][1]:
                res[info[q][0]] = s
                q += 1

            for index in range(p, q):
                heapq.heappush(heap, nums2[info[index][0]])
                s += nums2[info[index][0]]
                if len(heap) > k:
                    s -= heapq.heappop(heap)

            p = q
        
        return res
''',
    call='Solution().findMaxSum([4,2,2,5,3], [10,20,30,40,50], 2)',
    expect=[80, 0, 0, 80, 50],
    views=[
        dict(type='text', fn=lambda S: (f"当前一组：info[{S['p']}..{S.get('q', S['p'])-1 if S.get('q', S['p']) > S['p'] else S['p']}]，值 = {S['info'][S['p']][1]}；堆内和 `s` = =={S['s']}==" if 'info' in S and S['p'] < len(S['info']) else '')),
        dict(type='array', var='[f"{v}@{j}" for j, v in info]', pointers={'p': 'blue', 'q': 'pink'}, cell=110, h=220, label='info = (下标, nums1) 按值排序，显示 值@下标'),
        dict(type='heap', var='heap', fmt=lambda x: str(x), h=150, label='heap：大小至多 k 的小顶堆'),
        dict(type='array', var='res', h=150, label='res'),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('s', 's', 'yellow'), ('k', 'k', 'purple')],
    captions={
        'info = sorted': '把 nums1 的值和下标做成二元组，按值排序：==排在前面的都不大于当前值==',
        'while p < len': '`p = {p}`：处理下一组相同值' ,
        'q = p': '从 `p` 开始找这一组相同值的结尾',
        'while q < len': lambda S, B, r: (f'`info[p][1] = {S.info[S.p][1]}` 与 `info[q][1]` 相等 → 继续扩展这一组' if S.q < len(S.info) and S.info[S.p][1] == S.info[S.q][1] else '这一组到头了'),
        'res[info[q][0]] = s': '这一组的每个下标，答案都是组前的前 k 大之和：`res[{info[q][0]}] = {s}`',
        'for index': '这一组的 nums2 现在才入堆，因为同值互不「小于」',
        'heapq.heappush': '`{nums2[info[index][0]]}` 入堆',
        's += nums2': '`s` 加上新数 → {s}',
        'if len(heap) > k': lambda S, B, r: (f'堆大小 {len(S.heap)} > k = {S.k} → 要弹出最小的' if len(S.heap) > S.k else f'堆大小 {len(S.heap)} ≤ k = {S.k}，保留'),
        's -= heapq': '弹出堆顶（最小）并减去：`s = {s}`',
        'p = q': '下一组从 `{q}` 开始',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先排序转成前缀 top k，再用大小为 k 的小顶堆',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对每个下标，在 `nums1` 中严格更小的元素对应的 `nums2` 里选最大的至多 `k` 个求和',
                 '示例：`nums1=[4,2,1,5,3]`，`nums2=[10,20,30,40,50]`，`k=2` → `[80,30,0,80,50]`',
                 '本视频：`[4,2,2,5,3]`，含相同的 nums1'],
        quote='对info按元素值从小到大进行排序，……从中剔除掉值等于v的二元组后，问题就转化成了前缀的top k问题，接下来使用一个大小为k的小顶堆。',
        quote_src='—— yiduobo 题解原文',
        idea=['`info` 排序后，位置 `p` 之前都是小于等于 `v` 的',
              '剔除值等于 `v` 的一批，剩下就是前缀 top k',
              '`p`、`q` 圈出同值的一组：先记答案，再整组入堆'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：同值要整组处理，先写答案再入堆',
                 '堆超过 `k` 个就弹堆顶，`s` 同步增减',
                 '对比灵神：灵神把 nums2 也放进三元组排序，yiduobo 排下标二元组后回查 nums2'],
    ),
)
