S0 = 'abcd'
P0 = 'bcc'


def _inner(S):
    return S.get('_inner') or S


def _in_z(S):
    I = _inner(S)
    return 't' in I and 'z' in I and isinstance(I.get('left'), int)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = _inner(S)
    m = len(P0)
    W = x1 - x0 - 40
    ln = S.get('_line', 0)
    if _in_z(S):
        t, z = I['t'], I['z']
        second = t[:m] != P0
        n = len(t)
        cell = min(84, W / n)
        sx = x0 + 20 + (W - cell * n) / 2
        ys = y0 + 110
        ch = cell * 0.85
        idx = I.get('index')
        bl, br = I['left'], I['right']
        cv.text((x0 + 18, y0 + 4), f"get_match（{'反转后的' if second else '正向的'}拼接串 t）：z[i] = t[i:] 与 t 的最长公共前缀", 22, T['muted'], bold=True)
        cv.text((sx, ys - 40), 'pattern 部分' if not second else 'pattern 反转部分', 20, T['blue'], anchor='lb', bold=True)
        cv.text((sx + m * cell + 8, ys - 40), 's 部分' if not second else 's 反转部分', 20, T['cyan'], anchor='lb', bold=True)
        if br >= bl and br > 0:
            cv.rect((sx + bl * cell + 2, ys - 8, sx + (br + 1) * cell - 2, ys + ch + 8), fill=T['yellow'], alpha=45, r=10)
            cv.text((sx + bl * cell + 4, ys + ch + 32), f'已知区间 [{bl}, {br}]', 20, T['yellow'], anchor='lt', bold=True)
        for k, c in enumerate(t):
            X = sx + k * cell
            base = T['blue'] if k < m else T['cyan']
            cv.rect((X + 3, ys, X + cell - 3, ys + ch), fill=T['panel2'], r=8, outline=base, width=2)
            cv.text((X + cell / 2, ys + ch / 2), c, 34, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, ys + ch + 6), k, 18, T['dim'], anchor='mt', mono=True)
        if idx is not None and idx < n and ln == 15 and len(z) > idx:
            a, b = z[-1], idx + z[-1]
            if b < n:
                for k, col in ((a, 'pink'), (b, 'green' if t[a] == t[b] else 'red')):
                    X = sx + k * cell
                    cv.rect((X + 1, ys - 3, X + cell - 1, ys + ch + 3), outline=T[col], width=5, r=10)
        if idx is not None and idx < n:
            X = sx + idx * cell + cell / 2
            cv.tri_up(X, ys + ch + 68, 10, T['yellow'])
            cv.text((X, ys + ch + 82), 'index', 20, T['yellow'], anchor='mt', bold=True)
        yz = ys + ch + 150
        cv.text((x0 + 18, yz - 8), 'z 列表（已追加的部分；黄框 = 刚追加、还在改的 z[index]）', 22, T['muted'], bold=True)
        for k in range(n):
            X = sx + k * cell
            known = k < len(z)
            cur = known and idx is not None and k == idx and ln != 21
            cv.rect((X + 3, yz + 30, X + cell - 3, yz + 30 + ch), fill=T['panel2'], r=8,
                    outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
            cv.text((X + cell / 2, yz + 30 + ch / 2), z[k] if known else '·', 32,
                    T['text'] if known else T['dim'], anchor='mm', bold=True, mono=True)
        return
    # ---- 主函数里：left / right 两条匹配长度
    s = S.get('s', S0)
    n = len(s)
    cell = min(80, W / max(n, m + 1))
    sx = x0 + 20 + (W - cell * n) / 2
    ys = y0 + 50
    ch = cell * 0.75
    idx = S.get('index') if ln >= 26 else None
    L = S.get('left') if isinstance(S.get('left'), list) else None
    R = S.get('right') if isinstance(S.get('right'), list) and ln >= 25 else None
    cv.text((x0 + 18, y0 + 4), '枚举起点 index：子串 t = s[index : index + m]，看它和 pattern 差几个字符', 22, T['muted'], bold=True)
    if idx is not None:
        cv.rect((sx + idx * cell, ys - 8, sx + (idx + m) * cell, ys + ch + 8), fill=T['blue'], alpha=40, r=12)
    for k, c in enumerate(s):
        X = sx + k * cell
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=T['panel2'], r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), c, 34, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 10), k, 16, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 10, ys + ch / 2), 's', 28, T['muted'], anchor='rm', bold=True)
    yp = ys + ch + 40
    if idx is not None:
        for k, c in enumerate(P0):
            X = sx + (idx + k) * cell
            cv.rect((X + 4, yp, X + cell - 4, yp + ch), fill=T['panel2'], r=8, outline=T['pink'], width=2)
            cv.text((X + cell / 2, yp + ch / 2), c, 34, T['pink'], anchor='mm', bold=True, mono=True)
        cv.text((sx - 10, yp + ch / 2), 'pattern', 22, T['pink'], anchor='rm', bold=True)
    yr = yp + ch + 50
    cv.text((x0 + 18, yr - 4), 'left[j]：s[j:] 与 pattern 的最长公共前缀', 22, T['blue'], bold=True)
    for k in range(n):
        X = sx + k * cell
        cur = idx == k
        cv.rect((X + 4, yr + 30, X + cell - 4, yr + 30 + ch), fill=T['panel2'], r=8,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cell / 2, yr + 30 + ch / 2), L[k] if L and k < len(L) else '·', 30, T['text'] if L else T['dim'], anchor='mm', bold=True, mono=True)
    yr2 = yr + ch + 70
    cv.text((x0 + 18, yr2 - 4), 'right[j]：s[:j+1] 与 pattern 的最长公共后缀', 22, T['purple'], bold=True)
    for k in range(n):
        X = sx + k * cell
        cur = idx is not None and idx + m - 1 == k
        cv.rect((X + 4, yr2 + 30, X + cell - 4, yr2 + 30 + ch), fill=T['panel2'], r=8,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cell / 2, yr2 + 30 + ch / 2), R[k] if R and k < len(R) else '·', 30, T['text'] if R else T['dim'], anchor='mm', bold=True, mono=True)


