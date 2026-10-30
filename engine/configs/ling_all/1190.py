def _txt(S):
    if 'step' not in S:
        return '先预处理：用栈给每个括号找到另一半的下标，存进 `links`'
    d = '向右 →' if S['step'] == 1 else '← 向左'
    return f"当前方向 `step = {S['step']}`（{d}）；已收集 `ans = {''.join(S.get('ans', []))!r}`"


def _color(S, k, v):
    if S.get('i') is None:
        return None
    if k == S['i'] and ('ch' in S):
        return 'blue'
    return None


def _lcolor(S, k, v):
    if 'step' in S and 'ch' in S and S.get('ch') in '()' and k == S.get('i'):
        return 'blue'
    return None


CONFIG = dict(
    num=1190, title='反转每对括号间的子串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='预处理括号配对 · 左右横跳',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def reverseParentheses(self, s: str) -> str:
        n = len(s)
        links = [0] * n
        st = []
        for i, ch in enumerate(s):
            if ch == '(':
                st.append(i)
            elif ch == ')':
                # 右括号与栈顶左括号配对，下标建立双向链接
                j = st.pop()
                links[i] = j
                links[j] = i

        ans = []
        step = 1
        i = 0
        while i < n:
            ch = s[i]
            if ch == '(' or ch == ')':
                i = links[i]  # 跳到对应的括号位置
                step = -step  # 反向移动
            else:
                ans.append(ch)
            i += step
        return ''.join(ans)
''',
    call='Solution().reverseParentheses("(u(love)i)")',
    expect='iloveu',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前下标 i）', cell=70, pointers={'i': 'blue'}, color=_color, h=190),
        dict(type='array', var='links', label='links（括号 -> 另一半的下标）', cell=70, h=150),
        dict(type='stack', var='st', label='st（待配对的左括号下标）', fmt=lambda x: str(x), h=120),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'pink'), ('step', 'step', 'yellow'), ('ans', "''.join(ans)", 'green')],
    captions={
        'n = len(s)': '先预处理：给每个括号找到配对的另一半',
        'links = [0]': '`links[i]` 用来存下标 `i` 的括号所对应的另一半括号的下标',
        'st = []': '`st` 栈：放还没配对的左括号下标',
        'for i, ch in enumerate(s)': lambda S, B, r: (f"预处理第一遍：`i = {S.i}`，`ch = '{S.ch}'`" if S.i != B.get('i') or 'i' not in B else '预处理完成'),
        7: lambda S, B, r: (f"`'{S.ch}'` 是左括号，下标入栈" if S.ch == '(' else f"`'{S.ch}'` 不是左括号"),
        'st.append(i)': '左括号下标 `{i}` 入栈：`st = {st}`',
        "elif ch == ')'": lambda S, B, r: (f"`'{S.ch}'` 是右括号，和栈顶左括号配对" if S.ch == ')' else f"`'{S.ch}'` 是字母，不用处理"),
        'j = st.pop()': '栈顶 `{j}` 就是 `{i}` 配对的左括号',
        'links[i] = j': '`links[{i}] = {j}`：右括号记下左括号的位置',
        'links[j] = i': '`links[{j}] = {i}`：左括号也记下右括号的位置（双向链接）',
        'ans = []': '开始真正遍历：`ans` 收集字母',
        'step = 1': '`step = 1` 表示向右走，遇到括号就会取反',
        'i = 0': '从下标 `0` 开始',
        'while i < n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`，继续' if S.i < S.n else f'`i = {S.i} == n`：走出右端，结束'),
        'ch = s[i]': "当前字符 `ch = '{ch}'`",
        "if ch == '(' or": lambda S, B, r: (f"`'{S.ch}'` 是括号 → 要跳到另一半，并掉头" if S.ch in '()' else f"`'{S.ch}'` 是字母 → 直接收集"),
        'i = links[i]': '跳到配对括号：`i` = `links[{B.i}]` = =={i}==',
        'step = -step': '掉头：`step` 从 `{B.step}` 变成 =={step}==（反着走就不用真的反转）',
        'ans.append(ch)': "收集字母：`ans = {ans}`",
        'i += step': '按当前方向走一步：`i` → {i}',
        "return ''.join": '`ans` 拼起来：`"{ret}"`',
    },
    max_steps=110,
    cards=dict(
        one_liner='遇到括号就跳到另一半并掉头，不用真的反转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 含小写字母和成对括号，从内到外逐层反转每对括号里的子串',
                 '结果里不能有括号',
                 '示例：`(u(love)i)` → `iloveu`'],
        quote='当我们遇到左括号时，直接跳到右括号的左侧，倒着遍历，就不需要反转了。倒着遍历，再次遇到左括号时，跳到右括号的右侧，继续向右遍历。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用栈预处理：每对括号建立双向链接 `links[i] = j, links[j] = i`',
              '遍历时遇到括号：跳到另一半，`step` 取反——反着走就是反转',
              '再次遇到同一对括号，负负得正，跳到括号外继续向右'],
        summary=['时间 `O(n)`，空间 `O(n)`，每个字母只访问一次',
                 '题解还给了方法一：递归，遇右括号反转 `res`，最坏 `O(n^2)`',
                 '易错：括号本身不加入答案；跳转后还要执行 `i += step`',
                 '同类：394 字符串解码、合法括号字符串（RBS）题'],
    ),
)
