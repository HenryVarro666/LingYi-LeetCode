def _can(S, loop):
    sym, v = S.symbol, S.v
    ok = sym == '!' or (v and sym == '|') or (not v and sym == '&')
    why = '非运算，拿到值就能取反' if sym == '!' else ('与遇到 f，必假' if sym == '&' else '或遇到 t，必真')
    if loop and not S.stack:
        return f'栈空：没有外层可回，`v = {v}` 先不循环'
    if ok:
        return f'==能立刻定结果==：`v = {v}`，运算符 `{sym}`（{why}）→ 剩下的内容可以跳过'
    return f'`v = {v}`，运算符 `{sym}`：还不能定结果 → 继续扫描'


def _stk(S):
    st = S.get('stack')
    if st is None:
        return ''
    sym = S.get('symbol')
    v = S.get('v')
    return f"当前运算符 `{sym}`　外层待处理运算符栈 `{st}`　最近一个值 `v = {v}`"


CONFIG = dict(
    num=1106, title='解析布尔表达式', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='一趟扫描 · 运算符栈 · 短路跳过',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def parseBoolExpr(self, expression):

        n = len(expression)
        p = 0
        v = None
        symbol = None
        stack = []
        while p < n:
            if expression[p] in ['!', '|', '&']:
                if symbol is not None:
                    stack.append(symbol)
                symbol = expression[p]
                p += 2
            elif expression[p] in ['t', 'f']:
                if expression[p] == 't':
                    v = True
                else:
                    v = False
                p += 1
                while stack and (symbol == '!' or (v and symbol == '|') or (not v and symbol == '&')):
                    if symbol == '!':
                        v = not v
                    cnt = 1
                    while cnt > 0:
                        if expression[p] == '(':
                            cnt += 1
                        elif expression[p] == ')':
                            cnt -= 1
                        p += 1

                    symbol = stack[-1]
                    stack.pop()
                
                if symbol == '!' or (v and symbol == '|') or (not v and symbol == '&'):
                    if symbol == '!':
                        return not v
                    else:
                        return v

            elif expression[p] == ')':
                p += 1
                if symbol == '|':
                    v = False
                else:
                    v = True
                if stack:
                    symbol = stack[-1]
                    stack.pop()
                else:
                    return v
                
                while stack and (symbol == '!' or (v and symbol == '|') or (not v and symbol == '&')):
                    if symbol == '!':
                        v = not v
                    cnt = 1
                    while cnt > 0:
                        if expression[p] == '(':
                            cnt += 1
                        elif expression[p] == ')':
                            cnt -= 1
                        p += 1
                    symbol = stack[-1]
                    stack.pop()
                
                if symbol == '!' or (v and symbol == '|') or (not v and symbol == '&'):
                    if symbol == '!':
                        return not v
                    else:
                        return v

            else:
                p += 1
''',
    call='Solution().parseBoolExpr("!(&(t,|(f,f)))")',
    expect=True,
    views=[
        dict(type='string', var='expression', label='expression（蓝箭头 = 扫描位置 p）', pointers={'p': 'blue'}, cell=60, h=170,
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='stack', var='stack', label='stack（被嵌套压住的外层运算符，栈顶在右）', fmt=lambda x: f"'{x}'", h=130, font=32),
        dict(type='text', fn=_stk, size=26, h=80),
    ],
    skip=[26, 58, 11, 16],
    max_steps=90,
    watch=[('p', 'p', 'blue'), ('symbol', 'symbol', 'pink'), ('v', 'v', 'green'), ('cnt', 'cnt', 'yellow')],
    captions={
        7: '`symbol` 记录当前正在算的运算符；`stack` 保存被嵌套压住的外层运算符',
        10: lambda S, B, r: (f"`expression[{S.p}] = '{S.expression[S.p]}'` 是运算符 → 进入运算" if S.expression[S.p] in '!|&'
                             else f"`expression[{S.p}] = '{S.expression[S.p]}'` 不是运算符 → 看下一种情况"),
        12: '`symbol` 不为空 → ==嵌套==：先把外层运算符 `{stack[-1]}` 压栈保存',
        13: '当前运算符变成 `{symbol}`',
        14: '运算符后一定跟 `(`，所以==一次跳两格==：`p` → {p}',
        15: lambda S, B, r: (f"`expression[{S.p}] = '{S.expression[S.p]}'` 是布尔值 → 先取出它的值" if S.expression[S.p] in 'tf'
                             else f"`'{S.expression[S.p]}'` 不是 t/f → 看下一种情况"),
        17: '`t` → `v = True`',
        19: '`f` → `v = False`',
        20: '`p` → {p}',
        21: lambda S, B, r: _can(S, True),
        23: '非运算：`v` 取反 → =={v}==',
        24: '用括号匹配跳过后面的内容：`cnt` 记未闭合的 `(`',
        25: lambda S, B, r: f'`cnt = {S.cnt}`，还没到匹配的 `)` → 继续跳' if S.cnt > 0 else '`cnt = 0`：这个运算符的括号跳完了',
        26: '`expression[{p}] = {expression[p]!r}`：遇到 `(` 就 `cnt` +1',
        28: '`expression[{p}] = {expression[p]!r}`：遇到 `)` 就 `cnt` -1',
        30: '`p` → {p}',
        32: '子表达式有结果了 → 回到外层运算符 `{symbol}`',
        33: '外层运算符出栈，`stack = {stack}`',
        35: lambda S, B, r: _can(S, False),
        37: '最外层是非运算：返回 `not v` = =={not v}==',
        39: '整个表达式的值：=={v}==',
        41: lambda S, B, r: (f"`expression[{S.p}] = ')'` → 这一组括号==自然结束==，没被短路" if S.expression[S.p] == ')' else f"`expression[{S.p}] = '{S.expression[S.p]}'` 也不是 `)` → 走最后的 else：当逗号跳过"),
        42: '`p` → {p}',
        43: '没提前出结果就走到 `)`：`|` 说明里面全是 f',
        44: '`|` 全是 f → `v = False`',
        46: '`&`、`!` 走到这里说明里面全是 t → `v = True`',
        47: lambda S, B, r: '栈不空：还有外层运算符等着这个值' if S.stack else '栈空：最外层结束了',
        48: '回到外层运算符 `{symbol}`',
        49: '外层运算符出栈，`stack = {stack}`',
        51: '栈空：返回 `v` = =={v}==',
        53: lambda S, B, r: _can(S, True),
        55: '非运算：`v` 取反 → =={v}==',
        56: '括号匹配跳过：`cnt = 1`',
        57: lambda S, B, r: f'`cnt = {S.cnt}`，继续跳' if S.cnt > 0 else '`cnt = 0`：括号跳完了',
        58: '`expression[{p}] = {expression[p]!r}`：遇到 `(` 就 `cnt` +1',
        60: '`expression[{p}] = {expression[p]!r}`：遇到 `)` 就 `cnt` -1',
        62: '`p` → {p}',
        63: '回到外层运算符 `{symbol}`',
        64: '外层运算符出栈，`stack = {stack}`',
        66: lambda S, B, r: _can(S, False),
        68: '最外层是非运算：返回 `not v` = =={not v}==',
        70: '整个表达式的值：=={v}==',
        73: lambda S, B, r: f"`'{B.expression[B.p]}'` 是逗号 → 直接跳过，`p` → {S.p}",
    },
    cards=dict(
        one_liner='不存中间结果：能立刻定结果就用括号匹配跳过后面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['表达式由 `t f ! & | ( ) ,` 组成：`!(e)` 取反，`&(e1,e2,...)` 全真才真，`|(e1,e2,...)` 有真就真',
                 '求整个表达式的布尔值',
                 '本视频：`"!(&(t,|(f,f)))"` → `True`'],
        quote='若当前的运算符和v可以立即得出运算结果，那么我们就将v置为运算结果并依据括号匹配跳过后续不需要解析的部分',
        quote_src='—— yiduobo 题解原文',
        idea=['与：遇到 `f` 必假；或：遇到 `t` 必真；非：拿到值就取反 —— 都能==立刻定结果==',
              '定了结果就用 `cnt` 做括号匹配，跳到这个运算符的 `)` 之后',
              '嵌套时把外层运算符压栈，子表达式出结果后再弹出来继续判断'],
        summary=['时间 `O(n)`，空间 `O(n)`：栈深 = 嵌套层数',
                 '运算符后固定跟 `(`，所以 `p += 2` 一次跳过两格',
                 '自然走到 `)` 时：`|` 说明全是 f，`&`、`!` 说明全是 t',
                 '对比灵神：灵神用一个栈直接存所有字符，遇 `)` 时回头算；这里不存值，靠短路跳过'],
    ),
)
