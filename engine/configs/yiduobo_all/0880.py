def _top(S):
    if 'l' not in S:
        return ''
    l, K = S['l'], S['K']
    if 'last_pos' in S and S['_line'] >= 13 or S.get('_line', 0) >= 13:
        return f'倒推：当前整段长度 `l = {l}`，要找第 `K = {K}` 个字符'
    return f'正推：解码后长度 `l = {l}`，目标 `K = {K}`' + ('（已经 ≥ K，停）' if l >= K else '')


def _cur(S):
    return S.get('index')


CONFIG = dict(
    num=880, title='索引处的解码字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='先算长度 · 倒着还原',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def decodeAtIndex(self, S, K):

        l = 0
        last_pos = 0
        for index, char in enumerate(S):
            if char >= 'a' and char <= 'z':
                l += 1
            else:
                l *= int(char)
            if l >= K:
                last_pos = index
                break

        for index in range(last_pos, -1, -1):
            char = S[index]
            if char >= 'a' and char <= 'z':
                if l == K:
                    return char
                l -= 1
            else:
                l //= int(char)
                K %= l
                if K == 0:
                    K = l
''',
    call='Solution().decodeAtIndex("leet2code3", 15)',
    expect='e',
    views=[
        dict(type='text', fn=_top, size=28, h=60),
        dict(type='string', var='S', label='S（蓝 = 当前字符，黄 = 正推停下的位置）', cell=84, h=200,
             pointers={'index': 'blue', 'last_pos': 'orange'},
             color=lambda S, i, v: ('orange' if S.get('_line', 0) < 13 and S.get('l', 0) >= S.get('K', 1 << 60) and i == S.get('index') else None)),
        dict(type='text', fn=lambda S: f"解码后的串（前 {S['l']} 个字符里的第 `{S['K']}` 个就是答案）" if 'l' in S and 'K' in S else '', size=24, h=60),
        dict(type='text', fn=lambda S: '`leet2code3` 解码：`leetleetcode` 重复 3 遍，共 36 个字符，第 15 个是 `e`', size=24, h=60),
    ],
    watch=[('l', 'l', 'cyan'), ('K', 'K', 'yellow'), ('last_pos', 'last_pos', 'orange'), ('index', 'index', 'blue'), ('char', 'char')],
    skip=['char = S[index]', "if char >= 'a'", 'break'],
    captions={
        'l = 0': '`l` 记录解码后字符串的==长度==（不真的展开，K 可能很大）',
        'last_pos = 0': '`last_pos` 记录长度第一次 ≥ K 的位置',
        'for index, char in enumerate': '正推：下标 `{index}`，字符 `{char}`',
        "if char >= 'a'": lambda S, B, r: (f"`{S.char}` 是小写字母" if 'a' <= S.char <= 'z' else f"`{S.char}` 是数字"),
        'l += 1': '字母只多写 1 个字符：`l` → `{l}`',
        'l *= int': '数字 `{char}`：整段复制成 `{char}` 份（原来 1 份 + 再复制 `{char} - 1` 次）：`l` → `{l}`',
        'if l >= K': lambda S, B, r: (f'`l = {S.l} ≥ K = {S.K}`：第 K 个字符已经落在前 `{S.index + 1}` 个字符展开的范围里' if S.l >= S.K
                                       else f'`l = {S.l} < K = {S.K}`：还不够长，继续往后扩展'),
        'last_pos = index': '记下 `last_pos = {last_pos}`：后面的字符都不用看了',
        'for index in range(last_pos': '倒推：下标 `{index}`，字符 `{S[index]}`',
        'char = S[index]': '取出 `{char}`',
        "if char >= 'a'": lambda S, B, r: (f"`{S.char}` 是小写字母" if 'a' <= S.char <= 'z' else f"`{S.char}` 是数字"),
        'if l == K': lambda S, B, r: (f'`l = {S.l} == K`：第 K 个字符就是当前字母 `{S.char}`' if S.l == S.K
                                      else f'`l = {S.l} > K = {S.K}`：答案在这个字母的前面'),
        'return char': '找到答案：`{char}`',
        'l -= 1': '去掉这个字母，整段变短：`l` → `{l}`',
        'l //= int': '数字 `{char}`：整段是前面的串重复 `{char}` 次，前面串长 `l = {l}`',
        'K %= l': '重复的串里第 K 个 = 原串里第 `K % l` 个：`K` → `{K}`',
        'if K == 0': lambda S, B, r: ('`K` 取模得 0，说明是原串的==最后一个==字符' if S.K == 0 else f'`K = {S.K}` 不为 0，保持不变'),
        'K = l': '`K = l = {K}`：取模为 0 时要把 K 改成串长，不是 0',
    },
    cards=dict(
        one_liner='K 很大，不展开：先算长度，再倒着取模还原',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['编码串 `S` 由小写字母和数字 `2~9` 组成：读到字母就写下，读到数字 `d` 就把已有内容再重复 `d - 1` 次',
                 '返回解码后字符串的第 `K` 个字符（从 1 开始）',
                 '示例：`S = "leet2code3"`，`K = 10` → `"o"`；本视频取 `K = 15` → `"e"`'],
        quote='不能实打实地扩展，那么就只能先计算其长度……当某一时刻的l大于等于K时，记最后一个扩展的字符下标为last_pos。接下来，可以从last_pos开始往前，反过来找答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['正推：字母 `l += 1`，数字 `l *= d`，一旦 `l >= K` 就停',
              '倒推遇字母：`l == K` 就是答案，否则去掉它 `l -= 1`',
              '倒推遇数字：先 `l //= d` 得到前一段长度，再 `K %= l`；==余 0 要改成 l=='],
        summary=['时间 `O(n)`，空间 `O(1)`，不会真的展开字符串',
                 '易错点：`K % l == 0` 时 K 应置为 `l`（对应前一段的最后一个字符）',
                 '正推到 `l >= K` 就停，否则 `l` 会爆得非常大',
                 '原文为 Python 2 写法，整除 `l /= int(char)` 已改为 `l //= int(char)`，并删去类型说明文档字符串'],
    ),
)
