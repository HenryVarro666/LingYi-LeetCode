def _bin(x):
    return format(x, 'b')


def _win(S):
    if 'l' not in S or 's' not in S or S['_line'] < 16:
        return None
    l, line = S['l'], S['_line']
    if line in (24, 25, 26) and 'index' in S:
        return (S['index'], S['index'] + l - 1)
    if line >= 28 and line <= 33 and 'index' in S:
        return (S['index'] + 1, S['index'] + l)
    return (0, l - 1)


def _w0(S):
    w = _win(S)
    return None if w is None else w[0]


def _w1(S):
    w = _win(S)
    return None if w is None else w[1]


def _color(S, i, v):
    w = _win(S)
    if w is None or not (w[0] <= i <= w[1]):
        return None
    line = S['_line']
    if line in (25, 26) and 'index' in S and i == S['index']:
        return 'red'
    if line >= 28 and line <= 33 and i == w[1]:
        return 'green'
    return None


def _top(S):
    if 'l' not in S or S['_line'] < 11:
        return '先把每个查询要找的值 `first ^ second` 算出来，记下最大位数 `max_l`'
    if S['_line'] >= 36:
        return '查表：`pos[num]` 是左端点，右端点 = 左端点 + 位数 − 1'
    w = _win(S)
    if w is None:
        return ''
    return f"窗口长度 `l = {S['l']}`：当前窗口 `s[{w[0]}..{w[1]}]`，值 `now = {S.get('now', 0)}`（二进制 {_bin(S.get('now', 0))}）"


