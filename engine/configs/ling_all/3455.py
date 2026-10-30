def _cols(S, i, v):
    for nm, c in (('pos1', 'blue'), ('pos2', 'green'), ('pos3', 'orange')):
        ps = S.get(nm)
        pl = S.get('p' + nm[-1])
        if ps is not None and pl is not None and 'p1' in S:
            L = len(S['p' + nm[-1]])
            if any(q <= i < q + L for q in ps):
                return c
    return None


def _ptr(S):
    inn = S.get('_inner', {})
    return inn['i'] if 'cnt' in inn and 'v' in inn else None


def _info(S):
    inn = S.get('_inner', {})
    if 'cnt' in inn and 'pi' in inn and 'pos' in inn:
        return f"找 `p = '{inn['p']}'`：已匹配长度 cnt = ==%d==，命中位置 pos = `{inn['pos']}`" % inn['cnt']
    if 'cnt' in inn and 'pi' in inn:
        return f"计算 pi：`p = {S['p']}`  pi = `{inn['pi']}`  cnt = ==%d==" % inn['cnt']
    if 'pos3' in S:
        return f"`pos1 = {S['pos1']}`  `pos2 = {S['pos2']}`  `pos3 = {S['pos3']}`  ans = ==%s=="  % (S['ans'] if S['ans'] != inf else '∞')
    return ''


