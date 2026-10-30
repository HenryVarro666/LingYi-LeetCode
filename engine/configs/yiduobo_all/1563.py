def _info(S):
    if 'pos' not in S:
        return '`f[i][j]`：石子 `i..j`（闭区间）的最大得分；`pos[i][j]`：左半和不超过总和一半的最右切点'
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or i >= len(S['pos']) or j >= len(S['pos']) or S['pos'][i][j] is None:
        return '先预处理 `pos`，再按区间长度 `l` 从小到大做 DP'
    p = S['pos'][i][j]
    return f'区间 `[{i}..{j}]`：`pos = {p}`，切点 ≤ {p} 时左半 ≤ 右半，切点 > {p} 时左半 > 右半'


CONFIG = dict(
    num=1563, title='石子游戏 V', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · pos 临界点 + 区间最大值 g/h',
    tags=['数学算法', '难度分 2087'],
    code='''
class Solution(object):
    def stoneGameV(self, stoneValue):

        n = len(stoneValue)
        f = [[0] * n for _ in range(n)]
        g = [[0] * n for _ in range(n)]
        h = [[0] * n for _ in range(n)]
        s = [stoneValue[0]]
        for index in range(1, n):
            s.append(s[-1] + stoneValue[index])

        pos = [[None] * n for _ in range(n)]
        for i in range(n):
            now_s = 0
            p = i - 1
            for j in range(i + 1, n):
                tot_s = s[j]
                if i > 0:
                    tot_s -= s[i - 1]
                
                while p < j and (now_s + stoneValue[p + 1]) * 2 <= tot_s:
                    now_s += stoneValue[p + 1]
                    p += 1
                
                pos[i][j] = p
        
        for l in range(1, n + 1):
            for i in range(n):
                j = i + l - 1
                if j >= n:
                    continue
                
                if l == 1:
                    g[i][j] = h[i][j] = stoneValue[i]
                    continue

                tot_s = s[j]
                if i > 0:
                    tot_s -= s[i - 1]

                if i <= pos[i][j]:
                    f[i][j] = max(f[i][j], g[i][pos[i][j]])
                    l_s = s[pos[i][j]]
                    if i > 0:
                        l_s -= s[i - 1]
                    if l_s + l_s == tot_s:
                        f[i][j] = max(f[i][j], h[pos[i][j] + 1][j])

                if pos[i][j] + 1 < j:
                    f[i][j] = max(f[i][j], h[pos[i][j] + 2][j])
                

                g[i][j] = max(g[i][j - 1], f[i][j] + tot_s)
                h[i][j] = max(h[i + 1][j], f[i][j] + tot_s)

        return f[0][n - 1]
''',
    call='Solution().stoneGameV([2,2,4])',
    expect=6,
    views=[
        dict(type='text', fn=_info),
        dict(type='grid', var='pos', label='pos[i][j]（行 i，列 j）', h=190, cell=60, rows=lambda S: list(range(len(S['pos']))), cols=lambda S: list(range(len(S['pos']))),
             cursors=[('i', 'j', 'blue', '(i,j)')]),
        dict(type='grid', var='f', label='f[i][j] 最大得分', h=190, cell=60, rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f']))),
             cursors=[('i', 'j', 'blue', '(i,j)')]),
        dict(type='grid', var='g', label='g：固定左端点 i 的区间最大值', h=190, cell=60, rows=lambda S: list(range(len(S['g']))), cols=lambda S: list(range(len(S['g']))),
             cursors=[('i', 'j', 'blue', '(i,j)')]),
        dict(type='grid', var='h', label='h：固定右端点 j 的区间最大值', h=190, cell=60, rows=lambda S: list(range(len(S['h']))), cols=lambda S: list(range(len(S['h']))),
             cursors=[('i', 'j', 'blue', '(i,j)')]),
    ],
    watch=[('l', 'l', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), 'p', 'now_s', 'tot_s'],
    captions={
        16: lambda S, B, r: ('区间只剩一块石子，没有右端点要处理' if S.get('j') is None or S.j < S.i + 1 else
                             f'`j = {S.j}`：算区间 `[{S.i}..{S.j}]` 的临界点 `pos`' if S.pos[S.i][S.j] is None else '这个 `i` 的右端点都处理完了'),
        21: lambda S, B, r: (f'左半和 `{S.now_s}` + `stone[{S.p + 1}]` = {S.now_s + S.stoneValue[S.p + 1]}，乘 2 = {(S.now_s + S.stoneValue[S.p + 1]) * 2}，与总和 `{S.tot_s}` 比：'
                             + ('==没超过一半== → 左半还能扩大' if (S.now_s + S.stoneValue[S.p + 1]) * 2 <= S.tot_s else '==超过一半== → 停') if S.p < S.j else '`p` 已到右端点 → 停'),
        22: '左半并入 `stone[{p + 1}]`：`now_s = {now_s}`',
        23: '`p` → {p}：左半覆盖到下标 {p}',
        25: '==`pos[{i}][{j}] = {p}`==：切点在下标 {p} 之后，左半第一次超过一半（切点 ≤ {p} 时左半 ≤ 右半）',
        27: lambda S, B, r: ('所有长度都算完了' if B.get('l') == S.get('l') else f'`l = {S.l}`：按区间长度从短到长算，保证短区间的 `f/g/h` 已经就绪'),
        33: lambda S, B, r: ('`l == 1`：只剩一块石子，不能再分，`f = 0`，`g`、`h` 记下 `f + 区间和` = `stone[i]`' if S.l == 1 else f'`l = {S.l} > 1`：区间 `[{S.i}..{S.j}]` 要真正转移'),
        34: '`g[{i}][{j}] = h[{i}][{j}] = {stoneValue[i]}`：单块石子，`f = 0`，加区间和',
        41: lambda S, B, r: (f'`i ≤ pos = {S.pos[S.i][S.j]}`：存在左半 ≤ 右半的切点 → Bob 丢右半，Alice 留左半，用 `g` 取最大'
                             if S.i <= S.pos[S.i][S.j] else f'`i > pos = {S.pos[S.i][S.j]}`：没有左半更小的切点，跳过'),
        42: '`f[{i}][{j}] = max(f, g[{i}][{pos[i][j]}])` = =={f[i][j]}==：`g` 已含各切点的 `f + 左半和`',
        46: lambda S, B, r: (f'左半和 `{S.l_s}` × 2 = 总和 `{S.tot_s}`：左右相等，Alice 也可留右半 → 看 `h[pos+1][j]`'
                             if S.l_s + S.l_s == S.tot_s else f'`{S.l_s} × 2 = {2 * S.l_s} ≠ {S.tot_s}`：左右不相等，不用额外处理'),
        47: '相等切点：`f[{i}][{j}] = max(f, h[{pos[i][j] + 1}][{j}])` = =={f[i][j]}==',
        49: lambda S, B, r: (f'`pos + 1 = {S.pos[S.i][S.j] + 1} < j = {S.j}`：存在右半严格更小的切点（`pos + 2` 起）' if S.pos[S.i][S.j] + 1 < S.j
                             else f'`pos + 1 = {S.pos[S.i][S.j] + 1}` 已到右端点：没有右半更小的切点'),
        50: '右半更小，Alice 留右半：`f[{i}][{j}] = max(f, h[{pos[i][j] + 2}][{j}])` = =={f[i][j]}==',
        53: '`g[{i}][{j}] = max(g[{i}][{j - 1}], f[{i}][{j}] + 区间和{tot_s})` = =={g[i][j]}==：以 i 为左端点的前缀最大值',
        54: '`h[{i}][{j}] = max(h[{i + 1}][{j}], f[{i}][{j}] + 区间和{tot_s})` = =={h[i][j]}==：以 j 为右端点的后缀最大值',
        56: '整排石子 `f[0][{n - 1}]` = =={f[0][n - 1]}==',
    },
    skip=[28, 'for index in range', 's.append', 'now_s = 0', 'p = i - 1', 'tot_s = s[j]', 'if i > 0', 'tot_s -= s[i - 1]', 'j = i + l - 1', 'if j >= n', 'continue', 'l_s = s[', 'l_s -= s[', 'pos = [[None]', 'f = [[0]', 'g = [[0]', 'h = [[0]', 'n = len(stoneValue)', 's = [stoneValue[0]]'],
    max_steps=110,
    cards=dict(
        one_liner='先预处理左右半和的临界点 pos，再用 g、h 把 O(n³) 转移压成 O(1)',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['一排石子，Alice 每轮切成左右两段，Bob 丢掉和更大的一段，Alice 得到留下那段的和',
                 '相等时 Alice 自己选丢哪边，只剩一块石子时结束，求最大总分',
                 '本视频：`[2,2,4]` → `6`'],
        quote='上面做法是O(n^3)的，时间复杂度上还是比较吃紧的。注意到上面l_s和r_s的三种大小关系，实际上完全可以在动态规划之前就通过预处理求出……临界位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素区间 DP：`f[i][j]` 枚举切点，比较左右和，`O(n³)`',
              '前缀和单调：每个 `(i,j)` 的临界点 `pos` 可以双指针预处理',
              '左半更小的切点是一段前缀、右半更小的是一段后缀 → `g` 取前缀最大、`h` 取后缀最大'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '`pos[i][j] + 2` 才是右半严格更小的起点；相等时还要看 `h[pos + 1][j]`',
                 '`g`、`h` 里已经加上了区间和：`f[i][j] + tot_s`',
                 '对比灵神：灵神用 `suf_max` 与同向双指针，yiduobo 用 `pos/g/h` 三张表'],
    ),
)
