HOURS = [9, 9, 6, 0, 6, 6, 9]


def _txt(S):
    if 'i' not in S:
        return '把「劳累」当 +1、「不劳累」当 -1，找和 > 0 的最长子数组；这里 `s` 是前缀和取反'
    s = S['s']
    return f'前缀和 = `{-s}`（取反存成 `s = {s}`）    ans = `{S["ans"]}`'


CONFIG = dict(
    num=1124, title='表现良好的最长时间段', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 连续性（一次遍历）',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 1908'],
    code='''
class Solution:
    def longestWPI(self, hours: List[int]) -> int:
        pos = [0] * (len(hours) + 2)  # 记录前缀和首次出现的位置
        ans = s = 0
        for i, h in enumerate(hours, 1):
            s -= 1 if h > 8 else -1  # 取反，改为减法
            if s < 0:
                ans = i
            else:
                if pos[s + 1]:  # 原本是 s-1，取反改为 s+1
                    ans = max(ans, i - pos[s + 1])  # 这里手写 if 会更快
                if pos[s] == 0:
                    pos[s] = i
        return ans
''',
    call=f'Solution().longestWPI({HOURS!r})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var='hours', label='hours（粉 = 劳累 > 8 小时，蓝 = 当前第 i 天）', h=190,
             color=lambda S, i, v: 'blue' if S.get('i') == i + 1 else ('pink' if v > 8 else None)),
        dict(type='array', var='pos', label='pos[s]：取反前缀和 s 第一次出现的位置（0 = 还没出现）', h=190,
             color=lambda S, i, v: 'yellow' if S.get('s') == i and S.get('s', -1) >= 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'pos = [0]': '`pos[s]` 记录取反前缀和 `s` ==首次出现==的位置，`0` 表示还没出现过',
        'ans = s = 0': '`ans` 是答案，`s` 是（取反后的）前缀和，起点 `s[0] = 0`',
        's -= 1 if': lambda S, B, r: (f'第 `{S.i}` 天 `h = {S.h}` ' + ('> 8，劳累 → 真前缀和 +1，取反存储就是 `s` 减 1' if S.h > 8 else '≤ 8，不劳累 → 真前缀和 -1，取反存储就是 `s` 加 1') + f'：`s` = {S.s}'),
        'if s < 0': lambda S, B, r: (f'`s = {S.s} < 0`，即真前缀和 `{-S.s} > 0`：从第 1 天到第 `{S.i}` 天劳累天数更多 → ==整段都合格=='
                                     if S.s < 0 else f'`s = {S.s}` ≥ 0，真前缀和 ≤ 0：整段不合格，要去前面找一个左端点'),
        'ans = i': '`ans = {i}`：最远的左端点就是起点 0，长度 `{i}`',
        'if pos[s + 1]': lambda S, B, r: (f'前缀和相邻只差 1，想要真前缀和严格更小 → 左端点取 `s+1` 首次出现的位置：`pos[{S.s + 1}] = {S.pos[S.s + 1]}`'
                                          + ('，出现过' if S.pos[S.s + 1] else '，没出现过')),
        'ans = max': '`ans = max({B.ans}, {i} - {pos[s + 1]}) = {ans}`：区间长度 `{i - pos[s + 1]}`',
        'if pos[s] == 0': lambda S, B, r: (f'`s = {S.s}` 第一次出现吗？`pos[{S.s}] = {S.pos[S.s]}` → ' + ('是，记下首次位置' if S.pos[S.s] == 0 else '不是，保留更靠左的')),
        'pos[s] = i': '`pos[{s}] = {i}`：以后它就是 `s` 的最左出现位置',
        'return ans': '最长表现良好时间段长度 `{ret}`',
    },
    cards=dict(
        one_liner='前缀和每次只变 1：想找更小的值，只需找「刚好小 1」的最左位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一天工作 > 8 小时是「劳累的一天」；时间段内劳累天数 ==严格大于== 不劳累天数才算表现良好',
                 '求表现良好时间段的最大长度',
                 '示例：`[9,9,6,0,6,6,9]` → `3`（`[9,9,6]`）'],
        quote='相邻前缀和的差都恰好为 1，要想算出比 s[i]-1 更小的数，必然会先算出 s[i]-1。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['劳累记 `+1`、不劳累记 `-1`，问题变成：最长的、和 `> 0` 的子数组',
              '前缀和 `> 0`：左端点取 0 最远；否则取 `s-1` 首次出现的位置',
              '为什么是 `s-1`：前缀和一步一格地走，更小的值必先经过 `s-1`'],
        after=[dict(heading='另一种写法：单调栈（方法一）',
                    lines=['先把前缀和里「比之前都小」的下标压栈，作为候选左端点',
                           '再从右往左枚举 `i`，只要 `s[i] > s[栈顶]` 就弹出并更新答案',
                           '更通用；本视频演示的是利用 ±1 的一次遍历写法'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`s` 为取反的前缀和，所以「找 s-1」写成了 `pos[s + 1]`，别看反',
                 '只记录==首次==出现的位置（`pos[s] == 0` 才写），这样长度最大',
                 '`pos` 数组下标从 0 到 n，位置用 1 起算，所以 0 可以当「未出现」',
                 '同类题：962 最大宽度坡（方法一直接套）'],
    ),
)
