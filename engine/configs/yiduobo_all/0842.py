CONFIG = dict(
    num=842, title='将数组拆分成斐波那契序列', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举前两项 + 逐项验证',
    code='''
class Solution(object):
    def splitIntoFibonacci(self, S):

        n = len(S)
        for i in range(n - 2):
            if i > 0 and S[0] == '0':
                break
            a = int(S[:i + 1])
            if a > 2147483647:
                break
            for j in range(i + 1, n - 1):
                if j - i > 1 and S[i + 1] == '0':
                    break
                b = int(S[i + 1:j + 1])
                if b > 2147483647:
                    break
                pos = j + 1
                flag = True
                res = [a, b]
                while pos < n:
                    res.append(res[-1] + res[-2])
                    if res[-1] > 2147483647:
                        flag = False
                        break
                    l = len(str(res[-1]))
                    if pos + l - 1 >= n or int(S[pos : pos + l]) != res[-1]:
                        flag = False
                        break
                    pos = pos + l
                
                if flag:
                    return res
        
        return []
''',
    call='Solution().splitIntoFibonacci("1101111")',
    expect=[11, 0, 11, 11],
    skip=['if a > 2147483647', 'if b > 2147483647', 'if res[-1] > 2147483647', 'flag = True', 'res = [a, b]', 'flag = False', 'l = len', 'a = int', 'if i > 0 and'],
    max_steps=80,
    views=[
        dict(type='string', var='S', label='S（蓝 = a 的范围，粉 = b 的范围，黄 = 正在匹配的位置 pos）', cell=84, h=240,
             pointers={'pos': 'yellow'},
             color=lambda S, k, v: ('blue' if 'i' in S and 'j' in S and k <= S['i'] else
                                    'pink' if 'i' in S and 'j' in S and S['i'] < k <= S['j'] else None) if 'a' in S and 'b' in S else None,
             dim=lambda S, k, v: False),
        dict(type='text', size=28, h=70, fn=lambda S: (f"前两项 `a = {S['a']}`，`b = {S['b']}`　当前序列 ==`{S['res']}`==" if 'res' in S and 'b' in S
                                                       else (f"`a = {S['a']}`" if 'a' in S else ''))),
        dict(type='text', size=24, h=60, fn=lambda S: (f"下一项 `{S['res'][-1]}`（长 `{S['l']}`）对 `S[{S['pos']}:{S['pos'] + S['l']}] = {S['S'][S['pos']:S['pos'] + S['l']]}`" if 'l' in S and 'res' in S and S.get('pos', 99) < len(S['S']) else '')),
    ],
    watch=['i', 'j', 'a', 'b', ('pos', 'pos', 'yellow'), ('flag', 'flag', 'green')],
    captions={
        'n = len': '`n = {n}`：前两项之后至少还要有一项，所以 `i` 只到 `n - 3`',
        'for i in range(n - 2)': lambda S, B, r: ('`a` 的所有取法都试过了' if B.get('i') == S.i and 'n' in B else f'枚举第一项 `a` 的长度：取 `S[0:{S.i + 1}]`'),
        'if i > 0 and S[0]': lambda S, B, r: ('第一项长度大于 1 且以 `0` 开头 → 有前导零，==不合法==，不用再试更长的' if S.i > 0 and S.S[0] == '0' else '没有前导零问题'),
        'a = int': '`a = {a}`',
        'if a > 2147483647': '`a = {a}` 没超过 `2^31 - 1`' ,
        'for j in range': lambda S, B, r: ('`b` 的所有取法都试过了，换下一个 `a`' if B.get('j') == S.j and B.get('i') == S.i and 'j' in B else f'枚举第二项 `b` 的长度：取 `S[{S.i + 1}:{S.j + 1}]`'),
        'if j - i > 1 and': lambda S, B, r: ('第二项长度大于 1 且以 `0` 开头 → ==前导零==，更长的也不行，退出' if S.j - S.i > 1 and S.S[S.i + 1] == '0' else '第二项没有前导零问题'),
        'b = int': '`b = {b}`',
        'pos = j + 1': '`a = {a}`，`b = {b}`，序列 `[{a}, {b}]`：从 `pos = {pos}` 起匹配第三项',
        'if b > 2147483647': '`b = {b}` 没超过 `2^31 - 1`',
        'flag = True': '先假设这组前两项能拼出整个 `S`',
        'res = [a, b]': '序列从 `[{a}, {b}]` 开始',
        'while pos < n': lambda S, B, r: (f'`pos = {S.pos} < {S.n}`，`S` 还没匹配完，继续算下一项' if S.pos < S.n else f'`pos = {S.pos} = n`：==刚好匹配完整个 S=='),
        'res.append': '下一项 = 前两项之和：`{res[-2]} + {res[-3]} = {res[-1]}`',
        'if res[-1] > 2147483647': '这一项没超过 `2^31 - 1`',
        'l = len': '这一项写出来有 `{l}` 位，要和 `S` 从 `pos` 起的 `{l}` 位比较',
        'if pos + l - 1 >= n': lambda S, B, r: (f'`pos + l - 1 = {S.pos + S.l - 1} >= n`：`S` 剩下的不够长 → ==这组前两项失败==' if S.pos + S.l - 1 >= S.n
                                                 else (f'`S[{S.pos}:{S.pos + S.l}] = {S.S[S.pos:S.pos + S.l]}` ≠ `{S.res[-1]}` → ==对不上，失败==' if int(S.S[S.pos:S.pos + S.l]) != S.res[-1]
                                                       else f'`S[{S.pos}:{S.pos + S.l}] = {S.S[S.pos:S.pos + S.l]}` == `{S.res[-1]}` → 对上了')),
        'flag = False': '标记失败',
        'break': '放弃这组 `(a, b)`',
        'pos = pos + l': '`pos` 前进 `{l}` 位到 `{pos}`',
        'if flag': lambda S, B, r: ('`flag` 为真：整个 `S` 都被这个序列覆盖 → 找到答案' if S.flag else '`flag` 为假：这组前两项不行，换下一个 `b`'),
        'return res': '返回 `{ret}`',
        'return []': '没有任何一组前两项成功，返回 `[]`',
    },
    cards=dict(
        one_liner='S 很短：枚举前两项，后面的项全由递推决定，逐项验证',
        complexity='时间约 `O(n^3)`，空间 `O(n)`',
        problem=['把数字字符串 `S` 拆成若干整数，使其成为斐波那契式序列：每项等于前两项之和，至少 3 项',
                 '每个数不能有前导零（`0` 本身除外），且不超过 `2^31 - 1`',
                 '示例：`"1101111"` → `[11,0,11,11]`；无解返回 `[]`'],
        quote='需要特别注意的是，枚举的前两项值不能超过2^31 - 1，同时若长度超过1，那么必须满足最高位非0。另外，后续递推项的值也不能超过2^31 - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['前两项 `a`、`b` 一旦确定，整个序列就确定了：只需枚举它们的长度',
              '往后每算出一项，就看它的十进制写法是不是正好是 `S` 接下来的那一段',
              '前导零、超过 `2^31 - 1`、`S` 不够长，都是立刻放弃的情形'],
        summary=['枚举两个长度，每次验证 `O(n)`，总 `O(n^3)`，`n` 很小可行',
                 '易错：前导零要同时检查第一项和第二项；`0` 单独一位是合法的',
                 '递推项也要判断是否超过 `2^31 - 1`，并在 `S` 剩余长度不够时提前失败',
                 '原文已是 Python 3 可运行写法，代码无需改动'],
    ),
)
