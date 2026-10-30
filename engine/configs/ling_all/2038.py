def _col(S, i, v):
    if 'i0' in S and 'i' in S and S['i0'] <= i < S['i']:
        return 'green' if v == 'A' else 'orange'
    return None


def _txt(S):
    if 'cnt' not in S:
        return ''
    return f"Alice（A）能删的次数：=={S['cnt'][0]}==　　Bob（B）能删的次数：=={S['cnt'][1]}=="


def _grp(S):
    if 'l' in S and S['_line'] in (11, 12) and S.get('c') is not None:
        l = S['l']
        return f"这一段 `{S['c']}` × {l}：两端各留一个，中间能删 `{max(l - 2, 0)}` 个"
    if 'i0' in S and 'i' in S and S['i'] > S['i0'] and S['_line'] in (8, 9, 10):
        return f"这一段 `{S['c']}` 目前长 `{S['i'] - S['i0']}`"
    return ''


CONFIG = dict(
    num=2038, title='如果相邻两个颜色均相同则删除当前颜色', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 + 博弈论（Go 原文转写）',
    tags=['灵神题单·数学算法'],
    code='''
class Solution:
    def winnerOfGame(self, colors: str) -> bool:
        cnt = [0, 0]
        i, n = 0, len(colors)
        while i < n:
            i0 = i
            c = colors[i0]
            while i < n and colors[i] == c:
                i += 1  # 注意这里 i 就是外层循环的 i，所以复杂度是 O(n) 的
            l = i - i0
            if l > 2:
                cnt[ord(c) - ord('A')] += l - 2
        return cnt[0] > cnt[1]
''',
    call='Solution().winnerOfGame("AAAABBBAAB")',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='colors', label='colors（绿 = 当前这段的 A，橙 = 当前这段的 B）', cell=84,
             pointers={'i0': 'blue', 'i': 'pink'}, color=_col),
        dict(type='text', fn=_grp, size=26),
    ],
    watch=[('i', 'i', 'pink'), ('i0', 'i0', 'blue'), ('c', 'c'), ('cnt[0] (A)', 'cnt[0]', 'green'), ('cnt[1] (B)', 'cnt[1]', 'orange')],
    captions={
        'cnt = [0, 0]': '`cnt[0]`、`cnt[1]` 分别是 Alice、Bob 一共能删几次',
        'i, n = 0, len(colors)': '分组循环：一段一段地处理相同颜色',
        'while i < n:': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有一段没处理' if S.i < S.n else f'`i = {S.i} == n`：所有段都处理完了'),
        'i0 = i': '这一段从 `i0 = {i0}` 开始',
        'c = colors[i0]': '这一段的颜色是 `c = {c!r}`',
        'while i < n and colors[i] == c': lambda S, B, r: (
            f'`colors[{S.i}] = {S.colors[S.i]!r}` == `c` → 还是这一段，继续往右' if S.i < S.n and S.colors[S.i] == S.c
            else (f'`i = n`，走到末尾，这一段结束' if S.i >= S.n
                  else f'`colors[{S.i}] = {S.colors[S.i]!r}` ≠ `{S.c!r}` → 这一段结束，`[{S.i0}, {S.i})`')),
        'i += 1': '`i` → `{i}`',
        'l = i - i0': '这一段长 `l = {i} - {i0} = {l}`',
        'if l > 2': lambda S, B, r: (f'`l = {S.l} > 2`：两端的字符不能删，中间的 `{S.l - 2}` 个都能删' if S.l > 2
                                    else f'`l = {S.l} ≤ 2`：每个字符至少有一侧不是同色的邻居 → 一个也删不了'),
        'cnt[ord(c)': '`{c}` 能删的次数加 `l - 2 = {l - 2}`：`cnt[{ord(c) - 65}]` → =={cnt[ord(c) - 65]}==',
        'return cnt[0] > cnt[1]': '`cnt[0] = {cnt[0]}`，`cnt[1] = {cnt[1]}`：Alice 先手，==必须次数更多==才赢 → `{cnt[0] > cnt[1]}`',
    },
    cards=dict(
        one_liner='两人互不影响：谁能删的次数多，谁赢',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`colors` 由 `A`、`B` 组成；Alice 只能删「左右邻居都是 A」的 A，Bob 对 B 同理',
                 'Alice 先手，两端的字符不能删；无法操作的人输',
                 '示例：`"AAABABB"` → `true`；`"AA"` → `false`'],
        quote='对于每一串连续相同的颜色，最边上的两个颜色是不会被删除的。因此删除一种颜色不会对另一种颜色产生任何影响。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一段连续相同颜色，两端不能删，==长为 l 的段能删 l−2 个==',
              '删一个 A 不影响别的段，Alice 和 Bob 各删各的，互不干扰',
              '统计 `cnt[0]`（A 的总次数）和 `cnt[1]`（B 的总次数）：Alice 先手，要次数 ==严格更多==才赢'],
        result='A：`4→2`、`2→0`，共 2 次；B：`3→1`、`2→0`，共 1 次；`2 > 1` → Alice 赢 ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`cnt[c-\'A\']` → `cnt[ord(c) - ord(\'A\')]`，`l := ...; l > 2` 拆成两行）',
                 '时间 `O(n)`，空间 `O(1)`：内外层共用同一个 `i`',
                 '长度 ≤ 2 的段一个也删不了，所以只处理 `l > 2`',
                 '相等时 Alice 输：她先手，先无法操作的人输',
                 '同类题：分组循环模板，参见 1869、1887'],
    ),
)