def _fm(S):
    ln = S.get('_line', 0)
    L, R = S.get('left'), S.get('right')
    if not _in_z(S) and ln >= 26 and 'index' in S and isinstance(L, list) and isinstance(R, list):
        i, m = S['index'], len(P0)
        a, b = L[i], R[i + m - 1]
        ok = a + b + 1 >= m
        return f"`left[{i}] + right[{i + m - 1}] + 1` = `{a} + {b} + 1` = =={a + b + 1}== {'≥' if ok else '<'} `len(pattern)` = `{m}` → {'==至多改一个字符，合格==' if ok else '要改的字符超过 1 个'}"
    return ''


def _c_if(S, B, r):
    i, l, rr = S.index, S.left, S.right
    if i <= rr and S.z[i - l] < rr - i + 1:
        return f'`index = {i}` 在已知区间 `[{l}, {rr}]` 里，且镜像 `z[{i - l}] = {S.z[i - l]}` < 区间剩余长度 `{rr - i + 1}` → ==直接抄镜像=='
    if i <= rr:
        return f'`index = {i}` 在区间 `[{l}, {rr}]` 里，但镜像 `z[{i - l}] = {S.z[i - l]}` ≥ 剩余长度 `{rr - i + 1}` → 超出部分未知，只能从 `{rr - i + 1}` 起继续比'
    return f'`index = {i}` 在已知区间 `[{l}, {rr}]` 外 → 没有现成结果，从 0 开始比'


def _c_wh(S, B, r):
    t, i, z = S.t, S.index, S.z
    a, b = z[-1], i + z[-1]
    if b >= len(t):
        return f'`z[-1] + index = {b}` 到串尾了 → `z[{i}] = {a}` 定下来'
    ok = t[a] == t[b]
    pre = f'`index = {i}` 不在已知区间内，从头比：' if S.right < i and a == 0 else ''
    return pre + f'比 `t[{a}] = {t[a]}`（开头）和 `t[{b}] = {t[b]}`（`index` 处）：' + ('==相等== → 再多匹配一个' if ok else f'==不等== → `z[{i}] = {a}` 定下来')


def _c_ret(S, B, r):
    return f'取 `z[len(pattern):]`：前面 pattern 那部分不要，剩下的对应 `s` 每个起点：`{S.z[len(P0):]}`'


def _c_cmp(S, B, r):
    i, m = S.index, len(S.pattern)
    a, b = S.left[i], S.right[i + m - 1]
    tot = a + b + 1
    return (f'前缀匹配 `left[{i}] = {a}`，后缀匹配 `right[{i + m - 1}] = {b}`，再 +1（中间换掉的那个字符）= `{tot}`，'
            + (f'≥ `{m}` → ==至多改一个，合格==' if tot >= m else f'< `{m}` → 至少 2 处不同，试下一个起点'))


