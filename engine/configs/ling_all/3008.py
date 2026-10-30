CONFIG = dict(
    num=3008, title='找出数组中的美丽下标 II', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='KMP 找出现位置 · 双指针',
    tags=['灵神题单·字符串', 'KMP', '难度分 2016'],
    code='''
class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        pos_a = self.kmp(s, a)
        pos_b = self.kmp(s, b)

        ans = []
        j, m = 0, len(pos_b)
        for i in pos_a:
            while j < m and pos_b[j] < i - k:
                j += 1
            if j < m and pos_b[j] <= i + k:
                ans.append(i)
        return ans

    def kmp(self, text: str, pattern: str) -> List[int]:
        m = len(pattern)
        pi = [0] * m
        c = 0
        for i in range(1, m):
            v = pattern[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            pi[i] = c

        res = []
        c = 0
        for i, v in enumerate(text):
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                res.append(i - m + 1)
                c = pi[c - 1]
        return res
''',
    call='Solution().beautifulIndices("abcab", "ab", "ca", 1)',
    expect=[3],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 当前 i）', cell=60, h=150, pointers={'i': 'blue'}),
        dict(type='array', var='pos_a', label='pos_a：a 在 s 中的出现位置', cell=60, h=150, pointers={'(pos_a.index(i) if i in pos_a else None)': 'blue'}, pointer_labels={'(pos_a.index(i) if i in pos_a else None)': 'i'}),
        dict(type='array', var='pos_b', label='pos_b：b 在 s 中的出现位置', cell=60, h=150, pointers={'j': 'pink'}),
        dict(type='array', var='ans', label='ans：美丽下标', cell=60, h=130, color=lambda S, i, v: 'green'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k'), ('pos_a', 'pos_a', 'blue'), ('pos_b', 'pos_b', 'pink')],
    skip=['pi[i] = c', 'v = pattern[i]', 'pi = [0] * m', 'c = 0\n', 'res = []'],
    max_steps=130,
    captions={
        'pos_a = self.kmp': '先用 KMP 求出 a 在 s 中所有出现位置：`pos_a = {pos_a}`',
        'pos_b = self.kmp': '再用 KMP 求出 b 的所有出现位置：`pos_b = {pos_b}`',
        'ans = []': '`ans` 保存美丽下标',
        'j, m = 0, len(pos_b)': '`pos_b` 有序，`j` 只增不减：指向第一个 `≥ i - k` 的 b 位置',
        'for i in pos_a': '枚举 a 的出现位置 `i = {i}`',
        'while j < m and pos_b[j] < i - k': lambda S, B, r: (
            f"`pos_b[{S.j}] = {S.pos_b[S.j]} < i - k = {S.i - S.k}` → 太靠左，对这个 i 和之后的 i 都没用，==跳过=="
            if S.j < S.m and S.pos_b[S.j] < S.i - S.k
            else (f"`j = {S.j}` 已到末尾" if S.j >= S.m else f"`pos_b[{S.j}] = {S.pos_b[S.j]} ≥ i - k = {S.i - S.k}`，不再右移 j")),
        'j += 1': '`j` → `{j}`',
        'if j < m and pos_b[j] <= i + k': lambda S, B, r: (
            f"`pos_b[{S.j}] = {S.pos_b[S.j]}` ≤ `i + k = {S.i + S.k}` → 距离不超过 k，==i 是美丽下标==" if S.j < S.m and S.pos_b[S.j] <= S.i + S.k
            else ("`j` 越界，右边已没有 b" if S.j >= S.m else f"`pos_b[{S.j}] = {S.pos_b[S.j]} > i + k = {S.i + S.k}` → 最近的 b 也太远，i 不是")),
        'ans.append(i)': '`ans` 加入 `{i}` → `{ans}`',
        'return ans': '美丽下标：`{ret}`',
        'm = len(pattern)': 'KMP：先求 `pattern` 的前缀函数 `pi`，`m = {m}`',
        'pi = [0] * m': '`pi[i]`：`pattern[:i+1]` 最长的相同前后缀长度',
        'c = 0': '`c` 是当前已匹配的长度',
        'for i in range(1, m)': '算前缀函数：`i = {i}`',
        'while c and pattern[c] != v': lambda S, B, r: (
            f"`pattern[{S.c}] ≠ '{S.v}'` → 失配，`c` 回退到 `pi[c-1]`" if S.c and S.pattern[S.c] != S.v else '`c = 0` 或已能匹配，不回退'),
        'c = pi[c - 1]': '`c` 回退到 `{c}`，不用从头重新匹配',
        'if pattern[c] == v': lambda S, B, r: (
            f"`pattern[{S.c}] = '{S.pattern[S.c]}'` == `'{S.v}'` → 匹配长度 `c` 加一" if S.pattern[S.c] == S.v
            else f"`pattern[{S.c}] ≠ '{S.v}'`，这个位置没匹配上"),
        'c += 1': '`c` → `{c}`',
        'res = []': '`res` 保存 pattern 在 text 中的起点',
        'for i, v in enumerate(text)': '扫描 text：`i = {i}`，`v = {v!r}`',
        'if c == len(pattern)': lambda S, B, r: (
            f"`c = {S.c} == len(pattern)` → ==完整匹配一次==" if S.c == len(S.pattern) else f"`c = {S.c} < {len(S.pattern)}`，还没匹配完"),
        'res.append(i - m + 1)': '起点 `i - m + 1 = {i - m + 1}` 记入 `res`：`{res}`',
        'c = pi[c - 1]\n': '匹配完后 `c` 回退到 `{c}`，继续找下一个重叠的出现',
        'return res': 'pattern 的出现位置：`{ret}`',
    },
    cards=dict(
        one_liner='KMP 找出 a、b 的出现位置，再双指针判断距离',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`i` 是美丽下标：`s[i:]` 以 `a` 开头，且存在 `b` 的出现位置 `j`，`|j - i| ≤ k`',
                 '按从小到大返回所有美丽下标',
                 '本视频：`s="abcab"`，`a="ab"`，`b="ca"`，`k=1` → `[3]`'],
        quote='由于 posA 和 posB 都是有序的，也可以用双指针做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['KMP 求出 a、b 在 s 中的全部出现位置 `pos_a`、`pos_b`，都是有序的',
              '对每个 `i`，只要看 `pos_b` 里第一个 `≥ i - k` 的位置 `j` 是否 `≤ i + k`',
              '`i` 递增时 `i - k` 也递增，所以 `j` 只右移不回头，总共 `O(n)`'],
        summary=['时间 `O(n)`，空间 `O(n)`，双指针里 `j` 总共最多右移 `n` 次',
                 '易错：`pos_b[j] < i - k` 才右移；找到的第一个 `j` 只需检查 `≤ i + k`',
                 'KMP 匹配成功后要令 `c = pi[c - 1]`，才能找到重叠的出现',
                 '题解的写法一：对 `pos_b` 二分找最近的 j，`O(n log n)`'],
    ),
)
