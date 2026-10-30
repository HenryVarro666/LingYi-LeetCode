import sys as _sys

DIGITS = ["1", "3", "5", "7"]
N = 100
S_ = str(N)


def _frames():
    """custom 视图只拿到合并后的变量；从调用者（views.v_custom）的局部变量里取完整的帧列表"""
    f = _sys._getframe(2)
    for _ in range(6):
        if f is None:
            return []
        st = f.f_locals.get('st')
        if isinstance(st, dict) and '_frames' in st:
            return st['_frames']
        f = f.f_back
    return []


def slots_view(cv, S, B, box, T):
    """上排：n 的各位；下排：递归路径上已经填的数（· = 跳过不填，? = 正在决定）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'n = {N} 的各位 vs 正在构造的数（· = 不填，? = 当前位）', 24, T['muted'], bold=True)
    frs = [fr for fr in _frames() if fr['name'] == 'f']
    built = []
    for fr in frs[:-1]:
        loc = fr['locals']
        if fr['line'] == 11:
            built.append('·')
        elif fr['line'] == 18:
            built.append(loc.get('d', '?'))
    cur = frs[-1]['locals'] if frs else {}
    L = len(S_)
    cw = 110
    sx = x0 + (x1 - x0 - cw * L) / 2
    for k in range(L):
        X = sx + k * cw
        cv.rect((X + 6, y0 + 44, X + cw - 6, y0 + 110), fill=T['panel2'], outline=T['border'], width=1, r=10)
        cv.text((X + cw / 2, y0 + 77), S_[k], 34, T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cw / 2, y0 + 116), f'i={k}', 18, T['dim'], anchor='mt', mono=True)
        if k < len(built):
            ch, fill, tc = built[k], (T['blue'] if built[k] != '·' else T['panel']), (T['bg'] if built[k] != '·' else T['dim'])
        elif frs and k == cur.get('i'):
            ch, fill, tc = '?', T['yellow'], T['bg']
        else:
            ch, fill, tc = '', T['panel'], T['dim']
        cv.rect((X + 6, y0 + 146, X + cw - 6, y0 + 212), fill=fill, outline=T['border'], width=1, r=10)
        cv.text((X + cw / 2, y0 + 179), ch, 34, tc, anchor='mm', bold=True, mono=True)
    if frs:
        lim, num = cur.get('is_limit'), cur.get('is_num')
        t1 = f"is_limit = {lim}" + ('（受 n 约束：这一位最多填 n 的这一位）' if lim else '（不受约束：最多填 9）')
        t2 = f"is_num = {num}" + ('（前面填过数字）' if num else '（前面都没填：可以继续跳过）')
        cv.text((x0 + 30, y0 + 236), t1, 22, T['pink'] if lim else T['muted'], mono=False)
        cv.text((x0 + 30, y0 + 266), t2, 22, T['green'] if num else T['muted'], mono=False)


def _I(S):
    return S['_inner']


def _cap_term(S, B, ret):
    I = B['_inner']
    if I.get('i') == len(S_):
        if I.get('is_num'):
            return '`i == len(s)`：所有位都决定完，且==填了数字== → 构成 1 个合法数字，返回 `1`'
        return '`i == len(s)`：所有位都跳过了，==一个数字都没填== → 不算，返回 `0`'
    return f"`i = {I['i']}` 还没到末尾，继续决定这一位"


def _cap_skip_if(S, B, ret):
    I = B['_inner']
    if not I['is_num']:
        return '前面没填数字 → ==可以跳过这一位==（构造位数更少的数）'
    return '前面已经填了数字 → 这一位==必须填=='


def _cap_up(S, B, ret):
    I = S['_inner']
    who = f"`f({I['i']}, {I['is_limit']}, {I['is_num']})`"
    if I['is_limit']:
        return f"{who} 受约束：这一位最多填 `s[{I['i']}] = '{I['up']}'`"
    return f"{who} 不受约束：这一位最多填 `'9'`（digits 里的数都能填）"


def _cap_break(S, B, ret):
    I = S['_inner']
    d, up = I['d'], I['up']
    if d > up:
        return f"枚举 `d = '{d}'` `> up = '{up}'` → digits 有序，后面更大 → ==break=="
    return f"枚举 `d = '{d}'` `≤ up = '{up}'` → 可以填"


def _cap_rec(S, B, ret):
    I = B['_inner']
    lim = I['is_limit'] and I['d'] == I['up']
    call = f"f({I['i'] + 1}, {lim}, True)"
    pre = f"`d = '{I['d']}'` ≤ `up = '{I['up']}'`，"
    if S['_inner'].get('i') == I['i'] + 1 and S['_inner'].get('d') is None:
        return pre + f"填它，递归 `{call}`" + ('（填了上限，后面==仍受约束==）' if lim else '')
    return pre + f"填它：`{call}` ==之前算过，直接读缓存== → `res = {S['_inner'].get('res')}`"


def _cap_ret(S, B, ret):
    I = S['_inner']
    pre = ''
    if I.get('d') is not None and I['d'] > I['up']:
        pre = f"`d = '{I['d']}' > up = '{I['up']}'` → digits 有序，后面更大，break；"
    return pre + f"`f({I['i']}, {I['is_limit']}, {I['is_num']})` 算完：返回 =={ret}=="


CONFIG = dict(
    num=902, title='最大为 N 的数字组合', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP 通用模板（is_limit / is_num）',
    tags=['字节30天'],
    code='''
class Solution:
    def atMostNGivenDigitSet(self, digits: List[str], n: int) -> int:
        s = str(n)
        @cache
        def f(i: int, is_limit: bool, is_num: bool) -> int:
            if i == len(s): return int(is_num)  # 如果填了数字，则为 1 种合法方案
            res = 0
            if not is_num:  # 前面不填数字，那么可以跳过当前数位，也不填数字
                # is_limit 改为 False，因为没有填数字，位数都比 n 要短，自然不会受到 n 的约束
                # is_num 仍然为 False，因为没有填任何数字
                res = f(i + 1, False, False)
            up = s[i] if is_limit else '9'  # 根据是否受到约束，决定可以填的数字的上限
            # 注意：对于一般的题目而言，如果此时 is_num 为 False，则必须从 1 开始枚举，由于本题 digits 没有 0，所以无需处理这种情况
            for d in digits:  # 枚举要填入的数字 d
                if d > up: break  # d 超过上限，由于 digits 是有序的，后面的 d 都会超过上限，故退出循环
                # is_limit：如果当前受到 n 的约束，且填的数字等于上限，那么后面仍然会受到 n 的约束
                # is_num 为 True，因为填了数字
                res += f(i + 1, is_limit and d == up, True)
            return res
        return f(0, True, False)
''',
    call=f'Solution().atMostNGivenDigitSet({DIGITS}, {N})',
    expect=20,
    views=[
        dict(type='custom', draw=slots_view, h=300),
        dict(type='calls', h=230, label='递归栈 f(i, is_limit, is_num)'),
        dict(type='text', fn=lambda S: f"本层 `res = {S['_inner'].get('res')}`" if 'res' in S.get('_inner', {}) else '', size=26, h=56),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'yellow'), ('up', lambda S: S['_inner'].get('up'), 'pink'),
           ('d', lambda S: S['_inner'].get('d'), 'blue'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        's = str(n)': '把 `n` 转成字符串 `s = "{s}"`，从高位到低位一位一位地填',
        'return f(0, True, False)': '从第 0 位开始：一开始==受 n 约束==，且还没填数字',
        'if i == len(s)': _cap_term,
        'if not is_num': _cap_skip_if,
        'res = f(i + 1, False, False)': '跳过这一位：位数比 n 短，==不再受约束== → `f(i+1, False, False)`',
        'up = s[i] if is_limit': _cap_up,
        'if d > up: break': _cap_break,
        'res += f(i + 1': _cap_rec,
        'return res': _cap_ret,
    },
    skip=['res = 0', 'for d in digits', 'if d > up: break'],
    max_steps=60,
    cards=dict(
        one_liner='从高位往低位填：is_limit 管上限，is_num 管能不能跳过',
        complexity='时间 `O(d·log n)`，空间 `O(log n)`',
        problem=['给定按非递减排列的数字字符数组 `digits`，每个数字可以==重复使用任意次==',
                 '返回能写出的、==小于或等于== `n` 的正整数个数',
                 '示例：`digits = ["1","3","5","7"], n = 100` → `20`',
                 '（1 位数 4 个 + 2 位数 16 个；3 位数都 > 100）'],
        quote='isLimit 表示当前是否受到了 n 的约束。若为真，则第 i 位填入的数字至多为 s[i]，否则至多为 9……isNum 表示 i 前面的数位是否填了数字。若为假，则==当前位可以跳过（不填数字）==。',
        quote_src='—— 灵茶山艾府题解（数位 DP 通用模板）',
        idea=['`f(i, is_limit, is_num)`：构造第 `i` 位及之后的合法方案数',
              '`is_num` 为假时可以跳过这一位 → 自然地数出==位数更少==的数',
              '受约束且填了上限 `s[i]`，下一位仍受约束；`@cache` 记忆化重复状态'],
        result='返回 `20`：1 位数 4 个 + 2 位数 16 个 ✓',
        summary=['时间 `O(d·log n)`：状态数 `O(log n)`，每个状态枚举 `d` 个数字',
                 '易错：`is_limit` 往下传要写 `is_limit and d == up`，不是只看 `d == up`',
                 '本题 digits 没有 0，`is_num` 为假时不用特判从 1 开始枚举',
                 '模板通用：2376 统计特殊整数、233 数字 1 的个数、600 不含连续 1 的非负整数'],
    ),
)
