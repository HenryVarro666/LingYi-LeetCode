TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

S0, K0 = 'aabcbad', 2


def _cur(S):
    i = getattr(S.get('s'), 'k', None)
    return i if isinstance(i, int) and i >= 0 else None


def _kept(S):
    """已经追加进 res 的下标（只用于画图）"""
    s = S.get('s')
    if s is None:
        return set()
    m = getattr(s, 'k', -1)
    if m == -1:
        return set()
    if m is None:
        m = len(s)
    K = S['k']
    res, state, kept = [], 0, set()
    for i in range(m):
        v = 1 << (ord(s[i]) - 97)
        if state & v:
            continue
        res.append(s[i])
        kept.add(i)
        state |= v
        if len(res) > K:
            state ^= 1 << (ord(res[-K - 1]) - 97)
    return kept


def _verdict(S):
    if _cur(S) is None or 'v' not in S:
        return None
    line = S.get('_line', 0)
    if line < 9:
        return None
    if line >= 12:
        return True
    return not ((S['state'] & S['v']) == S['v'])


def _dim(S, i, v):
    c = _cur(S)
    return c is not None and i < c and i not in _kept(S)


def _color(S, i, v):
    if i != _cur(S):
        return None
    vd = _verdict(S)
    return 'blue' if vd is None else ('green' if vd else 'red')


def _win(S):
    res, K = S.get('res'), S.get('k')
    if res is None or not res:
        return None
    return max(0, len(res) - K)


def _win_end(S):
    res = S.get('res')
    return None if not res else len(res) - 1


