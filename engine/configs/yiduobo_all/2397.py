def _cols(S):
    now = S.get('now')
    if now is None or 'n' not in S:
        return set()
    return {j for j in range(S['n']) if now >> j & 1}


def _txt(S):
    if 'now' not in S or 'used' not in S:
        return '先把每一行需要的列压成整数 `need`'
    cols = sorted(_cols(S))
    if S['used'] == S['cols']:
        return f"已选列 {cols}，正好 `{S['cols']}` 列：数一数覆盖几行"
    return f"已选列 {cols}（`used = {S['used']}`，目标 `{S['cols']}` 列），正在决定第 `{S.get('level', '?')}` 列"


CONFIG = dict(
    num=2397, title='被列覆盖的最多行数', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 枚举列 + 状态压缩判断',
    tags=['灵神题单·链表树与回溯', '难度分 1719'],
    code='''
class Solution(object):
    def maximumRows(self, mat, cols):

        m = len(mat)
        n = len(mat[0])

        need = []
        for i in range(m):
            now = 0
            for j in range(n):
                if mat[i][j] == 1:
                    now += (1 << j)
            need.append(now)
        
        self.res = 0
        
        def dfs(now, used, level):
            if used == cols:
                cnt = 0
                for index in range(m):
                    if (now & need[index]) == need[index]:
                        cnt += 1
                self.res = max(self.res, cnt)
                return 
            
            if level == n:
                return
            
            dfs(now, used, level + 1)
            dfs(now | (1 << level), used + 1, level + 1)

        dfs(0, 0, 0)
        return self.res
''',
    call='Solution().maximumRows([[0,0,0],[1,0,1],[0,1,1],[0,0,1]], 2)',
    expect=3,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 选中列的 1，红 = 未选中列的 1）', h=260, cell=70,
             color=lambda S, i, j, v: ('yellow' if v == 1 and j in _cols(S) else 'red' if v == 1 else None)
             if 'now' in S and 'used' in S else None),
        dict(type='array', var='need', label='need（每行要求的列，二进制压成整数）', h=190, cell=80),
        dict(type='text', h=80, size=28, fn=_txt),
        dict(type='calls', h=250),
    ],
    skip=['for j in range(n)', 'if mat[i][j] == 1', 'now += (1 << j)', 'now = 0', 'for index in range(m)', 'cnt = 0', 'for i in range(m)'],
    max_steps=100,
    watch=[('now', 'now', 'yellow'), 'used', 'level', ('cnt', 'cnt', 'blue'), ('res', 'self.res', 'green')],
    captions={
        'now += (1 << j)': '第 `{j}` 列有 1 → 这一行需要它：`now = {now}`',
        'need.append': '第 `{i}` 行需要的列集合压成整数 `{now}` → `need = {need}`',
        'self.res = 0': '`self.res` 记录目前覆盖行数的最大值',
        'if used == cols': lambda S, B, r: (f"`used = {S.used}` 等于 `cols = {S.cols}`：选够了，数数能覆盖几行" if S.used == S.cols
                                            else f"`used = {S.used}` ≠ `cols = {S.cols}`：还没选够"),
        'if (now & need[index])': '`need[{index}] = {need[index]}` 是不是 `now = {now}` 的子集？`now & need` = {now & need[index]} → {"是，覆盖" if (now & need[index]) == need[index] else "否"}',
        'cnt += 1': '这一行被覆盖，`cnt` → {cnt}',
        'self.res = max': '`self.res = max({B.self.res}, {cnt}) = {self.res}`',
        'if level == n': lambda S, B, r: (f"`level = {S.level}` 等于列数，列看完了但没选够 → 返回" if S.level == S.n
                                          else f"`level = {S.level}`，还有列可以选"),
        'dfs(now, used, level + 1)': '==不选==第 `{B.level}` 列，去看下一列',
        'dfs(now | (1 << level)': '==选==第 `{B.level}` 列：`now | (1 << {B.level})`，`used + 1`',
        'dfs(0, 0, 0)': '从空集合、已选 0 列、第 0 列开始搜索',
        'return self.res': '最多覆盖 `{self.res}` 行',
    },
    cards=dict(
        one_liner='列数不超过 12，直接 DFS 枚举选哪些列',
        complexity='时间 `O(2^n · m)`，空间 `O(n + m)`',
        problem=['二进制矩阵 `mat`，必须选 `cols` 个不同的列',
                 '一行里所有的 1 都在选中列中，这行就算被覆盖',
                 '示例：`[[0,0,0],[1,0,1],[0,1,1],[0,0,1]]`，选 2 列 → `3`'],
        quote='题目中列的总数不超过12，那么完全可以直接暴力dfs，枚举每一种选取列的方式，然后计算当前选取方式下能覆盖多少行。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理：每行需要哪些列，压成整数 `need[i]`',
              'DFS 对每一列做选或不选，选够 `cols` 列就停下来统计',
              '判断一行被覆盖：`now & need[i] == need[i]`，即需要的列都在 `now` 里'],
        summary=['时间 `O(2^n · m)`，空间 `O(n + m)`',
                 '`used == cols` 要放在 `level == n` 之前，选够就统计、不再往后走',
                 '返回值存在 `self.res`，因为内层 `dfs` 不方便改外层的局部变量',
                 '对比灵神：灵神用 Gosper 技巧只生成大小恰好为 `numSelect` 的集合，这里靠 `used` 剪枝'],
    ),
)
