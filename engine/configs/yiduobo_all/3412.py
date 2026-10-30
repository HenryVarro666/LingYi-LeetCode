S = 'abzyaz'


def _pairs(s, upto):
    """在 s[:upto+1] 上重放一遍算法：返回 (已配对下标 -> 搭档, 本步 upto 的搭档或 None)"""
    stk = {}
    match = {}
    for i, ch in enumerate(s[:upto + 1]):
        m = chr(219 - ord(ch))
        if stk.get(m):
            j = stk[m].pop()
            match[i], match[j] = j, i
        else:
            stk.setdefault(ch, []).append(i)
    return match, match.get(upto)


def _working(S):
    ln = S['_line']
    if ln in (11, 12):
        return True
    if ln == 10:
        return 'mirror' not in S or S['mirror'] != chr(219 - ord(S['char']))
    return False


def _color(S, i, v):
    if 'index' not in S or 'mirror' not in S and S['_line'] < 10:
        return None
    cur, ln = S['index'], S['_line']
    match, partner = _pairs(S['s'], cur)
    if i == cur:
        if _working(S):
            return 'blue'
        if ln == 13:
            return 'yellow'
        return 'green' if i in match else 'cyan'
    if i < cur:
        if ln == 13 and i == partner:
            return 'yellow'
        return 'green' if i in match else 'cyan'
    return None


def _umap(S):
    u = S.get('unmarked')
    if u is None:
        return None
    return {k: u[k] for k in sorted(set(S['s'])) if k in u}


def _txt(S, B):
    if 'char' not in S or 'index' not in S or S['_line'] < 10:
        return '给每个字符准备一个栈：存它==还没被标记==的下标'
    ln, ch, idx = S['_line'], S['char'], S['index']
    if ln == 17 or (ln == 10 and B.get('index') == idx):
        return f'遍历完毕：总分 `res = {S["res"]}`'
    if ln == 10:
        return f'取出 `s[{idx}] = {ch}`，接下来算它的镜像'
    mi = chr(219 - ord(ch))
    if ln == 11:
        return f'`{ch}` 的 ASCII 码是 {ord(ch)}，镜像 = 219 − {ord(ch)} = {219 - ord(ch)} → ==`{mi}`=='
    if ln == 12:
        st = S['unmarked'][mi]
        return f'看 `{mi}` 的栈：' + (f'有 `{st}`，栈顶最近' if st else '空，左边没有可配的')
    if ln == 13:
        return f'`{ch}` 和栈顶下标配上，==下标之差==累加：`res = {S["res"]}`'
    return f'`{ch}` 暂时没配上，下标 `{idx}` 记进自己的栈'


CONFIG = dict(
    num=3412, title='计算字符串的镜像分数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字典 + 栈 · ASCII 码之和算镜像',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1578'],
    code='''
class Solution(object):
    def calculateScore(self, s):
        
        unmarked = {}
        for asc in range(92, 123):
            char = chr(asc)
            unmarked[char] = []
        
        res = 0
        for index, char in enumerate(s):
            mirror = chr(219 - ord(char))
            if unmarked[mirror]:
                res += index - unmarked[mirror].pop()
            else:
                unmarked[char].append(index)

        return res
''',
    call=f'Solution().calculateScore({S!r})',
    expect=5,
    skip=['for asc in range', 'char = chr(asc)', 'unmarked[char] = []'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前下标，青 = 在栈里等配对，绿 = 已标记，黄 = 刚配上）', cell=100, h=200,
             pointers={'index': 'blue'}, color=_color),
        dict(type='map', var=_umap, label='unmarked（字符 → 栈：未标记的下标，栈顶在右）',
             fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
        dict(type='text', fn=_txt, size=28, h=100),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink'), ('mirror', 'mirror', 'cyan'), ('res', 'res', 'green')],
    captions={
        'unmarked = {}': '要找“镜像字符上一次出现且未标记的位置” → 每个字符一个栈。原文先给 ASCII 92~122 各建一个空栈，这里直接快进到建好',
        'res = 0': '`res` 累计得分，初始 0',
        'for index, char in enumerate(s)': lambda S, B, r: (
            f'走到下标 `{S.index}`，字符 `{S.char}`' if 'index' not in B or B.index != S.index
            else '字符串走完了，结束循环'),
        'mirror = chr(219 - ord(char))': '一对镜像字符的 ASCII 码之和恰好是 219：`219 - {ord(char)}` = {219 - ord(char)} → 镜像 =={mirror}==',
        'if unmarked[mirror]': lambda S, B, r: (
            f'`{S.mirror}` 的栈是 `{S.unmarked[S.mirror]}`，==有未标记的下标== → 栈顶就是最近的那个 j'
            if S.unmarked[S.mirror] else
            f'`{S.mirror}` 的栈是空的 → 左边没有可以配对的镜像，==跳过=='),
        'res += index - unmarked[mirror].pop()': '弹出栈顶 `j = {B.unmarked[mirror][-1]}`，配上：`res += {index} - {B.unmarked[mirror][-1]}` → =={res}==',
        'unmarked[char].append(index)': '没配上：把 `{index}` 放进 `{char}` 自己的栈，留给后面的字符',
        'return res': '最终得分 =={ret}==',
    },
    cards=dict(
        one_liner='给每个字符一个栈，镜像字符的栈顶就是最近的未标记下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`a` 的镜像是 `z`，`y` 的镜像是 `b`；一开始都未标记',
                 '从左到右，对每个 `i` 找左侧最近的未标记 `j`，`s[j]` 是 `s[i]` 的镜像',
                 '找到就标记 `i`、`j` 并加 `i - j`，找不到就跳过',
                 '本视频：`"abzyaz"` → `5`'],
        quote='对每个字符都是用一个栈来储存其未被标记的下标位置，使用栈的理由是为了方便获取最近一次的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['要的是“镜像字符上一次出现且未被标记”的下标 → 栈顶正好是最近的',
              '镜像用 ASCII 码算：一组镜像字符的码之和恰好是 `219`，所以 `chr(219 - ord(c))`',
              '镜像栈非空就弹栈顶、累加差值；为空就把当前下标记进自己的栈'],
        result='遍历结束，得分 `5` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`97 + 122 = 219`：`a` 和 `z` 的 ASCII 码之和，其余镜像对也一样',
                 '易错：配上对的字符==不入栈==，否则会被后面的字符重复配对',
                 '原文建栈的范围是 `range(92, 123)`，覆盖了小写字母即可；代码为 Python 3 兼容，没有改动'],
    ),
)
