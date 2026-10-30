_STR = lambda S: S.get('s') or S.get('S')
_RES = lambda S: [''.join(x) for x in S.get('self.res', [])]


def _lo(S, B, r):
    c = S.s[S.depth]
    if ord(c) >= 97:
        return f'`ord({c!r}) = {ord(c)} >= 97`：小写字母 → 再试大写 `{c.upper()}`'
    return f'`ord({c!r}) = {ord(c)} < 97`：不是小写字母，继续看是不是大写'


def _up(S, B, r):
    c = S.s[S.depth]
    if ord(c) >= 65:
        return f'`ord({c!r}) = {ord(c)} >= 65`：大写字母 → 再试小写 `{c.lower()}`'
    return f'`{c!r}` 的编码 `{ord(c)}` < 65：是数字，==没有大小写==，只有“原样”这一种'


CONFIG = dict(
    num=784, title='字母大小写全排列', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 回溯 · 字母分两叉、数字一叉',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def letterCasePermutation(self, S):

        self.res = []

        l = len(S)
        self.dfs(S, 0, [], l)
        return [''.join(x) for x in self.res]

    def dfs(self, s, depth, now, l):
        if depth == l:
            self.res.append(now[:])
            return

        now.append(s[depth])
        self.dfs(s, depth + 1, now, l)
        if ord(s[depth]) >= 97:
            now[-1] = chr(ord(s[depth]) - 32)
            self.dfs(s, depth + 1, now, l)
        elif ord(s[depth]) >= 65:
            now[-1] = chr(ord(s[depth]) + 32)
            self.dfs(s, depth + 1, now, l)
        now.pop()
''',
    call="Solution().letterCasePermutation('a1b')",
    expect=['a1b', 'a1B', 'A1b', 'A1B'],
    views=[
        dict(type='string', var=_STR, label='s（蓝 = 当前要处理的字符）', cell=84, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('depth') else None),
        dict(type='array', var='now', label='now（正在拼的字符串）', cell=84, h=150, color=lambda S, i, v: 'green' if i == len(S['now']) - 1 else None),
        dict(type='calls', h=210, hide=('letterCasePermutation',)),
        dict(type='stack', var=_RES, label='self.res（已收集的结果）', fmt=lambda x: x, h=130),
    ],
    watch=[('depth', lambda S: S['_inner'].get('depth'), 'blue'), ('now', lambda S: ''.join(S['_inner'].get('now', [])), 'green')],
    skip=['l = len', 'self.res = []'],
    captions={
        'if depth == l': lambda S, B, r: (f'`depth = {S.depth} == l = {S.l}`：每一位都定下来了 → ==收集一个结果==' if S.depth == S.l
                                          else f'`depth = {S.depth} < l = {S.l}`：还要处理第 {S.depth} 个字符 `{S.s[S.depth]}`'),
        'self.res.append': lambda S, B, r: f'`now[:]` ==复制一份==存进 `res`：`{"".join(S.now)}`（不复制的话后面 `now` 变了结果也会变）',
        'now.append(s[depth])': '先==原样放入==当前字符 `{s[depth]}`',
        13: '这一支到底了，返回上一层继续',
        16: '递归：沿着==“原样”==这一支处理下一位',
        19: '递归：沿着==“换成大写”==这一支处理下一位',
        22: '递归：沿着==“换成小写”==这一支处理下一位',
        'self.dfs(S, 0, [], l)': '从第 `0` 位开始 dfs，`now = []` 是正在拼的字符列表',
        'if ord(s[depth]) >= 97': _lo,
        'elif ord(s[depth]) >= 65': _up,
        'now[-1] = chr(ord(s[depth]) - 32)': '把刚放进去的字符换成大写：`now[-1] = {now[-1]}`（`ord - 32`）',
        'now[-1] = chr(ord(s[depth]) + 32)': '把刚放进去的字符换成小写：`now[-1] = {now[-1]}`（`ord + 32`）',
        'now.pop()': lambda S, B, r: f'两种情况都走完了，==回溯==：弹出 `{B.now[-1]}`，回到上一位',
        "return [''.join": '把每个字符列表拼成字符串，共 `{len(self.res)}` 个结果',
    },
    max_steps=75,
    cards=dict(
        one_liner='从左往右逐位 DFS：字母分“原样 / 换大小写”两叉，数字只有一叉',
        complexity='时间 `O(2^k · n)`（k 为字母个数），空间 `O(n)`',
        problem=['给字符串 `S`，把其中的字母逐个变成大写或小写，得到所有可能的字符串',
                 '数字保持不变，结果顺序任意',
                 '示例：`"a1b2"` → `["a1b2","a1B2","A1b2","A1B2"]`',
                 '本视频：`"a1b"` → 4 个结果'],
        quote='dfs的过程比较简单，就是从头开始往后逐位进行，首先对当前字符执行一次，然后若当前字符为小写字符，则需要对当前字符的大写版本执行一次；若当前字符为大写字符，则需要对当前字符的小写版本执行一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `depth` 位先==原样==放入 `now`，递归下一位',
              '回来后如果是字母，把这一位==换成另一种大小写==，再递归一次',
              '两条分支都走完，`now.pop()` 回溯；`depth == l` 时收集 `now` 的拷贝'],
        result='4 个结果全部收集 ✓',
        summary=['时间 `O(2^k · n)`：k 个字母共 `2^k` 个结果，每个拼接要 `O(n)`；空间 `O(n)` 递归深度',
                 '易错：收集时要写 `now[:]` 拷贝，否则后续 `pop` 会改掉已存的结果',
                 '用 ASCII 码判断：`>= 97` 小写，`>= 65` 大写（数字 `< 65`）；大小写差 32',
                 '原文是 Python 2 风格，在 Python 3 下无需改动即可运行',
                 '原文提到也可以用 Python 的生成方法，这里选传统 DFS + 回溯'],
    ),
)
