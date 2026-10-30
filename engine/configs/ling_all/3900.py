def _t(S):
    if 'pre' not in S or 'total0' not in S:
        return ''
    return f"前缀和 `pre = {S['pre']}`（1 记 +1，0 记 −1）；子串和 = 2 → 交换一个 1 出去、一个 0 进来；和 = −2 则反过来"


CONFIG = dict(
    num=3900, title='一次交换后的最长平衡子串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表 · 记前两次出现位置',
    tags=['前缀和与哈希表', '难度分 2135'],
    code='''
class Solution:
    def longestBalanced(self, s: str) -> int:
        total0 = s.count('0')
        total1 = len(s) - total0

        pos = defaultdict(list)
        pos[0] = [-1]  # 见 525 题
        ans = 0
        pre = 0  # 前缀和

        for i, ch in enumerate(s):
            pre += 1 if ch == '1' else -1

            if len(pos[pre]) < 2:
                pos[pre].append(i)

            # 不交换
            ans = max(ans, i - pos[pre][0])

            # 交换子串内的一个 1 和子串外的一个 0
            if pre - 2 in pos:
                p = pos[pre - 2]
                if (i - p[0] - 2) // 2 < total0:
                    ans = max(ans, i - p[0])
                elif len(p) > 1:
                    ans = max(ans, i - p[1])

            # 交换子串内的一个 0 和子串外的一个 1
            if pre + 2 in pos:
                p = pos[pre + 2]
                if (i - p[0] - 2) // 2 < total1:
                    ans = max(ans, i - p[0])
                elif len(p) > 1:
                    ans = max(ans, i - p[1])

        return ans
''',
    call="Solution().longestBalanced('100001')",
    expect=4,
    views=[
        dict(type='string', var='s', label='s', cell=100, h=230, pointers={'i': 'blue'},
             color=lambda S, i, v: None),
        dict(type='map', var='pos', label='pos：前缀和 → 前两次出现的位置', fmt=lambda k, v: f'{k}: {v}', h=260, font=30),
        dict(type='text', h=110, size=26, fn=_t),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'cyan'), ('total0', 'total0', 'orange'), ('total1', 'total1', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'total0 = s.count': '先数全串的 0：`total0 = {total0}`，用来判断子串外面还有没有 0',
        'total1 = len': '`total1 = {total1}`：1 的个数',
        'pos = defaultdict': '`pos[前缀和]` 存这个前缀和出现过的前两个位置',
        'pos[0] = [-1]': '空前缀（位置 -1）的和是 0',
        'ans = 0': '`ans = 0`：空子串也算平衡',
        9: '`pre` 是前缀和，从 0 开始',
        'for i, ch in enumerate(s)': lambda S, B, r: (f'枚举右端点 `i = {S.i}`，字符 `{S.ch}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'pre += 1': '`{ch}` 记 `{1 if ch == "1" else -1}` → `pre = {pre}`',
        'if len(pos[pre]) < 2': lambda S, B, r: (f'`pos[{S.pre}]` 记录了 {len(S.pos[S.pre])} 个位置，不足 2 个 → 把 `i = {S.i}` 记下' if len(S.pos[S.pre]) < 2
                                                else f'`pos[{S.pre}]` 已有两个位置，不再记录'),
        'pos[pre].append(i)': '先更新 pos（允许空子串）：`pos[{pre}] = {pos[pre]}`',
        'ans = max(ans, i - pos[pre][0])': '不交换：和为 0 的最长子串长 `{i} − ({pos[pre][0]}) = {i - pos[pre][0]}` → `ans = {ans}`',
        'if pre - 2 in pos': lambda S, B, r: (f'`pre − 2 = {S.pre - 2}` 出现过：子串和为 2，多了两个 1（一个 1 换成外面的 0）' if S.pre - 2 in S.pos
                                              else f'`pre − 2 = {S.pre - 2}` 没出现过，跳过'),
        'if (i - p[0] - 2) // 2 < total0': lambda S, B, r: (
            f'子串内有 `({S.i} − ({S.p[0]}) − 2) // 2 = {(S.i - S.p[0] - 2) // 2}` 个 0，< total0 = {S.total0}：外面还有 0，可以换' if (S.i - S.p[0] - 2) // 2 < S.total0
            else f'子串内 0 的个数 = total0：外面没有 0 → 改用第二次出现的位置'),
        'if pre + 2 in pos': lambda S, B, r: (f'`pre + 2 = {S.pre + 2}` 出现过：子串和为 −2，多了两个 0（一个 0 换成外面的 1）' if S.pre + 2 in S.pos
                                              else f'`pre + 2 = {S.pre + 2}` 没出现过，跳过'),
        'if (i - p[0] - 2) // 2 < total1': lambda S, B, r: (
            f'子串内有 `({S.i} − ({S.p[0]}) − 2) // 2 = {(S.i - S.p[0] - 2) // 2}` 个 1，< total1 = {S.total1}：外面还有 1，可以换' if (S.i - S.p[0] - 2) // 2 < S.total1
            else f'子串内 1 的个数 = total1：外面没有 1 → 改用第二次出现的位置'),
        'ans = max(ans, i - p[0])': '最远的位置 `{p[0]}` 可用 → 子串长 `{i - p[0]}`，`ans = {ans}`',
        'ans = max(ans, i - p[1])': '用第二次出现的位置 `{p[1]}`：子串长 `{i - p[1]}`，外面必有可换的字符 → `ans = {ans}`',
        'elif len(p) > 1': lambda S, B, r: ('有第二次出现的位置' if len(S.p) > 1 else '只出现过一次，没有备选'),
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='平衡 = 和 0；换一次 = 和 ±2，且外面要有可换的字符',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，最多交换任意两个字符一次，再选一个 0 和 1 个数相等的子串',
                 '求这个平衡子串的最大长度（空串也平衡）',
                 '示例：`s = "100001"` → `4`'],
        quote='如果把子串中的一个 1 和外面的一个 0 交换后，子串变成平衡的，那么交换前，子串中的 1 的个数恰好比 0 的个数多 2。用 525 题的做法来说，就是子串的元素和恰好等于 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['1 记 +1、0 记 −1：不交换 = 找和为 0 的最长子串（525 题）',
              '交换 = 找和为 ±2 的子串：`sum[i] − sum[j] = ±2`，j 越小越长',
              '外面没有可换字符时，退而用该前缀和==第二次==出现的位置'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：外面是否还有 0（或 1）要用 `(i − j − 2) // 2 < total0` 判断',
                 '同一个前缀和只需保留前两次出现的位置',
                 '允许空子串：先更新 `pos`，再算长度',
                 '把哈希表换成数组会更快一些'],
    ),
)
