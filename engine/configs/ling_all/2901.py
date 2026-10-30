def _dec(h):
    out = ''
    while h:
        c = h & 31
        out += '?' if c == 31 else chr(96 + c)
        h >>= 5
    return out


def _fmt(k, v):
    mf, j, mf2, j2 = v
    return f'{_dec(k)} → 最长 {mf}（来自 {j}）｜次长 {mf2}（来自 {j2}）'


CONFIG = dict(
    num=2901, title='最长相邻不相等子序列 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='值域 DP：通配符哈希 + 维护最大次大',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1899'],
    code='''
class Solution:
    def getWordsInLongestSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        n = len(words)
        f_map = {}  # 哈希值 -> (max_f, j, max_f2, j2)
        from_ = [0] * n
        global_max_f = max_i = 0
        for i in range(n - 1, -1, -1):
            w, g = words[i], groups[i]

            # 计算 w 的哈希值
            hash_val = sum((ord(ch) & 31) << (k * 5) for k, ch in enumerate(w))

            f = 0  # 方法一中的 f[i]
            for k in range(len(w)):
                h = hash_val | (31 << (k * 5))  # 用记号笔把 w[k] 涂黑（置为 11111）
                max_f, j, max_f2, j2 = f_map.get(h, (0, 0, 0, 0))
                if g != groups[j]:  # 可以从最大值转移过来
                    if max_f > f:
                        f = max_f
                        from_[i] = j
                else:  # 只能从次大值转移过来
                    if max_f2 > f:
                        f = max_f2
                        from_[i] = j2

            f += 1
            if f > global_max_f:
                global_max_f, max_i = f, i

            # 用 f 更新 f_map[h] 的最大次大
            # 注意要保证最大次大的 group 值不同
            for k in range(len(w)):
                h = hash_val | (31 << (k * 5))
                max_f, j, max_f2, j2 = f_map.get(h, (0, 0, 0, 0))
                if f > max_f:  # 最大值需要更新
                    if g != groups[j]:
                        max_f2, j2 = max_f, j  # 旧最大值变成次大值
                    max_f, j = f, i
                elif f > max_f2 and g != groups[j]:  # 次大值需要更新
                    max_f2, j2 = f, i
                f_map[h] = (max_f, j, max_f2, j2)

        ans = [''] * global_max_f
        i = max_i
        for k in range(global_max_f):
            ans[k] = words[i]
            i = from_[i]
        return ans
''',
    call="Solution().getWordsInLongestSubsequence(['ab','aa','ba'], [1,2,1])",
    expect=['ab', 'aa', 'ba'],
    skip=['n = len', 'from_ = [0]', 'global_max_f = max_i', 'w, g = words', 'for k in range(len(w))', 'max_f, j, max_f2, j2 = f_map.get', 'ans = [', 'else:  #', 13, 33, 36, 41, 20, 28, 44, 45],
    max_steps=120,
    views=[
        dict(type='text', size=25, h=60, fn=lambda S: (
            f"当前单词 `{S['w']}`（组 {S['g']}）：把每一位涂成 `?`，查哈希表里等于它的「邻居」" if 'w' in S and 'f' in S and S.get('_line', 0) < 30 else
            ('用算出的 `f` 更新这几个通配符键的最大 / 次大' if 'w' in S and S.get('_line', 0) >= 30 else '倒着遍历 `words`；`?` 通配符：`a?` 同时代表 `aa`、`ab`…'))),
        dict(type='array', var='words', label='words（倒着遍历）', h=180, cell=90, pointers={'i': 'blue'},
             color=lambda S, k, v: 'yellow' if k == S.get('i') else None),
        dict(type='array', var='from_', label='from_（最优转移来源）', h=170, cell=90),
        dict(type='map', var='f_map', label='f_map：通配符串 → (最大, 来源, 次大, 来源)', h=260, fmt=_fmt, font=24),
    ],
    watch=['i', 'w', 'g', ('f', 'f', 'green'), ('global_max_f', 'global_max_f', 'green'), 'k'],
    captions={
        'f_map = {}': '`f_map`：以「带通配符的字符串」为键，记最长长度和次长长度（两者 group 不同）',
        'for i in range(n - 1': lambda S, B, r: ('`words` 倒着扫完了，开始按 `from_` 还原方案' if 'i' in B and B.i == S.i else f'倒着处理 `words[{S.i}] = {S.words[S.i]!r}`（组 {S.groups[S.i]}）'),
        'hash_val = sum': '把 `{w}` 压成哈希：每个字母 5 位 → `{hash_val}`',
        15: lambda S, B, r: f'把 `{S.w}` 的第 {S.k} 位涂黑成 `?` → `{_dec(S.h)}`，看表里有没有它',
        17: lambda S, B, r: (f"表里还没有 `{_dec(S.h)}`（最大值 0）→ 没有可转移的来源" if S.max_f == 0 else f"哈希表里 `{_dec(S.h)}` 的最大值来自下标 {S.j}（组 {S.groups[S.j]}），与当前组 {S.g} 不同 → ==可以接最大值==" if S.g != S.groups[S.j] else f"最大值的组 {S.groups[S.j]} 与当前组相同 → ==只能接次大值=="),
        'if max_f > f': '最大值 `{max_f}` {"大于" if max_f > f else "不大于"}当前 `f = {f}`',
        'f = max_f': '更新 `f = {f}`，来源 `from_[{i}] = {j}`',
        'if max_f2 > f': '次大值 `{max_f2}` {"大于" if max_f2 > f else "不大于"}当前 `f = {f}`',
        'f = max_f2': '更新 `f = {f}`，来源 `from_[{i}] = {j2}`',
        'f += 1': '加上 `{w}` 自己：`f = {f}`',
        'if f > global_max_f': lambda S, B, r: (f"`f = {S.f}` > 全局最大 `{S.global_max_f}` → 更新答案的起点" if S.f > S.global_max_f else f"`f = {S.f}` 不超过全局最大 `{S.global_max_f}`"),
        'global_max_f, max_i': '`global_max_f = {global_max_f}`，起点 `max_i = {max_i}`（后面从它出发还原方案）',
        'if f > max_f': lambda S, B, r: (f"涂黑第 {S.k} 位得 `{_dec(S.h)}`：`f = {S.f}` > 最大值 `{S.max_f}` → ==新的最大值==" + ('，旧最大值（组不同）降为次大' if S.g != S.groups[S.j] else '，旧最大值与它同组，直接丢弃') if S.f > S.max_f else f"涂黑第 {S.k} 位得 `{_dec(S.h)}`：`f = {S.f}` 不超过最大值 `{S.max_f}`，看能否更新次大"),
        'max_f2, j2 = max_f, j': '旧最大值降为次大：`({max_f2}, {j2})`',
        'max_f, j = f, i': lambda S, B, r: f'最大值换成 `({S.max_f}, {S.j})`，写回 `f_map[{_dec(S.h)}]`',
        'elif f > max_f2': lambda S, B, r: (f"`f = {S.f}` > 次大 `{S.max_f2}` 且组与最大值不同 → 更新次大" if S.f > S.max_f2 and S.g != S.groups[S.j] else '不满足次大的更新条件，保持不变'),
        'max_f2, j2 = f, i': lambda S, B, r: f'次大值换成 `({S.max_f2}, {S.j2})`，写回 `f_map[{_dec(S.h)}]`',
        'for k in range(global_max_f)': '沿着 `from_` 往后走，还原方案',
        'ans[k] = words[i]': '第 {k+1} 个：`{words[i]!r}`，再沿 `from_[{i}] = {from_[i]}` 找下一个',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='把汉明距离 1 变成「通配符相等」，一个字符串只查 l 个键',
        complexity='时间 `O(n·l)`，空间 `O(n·l)`',
        problem=['从 `words` 选最长子序列：相邻的 `groups` 不同，且单词等长、汉明距离恰为 1，输出方案',
                 '示例：`words=["bab","dab","cab"], groups=[1,2,2]` → `["bab","cab"]`',
                 '本视频：`["ab","aa","ba"], [1,2,1]` → `["ab","aa","ba"]`'],
        quote='反过来，枚举哪个字母不同。……与 w 只有一个字母不同的字符串，本质只有 10 种。关键思路：我们只需枚举这 10 种字符串，而不是 O(n) 个字符串！',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `bab` 看成 `?ab`、`b?b`、`ba?`：两个单词汉明距离为 1，当且仅当有一个通配符串相等',
              '倒着遍历，`f_map[通配符串]` 记以该串开头的最长长度，从子序列第二个字符串转移',
              '再加 `groups` 约束：每个键同时记最大与次大，并保证两者 group 不同'],
        summary=['时间 `O(n·l)`，空间 `O(n·l)`；方法一枚举下标是 `O(n²·l)`',
                 '每个字母占 5 位（`ord(ch) & 31`），`?` 记为 31，完美哈希',
                 '易错：最大值与当前 group 相同时只能接次大值；更新次大值要求与最大值 group 不同',
                 '只显示了方法二（值域 DP）；方法一是 `f[i] = 1 + max f[j]` 的 `O(n²)` 枚举，并用 `from_` 还原方案'],
    ),
)
