S0 = '00011'
OPS = 1


def _runs():
    out, i = [], 0
    while i < len(S0):
        j = i
        while j + 1 < len(S0) and S0[j + 1] == S0[i]:
            j += 1
        out.append((i, j))
        i = j + 1
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S0)
    cell = min(96, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 110
    line = S.get('_line', 0)
    phase1 = 7 <= line <= 13 and 'index' in S
    phase2 = 'mid' in S and 'p' in S and 22 <= line <= 31
    cv.text((x0 + 18, y0 + 4), ('s：统计「改成 0101…」要翻转几个（红 = 要翻转）' if phase1 else 's（黄点 = 要翻转的位置）'), 24, T['muted'], bold=True)
    for idx, ch in enumerate(S0):
        X = sx + idx * cell
        col = T['blue'] if ch == '0' else T['purple']
        cv.rect((X + 3, top, X + cell - 3, top + cell - 6), fill=col, r=8, alpha=210)
        cv.text((X + cell / 2, top + (cell - 6) / 2), ch, 38, T['bg'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, top + cell + 2), idx, 18, T['dim'], anchor='mt', mono=True)
    if phase1:
        for idx, ch in enumerate(S0):
            if idx > S['index'] or (idx == S['index'] and line < 9):
                continue
            X = sx + idx * cell
            bad = str(idx % 2) != ch
            cv.rect((X + 10, top + cell + 34, X + cell - 10, top + cell + 80), fill=T['red'] if bad else (60, 68, 80), r=6)
            cv.text((X + cell / 2, top + cell + 57), str(idx % 2), 30, T['text'], anchor='mm', bold=True, mono=True)
    if phase2:
        mid, p = S['mid'], S['p']
        q = S.get('q', p + 1) if line >= 25 else None
        for (a, b) in _runs():
            L = b - a + 1
            done = b < p or (b == p - 1)
            cur = line >= 25 and a == p
            yb = top + cell + 34
            if done or cur:
                cv.rect((sx + a * cell + 4, yb, sx + (b + 1) * cell - 4, yb + 8), fill=T['yellow'] if cur else (90, 98, 110), r=4)
            if done or (cur and line >= 30):
                c = L // (mid + 1)
                cv.text((sx + (a + b + 1) * cell / 2, yb + 18), f'{L} // {mid + 1} = {c}', 24, T['green'] if c else T['muted'], anchor='mt', bold=True, mono=True)
                for j in range(1, c + 1):
                    off = j * (mid + 1) - 1
                    if off == L - 1:
                        off -= 1
                    px = sx + (a + off) * cell + cell / 2
                    cv.rect((px - 10, top - 26, px + 10, top - 6), fill=T['yellow'], r=10)
        X = sx + p * cell + cell / 2
        cv.tri_up(X, top + cell + 22, 9, T['blue'])
        cv.text((X, top + cell + 50), 'p', 22, T['blue'], anchor='mt', bold=True)
        if q is not None and q < n:
            X = sx + q * cell + cell / 2
            cv.tri_up(X, top + cell + 22, 9, T['pink'])
            cv.text((X, top + cell + 50), 'q', 22, T['pink'], anchor='mt', bold=True)


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i < S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _top(S):
    line = S.get('_line', 0)
    if 'left' not in S:
        if 'index' in S:
            return f"先特判答案为 1：翻成 `0101…` 要 `cnt1 = {S.get('cnt1', 0)}` 个，翻成 `1010…` 要 `cnt2 = {S.get('cnt2', 0)}` 个，限额 `{OPS}`"
        return '最小化最长相同子串 → ==二分答案 mid==，先特判答案为 1'
    if 'mid' in S and 22 <= line <= 31:
        return f"试 `mid = {S['mid']}`：每个连续段长 `length` 要 `length // ({S['mid']} + 1)` 次，累计 `cnt = {S.get('cnt', 0)}`"
    return f"答案在闭区间 `[{S['left']}, {S['right']}]`"


def _inner_cond(S, B, ret):
    if S.q < len(S0) and S0[S.q] == S0[S.p]:
        return f"`q = {S.q}`：`s[{S.q}] = s[{S.p}] = '{S0[S.p]}'` → 同一段，`q` 继续右移"
    if S.q >= len(S0):
        return f'`q = {S.q} == len(s)` → 这段到头了'
    return f"`s[{S.q}] = '{S0[S.q]}'` ≠ `s[{S.p}] = '{S0[S.p]}'` → 这段结束于 `q - 1`"


CONFIG = dict(
    num=3399, title='字符相同的最短子字符串 II', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 先特判 1',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 2376'],
    code='''
class Solution(object):
    def minLength(self, s, numOps):
        
        cnt1 = 0
        cnt2 = 0

        for index, char in enumerate(s):
            if index % 2 == 0:
                cnt1 += int(char)
                cnt2 += 1 - int(char)
            else:
                cnt1 += 1 - int(char)
                cnt2 += int(char)
        
        if min(cnt1, cnt2) <= numOps:
            return 1
        
        left = 2
        right = len(s)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            p = 0
            while p < len(s):
                q = p + 1
                while q < len(s) and s[q] == s[p]:
                    q += 1
                
                length = q - p
                cnt += length // (mid + 1)
                p = q

            if cnt <= numOps:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call=f"Solution().minLength('{S0}', {OPS})",
    expect=2,
    views=[
        dict(type='text', fn=_top, size=25, h=90),
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=lambda S: list(range(len(S0) + 1)), label='候选答案 mid（红 = 已排除，绿 = 可行）',
             cell=70, color=_color, pointers={'left': 'blue', 'mid': 'yellow', 'right': 'green'}, h=190),
    ],
    watch=[('cnt1', 'cnt1', 'red'), ('cnt2', 'cnt2', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'green'),
           ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan')],
    skip=['cnt2 = 0', '            cnt = 0', '            p = 0'],
    max_steps=95,
    captions={
        'cnt1 = 0': '`cnt1`：改成 `0101…` 需要翻转的个数；`cnt2` 是改成 `1010…` 的（二者之和 = n）',
        'for index, char': lambda S, B, r: ('`s` 遍历完了' if B.get('index') == S.index == len(S0) - 1 and B.get('cnt1') == S.cnt1 and 'cnt2' in B and B['cnt2'] == S.cnt2 else f'看下标 `{S.index}`，字符 `{S.char}`'),
        'if index % 2': lambda S, B, r: (f"下标 `{S.index}` 是{'偶' if S.index % 2 == 0 else '奇'}数位"),
        'cnt1 += int(char)': '偶数位上的 `1` 要翻成 `0`：`cnt1 += {char}` → `cnt1 = {cnt1}`',
        'cnt2 += 1 - int(char)': '偶数位上的 `0` 要翻成 `1`（对 `1010…`）：`cnt2 = {cnt2}`',
        'cnt1 += 1 - int(char)': '奇数位上的 `0` 要翻成 `1`：`cnt1 += {1 - int(char)}` → `cnt1 = {cnt1}`',
        'cnt2 += int(char)': '奇数位上的 `1` 要翻成 `0`（对 `1010…`）：`cnt2 = {cnt2}`',
        'if min(cnt1, cnt2)': lambda S, B, r: (f'`min({S.cnt1}, {S.cnt2}) = {min(S.cnt1, S.cnt2)} <= {S.numOps}` → 可以交替，答案 1' if min(S.cnt1, S.cnt2) <= S.numOps
                                                else f'`min({S.cnt1}, {S.cnt2}) = {min(S.cnt1, S.cnt2)} > {S.numOps}` → ==做不到 1==，答案至少是 2，接着二分'),
        'left = 2': '`left = 2`：答案 1 已排除，从 2 开始',
        'right = len': '`right = len(s) = {right}`：不操作也满足',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}` → 继续二分' if S.left < S.right
                                              else f'`left == right = {S.left}` → 结束'),
        'mid = (left': '`mid = ({left} + {right}) // 2 = {mid}`：试==最长相同子串不超过 mid==行不行',
        'cnt = 0': '`cnt`：需要的翻转总数',
        'p = 0': '`p` 指向当前这段的起点',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p}`，还有新的一段' if S.p < len(S0) else f'`p = {S.p} == len(s)` → 所有段都算完'),
        'q = p + 1': '`q` 从 `p + 1` 往右找这段的结尾',
        'while q < len(s) and': _inner_cond,
        'q += 1': '`q` → {q}',
        'length = q - p': '这一段长 `length = {q} - {p} = {length}`',
        'cnt += length': '每 `{mid} + 1 = {mid + 1}` 个字符翻一个：`cnt += {length} // {mid + 1} = {length // (mid + 1)}` → `cnt = {cnt}`',
        'p = q': '`p = {p}`：跳到下一段',
        'if cnt <= numOps': lambda S, B, r: (f'`cnt = {S.cnt} <= {S.numOps}` → `mid = {S.mid}` 够用，答案 ==不超过 mid=='
                                              if S.cnt <= S.numOps else f'`cnt = {S.cnt} > {S.numOps}` → `mid = {S.mid}` 不够，答案 ==大于 mid=='),
        'right = mid': '`right = {right}`：`mid` 可行，上界收到 `mid`',
        'left = mid + 1': '`left = {left}`：`mid` 不行，下界抬到 `mid + 1`',
        'return left': '`left == right` → 最短的最长相同子串 =={ret}==',
    },
    cards=dict(
        one_liner='二分「最长相同子串」mid：每段切成每 mid+1 个翻一个',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['二进制串 `s`，最多翻转 `numOps` 个字符，使最长的==相同子串==尽量短',
                 '示例：`s = "000001", numOps = 1` → `2`',
                 '本视频：`s = "00011", numOps = 1` → `2`'],
        quote='将mid + 1个字符一组切分，包含mid个相同字符，然后紧接着1个翻转后的字符。这样一来，经过length // (mid + 1)次操作就可以保证相同子串的长度都不超过mid。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小化最大值 → 二分答案 `mid`，判断翻转次数是否 `<= numOps`',
              '`mid = 1` 切法会和相邻段粘连 → ==先单独特判==：只能是 `0101…` 或 `1010…`',
              '特判不过再二分，`left` 从 2 起；用 `p`、`q` 两个指针分出每个连续段'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`mid = 1` 必须在二分前特判（`cnt1`、`cnt2` 取小），否则公式会出错',
                 '`p`、`q` 双指针分段：`q` 停在下一段的第一个字符，下一轮 `p = q`',
                 '对比灵神：灵神把 `m == 1` 特判放进 `check`，这里放在二分之前',
                 '原文已是 Python 3 可运行，没有改动'],
    ),
)
