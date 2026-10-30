def _color(S, i, v):
    inv = S.get('invalid_set') or set()
    if i in inv:
        return 'red'
    if 'index' in S and i == S['index'] and 'char' in S:
        return 'blue'
    if v == '(' and i in (S.get('stack') or []):
        return 'yellow'
    return None


def _txt(S):
    if 'stack' not in S:
        return ''
    if S.get('_line', 0) >= 20 and 'res' in S:
        return f"第二遍：不在 `invalid_set` 里的字符才拼进 `res = \"{S['res']}\"`"
    return f"栈 `{S['stack']}` 里是未配对的左括号；`invalid_set = {sorted(S['invalid_set'])}` 是确定要删的"


CONFIG = dict(
    num=1249, title='移除无效的括号', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈判别括号 · 记下非法下标再重建',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1657'],
    code='''
class Solution(object):
    def minRemoveToMakeValid(self, s):

        stack = []
        invalid_set = set()
        for index, char in enumerate(s):
            if char == '(':
                stack.append(index)
            elif char == ')':
                if stack:
                    stack.pop()
                else:
                    invalid_set.add(index)
        
        while stack:
            invalid_set.add(stack.pop())
        
        res = ''
        for index, char in enumerate(s):
            if index not in invalid_set:
                res += char
        
        return res
''',
    call='Solution().minRemoveToMakeValid("l(e)e)t(c(")',
    expect='l(e)etc',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前，黄 = 栈中的左括号，红 = 非法要删）', cell=56, color=_color,
             pointers={'index': 'blue'}, h=170),
        dict(type='stack', var='stack', label='stack（左括号下标）', fmt=lambda x: str(x), h=150),
        dict(type='set', var='invalid_set', label='invalid_set（非法括号的下标）', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=lambda S: f"结果 `res = \"{S['res']}\"`" if 'res' in S else '', size=28),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink'), ('stack', 'stack', 'yellow'), ('invalid_set', 'invalid_set', 'orange')],
    captions={
        'stack = []': '`stack`：存放还没配对的左括号的==下标==',
        'invalid_set = set()': '`invalid_set`：记录确定非法的括号下标，最后统一删除',
        6: lambda S, B, r: (f"第一遍扫描：`index = {S.index}`，`char = '{S.char}'`" if S.index != B.get('index') or 'index' not in B else '第一遍扫描结束'),
        "if char == '('": lambda S, B, r: (f"`'{S.char}'` 是左括号 → 入栈等待配对" if S.char == '(' else f"`'{S.char}'` 不是左括号"),
        'stack.append(index)': '左括号下标 `{index}` 入栈：`stack = {stack}`',
        "elif char == ')'": lambda S, B, r: (f"`'{S.char}'` 是右括号 → 看栈里有没有左括号" if S.char == ')' else f"`'{S.char}'` 是字母 → 忽略，继续扫描"),
        'if stack': lambda S, B, r: (f"栈不空 `{S.stack}` → 有左括号可以和它成一对" if S.stack else '栈是空的 → 没有左括号能配，它是非法的'),
        11: '弹出栈顶 `{B.stack[-1]}`，和右括号 `{index}` 成一对：`stack = {stack}`',
        'invalid_set.add(index)': '右括号 `{index}` 非法 → 记入 `invalid_set = {invalid_set}`',
        'while stack': lambda S, B, r: (f"扫描完栈还剩 `{S.stack}`：这些左括号没有右括号" if S.stack else '栈空了，多余的左括号都处理完'),
        16: '多余的左括号 `{B.stack[-1]}` 弹出后记为非法：`invalid_set = {invalid_set}`',
        "res = ''": '第二遍扫描：把合法字符拼成答案 `res`',
        19: lambda S, B, r: (f"第二遍扫描：`index = {S.index}`，`char = '{S.char}'`" if S.index != B.get('index') else '第二遍扫描结束'),
        'if index not in invalid_set': lambda S, B, r: (f"`index = {S.index}` 不在 `invalid_set` 里 → 保留" if S.index not in S.invalid_set else f"`index = {S.index}` 在 `invalid_set` 里 → 跳过") if S.index != B.get('index') or True else '',
        'res += char': "保留 `'{char}'`：`res = \"{res}\"`",
        'return res': '返回 `"{res}"`',
    },
    max_steps=110,
    cards=dict(
        one_liner='忽略字母，用栈判别括号，非法的记下来再删',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串含小写字母和 `(` `)`，删去最少的括号使其有效，返回任意一个合法结果',
                 '示例：`lee(t(c)o)de)` → `lee(t(c)o)de`',
                 '本视频：`l(e)e)t(c(` → `l(e)etc`'],
        quote='题目的需求只跟括号有关，因此我们可以忽略掉所有的字母。题目中的有效括号字符串，实际上可以用经典的栈来进行判别。当出现非法的括号时，将其删去即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['左括号入栈；右括号时栈非空就弹出成对，栈空则它==非法==',
              '扫描完栈里还有的左括号也==非法==',
              '把非法下标放进 `invalid_set`，再扫一遍，只拼接不在集合里的字符'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '栈里存下标，才知道最后该删哪一个',
                 '`res += char` 在 Python 里逐个拼接可能偏慢，大数据可改用列表 `join`',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神直接把待删位置改成空串，只用一个 `t`；yiduobo 用集合记录再重建'],
    ),
)
