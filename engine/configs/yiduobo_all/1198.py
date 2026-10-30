def _cell(S, i, j, v):
    if 'p' not in S or 'num' not in S:
        return None
    if i == 0:
        return 'yellow' if v == S['num'] else ('green' if v < S['num'] else None)
    pi = S['p'][i]
    if j == pi:
        return 'green' if v == S['num'] else 'blue'
    if j < pi:
        return None
    return None


def _dim(S, i, j, v):
    if 'p' not in S or 'num' not in S:
        return False
    if i == 0:
        return v < S['num']
    return j < S['p'][i]


CONFIG = dict(
    num=1198, title='找出所有行中最小公共元素', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='枚举第 0 行 + 每行一个游标', tags=[],
    code='''
class Solution(object):
    def smallestCommonElement(self, mat):

        m = len(mat)
        n = len(mat[0])

        p = [0] * m

        for num in mat[0]:
            flag = True

            for i in range(1, m):
                while p[i] < n and mat[i][p[i]] < num:
                    p[i] += 1
                
                if p[i] == n:
                    return -1
                
                if mat[i][p[i]] != num:
                    flag = False
            
            if flag:
                return num
        
        return -1
''',
    call='Solution().smallestCommonElement([[1,2,3,4,5],[2,4,5,8,10],[3,5,7,9,11],[1,3,5,7,9]])',
    expect=5,
    skip=['flag = True', 'for i in range(1, m)'],
    max_steps=60,
    views=[
        dict(type='text', fn=lambda S: (f"枚举第 0 行的 `num = {S['num']}`，每行游标 `p[i]` 指向「第一个 ≥ {S['num']}」的位置" if 'num' in S else '每行一个游标 `p`，只右移、不回头')),
        dict(type='grid', var='mat', color=_cell, dim=_dim, cell=110, h=420,
             rows=lambda S: [f"行{i}" for i in range(len(S['mat']))]),
    ],
    watch=['num', ('p', 'p', 'blue'), 'i', 'flag'],
    captions={
        'm = len(mat)': '`m = {m}` 行',
        'n = len(mat[0])': '每行 `n = {n}` 列（行内严格递增）',
        'p = [0] * m': '`p[i]` 记录第 i 行当前检测到的下标，初始都在行首：`{p}`',
        'for num in mat[0]': '公共元素必在第 0 行里，从小到大枚举：`num = {num}`；先假设它是公共元素（`flag = True`），再逐行验证',
        'flag = True': '假设 `{num}` 是公共元素，逐行验证',
        'for i in range(1, m)': '检查第 `{i}` 行',
        'while p[i] < n and': lambda S, B, r: (f'`mat[{S.i}][{S.p[S.i]}] = {S.mat[S.i][S.p[S.i]]} < {S.num}`：还没到 num，游标继续右移' if S.p[S.i] < S.n and S.mat[S.i][S.p[S.i]] < S.num else (f'`p[{S.i}] = {S.n}` 已越界' if S.p[S.i] >= S.n else f'`mat[{S.i}][{S.p[S.i]}] = {S.mat[S.i][S.p[S.i]]} ≥ {S.num}`：游标停下')),
        'p[i] += 1': '`p[{i}]` → {p[i]}。`num` 只会越来越大，所以游标只右移、==不会回头==',
        'if p[i] == n': lambda S, B, r: (f'`p[{S.i}] = {S.n}`：第 {S.i} 行所有数都比 `{S.num}` 小，后面更大的 num 也不可能 → 返回 -1' if S.p[S.i] == S.n else f'`p[{S.i}] = {S.p[S.i]} < n`：第 {S.i} 行还有 ≥ num 的数'),
        'if mat[i][p[i]] != num': lambda S, B, r: (f'`mat[{S.i}][{S.p[S.i]}] = {S.mat[S.i][S.p[S.i]]} != {S.num}`：第 {S.i} 行没有 `{S.num}` → ==flag = False==' if S.mat[S.i][S.p[S.i]] != S.num else f'`mat[{S.i}][{S.p[S.i]}] = {S.num}`：第 {S.i} 行有 `{S.num}`'),
        'flag = False': '这个 num 不是公共元素，但仍要把后面的行游标推进',
        'if flag': lambda S, B, r: (f'每一行都有 `{S.num}` → 它就是最小公共元素' if S.flag else f'`{S.num}` 不是公共元素，换第 0 行下一个数'),
        'return num': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='公共元素必在第 0 行，从小到大试，每行游标只右移',
        complexity='时间 `O(m·n)`，空间 `O(m)`',
        problem=['`m × n` 矩阵 `mat`，每一行严格递增',
                 '求所有行中都出现的最小元素，没有则返回 `-1`',
                 '本视频：4 行 5 列的矩阵 → `5`'],
        quote='随着第0行中的数越来越大，其如果出现在其他行中，那么出现的下标也必然越来越靠后，于是可以使用一个数组p记录其他行中当前检测到下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案若存在，一定在第 0 行；从小到大枚举，第一个满足的就是最小',
              '每行用 `p[i]` 记录位置：枚举的数变大，位置只会变大，无需回头',
              '某行的 `p[i]` 走到头 → 后面更大的数更不可能 → 直接返回 `-1`'],
        summary=['时间 `O(m·n)`（每行游标最多走 n 步），空间 `O(m)`',
                 '代码原文已是 Python 3 可运行写法，无需改动',
                 '某行没有 `num` 时不 break，后面的行游标照常推进，下一个 num 才不用回头',
                 '游标越界要先判断：`p[i] < n` 写在 `mat[i][p[i]]` 前面'],
    ),
)
