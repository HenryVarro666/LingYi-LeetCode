TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

S0, K0 = 'yybyzybz', 2
NEG = float('-inf')


def _cur(S):
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _kept(S):
    """s 里已经入栈（没被合并）的下标（只用于画图）"""
    s = S.get('s')
    if s is None:
        return set()
    k = getattr(s, 'k', -1)
    if k == -1:
        return set()
    if k is None:
        k = len(s)
    kk = S['k']
    st, last, kept = 0, {}, set()
    for i in range(k):
        if st - last.get(s[i], NEG) > kk:
            last[s[i]] = st
            st += 1
            kept.add(i)
    return kept


def _verdict(S):
    """当前字符是否入栈：None = 还没判断"""
    i = _cur(S)
    if i is None or S.get('_line', 0) < 6:
        return None
    ch, st = S['ch'], S['st']
    last = S['last']
    pos = last.get(ch, NEG)
    if S['_line'] >= 7:
        return True
    return len(st) - pos > S['k']


def _dim(S, i, v):
    c = _cur(S)
    if c is None:
        return False
    if i < c:
        return i not in _kept(S)
    return False


def _color(S, i, v):
    c = _cur(S)
    if i != c:
        return None
    vd = _verdict(S)
    return 'blue' if vd is None else ('green' if vd else 'red')


def _stk(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 10), 'st（栈，框下数字 = 栈下标；虚线框 = 新字符将落在的位置 len(st)）', 22, T['muted'], bold=True)
    st = S.get('st')
    if st is None:
        return
    n = len(st)
    ch, line, K = S.get('ch'), S.get('_line'), S['k']
    ghost = ch is not None and _cur(S) is not None and line in (5, 6, 7)
    cell = min(104, (x1 - x0 - 60) / max(n + 1, 8))
    sx = x0 + 30
    ys = y0 + 130
    h = cell * 0.82
    pos = S['last'].get(ch, NEG) if ghost else None
    for i, c in enumerate(st):
        X = sx + i * cell
        hot = ghost and line == 6 and pos == i
        cv.rect((X + 4, ys, X + cell - 4, ys + h), fill=T['orange'] if hot else T['panel2'], r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + h / 2), c, 40, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + h + 10), i, 20, T['dim'], anchor='mt', mono=True)
    if not ghost:
        return
    X = sx + n * cell
    kept = _verdict(S)
    gcol = T['dim'] if line == 5 else (T['green'] if kept else T['red'])
    cv.rect((X + 4, ys, X + cell - 4, ys + h), outline=gcol, width=3, r=10)
    cv.text((X + cell / 2, ys + h / 2), ch, 40, gcol, anchor='mm', bold=True, mono=True)
    cv.text((X + cell / 2, ys + h + 10), n, 20, gcol, anchor='mt', mono=True)
    if line == 6 and pos != NEG and pos < n:
        d = n - pos
        col = T['green'] if d > K else T['red']
        mid = cv.arc_arrow((sx + pos * cell + cell / 2, ys - 8), (X + cell / 2, ys - 8), 34 + 8 * d, col)
        cv.text((mid[0], mid[1] - 8), f'距离 {d}', 26, col, anchor='mb', bold=True)


def _note(S):
    ch = S.get('ch')
    if ch is None or _cur(S) is None:
        return f'`k = {S["k"]}`：同字符的距离 ==≤ k== 就算靠近，右边的并入左边（被忽略）'
    st, K = S['st'], S['k']
    line = S.get('_line')
    pos = S['last'].get(ch, NEG)
    if line < 6:
        return f'新字符 `{ch}` 将落在栈下标 `len(st) = {len(st)}`，看看它上次在栈里的位置'
    if line >= 7:
        return f'`{ch}` 入栈：栈下标 `{S["last"][ch]}`，`last[{ch!r}]` 记下它'
    if pos == NEG:
        return f'`{ch}` 栈里还没有 → 距离 ==∞ > {K}== → 入栈'
    d = len(st) - pos
    return (f'距离 `{len(st)} − {pos} = {d}`，`{d} > {K}` → ==不靠近，入栈==' if d > K
            else f'距离 `{len(st)} − {pos} = {d}`，`{d} ≤ {K}` → ==靠近，右边并入左边，忽略==')


