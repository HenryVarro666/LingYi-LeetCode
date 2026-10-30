def _segs(S):
    """已经选定的回文段 [(l, r)]：用同一个贪心重放到当前 i（只用于画图）"""
    s, k, i0 = S['s'], S['k'], S['i']
    n, i, out = len(s), 0, []
    while i < i0 and i <= n - k:
        if s[i:i + k] == s[i:i + k][::-1]:
            out.append((i, i + k - 1)); i += k
        elif i < n - k and s[i:i + k + 1] == s[i:i + k + 1][::-1]:
            out.append((i, i + k)); i += k + 1
        else:
            i += 1
    out = [seg for seg in out if seg[1] < i0]
    if S['_line'] == 7:
        out.append((i0, i0 + k - 1))
    elif S['_line'] == 12:
        out.append((i0, i0 + k))
    return out


def _color(S, idx, v):
    if 'i' not in S or 'ans' not in S:
        return None
    for l, r in _segs(S):
        if l <= idx <= r:
            return 'green'
    if S['_line'] == 6 and S['i'] <= idx < S['i'] + S['k']:
        return 'blue'
    if S['_line'] == 9 and S['i'] <= idx <= S['i'] + S['k']:
        return 'yellow'
    return None


def _dim(S, idx, v):
    return 'i' in S and 'ans' in S and idx < S['i'] and not any(l <= idx <= r for l, r in _segs(S))


def _txt(S):
    if 'i' not in S or 'ans' not in S:
        return ''
    s, k, i = S['s'], S['k'], S['i']
    if i > len(s) - k:
        return '剩下的字母不足 `k` 个，不可能再选出回文串'
    sub = s[i:i + k]
    return f"当前起点 `i = {i}`，已选 ==`{S['ans']}`== 个；长 `k` 的候选 `{sub}`" + (' 是回文' if sub == sub[::-1] else ' 不是回文')


CONFIG = dict(
    num=2472, title='不重叠回文子字符串的最大数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型贪心 · 只看长 k / k+1',
    tags=['字符串', '难度分 2013'],
    code='''
class Solution:
    def maxPalindromes(self, s: str, k: int) -> int:
        n = len(s)
        ans = i = 0
        while i <= n - k:
            if s[i: i + k] == s[i: i + k][::-1]:
                ans += 1
                i += k  # 计算 s[i+k:] 中的最优方案
            elif i < n - k and s[i: i + k + 1] == s[i: i + k + 1][::-1]:
                # 如果跳过不选，即使 s[i+1:i+1+k] 是回文串，剩余内容仍然是 s[i+k+1:]，并不会更优
                # 所以不需要考虑跳过 s[i:i+k+1] 的情况
                ans += 1
                i += k + 1  # 计算 s[i+k+1:] 中的最优方案
            else:
                i += 1  # 计算 s[i+1:] 中的最优方案
        return ans
''',
    call='Solution().maxPalindromes("abaccdbbd", 3)',
    expect=2,
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, color=_color, dim=_dim, label='s（绿 = 已选回文段，蓝 = 长 k 的候选，黄 = 长 k+1 的候选）', h=250),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green'), ('k', 'k', 'orange')],
    captions={
        'ans = i = 0': '`ans` 是已选个数，`i` 是剩余后缀 `s[i:]` 的起点',
        'while i <= n - k': lambda S, B, r: (f'`i = {S.i} ≤ n-k = {len(S.s)-S.k}`：后缀还够放一个长 `k` 的串' if S.i <= len(S.s) - S.k else f'`i = {S.i} > n-k = {len(S.s)-S.k}`：后缀不足 `k` 个字母，==结束=='),
        'if s[i: i + k] ==': lambda S, B, r: (f'长 `k` 的 `{S.s[S.i:S.i+S.k]}` ' + ('是回文 → ==一定要选==（右端点越小，剩下的后缀越长）' if S.s[S.i:S.i+S.k] == S.s[S.i:S.i+S.k][::-1] else '不是回文')),
        'ans += 1': '选下这个回文串：`ans = {ans}`',
        'i += k  #': '跳到这个串后面：`i = {i}`，在 `s[{i}:]` 里继续选',
        'elif i < n - k': lambda S, B, r: (f'长 `k+1` 的 `{S.s[S.i:S.i+S.k+1]}` ' + ('是回文 → ==也要选==（不选的话剩余后缀也不会更长）' if S.i < len(S.s) - S.k and S.s[S.i:S.i+S.k+1] == S.s[S.i:S.i+S.k+1][::-1] else '不是回文（或已到末尾）')),
        'i += k + 1': '跳到这个串后面：`i = {i}`',
        'i += 1': '以 `i` 开头选不出回文串 → 跳过这个字母：`i = {i}`',
        'return ans': '最多能选 `{ret}` 个不重叠回文串',
    },
    cards=dict(
        one_liner='回文段越短越好：只看长 k 或 k+1，选到就立刻跳过',
        complexity='时间 `O((n-k)k)`，空间 `O(1)`',
        problem=['选出若干不重叠的回文子串，每个长度至少为 `k`，求最多能选几个',
                 '示例：`s = "abaccdbbd"`，`k = 3` → `2`（`aba` 和 `dbbd`）',
                 '本视频：同上例'],
        quote='贪心地，第一个回文子串的右端点 r 越小越好，这样剩下的后缀 [r+1,n-1] 更长，能从中选出更多的回文子串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长 `m` 的回文去掉两端仍是回文 → 只需考虑长 `k` 或 `k+1` 的回文',
              '长 `k` 的是回文就选；否则长 `k+1` 的是回文就选；否则 `i` 右移一位',
              '灵神还给出划分型 DP（`f[i]`）和 Manacher 把判回文降到 `O(1)`，本视频演示贪心'],
        summary=['时间 `O((n-k)k)`，空间 `O(1)`；用 Manacher 判回文可降到 `O(n)`',
                 '先判长 `k`，再判长 `k+1`；`k+1` 要求 `i < n - k` 防止越界',
                 '选了就整段跳过，不重叠',
                 '其他写法：DP `f[i] = max(f[i-1], f[i-k]+1, f[i-k-1]+1)` 与 Manacher 版本'],
    ),
)
