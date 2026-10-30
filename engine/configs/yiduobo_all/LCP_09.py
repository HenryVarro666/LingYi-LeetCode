def _txt(S):
    if 'f' not in S or 'now' not in S:
        return '`f[i]` = 从 0 走到 i 的最少步数，`·` 表示还没到过'
    return f"当前点 `now = {S['now']}`，`f[now] = {S['f'][S['now']]}`，向右跳到 `{S['now']} + jump[{S['now']}] = {S['now'] + S['jump'][S['now']]}`"


CONFIG = dict(
    num='LCP 09', title='最小跳跃次数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='bfs · last_backfill 避免重复回跳',
    tags=['图论算法', '动态规划'],
    code='''
class Solution(object):
    def minJump(self, jump):

        n = len(jump)
        f = [None] * n
        f[0] = 0
        q = [0]
        head, tail = 0, 1
        last_backfill = 0
        while head < tail:
            now = q[head]
            head += 1
            if now + jump[now] >= n:
                return f[now] + 1

            if f[now + jump[now]] is None:
                q.append(now + jump[now])
                f[now + jump[now]] = f[now] + 1
                tail += 1

            for index in range(last_backfill + 1, now):
                if f[index] is None:
                    q.append(index)
                    f[index] = f[now] + 1
                    tail += 1

            last_backfill = max(last_backfill, now)
''',
    call='Solution().minJump([2,5,1,1,1,1])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='jump', label='jump（蓝 = now，橙 = last_backfill）', h=170,
             color=lambda S, i, v: ('blue' if i == S['now'] else 'orange' if i == S['last_backfill'] else None) if 'now' in S else None),
        dict(type='array', var=lambda S: ['·' if x is None else x for x in S['f']] if 'f' in S else None, label='f（到每个点的最少步数）', h=170,
             color=lambda S, i, v: 'green' if v != '·' else None),
        dict(type='queue', var=lambda S: S['q'][S['head']:] if 'head' in S else S.get('q'), label='bfs 队列（待处理）', h=130),
    ],
    watch=[('now', 'now', 'blue'), ('head', 'head'), ('tail', 'tail'), ('last_backfill', 'last_backfill', 'orange')],
    max_steps=60,
    captions={
        'f = [None] * n': '`f[i]` 记录从 0 到 i 的最短路，`None` 表示没到过',
        'f[0] = 0': '起点 `f[0] = 0`',
        'q = [0]': 'bfs 队列从 0 开始',
        'last_backfill = 0': '`last_backfill`：已经「往回走」处理过的最远节点',
        'while head < tail': '`head < tail`：队列里还有没处理的点',
        'now = q[head]': '取出队首 `now = {now}`，它的最短路 `f[now] = {f[now]}`',
        'if now + jump[now] >= n': lambda S, B, r: (f'`{S.now} + {S.jump[S.now]} >= {S.n}`：这一跳直接出界 → 答案是 `f[now] + 1 = {S.f[S.now] + 1}`' if S.now + S.jump[S.now] >= S.n
                                                     else f'`{S.now} + {S.jump[S.now]} = {S.now + S.jump[S.now]} < {S.n}`：这一跳还没出界'),
        'if f[now + jump[now]] is None': lambda S, B, r: (f'`{S.now + S.jump[S.now]}` 还没到过 → 新发现' if S.f[S.now + S.jump[S.now]] is None else f'`{S.now + S.jump[S.now]}` 已经到过，跳过'),
        'q.append(now + jump[now])': '向右跳到的 `{now + jump[now]}` 入队',
        'f[now + jump[now]] = f[now] + 1': '`f[{now + jump[now]}] = {f[now]} + 1` = =={f[now + jump[now]]}==',
        'for index in range': lambda S, B, r: (f'往回走只补 `[{S.last_backfill + 1}, {S.now - 1}]`：更靠前的点已被步数不更大的点回跳覆盖' if S.last_backfill + 1 <= S.now - 1 else f'回跳范围 `[{S.last_backfill + 1}, {S.now - 1}]` 为空，没有要补的点'),
        'if f[index] is None': lambda S, B, r: (f'`{S.index}` 还没到过 → 先到 now 再回跳，步数 `f[now] + 1`' if S.f[S.index] is None else f'`{S.index}` 已经有更短的路，跳过'),
        'q.append(index)': '回跳点 `{index}` 入队',
        'f[index] = f[now] + 1': '`f[{index}] = {f[now]} + 1` = =={f[index]}==',
        'tail += 1': '队尾 `tail` → {tail}',
        'last_backfill = max': '`last_backfill = max({B.last_backfill}, {now})` = =={last_backfill}==：{now} 及更前的点已处理过回跳',
    },
    cards=dict(
        one_liner='bfs 中，用 last_backfill 跳过已经回跳过的节点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['弹簧游戏：在第 `i` 个位置可以跳到 `i + jump[i]`（出界即通关），或回跳到任一前面的位置',
                 '求从 0 出发通关的最少步数',
                 '示例：`jump = [2,5,1,1,1,1]` → `3`'],
        quote='可以使用一个变量last_backfill记录当前已经处理过的最远的节点，那么对于当前节点now，由于bfs的特性，走到now的最短路径长度必然是大于等于走到last_backfill的最短路径长度的。',
        quote_src='—— yiduobo 题解原文',
        idea=['图的边是 `O(n^2)` 级，直接 bfs 太慢，重点在「往回走」',
              '若 `p` 的最短路是 `k`，则 `1..p-1` 最多 `k+1`',
              '所以从 `now` 往回只需补 `last_backfill+1` 到 `now-1`，每个点只会被补一次'],
        summary=['时间 `O(n)`：每个点最多入队一次',
                 '易错点：回跳范围是 `range(last_backfill + 1, now)`，不含 `now`',
                 '易错点：出界那一跳要返回 `f[now] + 1`',
                 '本题也可以按动态规划视角思考，yiduobo 采用最短路视角'],
    ),
)
