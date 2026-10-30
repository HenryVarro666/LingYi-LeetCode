def _br(p):
    return f'工人{-p[1]}（来回{-p[0]}）'


def _wh(p):
    return f'工人{p[1]}→{p[0]}'


CONFIG = dict(
    num=2532, title='过桥的时间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='时序模拟 · 四个堆',
    tags=['灵神题单', '难度分 2589'],
    code='''
class Solution(object):
    def findCrossingTime(self, n, k, time):

        left_bridge = []
        left_warehouse = []
        right_bridge = []
        right_warehouse = []

        for index, (l2r, pick, r2l, put) in enumerate(time):
            heapq.heappush(left_bridge, [-l2r - r2l, -index])
        
        now = 0
        while n > 0 or right_bridge or right_warehouse:
            while left_warehouse and left_warehouse[0][0] <= now:
                t, index = heapq.heappop(left_warehouse)
                heapq.heappush(left_bridge, [-time[index][0] - time[index][2], -index])
            
            while right_warehouse and right_warehouse[0][0] <= now:
                t, index = heapq.heappop(right_warehouse)
                heapq.heappush(right_bridge, [-time[index][0] - time[index][2], -index])
            
            if right_bridge:
                _, index = heapq.heappop(right_bridge)
                index = -index
                now += time[index][2]
                heapq.heappush(left_warehouse, [now + time[index][3], index])
            elif left_bridge and n > 0:
                _, index = heapq.heappop(left_bridge)
                index = -index
                now += time[index][0]
                heapq.heappush(right_warehouse, [now + time[index][1], index])
                n -= 1
            else:
                next_t = None
                if left_warehouse:
                    next_t = left_warehouse[0][0]
                if right_warehouse:
                    if next_t is None or next_t > right_warehouse[0][0]:
                        next_t = right_warehouse[0][0]
                
                now = next_t
        
        return now
''',
    call='Solution().findCrossingTime(3, 2, [[1,5,1,8],[10,10,10,10]])',
    expect=37,
    views=[
        dict(type='heap', var='left_bridge', label='left_bridge 左等（堆顶最低效）', fmt=_br, top_color='blue', h=105),
        dict(type='heap', var='left_warehouse', label='left_warehouse 左放箱（→完成）', fmt=_wh, h=105),
        dict(type='heap', var='right_bridge', label='right_bridge 右等（堆顶最低效）', fmt=_br, top_color='pink', h=105),
        dict(type='heap', var='right_warehouse', label='right_warehouse 右搬箱（→完成）', fmt=_wh, h=105),
        dict(type='text', h=70, size=26, fn=lambda S: (f"时间节点 `now = {S['now']}`，还要从左边派 =={S['n']}== 个工人" if 'now' in S else '')),
    ],
    watch=[('now', 'now', 'yellow'), ('n', 'n', 'orange'), ('index', 'index', 'cyan')],
    captions={
        'heapq.heappush(left_bridge, [-l2r': '工人 `{index}` 一开始都在左边等桥：关键字 `[-(来+回), -下标]`，==来回之和大、下标大的在堆顶（最低效）==',
        'now = 0': '`now`：当前时间节点，围绕桥空闲的时刻往前推',
        'while n > 0 or': lambda S, B, r: (f'还有 `{S.n}` 个箱子未搬，或右边还有工人 → 继续' if S.n > 0 or S.right_bridge or S.right_warehouse
                                           else '箱子搬完，右边也没人了 → 结束'),
        'while left_warehouse and': lambda S, B, r: (f'左边放完箱的工人（完成 `{S.left_warehouse[0][0]}` ≤ now `{S.now}`）回桥边排队'
                                                     if S.left_warehouse and S.left_warehouse[0][0] <= S.now else '左边暂时没人放完箱'),
        't, index = heapq.heappop(left_warehouse)': '弹出最早放完箱的工人 `{index}`',
        'heapq.heappush(left_bridge, [-time': '工人 `{index}` 回到左边排队',
        'while right_warehouse and': lambda S, B, r: (f'右边搬完箱的工人（完成 `{S.right_warehouse[0][0]}` ≤ now `{S.now}`）到桥边排队'
                                                      if S.right_warehouse and S.right_warehouse[0][0] <= S.now else '右边暂时没人搬完箱'),
        't, index = heapq.heappop(right_warehouse)': '弹出最早搬完箱的工人 `{index}`',
        'heapq.heappush(right_bridge, [-time': '工人 `{index}` 在右边排队',
        'if right_bridge': lambda S, B, r: ('右边有人排队 → ==先让右边（效率最低）的工人过桥==' if S.right_bridge else '右边没人排队，看左边'),
        'heapq.heappop(right_bridge)': '右边效率最低的是工人 `{-index}`',
        'index = -index': '取回真实下标 `{index}`',
        'now += time[index][2]': '右→左过桥 `{time[index][2]}`：`now = {B.now} + {time[index][2]} = {now}`',
        'heapq.heappush(left_warehouse': '过桥后去放箱，放完时刻 `{now} + {time[index][3]} = {now + time[index][3]}`',
        'elif left_bridge and n > 0': lambda S, B, r: ('右边没人，左边有人排队且箱子没派完 → 让左边效率最低的过桥' if S.left_bridge and S.n > 0
                                                       else '左边也没人（或箱子已派完）→ 桥空着，找下一个时间节点'),
        'heapq.heappop(left_bridge)': '左边效率最低的是工人 `{-index}`',
        'now += time[index][0]': '左→右过桥 `{time[index][0]}`：`now = {B.now} + {time[index][0]} = {now}`',
        'heapq.heappush(right_warehouse': '过桥后去搬箱，搬完时刻 `{now} + {time[index][1]} = {now + time[index][1]}`',
        'n -= 1': '又有一个箱子开始被搬：`n = {n}`',
        'next_t = None': '==桥一直空闲==（所有工人都在搬箱）：时间要跳到最早完成搬运的时刻',
        'if left_warehouse:': lambda S, B, r: ('左边有人在放箱，先取它的最早完成时间' if S.left_warehouse else '左边没人在放箱'),
        'next_t = left_warehouse[0][0]': '候选 `next_t = {next_t}`',
        'if right_warehouse:': lambda S, B, r: ('右边有人在搬箱，和左边比较取更早的' if S.right_warehouse else '右边没人在搬箱'),
        'if next_t is None or': lambda S, B, r: ('右边更早 → 用右边的完成时间' if S.next_t is None or S.next_t > S.right_warehouse[0][0]
                                                  else '左边更早，保持不变'),
        'next_t = right_warehouse[0][0]': '`next_t = {next_t}`',
        'now = next_t': '时间直接跳到 `now = {now}`',
        'return now': '最后一个箱子到桥左侧的时间 =={ret}==（不用算放箱）',
    },
    skip=['index = -index'],
    cards=dict(
        one_liner='围绕「桥的空闲时刻」推进时间，四个堆管四种状态的工人',
        complexity='时间 `O((n+k) log k)`，空间 `O(k)`',
        problem=['`k` 个工人搬 `n` 个箱子，同一时刻只有一人过桥；右边等桥的优先，同侧效率最低的先走',
                 '效率低 = `left+right` 大，相同则下标大。求最后一个箱子到达桥左侧的时间',
                 '示例：`n=3, k=2, time=[[1,5,1,8],[10,10,10,10]]` → `37`'],
        quote='由于本题中只有过桥是独占的，而其他动作可以并行，因此本题的时间节点应该围绕桥的空闲时刻展开。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个「等桥」堆按 `-(来+回)`、`-下标` 排，堆顶即最低效的工人',
              '两个「仓库」堆按完成时间排；`now` 之前完成的先挪到等桥堆',
              '桥空闲且所有人都在搬箱时，`now` 直接跳到最早完成的时刻；右边搬空且过桥后即结束'],
        summary=['时间 `O((n+k) log k)`，空间 `O(k)`',
                 '答案是最后一个工人==到达桥左侧==的时刻，不含放箱时间',
                 '循环条件要包含 `right_bridge`、`right_warehouse`：箱子派完后右边还有人要过桥',
                 '桥空闲时必须跳到最早完成时刻，否则会死循环',
                 '对比灵神：他先排序用下标比效率；yiduobo 用 `[-(来+回), -下标]` 直接入堆'],
    ),
)
