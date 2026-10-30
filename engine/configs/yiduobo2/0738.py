N = 13332


def _phase(S):
    line = S.get('_line') or 0
    return 1 if line <= 9 else 2


def _color(S, i, v):
    p = S.get('p')
    if not isinstance(p, int):
        return None
    if _phase(S) == 1:
        if i < p:
            return 'green'
        if i == p:
            return 'blue'
        return None
    if i == p:
        return 'orange'
    if i > p:
        return 'purple'
    return 'green'


def _cond(S):
    p, s = S.get('p'), S.get('s')
    if not isinstance(p, int) or s is None:
        return ''
    line = S.get('_line')
    if 'res' in S:
        return f'前缀 `{s[:p + 1]}` 减 1 → `{int(s[:p + 1]) - 1}`，后面 `{len(s) - p - 1}` 位全填 9'
    if _phase(S) == 1:
        if p < len(s) - 1:
            ok = s[p] <= s[p + 1]
            return f"第一趟：`s[{p}] = {s[p]}` {'≤' if ok else '>'} `s[{p + 1}] = {s[p + 1]}`" + ('，继续往后' if ok else '　→ ==找到第一个下降的位置 p==')
        return '第一趟：扫到末尾都没有下降 → N 本身单调递增'
    if p > 0:
        a, b = int(s[p]) - 1, int(s[p - 1])
        return (f"第二趟：`s[{p}] − 1 = {a}` {'<' if a < b else '≥'} `s[{p - 1}] = {b}`"
                + ('　→ 减完会比左边小，==p 再左移==' if a < b else '　→ 减 1 后仍 ≥ 左边，就在这一位减'))
    return '第二趟：p 到了最高位，就在这里减 1'


CONFIG = dict(
    num=738, title='单调递增的数字', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贪心 · 第一个下降处减 1、后面填 9',
    tags=['字节30天'],
    code='''
class Solution(object):
    def monotoneIncreasingDigits(self, N):
        s = str(N)
        p = 0
        while p < len(s) - 1 and s[p] <= s[p + 1]:
            p += 1

        if p == len(s) - 1:
            return N

        while p > 0 and int(s[p]) - 1 < int(s[p - 1]):
            p -= 1

        res = str(int(s[:p + 1]) - 1) + '9' * (len(s) - p - 1)

        return int(res)
''',
    call=f'Solution().monotoneIncreasingDigits({N})',
    expect=12999,
    views=[
        dict(type='text', fn=_cond, size=28, h=64),
        dict(type='string', var='s', label='s = str(N)（绿 = 已确认单调，橙 = 要减 1 的位，紫 = 之后填 9）',
             pointers={'p': 'pink'}, color=_color, cell=100, h=230),
        dict(type='string', var='res', label='res（答案）', cell=100, h=170,
             color=lambda S, i, v: 'purple' if i > S['p'] else 'orange' if i == S['p'] else 'green'),
    ],
    watch=[('p', 'p', 'pink'), ('s', 's'), ('res', 'res', 'green')],
    captions={
        's = str(N)': '把 N 转成字符串，方便按位比较：`s = "{s}"`',
        'p = 0': '从最高位开始扫描',
        'while p < len(s) - 1': lambda S, B, ret: (
            f'`s[{S.p}] = {S.s[S.p]} ≤ s[{S.p + 1}] = {S.s[S.p + 1]}`：这两位单调 → 继续'
            if S.p < len(S.s) - 1 and S.s[S.p] <= S.s[S.p + 1] else
            (f'`s[{S.p}] = {S.s[S.p]} > s[{S.p + 1}] = {S.s[S.p + 1]}`：==第一个下降的位置 p = {S.p}=='
             if S.p < len(S.s) - 1 else '一直没有下降')),
        'p += 1': '这一对没问题，`p` 后移到 {p}',
        'if p == len(s) - 1': lambda S, B, ret: (
            '`p` 走到末尾：N 本身就单调递增' if S.p == len(S.s) - 1 else
            f'`p = {S.p}` 没走到末尾 → N 不单调，==只能把 s[p] 减小=='),
        'return N': 'N 本身满足条件，直接返回',
        'while p > 0': lambda S, B, ret: (
            f'`s[{S.p}]` 减 1 后是 `{int(S.s[S.p]) - 1}`，比左边 `s[{S.p - 1}] = {S.s[S.p - 1]}` 小 → ==破坏了单调==，往前挪'
            if S.p > 0 and int(S.s[S.p]) - 1 < int(S.s[S.p - 1]) else
            (f'`s[{S.p}]` 减 1 后是 `{int(S.s[S.p]) - 1}` ≥ 左边 `{S.s[S.p - 1]}` → ==就在 p = {S.p} 减 1=='
             if S.p > 0 else '`p = 0`：最高位，减 1 一定安全')),
        'p -= 1': '`p` 左移到 {p}：改为在这一位减 1，它后面全填 9',
        'res = str(': '前缀 `{s[:p + 1]}` − 1 = `{int(s[:p + 1]) - 1}`，再接 `{len(s) - p - 1}` 个 9 → `res = "{res}"`',
        'return int(res)': '`int` 一下（可以去掉前导 0），答案 =={ret}==',
    },
    cards=dict(
        one_liner='找到第一个下降的位置，在那里减 1，后面全部填 9',
        complexity='时间 `O(log N)`，空间 `O(log N)`',
        problem=['给定整数 `N`，返回 ==≤ N== 的最大整数，要求它的各位数字==单调递增==（相邻位 `x ≤ y`）',
                 '示例：`10` → `9`，`1234` → `1234`，`332` → `299`',
                 f'本视频：`{N}` → `12999`'],
        quote='设当前第p位上的数字nums[p] > nums[p + 1]，由于题目要求最终答案必须小于等于N，那么我们不能将nums[p + 1]变大，因此==只能将nums[p]变小==。为了使得答案尽可能大，我们可以将nums[p]减1，然后==从nums[p + 1]开始到末尾全部填上9==。',
        quote_src='—— yiduobo 题解',
        idea=['第一趟：从高位往低位找第一个 `s[p] > s[p+1]`；找不到就返回 N',
              '`s[p]` 减 1 可能比 `s[p-1]` 小 → 第二趟往前，直到减 1 后仍 `≥` 左边',
              '答案：前缀 `s[:p+1]` 减 1，后面全填 9'],
        summary=['时间、空间都是 `O(位数)` = `O(log N)`',
                 '第二趟其实只会跨过==相等==的数位（如 `333` 里减中间的会比左边小）',
                 '`int(s[:p+1]) - 1` 直接对前缀做减法，`10` → `"0" + "9"` → `9`，int 去掉前导 0',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改'],
    ),
)
