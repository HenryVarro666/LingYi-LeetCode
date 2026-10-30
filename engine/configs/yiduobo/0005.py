def _phase2(S):
    return 'max_pos' in S


def _ok(S):
    return isinstance(S.get('f'), list) and S['s'].startswith('!')   # s 已经插好 #


def P_mid(S):
    return S['mid'] if _ok(S) and not _phase2(S) and S.get('right', 0) > 0 else None


def P_right(S):
    return S['right'] if _ok(S) and not _phase2(S) and S.get('right', 0) > 0 else None


def P_mirror(S):
    i = S.get('index')
    if i is None or _phase2(S) or not (i < S['right']):
        return None
    return 2 * S['mid'] - i


def P_index(S):
    return S.get('index') if _ok(S) else None


def W_lo(S):
    if not _ok(S):
        return None
    if _phase2(S):
        p = S['max_pos']
        return p - S['f'][p] + 1 if p else None
    return 2 * S['mid'] - S['right'] + 1


def W_hi(S):
    if not _ok(S):
        return None
    if _phase2(S):
        p = S['max_pos']
        return p + S['f'][p] - 1 if p else None
    return S['right'] - 1


def _fcolor(S, i, v):
    if i == S.get('index'):
        return 'orange'
    if i == P_mirror(S):
        return 'cyan'
    return None


def _info(S):
    if not _ok(S):
        return '插入 `#` 后，每个回文都有中心：`f[i]` = 以 `i` 为中心的最长回文==半径=='
    i, f, s = S.get('index'), S['f'], S['s']
    if i is None or i >= len(f):
        return '`f[i]`：半径（含中心），回文是 `s[i-f[i]+1 .. i+f[i]-1]`'
    r = f[i]
    return f'以 `s[{i}]` 为中心：半径 `f[{i}] = {r}`，回文 `{s[i - r + 1:i + r]}`'


def _cap_append_min(S, B, ret):
    i, mid, right, f = S.index, S.mid, S.right, S.f
    j = 2 * mid - i
    tail = '，==被右边界截断==' if f[j] > right - i else '，直接照抄'
    return f'`{i} < right`：对称点 `j = {j}`，`min(f[{j}] = {f[j]}, right - index = {right - i}) = {f[i]}`' + tail


def _cap_while(S, B, ret):
    i, f, s = S.index, S.f, S.s
    r = f[i]
    a, b = i - r, i + r
    if s[a] == s[b]:
        return f'`s[{a}] = s[{b}] = {s[a]}` → 再扩'
    return f'`s[{a}] = {s[a]}` ≠ `s[{b}] = {s[b]}` → 停，`f[{i}] = {r}`'


def _cap_now(kind):
    def cap(S, B, ret):
        i, f = S.index, S.f
        if kind == '#':
            body = f'`#` 为中心（偶回文）：`{f[i]} // 2 * 2 = {S.now_len}`'
        else:
            body = f'字母 `{S.s[i]}` 为中心（奇回文）：`({f[i]} - 1) // 2 * 2 + 1 = {S.now_len}`'
        return body + (f'，==更长==' if S.now_len > S.max_len else '')
    return cap


