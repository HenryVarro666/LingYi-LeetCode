def _active(S):
    return S.get('_line') in (20, 21, 22, 25, 27) and 'j' in S and 'i' in S and 'cut_pos' in S


def _color(S, r, c, v):
    ln = S.get('_line')
    if 'j' not in S or 'i' not in S or S['j'] >= len(S['stones']) or ln not in (17, 19, 21, 22, 25, 27) or 'f' not in S:
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if ln in (19, 21, 22) and 'cut_pos' in S and (r, c) in ((i, S['cut_pos']), (S['cut_pos'] + 1, j)):
        return 'blue'
    return None


def _formula(S):
    ln = S.get('_line')
    if 'l' not in S or 'i' not in S or 'j' not in S or 'f' not in S:
        return '`f[i][j]` = 尽可能合并区间 `[i, j]` 的石头所需的最小代价'
    i, j, K = S['i'], S['j'], S['K']
    if ln in (19, 21, 22) and 'cut_pos' in S and S['l'] >= S['K']:
        c = S['cut_pos']
        f = S['f']
        return f'分割点 `cut_pos = {c}`：左 `[{i}, {c}]` 能合成 1 堆，`f[{i}][{c}] + f[{c + 1}][{j}]` = `{f[i][c]} + {f[c + 1][j]}` = =={f[i][c] + f[c + 1][j]}=='
    if ln in (25, 27):
        s = S['s']
        return f'区间和 `stones[{i}..{j}]` = `s[{j}] − s[{i - 1}]` = `{s[j]} − {s[i - 1] if i > 0 else 0}` = =={s[j] - (s[i - 1] if i > 0 else 0)}=='
    L = j - i + 1
    return f'区间 `[{i}, {j}]` 长 `l = {L}`：{"小于 K，不能再合并 → 0" if L < K else "≥ K，枚举分割点"}'


