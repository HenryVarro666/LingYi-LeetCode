def _prev(S):
    """当前字符上一次出现的位置（仅在 last_pos 更新之前有意义）"""
    if 'char' not in S or 'last_pos' not in S or S.get('_line') in (6, 14, 16):
        return None
    p = S['last_pos'].get(S['char'])
    return p if p is not None and p != S.get('index') else None


def _f_color(S, i, v):
    if 'index' not in S:
        return None
    p = _prev(S)
    if p is not None and p > 0 and i == p - 1 and S.get('_line') in (9, 10, 13):
        return 'purple'
    if i == len(S['f']) - 1 and S.get('_line') in (8, 9, 10, 11, 13):
        return 'yellow'
    return None


def _formula(S):
    if 'index' not in S or 'char' not in S:
        return '`f[i]`：`S[0..i]` 一共能形成多少种不同的子序列；`f[0] = 1`'
    i, ch = S['index'], S['char']
    line = S.get('_line')
    if line == 8:
        return f"不管重复：`f[{i}] = f[{i-1}] + f[{i-1}] + 1`（不选 / 选 `{ch}` / 单独一个 `{ch}`）"
    p = _prev(S)
    if p is None:
        return f"`{ch}` 之前没出现过 → 没有重复，不用减"
    if p == 0:
        return f"`{ch}` 上次在下标 0：重复的只有单独一个 `{ch}` → 减 `1`"
    return f"`{ch}` 上次在下标 `{p}`：重复的是 `f[{p-1}]` 种 `C(X)+{ch}` 和单独的 `{ch}` → 减 `f[{p-1}] + 1`"


CONFIG = dict(
    num=940, title='不同的子序列 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i] = 2·f[i−1] + 1，再按上次出现位置去重',
    tags=['字节30天'],
    code='''
class Solution(object):
    def distinctSubseqII(self, S):
        f = [1]
        mod = 10 ** 9 + 7
        last_pos = {S[0] : 0}
        for index in range(1, len(S)):
            char = S[index]
            f.append((f[-1] + f[-1] + 1) % mod)
            if char in last_pos:
                if last_pos[char] == 0:
                    f[-1] = (f[-1] + mod - 1) % mod
                else:
                    f[-1] = (f[-1] + mod - f[last_pos[char] - 1] - 1) % mod
            last_pos[char] = index

        return f[-1]
''',
    call="Solution().distinctSubseqII('abab')",
    expect=11,
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='string', var='S', label='S（index = 当前，last = 上次出现）', cell=90, h=200,
             pointers={'index': 'yellow', _prev: 'purple'}, pointer_labels={_prev: 'last'}),
        dict(type='array', var='f', label='f[i]：S[0..i] 的不同子序列数（紫 = 要减掉的 f[last−1]）', cell=90, h=150,
             color=_f_color),
        dict(type='map', var='last_pos', label='last_pos（字符 → 最近一次出现的下标）', h=110),
    ],
    watch=[('index', 'index', 'yellow'), ('char', 'char'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：只有 `S[0]` 一个字符时，只有它自己这一种子序列',
        'mod = 10': '答案要对 `10^9 + 7` 取余',
        'last_pos = {S[0] : 0}': '`last_pos` 记录每个字符==最近一次==出现的位置',
        'for index in range': lambda S, B, ret: (f'处理 `S[{S.index}]`' if S.index != B.get('index') else '遍历结束'),
        'char = S[index]': '`char = \'{char}\'`',
        'f.append((f[-1] + f[-1] + 1)': '先不管重复：不选 `{char}` 有 `f[{index - 1}]` 种，选它接在后面也 `f[{index - 1}]` 种，再加单独一个 → `{f[-1]}`',
        'if char in last_pos': lambda S, B, ret: (
            f'`{S.char}` 之前出现过（下标 `{S.last_pos[S.char]}`）→ 有重复，要减掉' if S.char in S.last_pos
            else f'`{S.char}` 第一次出现 → 没有重复'),
        'if last_pos[char] == 0': lambda S, B, ret: (
            '上次出现在下标 0：左边没有字符，重复的只有==单独一个== `' + S.char + '`' if S.last_pos[S.char] == 0
            else f'上次出现在下标 `{S.last_pos[S.char]}` > 0：左边还有 `S[0..{S.last_pos[S.char] - 1}]`'),
        'f[-1] = (f[-1] + mod - 1)': '减 1：`f[{index}] = {B.f[-1]} − 1 = {f[-1]}`',
        'f[-1] = (f[-1] + mod - f[last_pos': lambda S, B, ret: (
            f'`C(X) + {S.char}` 与上次重复了 `f[{S.last_pos[S.char] - 1}] = {S.f[S.last_pos[S.char] - 1]}` 种，'
            f'再加单独的 `{S.char}`：`f[{S.index}] = {B.f[-1]} − {S.f[S.last_pos[S.char] - 1]} − 1 = {S.f[-1]}`'),
        'last_pos[char] = index': '更新 `last_pos[\'{char}\'] = {index}`：下次只需和==最近一次==比',
        'return f[-1]': '`f[-1]` 就是整个串的答案：=={ret}==',
    },
    cards=dict(
        one_liner='每个字符选或不选翻倍再加一，减掉和它上一次出现重复的部分',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求字符串 `S` 的==不同非空子序列==个数，答案对 `10^9 + 7` 取余',
                 '示例：`"abc"` → `7`；`"aba"` → `6`；`"aaa"` → `3`',
                 '本视频：`"abab"` → `11`'],
        quote='设字符串的形式为[XXXX]A1[YYYY]A2……那么==C(X) + A1与C(X) + A2是重复的子序列==，于是此时有多少个C(X)，就会因为A1和A2产生多少种重复子序列。除此之外，==单独的A1和A2也是重复的==。',
        quote_src='—— yiduobo 题解原文',
        idea=['不考虑重复：`f[i] = f[i−1]（不选）+ f[i−1]（选）+ 1（单独一个）`',
              '若 `S[i]` 上次出现在 p：要减去 `f[p−1] + 1`；`p = 0` 时只减 `1`',
              '只需和==最近一次==出现比：更早的重复在算 `f[p]` 时已经清算过了'],
        result='`"abab"` → `11` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（`f` 数组 + `last_pos`）',
                 '易错：取模后做减法要先 `+ mod` 再 `% mod`，防止出现负数',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神按结尾字母分组 `f[26]`，yiduobo 按前缀算总数再去重，殊途同归'],
    ),
)