CONFIG = dict(
    num=3455, title='最短匹配子字符串', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='KMP 求三段位置 · 枚举中间段 · 三指针', tags=['字符串', '难度分 2303'],
    code='''
class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        p1, p2, p3 = p.split('*')

        # 三段各自在 s 中的所有匹配位置
        pos1 = self.kmp_search(s, p1)
        pos2 = self.kmp_search(s, p2)
        pos3 = self.kmp_search(s, p3)

        ans = inf
        i = k = 0
        # 枚举中间（第二段），维护最近的左右（第一段和第三段）
        for j in pos2:
            # 右边找离 j 最近的子串（但不能重叠）
            while k < len(pos3) and pos3[k] < j + len(p2):
                k += 1
            if k == len(pos3):  # 右边没有
                break
            # 左边找离 j 最近的子串（但不能重叠）
            while i < len(pos1) and pos1[i] <= j - len(p1):
                i += 1
            # 循环结束后，pos1[i-1] 是左边离 j 最近的子串下标（首字母在 s 中的下标）
            if i > 0:
                ans = min(ans, pos3[k] + len(p3) - pos1[i - 1])
        return -1 if ans == inf else ans

    # 计算字符串 p 的 pi 数组
    def calc_pi(self, p: str) -> List[int]:
        pi = [0] * len(p)
        cnt = 0
        for i in range(1, len(p)):
            v = p[i]
            while cnt > 0 and p[cnt] != v:
                cnt = pi[cnt - 1]
            if p[cnt] == v:
                cnt += 1
            pi[i] = cnt
        return pi

    # 在文本串 s 中查找模式串 p，返回所有成功匹配的位置（p[0] 在 s 中的下标）
    def kmp_search(self, s: str, p: str) -> List[int]:
        if not p:
            # s 的所有位置都能匹配空串，包括 len(s)
            return list(range(len(s) + 1))

        pi = self.calc_pi(p)
        pos = []
        cnt = 0
        for i, v in enumerate(s):
            while cnt > 0 and p[cnt] != v:
                cnt = pi[cnt - 1]
            if p[cnt] == v:
                cnt += 1
            if cnt == len(p):
                pos.append(i - len(p) + 1)
                cnt = pi[cnt - 1]
        return pos
''',
    call="Solution().shortestMatchingSubstring('abbc', 'a*b*c')",
    expect=4,
    views=[
        dict(type='string', var='s', h=250, label='s（蓝 = 第一段，绿 = 第二段，橙 = 第三段的命中位置）',
             color=_cols, pointers={"i if 'cnt' in _inner else None": 'yellow'}, pointer_labels={"i if 'cnt' in _inner else None": 'i'}, cell=90),
        dict(type='text', fn=_info, h=90),
    ],
    watch=[('j', 'j', 'green'), ('i', 'i', 'blue'), ('k', 'k', 'orange'), ('ans', 'ans', 'yellow')],
    skip=['if not p', 'pi = self.calc_pi(p)', 'pi = [0] * len(p)', 'cnt = 0', 'pos = []', 'for i in range(1, len(p))', 'v = p[i]',
          'pi[i] = cnt', 'return pi', 'while cnt > 0 and p[cnt] != v', 'cnt += 1', 'cnt = pi[cnt - 1]', 'pos.append'],
    max_steps=80,
    captions={
        'p1, p2, p3 = p.split': '两个 `*` 把 `p` 切成三段：`p1 = {p1!r}`，`p2 = {p2!r}`，`p3 = {p3!r}`',
        'pos1 = self.kmp_search': '用 KMP 找 `p1` 在 `s` 里的所有命中位置',
        'pos2 = self.kmp_search': '同样找 `p2` 的所有命中位置（中间段，等会儿逐个枚举）',
        'pos3 = self.kmp_search': '再找 `p3` 的所有命中位置',
        'for i, v in enumerate(s)': "读入 `s[{i}] = '{v}'`，目前已匹配 `{cnt}` 个字符",
        'if p[cnt] == v': lambda S, B, r: (f"`p[{S.cnt}] = '{S.p[S.cnt]}'` 对 `'{S.v}'`：" + ('==相等==，匹配长度 +1' if S.p[S.cnt] == S.v else '不等，失配（`cnt = 0` 无需回退）')),
        'if cnt == len(p)': lambda S, B, r: (f"已匹配 `{S.cnt}` / `{len(S.p)}`：" + (f'==整段匹配完==，起点 `{S.i - len(S.p) + 1}` 记入 `pos`，再按 `pi` 回退' if S.cnt == len(S.p) else '还没匹配完')),
        'return pos': '`{p!r}` 的命中位置：`{pos}`',
        'ans = inf': '`ans` 先设成无穷大，之后取最小',
        'i = k = 0': '`i`、`k` 分别指向 `pos1`、`pos3` 里“最近的”候选，只增不减',
        'for j in pos2': lambda S, B, r: ('`pos2` 枚举完了' if getattr(B, 'j', None) == S.j else f'枚举中间段的起点 `j = {S.j}`（`pos2 = {S.pos2}`）'),
        'pos3[k] < j + len(p2)': lambda S, B, r: (f'右边 `p3` 必须从 `j + len(p2) = {S.j + len(S.p2)}` 及以后开始；`pos3[{S.k}] = {S.pos3[S.k]}`，' + ('太靠左，会和 `p2` 重叠 → `k` 右移' if S.k < len(S.pos3) and S.pos3[S.k] < S.j + len(S.p2) else '不重叠，这就是最近的 `p3`')) if S.k < len(S.pos3) else '`pos3` 已用完',
        'if k == len(pos3)': lambda S, B, r: ('右边已经没有 `p3` 了，后面的 `j` 更没有 → `break`' if S.k == len(S.pos3) else f'`k = {S.k}`，右边还有 `p3`，继续'),
        'pos1[i] <= j - len(p1)': lambda S, B, r: (f'左边 `p1` 必须在 `j - len(p1) = {S.j - len(S.p1)}` 及以前开始；`pos1[{S.i}] = {S.pos1[S.i]}`，' + ('不重叠 → `i` 右移，看有没有更近的' if S.i < len(S.pos1) and S.pos1[S.i] <= S.j - len(S.p1) else '再往右就重叠了，停')) if S.i < len(S.pos1) else '`pos1` 已用完，`i` 停在末尾',
        'i += 1': '`i` → {i}：`pos1[{i-1}]` 是目前左边最近的候选',
        'k += 1': '`k` → {k}',
        'if i > 0': lambda S, B, r: ('左边至少有一个 `p1` 可用：`pos1[i-1]` 就是离 `j` 最近的' if S.i > 0 else '`i = 0`：左边一个 `p1` 都放不下，这个 `j` 不行'),
        'ans = min(': '匹配子串从 `pos1[{i-1}] = {pos1[i-1]}` 到 `pos3[{k}] + len(p3) = {pos3[k] + len(p3)}`，长度 `{pos3[k] + len(p3) - pos1[i-1]}`；`ans` = =={ans}==',
        'return -1 if ans == inf': '`ans = {ans}`：有解就返回它，否则返回 `-1`',
    },
    cards=dict(
        one_liner='p 被两个星号切成三段：枚举中间段，左右各取最近的',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`p` 恰好含两个 `*`，`*` 匹配任意（含空）字符串',
                 '求 `s` 中与 `p` 匹配的最短子串长度，没有就返回 `-1`',
                 '示例：`s = "abbc"`，`p = "a*b*c"` → `4`'],
        quote='核心思路：枚举 p2 在 s 中的位置，同时计算（维护）左边最近的 p1 的位置，和右边最近的 p3 的位置，用对应的子串长度更新答案的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个星号把 `p` 拆成 `p1, p2, p3`，三段在 `s` 里各自的命中位置用 KMP 一次求出',
              '“枚举中间”：对每个 `p2` 的位置 `j`，要 ==左边最近且不重叠的 p1==、右边最近且不重叠的 `p3`',
              '位置有序，所以用 `i`、`k` 两个指针只增不减',
              '空段当作能匹配 `s` 的所有位置（含 `len(s)`），省去分类讨论'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：`pos3[k] < j + len(p2)` 要避免与 `p2` 重叠；`pos1[i] <= j - len(p1)` 同理',
                 '易错：循环结束后用的是 `pos1[i-1]`，且要 `i > 0`',
                 '空串返回 `range(len(s)+1)`，所以 `**` 之类的特殊输入不用单独判断'],
    ),
)
