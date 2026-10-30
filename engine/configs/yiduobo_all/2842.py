def _tbl(S):
    c = S.get('c')
    if not c:
        return [[0]]
    return [r[:6] for r in c[:6]]


def _cell(S, r, col, v):
    if 'freq' in S and 'cnt' in S and 'k' in S and (r, col) == (S['cnt'], S['k']) and S['cnt'] > S['k']:
        return 'yellow'
    return 'green' if v else None


def _txt(S):
    if 'res' not in S:
        return '先统计字母频率，再统计「频率出现了几次」'
    if 'freq' not in S:
        return f"组合数表就绪，`res = {S['res']}`"
    return f"频率 `freq = {S['freq']}` 有 `cnt = {S['cnt']}` 种字母，还要选 `k = {S['k']}` 种　`res` = =={S['res']}=="


CONFIG = dict(
    num=2842, title='统计一个字符串的 k 子序列美丽值最大的数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='频率分组 · 杨辉三角预处理组合数',
    tags=['灵神题单', '数学算法', '难度分 2092'],
    code='''
class Solution(object):
    def countKSubsequencesWithMaxBeauty(self, s, k):

        char_freq = {}
        for char in s:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        if len(char_freq) < k:
            return 0
        
        freq_cnt = {}
        for v in char_freq.values():
            freq_cnt[v] = freq_cnt.get(v, 0) + 1

        mod = 10 ** 9 + 7
        c = [[0] * 26 for _ in range(26)]
        for i in range(26):
            for j in range(i + 1):
                if j == 0 or j == i:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
                    if c[i][j] >= mod:
                        c[i][j] -= mod

        res = 1
        for freq, cnt in sorted(freq_cnt.items(), reverse=True):
            if k >= cnt:
                for _ in range(cnt):
                    res *= freq
                    res %= mod
                k -= cnt
            else:
                res *= c[cnt][k]
                res %= mod
                for _ in range(k):
                    res *= freq
                    res %= mod
                break
        
        return res
''',
    call='Solution().countKSubsequencesWithMaxBeauty("abbcccdd", 3)',
    expect=12,
    views=[
        dict(type='map', var='char_freq', label='char_freq：字母 → 出现次数', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
        dict(type='map', var='freq_cnt', label='freq_cnt：频率 → 有几种字母', fmt=lambda k, v: f'频率 {k}: {v} 种', h=150, font=30),
        dict(type='table', var=_tbl, label='组合数表 c[i][j]（只显示前 6 行 6 列；黄 = 本次要用的 C(cnt, k)）', color=_cell, h=300, cell=70),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('k', 'k', 'blue'), ('freq', 'freq', 'orange'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    skip=['for _ in range', 'for i in range(26)', 'for j in range(i + 1)', 'if j == 0 or j == i', 'c[i][j]', 'if c[i][j] >= mod'],
    captions={
        'char_freq = {}': '先统计每种字母出现的频率',
        'for char in s': lambda S, B, r: ('字母都数完了' if sum(S.char_freq.values()) == len(S.s) else f'看字符 `{S.char!r}`'),
        'for v in char_freq.values()': lambda S, B, r: ('频率都统计完了' if sum(S.freq_cnt.values()) == len(S.char_freq) else f'看频率 `{S.v}`'),
        'char_freq[char] =': '`{char!r}` 出现 `{char_freq[char]}` 次',
        'if len(char_freq) < k': lambda S, B, r: (f'字母种类 `{len(S.char_freq)}` < `k = {S.k}` 凑不齐，答案必为 0' if len(S.char_freq) < S.k
                                                 else f'字母种类 `{len(S.char_freq)}` >= `k = {S.k}`，可以选出 k 种不同字母'),
        'freq_cnt = {}': '频率相同的字母互相等价，所以再统计「每种频率出现了几次」',
        'freq_cnt[v] =': '频率 `{v}` 的字母有 `{freq_cnt[v]}` 种',
        'mod = ': '要取模：`{mod}`',
        'c = [[0] * 26': '准备组合数表 `c`（26 种字母，最多 C(26, j)）',
        'res = 1': '组合数表已按 `c[i][j] = c[i-1][j] + c[i-1][j-1]` 填好（边界 `c[i][0] = c[i][i] = 1`），不用乘法逆元。`res` 从 1 开始',
        'for freq, cnt in sorted': lambda S, B, r: (f'从大到小看频率：频率 `{S.freq}` 的字母有 `{S.cnt}` 种，还要选 `k = {S.k}` 种'
                                                   if 'freq' in S and not (B.get('freq') == S.freq and B.get('_line') in (39, 46)) else '频率都看完了'),
        'if k >= cnt': lambda S, B, r: (f'`k = {S.k} >= cnt = {S.cnt}`：这 {S.cnt} 种字母==全部选上==' if S.k >= S.cnt
                                        else f'`k = {S.k} < cnt = {S.cnt}`：只需从 {S.cnt} 种里挑 {S.k} 种 → 组合数 `C({S.cnt}, {S.k})`'),
        'res *= freq': '每种字母有 `{freq}` 次出现可选，乘 `{freq}` → `res = {res}`',
        'res %= mod': '取模 → `res = {res}`',
        'k -= cnt': '选掉 `{cnt}` 种，`k` 剩 `{k}`',
        'res *= c[cnt][k]': '从 `{cnt}` 种里选 `{k}` 种：`C({cnt}, {k}) = {c[cnt][k]}`，乘进去 → `res = {res}`',
        'break': '`k` 种已选够，结束循环',
        'return res': '返回 =={res}==',
        'return 0': '种类不够，返回 0',
    },
    max_steps=70,
    cards=dict(
        one_liner='先选频率高的字母；频率相同的字母，靠预处理的组合数选',
        complexity='时间 `O(n + 26^2)`，空间 `O(26^2)`',
        problem=['从 `s` 中选 `k` 个下标，对应字母互不相同，美丽值 = 它们的出现次数之和',
                 '求美丽值最大的选法数量（对 `10^9+7` 取模）；下标不同就算不同',
                 '示例：`s = "bcca", k = 2` → `4`'],
        quote='两种出现频率相同的不同字符实际上是等价的，于是可以进一步对这些频率进行统计，即统计每种频率出现了多少次。',
        quote_src='—— yiduobo 题解原文',
        idea=['想美丽值最大，就==优先选频率高的字母==；字母种类不足 `k` 直接返回 0',
              '`cnt <= k`：这 `cnt` 种全要，每种 `freq` 种选法 → 乘 `freq^cnt`，`k` 减去 `cnt`',
              '`cnt > k`：从 `cnt` 种里选 `k` 种，`C(cnt, k) * freq^k`，然后结束',
              '组合数用杨辉三角预处理，不需要乘法逆元'],
        summary=['时间 `O(n + 26^2)`，空间 `O(26^2)`',
                 '边界：`len(char_freq) < k` 要先返回 0',
                 '`cnt == k` 时走「全选」分支，`C(cnt, k) = 1` 不用再乘',
                 '视频里为了节省时间，杨辉三角预处理的循环没有逐行演示',
                 '对比灵神：灵神直接用 `comb` 和 `pow`，这里用预处理的表和循环累乘'],
    ),
)
