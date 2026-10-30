def _txt(S):
    if 'now' not in S:
        return '先用栈求出每个括号的另一边括号位置 `match_pos`'
    d = S['d']
    return f"扫描方向 `d = {d}`（{'从前向后 →' if d == 1 else '← 从后向前'}），`res = {''.join(S.get('res', []))!r}`"


def _color(S, k, v):
    if 'now' in S and k == S['now'] and 0 <= S['now'] < len(S['s']):
        return 'blue'
    return None


CONFIG = dict(
    num=1190, title='反转每对括号间的子串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='一趟扫描 · 跳到匹配括号并调头',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def reverseParentheses(self, s):

        n = len(s)
        match_pos = [None] * n
        stack = []
        for index, char in enumerate(s):
            if char == '(':
                stack.append(index)
            elif char == ')':
                left_pos = stack.pop()
                match_pos[index] = left_pos
                match_pos[left_pos] = index
        
        now = 0
        d = 1
        res = []
        while now < n:
            if match_pos[now] is not None:
                d = -d
                now = match_pos[now] + d
            else:
                res.append(s[now])
                now += d
        
        return ''.join(res)
''',
    call='Solution().reverseParentheses("a(bc(d)e)")',
    expect='aedcb',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = now 扫描位置）', cell=76, pointers={'now': 'blue'}, color=_color, h=190),
        dict(type='array', var='match_pos', label='match_pos（括号 -> 另一边括号的位置，字母为 None）', cell=76, h=150),
        dict(type='stack', var='stack', label='stack（待配对的左括号）', fmt=lambda x: str(x), h=110),
    ],
    watch=[('now', 'now', 'blue'), ('d', 'd', 'yellow'), ('res', "''.join(res)", 'green')],
    captions={
        'n = len(s)': '第一步：求每个括号对应的另一边括号',
        'match_pos = [None]': '`match_pos[i]` 存括号 `i` 的另一边位置，字母留 `None`',
        'stack = []': '`stack` 用来括号匹配',
        'for index, char in enumerate(s)': lambda S, B, r: (f"扫描：`index = {S.index}`，`char = '{S.char}'`" if S.index != B.get('index') or 'index' not in B else '匹配完成'),
        8: lambda S, B, r: (f"`'{S.char}'` 是左括号，等它的右括号来配" if S.char == '(' else f"`'{S.char}'` 不是左括号"),
        'stack.append(index)': '左括号下标 `{index}` 入栈：`stack = {stack}`',
        10: lambda S, B, r: (f"`'{S.char}'` 是右括号，和栈顶的左括号成对" if S.char == ')' else f"`'{S.char}'` 是字母，跳过"),
        'left_pos = stack.pop()': '栈顶 `{left_pos}` 是右括号 `{index}` 的另一边',
        'match_pos[index] = left_pos': '`match_pos[{index}] = {left_pos}`',
        'match_pos[left_pos] = index': '`match_pos[{left_pos}] = {index}`：两个方向都记下',
        'now = 0': '第二步：一趟扫描模拟反转，`now` 是当前位置',
        'd = 1': '`d` 是方向：1 从前向后，-1 从后向前',
        'res = []': '`res` 按访问顺序收集字母',
        'while now < n': lambda S, B, r: (f'`now = {S.now}` 还在范围内，继续' if S.now < S.n else f'`now = {S.now}` 走出右端，结束'),
        'if match_pos[now] is not None': lambda S, B, r: (f"`s[{S.now}] = '{S.s[S.now]}'` 是括号，另一边在 `{S.match_pos[S.now]}`" if S.match_pos[S.now] is not None else f"`s[{S.now}] = '{S.s[S.now]}'` 是字母"),
        'd = -d': '遇到括号：==调转方向==，`d` 从 `{B.d}` 变成 `{d}`',
        'now = match_pos[now] + d': '跳到另一边括号再沿新方向走一步：`now` → =={now}==',
        'res.append(s[now])': "字母 `{s[now]}` 加入答案：`res = {res}`",
        'now += d': '沿当前方向走一步：`now` → {now}',
        "return ''.join": '拼接：`"{ret}"`',
    },
    max_steps=100,
    cards=dict(
        one_liner='遇到括号就跳到匹配括号，并调转扫描方向',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 含小写字母和括号，按括号内到外逐层反转每对括号间的子串',
                 '结果不应包含括号',
                 '示例：`(u(love)i)` → `iloveu`；本视频：`a(bc(d)e)` → `aedcb`'],
        quote='当反转开始时，我们直接通过括号匹配跳转到反转结束的位置，然后调转方向进行遍历，直到回到反转开始的地方位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用栈求出每个括号匹配的另一边位置',
              '一趟扫描：遇到括号，跳到另一边括号，`d = -d` 调头再走一步',
              '正向遇到的是奇数层，反向遇到的是偶数层，统一成「跳转 + 调头」两种情况'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '括号本身不进答案；跳转后沿新方向再走一步',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神同样预处理配对，但用 `links` 和 `step`；yiduobo 用 `match_pos` 和 `d`，并按五种情况归纳'],
    ),
)
