def _seg(S, k, v):
    if 'i' not in S:
        return None
    i = S['i']
    s = S['s']
    # 当前这一段 [i-cnt+1, i]
    if S['cnt'] > 0 and i - S['cnt'] < k <= i:
        return 'blue'
    return None


def _fmt(x):
    return '−∞' if x == -inf else str(x)


CONFIG = dict(
    num=3499, title='操作后最大活跃区段数 I', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 相邻两段 0 之和',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1729'],
    code='''
class Solution:
    def maxActiveSectionsAfterTrade(self, s: str) -> int:
        total1 = mx = cnt = 0
        pre0 = -inf
        for i, b in enumerate(s):
            cnt += 1
            if i == len(s) - 1 or b != s[i + 1]:  # i 是这一段的末尾
                if b == '1':
                    total1 += cnt
                else:
                    mx = max(mx, pre0 + cnt)
                    pre0 = cnt
                cnt = 0
        return total1 + mx
''',
    call='Solution().maxActiveSectionsAfterTrade("0011000100")',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"`1` 的总数 total1 = =={S['total1']}==，上一段 0：pre0 = {_fmt(S['pre0'])}，最优 010 中的 0：mx = =={S['mx']}==" if 'pre0' in S else ''), size=26),
        dict(type='string', var='s', label='s（蓝 = 正在数的这一段）', cell=76, pointers={'i': 'pink'}, color=_seg, h=300),
        dict(type='text', fn=lambda S: ('答案 = total1 + mx = ' + str(S['total1']) + ' + ' + str(S['mx']) if S['_line'] == 14 else ''), size=26),
    ],
    watch=[('i', 'i', 'pink'), ('cnt', 'cnt', 'blue'), ('total1', 'total1', 'green'), ('pre0', 'pre0', 'cyan'), ('mx', 'mx', 'orange')],
    captions={
        'total1 = mx = cnt': '`total1` 数全部的 `1`；`mx` 记最大的「0 + 1 + 0」里 0 的个数；`cnt` 数当前这一段',
        'pre0 = -inf': '`pre0` = 上一段连续 0 的长度；还没有时设为 `-inf`，这样 `pre0 + cnt` 不会被误选',
        'for i, b': '`i = {i}`，`b = {b}`',
        'cnt += 1': '这一段又多一个字符，`cnt = {cnt}`',
        'if i == len(s) - 1': lambda S, B, r: (f"`s[{S.i}] = {S.b}` 与下一个字符不同（或到末尾）→ ==这一段结束=="
                                               if S.i == len(S.s) - 1 or S.b != S.s[S.i + 1] else f"下一个字符还是 `{S.b}` → 这一段还没完，继续数"),
        "if b == '1'": lambda S, B, r: (f"这一段是 `{S.cnt}` 个 `1`：全部计入 total1" if S.b == '1' else f"这一段是 `{S.cnt}` 个 `0`"),
        'total1 += cnt': '`total1` → =={total1}==。题目只数 1 的个数，不要求连续',
        'mx = max': lambda S, B, r: (f"前面没有 0 段（`pre0 = −∞`），不能配对，`mx` 仍是 {S.mx}" if B.pre0 == -inf else
                                     f"`pre0 + cnt = {B.pre0} + {S.cnt}`：隔着一段 1 的两段 0 可以一起变成 1 → `mx` = =={S.mx}=="),
        'pre0 = cnt': '记下这段 0：`pre0 = {pre0}`，给下一段 0 当「前一段」',
        'cnt = 0': '这一段统计完，`cnt` 清零，开始下一段',
        'return': '`total1 + mx = {total1} + {mx}` = =={ret}==',
    },
    cards=dict(
        one_liner='答案 = 1 的总数 + 相邻两段 0 的最大长度和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把被 0 包围的一段 1 变成 0，再把被 1 包围的一段 0 变成 1，至多一次',
                 '求操作后 1 的最多个数（两端视为有 1 包围）',
                 '示例：`"0100"` → `4`；本视频：`"0011000100"` → `8`'],
        quote='根据题意，答案为 s 中 1 的个数，加上一个 010 子串中的 0 的个数。我们需要找一个 0 最多的 010 子串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分组循环：把 s 切成连续相同的一段段，遇到 1 段累加 `total1`',
              '遇到 0 段，和上一段 0 配对：中间只隔一段 1，正好是一个 `010`',
              '操作等价于把这两段 0 都变成 1（先擦掉中间的 1 再填满），用 `pre0 + cnt` 更新 `mx`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：题目求 1 的个数，不要求连续；原有的 1 并没有减少',
                 '`pre0` 初始为 `-inf`：没有前一段 0 时不能配对',
                 '灵神还给了 `groupby` 的写法，思路一样'],
    ),
)
