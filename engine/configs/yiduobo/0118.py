def _new_row(S):
    if 'index' not in S or 'f' not in S:
        return None
    idx, f = S['index'], S['f']
    if len(f) > idx:
        return f[idx]
    prev = f[idx - 1]
    k = S.get('i', 0)
    mid = [prev[t - 1] + prev[t] for t in range(1, k + 1)]
    return [1] + mid + ['?'] * (len(prev) - 1 - k) + ['?']


def _row_color(S, j, v):
    if 'index' not in S:
        return None
    if v == '?':
        return None
    row = _new_row(S)
    if j == 0 or (j == len(row) - 1):
        return 'green'
    if 'i' in S and j == S['i']:
        return 'orange'
    return 'purple'


def _grid_color(S, r, c, v):
    if 'index' not in S:
        return None
    idx, f = S['index'], S['f']
    if len(f) > idx and r == idx:
        return 'green'
    if len(f) > idx and r == idx - 1:
        return 'blue'
    if 'i' in S and r == idx - 1:
        if c == S['i'] - 1:
            return 'blue'
        if c == S['i']:
            return 'pink'
    return None


def _formula(S):
    if 'index' not in S:
        return '前两行直接给出：`[1]`、`[1, 1]`' if 'f' in S else ''
    idx, f = S['index'], S['f']
    if len(f) > idx:
        p = f[idx - 1]
        sums = ', '.join(f'{p[t - 1]}+{p[t]}' for t in range(1, len(p)))
        return f'`[1] + [{sums}] + [1]` = `{f[idx]}`'
    p = f[idx - 1]
    if 'i' in S:
        i = S['i']
        return f'新行第 `{i}` 个 = `f[{idx - 1}][{i - 1}] + f[{idx - 1}][{i}]` = {p[i - 1]} + {p[i]} = =={p[i - 1] + p[i]}=='
    return f'第 `{idx}` 行 = `[1]` + 上一行 `{p}` 的相邻两数之和 + `[1]`'


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('blue', '上一行 f[index-1]'), ('green', '新行 / 两头的 1'), ('purple', '新行中间：相邻两数之和')]:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 30


def _cap_append(S, B, ret):
    idx, f = S.index, S.f
    if 'i' in S:
        p = f[idx - 1]
        i = S.i
        return f'推导式第 `{i}` 轮：上一行相邻两数 `{p[i - 1]} + {p[i]}` = =={p[i - 1] + p[i]}=='
    p = f[idx - 1]
    sums = '、'.join(f'{p[t - 1]}+{p[t]}' for t in range(1, len(p)))
    return f'推导式把上一行==相邻两数逐对相加==（{sums}），两头补 `[1]`，`append` 新行 `{f[idx]}`'


CONFIG = dict(
    num=118, title='杨辉三角', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='逐行拼接：[1] + 相邻和 + [1]',
    code='''
class Solution(object):
    def generate(self, numRows):
        if numRows == 0:
            return []

        if numRows == 1:
            return [[1]]

        f = [[1], [1, 1]]
        for index in range(2, numRows):
            f.append([1] + [f[index - 1][i - 1] + f[index - 1][i] for i in range(1, len(f[index - 1]))] + [1])

        return f
''',
    call='Solution().generate(6)',
    expect=[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='f', color=_grid_color, rows=lambda S: [f'{k}' for k in range(len(S['f']))],
             cell=64, h=440),
        dict(type='array', var=_new_row, label='新的一行（[1] + 相邻和 + [1]）', color=_row_color, cell=72, h=140),
        dict(type='custom', draw=_legend, h=46),
    ],
    watch=[('index', 'index', 'orange'), ('i', 'i', 'orange'), ('len(f)', 'len(f)')],
    captions={
        'if numRows == 0': '特判：`numRows = 0` 返回空列表；这里 `numRows = {numRows}`',
        'if numRows == 1': '特判：只要 1 行就直接返回 `[[1]]`',
        'f = [[1], [1, 1]]': '前两行没有「中间的数」，==直接写出来==',
        'for index in': lambda S, B, ret: (f'第 `{S.index}` 行：上一行 `{S.f[S.index - 1]}` 有 `{len(S.f[S.index - 1])}` 个数 → '
                                           f'相邻对 `{len(S.f[S.index - 1]) - 1}` 个'
                                           if B.get('index') != S.index else f'`f` 已有 `{len(S.f)}` 行，循环结束'),
        'f.append(': _cap_append,
        'return f': '返回 `f`，共 `{len(f)}` 行',
    },
    cards=dict(
        one_liner='新的一行 = [1] + 上一行相邻两数之和 + [1]，一行代码拼出来',
        complexity='时间 `O(numRows²)`，空间 `O(1)`（返回值不计入）',
        problem=['生成「杨辉三角」的前 `numRows` 行',
                 '每个数是它==左上方和右上方==的数的和',
                 '示例：`numRows = 5` → `[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]`'],
        quote='118题需要求出所有的数字，119题则是求出某一层的数字即可。==可以按照题目动画给出的动态规划方法来求==。',
        quote_src='—— yiduobo 题解',
        idea=['每个数 = 上一行==相邻两个数==之和；首尾永远是 1',
              '上一行 `m` 个数 → `m-1` 个相邻对 → 新行 `1 + (m-1) + 1 = m+1` 个',
              '前两行特殊，直接写；之后每行用一个列表推导式 `append` 进去'],
        after=[dict(heading='yiduobo 的另一视角：二项式定理', lines=[
            '杨辉三角本质上就是==二项式定理==：第 k 行是 `(x+1)^k` 展开的系数',
            '第 k 行 = `C(k,0), C(k,1), …, C(k,k)`；`C(k,j) = C(k,j-1)·(k-j+1)/j`',
            '`C(m,n) = C(m,m-n)`：只求一半，再反过来复制一遍（119 题的做法）',
        ])],
        summary=['时间 `O(numRows²)`；除返回值外 `O(1)` 额外空间',
                 '原文为 Python 2 写法：本题仅删去 docstring，代码可直接在 Python 3 运行',
                 '`range(1, len(f[index - 1]))`：相邻对个数 = 上一行长度 − 1',
                 '前两行要特判（或直接写出），从 `index = 2` 开始拼'],
    ),
)
