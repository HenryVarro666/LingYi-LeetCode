def _cand(S):
    s = S['s']
    if 'res_preifx' not in S:
        return '目标：反转前 k 个或后 k 个字符，得到字典序最小的串（s = `%s`）' % s
    r = S['res_preifx']
    out = f"当前最优 反转前缀 k = =={r + 1}==：`{s[:r + 1][::-1] + s[r + 1:]}`"
    if 'res_suffix' in S:
        q = S['res_suffix']
        out += f"　　反转后缀 k = =={len(s) - q}==：`{s[:q] + s[q:][::-1]}`"
    return out


def _lcp(S, B, ret):
    return ''


CONFIG = dict(
    num=3735, title='反转后字典序最小的字符串 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='后缀数组（倍增 + 桶排序）+ height + ST 表求 LCP',
    tags=[],
    code='''
class Solution(object):
    def lexSmallest(self, s):

        n = len(s)
        a = [ord(c) - 96 for c in s]
        a = a + [27] + a[::-1]
        n = len(a)
        sa = list(range(n))
        ma = 27

        def sort(f, sa):
            cnt = [0] * (ma + 2)
            for index in range(n):
                cnt[f[index] + 1] += 1
            for index in range(1, ma + 2):
                cnt[index] += cnt[index - 1]

            order = [0] * n
            for index in range(n - 1, -1, -1):
                cnt[f[sa[index]] + 1] -= 1
                order[cnt[f[sa[index]] + 1]] = sa[index]

            for index in range(n):
                sa[index] = order[index]

        sort(a, sa)
        b = [0] * n
        rank = [0] * n

        def get_rank():
            ma = 0
            for index in range(n):
                if index > 0:
                    now = sa[index]
                    pre = sa[index - 1]
                    if a[now] != a[pre] or b[now] != b[pre]:
                        ma += 1
                rank[sa[index]] = ma

            return ma
        
        ma = get_rank()

        k = 1
        while k < n:
            b = [rank[index + k] if index + k < n else -1 for index in range(n)]
            sort(b, sa)
            a = rank[:]
            sort(a, sa)
            ma = get_rank()
            k += k

        t = s + "!" + s[::-1]
        height = [0] * n
        length = 0
        for index in range(n):
            if rank[index] == 0:
                continue
            pre = sa[rank[index] - 1]
            while index + length < n and pre + length < n and t[index + length] == t[pre + length]:
                length += 1
            height[rank[index]] = length
            if length > 0:
                length -= 1

        pow2 = [1]
        while pow2[-1] + pow2[-1] <= n:
            pow2.append(pow2[-1] + pow2[-1])
        
        f = [[None] * len(pow2) for _ in range(n)]
        for p in range(len(pow2)):
            for index in range(n):
                if index + pow2[p] - 1 >= n:
                    break
                if p == 0:
                    f[index][p] = height[index]
                else:
                    f[index][p] = min(f[index][p - 1], f[index + pow2[p - 1]][p - 1])

        def get(x, y):
            x = rank[x]
            y = rank[y]
            if x > y:
                x, y = y, x

            x += 1
            max_length = n
            p = len(pow2) - 1
            while x < y:
                while x + pow2[p] - 1 > y and p > 0:
                    p -= 1
                
                max_length = min(max_length, f[x][p])
                x += pow2[p]
            
            return min(max_length, height[y])

        res_preifx = 0
        for index in range(1, n // 2):
            rev_index = n - index - 1

            max_length = get(rev_index, n - res_preifx - 1)

            if max_length == res_preifx + 1:
                rest_part_index = rev_index + res_preifx + 1
                max_length = get(rest_part_index, res_preifx + 1)
                if max_length < n - rest_part_index and t[rest_part_index + max_length] < t[res_preifx + 1 + max_length]:
                    res_preifx = index
            elif t[n - res_preifx - 1 + max_length] > t[rev_index + max_length]:
                res_preifx = index

        res_suffix = n // 2 - 1
        for index in range(n // 2 - 2, -1, -1):
            max_length = get(n // 2 + 1, index)
            if max_length >= res_suffix - index:
                rest_part_index = n // 2 + 1 + res_suffix - index
                max_length = get(rest_part_index, n // 2 + 1)
                if max_length < n // 2 - res_suffix and t[rest_part_index + max_length] < t[n // 2 + 1 + max_length]:
                    res_suffix = index
            elif t[index + max_length] > t[n // 2 + 1 + max_length]:
                res_suffix = index

        return min(s[:res_preifx + 1][::-1] + s[res_preifx + 1:], s[:res_suffix] + s[res_suffix:][::-1])
''',
    call='Solution().lexSmallest("abba")',
    expect='aabb',
    views=[
        dict(type='text', fn=_cand, size=24, h=50),
        dict(type='string', var=lambda S: S['t'] if 't' in S else '', label='t = s + "!" + 反转的 s（用来比较「反转后的子串」）', cell=64, h=120),
        dict(type='array', var=lambda S: S['a'] if 'a' in S else [], label='a（字符的序：1~26，"!" = 27；倍增时变成上一轮的 rank）', cell=64, h=120,
             color=lambda S, i, v: 'yellow' if v == 27 and S['_line'] < 48 else None),
        dict(type='array', var=lambda S: S['sa'] if 'sa' in S else [], label='sa（排名第 i 的后缀从哪个下标开始）', cell=64, h=120,
             color=lambda S, i, v: 'blue' if v == 0 else None),
        dict(type='array', var=lambda S: S['rank'] if 'rank' in S else [], label='rank（下标 i 开头的后缀排第几，并列同名次）', cell=64, h=120),
        dict(type='array', var=lambda S: S['height'] if 'height' in S else [], label='height[i]（排名 i 与 i-1 的后缀的最长公共前缀）', cell=64, h=120,
             color=lambda S, i, v: 'green' if v > 0 else None),
    ],
    watch=['k', 'index', 'length', 'max_length', ('res_preifx', 'res_preifx', 'blue'), ('res_suffix', 'res_suffix', 'pink')],
    skip=[12, 13, 14, 15, 16, 18, 19, 20, 21, 23, 24, 31, 32, 33, 34, 35, 36, 37, 38, 40, 44, 45, 51, 54, 55, 57, 58, 60, 61, 66, 67, 68,
          5, 7, 8, 46, 98, 112, 27, 28, 47, 48, 50, 56, 59, 63, 64, 99, 105, 106, 113, 116, 117, 71, 72, 73, 74, 75, 76, 77, 78, 80, 81, 82, 83, 84, 86, 87, 88, 89, 90, 91, 93, 94, 96, 100, 9, 3, 4],
    max_steps=150,
    captions={
        5: '把每个字母变成序号：`a=1 … z=26`',
        6: '字母变序号（a=1…z=26），再拼成 `a + [27] + a[::-1]`：中间的 27 是分隔符 `!`，后面是反转后的 s。这样==反转后的子串也是 t 的子串==，可以和原来的比大小',
        7: '`t` 的长度 `n = {n}`。后面所有数组都按它来',
        8: '`sa` 先填 0..n-1，下面用桶排序 + 倍增把它排成「按后缀大小排序」',
        26: '先按单个字符（长度 1）桶排序：`sa` 里按字母序排好了，同字母保持原来的先后',
        42: lambda S, B, r: f'给 `sa` 里每个后缀标名次：和前一名的 `(a, b)` 完全相同就==并列==，否则名次 +1 ',
        46: lambda S, B, r: f'长度翻倍到 `2k = {S.k}`：每个后缀拆成「前一半」「后一半」，后一半的序 `b[i] = rank[i + {S.k}]`，越界是 -1（空串最小）',
        47: '先按==后一半== `b` 排 `sa`（桶排序，O(n)）',
        48: '`a = rank[:]`：前一半的序就是上一轮的 rank',
        49: lambda S, B, r: f'倍增到长度 `2k = {S.k}`：先按==后一半== `b = rank[i + k]`（越界为 -1）排，再按==前一半== `a` 稳定地排，重算 `rank`',
        50: '重新算 `rank`，名次个数 `ma = {ma}`',
        'k += k': '`k` → {k}。`k ≥ n` 时每个后缀的名次都互不相同，`sa` 和 `rank` 就完成了',
        53: '`t = s + "!" + s[::-1]`：和前面的 a 一一对应的字符串，用来取字符比大小',
        56: lambda S, B, r: f'算 height：按下标 `index = {S.index}` 从小到大，利用 ==height[rank[i]] ≥ height[rank[i-1]] − 1== 的性质，`length` 只减 1 不清零，整体 O(n)',
        59: lambda S, B, r: f'`index = {S.index}` 的名次前一名是下标 `pre = {S.pre}` 的后缀，和它比最长公共前缀',
        62: lambda S, B, r: f'`index = {S.index}`：和名次前一名 `pre = {S.pre}` 的后缀比公共前缀（接着上一轮剩下的 length 往后扩）：`length = {S.length}`，记进 `height[{S.rank[S.index]}]`；下一个下标至少还剩 `length - 1`，不用从头比',
        64: '下一个下标（`index + 1`）的公共前缀至少还剩 `length - 1`，不用从头比',
        70: '预处理 ST 表：`f[i][p]` = height 从 i 开始长度 `2^p` 的区间最小值，O(n log n)',
        98: '`res_preifx` 记录目前最优的「反转前缀」（初始 0：只反转第一个字符，即不变）',
        99: '从短到长枚举反转前缀的长度 `index + 1`，和目前最优比较',
        102: lambda S, B, r: (f'`index = {S.index}`：反转 `s[:{S.index + 1}]` 对应 `t[{S.rev_index}:]`，当前最优对应 `t[{S.n - S.res_preifx - 1}:]`。用 LCP（ST 表 O(log n)）求它们的最长公共前缀'),
        104: lambda S, B, r: (f'公共前缀 `{S.max_length}` 等于最优反转段长 `{S.res_preifx + 1}`：==反转的部分分不出胜负==，还要比后面保持原样的部分'
                              if S.max_length == S.res_preifx + 1 else
                              f'公共前缀 `{S.max_length}` < 反转段长 `{S.res_preifx + 1}`：在第 {S.max_length + 1} 个字符就能==分出胜负=='),
        105: '新候选反转之后剩下的部分从 `t[{rest_part_index}:]` 开始，要和最优的 `t[{res_preifx + 1}:]` 比',
        106: '再求一次最长公共前缀 `max_length = {max_length}`',
        107: lambda S, B, r: (f"`t[{S.rest_part_index + S.max_length}] = '{S.t[S.rest_part_index + S.max_length]}'` < `t[{S.res_preifx + 1 + S.max_length}] = '{S.t[S.res_preifx + 1 + S.max_length]}'` → ==新的更小，更新=="
                              if S.max_length < S.n - S.rest_part_index and S.t[S.rest_part_index + S.max_length] < S.t[S.res_preifx + 1 + S.max_length]
                              else '没分出更小（公共前缀已经够长或字符不更小）→ ==不更新=='),
        108: '`res_preifx = {index}`：最优反转前缀长度变为 `{index + 1}`',
        109: lambda S, B, r: (f"第一个不同的位置：最优是 `'{S.t[S.n - S.res_preifx - 1 + S.max_length]}'`，新候选是 `'{S.t[S.rev_index + S.max_length]}'` → "
                              + ('新候选更小，更新' if S.t[S.n - S.res_preifx - 1 + S.max_length] > S.t[S.rev_index + S.max_length] else '新候选不更小，保留原来的')),
        110: '`res_preifx = {index}`：最优反转前缀长度变为 `{index + 1}`',
        112: '`res_suffix` 记录目前最优的「反转后缀」起点，初始是最短的那个（反转最后一个字符等于不变）',
        113: '再从短到长枚举反转后缀 `s[index:]`（下标从后往前）',
        114: lambda S, B, r: f'反转 `s[{S.index}:]` 对应 `t` 中分隔符后的那一段，`index = {S.index}`，先求 `t[{S.n // 2 + 1}:]` 与 `t[{S.index}:]` 的最长公共前缀',
        115: lambda S, B, r: (f'`{S.max_length} ≥ {S.res_suffix - S.index}`：前面一段分不出胜负，继续比后面'
                              if S.max_length >= S.res_suffix - S.index else f'`{S.max_length} < {S.res_suffix - S.index}`：在第 {S.max_length + 1} 个字符就能分出胜负'),
        116: '剩下要比的部分从 `t[{rest_part_index}:]` 开始',
        117: '再求最长公共前缀 `max_length = {max_length}`',
        118: lambda S, B, r: ('比较后一个不同字符 → ==更小，更新 `res_suffix`==' if S.max_length < S.n // 2 - S.res_suffix and S.t[S.rest_part_index + S.max_length] < S.t[S.n // 2 + 1 + S.max_length]
                              else '没有更小 → ==不更新=='),
        119: '更新：最优反转后缀改为 `s[{index}:]`，`res_suffix = {index}`',
        120: lambda S, B, r: (f"`t[{S.index + S.max_length}] = '{S.t[S.index + S.max_length]}'` > `t[{S.n // 2 + 1 + S.max_length}] = '{S.t[S.n // 2 + 1 + S.max_length]}'` → 当前反转后缀更优，更新" if S.t[S.index + S.max_length] > S.t[S.n // 2 + 1 + S.max_length] else '不是更小 → 保留原来的'),
        121: '更新：最优反转后缀改为 `s[{index}:]`，`res_suffix = {index}`',
        122: '',
        123: lambda S, B, r: f"反转前缀最优：`{S.s[:S.res_preifx + 1][::-1] + S.s[S.res_preifx + 1:]}`，反转后缀最优：`{S.s[:S.res_suffix] + S.s[S.res_suffix:][::-1]}`，取较小的 → ==`{r}`=="
    },
    cards=dict(
        one_liner='把 s 反转拼到后面，用后缀数组 + LCP 在 O(1) 级别比较任意两个候选串',
        complexity='时间 `O(n log n)`，空间 `O(n log n)`',
        problem=['小写字母串 `s`（长度可达 `10^5`），==恰好操作一次==：选 `k`，反转 `s` 的前 `k` 个或后 `k` 个字符',
                 '返回操作后字典序最小的字符串',
                 '示例：`"abba"` → `"aabb"`（反转后 2 个字符 `"ba"` 变 `"ab"`）'],
        quote='字符串中的所有子串，都必然是其中某个后缀的前缀。基于这一点，只需要各个后缀间最长公共前缀的长度，就可以很方便的比较字符串中的任意两个子串的大小了。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举 `k` 暴力比较太慢：要能 O(1)/O(log) 比较「反转后的两个候选」',
              '把 `s` 反转后拼在 `s` 后面，中间加分隔符 `!`：反转后的段也是 `t` 的子串',
              '桶排序 + 倍增求 `sa` / `rank`，Kasai 求 `height`，ST 表取区间最小得到任意两后缀的 LCP',
              '前缀、后缀各扫一遍留最优，最后取较小者'],
        result='反转前缀、反转后缀各得一个最优，取较小：`aabb` ✓',
        summary=['时间 `O(n log n)`（倍增 log n 轮，每轮桶排序 O(n)；ST 表 O(n log n)），空间 `O(n log n)`',
                 '易错：前缀要从短到长扫，后缀要从长到短（下标从后往前）扫，比较时才能保证 `index` 与最优的长短关系',
                 '原文为 Python 2 写法，`sa = range(n)` 在 Python 3 里不是列表，不能原地赋值，已改为 `sa = list(range(n))`',
                 '`height[rank[i]] ≥ height[rank[i-1]] - 1`，所以暴力扩展总共只有 O(n) 次'],
    ),
)
