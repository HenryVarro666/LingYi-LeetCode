S0 = 'fly moon  '


def _found(S):
    """第二个循环结束后（到了 return 行）才知道单词区间 [j+1, i]"""
    return S.get('_line') == 11 and 'j' in S


def _color(S, i, v):
    if 'i' not in S:
        return None
    if _found(S) and S['j'] < i <= S['i']:
        return 'green'
    if i == S['i']:
        return 'blue'
    if 'j' in S and i == S['j'] and S['j'] >= 0:
        return 'pink'
    if 'j' in S and S['j'] < i < S['i']:
        return 'purple'  # 已确认是字母
    return None


def _dim(S, i, v):
    if 'i' not in S:
        return False
    if i > S['i']:
        return True  # 末尾空格，已经跳过
    return _found(S) and i <= S['j']


def _text(S):
    if 'j' in S and _found(S):
        return f"单词是 `s[{S['j'] + 1}..{S['i']}]`，长度 = `i − j` = `{S['i']} − ({S['j']})` = =={S['i'] - S['j']}=="
    if 'j' in S:
        return f"找 `i` 左边最近的空格 `j`：单词就是 `s[j+1..i]`"
    if 'i' in S:
        return '先跳过末尾空格，找到==最后一个非空格字符== `i`'
    return ''


def _cap_w1(S, B, ret):
    i = B.i
    if S.s[i] == ' ':
        return f'`s[{i}]` 是空格 → 还在末尾空格里，继续往左'
    return f'`s[{i}] = "{S.s[i]}"` 不是空格 → ==找到单词的最后一个字母== `i = {i}`'


def _cap_w2(S, B, ret):
    j = B.j
    if j < 0:
        return '`j = -1`：左边没有空格了 → 单词从下标 0 开始，停止'
    if S.s[j] != ' ':
        return f'`s[{j}] = "{S.s[j]}"` 还是字母 → 继续往左找空格'
    return f'`s[{j}]` 是==空格== → 它就是 `i` 左边最近的空格，停止'


CONFIG = dict(
    num=58, title='最后一个单词的长度', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='倒序找首尾：i − j',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        while s[i] == ' ':
            i -= 1

        j = i - 1
        while j >= 0 and s[j] != ' ':
            j -= 1

        return i - j
''',
    call=f'Solution().lengthOfLastWord({S0!r})',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='string', var='s', label='s（紫 = 已确认是字母，绿 = 最后一个单词）', cell=96, h=300,
             pointers={'i': 'blue', 'j': 'pink'}, color=_color, dim=_dim),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('i - j', lambda S: S['i'] - S['j'] if _found(S) else None, 'green')],
    captions={
        'i = len(s) - 1': '从最后一个字符开始：`i = len(s) - 1 = {i}`',
        "while s[i] == ' '": _cap_w1,
        'i -= 1': '`i` 左移 → {i}',
        'j = i - 1': '`s[i]` 一定是字母，所以从 `i - 1` 开始找空格：`j = {j}`',
        'while j >= 0': _cap_w2,
        'j -= 1': '`j` 左移 → {j}',
        'return i - j': '单词是 `s[j+1..i]`，长度 `i − j = {i} − {j}` = =={ret}==',
    },
    cards=dict(
        one_liner='最后一个字母的下标 i，减去它左边最近空格的下标 j',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 由单词和空格组成，返回==最后一个==单词的长度',
                 '单词：只由字母组成、不含空格的最长子串',
                 '示例：`"   fly me   to   the moon  "` → `4`（moon）',
                 '本视频：`"fly moon  "` → `4`'],
        quote='单词第一个字母的下标，我们可以找到在 i 左边的==最近空格的下标==，记作 j，那么 j+1 就是这个单词的第一个字母的下标。如果左边没有空格，那么 j=-1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i`：最后一个==非空格==字符的下标（先跳过末尾空格）',
              '`j`：`i` 左边最近的空格，没有就是 `-1`',
              '单词占 `s[j+1..i]`，长度 = `i − j`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '第一个循环不用判 `i >= 0`：题目保证至少有一个单词',
                 '第二个循环要判 `j >= 0`：单词可能从下标 0 开始，此时 `j = -1` 正好',
                 '写法二（库函数）：`s = s.rstrip()`，答案 `len(s) - 1 - s.rfind(" ")`'],
    ),
)