CONFIG = dict(
    num=3303, title='第一个几乎相等子字符串的下标', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='扩展 KMP（Z 函数）· 前后缀匹配',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2509'],
    code='''
class Solution(object):
    def minStartingIndex(self, s, pattern):

        if len(pattern) == 1:
            return 0

        def get_match(t):
            z = [0]
            left, right = 0, 0
            for index in range(1, len(t)):
                if index <= right and z[index - left] < right - index + 1:
                    z.append(z[index - left])
                else:
                    z.append(max(0, right - index + 1))
                    while z[-1] + index < len(t) and t[z[-1] + index] == t[z[-1]]:
                        z[-1] += 1

                    if index + z[-1] - 1 > right:
                        left, right = index, index + z[-1] - 1

            return z[len(pattern):]

        left = get_match(pattern + s)
        right = get_match(pattern[::-1] + s[::-1])[::-1]

        for index in range(len(s) - len(pattern) + 1):
            if left[index] + right[index + len(pattern) - 1] + 1 >= len(pattern):
                return index

        return -1
''',
    call=f'Solution().minStartingIndex({S0!r}, {P0!r})',
    expect=1,
    skip=['if index <= right and z', 'z.append(max(0', 'if len(pattern) == 1', 'return 0', 'def get_match', 'for index in range(1, len(t))', 'z = [0]',
          'if index + z[-1] - 1 > right', 'left, right = index, index + z[-1] - 1'],
    views=[
        dict(type='custom', draw=_draw, h=620),
        dict(type='text', fn=_fm, size=26, h=70),
    ],
    watch=[('index', 'index', 'yellow'), ('已知区间左', 'left if isinstance(left, int) else None', 'blue'),
           ('已知区间右', 'right if isinstance(right, int) else None', 'pink')],
    captions={
        'left, right = 0, 0': '`z[0]` 不用算；`[left, right]` 记录目前==最靠右的已匹配区间==，一开始为空',
        'z.append(z[index - left])': '`index = {index}` 落在已知区间 `[{left}, {right}]` 里，镜像 `z[{index - left}]` 比剩余长度短 → ==直接抄==：`z[{index}] = {z[-1]}`，不用再比',
        'while z[-1] + index < len(t)': _c_wh,
        'z[-1] += 1': '匹配长度 +1：`z[{index}] = {z[-1]}`',
        'return z[len(pattern):]': _c_ret,
        'left = get_match(pattern + s)': '`left[i]`：把 `pattern` 接在 `s` 前面求 Z，==s 里每个起点能匹配 pattern 前缀多长==',
        'right = get_match': '`right[j]`：两个串都反转再求 Z、再反转结果，得到「以 `s[j]` 结尾能匹配 pattern 后缀多长」',
        'for index in range(len(s) - len(pattern) + 1)': lambda S, B, r: f'枚举起点 `index = {S.index}`，子串 `s[{S.index}:{S.index + len(S.pattern)}]` = `{S.s[S.index:S.index + len(S.pattern)]}`',
        'if left[index] + right': _c_cmp,
        'return index': '这个起点就是最靠前的合格子串：==返回 {index}==',
    },
    cards=dict(
        one_liner='前缀匹配长度 + 后缀匹配长度 + 1 ≥ len(pattern)',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['在 `s` 中找最靠前的子串，它和 `pattern` ==至多改一个字符==后相等',
                 '找不到返回 `-1`',
                 '示例：`s = "abcdefg", pattern = "bcdffg"` → `1`'],
        quote='若 t 的前缀与 pattern 前缀的最大匹配长度，加上 t 的后缀与 pattern 的后缀的最大匹配长度，再加上 1 之后大于等于 pattern 的长度的话，就说明 t 中必然可以找到合法的 p。',
        quote_src='—— yiduobo 题解原文',
        idea=['确定起点后子串 `t` 就定了；要改的位置 `p` 需要 `t[:p]` 是 pattern 前缀、`t[p+1:]` 是 pattern 后缀',
              '把 `p` 放在前缀匹配长度之后（尽量用满前缀），剩下的看后缀能不能接上',
              '前缀匹配用扩展 KMP（Z）：`pattern + s`；后缀匹配把两个串都反转再求，最后翻回来'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '`pattern` 长度为 1 时直接返回 0（原文单独处理）',
                 '`right` 要先 `[::-1]` 翻回来，取值时下标是 `index + len(pattern) - 1`',
                 'Z 函数里「抄镜像」要看镜像是否超出已知区间，超出的部分要继续比',
                 '对比灵神：灵神用 `pre_z[i] + suf_z[i-1] >= m-1`，yiduobo 用 `left + right + 1 >= m`，是同一个条件'],
    ),
)
