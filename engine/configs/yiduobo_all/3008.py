CONFIG = dict(
    num=3008, title='找出数组中的美丽下标 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='两个 next 数组 · 一趟 KMP · 单调指针',
    tags=['灵神题单·字符串', 'KMP', '难度分 2016'],
    code='''
class Solution(object):
    def beautifulIndices(self, s, a, b, k):

        def get_nxt(t):
            f = [0]
            p = 0
            for index in range(1, len(t)):
                while p and t[p] != t[index]:
                    p = f[p - 1]
                
                if t[p] == t[index]:
                    p += 1
                
                f.append(p)
            
            return f

        nxt_a = get_nxt(a)
        nxt_b = get_nxt(b)

        p = q = 0
        match_a = []
        match_b = [-k - 1]

        for index in range(len(s)):
            while p and a[p] != s[index]:
                p = nxt_a[p - 1]
            if a[p] == s[index]:
                p += 1
                if p == len(a):
                    match_a.append(index - p + 1)
                    p = nxt_a[p - 1]
            
            while q and b[q] != s[index]:
                q = nxt_b[q - 1]
            if b[q] == s[index]:
                q += 1
                if q == len(b):
                    match_b.append(index - q + 1)
                    q = nxt_b[q - 1]
        
        
        p = q = 0
        res = []
        while p < len(match_a):
            while q + 1 < len(match_b) and match_b[q + 1] <= match_a[p]:
                q += 1
            
            if q != 0 and match_a[p] - match_b[q] <= k:
                res.append(match_a[p])
            elif q + 1 < len(match_b) and match_b[q + 1] - match_a[p] <= k:
                res.append(match_a[p])

            p += 1
            
        
        return res
''',
    call='Solution().beautifulIndices("abcab", "ab", "ca", 1)',
    expect=[3],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 当前扫描位置 index）', cell=60, h=150,
             pointers={'index': 'blue'}),
        dict(type='array', var='match_a', label='match_a：a 的起点', cell=60, h=150),
        dict(type='array', var='match_b', label='match_b：b 的起点（开头放哨兵 -k-1）', cell=60, h=170,
             pointers={'q': 'pink'}),
        dict(type='array', var='res', label='res：美丽下标', cell=60, h=130, color=lambda S, i, v: 'green'),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('k', 'k'), ('match_a', 'match_a', 'blue'), ('match_b', 'match_b', 'pink')],
    skip=['f = [0]', 6, 21, 'f.append(p)'],
    max_steps=130,
    captions={
        'nxt_a = get_nxt(a)': '先算 a 的 next 数组：`nxt_a = {nxt_a}`',
        'nxt_b = get_nxt(b)': '再算 b 的 next 数组：`nxt_b = {nxt_b}`',
        'match_a = []': '`match_a` 记 a 的所有起点',
        'match_b = [': '`match_b` 记 b 的所有起点，开头放哨兵 `-k-1`（距离永远 `> k`），省去判越界',
        'for index in range(len(s))': '一趟扫描 s：`index = {index}`，a、b 的 KMP 同时往前走',
        'for index in range(1, len(t))': '算 next：`index = {index}`',
        'while p and t[p] != t[index]': lambda S, B, r: (
            f"`t[{S.p}] ≠ t[{S.index}]` → 失配，`p` 按 next 回退" if S.p and S.t[S.p] != S.t[S.index] else '不用回退'),
        'if t[p] == t[index]': lambda S, B, r: (f"`t[{S.p}] == t[{S.index}]` → `p` 加一" if S.t[S.p] == S.t[S.index]
                                               else f"`t[{S.p}] ≠ t[{S.index}]`，`p` 不变"),
        'while p and a[p] != s[index]': lambda S, B, r: (
            f"`a[{S.p}] = '{S.a[S.p]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'` → `p` 回退到 `nxt_a[p-1]`" if S.p and S.a[S.p] != S.s[S.index]
            else '`p = 0` 或字符相等，不用回退'),
        'if a[p] == s[index]': lambda S, B, r: (
            f"`a[{S.p}] = '{S.a[S.p]}'` == `s[{S.index}]` → a 的匹配长度加一" if S.a[S.p] == S.s[S.index]
            else f"`a[{S.p}] = '{S.a[S.p]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'`，a 这一位没匹配"),
        'if p == len(a)': lambda S, B, r: (f"`p = {S.p} == len(a)` → ==a 完整出现=="  if S.p == len(S.a) else f"`p = {S.p} < {len(S.a)}`，a 还没匹配完"),
        'match_a.append(index - p + 1)': '记下 a 的起点 `index - p + 1`：`match_a = {match_a}`',
        'p = nxt_a[p - 1]': '`p` 回退到 `{p}`，继续找下一个出现',
        'while q and b[q] != s[index]': lambda S, B, r: (
            f"`b[{S.q}] = '{S.b[S.q]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'` → `q` 回退到 `nxt_b[q-1]`" if S.q and S.b[S.q] != S.s[S.index]
            else '`q = 0` 或字符相等，不用回退'),
        'if b[q] == s[index]': lambda S, B, r: (
            f"`b[{S.q}] = '{S.b[S.q]}'` == `s[{S.index}]` → b 的匹配长度加一" if S.b[S.q] == S.s[S.index]
            else f"`b[{S.q}] = '{S.b[S.q]}'` ≠ `s[{S.index}] = '{S.s[S.index]}'`，b 这一位没匹配"),
        'if q == len(b)': lambda S, B, r: (f"`q = {S.q} == len(b)` → ==b 完整出现==" if S.q == len(S.b) else f"`q = {S.q} < {len(S.b)}`，b 还没匹配完"),
        'match_b.append(index - q + 1)': '记下 b 的起点 `index - q + 1`：`match_b = {match_b}`',
        'q = nxt_b[q - 1]': '`q` 回退到 `{q}`',
        'res = []': '现在 `p`、`q` 改作 `match_a`、`match_b` 的下标；`res` 保存答案',
        'while p < len(match_a)': lambda S, B, r: (f"枚举 a 的起点 `match_a[{S.p}] = {S.match_a[S.p]}`" if S.p < len(S.match_a)
                                                  else 'a 的起点枚举完了'),
        'while q + 1 < len(match_b) and match_b[q + 1] <= match_a[p]': lambda S, B, r: (
            f"`match_b[{S.q + 1}] = {S.match_b[S.q + 1]} ≤ {S.match_a[S.p]}` → `q` 右移，找 ≤ 起点的最大 b" if S.q + 1 < len(S.match_b) and S.match_b[S.q + 1] <= S.match_a[S.p]
            else f"`q = {S.q}`：`match_b[q]` 是 ≤ `{S.match_a[S.p]}` 的最大 b 起点，`match_b[q+1]` 是更大的最近者"),
        'q += 1': '`q` → `{q}`',
        'if q != 0 and match_a[p] - match_b[q] <= k': lambda S, B, r: (
            f"左侧最近的 b：`{S.match_a[S.p]} - {S.match_b[S.q]} = {S.match_a[S.p] - S.match_b[S.q]}`" + (
                " ≤ k → ==美丽下标==" if S.q != 0 and S.match_a[S.p] - S.match_b[S.q] <= S.k
                else ("（`q = 0` 是哨兵，没有真的 b）→ 不行" if S.q == 0 else " > k → 不行"))),
        'elif q + 1 < len(match_b) and match_b[q + 1] - match_a[p] <= k': lambda S, B, r: (
            f"右侧最近的 b 距离更远？`q+1` 越界，右边没有 b" if S.q + 1 >= len(S.match_b) else
            f"右侧最近的 b：`{S.match_b[S.q + 1]} - {S.match_a[S.p]} = {S.match_b[S.q + 1] - S.match_a[S.p]}`" + (
                " ≤ k → ==美丽下标==" if S.match_b[S.q + 1] - S.match_a[S.p] <= S.k else " > k → 不行")),
        'res.append(match_a[p])': '`res` 加入 `{match_a[p]}` → `{res}`',
        'return res': '美丽下标：`{ret}`',
    },
    cards=dict(
        one_liner='一趟 KMP 记下 a、b 的起点，再让 q 单调右移比距离',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`i` 是美丽下标：`s` 里 `i` 处出现 `a`，且存在 `b` 的出现位置 `j`，`|j - i| ≤ k`',
                 '按从小到大返回所有美丽下标',
                 '本视频：`s="abcab"`，`a="ab"`，`b="ca"`，`k=1` → `[3]`'],
        quote='只需从左向右一趟遍历a的起点match_a[p]，那么match_b[q]也会随着match_a[p]单调不减',
        quote_src='—— yiduobo 题解原文',
        idea=['分别给 a、b 求 next 数组，扫一遍 s，同时用两个 KMP 记下 `match_a`、`match_b`',
              '对每个 `match_a[p]`，只需比较离它最近的两个 b：不超过它的最大者 `match_b[q]`，和更大的最近者 `match_b[q+1]`',
              '`p` 递增时 `q` 单调不减，均摊 `O(1)`；`match_b` 开头的 `-k-1` 是哨兵，不会误判'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`q != 0` 排除哨兵；右侧最近的 b 要先判 `q + 1` 不越界',
                 'KMP 匹配完整后 `p = nxt_a[p - 1]` 回退，才不会漏掉重叠的出现',
                 '对比灵神：灵神把 KMP 写成 `kmp(text, pattern)` 调两次，再用 `pos_b[j] < i - k` 右移；yiduobo 一趟扫描同时匹配 a、b',
                 '原文代码在 Python 3 下无需改动'],
    ),
)
