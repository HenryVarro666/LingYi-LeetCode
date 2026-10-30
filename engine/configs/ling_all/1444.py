PIZZA = ['A..', 'AAA']


def _txt(S):
    if 'f' not in S or 'i' not in S or 'j' not in S or '_inner' not in S or 'col_s' not in S.get('_inner', {}):
        return '`s` = 二维后缀和（右下角固定），`f[i][j]` = 左上角在 `(i,j)` 的披萨切 `c` 刀的方案数'
    i, j = S['i'], S['j']
    if not 18 <= S.get('_line', 0) <= 23:
        return '`f` 滚动更新：先看左/上边界有没有苹果，都有才用行、列后缀和相加'
    s = S['s']
    if s[i][j] == s[i][j + 1]:
        return f'左边界（第 {j} 列）没有苹果：`f[{i}][{j}] = f[{i}][{j + 1}]`'
    if s[i][j] == s[i + 1][j]:
        return f'上边界（第 {i} 行）没有苹果：`f[{i}][{j}] = f[{i + 1}][{j}]`'
    return f'边界都有苹果：`f[{i}][{j}] = 第 {i} 行后缀和 {S["row_s"]} + 第 {j} 列后缀和 {S["col_s"][j]}`'


def _fcol(S, i, j, v):
    if 'i' in S and 'j' in S and i == S['i'] and j == S['j'] and S.get('_line', 0) >= 18:
        return 'yellow'
    return None


