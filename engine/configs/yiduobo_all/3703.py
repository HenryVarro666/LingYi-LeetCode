def _fmt(v):
    return f'( × {v}' if v > 0 else f') × {-v}'


def _top(S):
    st = S.get('stack')
    if st is None:
        return ''
    cur = ''.join('(' * v if v > 0 else ')' * -v for v in st)
    return f"栈里的内容还原：`{cur or '（空）'}`（左括号记正数，右括号记负数）"


CONFIG = dict(
    num=3703, title='移除K-平衡子字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈（正负数记括号段）+ 批量消除',
    tags=['栈', '邻项消除', '难度分 1802'],
    code='''
class Solution(object):
    def removeSubstring(self, s, k):

        stack = []
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[q] == s[p]:
                q += 1
                
            cnt = q - p

            if s[p] == '(':
                if stack and stack[-1] > 0:
                    stack[-1] += cnt
                else:
                    stack.append(cnt)
            
            else:
                if stack and stack[-1] < 0:
                    stack[-1] -= cnt
                else:
                    stack.append(-cnt)
                
                while len(stack) >= 2 and stack[-1] <= -k and stack[-2] >= k:
                    right = -stack.pop()
                    left = stack.pop()
                    t = min(left, right) // k
                    right -= t * k
                    left -= t * k
                    if right == 0:
                        if left == 0:
                            pass
                        else:
                            stack.append(left)
                    elif left == 0:
                        if stack:
                            stack[-1] -= right
                        else:
                            stack.append(-right)
                    else:
                        stack.append(left)
                        stack.append(-right)
        
            p = q

        res = []
        for v in stack:
            if v > 0:
                res.append('(' * v)
            else:
                res.append(')' * -v)
        
        return ''.join(res)
''',
    call='Solution().removeSubstring("((()))(()", 2)',
    expect='()(()',
    views=[
        dict(type='string', var='s', label='s（蓝框 = 当前这一段相同的括号 [p, q)）', window=('p', 'q - 1'), cell=84, h=190,
             pointers={'p': 'blue'},
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='stack', var='stack', label='stack（左括号个数记正数，右括号个数记负数）', fmt=_fmt, h=130, font=30),
        dict(type='text', fn=_top, size=28, h=70),
    ],
    max_steps=80,
    watch=[('k', 'k', 'yellow'), ('p', 'p', 'blue'), ('cnt', 'cnt', 'cyan'), ('stack', 'stack', 'green')],
    captions={
        'stack = []': '栈里存括号段的个数：==左括号记正数，右括号记负数==',
        'p = 0': '`p` 是当前括号段的起点',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p}`，还有括号没处理' if S.p < len(S.s) else '`p` 走到结尾，s 处理完了'),
        'q = p + 1': '从 `p` 往右找这一段相同括号的终点，先令 `q = {q}`',
        'while q < len(s) and': lambda S, B, r: (f'`s[{S.q}] = {S.s[S.q]}` 和 `s[{S.p}]` 相同 → 这一段还能延长' if S.q < len(S.s) and S.s[S.q] == S.s[S.p]
                                                  else '到头了，或下一个括号不同 → 这一段结束'),
        'q += 1': '`q` → {q}',
        'cnt = q - p': '这一段有 `{cnt}` 个 `{s[p]}`',
        "if s[p] == '('": lambda S, B, r: ('是一段左括号' if S.s[S.p] == '(' else '是一段右括号：入栈后要检查能否消除'),
        'if stack and stack[-1] > 0': lambda S, B, r: ('栈顶也是左括号 → 个数累加' if S.stack and S.stack[-1] > 0 else '栈空或栈顶是右括号 → 新开一段'),
        'stack[-1] += cnt': '累加：栈顶变成 `{stack[-1]}`',
        'stack.append(cnt)': '新的一段入栈：`+{cnt}`',
        'if stack and stack[-1] < 0': lambda S, B, r: ('栈顶也是右括号 → 个数累加（用减）' if S.stack and S.stack[-1] < 0 else '栈空或栈顶是左括号 → 新开一段'),
        'stack[-1] -= cnt': '累加：栈顶变成 `{stack[-1]}`',
        'stack.append(-cnt)': '右括号段入栈：`{-cnt}`',
        'while len(stack) >= 2': lambda S, B, r: (
            f'栈顶 `{S.stack[-1]}` ≤ −k = `{-S.k}`，下面 `{S.stack[-2]}` ≥ k = `{S.k}` → ==能消除=='
            if len(S.stack) >= 2 and S.stack[-1] <= -S.k and S.stack[-2] >= S.k
            else ('栈里不到两段，不能消除' if len(S.stack) < 2 else '右括号不到 k 个，或左括号不到 k 个 → 停止消除')),
        'right = -stack.pop()': '弹出栈顶右括号段：`right = {right}`',
        'left = stack.pop()': '弹出下面的左括号段：`left = {left}`',
        't = min(left, right) // k': '能消 `min({left}, {right}) // {k}` = =={t}== 组 k-平衡子串',
        'right -= t * k': '右括号还剩 `{right}`',
        'left -= t * k': '左括号还剩 `{left}`',
        'if right == 0': lambda S, B, r: ('右括号用完了' if S.right == 0 else '右括号有剩余'),
        'pass': '两边都用光了，什么也不放回',
        'stack.append(left)': lambda S, B, r: f'剩余的左括号 `{S.left}` 个放回栈：`{S.stack}`',
        'elif left == 0': lambda S, B, r: ('左括号用光、右括号有剩余：把右括号放回' if S.left == 0 else '两边都有剩余：左右括号都放回栈'),
        'if left == 0': lambda S, B, r: ('左括号也用完了：无需放回' if S.left == 0 else '左括号有剩余：放回栈'),
        'if stack:': lambda S, B, r: ('栈非空：栈顶就是右括号段吗？合并进去' if S.stack else '栈空：直接放回右括号'),
        'stack[-1] -= right': '剩余右括号合并到栈顶：`{stack[-1]}`',
        'stack.append(-right)': lambda S, B, r: f'剩余的右括号 `{-S.stack[-1]}` 个放回栈：`{S.stack}`',
        'p = q': '处理完这一段，`p` 跳到 `{q}`',
        'res = []': '循环结束，把栈里每段还原成括号',
        "res.append('(' * v)": '`{v}` 个左括号',
        "res.append(')' * -v)": '`{-v}` 个右括号',
        "return ''.join": '拼起来：`{ret}`',
    },
    cards=dict(
        one_liner='先把连续括号按段压缩，再按段批量消除',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 只含 `(` 和 `)`；`k` 个 `(` 后跟 `k` 个 `)` 叫 k-平衡',
                 '重复删除所有 k-平衡子串，返回最终字符串',
                 '本视频：`"((()))(()"`，`k = 2` → `"()(()"`'],
        quote='可以改为记录括号的数量。为了区分左右括号，在这里可以将左括号的数量作为正数记录在栈中，相对的，右括号则作为负数记录在栈中。',
        quote_src='—— yiduobo 题解原文',
        idea=['它像括号匹配，只是 `k` 个一组：栈里存括号段的个数，左正右负',
              '一趟遍历，先切出一段相同括号 `[p, q)`，同号就合并，异号就新入栈',
              '右括号段入栈后，栈顶 `≤ -k` 且下面 `≥ k` 就批量消除 `min(left, right) // k` 组，剩余按四种情况放回'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：消除后剩下的右括号要和新栈顶（若是右括号）合并，否则会漏掉新的消除',
                 '易错：消除是 `while`，合并后可能又凑出新的 k-平衡',
                 '原文已是 Python 3 可运行，整数除法原文就写的 `//`，未做修改',
                 '对比灵神：灵神逐个字符入栈、栈里存 `[字符, 个数]`；yiduobo 一次切一整段并批量消除'],
    ),
)