CONFIG = dict(
    num=2564, title='子字符串异或查询', difficulty='Medium', category='位运算',
    author='yiduobo', technique='按长度滑窗 · 哈希表记首次出现',
    tags=['灵神题单', '位运算', '难度分 1959'],
    code='''
class Solution(object):
    def substringXorQueries(self, s, queries):

        num_list = []
        max_l = 0
        for first, second in queries:
            num_list.append(first ^ second)
            max_l = max(max_l, len(bin(num_list[-1])) - 2)
        
        pos = {}
        for l in range(1, max_l + 1):
            if l > len(s):
                break
            
            now = 0
            for char in s[:l]:
                now += now
                if char == '1':
                    now += 1
            
            if now not in pos:
                pos[now] = 0

            for index, char in enumerate(s[l:]):
                if s[index] == '1':
                    now -= (1 << (l - 1))
                
                now += now
                if char == '1':
                    now += 1
                
                if now not in pos:
                    pos[now] = index + 1
        
        res = []
        for num in num_list:
            if num not in pos:
                res.append([-1, -1])
            else:
                res.append([pos[num], pos[num] + len(bin(num)) - 3])
        
        return res
''',
    call='Solution().substringXorQueries("101", [[0,5],[1,3],[4,4],[0,8]])',
    expect=[[0, 2], [0, 1], [1, 1], [-1, -1]],
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', h=160, label='s', window=(_w0, _w1), color=_color),
        dict(type='map', var='pos', h=290, fmt=lambda k, v: f'{_bin(k)} = {k}  →  首次下标 {v}', label='pos：子串的值 → 首次出现的左端点'),
        dict(type='array', var='num_list', h=110, label='num_list（每个查询要找的值 first ^ second）', cell=70),
    ],
    watch=['l', 'max_l', ('now', 'now', 'yellow')],
    captions={
        'num_list = []': '`num_list` 存每个查询要找的值 `first ^ second`',
        'max_l = 0': '`max_l`：这些值里最长的二进制位数，决定要开多长的窗口',
        'for first, second': lambda S, B, r: f'取查询 `({S.first}, {S.second})`' if 'first' in S else '查询处理完',
        'num_list.append': '`val = {first} ^ {second} = {first ^ second}`：它有 `{len(bin(first ^ second)) - 2}` 位，`max_l` 记下最大位数',
        'max_l = max': '`max_l` = `max({B.max_l}, len(bin({num_list[-1]})) - 2)` = =={max_l}==',
        'pos = {}': '`pos`：子串的值 → 首次出现的左端点',
        'for l in range': lambda S, B, r: f'开始枚举窗口长度 `l = {S.l}`（最大到 `max_l = {S.max_l}`）' if B.get('l') != S.l or 'l' not in B else '所有长度都试完了',
        'if l > len(s)': lambda S, B, r: (f'`l = {S.l} > len(s) = {len(S.s)}`：比整个串还长，不可能有这么长的子串 → ==break==' if S.l > len(S.s) else f'`l = {S.l} <= len(s)`：这个长度可以取'),
        'now = 0': '新长度重新开始：`now = 0`',
        'for char in s[:l]': lambda S, B, r: f"把前 `l = {S.l}` 位 `s[:l] = {S.s[:S.l]!r}` 逐位读进 `now`",
        'now += now': '`now` 左移一位（二进制末尾补 0）：`now = {now}`' if False else '`now += now`：`now` 乘 2，也就是左移一位 → {now}',
        "if char == '1'": lambda S, B, r: (f"`char = '1'` → 末位要补 1" if S.char == '1' else "`char = '0'` → 末位保持 0"),
        'now += 1': '末位补 1：`now = {now}`',
        'if now not in pos': lambda S, B, r: (f'`now = {S.now}` 还没记录 → 这是它==第一次出现==，记下左端点' if S.now not in S.pos else f'`now = {S.now}` 已经记录过 → 保留更早的左端点，不更新'),
        'pos[now] = 0': '窗口 `s[0..{l-1}]` 的值是 `{now}`，左端点 `0` → `pos[{now}] = 0`',
        'for index, char in enumerate': lambda S, B, r: ('这个长度的窗口滑到头了，换下一个长度' if B.get('char') == S.char and B.get('index') == S.index and S._line == 24 else f"窗口右移一格：新进来 `char = {S.char!r}`（`s[{S.index + S.l}]`），滑出的是 `s[{S.index}]`"),
        "if s[index] == '1'": lambda S, B, r: (f"滑出的 `s[{S.index}] = '1'` 是窗口最高位 → 先把它减掉：`now -= 1 << (l-1)`" if S.s[S.index] == '1' else f"滑出的 `s[{S.index}] = '0'`，最高位本来就是 0 → 不用减"),
        'now -= (1': '减去最高位 `2^{l-1}`：`now = {now}`',
        'pos[now] = index + 1': '新窗口 `s[{index+1}..{index+l}]` 值为 `{now}` → `pos[{now}] = {index + 1}`',
        'res = []': '预处理结束，开始逐个回答查询',
        'for num in num_list': lambda S, B, r: f'回答目标值 `num = {S.num}`' if B.get('num') != S.num or 'num' not in B else '查询回答完了',
        'if num not in pos': lambda S, B, r: (f'`{S.num}` 不在 `pos` 里 → 没有这样的子串' if S.num not in S.pos else f'`{S.num}` 在 `pos` 里，左端点是 `{S.pos[S.num]}`'),
        'res.append([-1': '答案 `[-1, -1]`',
        'res.append([pos': lambda S, B, r: f'左端点 `{S.pos[S.num]}`，长度 `len(bin({S.num})) - 2 = {len(bin(S.num)) - 2}` → 右端点 `{S.pos[S.num] + len(bin(S.num)) - 3}`',
        'return res': '全部查询回答完 → =={res}==',
    },
    skip=['now += now', 'now = 0', 'res = []', 'pos = {}', 'num_list = []', 'max_l = 0', 'max_l = max'],
    max_steps=58,
    cards=dict(
        one_liner='按长度枚举窗口，哈希表记下每个值第一次出现的位置',
        complexity='时间 `O(n·L + q)`，空间 `O(n·L)`（`L` 为最长位数）',
        problem=['二进制串 `s`，每个查询 `[first, second]`：找最短子串，使其十进制值 `val` 满足 `val ^ first == second`',
                 '多个答案取 `left` 最小的；找不到返回 `[-1, -1]`',
                 '本视频：`s="101"`，查询 `[[0,5],[1,3],[4,4],[0,8]]`'],
        quote='根据异或的性质，有val = first ^ second，那么本题就是给出若干组询问，对于每组询问(first, second)，找出first ^ second在字符串中首次出现的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`val = first ^ second`，查询变成“这个数在 `s` 里首次出现的位置”',
              '`max_l` = 所有目标值的最大二进制位数；==从长度 1 到 max_l 逐个长度开滑窗==',
              '窗口里的值滚动更新：先减去滑出的最高位，再左移一位，加上新位',
              '值的位数就是子串长度，所以 `pos` 只需存左端点'],
        summary=['时间 `O(n·L + q)`，`L = max_l ≤ 30`；空间 `O(n·L)`',
                 '滑窗更新值：`now -= 1<<(l-1)`（去掉最高位）→ `now += now`（左移）→ 加新位',
                 '只在 `now not in pos` 时记录，保证左端点最小；不同长度的子串值不会冲突（最高位是 1，0 另论）',
                 '答案右端点 = `pos + len(bin(num)) - 3`；目标值为 0 时 `bin(0)` 也是一位，恰好对上',
                 '原文为 Python 2 风格（`class Solution(object)`），代码本身无需改动',
                 '对比灵神：他从每个 `1` 往右枚举 30 位并单独记 0；这里按长度分层滑窗'],
    ),
)
