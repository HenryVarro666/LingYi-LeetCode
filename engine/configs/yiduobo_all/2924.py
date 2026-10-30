CONFIG = dict(
    num=2924, title='找到冠军 II', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='统计入度', tags=[],
    code='''
class Solution(object):
    def findChampion(self, n, edges):

        ind = [0] * n
        for x, y in edges:
            ind[y] += 1
        
        res = None
        for index in range(n):
            if ind[index] == 0:
                if res is None:
                    res = index
                else:
                    res = -1
                    break
        
        return res
''',
    call='Solution().findChampion(5, [[0,1],[0,2],[0,3],[1,2],[4,3]])',
    expect=-1,
    views=[
        dict(type='text', fn=lambda S: '边 `' + '  '.join(f'{a}→{b}' for a, b in S['edges']) + '`', h=70),
        dict(type='array', var='ind', pointers={'index': 'blue'}, label='ind（入度 = 被几支队伍击败过）',
             color=lambda S, i, v: 'green' if v == 0 else None, h=260),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" if 'res' in S else '', h=70),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'ind = [0]': '`ind[i]`：第 `i` 支队伍被击败的次数，开始都是 0',
        'ind[y] += 1': '`{x}` 击败了 `{y}` → `ind[{y}]` 变成 `{ind[y]}`',
        'res = None': '`res = None`：还没有候选冠军',
        'if ind[index] == 0': lambda S, B, r: (f'队伍 `{S.index}` 入度 `0`：没输过 → 候选' if S.ind[S.index] == 0
                                              else f'队伍 `{S.index}` 入度 `{S.ind[S.index]}`：输过，不可能是冠军'),
        'if res is None': lambda S, B, r: ('还没有候选 → 它就是候选' if S.res is None
                                           else f'已有候选 `{S.res}`，又一支没输过的队伍：两队没比过，传递性也推不出强弱'),
        'res = index': '候选冠军 `res = {res}`',
        'res = -1': '多支队伍没被击败 → ==不存在冠军==，`res = -1`',
        'break': '结果已定，提前结束',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='入度 0 = 从没输过；只有一支这样的队伍才是冠军',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['有向无环图，`a→b` 表示 a 队强于 b 队',
                 '没有队伍强于 a 队，a 就是冠军；冠军唯一则返回，否则 `-1`',
                 '本视频：`n=5` 的 5 条边 → `-1`'],
        quote='若只有一支队伍没被击败过，那么由于传递性的存在，这支队伍一定是冠军。若存在多支队伍没有被击败过，说明这些队伍之间没有进行过比赛。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计每支队伍的入度，也就是被几支队伍击败过',
              '入度为 0 的队伍数量：1 个 → 冠军；多个 → 它们之间无法比较，没有冠军'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '上一题（2923）有全胜负关系，可以一趟比较；本题不保证，需要入度',
                 '易错：入度为 0 的有多个时要返回 `-1`，且第一个候选不能直接返回'],
    ),
)
