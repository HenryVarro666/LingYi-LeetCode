LET = 'abcdefghijklmnopqrstuvwxyz'


def _cur(S):
    c = S.get('c')
    return c if isinstance(c, int) else None


def _lo(S):
    c = _cur(S)
    return None if c is None else max(c - S['k'], 0)


def _hi(S):
    c = _cur(S)
    return None if c is None else min(c + S['k'], 25)


def _txt(S):
    c = _cur(S)
    if c is None:
        return '`f[c]` = 以字母 `c` 结尾的最长理想子序列长度（共 26 个字母）'
    lo, hi = _lo(S), _hi(S)
    return f'当前字母 ==`{LET[c]}`==：可接在 `{LET[lo]}`~`{LET[hi]}` 结尾的子序列后面（差 ≤ {S["k"]}）'


CONFIG = dict(
    num=2370, title='最长理想子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='枚举字符 · 滚动 DP',
    tags=['灵神题单', '动态规划', '难度分 1835'],
    code='''
class Solution:
    def longestIdealString(self, s: str, k: int) -> int:
        f = [0] * 26
        for c in s:
            c = ord(c) - ord('a')
            f[c] = 1 + max(f[max(c - k, 0): c + k + 1])
        return max(f)
''',
    call='Solution().longestIdealString("acfgbd", 2)',
    expect=4,
    views=[
        dict(type='string', var='s', label='s', h=130, cell=80),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='f', label='f[c]：下标 0~25 = a~z，黄框 = 可转移来源范围', h=260, cell=36,
             window=(_lo, _hi),
             pointers={'c': 'pink'},
             color=lambda S, i, v: ('green' if _cur(S) == i and S.get('_line') == 7 else None),
             dim=lambda S, i, v: v == 0 and _cur(S) is not None and not (_lo(S) <= i <= _hi(S))),
    ],
    watch=[('c', 'c', 'pink'), ('k', 'k', 'blue'), ('最大长度', 'max(f)', 'green')],
    captions={
        'f = [0] * 26': '`f[c]`：以第 `c` 个字母结尾的理想字符串最长长度，初始全 0',
        'for c in s': '依次取出 `s` 的每个字符',
        'c = ord': '字符转成 0~25 的下标：`c = {c}`（`{LET[c]}`）',
        'f[c] = 1 +': lambda S, B, r: (f'`{LET[S.c]}` 可以接在 `{LET[_lo(S)]}`~`{LET[_hi(S)]}` 之后，取这段 `f` 的最大值 `{max(B.f[_lo(S):_hi(S)+1])}`，再 +1 → `f[{S.c}]` = =={S.f[S.c]}=='),
        'return max(f)': '答案是 `f` 中的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='字符串套路：枚举字符，以字母结尾做状态',
        complexity='时间 `O(nk)`，空间 `O(|Σ|)`',
        problem=['`s` 的子序列 `t`，相邻字母在字母表中的位次差 `≤ k`，叫理想字符串',
                 '求最长理想字符串的长度；字母表不循环',
                 '示例：`s = "acfgbd", k = 2` → `4`（`"acbd"`）'],
        quote='字符串题目套路：枚举字符。定义 f[i][c] 表示 s 的前 i 个字母中的以 c 结尾的理想字符串的最长长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选 `s[i]` 作结尾：前一个字母只能在 `[c-k, c+k]` 里',
              '所以 `f[c] = 1 + max(f[c-k .. c+k])`，其余 `f` 不变',
              '第一维只依赖上一行，直接压缩掉，用一个长 26 的数组'],
        summary=['时间 `O(nk)`：每个字符扫一段长度 `≤ 2k+1` 的区间',
                 '空间 `O(26)`；答案是 `max(f)`，不是 `f[最后一个字母]`',
                 '易错：切片下界要 `max(c-k, 0)`，否则负数下标会绕到数组末尾',
                 '同类题：300. 最长递增子序列（也是子序列 + 相邻）'],
    ),
)
