CONFIG = dict(
    num=1417, title='重新格式化字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字母数字分组 · 从多的一类开始交替',
    code='''
class Solution(object):
    def reformat(self, s):

        char_list = []
        digit_list = []
        for char in s:
            if char >= '0' and char <= '9':
                digit_list.append(char)
            else:
                char_list.append(char)
        
        char_cnt = len(char_list)
        digit_cnt = len(digit_list)
        if abs(char_cnt - digit_cnt) > 1:
            return ""
        
        res = []
        if char_cnt > digit_cnt:
            for index in range(digit_cnt):
                res.append(char_list[index])
                res.append(digit_list[index])
            res.append(char_list[-1])
        else:
            for index in range(char_cnt):
                res.append(digit_list[index])
                res.append(char_list[index])
            if digit_cnt > char_cnt:
                res.append(digit_list[-1])
        
        return ''.join(res)
''',
    call='Solution().reformat("a1b23")',
    expect='1a2b3',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符）', cell=70, h=190,
             color=lambda S, i, v: 'blue' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='array', var=lambda S: S.get('char_list', []), label='char_list（字母）', cell=70, h=170,
             color=lambda S, i, v: 'pink'),
        dict(type='array', var=lambda S: S.get('digit_list', []), label='digit_list（数字）', cell=70, h=170,
             color=lambda S, i, v: 'cyan'),
        dict(type='array', var=lambda S: S.get('res', []), label='res（交替拼出的答案）', cell=70, h=170,
             color=lambda S, i, v: 'green'),
    ],
    watch=['char_cnt', 'digit_cnt', ('index', 'index', 'blue')],
    captions={
        'char_list = []': '`char_list` 存字母',
        'digit_list = []': '`digit_list` 存数字',
        'for char in s': '取下一个字符 `char = {char!r}`',
        "if char >= '0'": lambda S, B, r: (f"`'{S.char}'` 在 `'0'` 到 `'9'` 之间 → ==是数字==" if '0' <= S.char <= '9' else f"`'{S.char}'` 不在 `'0'` 到 `'9'` 之间 → 是字母"),
        'digit_list.append': '数字放进 `digit_list` → `{digit_list}`',
        'char_list.append': '字母放进 `char_list` → `{char_list}`',
        'char_cnt = len': '字母有 `{char_cnt}` 个',
        'digit_cnt = len': '数字有 `{digit_cnt}` 个',
        'if abs(': lambda S, B, r: (f'`|{S.char_cnt} − {S.digit_cnt}| = {abs(S.char_cnt - S.digit_cnt)} > 1`：多的一类塞不进空隙 → ==返回空串==' if abs(S.char_cnt - S.digit_cnt) > 1
                                    else f'`|{S.char_cnt} − {S.digit_cnt}| = {abs(S.char_cnt - S.digit_cnt)} ≤ 1`：可以交替排列，开始构造'),
        'res = []': '`res` 用列表收集，最后一次性 `join`',
        'if char_cnt > digit_cnt': lambda S, B, r: (f'字母 {S.char_cnt} 个 > 数字 {S.digit_cnt} 个 → ==字母打头，字母收尾==' if S.char_cnt > S.digit_cnt
                                                  else f'字母 {S.char_cnt} 个 ≤ 数字 {S.digit_cnt} 个 → ==数字打头=='),
        'for index in range(digit_cnt)': '字母多：按数字个数配对，每轮 “字母 + 数字”，`index = {index}`',
        'for index in range(char_cnt)': '数字不少于字母：按字母个数配对，每轮 “数字 + 字母”，`index = {index}`',
        'res.append(char_list[index])': '放入字母 `{res[-1]}`：`res` = `{res}`',
        'res.append(digit_list[index])': '放入数字 `{res[-1]}`：`res` = `{res}`，字母数字交替',
        'res.append(char_list[-1])': '字母比数字多 1 个，剩下的最后一个字母放末尾：`{res}`',
        'if digit_cnt > char_cnt': lambda S, B, r: ('数字比字母多 1 个 → 还剩一个数字要放末尾' if S.digit_cnt > S.char_cnt else '两类一样多，正好配完，不用补'),
        'res.append(digit_list[-1])': '剩下的最后一个数字放末尾：`{res}`',
        'return ': lambda S, B, r: f'拼成字符串 `{r}`',
    },
    cards=dict(
        one_liner='数字和字母个数最多差 1，才能交替；从多的一类开头',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含小写字母和数字，重新排列使得==相邻字符类型不同==（字母、数字交替）',
                 '有多种答案返回任意一个；不可能就返回空串',
                 '示例：`a0b1c2` → `0a1b2c`；`leetcode` → `""`'],
        quote='为了使得最终答案中数字与字符交替出现，那么数字出现的次数以及字符的次数之间的差值必须小于1。若满足该条件，那么我们从出现较多的那一种开始交替使用来构造答案。',
        quote_src='—— yiduobo 题解原文（原文“小于 1”指不超过 1）',
        idea=['一趟扫描把字母、数字分别放进两个列表',
              '个数差 `> 1` → 必有两个同类相邻 → 返回 `""`',
              '否则从多的一类开始，一个字母一个数字地交替放；多出的 1 个放末尾'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：差值 `> 1` 才无解；差为 0 时谁先谁后都行（原文数字打头）',
                 '字母多 1 个时必须字母打头、字母收尾，所以最后补 `char_list[-1]`',
                 '本例 `a1b23`：数字 3 个多于字母 2 个，数字打头 → `1a2b3`',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)


def _cur(S):
    if 'char' not in S:
        return None
    k = len(S.get('char_list', [])) + len(S.get('digit_list', []))
    return k - 1 if S['_line'] >= _ADDED else k


_ADDED = 8
