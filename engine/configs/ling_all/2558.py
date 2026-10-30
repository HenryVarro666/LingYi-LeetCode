CONFIG = dict(
    num=2558, title='从数量最多的堆取走礼物', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='原地最大堆',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1277'],
    code='''
class Solution:
    def pickGifts(self, gifts: List[int], k: int) -> int:
        heapify_max(gifts)  # 原地堆化
        while k and gifts[0] > 1:
            heapreplace_max(gifts, isqrt(gifts[0]))  # 直接修改堆顶
            k -= 1
        return sum(gifts)
''',
    # heapify_max / heapreplace_max 是 Python 3.14 才有的；这里用 heapq 的内部函数补上（不被追踪）
    setup='''
def heapify_max(heap):
    heapq._heapify_max(heap)

def heapreplace_max(heap, item):
    ret = heap[0]
    heap[0] = item
    heapq._siftup_max(heap, 0)
    return ret
''',
    call='Solution().pickGifts([25,64,9,4,100], 4)',
    expect=29,
    views=[
        dict(type='heap', var='gifts', label='gifts（最大堆，堆顶 = 最多的一堆）', top_color='orange', h=440),
    ],
    watch=[('k', 'k', 'orange'), ('堆顶', lambda S: S['gifts'][0] if 'gifts' in S else None, 'pink'), ('总数', lambda S: sum(S['gifts']) if 'gifts' in S else None, 'green')],
    captions={
        'heapify_max': '原地堆化：把数组直接调整成最大堆，堆顶 `{gifts[0]}` 就是礼物最多的一堆，不用额外空间',
        'while k and': lambda S, B, r: (f'`k = {S.k}` 还有次数，堆顶 `{S.gifts[0]}` > 1，可以继续取' if S.k and S.gifts[0] > 1 else (f'`k = 0`，次数用完，结束' if not S.k else f'堆顶 `{S.gifts[0]}` 已经是 1：==所有堆都是 1==，开方不会再变，提前退出')),
        'heapreplace_max': lambda S, B, r: f'`heapreplace_max` 直接把堆顶 `{B.gifts[0]}` 换成 `isqrt({B.gifts[0]}) = {__import__("math").isqrt(B.gifts[0])}` 再下沉，==省掉一次弹出 + 一次压入==，新堆顶 `{S.gifts[0]}`',
        'k -= 1': '用掉一秒：`k` → {k}',
        'return sum': '剩下礼物总数 = 堆中所有元素之和 =={ret}==',
    },
    cards=dict(
        one_liner='要反复取最大值：最大堆，原地改堆顶',
        complexity='时间 `O(n + k log n)`，空间 `O(1)`',
        problem=['每一秒：选礼物最多的一堆，把它变成原来数量的平方根（向下取整）',
                 '返回 `k` 秒后剩下的礼物总数',
                 '示例：`[25,64,9,4,100], k=4` → `29`'],
        quote='维护一些数的最大值，可以最大堆模拟。循环 k 次。每次循环，弹出堆顶 top，然后把 floor(sqrt(top)) 入堆。',
        quote_src='—— 灵茶山艾府题解',
        idea=['反复取最大值 → ==最大堆==；先 `heapify_max` 原地建堆，`O(n)`',
              '优化 1：堆顶是 1 说明全是 1，开方不变，直接退出',
              '优化 2：不弹出再压入，而是 `heapreplace_max` 直接替换堆顶'],
        summary=['时间 `O(n + k log n)`：建堆 `O(n)`，每次改堆顶 `O(log n)`',
                 '原地堆化会修改输入数组，空间 `O(1)`',
                 '`heapify_max` 等是 Python 3.14 新增，视频里用 `heapq` 内部函数补了等价实现',
                 '易错：`k` 用完或堆顶为 1 都要停止循环'],
    ),
)