CONFIG = dict(
    num=5, title='最长回文子串', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='马拉车（Manacher）算法',
    code='''
class Solution(object):
    def longestPalindrome(self, s):
        s = '!' + '#'.join(list(s)) + '@'
        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(s) - 1, 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        max_len = 0
        max_pos = 0
        for index in range(1, len(s) - 1, 1):
            if s[index] == '#':
                now_len = f[index] // 2 * 2
            else:
                now_len = (f[index] - 1) // 2 * 2 + 1
            if now_len > max_len:
                max_len = now_len
                max_pos = index
        return s[max_pos - f[max_pos] + 1 : max_pos + f[max_pos]].replace('#', '')
''',
    call='Solution().longestPalindrome("babad")',
    expect='bab',
    skip=['for index in range(1, len(s) - 1, 1)', 'if index < right', 'if right < index + f[index]',
          'right = index + f[index]', 'mid = 0', 'max_len = 0', "if s[index] == '#'",
          'if now_len > max_len', 'max_len = now_len'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='string', var='s', label='s',
             pointers={P_index: 'yellow', P_mirror: 'cyan', P_mid: 'purple', P_right: 'pink'},
             pointer_labels={P_index: 'index', P_mirror: 'j', P_mid: 'mid', P_right: 'right'},
             window=(W_lo, W_hi), cell=80, h=290),
        dict(type='array', var='f', label='f：回文半径（橙 = index，青 = 对称点 j）', min_slots=11, color=_fcolor,
             cell=80, h=220),
    ],
    watch=[('index', 'index', 'yellow'), ('mid', 'mid', 'purple'), ('right', 'right', 'pink'),
           'now_len', 'max_len', ('max_pos', 'max_pos', 'green')],
    captions={
        "s = '!' + '#'.join": '插入 `#`，==偶回文也变成奇回文==，都有中心；首尾哨兵 `!`、`@` 不相等，扩到边界自动停',
        'f = [0]': '`f[i]` = 以 `i` 为中心的最长回文==半径==（含中心）',
        'right = 0': '维护==最靠右的回文区间==：中心 `mid`，右边界 `right`（不含），先都为 0',
        'f.append(min(': _cap_append_min,
        'f.append(1)': '`{index} ≥ right`：大回文管不到 → `f = 1` 暴力扩展',
        'while s[index - f[index]]': _cap_while,
        'f[index] += 1': '半径 +1：`f[{index}] = {f[index]}`',
        'mid = index': '伸得更右 → 更新最右回文区间（青框）：`mid = {mid}`，`right = {right}`',
        'max_pos = 0': '第二遍：把半径换算成==去掉 # 后的长度==，找最长的那个中心',
        'now_len = f[index] // 2 * 2': _cap_now('#'),
        'now_len = (f[index] - 1)': _cap_now('a'),
        'max_pos = index': '记下（青框 = 目前最长）：`max_len = {max_len}`，`max_pos = {max_pos}`',
        'return s[max_pos': '截取 `s[{max_pos - f[max_pos] + 1} : {max_pos + f[max_pos]}]` = `{s[max_pos - f[max_pos] + 1:max_pos + f[max_pos]]}`，去掉 `#` → =={ret}==',
    },
    cards=dict(
        one_liner='大回文里，左边的小回文会在右边对称出现',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一个字符串 `s`，找到 `s` 中==最长的回文子串==',
                 '示例：`s = "babad"` → `"bab"`（`"aba"` 也对）',
                 '示例：`s = "cbbd"` → `"bb"`'],
        quote='对于一个大回文区间，如果其中心点左侧存在小回文区间，那么其右侧对应位置必然也存在同样的小回文区间。',
        quote_src='—— yiduobo 题解',
        idea=['先插 `#`：`abba` → `a#b#b#a`，所有回文都有中心（原文暴力法里的技巧）',
              '维护最右回文区间 `(mid, right)`；`i` 在区间内时，对称点 `j = 2·mid - i`',
              '`f[i] = min(f[j], right - i)`：==取 min 是为了保证小回文完全在大回文内==',
              '然后继续往 `right` 外暴力扩展；`right` 只增不减 → 总共 `O(n)`'],
        summary=['时间 `O(n)`：每次暴力扩展都让 `right` 右移；空间 `O(n)`',
                 '易错（原文提醒）：由 `f` 求答案要==仔细计算去掉特殊字符后的长度==',
                 '`#` 中心 → 偶回文 `f // 2 * 2`；字母中心 → 奇回文 `(f-1) // 2 * 2 + 1`',
                 '原文还介绍了 `O(n²)` 中心扩展、后缀数组两种做法',
                 '原文为 Python 2 写法：两处 `/` 已改为 `//`，并删去 docstring'],
    ),
)
