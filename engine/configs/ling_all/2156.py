def _wr(S):
    i = S.get('i')
    if i is None:
        return None
    return min(i + S['k'] - 1, len(S['s']) - 1)


def _calc(S, B):
    if 'i' not in S:
        return '倒着滑窗：每次==左端点进入==、右端点离开，只需 乘 `power` 再加一项'
    h = S.get('h')
    return f'窗口 `s[{S["i"]}:{S["i"]+S["k"]}]` 的哈希 `h = {h}`，目标 `hashValue = {S["hashValue"]}`'


CONFIG = dict(
    num=2156, title='查找给定哈希值的子串', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='倒着滑窗 · 字符串哈希',
    tags=['字符串', '难度分 2063'],
    code='''
class Solution:
    def subStrHash(self, s: str, power: int, mod: int, k: int, hashValue: int) -> str:
        n = len(s)
        p = pow(power, k - 1, mod)
        h = ans_left = 0  # 题目保证答案存在

        for i in range(n - 1, -1, -1):  # 倒着滑窗
            # 1. 左端点进入窗口
            h = (h * power + (ord(s[i]) & 31)) % mod

            right = i + k - 1  # 窗口右端点
            if right >= n:  # 窗口大小不足 k，尚未形成第一个窗口
                continue

            # 2. 更新答案
            if h == hashValue:
                ans_left = i

            # 3. 右端点离开窗口，为下一个循环做准备
            h = (h - (ord(s[right]) & 31) * p) % mod

        return s[ans_left: ans_left + k]
''',
    call="Solution().subStrHash('leetcode', 7, 20, 2, 0)",
    expect='ee',
    views=[
        dict(type='string', var='s', label='s（框 = 当前窗口，从右往左滑）', cell=100, h=230,
             pointers={'i': 'blue'}, window=('i', _wr)),
        dict(type='text', h=90, size=30, fn=_calc),
        dict(type='text', h=80, size=28,
             fn=lambda S: f"`p = power^(k-1) mod {S['mod']} = {S['p']}`：窗口最高位 `p^(k-1)` 的系数" if 'p' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('right', 'right', 'pink'), ('h', 'h', 'orange'), ('ans_left', 'ans_left', 'green')],
    captions={
        'n = len(s)': '字符串长度 `n = {n}`',
        'p = pow': '`p = power^(k-1) mod {mod} = {p}`：窗口里最高次项 `p^(k-1)` 要用它来删除',
        'h = ans_left = 0': '`h` 是窗口哈希，`ans_left` 记录答案左端点，先都置 0',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：窗口的左端点，倒着往左走' if not ('i' in B and S.i == B.i) else '`i` 已经走完 0，遍历结束'),
        'h = (h * power': '`h = (h × {power} + val({s[i]!r})) % {mod} = {h}`：旧项整体升一次幂，新字母放进最低次项 `p^0`',
        'right = i + k - 1': '窗口右端点 `right = {i} + {k} - 1 = {right}`',
        'if right >= n': lambda S, B, r: (f'`right = {S.right} >= n = {S.n}`：窗口还没够 `k` 个 → 先只进不出' if S.right >= S.n
                                          else f'`right = {S.right} < n`：窗口 `{S.s[S.i:S.right+1]!r}` 已满 k 个，可以判断'),
        'continue': '窗口没满，继续往左',
        'if h == hashValue': lambda S, B, r: (f'`h = {S.h} == {S.hashValue}`：窗口 `{S.s[S.i:S.i+S.k]!r}` 满足，==更新答案左端点== '
                                              f'（越往左越靠前，所以后面找到的会覆盖前面的）' if S.h == S.hashValue
                                              else f'`h = {S.h} ≠ {S.hashValue}`，不是答案'),
        'ans_left = i': '`ans_left = {ans_left}`：倒着扫，最后写入的一定是最靠前的',
        'h = (h - (ord': '右端点字母 `{s[right]!r}` 离开：减去 `val × p` = `{(ord(s[right]) & 31)} × {p}`，`h = {h}`（Python 的 `%` 保证非负）',
        'return s[': '返回 `s[{ans_left}:{ans_left}+{k}]` = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='第一个字母次数最低 → 倒着滑窗，只乘不除',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['哈希 `= Σ val(s[j])·power^j mod m`（`val(a)=1`），首字母的幂次最小',
                 '求 `s` 中==第一个==长为 `k`、哈希等于 `hashValue` 的子串',
                 '示例：`s="leetcode", power=7, mod=20, k=2, hashValue=0` → `"ee"`'],
        quote='倒着滑窗更好计算。……在本题的哈希函数中，第一个字母的 p 的幂次是最小的，这和通常字符串哈希中的定义是相反的。所以在计算哈希值时，要倒序遍历。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正着滑要除以 `p`，要逆元，而 `p` 不保证是质数 → 做不了',
              '倒着滑：新字母放最低位，旧项整体 ×`p`，只用乘法',
              '窗口满后再删右端：`- val × p^(k-1)`，所以先预处理 `p`'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计）',
                 '易错：减法后要再取模，Python 的 `%` 自动非负；其他语言要 `+ mod`',
                 '倒着扫时遇到相等就覆盖 `ans_left`，才能得到最靠前的答案',
                 '`ord(c) & 31` 等于 `c - 96`，即 a=1…z=26',
                 '同类：字符串哈希、Rabin-Karp'],
    ),
)
