CONFIG = dict(
    num=1962, title='移除石子使总数最小', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最大堆模拟 + 原地堆化',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1419'],
    code='''
class Solution:
    def minStoneSum(self, piles: List[int], k: int) -> int:
        heapify_max(piles)  # 原地堆化
        while k and piles[0] != 1:
            heapreplace_max(piles, (piles[0] + 1) // 2)
            k -= 1
        return sum(piles)
''',
    setup='heapify_max = heapq._heapify_max\nheapreplace_max = heapq._heapreplace_max',
    call='Solution().minStoneSum([5,4,9,7], 3)',
    expect=16,
    views=[
        dict(type='heap', var='piles', label='piles（原地堆化后的最大堆，堆顶 = 最大的一堆）', top_color='yellow', h=160),
        dict(type='text', fn=lambda S: f'堆顶 `{S["piles"][0]}`：移除一半后剩 `ceil({S["piles"][0]}/2)`，当前总数 ==`{sum(S["piles"])}`==', size=26, h=60),
    ],
    watch=['k', ('堆顶', 'piles[0]', 'yellow'), ('总数', 'sum(piles)', 'green')],
    captions={
        'heapify_max': '原地堆化：不开新数组，直接把 `piles` 调整成最大堆，堆顶 = ==`{piles[0]}`== 是最多的一堆',
        'while k': lambda S, B, ret: (f'`k` = {S.k}，操作次数用完，退出循环' if S.k == 0 else f'还剩 `{S.k}` 次操作；堆顶 `{S["piles"][0]}`，' + ('不是 1，还能继续减' if S['piles'][0] != 1 else '是 1，所有堆都是 1，再操作也不变，直接退出')),
        'heapreplace_max': '最多的一堆 `{B.piles[0]}` 移走一半，剩 `({B.piles[0]}+1)//2` = ==`{(B.piles[0] + 1) // 2}`==；替换堆顶并下沉，堆顶变成 `{piles[0]}`',
        'k -= 1': '用掉一次操作，还剩 `{k}` 次',
        'return sum': '`k` 用完，所有堆的和 = ==`{ret}`== 就是最小剩余总数',
    },
    max_steps=60,
    cards=dict(
        one_liner='每次都对最大的一堆减半，用最大堆维护',
        complexity='时间 `O(n + k log n)`，空间 `O(1)`',
        problem=['`piles[i]` 是每堆石子数，恰好操作 `k` 次，每次选一堆移除 `floor(x/2)` 颗',
                 '求剩下石子总数的最小值',
                 '本视频：`piles=[5,4,9,7], k=3` → ==16=='],
        quote='每次操作，应当选数组中最大的数，移除它的一半（下取整）。动态维护数组的最大值，可以最大堆模拟。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：同样操作一次，==越大的堆减得越多==，所以每次选最大的',
              '一次操作后 `x` 变成 `x - floor(x/2) = ceil(x/2) = (x+1)//2`',
              '最大值会变，所以用堆；`heapreplace_max` 一步完成“弹出堆顶 + 放入新值”'],
        summary=['时间 `O(n + k log n)`：原地堆化 `O(n)`，每次改堆顶 `O(log n)`；原地堆化空间 `O(1)`',
                 '优化 1：堆顶为 1 说明全是 1，操作无效，直接退出循环',
                 '`heapify_max` / `heapreplace_max` 是 Python 3.14 新增的；本视频用 heapq 内部同名实现代替',
                 '易错：向上取整写成 `(x+1)//2`，不要写 `x//2`',
                 '同类题：2530. 执行 K 次操作后的最大分数'],
    ),
)
