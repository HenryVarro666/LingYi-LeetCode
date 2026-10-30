def _ss(S):
    return S['s'] * 2 if 's' in S else None


def _wl(S):
    if 'i' not in S:
        return None
    return max(0, S['i'] - S['n'] + 2)


def _wr(S):
    return S['i'] + 1 if 'i' in S else None


def _col(S, j, v):
    if 'i' not in S:
        return None
    l, r = _wl(S), _wr(S)
    if not (l <= j <= r):
        return None
    ss = S['s'] * 2
    if (j < r and ss[j] == ss[j + 1]) or (j > l and ss[j] == ss[j - 1]):
        return 'yellow'
    return 'cyan'


def _txt(S):
    if 'i' not in S:
        return '任意循环移位都是 `s + s` 的长为 n 的子串'
    l = S['i'] - S['n'] + 2
    if l < 0:
        return f"窗口还没满：已统计 `{S['i'] + 1}` 对，相同 `same = {S['same']}`"
    t = (S['s'] * 2)[l:l + S['n']]
    return f"循环移位 `{t}`：相邻相同 `same = {S['same']}`，`ans = {S['ans']}`"


CONFIG = dict(
    num=4043, title='恰好有 K 对相等相邻字符的循环移位数量', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='s + s 上的定长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def countRotations(self, s: str, k: int) -> int:
        n = len(s)
        ans = same = 0
        for i in range(n * 2 - 2):
            # 1. 入
            if s[i % n] == s[(i + 1) % n]:
                same += 1

            # 一个窗口内有 n-1 对字母
            left = i - n + 2
            if left < 0:
                continue

            # 2. 更新答案
            if same == k:
                ans += 1

            # 3. 出
            if s[left] == s[(left + 1) % n]:
                same -= 1
        return ans
''',
    call="Solution().countRotations('aaba', 1)",
    expect=2,
    views=[
        dict(type='string', var=_ss, label='s + s（框 = 当前循环移位，黄 = 相邻相同）', h=250, cell=100,
             pointers={'i': 'blue', 'left': 'pink'}, window=(_wl, _wr), color=_col),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=['n', ('k', 'k'), ('i', 'i', 'blue'), ('left', 'left', 'pink'), ('same', 'same', 'orange'),
           ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`；在 `s + s` 上滑长为 n 的窗口',
        'ans = same = 0': '`same`：窗口内相邻相同的对数；`ans`：得分为 k 的个数',
        'for i in range': lambda S, B, ret: (f'第 `{S.i}` 对字母 `({S.i}, {S.i + 1})` 进入窗口'
                                            if 'i' not in B or S.i != B.i else '只看 n 个窗口（最后一个与第一个相同，不重复统计）'),
        'if s[i % n] == s[(i + 1) % n]': lambda S, B, ret: (
            f"1. 入：`s[{S.i % S.n}] = s[{(S.i + 1) % S.n}] = {S.s[S.i % S.n]!r}`，相同" if S.s[S.i % S.n] == S.s[(S.i + 1) % S.n]
            else f"1. 入：`{S.s[S.i % S.n]!r} ≠ {S.s[(S.i + 1) % S.n]!r}`，不相同"),
        'same += 1': '`same` → {same}',
        'left = i - n + 2': '一个窗口有 `n − 1` 对字母，左端点 `left = {i} − {n} + 2 = {left}`',
        'if left < 0': lambda S, B, ret: (f'`left = {S.left} < 0`：窗口里还不够 n − 1 对' if S.left < 0
                                          else f'窗口 `{(S.s * 2)[S.left:S.left + S.n]!r}` 齐了'),
        'continue': '继续入',
        'if same == k': lambda S, B, ret: (f'2. 更新：`same = {S.same} == k`，这个循环移位得分恰好为 k' if S.same == S.k
                                           else f'2. 更新：`same = {S.same} ≠ k = {S.k}`'),
        'ans += 1': '`ans` → {ans}',
        'if s[left] == s[(left + 1) % n]': lambda S, B, ret: (
            f"3. 出：最左边一对 `{S.s[S.left]}{S.s[(S.left + 1) % S.n]}` 相同，离开窗口要减掉" if S.s[S.left] == S.s[(S.left + 1) % S.n]
            else f"3. 出：最左边一对 `{S.s[S.left]}{S.s[(S.left + 1) % S.n]}` 不同，`same` 不变"),
        'same -= 1': '`same` → {same}',
        'return ans': '得分恰好为 k 的循环移位有 =={ans}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='循环移位 = s + s 的子串：在上面滑一个窗口维护得分',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `s` 的一个前缀（长 0 到 n−1）移到末尾，得到循环移位',
                 '得分 = 相邻相同字符的对数；问得分==恰好为 k== 的循环移位有几个',
                 '示例：`"aab", k = 1` → `2`；本视频 `"aaba", k = 1` → `2`'],
        quote='任意循环移位后的字符串，都是 s+s 的子串。……s+s 的第一个长为 n 的子串和最后一个长为 n 的子串是同一个，为避免重复统计，==不考虑最后一个==长为 n 的子串。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['窗口里的单位是「一对相邻字母」，长为 n 的子串含 `n − 1` 对',
              '用 `% n` 代替真正拼接 `s + s`',
              '定长滑窗三步：入 → 更新答案 → 出'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环只到 `2n − 2`：恰好 n 个窗口，不重复统计',
                 '方法二：环上共 c 对相同；`c = k` 答案 `n − c`，`c = k + 1` 答案 `c`，否则 0',
                 '易错：窗口大小是 ==n − 1 对==，所以 `left = i − n + 2`'],
    ),
)
