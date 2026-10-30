A0, B0 = 'abc', 'bca'


def _c1(S, k, v):
    I = S.get('_inner', {})
    i, l = I.get('i'), I.get('l')
    if i is None or l is None:
        return None
    return 'blue' if i <= k < i + l else None


def _c2(S, k, v):
    I = S.get('_inner', {})
    j, l = I.get('j'), I.get('l')
    if j is None or l is None:
        return None
    return 'pink' if j <= k < j + l else None


def _fm(S):
    I = S.get('_inner', {})
    if 'i' not in I:
        return '`f[i][j][l]`：`s1` 从 `i` 起、`s2` 从 `j` 起、长度 `l` 的子串能否互为扰乱'
    i, j, l = I['i'], I['j'], I['l']
    a, b = S['s1'][i:i + l], S['s2'][j:j + l]
    return f'比较 `s1[{i}:{i+l}]` = =={a}== 与 `s2[{j}:{j+l}]` = =={b}=='


CONFIG = dict(
    num=87, title='扰乱字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 三维记忆化搜索',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def isScramble(self, s1, s2):

        n = len(s1)
        if len(s2) != n:
            return False

        f = [[[None] * (n + 1) for index in range(n)] for index in range(n)]
        return self.dfs(0, 0, n, s1, s2, f)

    def dfs(self, i, j, l, s1, s2, f):
        if f[i][j][l] is not None:
            return f[i][j][l]

        if l == 1:
            if s1[i] == s2[j]:
                f[i][j][l] = True
            else:
                f[i][j][l] = False
            return f[i][j][l]

        for left in range(1, l):
            right = l - left
            if self.dfs(i, j, left, s1, s2, f) and self.dfs(i + left, j + left, right, s1, s2, f):
                f[i][j][l] = True
                return True
            if self.dfs(i, j + right, left, s1, s2, f) and self.dfs(i + left, j, right, s1, s2, f):
                f[i][j][l] = True
                return True

        f[i][j][l] = False
        return False
''',
    call=f'Solution().isScramble({A0!r}, {B0!r})',
    expect=True,
    skip=['n = len(s1)', 'if len(s2)', 'return False\n'],
    views=[
        dict(type='string', var='s1', label='s1（蓝 = 当前比较的区间 i..i+l）', h=150, cell=80, color=_c1),
        dict(type='string', var='s2', label='s2（粉 = 当前比较的区间 j..j+l）', h=150, cell=80, color=_c2),
        dict(type='text', fn=_fm, size=26, h=60),
        dict(type='calls', h=240, hide=('s1', 's2', 'f')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('l', 'l', 'orange'), ('left', 'left', 'purple')],
    captions={
        'f = [[[None]': '`f[i][j][l]`：`s1` 从 `i`、`s2` 从 `j`、长度 `l` 能否扰乱得到；None 表示没算过',
        'return self.dfs(0, 0': '答案就是 `f[0][0][n]`，用记忆化搜索求',
        'if f[i][j][l] is not None': lambda S, B, r: (f'`f[{S.i}][{S.j}][{S.l}]` 算过了，直接返回' if S.f[S.i][S.j][S.l] is not None else '这个状态没算过，继续算'),
        'if l == 1': lambda S, B, r: (f'长度为 1：只需 `s1[{S.i}] = {S.s1[S.i]}` 与 `s2[{S.j}] = {S.s2[S.j]}` ' + ('==相同==' if S.s1[S.i] == S.s2[S.j] else '不同')
                                       if S.l == 1 else f'长度 `{S.l}`：枚举分隔点 `left`'),
        'f[i][j][l] = True': '`f[{i}][{j}][{l}] = True`',
        'f[i][j][l] = False': '`f[{i}][{j}][{l}] = False`',
        'for left in range': '枚举分隔点：`s1` 切成长度 `left` 和 `{l}-left` 两段',
        'right = l - left': '`left = {left}`，`right = {right}`',
        'if self.dfs(i, j, left': '不交换：`s1` 前 {left} 个对 `s2` 前 {left} 个，`s1` 后 {right} 个对 `s2` 后 {right} 个，两段都要成立',
        'if self.dfs(i, j + right': '交换：`s1` 前 {left} 个对 `s2` ==后== {left} 个，`s1` 后 {right} 个对 `s2` ==前== {right} 个',
        'return True': '找到可行分割，返回 ==True==',
        'return f[i][j][l]': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='枚举分隔点，两段「不交换」或「交换」都试一遍',
        complexity='时间 `O(n^4)`，空间 `O(n^3)`',
        problem=['把字符串切成两段，可以交换两段，再对每段递归地同样操作，得到的是 `s1` 的扰乱字符串',
                 '判断 `s2` 是否为 `s1` 的扰乱字符串',
                 '示例：`"great"` 与 `"rgeat"` → `true`；本视频：`"abc"` 与 `"bca"` → `true`'],
        quote='设f[i][j][l]表示s1从i开始，s2从j开始，长度为l的字串是否能经过反转然后匹配上。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l == 1`：两个字符相等才行',
              '`l > 1`：枚举分隔点 `left`，`right = l - left`',
              '不扰乱：`s1` 前段配 `s2` 前段，后段配后段；扰乱：前段配 `s2` 的后段，后段配前段',
              '三个维度的状态，转移枚举一维，所以 `O(n^4)`'],
        summary=['时间 `O(n^4)`，空间 `O(n^3)`',
                 '易错：交换时 `s2` 的起点是 `j + right`，而 `s1` 后段对应 `s2` 的 `j`',
                 '易错：记忆数组第三维开 `n + 1`，因为长度可取到 `n`',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行',
                 '题意（原文未写）：将字符串切成两个非空部分，可交换，递归对每部分进行同样操作'],
    ),
)
