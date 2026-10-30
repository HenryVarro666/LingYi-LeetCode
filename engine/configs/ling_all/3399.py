from bisect import bisect_left as _bl

S0 = '00011'
OPS = 1


def _chk(m):
    n = len(S0)
    if m == 1:
        c = sum((ord(b) ^ i) & 1 for i, b in enumerate(S0))
        c = min(c, n - c)
    else:
        c = sum(len(list(t)) // (m + 1) for _, t in __import__('itertools').groupby(S0))
    return c <= OPS


_SEQ = []
_bl(range(len(S0)), True, 1, key=lambda m: (_SEQ.append((m, _chk(m))), _chk(m))[1])


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
    m = S.get('m')
    live = m is not None and 'cnt' in S
    cv.text((x0 + 18, y0 + 4), 's（黄点 = 要翻转的位置）' if not (live and m == 1) else 's 与目标 0101…（红 = 要翻转）', 24, T['muted'], bold=True)
    i_cur = S.get('i') if live and m != 1 and line >= 14 else None
    runs = _runs()
    for idx, ch in enumerate(S0):
        X = sx + idx * cell
        col = T['blue'] if S0[idx] == '0' else T['purple']
        cv.rect((X + 3, top, X + cell - 3, top + cell - 6), fill=col, r=8, alpha=210)
        cv.text((X + cell / 2, top + (cell - 6) / 2), ch, 38, T['bg'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, top + cell + 2), idx, 18, T['dim'], anchor='mt', mono=True)
    if live and m != 1 and line >= 14:
        for (a, b) in runs:
            L = b - a + 1
            done = b < i_cur or (b == i_cur and line >= 18)
            active = a <= i_cur <= b
            yb = top + cell + 34
            cv.rect((sx + a * cell + 4, yb, sx + (b + 1) * cell - 4, yb + 8), fill=T['yellow'] if active else (90, 98, 110), r=4)
            if done:
                c = L // (m + 1)
                cv.text((sx + (a + b + 1) * cell / 2, yb + 18), f'{L} // {m + 1} = {c}', 24, T['green'] if c else T['muted'], anchor='mt', bold=True, mono=True)
                for j in range(1, c + 1):
                    off = j * (m + 1) - 1
                    if off == L - 1:
                        off -= 1
                    px = sx + (a + off) * cell + cell / 2
                    cv.rect((px - 10, top - 26, px + 10, top - 6), fill=T['yellow'], r=10)
        X = sx + i_cur * cell + cell / 2
        cv.tri_up(X, top + cell + 22, 9, T['cyan'])
    if live and m == 1 and line >= 9:
        for idx, ch in enumerate(S0):
            X = sx + idx * cell
            tgt = str(idx % 2)
            bad = tgt != ch
            cv.rect((X + 10, top + cell + 34, X + cell - 10, top + cell + 34 + 46), fill=T['red'] if bad else (60, 68, 80), r=6)
            cv.text((X + cell / 2, top + cell + 34 + 23), tgt, 30, T['text'], anchor='mm', bold=True, mono=True)
        if line >= 9:
            c = S['cnt']
            cv.text((x0 + 30, top + cell + 110), f'改成 0101…：红格 `{c if line < 11 else B.get("cnt", c)}` 个' if False else '改成 0101…：红格个数 = cnt；改成 1010… 要改 n − cnt 个', 24, T['muted'])


def _cand_color(S, i, v):
    m = S.get('m')
    seen = {}
    for mm, r in _SEQ:
        if mm == m:
            if S.get('_line', 0) >= 20:
                seen[mm] = r
            break
        seen[mm] = r
    if i in seen:
        return 'green' if seen[i] else 'red'
    return None


def _top(S):
    m = S.get('m')
    line = S.get('_line', 0)
    if m is None:
        return '最小化「最长相同子串」→ ==二分上界 m==：每段至多 m 长，要改几次？'
    if m == 1:
        return f'`m = 1` 特判：只能是 `0101…` 或 `1010…`，要改 `min(cnt, n − cnt)` 次，限额 `{OPS}`'
    return f"每段连续相同子串切成 ≤ `{m}` 长：每 `{m + 1}` 个字符改一个，累计 `cnt = {S.get('cnt', 0)}`，限额 `{OPS}`"


def _run_end(S, B, ret):
    if S.i == len(S0) - 1:
        return f'`i = {S.i}` 是最后一个字符 → 一段结束，长度 `k = {S.k}`'
    if S.b != S0[S.i + 1]:
        return f"`s[{S.i}] = '{S.b}'` ≠ `s[{S.i + 1}] = '{S0[S.i + 1]}'` → 一段结束，长度 `k = {S.k}`"
    return f"`s[{S.i}] = s[{S.i + 1}] = '{S.b}'` → 这段还没结束，继续"


def _ret(S, B, ret):
    if ret is True:
        return f'`cnt = {S.cnt} <= numOps = {S.numOps}` → ==m = {S.m} 可行=='
    if ret is False:
        return f'`cnt = {S.cnt} > numOps = {S.numOps}` → ==m = {S.m} 不行==，改的次数超了'
    return None


CONFIG = dict(
    num=3399, title='字符相同的最短子字符串 II', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 切香肠',
    tags=['灵神题单·二分算法', '灵神题单·常用数据结构', '难度分 2376'],
    code='''
class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        def check(m: int) -> bool:
            cnt = 0
            if m == 1:
                # 改成 0101...
                # 如果 s[i] 和 i 的奇偶性不同，cnt 加一
                cnt = sum((ord(b) ^ i) & 1 for i, b in enumerate(s))
                # n-cnt 表示改成 1010...
                cnt = min(cnt, n - cnt)
            else:
                k = 0
                for i, b in enumerate(s):
                    k += 1
                    # 到达连续相同子串的末尾
                    if i == n - 1 or b != s[i + 1]:
                        cnt += k // (m + 1)
                        k = 0
            return cnt <= numOps
        return bisect_left(range(n), True, 1, key=check)
''',
    call=f"Solution().minLength('{S0}', {OPS})",
    expect=2,
    views=[
        dict(type='text', fn=_top, size=25, h=90),
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=lambda S: list(range(len(S0))), label='二分猜的 m（绿 = 可行，红 = 不行）',
             cell=70, color=_cand_color, pointers={'m': 'yellow'}, h=190),
    ],
    watch=[('m', 'm', 'yellow'), ('cnt', 'cnt', 'cyan'), ('k', 'k', 'orange'), ('numOps', 'numOps', 'green')],
    captions={
        3: '`n = {n}`',
        'return bisect_left': '在 `[1, n)` 里二分，找==最小的 m==使 `check(m)` 为 True（`check` 有单调性）',
        5: '`cnt` 记录要翻转的次数',
        6: lambda S, B, r: ('`m == 1` ==特判==：切成 1 长就是相邻必须不同，只能是 0101… 或 1010…' if S.m == 1
                           else f'`m = {S.m} != 1` → 走「切香肠」公式'),
        9: '改成 `0101…`：`s[i]` 与 `i` 奇偶不同就要翻转 → `cnt = {cnt}`',
        11: '改成 `1010…` 要翻转 `n - cnt` 个，两者取小：`cnt = min({B.cnt}, {n} - {B.cnt}) = {cnt}`',
        13: '`k` 统计当前连续相同子串的长度',
        14: lambda S, B, r: ('`s` 遍历完了 → 去 `return`' if B.get('i') == S.i == len(S0) - 1 and B.get('k') == 0 else f"遍历 `s[{S.i}] = {S.b!r}`"),
        15: '`k = {k}`：当前这段已有 `{k}` 个字符',
        17: _run_end,
        18: '切香肠：每 `{m} + 1 = {m + 1}` 个字符改 1 个 → `cnt += {k} // {m + 1} = {k // (m + 1)}` → `cnt = {cnt}`',
        19: '这段处理完，`k` 清零重新数',
        'return cnt <=': _ret,
    },
    cards=dict(
        one_liner='最小化最大值 → 二分 m；每段长 L 要改 L // (m+1) 次',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['二进制串 `s`，最多翻转 `numOps` 个字符，使最长的==相同子串==尽量短',
                 '示例：`s = "000001", numOps = 1` → `2`（改成 `001001`）',
                 '本视频：`s = "00011", numOps = 1` → `2`'],
        quote='好比切香肠，既然每一段至多为 m，那么就每隔 m 个字符操作一次（切一刀）。相当于每有 m+1 个字符，就要操作一次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m` 越大越容易做到 → 有单调性，==二分长度上界 m==',
              '一段长 `L` 的相同子串：每 `m+1` 个字符改一个，共 `L // (m+1)` 次',
              '`m = 1` 要特判：只能变成 `0101…` 或 `1010…`，取翻转次数较少的'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`m = 1` 不能套公式：改倒数第二个字符会让相邻段变长',
                 '`bisect_left(range(n), True, 1, key=check)`：左端点 1 表示长度不能为 0',
                 '另有 groupby 写法、最大堆写法（先特判答案为 1）和 O(n) 的分桶优化，思路见题解']
    ),
)
