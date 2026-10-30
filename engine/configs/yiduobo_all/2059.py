def _txt(S):
    if 'q' not in S:
        return ''
    if 'now' in S and 'num' in S and 'opt' in S:
        sym = ['+', '-', '^'][S['opt']]
        return f"当前 `now = {S['now']}`，用 `{S['now']} {sym} {S['num']}`；目标 goal 是 =={S['goal']}=="
    return f"第 {S['step']} 轮 bfs，队列 `q` 的 `[l, r)` 区间是这一轮要处理的数" if 'step' in S else ''


CONFIG = dict(
    num=2059, title='转化数字的最小运算数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='分层 bfs · 只入队 0~1000 内的新数',
    tags=['图论算法', '难度分 1850'],
    code='''
class Solution(object):
    def minimumOperations(self, nums, start, goal):

        l = 0
        r = 1
        q = [start]
        used = set([start])

        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for num in nums:
                    for opt in range(3):
                        if opt == 0:
                            next = now + num
                        elif opt == 1:
                            next = now - num
                        else:
                            next = now ^ num

                        if next == goal:
                            return step
                        elif next >= 0 and next <= 1000 and next not in used:
                            used.add(next)
                            q.append(next)

            l, r = r, len(q)

        return -1
''',
    call='Solution().minimumOperations([2,4,12], 2, 12)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='q', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r - 1'), label='队列 q（蓝框 = 本轮要处理的数）', h=170),
        dict(type='set', var='used', label='used（已经入过队的数）', h=200),
    ],
    watch=[('step', 'step', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'now', 'num', 'next', ('goal', 'goal', 'green')],
    max_steps=64,
    skip=['opt == 0', 'opt == 1'],
    captions={
        'q = [start]': '起点 `start = {start}` 进队列：它是第 0 层',
        'used = set': '`used` 记录进过队的数，防止重复访问',
        'step += 1': '开始处理新的一层：走了 ==`{step}`== 步能到的数',
        'for now in q': lambda S, B, r: (f'取出 `now = {S.now}`，逐个枚举 `nums` 和三种运算' if B.get('now') != S.get('now') or 'now' not in B else '这一层的数都处理完了'),
        'next = now + num': '`next = {now} + {num} = {next}`',
        'next = now - num': '`next = {now} - {num} = {next}`',
        'next = now ^ num': '`next = {now} ^ {num} = {next}`（异或）',
        'if next == goal': lambda S, B, r: (f"`next = {S.next}` 等于 `goal` → 这一轮就到了，答案 = ==`step = {S.step}`==" if S.next == S.goal
                                            else f"`next = {S.next}` 不是 `goal = {S.goal}`，看它能否入队"),
        'elif next >= 0': lambda S, B, r: (f"`{S.next}` 在 0~1000 内且没用过 → 入队，下一轮继续扩展" if 0 <= S.next <= 1000 and S.next not in B.used
                                           else f"`{S.next}` 已用过或越界：越界的数即使不是 goal 也不能再运算，不入队"),
        'used.add': '`used` 加入 `{next}`',
        'q.append': '`{next}` 入队',
        'l, r = r, len(q)': '这一层处理完：新的一层是 `q[{l}:{r}]`',
        'return step': '返回 ==`{step}`== 步',
        'return -1': 'bfs 耗尽仍到不了 → `-1`',
    },
    cards=dict(
        one_liner='把数字当成图的点，bfs 的层数就是最少运算数',
        complexity='时间 `O(1001 × n × 3)`，空间 `O(1001)`',
        problem=['`x` 从 `start` 出发，每次对一个 `nums[i]` 做 `+`、`-`、`^`',
        '只有 `0 <= x <= 1000` 时才能继续运算；越界的结果可以生效，但不能再算',
        '示例：`nums=[2,4,12], start=2, goal=12` → `2`（2 → 14 → 12）'],
        quote='由于题目保证了运算的中间结果只会在0到1000之间，因此可以直接从start开始进行bfs，只将在0到1000之内的且没有被使用过的数添加到bfs的队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['能继续运算的数只有 1001 个，所以点数很少，直接 bfs',
              '一层 bfs = 多走一步；`next == goal` 时轮次 `step` 就是答案',
              'goal 可以在 0~1000 之外：所以==先判断 goal，再判断是否入队=='],
        summary=['时间 `O(1001 × n)`：每个数最多入队一次，每次枚举 `n × 3` 种运算',
                 '易错点：`next == goal` 必须放在范围判断之前，越界的 goal 也算到达',
                 '越界的数不入队，因为它不能再做运算',
                 '用 `l, r` 切出每一层，不需要额外存距离'],
    ),
)
