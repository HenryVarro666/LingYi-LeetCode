MAT = [[0, 1, 1], [1, 1, 1]]


def _info(S):
    if 'f' not in S or 'j' not in S:
        return ''
    j = S['j']
    st = S.get('stack') or []
    h = S['height']
    if st:
        q = st[-1]
        return f"`f[{j}] = f[{q}] + ({j} − {q})×h[{j}]`（`q = {q}`）" if S.get('_line', 0) >= 20 else f"当前 `h[{j}] = {h[j]}`"
    return f"栈空：`f[{j}] = h[{j}] × ({j}+1)`" if S.get('_line', 0) >= 20 else f"当前 `h[{j}] = {h[j]}`"


CONFIG = dict(
    num=1504, title='统计全 1 子矩形', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='高度 + 单调栈 · f[i][j] 以 (i,j) 为右下角',
    tags=['灵神题单·单调栈'],
    code='''
class Solution(object):
    def numSubmat(self, mat):

        m = len(mat)
        n = len(mat[0])
        
        res = 0
        height = [0] * n
        for i in range(m):
            f = [0] * n
            stack = []
            for j in range(n):
                if mat[i][j] == 0:
                    height[j] = 0
                elif i == 0:
                    height[j] = mat[i][j]
                else:
                    height[j] += 1
                while stack and height[stack[-1]] >= height[j]:
                    stack.pop()
                
                if not stack:
                    f[j] = height[j] * (j + 1)
                else:
                    f[j] = f[stack[-1]] + height[j] * (j - stack[-1])

                res += f[j]

                stack.append(j)
            
        return res
''',
    call=f'Solution().numSubmat({MAT})',
    expect=12,
    skip=['m = len', 'n = len', 'res = 0', 'height = [0]', 'if mat[i][j] == 0', 'elif i == 0', 'for j in range(n)'],
    views=[
        dict(type='grid', var='mat', h=200, cell=60, label='mat（黄 = 当前行，蓝 = 当前 (i, j)）',
             color=lambda S, i, j, v: ('blue' if i == S['i'] and j == S.get('j') else ('yellow' if i == S['i'] else None)) if 'i' in S else None),
        dict(type='array', var='height', pointers={'j': 'blue'}, h=250, label='height（每列向上连续 1 的个数）',
             color=lambda S, i, v: 'blue' if S.get('j') == i else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}', label='stack（下标，高度严格递增，栈顶在右）', h=140),
        dict(type='array', var='f', label='f（以 (i, j) 为右下角的全 1 子矩形数）', h=170,
             color=lambda S, i, v: 'green' if S.get('j') == i and S.get('_line', 0) >= 24 else None),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), ('stack', 'stack', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [0] * n': '第 `{i}` 行：`f[j]` 记录以 `(i, j)` 为右下角的矩形数',
        'stack = []': '栈重置，用来找每个 `j` 左边第一个更矮的柱子 `q`',
        'height[j] = 0': '`mat[{i}][{j}] = 0`：柱子断了，`height[{j}] = 0`',
        'height[j] = mat[i][j]': '第一行：`height[{j}] = {height[j]}`',
        'height[j] += 1': '`mat[{i}][{j}] = 1`：柱子长高，`height[{j}] = {height[j]}`',
        'while stack and height[stack[-1]]': lambda S, B, r: (
            "栈空，左边没有更矮的柱子" if not S.stack else
            f"栈顶 `height[{S.stack[-1]}] = {S.height[S.stack[-1]]}` ≥ `height[{S.j}] = {S.height[S.j]}` → ==弹出==，它不比当前矮"
            if S.height[S.stack[-1]] >= S.height[S.j] else
            f"栈顶 `height[{S.stack[-1]}] = {S.height[S.stack[-1]]}` < `{S.height[S.j]}` → ==q = {S.stack[-1]}== 就是左边第一个更矮的"),
        'stack.pop()': '弹出，`stack = {stack}`',
        'if not stack': lambda S, B, r: ('栈空：没有 `q`，左边界可以是 `0..j` 任意位置' if not S.stack else f'`q = {S.stack[-1]}`：左边界 `≤ q` 的情况可以复用 `f[{S.stack[-1]}]`'),
        'f[j] = height[j] * (j + 1)': '`f[{j}] = {height[j]} × ({j}+1)` = =={f[j]}==：宽度 1..j+1，高度 1..h',
        'f[j] = f[stack[-1]]': '`f[{j}] = f[{stack[-1]}] + {height[j]}×({j}−{stack[-1]})` = {f[stack[-1]]} + {height[j]*(j-stack[-1])} = =={f[j]}==',
        'res += f[j]': '累加：`res = {res}`',
        'stack.append(j)': '`{j}` 入栈，供右边更高的柱子当 `q`',
        'return res': '所有 `(i, j)` 为右下角的矩形数相加 =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] = f[q] + (j−q)×h[j]，q 是左边第一个更矮的柱子',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['给一个 `m×n` 的 0/1 矩阵，数一数有多少个子矩形里全是 1',
                 '示例：`[[0,1,1,0],[0,1,1,1],[1,1,1,0]]` → `24`',
                 '本视频：`[[0,1,1],[1,1,1]]` → `12`'],
        quote='若q是第一个满足h[q] < h[j]的位置，……因此一共可以形成(j - q) * h[j]个以mat[i][j]为右下角的全1子矩形。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 以 `mat[i][j]` 为右下角的全 1 子矩形数；`h[j]` 是这一列向上连续 1 的个数',
              '左边界在 `q+1..j`：宽 `j−q` 种 × 高 `h[j]` 种，全是新数的 `(j−q)×h[j]`',
              '左边界在 `q` 及更左：高度受限于 `h[q]`，直接接上 `f[q]`；`q` 用单调栈找'],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '`f` 的行维度可以省掉，每行重新开 `f` 和栈',
                 '栈空时 `f[j] = h[j] × (j+1)`，相当于 `q = -1`',
                 '原文本身已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神把 `f` 存进栈元组 `(j, f, h)`，这里单独开了数组 `f`'],
    ),
)
