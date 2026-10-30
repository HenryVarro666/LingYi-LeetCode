def _pos(i, j, n=2):
    return [(i, j), (j, n - i - 1), (n - i - 1, n - j - 1), (n - j - 1, i)]


def _tc(S, i, j, v):
    if 'i' not in S or 'j' not in S:
        return None
    for k, p in enumerate(_pos(S['i'], S['j'])):
        if p == (i, j):
            return ['blue', 'pink', 'orange', 'purple'][k]
    return None


def _txt(S):
    if 'impossible' not in S:
        return ''
    return '还可能的旋转次数：' + ('、'.join(f'==转{k}次==' for k in range(4) if k not in S['impossible']) or '无')


def _cmp(k):
    def f(S, B, r):
        i, j, t = S.i, S.j, S.target
        a, b = _pos(i, j)[k]
        x = S.mat[i][j]
        return f'转 {k} 次：`mat[{i}][{j}] = {x}` 对 `target[{a}][{b}] = {t[a][b]}`' + (' → 相同' if x == t[a][b] else f' → 不同，转 {k} 次不可能')
    return f


CONFIG = dict(
    num=1886, title='判断矩阵经轮转后是否一致', difficulty='Easy', category='模拟',
    author='yiduobo', technique='公式推导 · 逐格排除旋转次数',
    code='''
class Solution(object):
    def findRotation(self, mat, target):

        n = len(mat)
        impossible = set()
        for i in range(n):
            for j in range(n):
                if mat[i][j] != target[i][j]:
                    impossible.add(0)
                if mat[i][j] != target[j][n - i - 1]:
                    impossible.add(1)
                if mat[i][j] != target[n - i - 1][n - j - 1]:
                    impossible.add(2)
                if mat[i][j] != target[n - j - 1][i]:
                    impossible.add(3)
                
                if len(impossible) == 4:
                    return False

        return True
''',
    call='Solution().findRotation([[0,1],[1,0]], [[1,0],[0,1]])',
    expect=True,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 当前格 (i,j)）', cursors=[('i', 'j', 'yellow', '(i,j)')], cell=110, h=290),
        dict(type='grid', var='target', label='target（蓝/粉/橙/紫 = 转 0/1/2/3 次后要对上的格子）', cell=110, h=290, color=_tc),
        dict(type='text', size=30, h=90, fn=_txt),
    ],
    watch=['i', 'j', ('impossible', 'sorted(impossible)', 'red')],
    max_steps=130,
    captions={
        'n = len(mat)': '矩阵边长 `n = {n}`',
        'impossible = set()': '`impossible` 记录已被排除的旋转次数，开始为空',
        'for i in range': '换到下一行（行都看完则结束），当前行号 `{i}`',
        'for j in range': '取下一个格子（本行取完则换行），上一个是 `({i},{j})`，对照它转 0/1/2/3 次后的落点',
        'if mat[i][j] != target[i][j]': _cmp(0),
        'if mat[i][j] != target[j][n - i - 1]': _cmp(1),
        'if mat[i][j] != target[n - i - 1][n - j - 1]': _cmp(2),
        'if mat[i][j] != target[n - j - 1][i]': _cmp(3),
        'impossible.add': '排除这种转法：`impossible = {sorted(impossible)}`',
        'if len(impossible) == 4': lambda S, B, r: ('四种转法全被排除 → 返回 False' if len(S.impossible) == 4 else f'已排除 `{len(S.impossible)}` 种，还没排光，继续'),
        'return True': '每个格子都看过，还剩转法没被排除（`impossible = {sorted(impossible)}`）→ 返回 ==True==',
    },
    cards=dict(
        one_liner='转 0~3 次的落点是固定公式，逐格验证并排除不可能的次数',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['给两个 `n×n` 的 0/1 矩阵 `mat` 和 `target`，可把 `mat` 顺时针转 90° 若干次',
                 '能否让 `mat` 和 `target` 一致',
                 '本视频：`[[0,1],[1,0]]` 转 1 次可一致 → `true`'],
        quote='格子(x, y)，经过一次轮转之后是(y, n - x - 1) ……第四次轮转就回到了原位(x, y)，也就是说，只需要考察轮转0到3次的可能性。',
        quote_src='—— yiduobo 题解原文',
        idea=['先推公式：一次轮转 `(x,y)→(y,n-x-1)`，代入得两次 `(n-x-1,n-y-1)`，三次 `(n-y-1,x)`',
              '四次回到原位，所以只需验证转 0、1、2、3 次',
              '某个格子转 k 次后对不上 target，就把 k 放进 `impossible`；四个都进去了就返回 False'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '公式里要写 `n - i - 1`，别漏掉 `- 1`',
                 '`impossible` 用集合，重复添加不会变多，长度为 4 才表示全排除',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
