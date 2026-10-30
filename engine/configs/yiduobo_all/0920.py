N0, L0, K0 = 3, 4, 1


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 10:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) == (i - 1, j - 1):
        return 'blue'
    if (r, c) == (i, j - 1) and i >= S['K']:
        return 'pink'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = 用 i 首不同的歌排出长度 j 的播放列表有多少种'
    return (f'`f[{i}][{j}]` = 新歌 `f[{i-1}][{j-1}]×({S["N"]}-{i}+1)` + 旧歌 `f[{i}][{j-1}]×({i}-{S["K"]})`')


CONFIG = dict(
    num=920, title='播放列表的数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 新歌 / 旧歌',
    tags=[],
    code='''
class Solution(object):
    def numMusicPlaylists(self, N, L, K):

        f = [[0] * (L + 1) for _ in range(N + 1)]
        mod = 10 ** 9 + 7

        f[0][0] = 1
        for i in range(1, N + 1):
            for j in range(1, L + 1):
                f[i][j] = f[i - 1][j - 1] * (N - i + 1)
                if i >= K:
                    f[i][j] += f[i][j - 1] * (i - K)
                f[i][j] %= mod

        return f[-1][-1]
''',
    call=f'Solution().numMusicPlaylists({N0}, {L0}, {K0})',
    expect=18,
    skip=['mod = ', 'f[i][j] %= mod', 'for j in range', 'f = [[0]'],
    max_steps=70,
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='table', var='f', label='f[i][j]（行 i = 用了几首不同的歌，列 j = 列表长度；黄 = 在算，蓝 = 新歌来源，粉 = 旧歌来源）',
             h=400, cell=100, rows=lambda S: [str(k) for k in range(S['N'] + 1)], cols=lambda S: [str(k) for k in range(S['L'] + 1)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('N-i+1', 'N - i + 1', 'green'), ('i-K', 'i - K', 'yellow')],
    captions={
        'f[0][0] = 1': '空列表有 `1` 种（用 0 首歌排出长度 0），这是 DP 起点',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：用 `{S.i}` 首不同的歌' if S.get('i') != B.get('i') else '全部算完'),
        'f[i][j] = f[i - 1][j - 1]': '第 `j` 首是==新歌==：前面用了 `{i-1}` 首，还剩 `N-i+1 = {N-i+1}` 首可选 → `{f[i-1][j-1]} × {N-i+1}` = `{f[i][j]}`',
        'if i >= K': lambda S, B, r: (f'`i = {S.i} ≥ K = {S.K}`：可以选==旧歌==，最近 `K` 首不能重复，剩 `i-K = {S.i - S.K}` 首' if S.i >= S.K
                                      else f'`i = {S.i} < K = {S.K}`：歌太少，选不出间隔够远的旧歌'),
        'f[i][j] += ': '旧歌：`{f[i][j-1]} × {i-K}` 加进来 → `f[{i}][{j}] = {f[i][j]}`',
        'f[i][j] %= mod': '取模 `10^9+7`（本例数很小，不变）：`f[{i}][{j}] = {f[i][j]}`',
        'return f[-1][-1]': '`f[N][L]` = =={ret}==：用恰好 `N` 首歌、长度 `L` 的播放列表数',
    },
    cards=dict(
        one_liner='第 j 首要么是新歌，要么是隔了 K 首的旧歌',
        complexity='时间 `O(N·L)`，空间 `O(N·L)`',
        problem=['有 `N` 首不同的歌，要排一个长为 `L` 的播放列表',
                 '每首歌==至少播放一次==；同一首歌再播放前，必须先播 ==K 首别的歌==',
                 '求方案数，对 `10^9+7` 取模。例：`N=3, L=3, K=1` → `6`；视频用 `N=3, L=4, K=1` → `18`'],
        quote='设f[i][j]表示由i个不同的数字构成长度为j的序列有多少种……假设序列中的第j数字是这一次才加入到序列中……假设序列中的第j个数字之前已经被使用过了，由于最近使用的k个数字不能再使用，因此只能在剩下的j - k个数字中选择。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]`：用 `i` 首不同的歌，排出长度 `j`',
              '第 `j` 首是新歌：`f[i-1][j-1] × (N-i+1)`，从没用过的歌里任选',
              '第 `j` 首是旧歌：`f[i][j-1] × (i-K)`，`i` 首里最近 `K` 首不能选',
              '作者先想到组合数学，没想出来，退而求其次用 DP'],
        summary=['时间、空间都是 `O(N·L)`',
                 '易错：旧歌的选择数是 `i - K`（按已用歌曲数 `i`），==不是 `j - K`==；`i < K` 时没有旧歌可选',
                 '原文这里写的是 `j - k`，代码用的是 `i - K`；以代码为准',
                 '每格都对 `10^9+7` 取模；初始 `f[0][0] = 1`，答案 `f[N][L]`'],
    ),
)
