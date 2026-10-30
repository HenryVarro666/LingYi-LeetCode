STR = '5223343'


def _lo(S):
    if 'index' not in S:
        return None
    return 0 if S.get('b') is None else S['b']


def _pair_idx(S):
    """到当前 index 为止所有相邻重复组的后一个字符下标"""
    if 'index' not in S:
        return []
    s = S['s']
    return [i for i in range(1, S['index'] + 1) if s[i] == s[i - 1]]


def _color(S, i, v):
    if 'index' not in S:
        return None
    a, b = S.get('a'), S.get('b')
    if a is not None and i in (a - 1, a):
        return 'orange'
    if b is not None and i in (b - 1, b):
        return 'purple'
    lo = _lo(S)
    if lo <= i <= S['index']:
        return 'blue'
    return None


def _dim(S, i, v):
    return 'index' in S and i > S['index']


def _top(S):
    if 'index' not in S:
        return '先找出所有==相邻重复字符组==的位置'
    a, b = S.get('a'), S.get('b')
    if b is None:
        return f"重复组不到两组 → 整个前缀 `s[0..{S['index']}]` 都合法，长 `{S['index'] + 1}`"
    return f"最近两组在 `{b - 1},{b}`（紫）和 `{a - 1},{a}`（橙）：左边界最远到 `b = {b}`，长 `{S['index'] - b + 1}`"


def _if(S, B, ret):
    i, s = S.index, S.s
    if i > 0 and s[i] == s[i - 1]:
        return f'`s[{i}] = s[{i - 1}] = {s[i]}`：发现一组相邻重复'
    if i == 0:
        return '`index = 0`，没有前一个字符'
    return f'`{s[i - 1]} ≠ {s[i]}`，不是重复组'


CONFIG = dict(
    num=2730, title='找到最长的半重复子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='记录最近两组相邻重复位置',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def longestSemiRepetitiveSubstring(self, s):

        res = 0
        b = a = None
        for index in range(len(s)):
            if index > 0 and s[index] == s[index - 1]:
                b, a = a, index

            if b is None:
                res = index + 1
            else:
                res = max(res, index - b + 1)

        return res
''',
    call=f'Solution().longestSemiRepetitiveSubstring({STR!r})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='s', label='s（橙 = 最近一组重复 a，紫 = 前一组 b，框 = 以 index 结尾的最长合法子串）',
             pointers={'index': 'pink', 'b': 'purple', 'a': 'orange'}, window=(_lo, 'index'), color=_color, dim=_dim,
             cell=110, h=340),
    ],
    watch=[('index', 'index', 'pink'), ('b', 'b', 'purple'), ('a', 'a', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res = 0`',
        'b = a = None': '`a`：最靠后一组重复的后一个字符下标；`b`：再前一组；初始都没有',
        'for index in': lambda S, B, r: ('遍历结束' if 'index' in B and B.index == S.index
                                         else f'看 `s[{S.index}] = {S.s[S.index]}`'),
        'if index > 0 and': _if,
        'b, a = a, index': '两个变量往后迭代：`b = {b}`，`a = {a}`',
        'if b is None': lambda S, B, r: ('`b is None`：重复组不到两组，==整个前缀都合法==' if S.b is None
                                         else f'已有两组：子串若包含 a 这组，左边界最远是 `b = {S.b}`'),
        'res = index + 1': '前缀长度 `{index} + 1` → `res = {res}`',
        'res = max(res': '`s[{b}..{index}]` 长 `{index - b + 1}`：`res = max({B.res}, {index - b + 1})` = =={res}==',
        'return res': '最长半重复子串长 =={ret}==',
    },
    cards=dict(
        one_liner='只看最近两组相邻重复：左边界最远只能到前一组的后一个字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==半重复==：至多一对相邻字符相等',
                 '求 `s` 中最长半重复子串的长度',
                 '示例：`"52233"` → `4`；本视频 `"5223343"` → `5`'],
        quote='如果子串需要包含这一组字符，那么其==左边界最远就只能选择第index - 1组相邻重复字符的后一个字符==，而右边界最远则是第index + 1组相邻重复字符的前一个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['只需考虑连续的三组重复，用 `b`、`a` 两个变量迭代最近两组',
              '以 index 结尾时，合法子串最远从 `b`（前一组的后一个字符）开始',
              '不到两组时，整个前缀都合法'],
        summary=['时间 `O(n)`，空间 `O(1)`，不需要显式的 left 指针',
                 '`b, a = a, index`：记录的是重复组==后一个字符==的下标',
                 '长度是 `index − b + 1`：`s[b−1]` 被排除，这一组就拆开了',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动',
                 '对比灵神：灵神用 cnt 计数 + 滑窗缩左端；这里直接跳到 b'],
    ),
)
