CODE = '''
class Solution(object):
    def strStr(self, haystack, needle):
        f = []

        m = len(haystack)
        n = len(needle)

        if n == 0:
            return 0
        if m == 0:
            return -1

        pos = 0
        f.append(0)
        for index in range(1, n):
            while pos > 0 and needle[pos] != needle[index]:
                pos = f[pos - 1]
            if needle[pos] == needle[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m):
            while pos > 0 and needle[pos] != haystack[index]:
                pos = f[pos - 1]
            if needle[pos] == haystack[index]:
                pos += 1
            if pos == n:
                return index - n + 1

        return -1
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(s, k=0):
    hits = [i + 1 for i, t in enumerate(_LINES) if s in t]
    return hits[k]


L_POS1 = _ln('pos = 0', 0)
L_POS2 = _ln('pos = 0', 1)
L2 = _ln('for index in range(m)')
INC = {_ln('pos += 1', 0), _ln('pos += 1', 1), _ln('f.append(pos)'), _ln('if pos == n'), _ln('return index - n + 1')}


def _phase2(S):
    return S.get('_line', 0) >= L2


def _draw_align(cv, S, B, box, T):
    """上排：被匹配的串（求 f 时是 needle 自己，匹配时是 haystack）；下排：needle 平移到 needle[pos] 对齐 index"""
    x0, y0, x1, y1 = box
    nd = S.get('needle')
    if nd is None:
        return
    p2 = _phase2(S) or S.get('_line') == L_POS2
    has_i = 'index' in S and S.get('_line') != L_POS2
    top = S['haystack'] if p2 else nd
    title = '对齐：上 = haystack，下 = needle（绿 = 已匹配，黄 = 正在比较）' if p2 else '对齐：上 = needle，下 = needle 的前缀（绿 = 已匹配，黄 = 正在比较）'
    cv.text((x0 + 18, y0 + 4), title, 23, T['muted'], bold=True)
    if not has_i:
        top, i, p, off, inc = top, None, 0, 0, False
    else:
        i, p = S['index'], S['pos']
        inc = S.get('_line') in INC
        off = i - p + (1 if inc else 0)
    span = max(len(top), off + len(nd), 1)
    cell = min(76, (x1 - x0 - 190) / span)
    sx = x0 + 160
    ty = y0 + 112
    by = ty + cell + 56
    cv.text((x0 + 18, ty + cell / 2), 'haystack' if p2 else 'needle', 24, T['blue'], anchor='lm', bold=True, mono=True)
    cv.text((x0 + 18, by + cell / 2), 'needle', 24, T['pink'], anchor='lm', bold=True, mono=True)
    for k, ch in enumerate(top):
        X = sx + k * cell
        fill = T['panel2']
        if i is not None:
            lo, hi = off, (i if inc else i - 1)
            if lo <= k <= hi:
                fill = (35, 90, 50)
        oc = T['blue'] if (i is not None and k == i) else T['border']
        cv.rect((X + 3, ty, X + cell - 3, ty + cell), fill=fill, outline=oc, width=4 if k == i else 1, r=8)
        cv.text((X + cell / 2, ty + cell / 2), ch, 32, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ty - 6), k, 17, T['dim'], anchor='mb', mono=True)
    if i is not None:
        X = sx + i * cell + cell / 2
        cv.tri_down(X, ty - 26, 10, T['blue'])
        cv.text((X, ty - 42), 'index', 20, T['blue'], anchor='mb', bold=True)
    for k, ch in enumerate(nd):
        X = sx + (off + k) * cell
        fill = T['panel2']
        if i is not None and k < p:
            fill = (35, 90, 50)
        cmp_ = i is not None and not inc and k == p
        oc = T['yellow'] if cmp_ else T['border']
        cv.rect((X + 3, by, X + cell - 3, by + cell), fill=fill, outline=oc, width=4 if cmp_ else 1, r=8)
        cv.text((X + cell / 2, by + cell / 2), ch, 32, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, by + cell + 4), k, 17, T['dim'], anchor='mt', mono=True)
    if i is not None and p < len(nd):
        X = sx + (off + p) * cell + cell / 2
        cv.tri_up(X, by + cell + 28, 10, T['pink'])
        cv.text((X, by + cell + 44), 'pos', 20, T['pink'], anchor='mt', bold=True)
    if i is not None and not inc and p < len(nd) and i < len(top):
        a, b = nd[p], top[i]
        msg = f"needle[{p}] = '{a}'  vs  {'haystack' if p2 else 'needle'}[{i}] = '{b}'  →  {'相同' if a == b else '不同'}"
        cv.text(((x0 + x1) / 2, y1 - 22), msg, 24, T['green'] if a == b else T['red'], anchor='mm', bold=True, mono=True)


def _while(S, B, ret):
    p, i = B.pos, B.index
    top = B.haystack if _phase2(B) else B.needle
    nm = 'haystack' if _phase2(B) else 'needle'
    if p == 0:
        return '`pos = 0`：没有可回退的了，不进入套娃'
    if B.needle[p] == top[i]:
        return f"`needle[{p}] = '{B.needle[p]}'` 等于 `{nm}[{i}]`：可以在这 {p} 位的基础上接上，停止套娃"
    return f"`needle[{p}] = '{B.needle[p]}'` ≠ `{nm}[{i}] = '{top[i]}'`：==接不上==，需要套娃"


def _back(S, B, ret):
    return f'套娃：`pos = f[{B.pos - 1}] = {S.pos}`（needle 前 {B.pos} 位的最长「前缀 = 后缀」），needle 右移'


def _if(S, B, ret):
    p, i = B.pos, B.index
    top = B.haystack if _phase2(B) else B.needle
    nm = 'haystack' if _phase2(B) else 'needle'
    if B.needle[p] == top[i]:
        return f"`needle[{p}] == {nm}[{i}] = '{top[i]}'` → 匹配长度 ==加一位=="
    return f"`needle[0] = '{B.needle[0]}'` ≠ `{nm}[{i}] = '{top[i]}'`：一位都匹配不上"


CONFIG = dict(
    num=28, title='找出字符串中第一个匹配项的下标', difficulty='Easy', category='字符串',
    author='yiduobo', technique='KMP（用 DP 理解 next 数组）',
    tags=['字节30天', '面试经典150'],
    code=CODE,
    call="Solution().strStr('ababac', 'abac')",
    expect=2,
    views=[
        dict(type='custom', draw=_draw_align, h=420),
        dict(type='array', var='f', label='f[i]：needle[:i+1] 中「前缀 = 后缀」的最长长度', cell=76, min_slots=4,
             pointers={"index if _line < %d else None" % L2: 'blue'},
             pointer_labels={"index if _line < %d else None" % L2: 'index'}),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'pink'), 'f'],
    skip=['m = len', 'n = len', 'if m == 0'],
    captions={
        'f = []': '`f[i]`：needle 以第 i 个字符结尾的串，能与 ==needle 前缀== 匹配的最长长度',
        'if n == 0': 'needle 为空 → 返回 0；这里 `n = {n}`，继续',
        L_POS1: '第一段：用 DP 的思路求 `f`，`pos` 是当前已匹配的前缀长度',
        'f.append(0)': '`f[0] = 0`：单个字符没有真前缀可以匹配',
        'for index in range(1, n)': lambda S, B, r: (f'求 `f[{S.index}]`：先看上一位的结果 `pos = f[{S.index - 1}] = {S.pos}`'
                                                    if S.get('index') != B.get('index') else '`f` 求完了'),
        'while pos > 0 and needle[pos] != needle[index]': _while,
        'pos = f[pos - 1]': _back,
        'if needle[pos] == needle[index]': _if,
        'pos += 1': '`pos = {pos}`：已匹配 {pos} 位',
        'f.append(pos)': '`f[{index}] = {pos}`',
        L_POS2: '第二段：==用相同的思路去匹配 haystack==，`pos` 归零',
        'for index in range(m)': lambda S, B, r: f"看 `haystack[{S.index}] = '{S.haystack[S.index]}'`，此前已匹配 `pos = {S.pos}` 位",
        'while pos > 0 and needle[pos] != haystack[index]': _while,
        'if needle[pos] == haystack[index]': _if,
        'if pos == n': lambda S, B, r: (f'`pos = {S.pos} == n`：needle ==整串匹配上了==' if S.pos == S.n
                                        else f'`pos = {S.pos} < n = {S.n}`，还没匹配完'),
        'return index - n + 1': '匹配结束在 `index = {index}`，起点 `index - n + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 记录最长的「前缀 = 后缀」，失配时套娃回退，不回头扫 haystack',
        complexity='时间 `O(m + n)`，空间 `O(n)`',
        problem=['给你两个字符串 `haystack` 和 `needle`',
                 '找出 needle 在 haystack 中==第一个匹配项==的下标（从 0 开始），不存在返回 `-1`',
                 '示例：`haystack = "sadbutsad"`，`needle = "sad"` → `0`',
                 '`"leetcode"`，`"leeto"` → `-1`；本视频：`"ababac"`，`"abac"` → `2`'],
        quote='f[i]表示needle中以第i个字符结尾的字符串中，==能与needle的前缀匹配的最长的长度==……通过needle计算出f之后，用相同的思路去匹配haystack即可。',
        quote_src='—— yiduobo 题解原文（kmp 算法）',
        idea=['`needle[f[i-1]] == needle[i]`：在 `f[i-1]` 的基础上==加一位==',
              '不相同就「套娃」：`pos = f[pos-1]`，直到能接上或 `pos = 0`',
              '匹配 haystack 时一模一样，`pos == n` 就找到了答案'],
        summary=['时间 `O(m + n)`：pos 每次最多 +1，套娃只会让它变小，总回退次数不超过总前进次数',
                 '易错：套娃是 `pos = f[pos - 1]`，不是 `f[pos]`',
                 '易错：`while` 要先判 `pos > 0`，再比较字符',
                 '原文还介绍了 RK（滚动哈希）算法，同样是线性的',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
