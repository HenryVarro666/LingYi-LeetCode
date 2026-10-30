def _s_ptr(S):
    i = S['_inner'].get('i')
    return i if isinstance(i, int) and 0 <= i < len(S['s']) else None


def _seq(S):
    return S['_inner'].get('seq')


CONFIG = dict(
    num=2014, title='重复 K 次的最长子序列', difficulty='Hard', category='二叉树与回溯',
    author='灵茶山艾府', technique='枚举排列 + 子序列自动机',
    tags=['回溯', '字符串', '难度分 2558'],
    code='''
class Solution:
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        s = [ord(c) - ord('a') for c in s]  # 转成 0 到 25，这样下面无需频繁调用 ord

        # 392. 判断子序列（进阶做法）
        n = len(s)
        nxt = [[n] * 26 for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            nxt[i][:] = nxt[i + 1]
            nxt[i][s[i]] = i

        def isSubsequence(seq: Tuple[int, ...]) -> bool:
            i = -1
            for _ in range(k):
                for c in seq:
                    i = nxt[i + 1][c]
                    if i == n:  # c 不在 s 中，说明 seq*k 不是 s 的子序列
                        return False
            return True  # seq*k 是 s 的子序列

        cnt = Counter(s)
        a = [ch for ch, freq in cnt.items() for _ in range(freq // k)]
        a.sort(reverse=True)  # 排序后，下面会按照字典序从大到小枚举排列

        for i in range(len(a), 0, -1):  # 长的优先
            for seq in permutations(a, i):  # 枚举 a 的长为 i 的排列
                if isSubsequence(seq):  # seq*k 是 s 的子序列
                    return ''.join(ascii_lowercase[c] for c in seq)
        return ''
''',
    call="Solution().longestSubsequenceRepeatedK('abcabcab', 2)",
    expect='cab',
    views=[
        dict(type='array', var='s', label='s（a=0, b=1, c=2）', cell=56, h=175, pointers={_s_ptr: 'blue'}, pointer_labels={_s_ptr: 'i'}),
        dict(type='table', var=lambda S: [r[:3] for r in S['nxt']] if 'nxt' in S else None,
             label='nxt[i][c]：从 i 起字母 c 第一次出现的下标（8 = 没有）', cols=['a', 'b', 'c'], rows=list(range(9)), h=330, cell=84),
        dict(type='array', var='a', label='a：每个字母可出现 freq//k 次，降序', cell=56, h=125),
        dict(type='array', var=_seq, label='当前枚举的 seq（重复 k 次去匹配 s）', cell=56, h=125),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('c', lambda S: S['_inner'].get('c'), 'pink'), 'k', 'n'],
    skip=['nxt[i][:] = nxt[i + 1]', 'for i in range(n - 1', 'for _ in range(k)', 'for c in seq', 'cnt = Counter', 'n = len(s)'],
    captions={
        's = [ord': '字母转成 0..25：`{s}`',
        'nxt = [[n]': '`nxt[i][c]` 表示 ==从下标 i 开始，字母 c 第一次出现的位置==；初始全是 `n = {n}`（没有）',
        'nxt[i][s[i]] = i': '倒着建表：先抄 `nxt[{i}+1]`，再把自己这个字母 `{s[i]}` 改成 `{i}`',
        'i = -1': '`i = -1`：从 s 开头开始匹配，`nxt[i+1]` 就是 `nxt[0]`',
        'i = nxt[i + 1][c]': '要匹配字母 `{c}`：查 `nxt[{B.i}+1][{c}]` = `{i}`，一步跳到下一次出现的位置',
        'if i == n': lambda S, B, ret: (
            f'`i == n = {S.n}`：后面再没有字母 `{S.c}` → ==seq*k 不是子序列== → False' if S.i == S.n
            else f'`i = {S.i} != n`：匹配上了 `s[{S.i}]`，继续匹配下一个字母'),
        'return False': '这个 seq 不行，换下一个排列',
        'return True': '`seq` 重复 `{k}` 次全部匹配上 → ==是子序列==',
        'cnt = Counter': '统计每个字母出现次数',
        'a = [ch': '字母出现 `freq` 次，seq 里最多放 `freq // k` 个：`a = {a}`（回忆 47 题：带重复元素的排列）',
        'a.sort(reverse=True)': '降序排列：这样 permutations 先枚举到的就是==字典序最大==的排列 → `{a}`',
        'for i in range(len(a)': '先试最长的长度 `{i}`：长的优先',
        'for seq in permutations': '枚举 a 的长为 `{i}` 的排列：`seq = {seq}`',
        'if isSubsequence(seq)': '用自动机判断 `seq * {k}` 是不是 s 的子序列：`{seq}` 重复 {k} 次，逐个字母查表跳转',
        "return ''.join": '把下标转回字母，答案是 `{ret!r}`',
        "return ''\n": '所有排列都不行 → 返回空串',
    },
    max_steps=100,
    cards=dict(
        one_liner='n < 8k 保证至多 7 个字母可用，枚举排列 + 自动机判断',
        complexity='时间 `O((n/k)!·n)`，空间 `O(n|Σ|)`',
        problem=['在 `s` 中找==重复 `k` 次==的最长子序列：`seq * k` 是 `s` 的子序列',
                 '长度相同取==字典序最大==，不存在返回空串',
                 '示例：`s="letsleetcode", k=2` → `"let"`',
                 '本视频：`s="abcabcab", k=2` → `"cab"`'],
        quote='设有 x 个字母至少出现 k 次，那么 kx ≤ n，即 x ≤ n/k < 8，所以==至多有 7 个字母==至少出现 k 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['seq 里的字母必须在 s 中至少出现 `k` 次；出现 `freq` 次的字母，seq 里最多放 `freq // k` 个',
              '枚举这些字母的排列（47 题），总共不超过 13699 个',
              '用子序列自动机 `nxt` 判断 `seq*k`：每个字母 O(1) 跳到下一次出现位置',
              '长度从大到小、字母降序枚举，第一个满足的就是答案'],
        result='找到 `cab`：先试 `cba` 失败，再试 `cab` 成功',
        summary=['时间 `O((n/k)!·n)`，空间 `O(n|Σ|)`',
                 '`a` 降序排序后 permutations 才是按字典序从大到小枚举',
                 '`nxt[i+1][c]`：下标要加 1，因为 i 初始为 -1',
                 '优化前写法：用 `iter(s)` 判断子序列，每次 `O(n)`，思路相同，本视频展示自动机写法',
                 '同类题：回溯题单 §4.5 排列型回溯、392 判断子序列'],
    ),
)
