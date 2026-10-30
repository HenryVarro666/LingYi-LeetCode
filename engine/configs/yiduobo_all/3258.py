S0, K0 = '1010101', 2


def _color(S, i, v):
    if 'index' not in S:
        return None
    if S['p'] <= i <= S['index']:
        return 'green' if S['_line'] == 22 else 'blue'
    return None


def _top(S):
    if 'index' not in S:
        return f'`k = {K0}`：窗口内 0、1 ==同时超过== k 才需要收缩左边界 p'
    p, i = S['p'], S['index']
    z, o = S['zero'], S['one']
    bad = z > K0 and o > K0
    return (f"窗口 `s[{p}..{i}] = {S0[p:i + 1]!r}`：zero = `{z}`，one = `{o}` → "
            + ('都超过 k，p 要右移' if bad else '==满足 k 约束=='))


def _while(S, B, ret):
    if S.one > S.k and S.zero > S.k:
        return f'`one = {S.one}`、`zero = {S.zero}` ==都超过== `k = {S.k}` → 移动左边界 p'
    return f'`one = {S.one}`、`zero = {S.zero}`：至少一个 ≤ {S.k}，窗口合法'


CONFIG = dict(
    num=3258, title='统计满足 K 约束的子字符串数量 I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 按右端点计数',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def countKConstraintSubstrings(self, s, k):

        zero = 0
        one = 0
        res = 0

        p = 0
        for index, char in enumerate(s):
            if char == '1':
                one += 1
            else:
                zero += 1

            while one > k and zero > k:
                if s[p] == '0':
                    zero -= 1
                else:
                    one -= 1
                p += 1

            res += (index - p + 1)

        return res
''',
    call=f'Solution().countKConstraintSubstrings({S0!r}, {K0})',
    expect=25,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（框 = 窗口 [p, index]，绿 = 本轮累加的起点）',
             pointers={'p': 'cyan', 'index': 'orange'}, window=('p', 'index'), color=_color, cell=110, h=300),
    ],
    watch=[('p', 'p', 'cyan'), ('index', 'index', 'orange'), ('zero', 'zero', 'blue'), ('one', 'one', 'pink'),
           ('res', 'res', 'green')],
    skip=['zero = 0', 'one = 0', "if char == '1'"],
    captions={
        'res = 0': '`zero`、`one` 记录窗口内 0 和 1 的数量，`res` 累计答案',
        'p = 0': '窗口左边界 `p = 0`',
        'for index, char': lambda S, B, r: ('右边界走到末尾，结束' if 'index' in B and B.index == S.index
                                            else f'右边界移到 `index = {S.index}`，`{S.char!r}` 进窗口'),
        "if char == '1'": lambda S, B, r: f"新字符是 `{S.char!r}`",
        'one += 1': "新字符是 '1'：`one` → {one}",
        'zero += 1': "新字符是 '0'：`zero` → {zero}",
        'while one > k': _while,
        "if s[p] == '0'": '左边界字符 `s[{p}] = {s[p]!r}` 离开窗口',
        'zero -= 1': '`zero` → {zero}',
        'one -= 1': '`one` → {one}',
        'p += 1': '`p` → {p}',
        'res += (index': '起点 `{p}..{index}`、终点 `{index}` 的子串都满足：`res += {index - p + 1}` → =={res}==',
        'return res': '共 =={ret}== 个 k 约束子串',
    },
    cards=dict(
        one_liner='右边界每走一步，以它为终点的合法子串有 index − p + 1 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`：0 的数量 ≤ k ==或== 1 的数量 ≤ k，就称满足 k 约束',
                 '求 `s` 中满足 k 约束的子串个数',
                 '示例：`s = "1010101", k = 2` → `25`（长度 > 5 的子串都不满足）'],
        quote='窗口内0和1的数量可能同时超过k，此时就需要不断向后移动左边界……起点在p、p + 1、…、index，终点在index的子串都是满足k约束的，一共有==index - p + 1==个',
        quote_src='—— yiduobo 题解原文',
        idea=['`zero`、`one` 两个计数器跟着窗口进出更新',
              '两个都 > k 时窗口不合法，p 右移直到有一个回到 ≤ k',
              '合法窗口的任意后缀也合法 → 累加窗口长度'],
        summary=['时间 `O(n)`：p 只右移；空间 `O(1)`',
                 '易错：收缩条件是 `one > k and zero > k`，不是 `or`',
                 '累加的是窗口长度 `index − p + 1`，不是 1',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