CONFIG = dict(
    num=1444, title='切披萨的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多维 DP + 二维后缀和 + 空间优化',
    tags=['灵神题单', '多维 DP', '难度分 2127'],
    code='''
class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10 ** 9 + 7
        m, n = len(pizza), len(pizza[0])
        s = [[0] * (n + 1) for _ in range(m + 1)]  # 二维后缀和
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                s[i][j] = s[i][j + 1] + s[i + 1][j] - s[i + 1][j + 1] + (pizza[i][j] == 'A')
                if s[i][j]: f[i][j] = 1  # 初始值

        for _ in range(1, k):
            col_s = [0] * n  # col_s[j] 表示 f 第 j 列的后缀和
            for i in range(m - 1, -1, -1):
                row_s = 0  # f[i] 的后缀和
                for j in range(n - 1, -1, -1):
                    tmp = f[i][j]
                    if s[i][j] == s[i][j + 1]:  # 左边界没有苹果
                        f[i][j] = f[i][j + 1]
                    elif s[i][j] == s[i + 1][j]:  # 上边界没有苹果
                        f[i][j] = f[i + 1][j]
                    else:  # 左边界上边界都有苹果，那么无论怎么切都有苹果
                        f[i][j] = (row_s + col_s[j]) % MOD
                    row_s += tmp
                    col_s[j] += tmp
        return f[0][0]
''',
    call=f'Solution().ways({PIZZA!r}, 2)',
    expect=3,
    max_steps=95, skip=['MOD = 10', 'm, n = len', 'tmp = f[i][j]', 'for j in range', 'row_s += tmp'],
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='table', var='pizza', label='pizza（绿 = 苹果）', h=190, cell=50,
             color=lambda S, i, j, v: 'green' if v == 'A' else None),
        dict(type='table', var='s', label='s：右下角固定的二维后缀和（苹果数）', h=250, cell=56,
             cursors=[('i', 'j', 'blue')]),
        dict(type='table', var='f', label='f[i][j]：切 c 刀的方案数（黄框 = 刚更新）', h=250, cell=56,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='array', var='col_s', label='col_s：f 每列的后缀和', h=130, cell=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'row_s', ('f[0][0]', 'f[0][0]', 'green')],
    captions={
        'm, n = len': '披萨 `{m}` 行 `{n}` 列',
        's = [[0]': '`s[i][j]` = 左上角 `(i,j)`、右下角 `(m-1,n-1)` 的子矩形里的苹果数，多开一圈 0 当哨兵',
        'f = [[0]': '`f[i][j]` 先装「切 0 刀」：只要剩下的这块有苹果就是 1',
        'for i in range(m - 1': lambda S, B, r: ('这一层所有行都算完了' if S.i == B.get('i') else (f'`i = {S.i}`：从下往上算（要用到下面一行）' if 'col_s' not in S else f'`i = {S.i}`：从下往上，这一行的 `f` 只依赖上一层的右边和下面')),
        's[i][j] = s[i][j + 1]': '`s[{i}][{j}] = {s[i][j+1]} + {s[i+1][j]} − {s[i+1][j+1]} + 当前格` = =={s[i][j]}==（容斥）',
        'if s[i][j]: f[i][j] = 1': lambda S, B, r: (f'`s[{S.i}][{S.j}] = {S.s[S.i][S.j]} > 0`：这块有苹果 → 切 0 刀方案数 `f = 1`' if S.s[S.i][S.j] else f'`s[{S.i}][{S.j}] = 0`：没苹果，`f` 保持 0'),
        'for _ in range(1, k)': lambda S, B, r: ('`k−1` 轮都做完了' if S.get('_') == B.get('_') else '再多切一刀：`f` 从「切 c−1 刀」升级成「切 c 刀」，只用到上一层 → ==滚动数组=='),
        'col_s = [0]': '`col_s[j]`：上一层 `f` 第 `j` 列、已经扫过的行的和，用来表示「水平切」',
        'row_s = 0': '`row_s`：上一层 `f` 当前行、已经扫过的列的和，用来表示「垂直切」',
        'if s[i][j] == s[i][j + 1]': lambda S, B, r: (f'`s[{S.i}][{S.j}] = s[{S.i}][{S.j + 1}] = {S.s[S.i][S.j]}`：多出的第 `{S.j}` 列没有苹果 → ==左边界空=='
                                                      if S.s[S.i][S.j] == S.s[S.i][S.j + 1] else f'`s[{S.i}][{S.j}] = {S.s[S.i][S.j]} ≠ s[{S.i}][{S.j + 1}] = {S.s[S.i][S.j + 1]}`：左边界有苹果'),
        'f[i][j] = f[i][j + 1]': '左边界没苹果，这一列根本切不出去 → 直接继承右边：`f[{i}][{j}] = f[{i}][{j+1}] = {f[i][j]}`',
        'elif s[i][j] == s[i + 1][j]': lambda S, B, r: (f'`s[{S.i}][{S.j}] = s[{S.i + 1}][{S.j}] = {S.s[S.i][S.j]}`：第 `{S.i}` 行没有苹果 → ==上边界空=='
                                                        if S.s[S.i][S.j] == S.s[S.i + 1][S.j] else f'`s[{S.i}][{S.j}] ≠ s[{S.i + 1}][{S.j}]`：上边界也有苹果'),
        'f[i][j] = f[i + 1][j]': '上边界没苹果 → 直接继承下面：`f[{i}][{j}] = f[{i+1}][{j}] = {f[i][j]}`',
        'f[i][j] = (row_s': '左、上边界都有苹果 → 切出去的那块一定有苹果，不用再判断：`f[{i}][{j}] = {B.row_s} + {B.col_s[j]}` = =={f[i][j]}==',
        'row_s += tmp': '旧值（上一层的 `f`，先存进了 `tmp`）加进行后缀和 `row_s = {row_s}`',
        'col_s[j] += tmp': '旧值 `tmp`（上一层的 `f`）加进行后缀和 `row_s = {row_s}` 和列后缀和 `col_s[{j}] = {col_s[j]}`，留给左边/上边的格子用',
        'return f[0][0]': '整块披萨切 `k−1` 刀的方案数 `f[0][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举第一刀切在哪，剩下的还是左上角在 (i,j) 的小披萨',
        complexity='时间 `O(kmn)`，空间 `O(mn)`',
        problem=['`rows×cols` 的披萨，`A` 是苹果，`.` 是空格；切 `k−1` 刀得到 `k` 块',
                 '竖切送出左边，横切送出上边；每一块都要 ==至少有一个苹果==',
                 '示例：`["A..","AAA","..."]`，`k = 3` → `3`',
                 '本视频演示 `["A..","AAA"]`，`k = 2`（切一刀）'],
        quote='如果左边界没有苹果，那么必不可能切出这一列……如果左边界和上边界都有苹果，那就意味着==无论这一刀怎么切，切出来的送人的那一块披萨一定有苹果==！',
        quote_src='—— 灵茶山艾府题解（五、终极优化）',
        idea=['剩下的披萨右下角永远是 `(m-1,n-1)`，状态只要记左上角 `(i,j)` 和还要切几刀 `c`',
              '`f[c][i][j]` = 第 `i` 行后缀和 + 第 `j` 列后缀和（对上一层 `f` 求和）',
              '左/上边界为空时，把这行/列加在小披萨上，方案数不变 → 直接继承'],
        summary=['时间 `O(kmn)`：每个状态 `O(1)`，用后缀和代替枚举切点',
                 '易错：`i`、`j` 必须倒序，既要累加后缀和，也避免新值覆盖还没用的旧值',
                 '易错：先存 `tmp`，再把 `tmp`（旧值）加进 `row_s` / `col_s`',
                 '灵神题解还有 3 种写法：暴力递归 → `@cache` 记忆化 → 1:1 递推 `f[c][i][j]`，终极版去掉了 `c` 维',
                 '二维后缀和用 `s[i][j+1] + s[i+1][j] - s[i+1][j+1]` 容斥'],
    ),
)