def _bits(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 10), 'state：26 个二进制位，第 i 位 = 字母 chr(97+i) 在不在 res 最后 k 个字符里', 22, T['muted'], bold=True)
    st = S.get('state')
    if st is None:
        return
    v = S.get('v')
    cell = (x1 - x0 - 40) / 26
    sx = x0 + 20
    ys = y0 + 56
    h = min(cell * 1.3, 52)
    for i in range(26):
        on = (st >> i) & 1
        X = sx + i * cell
        cv.rect((X + 2, ys, X + cell - 2, ys + h), fill=T['blue'] if on else T['panel2'], r=6, outline=T['border'])
        cv.text((X + cell / 2, ys + h / 2), '1' if on else '0', 22, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
        mark = v is not None and v == (1 << i) and _cur(S) is not None
        cv.text((X + cell / 2, ys + h + 8), chr(97 + i), 22, T['pink'] if mark else T['muted'], anchor='mt', bold=True, mono=True)
        if mark:
            cv.rect((X, ys - 4, X + cell, ys + h + 4), outline=T['pink'], width=4, r=8)
    cv.text((x0 + 20, ys + h + 46), f'state = {st}（二进制 {st:b}）', 24, T['text'], mono=True)


def _note(S):
    res, K = S.get('res'), S['k']
    if res is None:
        return f'`k = {K}`：只要新字符和==答案最后 {K} 个字符==里的某个相同，就算靠近'
    win = ''.join(res[-K:]) if res else ''
    line = S.get('_line', 0)
    if _cur(S) is None:
        return f'遍历结束：`res = {"".join(res)}`'
    c = S['c']
    if line < 9:
        return f'答案最后 {K} 个字符 = `{win or "空"}`，新字符 `{c}`：看它在不在里面'
    if line == 9 or line == 10:
        return (f'`{c}` 在最后 {K} 个字符 `{win}` 里 → ==靠近，丢弃==' if (S['state'] & S['v']) == S['v']
                else f'`{c}` 不在最后 {K} 个字符 `{win or "空"}` 里 → ==保留==')
    return f'`{c}` 已加入，最后 {K} 个字符 = `{win}`，`state` 里置 1 的位就是它们'


def _if(S, B, ret):
    c, v, st = S.c, S.v, S.state
    if (st & v) == v:
        return f'`state & v = {st & v} == v`：位已是 1 → `{c}` 在最后 `k` 个字符里 → ==靠近，要合并=='
    return f'`state & v = {st & v} ≠ v`：位是 0 → `{c}` 不在最后 `k` 个字符里 → 保留'


def _len(S, B, ret):
    if len(S.res) > S.k:
        return f'`len(res) = {len(S.res)} > k = {S.k}` → 窗口多出一个字符，最左边的 `{S.res[-S.k - 1]}` 要滑出去'
    return f'`len(res) = {len(S.res)} ≤ k = {S.k}` → 窗口还没满，没有字符滑出'


CONFIG = dict(
    num=3853, title='合并靠近字符', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二进制位记录最后 k 个字符',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1472'],
    code='''
class Solution(object):
    def mergeCharacters(self, s, k):
        
        res = []
        state = 0

        for c in s:
            v = 1 << (ord(c) - 97)
            if (state & v) == v:
                continue
            
            res.append(c)
            state |= v
            if len(res) > k:
                state ^= 1 << (ord(res[-k - 1]) - 97)
        
        return ''.join(res)
''',
    setup=TRACK,
    call=f'Solution().mergeCharacters(Tracked({S0!r}), {K0})',
    expect='abcad',
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（蓝 = 当前；绿 = 保留；红 = 靠近被丢弃；灰 = 已丢弃）', h=200, cell=100,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'c'}, dim=_dim, color=_color),
        dict(type='array', var='res', label='res（框 = 最后 k 个字符，也就是 state 记录的窗口）', cell=96, h=175,
             window=(_win, _win_end), window_color='orange'),
        dict(type='custom', draw=_bits, h=245),
        dict(type='text', fn=_note, size=26, h=100),
    ],
    watch=[('c', 'c', 'blue'), ('k', 'k', 'orange'), ('state', 'state', 'purple'), ('res', "''.join(res)", 'green')],
    captions={
        'res = []': '`res` 就是答案：一边扫描，一边往后追加',
        'state = 0': '`state` 是一个整数，用它的二进制位记录 res ==最后 k 个字符==里有哪些字母',
        'for c in s': lambda S, B, ret: (f"从左到右扫描：`s[{S.s.k}] = '{S.c}'`" if getattr(S.s, 'k', None) is not None
                                         else '`s` 扫描完毕'),
        'v = 1 << (ord(c) - 97)': "`{c}` 是第 `{ord(c) - 97}` 个字母 → `v = 1 << {ord(c) - 97} = {v}`，只有这一位是 1",
        'if (state & v) == v': _if,
        'continue': '靠近 → 右边并入左边：丢弃这个字符，`res` 和 `state` 都不变',
        'res.append(c)': '`{c}` 加入答案：`res = {"".join(res)}`',
        'state |= v': '把 `{c}` 这一位置 1：`state = {state}`',
        'if len(res) > k': _len,
        'state ^=': '最左边的 `{res[-k - 1]}` 滑出窗口：异或把它那一位清零 → `state = {state}`',
        "return ''.join(res)": '返回 `{ret}`',
    },
    cards=dict(
        one_liner='用一个整数的 26 个二进制位，记住答案最后 k 个字符里有哪些字母',
        complexity='时间 `O(n)`，空间 `O(n)`（答案 res）；`state` 只是一个整数',
        problem=['两个相同字符的下标距离 ==≤ k== 就算靠近，右边的合并到左边，先合并左下标最小的',
                 '问合并完成后的字符串是什么',
                 '本视频：`s = "aabcbad", k = 2` → `"abcad"`'],
        quote='若当前字符出现在答案字符串的最后k个字符中，就说明当前字符需要被合并，反之则需要将其加入到答案字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['合并必须先处理左下标最小的一对 → 从左到右扫描，边扫边定答案',
              '新字符出现在答案最后 `k` 个字符里 → 靠近 → 丢掉；否则追加到 `res`',
              '只有小写字母：压成 26 位二进制，追加时置 1，字符滑出最后 `k` 个时清 0'],
        result='`res` 拼起来是 `"abcad"`：两个 b、两个 a 靠得太近的都被合并 ✓',
        summary=['时间 `O(n)`，查询“在不在最后 k 个”只要一次位与，`O(1)`',
                 '`state ^= …` 用异或清位是安全的：窗口里的字母互不相同（靠近的早被合并了）',
                 '易错：滑出的是 `res[-k-1]`（追加之后的第 k+1 个），且要先判断 `len(res) > k`',
                 '同样的判断也可以暴力 `c in res[-k:]` 或哈希表，位运算只是常数更小',
                 '对比灵神：灵神用栈 + `last[ch]` 算下标距离；这里直接维护最后 k 个字符的集合'],
    ),
)