def _if(S, B, ret):
    ch, st, K = S.ch, S.st, S.k
    pos = S.last[ch]
    if pos == NEG:
        return f'`{ch!r}` 还没进过栈，`last[{ch!r}] = -inf` → `len(st) − last = ∞ > {K}` → ==入栈=='
    d = len(st) - pos
    if d > K:
        return f'`len(st) − last[{ch!r}] = {len(st)} − {pos} = {d} > {K}` → 离左边的 `{ch}` 够远 → ==入栈=='
    return f'`len(st) − last[{ch!r}] = {len(st)} − {pos} = {d} ≤ {K}` → 和左边的 `{ch}` ==靠近== → 并入左边，忽略它'


CONFIG = dict(
    num=3853, title='合并靠近字符', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 + last 数组 · 邻项消除',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1472'],
    code='''
class Solution:
    def mergeCharacters(self, s: str, k: int) -> str:
        st = []
        last = defaultdict(lambda: -inf)
        for ch in s:
            if len(st) - last[ch] > k:
                last[ch] = len(st)
                st.append(ch)
        return ''.join(st)
''',
    setup=TRACK,
    call=f'Solution().mergeCharacters(Tracked({S0!r}), {K0})',
    expect='ybzybz',
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（蓝 = 当前；绿 = 入栈；红 = 靠近被合并；灰 = 已被合并）', h=215, cell=100,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'ch'}, dim=_dim, color=_color),
        dict(type='custom', draw=_stk, h=260),
        dict(type='map', var='last', label='last：字符 → 它在栈中的最大下标（-∞ = 还没有）',
             fmt=lambda k, v: f"'{k}': " + ('-∞' if v == NEG else str(v)), h=120, font=32),
        dict(type='text', fn=_note, size=28, h=90),
    ],
    watch=[('ch', 'ch', 'blue'), ('k', 'k', 'orange'), ('len(st)', 'len(st)', 'purple'), ('st', "''.join(st)", 'green')],
    captions={
        'st = []': '栈保存==没被合并掉的字符==；栈的大小，就是新字符将来的“下标”',
        'last = defaultdict': '`last[c]` = 字符 `c` 在栈中的最大下标；没出现过就是 `-inf`，距离无穷大',
        'for ch in s': lambda S, B, ret: (f"取下一个字符 `s[{S.s.k}] = '{S.ch}'`，它若入栈会落在下标 `{len(S.st)}`"
                                          if getattr(S.s, 'k', None) is not None else '`s` 遍历完毕'),
        'if len(st) - last[ch] > k': _if,
        'last[ch] = len(st)': '`last[{ch!r}] = {last[ch]}`：记下它在栈里的下标',
        'st.append(ch)': '`{ch}` 入栈，栈 = `{"".join(st)}`',
        "return ''.join(st)": '栈里的字符拼起来就是答案 `{ret}`',
    },
    cards=dict(
        one_liner='栈只留“没被合并”的字符：新字符离同字符太近就忽略',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（返回值不计）',
        problem=['两个相同字符的下标距离 ==≤ k== 就算靠近，右边的合并到左边',
                 '每次先合并左下标最小的一对，合到没有靠近的字符为止',
                 '示例：`s = "yybyzybz", k = 2` → `"ybzybz"`'],
        quote='新遍历到的字符下标 - 该字符在栈中的最大下标 > k 那么把新遍历到的字符入栈，否则忽略新遍历到的字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这是邻项消除类的“消除”：用栈保存未被消除的字符',
              '未被消除的字符都在栈里 → 新字符的下标就是 `len(st)`',
              '用 `last` 记录每个字符在栈中的最新位置，距离 = `len(st) - last[ch]`，`O(1)` 查询'],
        result='栈里的字符拼成 `"ybzybz"`，与示例 3 一致 ✓',
        summary=['时间 `O(n)`；`last` 大小为 `|Σ| = 26`，空间 `O(|Σ|)`',
                 '`last` 默认值 `-inf`：第一次出现时距离无穷大，必然入栈',
                 '易错：`last` 存的是==栈下标==，不是 `s` 的下标，因为被忽略的字符不占位置',
                 '被忽略的字符不更新 `last`：它并入了左边那个字符，位置不变'],
    ),
)
