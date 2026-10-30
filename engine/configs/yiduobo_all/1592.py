def _pos(S):
    """已经处理过的字符数（每个字符不是进了 cnt，就是进了单词）"""
    if 'cnt' not in S:
        return 0
    return S['cnt'] + sum(len(w) for w in S['word_list']) + len(S['now'])


def _top(S):
    if 'cnt' not in S:
        return ''
    if 'n' in S:
        return f"{S['cnt']} 个空格，{S['n']} 个间隔 → 每个间隔 `{S['cnt'] // S['n']}` 个，末尾剩 `{S['cnt'] % S['n']}` 个"
    return f"空格数 `cnt = {S['cnt']}`，单词 `{S['word_list']}`，正在拼 `'{S['now']}'`"


CONFIG = dict(
    num=1592, title='重新排列单词间的空格', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 分离单词并数空格',
    tags=[],
    code='''
class Solution(object):
    def reorderSpaces(self, text):

        cnt = 0
        word_list = []
        now = ''
        for char in text:
            if char == ' ':
                if now != '':
                    word_list.append(now)
                    now = ''
                cnt += 1
            else:
                now += char
        
        if now != '':
            word_list.append(now)
        
        if len(word_list) == 1:
            return word_list[0] + ' ' * cnt
        
        n = len(word_list) - 1 
        return (' ' * (cnt // n)).join(word_list) + ' ' * (cnt % n)
''',
    call='Solution().reorderSpaces("  this   is  a sentence  ")',
    expect="this   is   a   sentence ",
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='text', label='text（绿 = 已数过的空格，灰 = 已进单词的字母）', cell=38,
             color=lambda S, i, v: 'green' if v == ' ' and i < _pos(S) else None,
             dim=lambda S, i, v: i < _pos(S) and v != ' '),
        dict(type='array', var='word_list', label='word_list（分离出的单词）', cell=200),
        dict(type='text', fn=lambda S: f"当前单词 `now = '{S['now']}'`" if 'now' in S else '', size=26),
    ],
    watch=[('cnt', 'cnt', 'green'), ('now', 'now', 'blue'), ('word_list', 'word_list', 'pink'), 'n'],
    captions={
        'cnt = 0': '`cnt` 统计空格总数',
        'word_list = []': '`word_list` 收集分离出来的单词',
        "now = ''": lambda S, B, ret: ('`now` 拼正在读的单词' if S['_line'] < 7 else '`now` 清空，准备读下一个单词'),
        'for char in text': "读下一个字符 `char = '{char}'`",
        "if char == ' '": lambda S, B, ret: ("是空格 → 当前单词（如果有）到此结束" if S.char == ' ' else "是字母 → 接到当前单词后面"),
        "if now != ''": lambda S, B, ret: (("`now` 非空：最后一个单词后面没有空格，==别漏掉它==，存起来" if S['_line'] > 9 else f"`now = '{S.now}'` 非空：空格前是一个完整单词，存起来") if S.now != ''
                                           else ("`now` 为空：已经存过，没有漏掉的单词" if S['_line'] > 9 else "`now` 为空：连续空格或开头空格，没有单词可存")),
        'word_list.append(now)': '单词 `{now}` 放进 `word_list`：{word_list}',
        'cnt += 1': '空格数 `cnt` → =={cnt}==',
        'now += char': '`now` → `{now}`',
        'if len(word_list) == 1': lambda S, B, ret: (f'只有 1 个单词：没有间隔可分，==空格全放末尾==' if len(S.word_list) == 1
                                                     else f'有 {len(S.word_list)} 个单词，可以平均分配空格'),
        'return word_list[0]': '单词 `{word_list[0]}` 后面补 `{cnt}` 个空格',
        'n = len': '间隔数 `n = 单词数 - 1 = {n}`',
        'return (': '每个间隔 `{cnt} // {n} = {cnt // n}` 个空格，多出的 `{cnt} % {n} = {cnt % n}` 个放末尾 → `"{ret}"`',
    },
    cards=dict(
        one_liner='一趟扫描分出单词、数出空格，再平均分给间隔，余数补末尾',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`text` 由单词和空格组成，重新排列空格：==相邻单词间的空格数相同且尽量多==',
                 '若有多余空格，放在字符串==末尾==；返回长度不变的新字符串',
                 '本视频：`"  this   is  a sentence  "` → `"this   is   a   sentence "`'],
        quote='直接一趟扫描，将各个单词分离出来，并统计空格的总数，最后按题目要求的分配空格之后输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['扫描时遇到空格：先把 `now` 里攒的单词存起来，再 `cnt += 1`',
              '遇到字母就接到 `now` 后面；扫完别漏了最后一个单词',
              '`n = 单词数 - 1` 个间隔，每个 `cnt // n` 个空格，余 `cnt % n` 个放末尾'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：循环结束后==还要把最后一个单词存起来==（文本不以空格结尾时）',
                 '易错：只有 1 个单词时 `n = 0`，会除零，要特判：空格全放末尾',
                 '原文为 Python 2 写法，整数除法 `cnt / n` 已改为 `cnt // n`'],
    ),
)
