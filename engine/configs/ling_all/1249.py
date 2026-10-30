def _color(S, i, v):
    t = S.get('t')
    if t is not None and i < len(t) and t[i] == '':
        return 'red'
    if S.get('i') is not None and 'ch' in S and i == S['i']:
        return 'blue'
    if v == '(' and 'st' in S and i in S['st']:
        return 'yellow'
    return None


def _txt(S):
    st = S.get('st')
    if st is None:
        return ''
    t = S['t']
    gone = sum(1 for x in t if x == '')
    return f"栈里是==还没配对==的左括号下标 `{st}`；已标记删除 `{gone}` 个"


CONFIG = dict(
    num=1249, title='移除无效的括号', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈记录未匹配左括号的下标',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1657'],
    code='''
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        t = list(s)
        st = []

        for i, ch in enumerate(t):
            if ch == '(':
                st.append(i)  # 记录左括号的下标
            elif ch == ')':
                if st:
                    st.pop()  # 左右括号匹配
                else:
                    t[i] = ''  # 右括号没有与之匹配的左括号，标记为移除

        for i in st:
            t[i] = ''  # 栈中剩下的左括号没有与之匹配的右括号，标记为移除

        return ''.join(t)
''',
    call='Solution().minRemoveToMakeValid("l(e)e)t(c(")',
    expect='l(e)etc',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前，黄 = 栈中的左括号，红 = 标记删除）', cell=56, color=_color,
             pointers={'i': 'blue'}, h=180),
        dict(type='stack', var='st', label='st（未匹配左括号的下标）', fmt=lambda x: str(x), h=200),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'pink'), ('st', 'st', 'yellow')],
    captions={
        't = list(s)': '先转成列表 `t`，这样待删除的字符可以直接改成空串',
        'st = []': '`st` 是栈，只存==还没配对的左括号==的下标',
        'for i, ch in enumerate(t)': lambda S, B, r: (f"从左到右遍历：`i = {S.i}`，`ch = '{S.ch}'`" if S.i != B.get('i') or 'i' not in B else '遍历完 t 了'),
        "if ch == '('": lambda S, B, r: (f"`'{S.ch}'` 是左括号，先压栈等右括号来配" if S.ch == '(' else f"`'{S.ch}'` 不是左括号"),
        'st.append(i)': '左括号下标 `{i}` 入栈：栈 = `{st}`',
        "elif ch == ')'": lambda S, B, r: (f"`'{S.ch}'` 是右括号，要找左边最近的未匹配左括号" if S.ch == ')' else f"`'{S.ch}'` 是字母，保留，不管"),
        'if st:': lambda S, B, r: (f"栈非空 `{S.st}` → 左边有未匹配的左括号可以配对" if S.st else "栈是空的 → 左边没有左括号可配，这个右括号多余"),
        'st.pop()': '弹出栈顶：右括号 `{i}` 与左括号 `{B.st[-1]}` 配对，栈 = `{st}`',
        "t[i] = ''  # 右": '右括号 `{i}` 无法配对，==标记为删除==（改成空串）',
        'for i in st': lambda S, B, r: (f"栈里剩下 `{S.st}`，取出 `i = {S.i}`：这个左括号永远等不到右括号" if S.i != B.get('i') else '栈里的左括号都处理完了'),
        "t[i] = ''  # 栈": '栈中左括号 `{i}` 没有右括号配对，==标记为删除==',
        "return ''.join": '只保留没被标记的字符：`"{ret}"`',
    },
    max_steps=90,
    cards=dict(
        one_liner='栈存未匹配左括号的下标，配不上的括号统统删掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串含小写字母和 `(` `)`，删去最少的括号使其有效，返回任意一个合法结果',
                 '示例：`lee(t(c)o)de)` → `lee(t(c)o)de`',
                 '本视频：`l(e)e)t(c(` → `l(e)etc`，多余的 `)` 和 `(` 都要删'],
        quote='对于一个右括号 s[i]，我们需要找到 s[i] 左边最近未匹配的左括号，与之匹配。如果没有左括号，那么 s[i] 无法匹配，必须删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用栈记录未匹配的左括号下标；遇右括号：栈非空就弹出配对，栈空则标记删除',
              '遍历完后栈里剩下的左括号也没有右括号，全部标记删除',
              '先把待删位置改成空串，最后 `join` 即得答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：栈里存的是==下标==而不是字符，最后才知道删哪些',
                 '右括号多余在遍历中就能发现；左括号多余只有遍历完才知道',
                 '同类：1614、1963 等合法括号字符串（RBS）题'],
    ),
)
