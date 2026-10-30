def _top(S):
    if 'l' not in S or 'text' not in S:
        return ''
    t, l, r, p = S['text'], S['l'], S['r'], S['p']
    if S['_line'] in (11, 12, 13):
        return f"已切好 `res = {S['res']}` 段；剩下的中间部分 `text[{l}..{r}]`"
    return f"前缀候选 `text[{l}:{p + 1}] = \"{t[l:p + 1]}\"`　末尾字符 `text[{r}] = '{t[r]}'`"


CONFIG = dict(
    num=1147, title='段式回文', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='贪心 · 双指针 + 前缀逐字扩展',
    tags=['灵神题单', '难度分 1912'],
    code='''
class Solution(object):
    def longestDecomposition(self, text):

        l = 0
        r = len(text) - 1
        res = 0
        p = l
        while l < r:
            while p < r and text[p] != text[r]:
                p += 1
            
            if p == r:
                return res + 1
            
            part_len = p - l + 1
            q = r - part_len + 1
            if q <= p:
                return res + 1
            
            if text[l:p] == text[q:r]:
                res += 2
                l = p + 1
                r = q - 1
                p = l
            else:
                p += 1
        
        if l == r:
            res += 1
        return res
''',
    call='Solution().longestDecomposition("antaprezatepzapreanta")',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='text', label='text（蓝 = l，粉 = r，黄 = p；绿 = 已切好的段）', cell=44, h=230,
             pointers={'l': 'blue', 'r': 'pink', 'p': 'yellow'},
             color=lambda S, i, v: 'green' if 'l' in S and (i < S['l'] or i > S['r']) else None,
             dim=lambda S, i, v: False),
    ],
    skip=['part_len = ', 'l = p + 1', 24],
    max_steps=80,
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'l = 0': '`l` 是左边还没切的起点',
        'r = len': '`r` 是右边还没切的终点 = `{r}`',
        'res = 0': '`res` 记录切出的段数',
        'p = l': '`p` 从 `l` 开始：向右找前缀的末尾，使 `text[p]` 等于 `text[r]`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：中间还有没切的部分' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：不剩（或只剩 1 个字符）→ 结束循环'),
        'while p < r and text[p] != text[r]': lambda S, B, r: (
            f'`text[{S.p}] = {S.text[S.p]!r}` 和 `text[{S.r}] = {S.text[S.r]!r}` 不同 → `p` 继续右移' if S.p < S.r and S.text[S.p] != S.text[S.r]
            else (f'`p = {S.p}`：`text[p] = text[r] = {S.text[S.r]!r}` → 找到候选前缀 `"{S.text[S.l:S.p + 1]}"`' if S.p < S.r
                  else '`p` 走到了 `r`：没找到和末尾相同的字符')),
        'p += 1': '`p` → `{p}`',
        'if p == r': lambda S, B, r: ('`p == r`：整段里没有可切的前缀 → 剩下的当 ==1 段== 返回 `res + 1`' if S.p == S.r
                                      else f'`p = {S.p} ≠ r = {S.r}`：有候选前缀，下面检查后缀'),
        'return res + 1': lambda S, B, r: f'剩下的整体算 1 段 → 返回 `{S.res} + 1` = =={r}=='.replace('{r}', str(r)),
        'part_len = ': '候选前缀 `text[{l}..{p}]` 长度 `part_len = {part_len}`',
        'q = r - part_len': '候选前缀 `text[{l}..{p}]` 长 `{part_len}` → 末尾等长的后缀是 `text[{q}..{r}]`，起点 `q = {q}`',
        'if q <= p': lambda S, B, r: (f'`q = {S.q} ≤ p = {S.p}`：前后缀重叠 → 不能再切，剩下当 1 段' if S.q <= S.p
                                      else f'`q = {S.q} > p = {S.p}`：前后缀不重叠，可以比较'),
        'if text[l:p] == text[q:r]': lambda S, B, r: (
            f'前缀 `"{S.text[S.l:S.p + 1]}"` == 后缀 `"{S.text[S.q:S.r + 1]}"`（首尾字符已相同，比较中间）→ ==匹配，立刻切下==' if S.text[S.l:S.p] == S.text[S.q:S.r]
            else f'前缀 `"{S.text[S.l:S.p + 1]}"` ≠ 后缀 `"{S.text[S.q:S.r + 1]}"` → 这个 `p` 不行，`p` 再右移'),
        'res += 2': '前后各切下一段 → `res = {res}`',
        'r = q - 1': '两端同时收缩：`l` → `{l}`，`r` → `{r}`；`p` 回到 `l` 重新找',
        'if l == r': lambda S, B, r: (f'`l == r = {S.l}`：正中间还剩 1 个字符 → 它自己是 1 段' if S.l == S.r
                                      else f'`l = {S.l} > r = {S.r}`：刚好切完，没有剩余'),
        'res += 1': '正中间的单个字符自成一段 → `res = {res}`',
        'return res': '最多切成 `{res}` 段',
    },
    cards=dict(
        one_liner='从两端向中间探测，找到匹配的前后缀就立即切下',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['把 `text` 切成 `k` 个非空子串，第 `i` 段等于倒数第 `i` 段',
                 '求 `k` 的==最大值==',
                 '示例：`"ghiabcdefhelloadamhelloabcdefghi"` → `7`',
                 '本视频：`"antaprezatepzapreanta"` → `11`'],
        quote='每次从两端向中心探测，当出现一个匹配的段氏回文时就立即将其加入答案，这样一来才能得到最多的段数。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心证明：前缀 A 比 B 长，若 A 和 B 都有匹配后缀，则 A 自己还能切出 B → ==先切短的更好==',
              '双指针 `l` / `r` 指向未切部分的两端；`p` 从 `l` 起向右找和 `text[r]` 相同的字符',
              '以 `text[l..p]` 为前缀，取末尾等长的后缀比较；相同就切下，否则 `p` 继续右移'],
        result='依次切下 `a`、`nt`、`a`、`pre`、`za`（每对 2 段），最后剩中间 `tep` 一段 → 11',
        summary=['时间 `O(n^2)`，空间 `O(1)`（用下标，不生成新串）',
                 '`text[l:p] == text[q:r]` 比较的是去掉首尾字符后的中间部分，因为 `text[p] == text[r]` 已确认',
                 '`q <= p` 表示前后缀重叠，不能再切，剩余整体算 1 段',
                 '循环结束时 `l == r` 说明正中间多出 1 个字符，要 `res += 1`',
                 '对比灵神：灵神用切片递归，每次比较前后缀；yiduobo 用指针 + 先匹配末位字符来减少比较'],
    ),
)
