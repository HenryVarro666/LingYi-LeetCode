def _color(S, i, v):
    return 'green' if v == '1' else None


def _text(S):
    s = S['s']
    if 'cnt' not in S:
        return '把字符串切成三段，每段 `1` 的个数相同'
    if 'l_cnt' in S and 'r_cnt' in S:
        return f"左边可挪的 0：`{S['l_cnt']}` 个 → `{S['l_cnt'] + 1}` 种；右边：`{S['r_cnt']}` 个 → `{S['r_cnt'] + 1}` 种；乘起来 =={(S['l_cnt'] + 1) * (S['r_cnt'] + 1)}=="
    if 'l_cnt' in S:
        return f"左切口：第 `{S['cnt']}` 个 1 与下一个 1 之间有 `{S['l_cnt']}` 个 0 可左可右"
    return f"共 `{S['cnt']}` 个 1"


CONFIG = dict(
    num=1573, title='分割字符串的方案数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数 1 的个数 · 两侧 0 的空隙相乘',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numWays(self, s):

        cnt = 0
        for char in s:
            if char == '1':
                cnt += 1
        
        n = len(s)
        mod = 10 ** 9 + 7
        if cnt == 0:
            return (n - 1) * (n - 2) // 2 % mod
        
        if cnt % 3 != 0:
            return 0
        
        cnt //= 3
        now = 0
        for index in range(n):
            if s[index] == '1':
                now += 1
                if now == cnt:
                    break
        
        p = index + 1
        while s[p] != '1':
            p += 1

        l_cnt = p - index - 1

        now = 0
        for index in range(n - 1, -1, -1):
            if s[index] == '1':
                now += 1
                if now == cnt:
                    break
        
        p = index - 1
        while s[p] != '1':
            p -= 1
        
        r_cnt = index - p - 1

        return (l_cnt + 1) * (r_cnt + 1) % mod
''',
    call="Solution().numWays('0010010010')",
    expect=9,
    views=[
        dict(type='text', fn=_text, h=110),
        dict(type='string', var='s', pointers={'index': 'blue', 'p': 'pink'}, color=_color, h=300),
    ],
    watch=['cnt', 'now', ('l_cnt', 'l_cnt', 'blue'), ('r_cnt', 'r_cnt', 'pink'), 'index', 'p'],
    captions={
        'cnt = 0': '`cnt` 先数整个字符串里 1 的个数',
        'for char in s': '逐个字符看，数 `1` 有几个',
        'if char == ': lambda S, B, r: (f"`'{S.char}'` 是 1，`cnt` 加一" if S.char == '1' else f"`'{S.char}'` 是 0，不计数"),
        'if cnt == 0': lambda S, B, r: ('全是 0：`n` 个球放 3 个盒子，插 2 块板子 → `C(n-1, 2)`' if S.cnt == 0 else f'`cnt = {S.cnt}` 不是 0，走一般情况'),
        'if cnt % 3 != 0': lambda S, B, r: (f'`{S.cnt} % 3 != 0`：1 无法平分成三份 → 答案 0' if S.cnt % 3 else f'`{S.cnt}` 是 3 的倍数，每段恰好 `{S.cnt // 3}` 个 1'),
        'cnt //= 3': '每段 1 的个数 `cnt = {cnt}`',
        'if s[index] == ': lambda S, B, r: (f"`s[{S.index}] = '1'`，从一侧数 1" if S.s[S.index] == '1' else f"`s[{S.index}] = '0'`，不是 1，继续"),
        'now += 1': '数到第 `{now}` 个 1',
        'if now == cnt': lambda S, B, r: ((f'`now = {S.now}` == `cnt`：从左数够了第一段的 1，`index = {S.index}` 是左边界' if S._line < 30 else f'`now = {S.now}` == `cnt`：从右数够了第三段的 1，`index = {S.index}` 是右边界') if S.now == S.cnt else f'`now = {S.now} < cnt = {S.cnt}`，继续数'),
        'break': '找到边界，退出',
        'p = index + 1': '从边界右边找下一个 1：`p = {p}`',
        'p = index - 1': '从边界左边找前一个 1：`p = {p}`',
        'while s[p] != ': lambda S, B, r: (f"`s[{S.p}] = '0'`：这段 0 夹在两个 1 之间，继续找" if S.s[S.p] != '1' else f"`s[{S.p}] = '1'`：找到了"),
        'p += 1': '`p` 右移到 {p}',
        'p -= 1': '`p` 左移到 {p}',
        'l_cnt =': '左切口 `index` 与 `p` 之间有 `{l_cnt}` 个 0，这些 0 可以归第一段或第二段，分配方案 `{l_cnt + 1}` 种',
        'r_cnt =': '右切口 `p` 与 `index` 之间有 `{r_cnt}` 个 0，可归第二段或第三段，方案 `{r_cnt + 1}` 种',
        'now = 0': '`now` 记录已经数到第几个 1',
        'return (l_cnt': '两处独立，乘法原理：`({l_cnt} + 1) × ({r_cnt} + 1)` = =={ret}==',
    },
    cards=dict(
        one_liner='三段 1 一样多，只剩两处 0 的空隙可以挪，两处方案数相乘',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，切成三个非空部分，每部分 `1` 的个数相同',
                 '求切法总数，对 `10^9 + 7` 取余',
                 '示例：`"10101"` → `4`；本视频：`"0010010010"` → `9`'],
        quote='若cnt是3的倍数，则可以从两侧开始，向中间分别数cnt/3个1，此时可以得到两个位置l和r。接下来找出l下一个1的位置l_next，以及r的前一个位置r_prev，而最终的操作空间就是l + 1到l_next - 1之间的0，以及r_prev + 1到r - 1之间的0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数 1 的总数 `cnt`：不是 3 的倍数 → 0；全是 0 → `C(n-1, 2)`',
              '从左数 `cnt/3` 个 1 得边界，再看它与下一个 1 之间的 0，每个位置都可左可右',
              '右侧同理；两侧互不影响，答案 `(l_cnt + 1) * (r_cnt + 1)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（含 `cnt /= 3`），并删去类型文档',
                 '全 0 的特判必须在 `cnt % 3` 之前，否则 `0 % 3 == 0` 会走到下面越界',
                 '切口位置 = 两个 1 之间 `k` 个 0 的 `k + 1` 个空隙'],
    ),
)
