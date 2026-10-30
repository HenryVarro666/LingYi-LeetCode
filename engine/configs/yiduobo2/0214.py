S0 = 'abac'


def _ok(S):
    return isinstance(S.get('f'), list) and S.get('s', '').startswith('!')


def _phase2(S):
    return 'end_pos' in S


def P_index(S):
    return S.get('index') if _ok(S) and not _phase2(S) else None


def P_mirror(S):
    i = S.get('index')
    if i is None or _phase2(S) or not _ok(S) or not (i < S['right']) or S.get('_line') not in (9, 10):
        return None
    return 2 * S['mid'] - i


def P_right(S):
    return S['right'] if _ok(S) and not _phase2(S) and S.get('right', 0) > 0 else None


def P_end(S):
    return S.get('end_pos') if _phase2(S) else None


def P_middle(S):
    return S.get('middle_pos') if _phase2(S) and 'middle_pos' in S and S.get('_line') in (21, 22, 23) else None


def W_lo(S):
    if not _ok(S):
        return None
    if _phase2(S):
        m = P_middle(S)
        return m - S['f'][m] + 1 if m is not None else None
    i = S.get('index')
    if i is None or i >= len(S['f']):
        return None
    return i - S['f'][i] + 1


def W_hi(S):
    if not _ok(S):
        return None
    if _phase2(S):
        m = P_middle(S)
        return m + S['f'][m] - 1 if m is not None else None
    i = S.get('index')
    if i is None or i >= len(S['f']):
        return None
    return i + S['f'][i] - 1


def _fcolor(S, i, v):
    if _phase2(S):
        return 'orange' if i == P_middle(S) else None
    if i == S.get('index'):
        return 'orange'
    if i == P_mirror(S):
        return 'cyan'
    return None


def _info(S):
    if not _ok(S):
        return '目标：求 s 的==最长回文前缀==，把剩下的部分翻转后加到前面'
    if _phase2(S):
        m = P_middle(S)
        if m is None:
            return f"从后往前检查前缀 `s[1..{S['end_pos'] - 1}]` 是不是回文"
        return (f"前缀 `s[1..{S['end_pos'] - 1}]` 的中心是 `{m}`：它是回文 ⇔ `f[{m}] == {m}`（以 {m} 为中心的回文==刚好伸到第 1 位==）")
    i, f, s = S.get('index'), S['f'], S['s']
    if i is None or i >= len(f):
        return '马拉车：`f[i]` = 以 `i` 为中心的最长回文半径（含中心）'
    r = f[i]
    return f'以 `s[{i}]` 为中心：`f[{i}] = {r}`，回文 `{s[i - r + 1:i + r]}`'


def _cap_append_min(S, B, ret):
    i, mid, right, f = S.index, S.mid, S.right, S.f
    j = 2 * mid - i
    return f'`{i} < right = {right}`：对称点 `j = {j}`，`f[{i}] = min(f[{j}], right − index) = min({f[j]}, {right - i}) = {f[i]}`'


def _cap_while(S, B, ret):
    i, f, s = S.index, B.f, S.s
    r = f[i]
    a, b = i - r, i + r
    if s[a] == s[b]:
        return f'`s[{a}] = s[{b}] = {s[a]}` → 回文还能再扩'
    return f'`s[{a}] = {s[a]}` ≠ `s[{b}] = {s[b]}` → 停，`f[{i}] = {r}`'


def _cap_mid(S, B, ret):
    return f'回文伸到了更右边 → 更新 `mid = {S.mid}`，`right = {S.right}`（不含）'


def _cap_check(S, B, ret):
    m = S.middle_pos
    if S.f[m] == m:
        return f'`f[{m}] = {S.f[m]}` == `{m}`：前缀 `s[1..{2 * m - 1}]` 是回文 → 对应原串的前 {m} 个字符'
    return f'`f[{m}] = {S.f[m]}` ≠ `{m}`：以 {m} 为中心的回文伸不到第 1 位 → 这个前缀不是回文'


