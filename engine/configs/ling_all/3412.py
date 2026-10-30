S = 'aaczzxby'


def _letters(S):
    return sorted({ord(ch) - 97 for ch in S['s']})


def _stk(S):
    if 'stk' not in S:
        return None
    return {chr(97 + k): S['stk'][k] for k in _letters(S)}


def _pairs(s, upto):
    """在 s[:upto+1] 上重放一遍算法：返回 (已配对下标 -> 搭档, 本步 upto 的搭档或 None)"""
    stk = [[] for _ in range(26)]
    match = {}
    for i, ch in enumerate(s[:upto + 1]):
        c = ord(ch) - 97
        if stk[25 - c]:
            j = stk[25 - c].pop()
            match[i], match[j] = j, i
        else:
            stk[c].append(i)
    return match, match.get(upto)


def _color(S, i, v):
    if 'i' not in S or 'c' not in S:
        return None
    cur, ln = S['i'], S['_line']
    match, partner = _pairs(S['s'], cur)
    working = ln in (6, 7) or (ln == 5 and S['c'] >= 97)
    if i == cur:
        if working:
            return 'blue'
        if ln == 8:
            return 'yellow'
        return 'green' if i in match else 'cyan'
    if i < cur:
        if ln == 8 and i == partner:
            return 'yellow'
        return 'green' if i in match else 'cyan'
    return None


def _mirror(S):
    if 'c' not in S or 'i' not in S:
        return '每个字母各用一个栈，存放它还没被标记的下标'
    if S['_line'] == 11 or (S['_line'] == 5 and S['c'] < 97):
        return f'遍历完毕：总分 `ans = {S["ans"]}`'
    if S['_line'] == 8:
        return f'配对成功：`s[{S["i"]}]` 和栈顶下标一起标记，==下标之差==加进 `ans = {S["ans"]}`'
    if S['_line'] == 10:
        return f'`s[{S["i"]}]` 暂时配不上，留在自己的栈里'
    c = S['c']
    c = c - 97 if c >= 97 else c
    ch, mi = chr(97 + c), chr(97 + 25 - c)
    st = S['stk'][25 - c] if 'stk' in S else []
    tail = f'，栈里有 `{st}`' if st else '，栈是空的'
    return f'`s[{S["i"]}] = {ch}`，镜像是 ==`{mi}`==（{c} + {25 - c} = 25）：看 `{mi}` 的栈{tail}'


CONFIG = dict(
    num=3412, title='计算字符串的镜像分数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='每个字母一个栈 · 栈顶 = 最近的未标记下标',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1578'],
    code='''
class Solution:
    def calculateScore(self, s: str) -> int:
        stk = [[] for _ in range(26)]
        ans = 0
        for i, c in enumerate(map(ord, s)):
            c -= ord('a')
            if stk[25 - c]:
                ans += i - stk[25 - c].pop()
            else:
                stk[c].append(i)
        return ans
''',
    call=f'Solution().calculateScore({S!r})',
    expect=10,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前 i，青 = 栈里等配对，绿 = 已标记，黄 = 刚配上）', cell=96, h=200,
             pointers={'i': 'blue'}, color=_color),
        dict(type='map', var=_stk, label='stk（每个字母的栈：未标记的下标，栈顶在右）',
             fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
        dict(type='text', fn=_mirror, size=28, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'stk = [[] for': '镜像字母要找==最近==的未标记下标 → 每个字母各配一个栈，栈顶就是最近的',
        'ans = 0': '`ans` 累计总分',
        'for i, c in enumerate(map(ord, s))': lambda S, B, r: (f'取出 `s[{S.i}] = {chr(S.c)}`，`c` 暂时是 ASCII 码 `{S.c}`'
                                                              if S.c >= 97 else '每个下标都处理过了，循环结束'),
        "c -= ord('a')": '字母转成 `0~25`：`c = {c}`。镜像是 `25 - c = {25 - c}`，所以镜像字母的栈是 `stk[{25 - c}]`',
        'if stk[25 - c]': lambda S, B, r: (
            f'镜像栈 `stk[{25 - S.c}]` = `{S.stk[25 - S.c]}` ==非空== → 栈顶就是左边最近的未标记镜像下标'
            if S.stk[25 - S.c] else
            f'镜像栈 `stk[{25 - S.c}]` ==为空== → 左边没有可配对的镜像字母'),
        'ans += i - stk[25 - c].pop()': '弹出栈顶 `j = {B.stk[25 - c][-1]}`（它和 `i` 一起被标记）：`ans += {i} - {B.stk[25 - c][-1]}` → =={ans}==',
        'stk[c].append(i)': '没有镜像可配 → 下标 `{i}` 留在 `stk[{c}]` 里（未标记），等后面的镜像字母来找它',
        'return ans': '返回总分 =={ret}==，配对分数都已加进 `ans`',
    },
    cards=dict(
        one_liner='每个字母一个栈：镜像在栈顶就配对，否则自己入栈',
        complexity='时间 `O(n + |Σ|)`，空间 `O(n + |Σ|)`',
        problem=['字母 `c` 的镜像是反转字母表后的位置：`a↔z`、`y↔b`',
                 '从左到右，每个 `i` 找左边==最近的未标记==镜像下标 `j`，配上就加 `i - j`',
                 '示例：`"aczzx"` → `5`；`"abcdef"` → `0`',
                 '本视频：`"aaczzxby"` → `10`'],
        quote='对于每种字母，分别用一个栈维护未标记字母的下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s[i]` 左边没有它的镜像字母：把下标 `i` 加到 `s[i]` 自己的栈里',
              '有镜像字母：弹出镜像字母栈顶，就是要找的最近 `j`，答案加 `i - j`',
              '后进先出 → 栈顶永远是离 `i` 最近的未标记下标'],
        result='所有配对分数加起来，返回 `10` ✓',
        summary=['时间、空间都是 `O(n + |Σ|)`，`|Σ| = 26`',
                 '`25 - c` 就是镜像：字母编号 `0~25`，`a` 对 `z`、`b` 对 `y`',
                 '易错：配上对的字母==不会==入栈，两个下标都算已标记',
                 '同类题：括号匹配等「找最近的未匹配」问题都可以用栈'],
    ),
)
