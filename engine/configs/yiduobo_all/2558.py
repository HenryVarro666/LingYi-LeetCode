CONFIG = dict(
    num=2558, title='从数量最多的堆取走礼物', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='大顶堆模拟（存负数）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1277'],
    code='''
class Solution(object):
    def pickGifts(self, gifts, k):

        heap = []
        for v in gifts:
            heapq.heappush(heap, -v)
        
        for _ in range(k):
            v = -heapq.heappop(heap)
            v = int(sqrt(v))
            heapq.heappush(heap, -v)
        
        return -sum(heap)
''',
    setup='from math import sqrt',
    call='Solution().pickGifts([25,64,9,4,100], 4)',
    expect=29,
    views=[
        dict(type='heap', var='heap', fmt=lambda x: str(-x), label='heap（存负数，图中显示礼物数）', top_color='orange', h=330),
        dict(type='text', fn=lambda S, B: (f"开方：`{B['v']}` → =={S['v']}==" if S.get('_line') == 10 and 'v' in B else ''), h=60),
    ],
    watch=[('v', lambda S: S.get('v'), 'pink'), ('总数', lambda S: -sum(S['heap']) if 'heap' in S else None, 'green')],
    captions={
        'heap = []': '准备一个堆；Python 只有最小堆，所以==存负数==来当大顶堆用',
        'for v in gifts': lambda S, B, r: ('礼物都压进堆了，建堆完成' if B.get('v') is not None and B.get('v') == S.get('v') else f'取下一堆礼物：`v = {S.v}`，等会取负后压入堆'),
        'heappush(heap, -v)': lambda S, B, r: (f'`-{S.v}` 入堆，堆顶 `{S.heap[0]}`（礼物 {-S.heap[0]}）' if S.get('_line') == 6 else f'开方后的 `{S.v}` 重新入堆：存 `-{S.v}`，堆顶变为礼物 {-S.heap[0]}'),
        'for _ in range(k)': lambda S, B, r: ('`k` 秒都过完了，退出循环' if S.get('_') == 3 and B.get('_') == 3 else '又过一秒：这一秒要处理礼物最多的那堆'),
        'v = -heapq.heappop': '弹出堆顶再取负还原：当前最多的一堆有 `{v}` 个礼物',
        'v = int(sqrt(v))': '减少到原来的平方根（向下取整）：`{B.v}` → =={v}==',
        'return -sum': '堆里存的是负数，求和后再取负：剩下礼物总数 =={ret}==',
    },
    cards=dict(
        one_liner='题目把大顶堆写在明面上：每秒处理堆顶',
        complexity='时间 `O((n + k) log n)`，空间 `O(n)`',
        problem=['每一秒：选礼物最多的一堆，把它变成原来数量的平方根（向下取整）',
                 '返回 `k` 秒后剩下的礼物总数',
                 '示例：`[25,64,9,4,100], k=4` → `29`'],
        quote='题目都把大顶堆写在明面上了，那么就按照题目意思，使用一个堆来维护这些礼物，然后执行k轮，每轮都对堆顶的礼物进行相应的操作即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`heapq` 是最小堆，==每个数取负==后存入，堆顶就是最大值',
              '循环 `k` 轮：弹出堆顶 → 取负还原 → 开方取整 → 取负压回堆',
              '最后把堆里所有数求和再取负'],
        summary=['时间 `O((n+k) log n)`，逐个压入建堆比 `heapify` 稍慢但更直观',
                 '开方用 `int(sqrt(v))`，`v` 最大 10^9，浮点精度够用',
                 '没有处理「全是 1 提前退出」的优化，`k` 最大 1000 也不影响',
                 '原文用到 `sqrt`，视频里在 setup 里 `from math import sqrt`'],
    ),
)
