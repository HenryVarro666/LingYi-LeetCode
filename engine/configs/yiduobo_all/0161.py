CONFIG = dict(
    num=161, title='相隔为 1 的编辑距离', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按长度差分情况，一趟遍历',
    code='''
class Solution(object):
    def isOneEditDistance(self, s, t):

        length_diff = len(s) - len(t)
        if abs(length_diff) > 1:
            return False
        
        if length_diff == 0:
            flag = False
            for index in range(len(s)):
                if s[index] != t[index]:
                    if not flag:
                        flag = True
                    else:
                        return False
            
            return flag
        
        else:
            if length_diff < 0:
                s, t = t, s
            
            p = 0
            flag = False
            for index in range(len(t)):
                if t[index] != s[p]:
                    if not flag:
                        flag = True
                    else:
                        return False
                    
                    p += 1
                    if s[p] != t[index]:
                        return False
                
                p += 1
            
            return True
''',
    call="Solution().isOneEditDistance('abcde', 'abde')",
    expect=True,
    views=[
        dict(type='string', var='s', label='s（较长者）', cell=80, h=190,
             pointers={'p': 'pink'}, color=lambda S, i, v: 'pink' if i == S.get('p') else None),
        dict(type='string', var='t', label='t', cell=80, h=190,
             pointers={'index': 'blue'}, color=lambda S, i, v: 'blue' if i == S.get('index') else None),
    ],
    watch=['length_diff', 'index', 'p', ('flag', 'flag', 'orange')],
    captions={
        'length_diff = ': '长度差 `{length_diff}`：0 → 恰好改一个字符；±1 → 恰好多/少一个字符',
        'if abs(length_diff) > 1': lambda S, B, ret: ('长度差超过 1，一次编辑不可能 → False' if abs(S.length_diff) > 1 else f'`|{S.length_diff}| <= 1`，有可能，继续分情况'),
        'if length_diff == 0': lambda S, B, ret: ('等长：只能是==替换==，要恰好有一个位置不同' if S.length_diff == 0 else '长度差为 1：只能是==插入/删除==一个字符'),
        'if length_diff < 0': lambda S, B, ret: ('`s` 更短，交换让 `s` 一定是较长的' if S.length_diff < 0 else '`s` 已经是较长的，不用交换'),
        's, t = t, s': '交换后 `s = {s!r}` 较长，`t = {t!r}` 较短',
        'p = 0': '`p`：`s` 中下一个要和 `t` 匹配的位置',
        'flag = False': '`flag`：是否已经出现过一处不同',
        'if s[index] != t[index]': '比较 `s[{index}] = {s[index]!r}` 和 `t[{index}] = {t[index]!r}`：{"不同" if s[index] != t[index] else "相同，跳过"}',
        'if t[index] != s[p]': '比较 `t[{index}] = {t[index]!r}` 和 `s[{p}] = {s[p]!r}`：{"不同，s 里这个字符多出来了" if t[index] != s[p] else "相同，一起往后走"}',
        'if not flag': lambda S, B, ret: ('第一处不同，允许一次' if not S.flag else '已经有过一处不同，这是第二处 → False'),
        'flag = True': '记下：已经用掉这一次编辑',
        'return False': '不满足 → `False`',
        32: '`s[{p-1}]` 是多出来的那个字符，跳过它：`p` → {p}',
        36: '这一位匹配成功，`p` 后移到 {p}',
        'if s[p] != t[index]': '跳过 `s` 里多的那个字符，用 `s[{p}] = {s[p]!r}` 再匹配 `t[{index}] = {t[index]!r}`：{"仍不匹配 → False" if s[p] != t[index] else "匹配上了"}',
        'return flag': '等长情况：`flag = {flag}`（全相同则 flag 仍为 False，不算一次编辑）',
        'return True': '一趟走完都能匹配 → ==True==',
    },
    cards=dict(
        one_liner='先看长度差：等长就找唯一不同，差 1 就跳过多出的那个字符',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给两个字符串 `s` 和 `t`，判断它们是否==恰好相差一次编辑==',
                 '一次编辑：插入、删除或替换一个字符',
                 '示例：`s = "abcde"`，`t = "abde"` → `True`（删掉 `c`）'],
        quote='若s和t长度差的绝对值大于1，那么答案必然也是false。……当两个字符串长度相等时，那么s和t中就必须有且仅有一个位置上的字符不同。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度差 > 1：直接 False；完全相同也不算（编辑距离是 0）',
              '等长：用 `flag` 记是否已有不同位置，出现第二处就 False，最后返回 `flag`',
              '差 1：先交换让 `s` 更长，`p` 指 `s`；遇到不同时跳过 `s[p]`，再试 `s[p+1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：等长时 `flag` 为 False（两串相同）要返回 False',
                 '易错点：长度差 1 时，若 `t` 已走完而 `s` 还多一个字符，也是合法（末尾多一个字符）',
                 '易错点：不同时 `p += 1` 后要再检查 `s[p]`，注意别越界',
                 '本视频演示长度差 1 的删除情形 `abcde` 与 `abde`'],
    ),
)
