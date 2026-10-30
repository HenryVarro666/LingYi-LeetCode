_OPS = ['+', '-', '^']


def _cand(S, B):
    if 'now' not in S or 'num' not in S or 'step' not in S:
        return ''
    a, n = S['now'], S['num']
    return f"第 `{S['step']}` 轮：`now = {a}`，`num = {n}` → `{a}+{n}={a+n}`，`{a}−{n}={a-n}`，`{a}^{n}={a^n}`（目标 `{S['goal']}`）"


CONFIG = dict(
    num=2059, title='转化数字的最小运算数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 按轮扩展 + used 去重',
    tags=['灵神题单·图论算法', '难度分 1850'],
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
    call='Solution().minimumOperations([2,12], 2, 12)',
    expect=2,
    views=[
        dict(type='text', fn=_cand, h=70, size=26),
        dict(type='array', var='q', pointers={'l': 'blue'}, window=('l', 'r - 1'), label='队列 q（框 = 本轮 [l, r) 要处理的数）', h=210),
        dict(type='array', var='sorted(used)', label='已使用 used', index=False, h=130),
    ],
    skip=['used.add(next)', 'step = 0', 'l = 0'],
    max_steps=80,
    watch=[('step', 'step', 'blue'), 'l', 'r', 'now', 'num', ('next', 'next', 'yellow'), ('goal', 'goal', 'green')],
    captions={
        'r = 1': '`[l, r)` 是本轮要处理的队列区间：`l = 0, r = 1`',
        'q = [start]': '起点 `{start}` 入队，`used` 记录用过的数',
        'while l < r': lambda S, B, r_: f'区间 `[{S.l}, {S.r})` 非空，继续下一轮' if S.l < S.r else '区间为空，没有新的数可扩展 → 失败',
        'step += 1': '开始新一轮 BFS，运算次数 `step` → {step}',
        'for now in': lambda S, B, r_: f'取本轮的数 `now = {S.now}`' if B.get('now') != S.now else '本轮的数都处理完',
        'for num in nums': lambda S, B, r_: f'拿 `nums` 里的 `num = {S.num}` 对 `{S.now}` 运算' if B.get('num') != S.num or B.get('now') != S.now else '`nums` 用完了',
        'for opt in': lambda S, B, r_: f'第 `{S.opt}` 种运算：{"加" if S.opt == 0 else "减" if S.opt == 1 else "异或"}' if B.get('opt') != S.opt or B.get('num') != S.num else '三种运算做完',
        'if opt == 0': '`opt = {opt}`：{"opt == 0 → 加法" if opt == 0 else "不是加法，往下看"}',
        'elif opt == 1': '`opt = {opt}`：{"opt == 1 → 减法" if opt == 1 else "不是减法，只剩异或"}',
        'next = now + num': '`next = {now} + {num} = {next}`',
        'next = now - num': '`next = {now} − {num} = {next}`',
        'next = now ^ num': '`next = {now} ^ {num} = {next}`',
        'if next == goal': lambda S, B, r_: (f'`next = {S.next}` 等于目标 → 当前 `step = {S.step}` 就是答案' if S.next == S.goal else f'`next = {S.next}` ≠ 目标 `{S.goal}`'),
        'elif next >= 0': lambda S, B, r_: (f'`{S.next}` 越界：只能比较 `goal`，不能继续运算' if not 0 <= S.next <= 1000
                                            else f'`{S.next}` 已在 `used` 里，不重复入队' if S.next in S.used else f'`{S.next}` 在 `[0, 1000]` 且没用过 → 记入 `used` 并入队'),
        'q.append(next)': '`{next}` 入队：`q = {q}`',
        'l, r = r, len(q)': '本轮结束：新区间 `[l, r) = [{l}, {r})` 就是这一轮新加入的数',
        'return step': '第一次碰到 `goal`，答案 `{step}`',
        'return -1': '没有新数可扩展 → `-1`',
    },
    cards=dict(
        one_liner='只要 0 到 1000 里的数入队，一轮 BFS 就是多做一次运算',
        complexity='时间 `O(1001 × n)`，空间 `O(1001)`',
        problem=['`x` 从 `start` 出发，每次对 `x` 加、减或异或 `nums[i]`',
                 '只有 `0 <= x <= 1000` 才能继续运算，越界的结果也算但是不能再动',
                 '求变成 `goal` 的最少运算次数，不行则 `-1`',
                 '本视频：`nums=[2,12], start=2, goal=12` → `2`'],
        quote='由于题目保证了运算的中间结果只会在0到1000之间，因此可以直接从start开始进行bfs，只将在0到1000之内的且没有被使用过的数添加到bfs的队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q[l:r]` 是本轮要处理的数，轮次 `step` 就是已经做的运算次数',
              '对每个 `now`，枚举 `nums` 和三种运算（用 `opt` 编号）得到 `next`',
              '`next` 等于 `goal` 立刻返回；在范围内且没用过才入队'],
        summary=['原文为 Python 2 风格，在 Python 3 下无需改动，代码照搬',
                 '时间 `O(1001 × n)`，空间 `O(1001)`',
                 '易错点：先判断 `next == goal`，再判断范围；`goal` 可以越界',
                 '`l, r = r, len(q)` 用区间切分轮次，代替 BFS 里的分层列表',
                 '对比灵神：他按层拷贝队列 `tmp`，这里用下标区间；思路相同'],
    ),
)
