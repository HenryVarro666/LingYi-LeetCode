CONFIG = dict(
    num=997, title='找到小镇的法官', difficulty='Easy', category='图论算法',
    author='yiduobo', technique='统计入度与出度',
    tags=[],
    code='''
class Solution(object):
    def findJudge(self, N, trust):

        ind = [0] * N
        oud = [0] * N
        for x, y in trust:
            oud[x - 1] += 1
            ind[y - 1] += 1
        
        for x in range(N):
            if ind[x] == N - 1 and oud[x] == 0:
                return x + 1
        
        return -1
''',
    call='Solution().findJudge(4, [[1, 3], [1, 4], [2, 3], [2, 4], [4, 3]])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('小镇 `N = %d` 人，法官需要：入度 `= N-1 = %d`，出度 `= 0`' % (S['N'], S['N'] - 1)) if 'N' in S else ''),
        dict(type='array', var='ind', label='ind（入度：被多少人信任）', pointers={'(y - 1) if _line < 10 else x': 'blue'}, pointer_labels={'(y - 1) if _line < 10 else x': 'y-1 / x'}, h=200,
             color=lambda S, i, v: 'green' if v == S['N'] - 1 else None),
        dict(type='array', var='oud', label='oud（出度：信任多少人）', pointers={'(x - 1) if _line < 10 else x': 'blue'}, pointer_labels={'(x - 1) if _line < 10 else x': 'x-1 / x'}, h=200,
             color=lambda S, i, v: 'pink' if v > 0 else None),
        dict(type='text', fn=lambda S: ('当前这条信任：`%s → %s`（编号从 1 开始，下标要减 1）' % (S['x'], S['y'])) if 'y' in S and isinstance(S.get('x'), int) and S.get('_line') and S['_line'] < 9 else ''),
    ],
    watch=['x', 'y', 'N'],
    captions={
        'ind = [0]': '`ind[i]`：第 `i+1` 个人被几个人信任（入度），共 `{N}` 人',
        'oud = [0]': '`oud[i]`：第 `i+1` 个人信任了几个人（出度）',
        'for x, y in trust': lambda S, B, r: ('trust 遍历完毕，入度出度统计好了' if 'x' in B and (S.x, S.y) == (B.x, B.y) else f'处理一条信任关系：`{S.x}` 信任 `{S.y}`，即图中边 `{S.x} → {S.y}`'),
        'oud[x - 1] += 1': '`{x}` 信任了别人，出度 +1 → `oud[{x - 1}] = {oud[x - 1]}`：==他不可能是法官==',
        'ind[y - 1] += 1': '`{y}` 多了一个信任者，入度 +1 → `ind[{y - 1}] = {ind[y - 1]}`',
        'for x in range(N)': '检查第 `{x + 1}` 个人：入度 `{ind[x]}`，出度 `{oud[x]}`',
        'if ind[x] == N - 1': lambda S, B, r: (f'`ind = {S.ind[S.x]}` {"==" if S.ind[S.x] == S.N - 1 else "≠"} `N-1 = {S.N - 1}`' + (f'，`oud = {S.oud[S.x]}`' + (' = 0 → ==是法官==' if S.oud[S.x] == 0 else '≠ 0 → 他信任了别人，不是法官') if S.ind[S.x] == S.N - 1 else '：不是所有人都信任他 → 不是法官')),
        'return x + 1': '法官是第 `{x + 1}` 个人（下标要 +1）',
        'return -1': '没有人满足条件 → 返回 `-1`',
    },
    cards=dict(
        one_liner='法官 = 入度 N-1、出度 0 的点',
        complexity='时间 `O(N + len(trust))`，空间 `O(N)`',
        problem=['小镇有 `N` 个人，编号 1 到 N，可能有一位秘密法官',
                 '法官不信任任何人，其余所有人都信任法官，且只有一位这样的人',
                 '`trust[i] = [a, b]` 表示 a 信任 b；返回法官编号，不存在返回 `-1`',
                 '示例：`N=4`，`trust=[[1,3],[1,4],[2,3],[2,4],[4,3]]` → `3`'],
        quote='将小镇的每个人视为有向图中的一个点，若a信任b则在图中建立一条a指向b的边……找出图中入度为n - 1，出度为0的点即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['信任关系就是有向边 `a → b`：数出每个点的入度、出度',
              '法官不信任任何人：出度 `= 0`',
              '其余 `N-1` 人都信任他：入度 `= N-1`；这样的人至多一个'],
        summary=['时间 `O(N + T)`，两个数组各 `O(N)`',
                 '易错：编号从 1 开始，访问数组要 `x - 1`，返回时要 `+ 1`',
                 '易错：`N = 1` 且 `trust` 为空时，入度 0 = N-1，出度 0，法官是 1'],
    ),
)
