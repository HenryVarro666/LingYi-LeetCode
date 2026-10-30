S0 = '  is joy  '


def _found(S):
    return S.get('_line') == 9 and 'start' in S


def _color(S, i, v):
    if 'end' not in S:
        return None
    if _found(S) and S['start'] < i <= S['end']:
        return 'green'
    if i == S['end'] and 'start' not in S:
        return 'blue'
    if 'start' in S and i == S['start'] and S['start'] >= 0:
        return 'pink'
    if 'start' in S and S['start'] < i <= S['end']:
        return 'purple'
    return None


def _dim(S, i, v):
    if 'end' not in S:
        return False
    if i > S['end']:
        return True
    return _found(S) and i <= S['start']


def _text(S):
    if _found(S):
        return f"`end − start` = `{S['end']} − {S['start']}` = =={S['end'] - S['start']}==（start 是空格，不算在单词里）"
    if 'start' in S:
        return '第二步：从结尾字符往前，找==第一个空字符== → `start`'
    if 'end' in S:
        return '第一步：从后往前，找==第一个非空字符== → `end`'
    return ''


def _cap_w1(S, B, ret):
    e = B.end
    if e < 0:
        return '`end < 0`：已经走出字符串'
    if S.s[e] == ' ':
        return f'`end = {e} ≥ 0` 且 `s[{e}]` 是空格 → 继续往前'
    return f'`s[{e}] = "{S.s[e]}"` 非空 → ==它就是最后一个单词的结尾字符==，停止'


def _cap_w2(S, B, ret):
    st = B.start
    if st < 0:
        return '`start = -1`：走出了字符串左边界 → 停止（==边界问题==）'
    if S.s[st] != ' ':
        return f'`s[{st}] = "{S.s[st]}"` 还是字母 → 继续往前'
    return f'`s[{st}]` 是==空字符== → 它的后一个字符就是单词的起始字符，停止'


CONFIG = dict(
    num=58, title='最后一个单词的长度', difficulty='Easy', category='字符串',
    author='yiduobo', technique='从后往前：找结尾，再找空格',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def lengthOfLastWord(self, s):
        end = len(s) - 1
        while end >= 0 and s[end] == ' ':
            end -= 1
        start = end
        while start >=0 and s[start] != ' ':
            start -= 1
        return end - start
''',
    call=f'Solution().lengthOfLastWord({S0!r})',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='string', var='s', label='s（灰 = 跳过，紫 = 已扫过的字母，绿 = 最后一个单词）', cell=96, h=300,
             pointers={'end': 'blue', 'start': 'pink'}, color=_color, dim=_dim),
    ],
    watch=[('end', 'end', 'blue'), ('start', 'start', 'pink'),
           ('end - start', lambda S: S['end'] - S['start'] if _found(S) else None, 'green')],
    captions={
        'end = len(s) - 1': '从后往前扫：`end = len(s) - 1 = {end}`',
        "while end >= 0 and s[end] == ' '": _cap_w1,
        'end -= 1': '`end` 前移 → {end}',
        'start = end': '从结尾字符开始往前找空字符：`start = end = {start}`',
        'while start >=0': _cap_w2,
        'start -= 1': '`start` 前移 → {start}',
        'return end - start': '单词是 `s[start+1 .. end]`，长度 `{end} − {start}` = =={ret}==',
    },
    cards=dict(
        one_liner='从后往前：先找最后一个非空字符，再找它前面的空字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 由单词和空格组成，返回==最后一个==单词的长度',
                 '单词：只由字母组成、不含空格的最长子串',
                 '示例：`"luffy is still joyboy"` → `6`',
                 '本视频：`"  is joy  "` → `3`'],
        quote='从后往前，找到第一个非空字符，那么这个字符就是最后一个单词的结尾字符。接下来从这个结尾字符往前，找到第一个空字符，那么这个空字符的==后一个字符==就是最后一个单词的起始字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`end`：最后一个单词的结尾字符；`start`：它前面第一个空字符',
              '单词是 `s[start+1 .. end]`，长度 `end − start`',
              '原文提醒：==往前找字符时注意边界==，两个循环都判了 `>= 0`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`start` 走到 `-1` 时恰好相当于"下标 -1 处有个空格"，公式不变',
                 '第一个循环的 `end >= 0` 是防御性写法：全是空格时不会越界',
                 '对比灵神：灵神 `j = i - 1` 起步、第一个循环省掉边界判断，思路一致',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