CONFIG = dict(
    num=214, title='最短回文串', difficulty='Hard', category='字符串',
    author='yiduobo', technique='马拉车求最长回文前缀',
    tags=['字节30天'],
    code='''
class Solution(object):
    def shortestPalindrome(self, s):
        origial_s = s
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

        end_pos = len(s) - 1
        while end_pos > 1:
            middle_pos = (end_pos + 1) // 2
            if f[middle_pos] == middle_pos:
                return origial_s[middle_pos:][::-1] + origial_s
            end_pos -= 2

        return origial_s[1:][::-1] + origial_s
''',
    call=f'Solution().shortestPalindrome("{S0}")',
    expect='cabac',
    skip=['origial_s = s', 'f = [0]', 'mid = 0', 'for index in range', 'if index < right', 'if right < index + f[index]',
          'right = index + f[index]'],
    views=[
        dict(type='text', fn=_info, h=96, size=26),
        dict(type='string', var='s', label='s（插入 # 后；框 = 当前讨论的回文）',
             pointers={P_index: 'yellow', P_mirror: 'cyan', P_right: 'pink', P_end: 'pink', P_middle: 'yellow'},
             pointer_labels={P_index: 'index', P_mirror: 'j', P_right: 'right', P_end: 'end_pos', P_middle: 'middle_pos'},
             window=(W_lo, W_hi), cell=96, h=300),
        dict(type='array', var='f', label='f：回文半径（含中心）', min_slots=9, color=_fcolor, cell=96, h=180),
    ],
    watch=[('index', 'index', 'yellow'), ('mid', 'mid', 'purple'), ('right', 'right', 'pink'),
           ('end_pos', 'end_pos', 'pink'), ('middle_pos', 'middle_pos', 'yellow')],
    captions={
        "s = '!' + '#'.join": '插 `#` 让偶回文也有中心；首尾哨兵 `!`、`@` 不相等，扩展到边界自动停',
        'right = 0': '马拉车（同第 5 题）：维护最靠右的回文 `(mid, right)`',
        'f.append(min(': _cap_append_min,
        'f.append(1)': '`index = {index}` 不在大回文里 → 从 `f = 1` 开始暴力扩展',
        'while s[index - f[index]]': _cap_while,
        'f[index] += 1': '`f[{index}] = {f[index]}`',
        'mid = index': _cap_mid,
        'end_pos = len(s) - 1': '第二步：==从后往前==扫描，找最长的回文前缀（第一个满足的就是最长的）',
        'while end_pos > 1': lambda S, B, r: (f'`end_pos = {B.end_pos}`：检查前缀 `s[1..{B.end_pos - 1}]`' if B.end_pos > 1
                                              else '只剩第一个字符'),
        'middle_pos = (end_pos + 1) // 2': lambda S, B, r: (f'这个前缀的回文中心 `middle_pos = ({S.end_pos} + 1) // 2 = {S.middle_pos}`'
                                                            + ('（原文 `/` 已改为整除 `//`）' if 'middle_pos' not in B else '')),
        'if f[middle_pos] == middle_pos': _cap_check,
        'return origial_s[middle_pos:]': '最长回文前缀 `"{origial_s[:middle_pos]}"`，把剩下的 `"{origial_s[middle_pos:]}"` 翻转加到前面 → =={ret}==',
        'end_pos -= 2': '`end_pos -= 2`：跳过 `#`，只检查以真实字符结尾的前缀',
    },
    max_steps=60,
    cards=dict(
        one_liner='问题等价于求 s 的最长回文前缀：剩下的部分翻转后补到前面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在字符串 `s` 的==前面==添加字符，把它变成回文串',
                 '返回能得到的==最短==回文串',
                 '示例：`"aacecaaa"` → `"aaacecaaa"`；`"abcd"` → `"dcbabcd"`',
                 '本视频：`"abac"` → `"cabac"`'],
        quote='[XXX....XX][YY...YYY][XXX..XX] 其中，第一个中括号里面的是加上的k个字符……中间的len(s) - k个字符则是==s的一个回文前缀==。要使得k尽量的小，实际上就要要让中间括号的子回文串尽可能长。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目变成：求 s 的最长回文前缀',
              '先跑马拉车得到 `f`（以每个位置为中心的最长回文半径），`O(n)`',
              '从后往前看前缀 `s[:p]`：中心在 `p/2`，它是回文 ⇔ ==f[p/2] 正好等于 p/2==，每次判断 `O(1)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法：`(end_pos + 1) / 2` 已改为 `//`，并删去 docstring',
                 '易错（原文提醒）：插入特殊字符后，从后往前扫描==不要扫到特殊字符==上，所以 `end_pos -= 2`',
                 '马拉车部分和第 5 题（最长回文子串）完全一样',
                 '其他做法：KMP 求 `s + "#" + reverse(s)` 的最长公共前后缀'],
    ),
)
