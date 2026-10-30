def _tc(S, i, j, v):
    ln = S.get('_line', 0)
    I, J = S.get('i'), S.get('j')
    if ln >= 21 and I is not None and J is not None:
        if (i, j) == (I, J):
            return 'yellow'
        if (i, j) == (I + 1, J + 1):
            return 'blue'
    elif I is not None and i == I and ln < 21:
        return 'blue' if j != J else 'yellow'
    return None


def _txt(S):
    ln = S.get('_line', 0)
    s = S.get('s')
    if ln >= 21 and 'actual_lcp' in S:
        return f"验证 `({S['i']},{S['j']})`：实际 LCP = =={S['actual_lcp']}==，输入 `lcp[{S['i']}][{S['j']}]` = {S['lcp'][S['i']][S['j']]}"
    if s is not None and 'c' in S:
        return f"现在填字母 =={S['c']}==：`lcp[i][j] > 0` 的位置和 `s[i]` 相同"
    return '`lcp[i][j] > 0` ⇔ `s[i] == s[j]`'


CONFIG = dict(
    num=2573, title='找出对应 LCP 矩阵的字符串', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='贪心构造 + 验证 LCP',
    tags=['灵神题单', '贪心与思维', '难度分 2682'],
    code='''
class Solution:
    def findTheString(self, lcp: List[List[int]]) -> str:
        n = len(lcp)
        s = [''] * n
        i = 0  # s[i] 没有填字母
        for c in ascii_lowercase:
            for j in range(i, n):
                if lcp[i][j]:  # s[j] == s[i]
                    s[j] = c
            # 找下一个空位
            while i < n and s[i]:
                i += 1
            if i == n:  # 没有空位
                break

        if i < n:  # 还有空位
            return ""

        # 验证 s 是否符合 lcp 矩阵
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # 计算后缀 [i,n-1] 和后缀 [j,n-1] 的实际 LCP
                actual_lcp = 0 if s[i] != s[j] else (1 if i == n - 1 or j == n - 1 else lcp[i + 1][j + 1] + 1)
                if lcp[i][j] != actual_lcp:  # 矛盾
                    return ""
        return ''.join(s)
''',
    call='Solution().findTheString([[3, 0, 1], [0, 2, 0], [1, 0, 1]])',
    setup='from string import ascii_lowercase',
    expect='aba',
    max_steps=90,
    skip=['for j in range(i, n)', 'for j in range(n - 1', 'for i in range(n - 1'],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='table', var='lcp', label='lcp（黄 = 当前格，蓝 = 依赖的格子）', cell=84, h=300, color=_tc),
        dict(type='array', var='s', label='s（空串 = 还没填）', cell=84, h=200,
             color=lambda S, k, v: 'green' if v else None),
    ],
    watch=['i', 'j', 'c', 'actual_lcp'],
    captions={
        's = [': '`s` 先放 `n = {n}` 个空位',
        'i = 0': '`i` 指向第一个还没填字母的位置',
        'for c in ascii_lowercase': '依次尝试字母 `{c}`：每个新字母填在第一个空位 `s[{i}]` 上，字典序最小',
        'if lcp[i][j]:': lambda S, B, r: (f'`lcp[{S.i}][{S.j}] = {S.lcp[S.i][S.j]} > 0` → `s[{S.j}]` 和 `s[{S.i}]` 相同，填 `{S.c}`'
                                         if S.lcp[S.i][S.j] else
                                         f'`lcp[{S.i}][{S.j}] = 0` → 两个后缀首字母不同，`s[{S.j}]` 不能是 `{S.c}`'),
        's[j] = c': '`s[{j}] = {c}` → {s}',
        'while i < n and s[i]': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]!r}` 已填，`i` 右移' if S.i < len(S.s) and S.s[S.i]
                                                 else f'`i = {S.i}`：找到下一个空位'),
        'if i == n:': lambda S, B, r: ('`i == n`：没有空位，所有位置填完，退出字母循环' if S.i == len(S.s)
                                      else f'`i = {S.i} < n`：还有空位，换下一个字母'),
        'if i < n:': lambda S, B, r: ('填完了，没有空位' if S.i >= len(S.lcp)
                                     else '26 个字母用完还有空位 → 无解，返回空串'),
        23: lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]} ≠ s[{S.j}] = {S.s[S.j]}` → 实际 LCP = 0' if S.s[S.i] != S.s[S.j]
                                          else (f'字母相同且到了末尾 → 实际 LCP = 1' if S.i == len(S.s) - 1 or S.j == len(S.s) - 1
                                                else f'字母相同 → `lcp[{S.i + 1}][{S.j + 1}] + 1` = =={S.actual_lcp}==')),
        24: lambda S, B, r: (f'`lcp[{S.i}][{S.j}] = {S.lcp[S.i][S.j]}` 和实际 `{S.actual_lcp}` ' +
                                                       ('不一致 → 矛盾，返回空串' if S.lcp[S.i][S.j] != S.actual_lcp else '一致，继续')),
        "return ''.join(s)": '全部格子都对得上 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='第一个空位填最小字母，再用 lcp 验证',
        complexity='时间 `O(n²)`，空间 `O(1)`（返回值不计入）',
        problem=['`lcp[i][j]` 是后缀 `word[i:]` 与 `word[j:]` 的最长公共前缀长度',
                 '给定 `n×n` 的 `lcp`，返回对应的字典序最小的字符串，没有则返回空串',
                 '本视频：`lcp = [[3,0,1],[0,2,0],[1,0,1]]` → `"aba"`'],
        quote='找到第一个没有填入字母的位置 i，为了让 s 的字典序尽量小，s[i] 填 b 是最优的。同理，所有满足 lcp[i][j]>0 的 s[j] 都一定是 b。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`lcp[i][j] > 0` 当且仅当 `s[i] == s[j]`',
              '依次填 a、b、c…：每次填在第一个空位，以及与它 lcp 非零的位置',
              '只访问了至多 26 行，所以最后必须用 DP 公式重算整张 lcp 来验证'],
        summary=['时间 `O(n²)`，空间 `O(1)`',
                 '易错：构造完必须验证，只看了至多 26 行，其余行可能矛盾',
                 '验证公式：字母不同 → 0；相同 → `lcp[i+1][j+1] + 1`，边界为 1',
                 '用了 `string.ascii_lowercase`，在 `setup` 里补了 `import`',
                 '同类题：字符串题单「Z 函数」、贪心题单「字典序最小」'],
    ),
)
