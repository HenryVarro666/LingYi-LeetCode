def _outside_ok(S):
    return max(S['cnt'].values()) <= S['m']


CONFIG = dict(
    num=1234, title='替换子串得到平衡字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑窗 · 统计子串外的字母',
    tags=['滑动窗口与双指针', '难度分 1878'],
    code='''
class Solution:
    def balancedString(self, s: str) -> int:
        m = len(s) // 4
        cnt = Counter(s)
        if len(cnt) == 4 and min(cnt.values()) == m:  # 已经符合要求啦
            return 0

        ans, left = inf, 0
        for right, c in enumerate(s):  # 枚举子串右端点
            cnt[c] -= 1  # 注意 cnt 统计的是在子串 [left,right] 外面的字母个数
            while max(cnt.values()) <= m:  # 子串 [left,right] 满足要求
                ans = min(ans, right - left + 1)
                cnt[s[left]] += 1  # 缩小子串，把 s[left] 放到外面
                left += 1
        return ans
''',
    call="Solution().balancedString('QQWQERQQ')",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 待替换子串 [left, right]）', cell=100, h=230,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and 'left' in S and S['left'] <= i <= S['right'] and False),
        dict(type='map', var='cnt', label='cnt（子串外面各字母的个数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"目标：子串外每种字母 ==不超过 {S['m']}== 个；当前最多的是 ==" + str(max(S['cnt'].values())) + '==') if 'm' in S and 'cnt' in S and 'right' in S else ''),
    ],
    watch=[('m', 'm', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'm = len': '平衡时每种字母恰好 `m = n / 4 = {m}` 个',
        'cnt = Counter': '先统计整个字符串：`{dict(cnt)}`，此刻子串为空，==cnt 就是子串外的个数==',
        'if len(cnt) == 4': '`len(cnt)` = {len(cnt)}，最少的个数 = {min(cnt.values())}：已经平衡才能直接返回 0，这里不是',
        'ans, left = inf': '`ans` 先设为无穷大；`left = 0`',
        'for right, c': '枚举子串右端点：`right = {right}`，字母 `{c}` 并入子串',
        'cnt[c] -= 1': '`{c}` 进入子串 → 子串外的 `{c}` 少一个：`cnt[{c!r}] = {cnt[c]}`',
        'while max(cnt': lambda S, B, r: (f'子串外最多的字母有 `{max(S.cnt.values())}` 个 <= m = `{S.m}`：外面的字母都能补到 m，子串合法' if max(S.cnt.values()) <= S.m
                                         else f'子串外最多的字母有 `{max(S.cnt.values())}` 个 > m = `{S.m}`：外面已经超了，怎么替换都救不回，子串还得再长'),
        'ans = min': '合法子串长度 `{right - left + 1}`：`ans = min({B.ans}, {right - left + 1}) = {ans}`',
        'cnt[s[left]] += 1': '想让子串更短：把 `{s[left]}` 放回外面，`cnt[{s[left]!r}] = {cnt[s[left]]}`',
        'left += 1': '`left` 右移到 {left}，继续检查缩短后是否还合法',
        'return ans': '最短的待替换子串长度 `{ans}`',
    },
    cards=dict(
        one_liner='子串之外的字母不能超过 m 个，枚举右端点缩左端点',
        complexity='时间 `O(n|Σ|)`，空间 `O(|Σ|)`（|Σ| = 4）',
        problem=['`s` 只含 `Q W E R`，长度 `n` 是 4 的倍数，每种字母恰好 `n/4` 个才算平衡',
                 '替换一个子串（可换成任意字母），求子串最短长度；已平衡返回 0',
                 '示例：`"QQQW"` → `2`；本视频：`"QQWQERQQ"` → `4`'],
        quote='如果在待替换子串**之外**，某种字母的个数超过 m，那么无论怎么替换，都无法使这个字母在整个字符串中的个数为 m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子串外的字母改不了：任何一种 `> m`，就一定不平衡',
              '反过来，外面都 `<= m`，子串里的字母可以随便补齐 → 合法',
              '子串越长越容易合法，有单调性 → ==滑动窗口==，`cnt` 直接记子串外的个数'],
        summary=['时间 `O(n|Σ|)`，空间 `O(|Σ|)`',
                 '`cnt` 统计的是子串==外面==的字母，进窗口 `-1`，出窗口 `+1`',
                 '内层循环不比较 left 和 right：提前返回 0 保证空窗口时一定不合法，不会越界',
                 '这是「越长越合法，求最短」的模板：合法时先更新答案，再缩左端点'],
    ),
)
