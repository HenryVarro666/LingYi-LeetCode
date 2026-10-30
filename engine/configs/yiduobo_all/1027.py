A0 = [9, 4, 7, 2, 10]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if r == i and c == j:
        return 'yellow'
    pre = S.get('pre')
    if S.get('_line', 0) in (11, 12, 13) and pre in S.get('pos_dict', {}) and (r, c) == (S['pos_dict'][pre], i):
        return 'green'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'pre' not in S or S.get('_line', 0) not in (10, 11, 12, 13):
        return '`f[i][j]`：以 `A[i]`、`A[j]` 为最后两项的等差数列最长长度（至少 2）'
    A = S['A']
    base = f'公差 `{A[j]} − {A[i]}` = {A[j] - A[i]}，`pre = {A[i]} + {A[i]} − {A[j]}` = =={S["pre"]}=='
    pd = S['pos_dict']
    if S['pre'] in pd:
        k = pd[S['pre']]
        return base + f'\n`pre` 最后出现在下标 {k} → 接在 `f[{k}][{i}]` = {S["f"][k][i]} 后面'
    return base + '\n`pre` 之前没出现过 → 只有 `A[i], A[j]` 两项'


CONFIG = dict(
    num=1027, title='最长等差数列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维 DP f[i][j] · 倒推前一项 + 最后出现位置',
    tags=['灵神题单', '动态规划', '难度分 1759'],
    code='''
class Solution(object):
    def longestArithSeqLength(self, A):

        n = len(A)
        f = [[2] * n for _ in range(n - 1)]
        pos_dict = {}
        res = 2
        for i in range(n - 1):
            for j in range(i + 1, n):
                pre = A[i] + A[i] - A[j]
                if pre in pos_dict:
                    f[i][j] = max(f[i][j], f[pos_dict[pre]][i] + 1)
                res = max(res, f[i][j])

            pos_dict[A[i]] = i

        return res
''',
    call=f'Solution().longestArithSeqLength({A0!r})',
    expect=3,
    skip=['for j in range', 'for i in range'],
    views=[
        dict(type='array', var='A', label='A（蓝 = i，粉 = j）', h=240, cell=96,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿 = 它依赖的 f[k][i]）', h=320, cell=70,
             rows=lambda S: [f'{k}:{x}' for k, x in enumerate(S['A'][:-1])],
             cols=lambda S: [f'{k}:{x}' for k, x in enumerate(S['A'])], color=_cell),
        dict(type='map', var='pos_dict', label='pos_dict（数 → 最后出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=130, font=26),
        dict(type='text', fn=_txt, size=24, h=110, lines=3),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pre', 'pre', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len(A)': '`n = {n}`',
        'f = [[2] * n': '`f[i][j]` 默认 2：任意两个数都能组成长度为 2 的等差数列；只需要 `i < j`，所以有 `n−1` 行',
        'pos_dict = {}': '`pos_dict[x]`：数 `x` 最后一次出现在 `A` 的哪个下标（只记 `i` 之前的）',
        'res = 2': '答案至少是 2',
        'pre = A[i]': lambda S, B, r: (f'末两项是 `A[{S.i}]={S.A[S.i]}`、`A[{S.j}]={S.A[S.j]}`，公差 `{S.A[S.j] - S.A[S.i]}`'
                                       f' → 再往前一项 `pre = {S.pre}`'),
        'if pre in pos_dict': lambda S, B, r: (f'`pre = {S.pre}` 在 `i` 之前出现过（下标 {S.pos_dict[S.pre]}）→ 可以往前接' if S.pre in S.pos_dict
                                               else f'`pre = {S.pre}` 在 `i` 之前没出现过 → 保持 2'),
        'f[i][j] = max': lambda S, B, r: (f'`f[{S.i}][{S.j}] = max(2, f[{S.pos_dict[S.pre]}][{S.i}] + 1)` = =={S.f[S.i][S.j]}==；'
                                          '多个相同的 pre 取==最靠后==的那个'),
        'res = max': '`res = max({B.res}, f[{i}][{j}]) = {res}`',
        'pos_dict[A[i]] = i': '`A[{i}]` 处理完，登记它的位置：`pos_dict[{A[i]}] = {i}`（后出现的覆盖先出现的）',
        'return res': '最长等差数列长度 = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='用最后两项定公差，倒推出前一项，去字典里找它最靠后的位置',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你整数数组 `nums`，返回其中==最长等差子序列==的长度',
                 '子序列不要求连续，相邻两项差都相同',
                 '示例：`[9,4,7,2,10]` → `3`（4,7,10）'],
        quote='令f[i][j]表示以A[i]以及A[j]作为末尾两项的等差数列的最长长度，那么对于f[i][j]，该等差数列的公差为A[j] - A[i]，因此A[i]的前一项pre的大小就应该是 A[i] + A[i] - A[j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 是二维状态：末两项 `(A[i], A[j])` 定下了公差',
              '前一项 `pre = 2·A[i] − A[j]`；若它出现在 `i` 之前，就从 `f[k][i]` 转移',
              '相同的 pre 有多个时取最靠后的，用 `pos_dict` 记每个数最后出现的位置'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：`pos_dict` 要在内层循环结束后才登记 `A[i]`，保证只找到 `i` 之前的位置',
                 '`f[i][j]` 默认 2，答案 `res` 也从 2 开始',
                 '对比灵神：灵神用“结尾 + 公差”的哈希表 `f[i][d]`，yiduobo 用“末两项”的二维表'],
    ),
)
