def _src_color(S, i, j, v):
    """A 中已经读过的格子：列优先，(j, i) 字典序在当前位置之前"""
    if 'j' not in S or 'res' not in S:
        return None
    res = S['res']
    done = j < len(res) and i < len(res[j])
    return 'green' if done else None


def show(S):
    if 'res' not in S:
        return '先列后行遍历 A，按先行后列的顺序写进答案'
    if 'i' in S and S.get('_line') == 10:
        return f"`res[{S['j']}]` 末尾追加 `A[{S['i']}][{S['j']}] = {S['A'][S['i']][S['j']]}`"
    if 'j' in S and S.get('_line') == 8:
        return f"开始处理 A 的第 `{S['j']}` 列 → 它会变成 `res` 的第 `{S['j']}` 行"
    if 'm' in S and 'n' in S:
        return f"`A` 是 `{S['m']}×{S['n']}`，`res` 将是 `{S['n']}×{S['m']}`"
    return '先列后行遍历 A，按先行后列的顺序写进答案'


CONFIG = dict(
    num=867, title='转置矩阵', difficulty='Easy', category='矩阵',
    author='yiduobo', technique='先列后行遍历 · 逐行 append',
    tags=['List.md'],
    code='''
class Solution(object):
    def transpose(self, A):
        res = []

        m = len(A)
        n = len(A[0])
        for j in range(n):
            res.append([])
            for i in range(m):
                res[-1].append(A[i][j])

        return res
''',
    call='Solution().transpose([[1,2],[3,4],[5,6]])',
    expect=[[1, 3, 5], [2, 4, 6]],
    views=[
        dict(type='grid', var='A', label='A（m × n = 3 × 2，黄框 = A[i][j]，绿 = 已读过）', h=300, cell=76,
             rows=lambda S: list(range(len(S['A']))), cols=lambda S: list(range(len(S['A'][0]))),
             cursors=[(lambda S: S['i'] if S.get('_line') in (9, 10) else None, 'j', 'yellow')], color=_src_color),
        dict(type='grid', var='res', label='res（逐行长出来，最终 n × m = 2 × 3）', h=230, cell=76,
             rows=lambda S: list(range(len(S['res']))) if S.get('res') else None,
             cols=lambda S: list(range(len(S['A']))),
             color=lambda S, r, c, v: 'green'),
        dict(type='text', fn=show, size=28, h=60),
    ],
    watch=[('j', 'j', 'pink'), ('i', 'i', 'yellow'), ('m', 'm'), ('n', 'n')],
    captions={
        'res = []': '答案 `res` 从空列表开始，一行一行往里加',
        'm = len(A)': '`A` 有 `m = {m}` 行',
        'n = len(A[0])': '`A` 有 `n = {n}` 列',
        'for j in range(n)': lambda S, B, ret: (f'==外层枚举列== `j = {S.j}`：A 的第 `{S.j}` 列会成为答案的第 `{S.j}` 行'
                                                if S.get('j') != B.get('j') else '每一列都处理完了'),
        'res.append([])': '答案新开一行 `res[{j}]`',
        'for i in range(m)': lambda S, B, ret: (f'内层枚举行 `i = {S.i}`'
                                                if S.get('i') != B.get('i') or B.get('j') != S.get('j') or 'i' not in B
                                                else f'第 `{S.j}` 列读完 → 答案第 `{S.j}` 行填满了'),
        'res[-1].append(A[i][j])': '`A[{i}][{j}] = {A[i][j]}` 追加到 `res[{j}]` 末尾：`res[{j}] = {res[-1]}`',
        'return res': '返回 `res = {ret}`',
    },
    cards=dict(
        one_liner='先列后行读 A，读到的数依次 append 到答案的新一行',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
        problem=['给你一个 `m×n` 的二维数组，返回它的==转置矩阵==',
                 '转置：沿主对角线翻转，==交换行索引与列索引==',
                 '示例：`[[1,2,3],[4,5,6]]` → `[[1,4],[2,5],[3,6]]`'],
        quote='根据转置矩阵的定义，我们只需==先列后行遍历==整个矩阵，然后依次将遍历到的数==按先行后列的顺序==加入到答案矩阵中即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['外层枚举 A 的列 `j`，每一列在答案里新开一行 `res.append([])`',
              '内层枚举行 `i`，把 `A[i][j]` 追加到这一行末尾',
              '不用预先开好 `n×m` 的数组，答案随遍历逐行长出来'],
        result='返回 `[[1,3,5],[2,4,6]]`：A 的第 0 列 `1,3,5` 变成了第 0 行 ✓',
        summary=['时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
                 '关键：遍历顺序换成「先列后行」，写入顺序就是答案的「先行后列」',
                 '对比灵神：他按行遍历，直接写 `ans[j][i]`，要先建好 `n×m` 的数组',
                 '原文为 Python 2 风格：删去了文档字符串，逻辑未改'],
    ),
)
