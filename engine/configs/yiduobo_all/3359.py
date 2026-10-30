GRID = [[4, 3, 4], [2, 3, 1]]
K = 4


def _txt(S):
    ln = S.get('_line', 0)
    if ln >= 20 and 'j' in S and 'g' in S and 'stack' in S:
        return f"第 `{S['j']}` 列：自上而下用单调栈（栈里存 f 递增的行），算以 `(i, j)` 为右下角的子矩阵数 g"
    if ln >= 5 and 'f' in S and 'g' not in S:
        return f"先算 f：每格向左最多连续非递增扩几列（`> k` 的格子记 0），k = {S['k']}"
    return f"k = {K}；数「每行非递增、最大值 ≤ k」的子矩阵"


def _fcol(S, i, j, v):
    if 'i' in S and 'j' in S and S.get('_line', 0) < 20 and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return None


def _gcol(S, i, j, v):
    if 'g' in S and 'i' in S and S.get('_line', 0) >= 20 and (i, j) == (S['i'], S['j']):
        return 'yellow'
    return None


def _gridcol(S, i, j, v):
    if v > S['k']:
        return 'red'
    if S.get('_line', 0) < 20 and (i, j) == (S.get('i'), S.get('j')):
        return 'yellow'
    return None


CONFIG = dict(
    num=3359, title='查找最大元素不超过K的有序子矩阵', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='按行预处理 f + 逐列单调栈累计 g',
    tags=[],
    code='''
class Solution(object):
    def countSubmatrices(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] <= k:
                    if j > 0 and grid[i][j] <= grid[i][j - 1]:
                        f[i][j] = f[i][j - 1] + 1
                    else:
                        f[i][j] = 1
        
        g = [[0] * n for _ in range(m)]
        res = 0
        for j in range(n):
            stack = []
            for i in range(m):
                while stack and f[i][j] < f[stack[-1]][j]:
                    stack.pop()

                if stack:
                    g[i][j] = g[stack[-1]][j] + (i - stack[-1]) * f[i][j]
                else:
                    g[i][j] = (i + 1) * f[i][j]
                
                stack.append(i)
                res += g[i][j]
        
        return res
''',
    call=f'Solution().countSubmatrices({GRID!r}, {K})',
    expect=11,
    skip=['m = len', 'n = len', 'f = [[0]', 'g = [[0]', 'stack.pop()', 'if stack:', 'stack = []'],
    max_steps=100,
    views=[
        dict(type='text', h=50, size=26, fn=_txt),
        dict(type='grid', var='grid', label='grid（红 = 大于 k）', h=150, cell=64,
             color=_gridcol),
        dict(type='grid', var='f', label='f：向左能扩几列', h=150, cell=64, color=_fcol),
        dict(type='grid', var='g', label='g：以该格为右下角的子矩阵数', h=150, cell=64, color=_gcol),
        dict(type='stack', var='stack', h=70, fmt=lambda i: str(i)),
    ],
    watch=['i', 'j', ('res', 'res', 'green'), ('k', 'k', 'cyan')],
    captions={
        'if grid[i][j] <= k': lambda S, B, ret: (
            f"`grid[{S['i']}][{S['j']}] = {S['grid'][S['i']][S['j']]}` `<= k = {S['k']}`：==成立==，这格可以用"
            if S['grid'][S['i']][S['j']] <= S['k'] else
            f"`grid[{S['i']}][{S['j']}] = {S['grid'][S['i']][S['j']]}` `> k = {S['k']}`：不成立 → `f` 保持 0，任何子矩阵都不能含它"),
        'if j > 0 and grid': lambda S, B, ret: (
            f"左边 `{S['grid'][S['i']][S['j']-1]}` `>=` 当前 `{S['grid'][S['i']][S['j']]}`，行仍非递增：==可以接在左边那段后面=="
            if S['j'] > 0 and S['grid'][S['i']][S['j']] <= S['grid'][S['i']][S['j']-1] else
            ('`j = 0`：左边没有格子，只能自己成一段' if S['j'] == 0 else f"左边 `{S['grid'][S['i']][S['j']-1]}` 比当前 `{S['grid'][S['i']][S['j']]}` 小，非递增断了：只能自己成一段")),
        'f[i][j] = f[i][j - 1] + 1': '接上：`f[{i}][{j}] = f[{i}][{j-1}] + 1 = {f[i][j]}`',
        'f[i][j] = 1': '重新开始：`f[{i}][{j}] = 1`',
        'while stack and': lambda S, B, ret: (
            f"栈顶行 `{S['stack'][-1]}` 的 `f = {S['f'][S['stack'][-1]][S['j']]}` 比当前 `f[{S['i']}][{S['j']}] = {S['f'][S['i']][S['j']]}` ==大==：它向左扩得更远，限制不了当前，弹出"
            if S['stack'] and S['f'][S['i']][S['j']] < S['f'][S['stack'][-1]][S['j']] else
            ('栈空：这一列上方没有更窄的行' if not S['stack'] else f"栈顶行 `{S['stack'][-1]}` 的 `f = {S['f'][S['stack'][-1]][S['j']]}` 不大于当前 `{S['f'][S['i']][S['j']]}`：它就是上一个更窄（或相等）的行 `p`")),
        'g[i][j] = g[stack[-1]][j]': '左上角在 `p+1..i` 行：`({i}-{stack[-1]}) × f = {(i - stack[-1]) * f[i][j]}` 个；左上角在 `p` 行及以上的，直接借用 `g[{stack[-1]}][{j}] = {g[stack[-1]][j]}` → `g[{i}][{j}] = {g[i][j]}`',
        'g[i][j] = (i + 1)': '栈空：上面没有更窄的行，所有行都能向左扩 `f` 列：`({i}+1) × {f[i][j]} = {g[i][j]}`',
        'stack.append(i)': '行 `{i}` 入栈',
        'res += g[i][j]': '把以 `({i}, {j})` 为右下角的 `{g[i][j]}` 个累加：`res = {res}`',
    },
    cards=dict(
        one_liner='先按行算向左能扩几列，再逐列用单调栈累计子矩阵数',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给定 `m × n` 矩阵 `grid` 和 `k`，数满足两个条件的子矩阵：',
                 '1. 最大元素 `<= k`　2. ==每一行都是非递增==的',
                 '视频用 `2×3` 矩阵、`k=4` 演示，答案 `11`'],
        quote='令f[i][j]表示以第i行，第j列为结尾，且所有元素都小于等于k的最长非递增子数组的长度。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]`：行内向左最多能连续非递增扩几列，`> k` 记 0',
              '`f[i][j]` 就是以 `(i, j)` 为右下角的子矩阵宽度上限，上方更窄的行 `p` 会卡住',
              '`g[i][j] = (i-p)·f[i][j] + g[p][j]`；`p` 用单调栈找，逐列扫描'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：`grid[i][j] > k` 时 `f` 必须为 0，下一格接不上它',
                 '栈空时 `g = (i+1)·f`；非空时借用 `g[p][j]`，不会漏数也不会重复',
                 '单调栈弹出条件是 `f[i][j] < f[栈顶][j]`，相等不弹'],
    ),
)
