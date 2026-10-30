CONFIG = dict(
    num=2374, title='边积分最高的节点', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='一次遍历 · 边遍历边更新答案',
    tags=[],
    code='''
class Solution:
    def edgeScore(self, edges: List[int]) -> int:
        ans = 0
        score = [0] * len(edges)
        for i, to in enumerate(edges):
            score[to] += i
            if score[to] > score[ans] or score[to] == score[ans] and to < ans:
                ans = to
        return ans
''',
    call='Solution().edgeScore([1,0,0,0,0,7,7,5])',
    expect=7,
    views=[
        dict(type='array', var='edges', label='edges（边 i → edges[i]，蓝 = 当前边）', pointers={'i': 'blue'}, h=200),
        dict(type='array', var='score', label='score（粉 = 刚加分的节点，绿 = 当前答案）', pointers={'to': 'pink', 'ans': 'green'}, h=230),
    ],
    watch=[('i', 'i', 'blue'), ('to', 'to', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 先设为节点 0',
        'score = [0]': '`score[x]`：指向节点 x 的所有节点编号之和',
        'score[to] += i': '边 `{i} → {to}`：把 `{i}` 加到 `score[{to}]` → =={score[to]}==',
        'if score[to] > score[ans]': lambda S, B, r: (
            f'`score[{S.to}] = {S.score[S.to]}` 比答案 `score[{B.ans}] = {S.score[B.ans]}` 大 → 更新答案' if S.score[S.to] > S.score[B.ans]
            else (f'积分相同且 `{S.to} < {B.ans}` → 取编号小的' if S.score[S.to] == S.score[B.ans] and S.to < B.ans
                  else f'`score[{S.to}] = {S.score[S.to]}` 没超过答案 `{S.score[B.ans]}` → 不更新')),
        'ans = to': '`ans = {ans}`',
        'return ans': '积分最高（相同取编号最小）的节点是 `{ans}`',
    },
    cards=dict(
        one_liner='边加分边维护答案：积分大，或积分同且编号小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个节点恰有一条出边 `i → edges[i]`',
                 '节点的边积分 = 指向它的所有节点的编号之和',
                 '求积分最高的节点，相同取编号最小；示例 `[1,0,0,0,0,7,7,5]` → `7`'],
        quote='用一个长为 n 的数组 score 记录每个节点的得分。遍历 edges，根据题意，把 i 加到 score[edges[i]] 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历时 `score[to] += i`',
              '只有被加分的节点才可能成为新答案，所以在这里立刻比较',
              '积分相同时要比编号，别漏掉 `to < ans`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：积分相同取编号小的，这个判断要写进比较里',
                 '另一种写法：先算完 `score`，再 `score.index(max(score))`，但不是一次遍历'],
    ),
)
