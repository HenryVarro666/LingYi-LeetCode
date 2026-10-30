S0 = 'aabc'


def _phase(S):
    ln = S.get('_line', 0)
    if ln <= 13:
        return '一、只含一种字母：分组循环找最长连续相同段'
    if ln <= 32:
        return f'二、只含两种字母：`{S.get("x", "?")}` 记 +1，`{S.get("y", "?")}` 记 −1，找和为 0 的最长段'
    return '三、含三种字母：key = (a−b, b−c) 相同 ⇒ 中间三者个数相等'


def _win(S):
    ln = S.get('_line', 0)
    i = S.get('i')
    if i is None:
        return None
    if ln <= 13:
        return S.get('start')
    return None


def _txt(S):
    ln = S.get('_line', 0)
    ans = S.get('ans')
    return _phase(S) + (f'　当前最长 ==`{ans}`==' if ans is not None else '')


def _hi(S, i, v):
    ln = S.get('_line', 0)
    cur = S.get('i')
    if cur is None:
        return None
    if ln <= 13:
        st = S.get('start')
        return 'blue' if st is not None and st <= i < cur else None
    if ln <= 32:
        x, y = S.get('x'), S.get('y')
        return ('green' if v == x else 'pink' if v == y else None)
    return None


CONFIG = dict(
    num=3714, title='最长的平衡子串 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='分类讨论 + 前缀和哈希表',
    tags=['前缀和与哈希表', '难度分 2202'],
    code='''
class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)

        # 一种字母
        ans = i = 0
        while i < n:
            start = i
            i += 1
            while i < n and s[i] == s[i - 1]:
                i += 1
            ans = max(ans, i - start)

        # 两种字母
        def f(x: str, y: str) -> None:
            nonlocal ans
            i = 0
            while i < n:
                pos = {0: i - 1}  # 前缀和数组的首项是 0，位置相当于在 i-1
                d = 0  # x 的个数减去 y 的个数
                while i < n and (s[i] == x or s[i] == y):
                    d += 1 if s[i] == x else -1
                    if d in pos:
                        ans = max(ans, i - pos[d])
                    else:
                        pos[d] = i
                    i += 1
                i += 1

        f('a', 'b')
        f('a', 'c')
        f('b', 'c')

        # 三种字母
        # 前缀和数组的首项是 0，位置相当于在 -1
        pos = {(0, 0): -1}
        cnt = defaultdict(int)
        for i, b in enumerate(s):
            cnt[b] += 1
            p = (cnt['a'] - cnt['b'], cnt['b'] - cnt['c'])
            if p in pos:
                ans = max(ans, i - pos[p])
            else:
                pos[p] = i
        return ans
''',
    call=f'Solution().longestBalanced({S0!r})',
    expect=3,
    skip=['i += 1', 'd = 0', 'cnt[b] += 1', 'n = len(s)', 'nonlocal ans', 'i = 0', 'ans = i = 0', 'start = i', 'f(\'a\', \'c\')', 'f(\'b\', \'c\')',
          'def f', 'cnt = defaultdict'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前一种字母段，绿/粉 = 两种字母的 +1/−1）', cell=110, h=220,
             pointers={'i': 'blue'}, color=_hi),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='map', var='pos', label='pos（前缀和 → 最早位置）', fmt=lambda k, v: f'{k}: {v}', h=210, font=28),
        dict(type='map', var='cnt', label='cnt（三种字母个数）', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
    ],
    watch=[('i', 'i', 'blue'), ('d', 'd', 'orange'), ('p', 'p', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = max(ans, i - start)': '这一段连续相同字母长 `{i - start}` → `ans = {ans}`',
        'while i < n:': lambda S, B, r: ('分组循环：外层准备一组的起点，内层找这组的终点' if S.get('_line') == 7 else
                                       ('`i` 走到末尾，这一轮结束' if S.get('i', 0) >= S.n else '还有字符，继续')),
        'while i < n and s[i] == s[i - 1]': '`s[{i}]` 和前一个相同吗？相同就并入这一组，`i` 右移',
        'i += 1': '`i` → {i}',
        'pos = {0: i - 1}': '前缀和数组首项 0 的位置是 `i - 1 = {i - 1}`：新的一组从 `i = {i}` 开始',
        'd = 0': '`d` = x 的个数 − y 的个数，一开始 0',
        'while i < n and (s[i] == x': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]!r}` 是 `{S.x}` 或 `{S.y}`：还在这一组里' if S.i < S.n and S.s[S.i] in (S.x, S.y)
                                                      else ('到末尾了，这一组结束' if S.i >= S.n else f'`s[{S.i}] = {S.s[S.i]!r}` 是第三种字母：这一组结束')),
        'd += 1 if': '`{s[i]!r}` 是 `{x if s[i] == x else y}` → `d` 变成 `{d}`',
        'if d in pos': lambda S, B, r: (f'`d = {S.d}` 以前出现过（位置 {S.pos[S.d]}）：中间 x、y 个数相等 → ==可以更新答案==' if S.d in S.pos
                                         else f'`d = {S.d}` 第一次出现，登记位置'),
        'ans = max(ans, i - pos[d])': '长度 `{i} − {pos[d]} = {i - pos[d]}` → `ans = {ans}`',
        'pos[d] = i': '记下 `d = {d}` 最早出现在位置 `{i}`（越早越长）',
        'f(\'a\', \'b\')': '分别对 `(a,b)`、`(a,c)`、`(b,c)` 三对字母各跑一遍',
        'pos = {(0, 0): -1}': '三种字母：key = `(a−b, b−c)`，首项 `(0,0)` 的位置在 -1',
        'cnt[b] += 1': '`{b!r}` 个数加一 → `{dict(cnt)}`',
        'p = (cnt': '`{b!r}` 个数加一 → `{dict(cnt)}`，key `p = (a−b, b−c) = {p}`',
        'if p in pos': lambda S, B, r: (f'`{S.p}` 以前出现过（位置 {S.pos[S.p]}）：这两次之间 a、b、c 个数增量相同 → ==三者相等=='
                                         if S.p in S.pos else f'`{S.p}` 第一次出现，登记位置'),
        'ans = max(ans, i - pos[p])': '长度 `{i} − {pos[p]} = {i - pos[p]}` → `ans = {ans}`',
        'pos[p] = i': '记下 `p = {p}` 最早出现在位置 `{i}`',
        'return ans': '最长平衡子串长度 `{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='分三类：一种、两种、三种字母，后两类用前缀和找最远相等对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串只含 `a`、`b`、`c`；子串里所有出现过的字母次数都相同，就是平衡子串',
                 '求最长平衡子串的长度',
                 '本视频：`s = "aabc"` → `3`（`"abc"`）'],
        quote='设 a 在这个组的个数前缀和数组为 S_a……定义数组 a[i] = (S_a[i] − S_b[i], S_b[i] − S_c[i])，问题变成：计算数组 a 中的一对相等元素的最远距离。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一种字母：==分组循环==，外层找起点，内层找终点',
              '两种字母：被第三种字母切成若干组，每组做 525 题（+1/−1 前缀和）',
              '三种字母：两个等式同时成立，用二元组 `(a−b, b−c)` 当 key'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '前缀和首项 0 的位置要放在组起点前一位（`i - 1`）',
                 '遇到第三种字母就跳过它，`pos`、`d` 重新开始',
                 '同类题：525、1446、560；分组循环是双指针题单里的模板'],
    ),
)
