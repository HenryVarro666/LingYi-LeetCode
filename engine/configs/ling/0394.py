def _level(S):
    """当前在第几层 decode（只用于画图）：已读部分中未闭合的 '[' 个数 + 1；刚读到 ']' 时本层还没返回"""
    s, i = S.get('s'), S.get('i')
    if s is None or i is None:
        return 0
    d = 1 + (S.get('c') == ']')
    for ch in s[:i]:
        d += (ch == '[') - (ch == ']')
    return d


def _ret_cap(S, B, ret):
    if B.get('c') == ']':
        return f'这一层遇到 `]` → ==归==：返回本层的 `res = {ret!r}` 给上一层'
    return f'字符串读完，最外层返回 =={ret!r}=='


CONFIG = dict(
    num=394, title='字符串解码', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='递归（外部下标 i）',
    code='''
class Solution:
    def decodeString(self, s: str) -> str:
        i = 0

        def decode() -> str:
            nonlocal i
            res = ''  # 或者 res = []，具体见另一份代码【Python3 列表】
            k = 0
            while i < len(s):
                c = s[i]
                i += 1
                if c.isalpha():
                    res += c
                elif c.isdigit():
                    k = k * 10 + int(c)
                elif c == '[':  # 递
                    res += decode() * k  # 把括号内的字符串重复 k 次
                    k = 0  # 重置 k，若不重置，2[a]3[b] 后面的 3 会算出 k = 23
                else:  # ']' 归
                    break
            return res

        return decode()
''',
    call='Solution().decodeString("3[a2[c]]")',
    expect='accaccacc',
    skip=['i += 1'],
    views=[
        dict(type='string', var='s', label='s（灰色 = 已读，箭头 i = 下一个要读的字符）', h=190, cell=96,
             pointers={'i': 'blue'}, dim=lambda S, i, v: S.get('i') is not None and i < S['i']),
        dict(type='calls', label='调用栈：每遇到 [ 就多一层 decode()', h=190),
        dict(type='text', fn=lambda S: (f"当前在第 =={_level(S)}== 层 decode：`res = {S['res']!r}`　`k = {S['k']}`"
                                        if 'res' in S and 'k' in S else ''), size=28),
        dict(type='text', fn=lambda S: '遇到 `[` → ==递==：进入新一层；遇到 `]` → ==归==：返回本层 `res`', size=26),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c'), ('k', 'k', 'purple'), ('res', 'res', 'green')],
    captions={
        'i = 0': '下标 `i` 放在递归函数外面：==所有层共用==，读到哪里都记得',
        'res = \'\'': '新的一层开始：本层结果 `res = \'\'`',
        8: '本层的重复次数 `k = 0`',
        18: lambda S, B, ret: (f'下层返回后 `res += 下层结果 × {B.k}` → `res = {S.res!r}`；'
                               f'`k` 用完==重置为 0==，否则 `2[a]3[b]` 会算出 23'),
        'while i < len(s)': lambda S, B, ret: (f'`i = {B.i} < {len(S.s)}` → 还有字符没读' if B.i < len(S.s)
                                              else f'`i = {B.i}` 已到末尾 → 循环结束'),
        'c = s[i]': '读字符 `c = s[{B.i}] = {c!r}`，然后 `i += 1`',
        'if c.isalpha()': lambda S, B, ret: (f'`{S.c}` 是字母' if S.c.isalpha() else f'`{S.c}` 不是字母'),
        'res += c': '字母直接接到本层结果后面：`res = {res!r}`',
        'elif c.isdigit()': lambda S, B, ret: (f'`{S.c}` 是数字' if S.c.isdigit() else f'`{S.c}` 不是数字'),
        'k = k * 10': '`k = {B.k} × 10 + {c} = {k}`（多位数也能拼出来）',
        "elif c == '['": lambda S, B, ret: ('`[` → ==递==：括号里的内容交给下一层 `decode()` 去解码' if S.c == '['
                                            else f'`{S.c}` 不是 `[`，那就是 `]`'),
        'res += decode()': '`[` 后面的内容交给==新一层== `decode()`，等它返回再重复 `k = {k}` 次',
        'break': '`]` → ==归==：本层到此结束，跳出循环',
        'return res': _ret_cap,
        'return decode()': '调用 `decode()`：从第 1 层开始解码整个 `s`',
    },
    cards=dict(
        one_liner='遇到 [ 往下递，遇到 ] 往上归，外部变量 i 记录读到哪',
        complexity='时间、空间都是 `O(U^m)`，即输出串长度',
        problem=['编码规则 `k[encoded_string]`：方括号内的字符串重复 `k` 次，可以嵌套',
                 '示例：`"3[a]2[bc]"` → `"aaabcbc"`',
                 '示例：`"3[a2[c]]"` → `"accaccacc"`'],
        quote='把 s 视作若干基础字符串和 `k[encoded_string]` 的并……s₃=`[`，==往下递归==……s₆=`]`，==递归返回== cd。上层递归函数接收到 cd，将其重复 k=2 次。',
        quote_src='—— 灵茶山艾府题解（第二种递归写法）',
        idea=['从左到右读：字母 → 接到 `res`；数字 → `k = k·10 + int(c)`',
              '`[` → 递归解码括号里的内容，返回值重复 `k` 次接到 `res`；`]` → 本层结束',
              '用递归函数外的变量 `i` 表示当前下标，所有层共享'],
        result='`"3[a2[c]]"` 解码为 `"accaccacc"` ✓',
        after=[dict(heading='用栈模拟递归', lines=[
            '把这种递归改写成非递归：在“递”的时候把局部变量存进栈',
            '遇到 `[`：`stack.append((res, k))`，再把 `res, k` 重置',
            '遇到 `]`：弹出 `(res, k)` 恢复现场，再 `res += sub_res * k`',
            '计算机的递归本质上就是在用栈保存每一层的局部变量'])],
        summary=['复杂度 `O(U^m)`：生成的串有多长就要多少时间',
                 '易错：用完 `k` 要==重置为 0==，否则 `2[a]3[b]` 算出 `k = 23`',
                 '易错：`k` 可能是多位数，用 `k = k * 10 + int(c)` 累积',
                 '另一种递归：找到匹配的 `]` 把 s 切三段，`a * k + b`'],
    ),
)