CONFIG = dict(
    num=1000, title='合并石头的最低成本', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP（分割点步长 K-1）',
    tags=['灵神题单', '动态规划', '难度分 2423'],
    code='''
class Solution(object):
    def mergeStones(self, stones, K):

        n = len(stones)
        if (n - 1) % (K - 1) != 0:
            return -1
        
        f = [[None] * n for _ in range(n)]
        s = [stones[0]]
        for num in stones[1:]:
            s.append(s[-1] + num)

        for l in range(1, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                if l < K:
                    f[i][j] = 0
                else:
                    for cut_pos in range(i, j, K - 1):
                        tmp = f[i][cut_pos] + f[cut_pos + 1][j]
                        if f[i][j] is None or f[i][j] > tmp:
                            f[i][j] = tmp

                    if (l - 1) % (K - 1) == 0:
                        f[i][j] += s[j]
                        if i > 0:
                            f[i][j] -= s[i - 1]
        
        return f[0][n - 1]
''',
    call='Solution().mergeStones([3, 2, 4, 1, 5], 3)',
    expect=22,
    skip=['for num in stones', 's.append', 'j = i + l - 1', 'if l < K', 'if i > 0', 'for i in range', 'f[i][j] = 0', 'tmp = f['],
    max_steps=75,
    views=[
        dict(type='array', var='stones', label='stones', h=215, cell=80, pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j')),
        dict(type='text', fn=_formula, size=22, h=100),
        dict(type='table', var='f', label='f[i][j]（None 表示还没算；黄 = 正在算，蓝 = 当前用到的两段）', h=330, cell=64,
             rows=lambda S: [str(k_) for k_ in range(len(S['stones']))], cols=lambda S: [str(k_) for k_ in range(len(S['stones']))],
             color=_color),
    ],
    watch=[('l', 'l', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cut_pos', 'cut_pos', 'green'), ('s', 's')],
    captions={
        'n = len': '`n = {n}` 堆，每次合并 `K = {K}` 堆',
        'if (n - 1)': '每次合并减少 `K − 1` 堆，要从 `n` 堆减到 1 堆：`({n} − 1) % ({K} − 1) = {(n - 1) % (K - 1)}` → ==有解==',
        'f = [[None]': '`f[i][j]`：尽可能合并 `[i, j]` 之间石头的最小代价（长度不一定能合成 1 堆）',
        's = [stones[0]]': '前缀和 `s[j] = stones[0] + … + stones[j]`（下面的累加循环不逐步演示）',
        'for l in range': lambda S, B, r: ('所有区间长度都算完了' if S.get('l') == B.get('l') else
                                           (f'区间长度 `l = {S.l}` < `K = {S.K}`：这些区间不够合并，`f[i][j] = 0`（自动填好，不逐个演示）' if S.l < S.K
                                            else f'区间长度 `l = {S.l}`：==先算短区间，再算长区间==，逐个区间演示')),
        'for cut_pos in range': lambda S, B, r: (
            f'枚举分割点：从 `i = {S.i}` 起步长 `K − 1 = {S.K - 1}`，保证左段恰好能合成 1 堆（不会丢掉这次合并）'
            if S.f[S.i][S.j] is None and S.cut_pos == S.i
            else f'再试下一个分割点 `cut_pos = {S.cut_pos}`' if S.get('cut_pos') != B.get('cut_pos')
            else f'分割点都试完了，`f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'tmp = f[i]': '`tmp = f[{i}][{cut_pos}] + f[{cut_pos+1}][{j}]` = `{f[i][cut_pos]} + {f[cut_pos+1][j]}` = {tmp}',
        'if f[i][j] is None': lambda S, B, r: (f'`tmp = f[{S.i}][{S.cut_pos}] + f[{S.cut_pos + 1}][{S.j}]` = `{S.f[S.i][S.cut_pos]} + {S.f[S.cut_pos + 1][S.j]}` = {S.tmp}；`f[i][j]` 还是 `None`，直接取它' if S.f[S.i][S.j] is None
                                               else f'`tmp = {S.f[S.i][S.cut_pos]} + {S.f[S.cut_pos + 1][S.j]}` = {S.tmp}，已有 `{S.f[S.i][S.j]}` → ' + ('更小，替换' if S.f[S.i][S.j] > S.tmp else '不更小，保留')),
        'f[i][j] = tmp': '`f[{i}][{j}]` 更新为 =={f[i][j]}==',
        'if (l - 1)': lambda S, B, r: (f'`({S.l} − 1) % ({S.K} − 1) = {(S.l - 1) % (S.K - 1)}`：' +
                                       ('这段最后能合成 1 堆 → ==还要加上这次合并的代价（区间和）==' if (S.l - 1) % (S.K - 1) == 0
                                        else '合不成 1 堆，不加区间和')),
        'f[i][j] += s[j]': lambda S, B, r: ('`f[i][j]` 加上 `s[j]` = {0}'.format(S.s[S.j]) + ('，再减去 `s[i − 1]` 得区间和' if S.i > 0 else '，`i = 0` 时前缀和就是区间和')
                                            + f' → `f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'f[i][j] -= s[i - 1]': '减去 `s[{i-1}]` = {s[i-1]} → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][n - 1]': '整排石头合成一堆的最低代价 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] 是「尽可能合并」的代价，分割点步长取 K-1',
        complexity='时间 `O(n^3 / K)`，空间 `O(n^2)`',
        problem=['`n` 堆石头排成一排，每次把 ==连续 `K` 堆== 合成一堆，代价 = 这 `K` 堆石头总数',
                 '求合成一堆的最小代价，做不到返回 `-1`',
                 '本视频：`stones = [3,2,4,1,5], K = 3` → `22`'],
        quote='这里的分割点必须分割出一个可合并的部分，也就是(cut_pos - i + 1 - 1) % (k - 1) = 0。于是我们需要从i开始，以步长k - 1开始枚举cut_pos。',
        quote_src='—— yiduobo 题解原文',
        idea=['无解：`(N − 1) % (K − 1) != 0`，每次合并只减少 `K − 1` 堆；`f[i][j]` 是「尽可能合并」的代价',
              '`(l − 1) % (K − 1) == 0` 说明能合成 1 堆，再加区间和（前缀和 `s[j] − s[i−1]`）'],
        summary=['时间 `O(n^3 / K)`，空间 `O(n^2)`',
                 '易错：分割点步长是 `K − 1` 而不是 1，否则会错过「合成一堆」的机会',
                 '对比灵神：灵神 `i` 倒序、`j` 正序，且用 `s[j+1] − s[i]`；yiduobo 按区间长度由短到长填表，前缀和不含前导 0'],
    ),
)
