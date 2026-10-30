def _runs(s):
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append((i, j))
        i = j
    return out


def _pos(S):
    """当前扫到的下标：由已结算的 res 推出已完成几段，再按所在行修正"""
    s = S['s']
    runs = _runs(s)
    tot, k = 0, 0
    while k < len(runs) and tot < S['res']:
        L = runs[k][1] - runs[k][0]
        tot += L * (L + 1) // 2
        k += 1
    if k >= len(runs):
        return len(s) - 1
    ln = S['_line']
    if ln in (8, 9):
        return -1 + 1 if S['cnt'] == 0 else runs[k][0] + S['cnt']
    if ln in (12, 13):
        return runs[k][0]
    return runs[k][0] + max(S['cnt'], 1) - 1


def _col(S, i, v):
    if 'res' not in S:
        return None
    p = _pos(S)
    runs = _runs(S['s'])
    for a, b in runs:
        if a <= p < b:
            if i == p:
                return 'blue'
            return 'green' if a <= i < p else None
    return None


def _top(S):
    if 'cnt' not in S:
        return ''
    return f"当前连续段长度 `cnt = {S['cnt']}`，已结算 `res = {S['res']}`"


def _end(S, B, ret):
    return f"最后一段长度 `{S.cnt}` 还没结算 → 补上 `{S.cnt}×{S.cnt + 1}//2 = {S.cnt * (S.cnt + 1) // 2}`，答案 =={ret}=="


CONFIG = dict(
    num=1759, title='统计同构子字符串的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='切分连续段 · 等差求和',
    tags=['灵神题单', '难度分 1491'],
    code='''
class Solution(object):
    def countHomogenous(self, s):

        now = None
        cnt = 0
        res = 0
        mod = 10 ** 9 + 7
        for char in s:
            if char == now:
                cnt += 1
            else:
                res = (res + cnt * (cnt + 1) // 2) % mod
                now = char
                cnt = 1
        
        return (res + cnt * (cnt + 1) // 2) % mod
''',
    call='Solution().countHomogenous("abbcccaa")',
    expect=13,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 当前连续段）', cell=84, color=_col),
        dict(type='text', fn=lambda S: '段长 k 的同字符串，贡献 `1+2+…+k = k(k+1)/2` 个同构子串：`1 + 3 + 6 + 3 = 13`', size=24),
    ],
    watch=[('now', 'now', 'blue'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'now = None': '`now` 记录当前连续段的字符，开头还没有',
        'cnt = 0': '`cnt` 记录当前连续段已有多长',
        'res = 0': '`res` 累计已经结算的段贡献的子串数',
        'mod = ': '答案要对 `10^9+7` 取模',
        'for char in s': "扫到 `char = '{char}'`",
        'if char == now': lambda S, B, r: (f"`'{S.char}' == '{S.now}'` → 还在同一段里" if S.char == S.now
                                           else f"`'{S.char}' ≠ {S.now!r}` → 上一段结束了，要结算它"),
        'cnt += 1': '同一段又多一个字符，`cnt` → =={cnt}==',
        'res = (res': '上一段长 `{B.cnt}`，贡献 `{B.cnt}×{B.cnt + 1}//2 = {B.cnt * (B.cnt + 1) // 2}` 个子串 → `res = {res}`',
        'now = char': '新的一段开始，字符是 `{now}`',
        'cnt = 1': '新段目前只有 1 个字符，`cnt = 1`',
        'return': _end,
    },
    cards=dict(
        one_liner='同构子串只能落在连续相同的段里，一段长 k 贡献 k(k+1)/2 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['同构字符串：所有字符都==相同==。数 `s` 里同构子字符串的个数（对 `10^9+7` 取模）',
                 '相同位置不同长度算不同子串，出现多次要重复计数',
                 '示例：`"abbcccaa"` → `13`'],
        quote='对于一个长度为k的由同一个字符构成的字符串而言，其可以构成k个长度为1的同构子字符串，k - 1个长度为2的同构子字符串，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `s` 切成若干连续相同字符的段，段与段之间互不影响',
              '一段长 `k`：长度 1 有 k 个、长度 2 有 k-1 个 … 长度 k 有 1 个，合计 `k(k+1)/2`',
              '一趟扫描用 `cnt` 记当前段长，换字符时结算上一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：最后一段没有“下一个不同字符”触发结算，==循环后要再加一次==',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '开头 `cnt = 0` 时第一次结算加的是 0，不影响答案'],
    ),
)
