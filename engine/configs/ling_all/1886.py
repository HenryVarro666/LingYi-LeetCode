def _pos(i, j, n=2):
    return [(i, j), (j, n - 1 - i), (n - 1 - i, n - 1 - j), (n - 1 - j, i)]


def _tc(S, i, j, v):
    if 'i' not in S or 'j' not in S:
        return None
    for k, p in enumerate(_pos(S['i'], S['j'])):
        if p == (i, j):
            return ['blue', 'pink', 'orange', 'purple'][k]
    return None


def _txt(S):
    if S.get('ok') is None:
        return ''
    return '还没被排除的旋转次数：' + ('、'.join(f'==转{k}次==' for k in range(4) if S['ok'] >> k & 1) or '无')


def _cmp(k):
    def f(S, B, r):
        i, j, x, t = S.i, S.j, S.x, S.target
        a, b = _pos(i, j)[k]
        same = x == t[a][b]
        return f'转 {k} 次：`{x}` 对 `target[{a}][{b}] = {t[a][b]}`' + (' → 相同' if same else f' → 不同，排除转 {k} 次')
    return f


def _clr(k):
    return lambda S, B, r: f'清掉第 {k} 位：转 {k} 次不可能 → `ok = {S.ok:04b}`'


CONFIG = dict(
    num=1886, title='判断矩阵经轮转后是否一致', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='位掩码 · 直接比较四种旋转',
    code='''
class Solution:
    def findRotation(self, mat: List[List[int]], target: List[List[int]]) -> bool:
        ok = (1 << 4) - 1  # ok = [True] * 4
        for i, row in enumerate(mat):
            for j, x in enumerate(row):
                if x != target[i][j]:
                    ok &= ~(1 << 0)  # ok[0] = False
                if x != target[j][-1 - i]:
                    ok &= ~(1 << 1)  # ok[1] = False
                if x != target[-1 - i][-1 - j]:
                    ok &= ~(1 << 2)  # ok[2] = False
                if x != target[-1 - j][i]:
                    ok &= ~(1 << 3)  # ok[3] = False
                if ok == 0:  # 所有的 ok[i] 都是 False
                    return False
        return True  # 至少有一个 ok[i] 是 True
''',
    call='Solution().findRotation([[0,1],[1,0]], [[1,0],[0,1]])',
    expect=True,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 当前格 x）', cursors=[('i', 'j', 'yellow', 'x')], cell=110, h=290),
        dict(type='grid', var='target', label='target（蓝/粉/橙/紫 = x 转 0/1/2/3 次后要对上的格子）', cell=110, h=290, color=_tc),
        dict(type='text', size=30, h=90, fn=_txt),
    ],
    watch=['i', 'j', 'x', ('ok', 'format(ok, "04b")', 'green')],
    max_steps=130,
    captions={
        'ok = (1 << 4)': '`ok` 的 4 个二进制位代表转 0/1/2/3 次是否还可能：初始全 1 = `{ok:04b}`',
        'for i, row': '换到下一行（行都看完则结束），当前行号 `{i}`',
        'for j, x': '取下一个格子（本行取完则换行），上一个是 `({i},{j})`，对照它转 0/1/2/3 次后的四个落点',
        'if x != target[i][j]': _cmp(0),
        'if x != target[j][-1 - i]': _cmp(1),
        'if x != target[-1 - i][-1 - j]': _cmp(2),
        'if x != target[-1 - j][i]': _cmp(3),
        'ok &= ~(1 << 0)': _clr(0),
        'ok &= ~(1 << 1)': _clr(1),
        'ok &= ~(1 << 2)': _clr(2),
        'ok &= ~(1 << 3)': _clr(3),
        'if ok == 0': lambda S, B, r: ('`ok = 0`：四种旋转都被排除 → 直接返回 False' if S.ok == 0 else f'`ok = {S.ok:04b}` 还不为 0，继续'),
        'return True': '格子全看完，`ok = {ok:04b}` 里还有 1 → 至少一种旋转成立，返回 ==True==',
    },
    cards=dict(
        one_liner='不真转矩阵：每个格子同时对照四种旋转后的位置，用 4 位掩码记哪些还成立',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['给两个 `n×n` 的 0/1 矩阵 `mat` 和 `target`，可把 `mat` 顺时针转 90° 若干次',
                 '能否让 `mat` 和 `target` 一致',
                 '本视频：`[[0,1],[1,0]]` 转 1 次可一致 → `true`'],
        quote='顺时针旋转 90° 后，位于 (i,j) 的元素去哪了？ (i,j) → (j,n-1-i) → (n-1-i,n-1-j) → (n-1-j,i)',
        quote_src='—— 灵茶山艾府题解',
        idea=['(i,j) 转 1/2/3 次后分别落在三个固定位置，加上原位共四个',
              '对每个 `mat[i][j]`，同时和 `target` 的这四个位置比较',
              '`ok` 第 k 位表示转 k 次还成立；某格不符就清掉那一位，全清零提前返回'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '用负下标 `-1 - i` 代替 `n - 1 - i`，省掉变量 n',
                 '`ok &= ~(1 << k)` 清第 k 位，`ok == 0` 即四种全排除',
                 '另一种写法：先枚举 mat 转 0~3 次（原地转置+行翻转，见 48 题）再比较，同样 `O(n^2)`'],
    ),
)
