def _edges(S):
    e = S['edges']
    return '边 `' + '  '.join(f'{a}→{b}' for a, b in e) + '`（a→b：a 比 b 强）'


CONFIG = dict(
    num=2924, title='找到冠军 II', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='标记被击败的队伍', tags=[],
    code='''
class Solution:
    def findChampion(self, n: int, edges: List[List[int]]) -> int:
        is_weak = [False] * n
        for _, y in edges:
            is_weak[y] = True  # 不是冠军

        ans = -1
        for i, weak in enumerate(is_weak):
            if weak:
                continue
            if ans != -1:
                return -1  # 冠军只能有一个
            ans = i
        return ans
''',
    call='Solution().findChampion(4, [[0,2],[1,3],[1,2]])',
    expect=-1,
    views=[
        dict(type='text', fn=_edges, h=70),
        dict(type='array', var='is_weak', pointers={'i': 'blue'}, label='is_weak（True = 被人击败，不是冠军）',
             color=lambda S, i, v: 'pink' if v else None, h=260),
        dict(type='text', fn=lambda S: f"候选冠军 `ans = {S['ans']}`" if 'ans' in S else '', h=70),
    ],
    watch=['i', 'weak', ('ans', 'ans', 'green')],
    captions={
        'is_weak = [False]': '先假设 `{n}` 支队伍都没被击败过',
        'is_weak[y] = True': '边的终点 `{y}` 被人击败了 → `is_weak[{y}] = True`，==不可能是冠军==',
        'ans = -1': '`ans = -1`：还没找到冠军',
        'if weak': lambda S, B, r: f'队伍 `{S.i}` 被击败过 → 跳过' if S.weak else f'队伍 `{S.i}` 没被击败过 → 冠军候选',
        'continue': '被击败的队伍直接略过',
        'if ans != -1': lambda S, B, r: (f'`ans = {S.ans}` 已有候选，又来一个没被击败的 `{S.i}` → 两个冠军候选互不可比' if S.ans != -1
                                      else '`ans = -1`，这是第一个候选'),
        'return -1': '==冠军只能有一个==：两支队伍都没人能击败 → 返回 `-1`',
        'ans = i': '`ans = {i}`：记下候选冠军',
        'return ans': '恰好一个候选 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='没被任何人击败的队伍才可能是冠军，恰好一个才算数',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['`n` 支队伍组成 DAG，边 `a→b` 表示 a 比 b 强',
                 '没有队伍强于 `a`，则 `a` 是冠军；冠军唯一就返回它，否则 `-1`',
                 '示例：`n=4, edges=[[0,2],[1,3],[1,2]]` → `-1`'],
        quote='标记所有 edges[i][1]，这些队伍都不是冠军。然后遍历每个节点 i，如果恰好有一个 i 没有被标记，说明没有可以击败 i 的队伍，i 队是冠军。',
        quote_src='—— 灵茶山艾府题解',
        idea=['边的终点都有人比它强，先全部打上「弱」标记',
              '再扫一遍：没标记的就是候选，出现第二个就直接返回 `-1`'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '「入度为 0」就是「没人能击败」，题目保证传递性，所以唯一入度 0 即冠军',
                 '易错：有两个及以上入度 0 的点要返回 `-1`，不要返回第一个'],
    ),
)
