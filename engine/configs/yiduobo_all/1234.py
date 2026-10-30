CONFIG = dict(
    num=1234, title='替换子串得到平衡字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='字符串拼接两遍 · 保留前缀+后缀',
    tags=['滑动窗口与双指针', '难度分 1878'],
    code='''
class Solution(object):
    def balancedString(self, s):

        cnt = {'Q':0, 'W':0, 'E':0, 'R':0}
        n = len(s)
        l = 0
        for r, char in enumerate(s):
            cnt[char] += 1
            if cnt[char] > n // 4:
                break

        if cnt[char] <= n // 4:
            return 0

        cnt[char] -= 1
        r -= 1
        res = n - (r - l + 1)
        s += s
        while l < n:
            cnt[s[l]] -= 1
            l += 1
            while cnt[s[r + 1]] < n // 4:
                r += 1
                cnt[s[r]] += 1

            if r >= n - 1 and n - (r - l + 1) < res:
                res = n - (r - l + 1)
        return res
''',
    call="Solution().balancedString('QWQQQQER')",
    expect=3,
    views=[
        dict(type='string', var='s', label='s（框 = 保留的前缀 + 后缀，拼成一段）', cell=60, h=230,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r')),
        dict(type='map', var='cnt', label='cnt（保留部分里各字母的个数，不能超过 n/4）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"保留长度 ==`{S['r']-S['l']+1}`==（窗口 [l, r]），要替换的是 n − 保留 = ==`{S['n']-(S['r']-S['l']+1)}`==") if 'r' in S and 'l' in S and 'n' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('n', 'n', 'yellow'), ('res', 'res', 'green')],
    captions={
        "cnt = {'Q'": '`cnt` 记录保留部分里每种字母的个数，保留部分里每种都 ==不能超过 n/4==',
        'n = len': '`n = {n}`，每种字母应该恰好 `n // 4 = {n // 4}` 个',
        'for r, char': '先从左往右扫，找最长的合法前缀：`r = {r}`，字母 `{char}`',
        'cnt[char] += 1': '`cnt[{char!r}] = {cnt[char]}`',
        'if cnt[char] > n': lambda S, B, rr: (f'`{S.cnt[S.char]} > {S.n // 4}`：`{S.char}` 超过 n/4，前缀到这里为止不合法 → 停' if S.cnt[S.char] > S.n // 4
                                              else f'`{S.cnt[S.char]} <= {S.n // 4}`：前缀还合法，继续扫'),
        'break': '第一次超标，退出循环：前缀不能把 `s[{r}]` 也包含进去',
        'if cnt[char] <= n': lambda S, B, rr: ('从没超标：原串已经平衡，返回 0' if S.cnt[S.char] <= S.n // 4
                                               else f'`{S.char}` 有超标，需要替换；先考虑只保留前缀、替换后面'),
        'cnt[char] -= 1': '把刚超标的那个 `{char}` 退回去：保留的前缀是 `s[0..r-1]`',
        'r -= 1': '`r` 退回到 {r}：最长合法前缀结束位置',
        's += s': '把 s 拼接两遍：后缀和前缀就连成了一段连续子串，窗口 [l, r] 就能同时表示「保留的后缀 + 保留的前缀」',
        'while l < n': '`l = {l}` < n = {n}：枚举保留后缀的起点，继续',
        'cnt[s[l]] -= 1': '`l` 右移：`{B.s[B.l]}` 不再保留（从窗口左侧移出），`cnt[{B.s[B.l]!r}] = {cnt[B.s[B.l]]}`',
        'l += 1': '`l` → {l}',
        'while cnt[s[r + 1]]': lambda S, B, rr: (f'下一个字母 `{S.s[S.r + 1]}` 保留后个数 `{S.cnt[S.s[S.r + 1]] + 1}` <= n/4 = {S.n // 4}：还能再向右扩 → 扩' if S.cnt[S.s[S.r + 1]] < S.n // 4
                                                  else f'下一个字母 `{S.s[S.r + 1]}` 已有 `{S.cnt[S.s[S.r + 1]]}` 个，再保留就超过 n/4 = {S.n // 4}：停止扩张'),
        'r += 1': '`r` 右移到 {r}，保留 `s[{r}]`',
        'cnt[s[r]] += 1': '`cnt[{s[r]!r}] = {cnt[s[r]]}`',
        'if r >= n - 1': lambda S, B, rr: (
            f'`r = {S.r} < n - 1`：窗口没跨过原串末尾，不是「后缀 + 前缀」，不更新' if S.r < S.n - 1 else
            (f'跨过末尾，需替换 `{S.n - (S.r - S.l + 1)}` < res = `{S.res}` → 更新答案' if S.n - (S.r - S.l + 1) < S.res
             else f'跨过末尾，但需替换 `{S.n - (S.r - S.l + 1)}` 不比 res = `{S.res}` 更小，不更新')),
        17: '情况 1：只保留合法前缀、替换其余 → `res = {n} - {r - l + 1} = {res}`',
        27: '更新：`res = {n} - {r - l + 1} = {res}`',
        'return res': '最少替换 `{res}` 个',
    },
    skip=[],
    cards=dict(
        one_liner='拼成两倍字符串，保留的前缀 + 后缀变成连续窗口',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 只含 `Q W E R`，长 `n`（4 的倍数），每种恰好 `n/4` 个才平衡',
                 '替换一个子串，求子串最短长度；已平衡返回 0',
                 '示例：`"QQWE"` → `1`；本视频：`"QWQQQQER"` → `3`'],
        quote='如果我们将字符串原样复制一遍拼在后面，那么这里的前缀和后缀就能连接起来，成为这个两倍字符串中的一个连续子串',
        quote_src='—— yiduobo 题解原文',
        idea=['换个角度：不替换的部分 = 保留一段前缀 + 一段后缀，替换中间',
              '把 `s` 复制拼接后，前缀 + 后缀 `= 跨过原串末尾的连续子串`，如 `QERQW`',
              '用滑动窗口找最长的、每种字母 `<= n/4` 的这种子串，答案 `n − 窗口长度`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先扫最长合法前缀（情况 1），之后窗口左端 `l` 每右移一次就代表多保留一个后缀字母',
                 '只有 `r >= n - 1`（窗口跨过原串末尾）才更新答案',
                 '原文为 Python 2 写法，`n / 4` 是整数除法，已改为 `n // 4`',
                 '对比灵神：灵神枚举「被替换的子串」，yiduobo 枚举「保留的前缀 + 后缀」'],
    ),
)
