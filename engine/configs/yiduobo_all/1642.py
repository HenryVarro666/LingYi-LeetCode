CONFIG = dict(
    num=1642, title='可以到达的最远建筑', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='小根堆（存负数）· 反悔用梯子',
    tags=['二分算法', '常用数据结构'],
    code='''
class Solution(object):
    def furthestBuilding(self, heights, bricks, ladders):

        heap = []
        for index in range(1, len(heights)):
            if heights[index] > heights[index - 1]:
                diff = heights[index] - heights[index - 1]
                if diff <= bricks:
                    bricks -= diff
                    heapq.heappush(heap, -diff)
                elif ladders > 0:
                    if heap and -heap[0] > diff:
                        bricks += -heapq.heappop(heap) - diff
                        heapq.heappush(heap, -diff)
                    ladders -= 1
                else:
                    return index - 1

        return len(heights) - 1
''',
    call='Solution().furthestBuilding([4,2,7,6,9,14,12], 5, 1)',
    expect=4,
    views=[
        dict(type='bars', var='heights', label='heights（蓝 = 当前所在，粉 = 要爬上的）', pointers={'index': 'pink'}, h=330, cell=100,
             color=lambda S, i, v: 'pink' if 'index' in S and i == S['index'] else ('blue' if 'index' in S and i == S['index'] - 1 else None)),
        dict(type='heap', var='heap', label='heap：用砖块爬过的高度差（存负数，堆顶 = 差最大）', fmt=lambda x: str(-x), top_color='orange', h=130),
        dict(type='text', h=90, size=30, fn=lambda S: f"剩余 砖块 `{S['bricks']}` 块，梯子 `{S['ladders']}` 架" if 'bricks' in S else ''),
    ],
    watch=[('index', 'index', 'pink'), ('diff', 'diff', 'orange'), ('bricks', 'bricks', 'yellow'), ('ladders', 'ladders', 'cyan')],
    captions={
        'heap = []': '`heap` 记录所有「用砖」爬过的高度差',
        'for index in range': '要从建筑 `{index-1}` 走到 `{index}`',
        'if heights[index] > heights[index - 1]': lambda S, B, r: (f'`{S.heights[S.index]} > {S.heights[S.index-1]}` → ==往上爬==，要消耗资源' if S.heights[S.index] > S.heights[S.index-1]
                                                                 else f'`{S.heights[S.index]} ≤ {S.heights[S.index-1]}` → 下坡或平地，==免费=='),
        'diff = ': '高度差 `diff = {diff}`',
        'if diff <= bricks': lambda S, B, r: (f'`{S.diff} <= {S.bricks}` → 砖够，先用砖（尽量保留梯子）' if S.diff <= S.bricks else f'`{S.diff} > {S.bricks}` → 砖不够了'),
        'bricks -= diff': '用掉 `{diff}` 块砖，剩 `{bricks}`',
        10: '记下这次用砖的差 `{diff}`，以后可能「反悔」换成梯子 → `heap` 有 `{[-x for x in heap]}`',
        'elif ladders > 0': lambda S, B, r: (f'还有 `{S.ladders}` 架梯子 → 必须用一架' if S.ladders > 0 else '梯子也没了 → 走不过去'),
        'if heap and -heap[0] > diff': lambda S, B, r: (f'堆顶 `{-S.heap[0]}` > 当前 `{S.diff}`：把梯子架在以前那处更划算' if S.heap and -S.heap[0] > S.diff
                                                       else '以前用砖的最大差也不比当前大 → 梯子直接用在当前'),
        'bricks += -heapq.heappop(heap) - diff': '梯子架到以前最大差那处，退回 `{-B.heap[0]}` 块砖，当前改用 `{diff}` 块 → 砖 `{B.bricks} + {-B.heap[0]} − {diff} = {bricks}`',
        14: '当前这处改用砖，记入堆：`{[-x for x in heap]}`',
        'ladders -= 1': '梯子用掉一架，剩 `{ladders}`',
        'return index - 1': '砖和梯子都不够爬到 `{index}` → 最远只能到 `{index-1}`',
        'return len(heights) - 1': '一路走到底，最远是最后一栋 `{len(heights)-1}`',
    },
    cards=dict(
        one_liner='先用砖，砖不够时把梯子换到最贵的那一步',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`heights[i]` 是建筑高度，从 0 号出发，砖块 `bricks`、梯子 `ladders`',
                 '下坡免费；上坡差 `d`：用 `d` 块砖，或用一架梯子（任意高度）',
                 '求最远能到的建筑下标。示例：`[4,2,7,6,9,14,12]`，5 砖 1 梯 → `4`'],
        quote='一个自然的想法是尽量保留梯子，只有当不得已的时候拿出来用，同时也必须满足用在当前最划算的位置上。',
        quote_src='—— yiduobo 题解原文',
        idea=['上坡一律先用砖，并把用砖的高度差放进堆',
              '砖不够时才动梯子：看堆顶（以前用砖最多的一步）',
              '堆顶比当前差大 → 梯子换到那一步，退回的砖补到当前；否则梯子用在当前'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '堆里存负数，Python 的 `heapq` 才能当大根堆用，`-heap[0]` 才是最大差',
                 '梯子为 0 又缺砖，直接返回 `index - 1`，不是 `index`',
                 '原文已是 Python 3 可运行代码，无需改动（只删了类型说明）',
                 '同类：灵神把梯子数当堆大小，砖用「超出的差之和」，思路对偶'],
    ),
)
