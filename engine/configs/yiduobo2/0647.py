S0 = 'aaa'
T0 = '#' + '#'.join(list(S0)) + '#'


def _live(S):
    return S.get('s') == T0 and isinstance(S.get('index'), int)


def _first_loop(S):
    return 'res' not in S


def _idx(S):
    return S.get('index') if _live(S) else None


def _mirror(S):
    if not _live(S) or not _first_loop(S) or S.get('_line') != 9:
        return None
    return 2 * S['mid'] - S['index']


def _win(S):
    """以 index 为中心、半径 f[index] 的回文：[index - f + 1, index + f - 1]"""
    if not _live(S) or not _first_loop(S):
        return None
    i, f = S['index'], S.get('f') or []
    if i >= len(f):
        return None
    return i - f[i] + 1, i + f[i] - 1


def _s_color(S, i, v):
    if not _live(S):
        return None
    if _first_loop(S) and i == S['index']:
        return 'orange'
    if _first_loop(S) and S.get('right', 0) > 0 and S['mid'] - (S['right'] - S['mid']) < i < S['right'] and i != S['index']:
        return 'purple'  # 当前最右回文覆盖的范围
    return None


def _f_color(S, i, v):
    if not _live(S):
        return None
    if i == S['index']:
        return 'orange'
    m = _mirror(S)
    if m is not None and i == m:
        return 'cyan'
    return None


def _text(S):
    if not _live(S):
        return f'插入 `#` 后：`{T0}`（长度 {len(T0)}），==所有回文串都是奇数长度=='
    if not _first_loop(S):
        f, i = S['f'], S['index']
        return f'答案 = `sum(f[i] // 2)`：`f[{i}] = {f[i]}` 贡献 =={f[i] // 2}== 个'
    w = _win(S)
    if w:
        a, b = w
        return f"以 `index = {S['index']}` 为中心：`{T0[a:b + 1]}`，回文半径 `f = {S['f'][S['index']]}`"
    return ''


def _cap_mirror(S, B, ret):
    i, m, r = S.index, S.mid, S.right
    j = 2 * m - i
    return (f'`index = {i} < right = {r}`：对称点 `2·mid − index = {j}`，'
            f'先继承 `min(f[{j}] = {S.f[j]}, right − index = {r - i})` = =={S.f[i]}==')


def _cap_while(S, B, ret):
    i, f, s = B.index, B.f[B.index], B.s
    if not (i >= f):
        return f'`index = {i} < f = {f}`：左边==出界== → 停止扩展'
    if not (i + f < len(s)):
        return f'`index + f = {i + f}` ≥ `{len(s)}`：右边==出界== → 停止扩展'
    if s[i - f] != s[i + f]:
        return f'`s[{i - f}] = "{s[i - f]}" ≠ s[{i + f}] = "{s[i + f]}"` → 停止扩展'
    return f'`s[{i - f}] == s[{i + f}] = "{s[i - f]}"` → 半径还能加一'


def _cap_if_right(S, B, ret):
    i, f, r = S.index, S.f[S.index], B.right
    if r < i + f:
        return f'`index + f[index] = {i + f}` > `right = {r}` → 右边界更远，更新 `mid`、`right`'
    return f'`index + f[index] = {i + f}` ≤ `right = {r}` → 不更新'


CONFIG = dict(
    num=647, title='回文子串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='马拉车（Manacher）：答案 = Σ 回文半径 // 2',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def countSubstrings(self, s):
        s = '#' + '#'.join(list(s)) + '#'
        f = []
        mid = 0
        right = 0
        for index in range(len(s)):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while index >= f[index] and index + f[index] < len(s) and \\
                    s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        res = 0
        for index in range(len(s)):
            res += f[index] // 2

        return res
''',
    call=f'Solution().countSubstrings({S0!r})',
    expect=6,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='string', var='s', label='s（橙 = 中心 index，紫 = 最右回文覆盖的范围，框 = 以 index 为中心的回文）', cell=100,
             pointers={_idx: 'orange', 'mid': 'purple', 'right': 'pink'}, pointer_labels={_idx: 'index'},
             window=(lambda S: _win(S)[0] if _win(S) else None, lambda S: _win(S)[1] if _win(S) else None),
             color=_s_color),
        dict(type='array', var='f', label='f（回文半径，青 = 对称点）', cell=100, min_slots=len(T0),
             pointers={_idx: 'orange', _mirror: 'cyan'}, pointer_labels={_idx: 'index', _mirror: '2·mid−index'},
             color=_f_color),
    ],
    watch=[('index', 'index', 'orange'), ('mid', 'mid', 'purple'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    skip=['f = []', 'mid = 0', 'right = 0', 'for index in range(len(s))', 'if index < right',
          's[index - f[index]] == s[index + f[index]]:', 'mid = index', 'res = 0'],
    captions={
        "s = '#' + '#'.join": '每个字符两侧插入 `#`：`"{s}"`，偶数长度的回文也有了中心',
        'f.append(min(': _cap_mirror,
        'f.append(1)': '`index = {index}` 超出最右回文的范围（`right = {right}`）→ 从 `f = 1` 开始暴力扩展',
        'while index >= f[index]': _cap_while,
        'f[index] += 1': '`f[{index}]` → {f[index]}',
        'if right < index + f[index]': _cap_if_right,
        'right = index + f[index]': '`right = {right}`，`mid = {index}`',
        'res += f[index] // 2': '`f[{index}] = {f[index]}` → 贡献 `{f[index]} // 2 = {f[index] // 2}` 个回文，`res` = =={res}==',
        'return res': '所有回文半径 // 2 之和 = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='回文半径为 k，就有 k 个同中心的回文；插入 # 后用马拉车求半径',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['统计字符串 `s` 中==回文子串==的数目（位置不同的相同子串分别计数）',
                 '示例：`"abc"` → `3`',
                 '示例：`"aaa"` → `6`（本视频）'],
        quote='对于一个长度为奇数回文串，若其==回文半径为k==，设其回文中心为c，那么以c为回文中心的回文子串==就有k个==。',
        quote_src='—— yiduobo 题解原文',
        idea=['插入 `#` 后所有回文都是奇数长度；`f[i]` = 以 `i` 为中心的回文半径（含中心）',
              '原串中对应的回文个数 = `f[i] // 2`（中心是字母或 `#` 都成立）',
              '马拉车：`index` 在最右回文 `[.., right)` 内时，先用对称点 `2·mid − index` 的半径'],
        before=[dict(heading='为什么是 f // 2？', chapter='② 推导',
                     lines=['中心是字母：`#a#b#…#c` 半径 `k` 为偶数，正常字符 `k/2` 个',
                            '中心是 `#`：`#a#b…#c#` 半径 `k` 为奇数，正常字符 `(k−1)/2` 个',
                            '两种情况都等于 ==`k // 2`==，所以答案 = `sum(f[index] // 2)`'])],
        summary=['时间 `O(n)`：`right` 只增不减，暴力扩展总次数 `O(n)`；空间 `O(n)`',
                 '`min(f[2·mid − index], right − index)`：对称点的半径不能超出最右回文的边界',
                 '`while` 先判 `index >= f[index]`、`index + f[index] < len(s)` 防越界',
                 '对比灵神：灵神主推 `O(n²)` 中心扩展（奇偶合并），马拉车作为方法二',
                 '原文为 Python 2 写法：`f[index] / 2` 改为 `//`；删去文档字符串，过长的 `while` 条件用 `\\` 折成两行'],
    ),
)
