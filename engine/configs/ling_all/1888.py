S0 = '1110'


def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - len(S['s']) + 1)


def _bad(S, i, v):
    # X：与 0101… 不符的位置（ord(t[i]) % 2 != i % 2）
    return 'orange' if (ord(v) % 2 != i % 2) else None


def _txt(S):
    if 'cnt' not in S:
        return '把 `s+s` 当成大串；`X` = 与 `0101…` 不符的位置'
    n = len(S['s'])
    return f"窗口里 `X` 有 `cnt = {S['cnt']}` 个：改成 0101… 要 `{S['cnt']}` 次，改成 1010… 要 `{n} − {S['cnt']} = {n - S['cnt']}` 次"


CONFIG = dict(
    num=1888, title='使二进制字符串字符交替的最少反转次数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='环形定长滑窗 · 统计不符位置',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2006'],
    code='''
class Solution:
    def minFlips(self, s: str) -> int:
        ans = n = len(s)
        cnt = 0
        for i in range(n * 2 - 1):
            if ord(s[i % n]) % 2 != i % 2:
                cnt += 1
            left = i - n + 1
            if left < 0:
                continue
            ans = min(ans, cnt, n - cnt)
            if ord(s[left]) % 2 != left % 2:
                cnt -= 1
        return ans
''',
    call=f'Solution().minFlips({S0!r})',
    expect=1,
    views=[
        dict(type='string', var=lambda S: S['s'] * 2, label='t = s + s（橙 = X：与 0101… 不符；框 = 长为 n 的窗口）',
             pointers={'i': 'blue'}, window=(_wl, 'i'), cell=96, h=210, color=_bad),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('n', 'n', 'orange'), ('i', 'i', 'blue'), ('cnt', 'cnt', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = n = len(s)': '`n = {n}`；`ans` 初值取 `n`（最多全部翻转）',
        'cnt = 0': '`cnt` 统计窗口里 `X`（与 0101… 不符）的个数',
        'for i in range': lambda S, B, ret: (f'窗口右端点 `i = {S.i}`，对应字符 `{S.s[S.i % S.n]!r}`' if 'i' not in B or S.i != B.i else '窗口枚举完（后面的与前面重复）'),
        'if ord(s[i % n]) % 2 != i % 2': lambda S, B, ret: (
            f"`ord({S.s[S.i % S.n]!r}) % 2 = {ord(S.s[S.i % S.n]) % 2}`，`i % 2 = {S.i % 2}` → 不相等，是 ==X=="
            if ord(S.s[S.i % S.n]) % 2 != S.i % 2 else
            f"`ord({S.s[S.i % S.n]!r}) % 2 = {ord(S.s[S.i % S.n]) % 2}`，`i % 2 = {S.i % 2}` → 相等，是 `.`（与 0101… 相符）"),
        'cnt += 1': 'X 进入窗口：`cnt = {cnt}`',
        'left = i - n + 1': '窗口左端点 `left = {left}`',
        'if left < 0': lambda S, B, ret: (f'`left = {S.left} < 0`：窗口还不足 n 个' if S.left < 0 else f'窗口 `[{S.left}, {S.i}]` 正好 n 个，可以算答案'),
        'continue': '继续扩大窗口',
        'ans = min': '改成 0101… 要 `{cnt}` 次，改成 1010… 要 `{n - cnt}` 次 → `ans = min({B.ans}, {cnt}, {n - cnt}) = {ans}`',
        'if ord(s[left]) % 2 != left % 2': lambda S, B, ret: (
            f'`s[{S.left}]` 是 ==X==，要离开窗口，`cnt` 减一' if ord(S.s[S.left]) % 2 != S.left % 2
            else f'`s[{S.left}]` 不是 X，离开窗口不影响 `cnt`'),
        'cnt -= 1': 'X 离开窗口：`cnt = {cnt}`',
        'return ans': '最少反转 `{ans}` 次',
    },
    cards=dict(
        one_liner='类型 1 免费：把 s+s 里所有长 n 的窗口都试一遍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['类型 1：把首字符移到末尾（次数不限）；类型 2：反转一个字符',
                 '求变成 ==交替串== 所需类型 2 的最少次数',
                 f'本视频：`s = "{S0}"` → `1`'],
        quote='这些字符串其实都是 s+s（去掉最后一个字符）的长为 n 的子串。……取最小值，用 min(cnt, n−cnt) 更新答案的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['循环移位 = `s+s` 的长 n 子串，==免费==，所以枚举全部窗口',
              '`ord(t[i]) % 2 != i % 2` 的位置记为 `X`，窗口里 `X` 数 = 改成 `0101…` 的次数',
              '另一种目标 `1010…` 的次数就是 `n − cnt`，取较小者'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`range(2n−1)`：`[0,n−1]` 与 `[n,2n−1]` 是同一个字符串，不必重复',
                 '`t[i]` 用 `s[i % n]` 代替，不用真的拼接',
                 '写法二用 `(ord(s[i % n]) ^ i) & 1` 代替比较，思路相同；本视频选写法一'],
    ),
)
