S0, K0 = '10101', 1


def _top(S):
    if 'i' not in S:
        return f'`k = {K0}`：0 不超过 k ==或== 1 不超过 k 就合法 → 子串越短越合法'
    l, i, c = S['left'], S['i'], S['cnt']
    ok = c[0] <= K0 or c[1] <= K0
    return (f"窗口 `s[{l}..{i}] = {S0[l:i + 1]!r}`：0 有 `{c[0]}` 个，1 有 `{c[1]}` 个 → "
            + ('==合法==' if ok else '0 和 1 都超过 k，要缩小'))


def _subs(S):
    if 'i' not in S or S['_line'] != 10:
        return ''
    l, i = S['left'], S['i']
    parts = [repr(S0[j:i + 1]) for j in range(l, i + 1)]
    return f"右端点 {i}：{'、'.join(parts)} → 共 =={i - l + 1}== 个"


def _color(S, i, v):
    if 'i' not in S:
        return None
    if S['left'] <= i <= S['i']:
        return 'green' if S['_line'] == 10 else 'blue'
    return None


def _while(S, B, ret):
    c = S.cnt
    if c[0] > S.k and c[1] > S.k:
        return f'`cnt[0] = {c[0]} > {S.k}` 且 `cnt[1] = {c[1]} > {S.k}`：==两个条件都不满足== → 缩小窗口'
    return f'`cnt = {c}`：至少一种字符不超过 {S.k} 个，窗口 `[{S.left}, {S.i}]` 合法'


CONFIG = dict(
    num=3258, title='统计满足 K 约束的子字符串数量 I', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越短越合法',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        ans = left = 0
        cnt = [0] * 2
        for i, c in enumerate(s):
            cnt[ord(c) & 1] += 1
            while cnt[0] > k and cnt[1] > k:
                cnt[ord(s[left]) & 1] -= 1
                left += 1
            ans += i - left + 1
        return ans
''',
    call=f'Solution().countKConstraintSubstrings({S0!r}, {K0})',
    expect=12,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = 窗口 [left, i]，绿 = 本轮计入答案的左端点）',
             pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), color=_color, cell=130, h=300),
        dict(type='text', fn=_subs, size=26, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), 'c', ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'cnt = [0] * 2': '`cnt[0]`、`cnt[1]`：窗口内 0 和 1 的个数',
        'for i, c in': lambda S, B, r: ('右端点枚举完毕' if 'i' in B and B.i == S.i
                                        else f'枚举右端点 `i = {S.i}`，字符 `{S.c!r}` 进入窗口'),
        'cnt[ord(c) & 1] += 1': "`ord({c!r}) & 1 = {ord(c) & 1}`（'0' 的 ASCII 是偶数，'1' 是奇数）→ `cnt = {cnt}`",
        'while cnt[0] > k': _while,
        'cnt[ord(s[left]) & 1] -= 1': '移出左端字符 `s[{left}] = {s[left]!r}` → `cnt = {cnt}`',
        'left += 1': '`left` → {left}：窗口变短，更容易合法',
        'ans += i - left': '左端点取 `{left}..{i}` 都合法：`ans += {i} − {left} + 1` → =={ans}==',
        'return ans': '共有 =={ret}== 个满足 k 约束的子串',
    },
    cards=dict(
        one_liner='枚举右端点，算出最小合法左端点，一次加上 i − left + 1 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`：子串中 ==0 不超过 k 个，或 1 不超过 k 个==，就满足 k 约束',
                 '求满足 k 约束的子串个数',
                 '示例：`s = "10101", k = 1` → `12`（除 "1010"、"10101"、"0101" 外都满足）'],
        quote='由于随着 i 的变大，窗口内的字符数量变多，越不能满足题目要求，所以最小左端点会随着 i 的增大而增大，有==单调性==，因此可以用滑动窗口计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['以 i 为右端点，最小合法左端点是 `left_i`',
              '左端点取 `left_i, …, i` 都合法：==一共 i − left_i + 1 个==',
              '`left_i` 只增不减 → 滑动窗口'],
        summary=['时间 `O(n)`：left 只右移，最多 n 次；空间 `O(1)`',
                 '易错：不合法要求 ==0 和 1 都超过 k==，while 条件是 `and`',
                 '小技巧：`ord(c) & 1` 把 \'0\'/\'1\' 变成 0/1；写法二用 `int(c)`，效果相同',
                 '同类：越短越合法求个数，都是 `ans += right − left + 1`'],
    ),
)
