MAT = [[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]]


def _color(S, i, j, v):
    if 'j' not in S or 'i' not in S:
        return None
    if i != S['i']:
        return None
    if j == S['j']:
        return 'blue'
    if j == (S['j'] + S['t']) % S['m']:
        return 'pink'
    return None


def _txt(S):
    if 't' not in S or 'j' not in S:
        return ''
    i, j, t, m = S['i'], S['j'], S['t'], S['m']
    a, b = (j + t) % m, S['mat'][i][(j + t) % m]
    return f"行 {i}：`t = {t}`，第 {j} 列的元素 `{S['mat'][i][j]}` 应移到第 `({j}+{t})%{m} = {a}` 列，该处是 `{b}`"


CONFIG = dict(
    num=2946, title='循环移位后的矩阵相似检查', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='统一成右移 t 位 · 逐元素对照',
    tags=['灵神题单', '贪心与思维', '难度分 1406'],
    code='''
class Solution(object):
    def areSimilar(self, mat, k):

        n = len(mat)
        m = len(mat[0])

        k %= m

        for i in range(n):
            if i % 2 == 0:
                t = m - k
            else:
                t = k

            for j in range(m):
                if mat[i][j] != mat[i][(j + t) % m]:
                    return False

        return True
''',
    call=f'Solution().areSimilar({MAT}, 2)',
    expect=True,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var='mat', color=_color, h=330),
    ],
    watch=['k', 'i', 't', 'j', ('m', 'm', 'cyan')],
    captions={
        'n = len': '`n = {n}` 行',
        'm = len': '`m = {m}` 列',
        'k %= m': '`k` 可能 ≥ 列数（套圈），先对 `m` 取模：`k = {k}`',
        'for i in range': '开始检查第 `{i}` 行',
        'if i % 2 == 0': '`i = {i}`：=={"偶数行，原本向左移" if i % 2 == 0 else "奇数行，原本向右移"}==',
        't = m - k': '向左移 `k` 位 ≡ 向右移 `m - k` 位 → `t = {m} - {k} = {t}`',
        't = k': '奇数行本来就是向右移 → `t = {t}`',
        'if mat[i][j] !=': lambda S, B, r: (
            f'第 {S.j} 列元素 `{S.mat[S.i][S.j]}` 右移 `{S.t}` 位到第 `{(S.j + S.t) % S.m}` 列，那里是 `{S.mat[S.i][(S.j + S.t) % S.m]}`：'
            + ('==不相等== → 这行移完就变了' if S.mat[S.i][S.j] != S.mat[S.i][(S.j + S.t) % S.m] else '相等，继续')),
        'return False': '有元素对不上 → 矩阵不相似，返回 `False`',
        'return True': '每一行每个位置都对得上 → 返回 `True`',
    },
    cards=dict(
        one_liner='先统一成「向右移 t 位」，再逐个对照目标位置',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['偶数行向左、奇数行向右各循环移位，重复 `k` 次',
                 '最后和原矩阵相同吗？',
                 '示例：`[[1,2,1,2],[5,5,5,5],[6,3,6,3]]`，`k = 2` → `true`'],
        quote='对于一个长度为m的数组，将其中的元素向左移动k位，就相当于将其中的元素向右移动m - k位，于是可以在进行比较之前可以先通过这个计算将问题都转化为每一行对应的数组向右移动的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k >= m` 会套圈，先 `k %= m`',
              '偶数行左移 k = 右移 `m - k`，奇数行右移 `k`',
              '原来第 `j` 列的元素会到 `(j + t) % m` 列：和那里的值对照即可'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '先取模再换算：`t = m - k` 在 `k = 0` 时等于 `m`，下标要 `% m`',
                 '对照对象是同一行的原数组，所以不用真的移位',
                 '对比灵神：他证明了无需分奇偶；yiduobo 分奇偶各算 t'],
    ),
)
