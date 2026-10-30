def _txt(S):
    a = S.get('a')
    if a is None or '_line' not in S:
        return ''
    if S['_line'] < 11:
        return ''
    a = list(a)
    if len(a) >= 3 and S['_line'] >= 13:
        x = a + [0] * max(0, 3 - len(a))
        return f"`max({x[0]}−2, min({x[0]}−1, {x[1]}), {x[2]})` = =={max(x[0]-2, min(x[0]-1, x[1]), x[2])}=="
    return f'当前字母的长度列表 `a = {a}`'


CONFIG = dict(
    num=2982, title='找出出现至少三次的最长特殊子字符串 II', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='分组 + 分类讨论取前三长',
    tags=['二分算法', '贪心与思维', '难度分 1773'],
    code='''
class Solution:
    def maximumLength(self, s: str) -> int:
        groups = defaultdict(list)
        cnt = 0
        for i, ch in enumerate(s):
            cnt += 1
            if i + 1 == len(s) or ch != s[i + 1]:
                groups[ch].append(cnt)  # 统计连续字符长度
                cnt = 0

        ans = 0
        for a in groups.values():
            a.sort(reverse=True)
            a.extend([0, 0])  # 假设还有两个空串
            ans = max(ans, a[0] - 2, min(a[0] - 1, a[1]), a[2])

        return ans if ans else -1
''',
    call="Solution().maximumLength('aaaabbbabbaa')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s', pointers={'i': 'blue'}, cell=70, h=190),
        dict(type='map', var='groups', label='groups：每个字母的连续段长度', fmt=lambda k, v: f"'{k}': {v}", h=190, font=34),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'orange'), ('a', 'a', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'cnt += 1': '当前连续段又多一个字符：`cnt = {cnt}`',
        'if i + 1 == len(s)': lambda S, B, r: (f"`s[{S.i}]` 是最后一个字符，或者和下一个不同 → ==这一段结束==" if (S.i + 1 == len(S.s) or S.ch != S.s[S.i + 1])
                                              else f"`s[{S.i}] = s[{S.i + 1}] = '{S.ch}'` → 同一段还没结束"),
        'groups[ch].append': "字母 `'{ch}'` 记下一段长度 `{cnt}`：`groups['{ch}'] = {groups[ch]}`",
        4: '`cnt` 记录当前这一段的连续长度',
        9: '这一段统计完了，`cnt` 清零，重新开始统计下一段',
        'for a in groups.values()': '逐个字母处理，`a` = 这个字母所有连续段的长度',
        'a.sort': '从大到小排序：`a = {a}`，只有最长的前三段可能有用',
        'a.extend': '末尾补两个 0，当作还有两个空串 → 不用特判长度不足三段：`a = {a}`',
        'ans = max': lambda S, B, r: (f"三种取法：最长段切三份 `{S.a[0]}−2={S.a[0]-2}`；前两段 `min({S.a[0]}−1, {S.a[1]})={min(S.a[0]-1, S.a[1])}`；前三段各取一个 `{S.a[2]}` → `ans = {B.ans} → {S.ans}`"),
        'return ans if ans': lambda S, B, r: f'`ans = {S.ans}`，' + ('为 0 说明没有出现三次的特殊子串 → 返回 `-1`' if not S.ans else '不是 0 → 直接返回'),
    },
    cards=dict(
        one_liner='按字母分组，只看每个字母最长的三段',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`s` 只含小写字母。特殊子串 = 只由同一个字母组成',
                 '求出现 ==至少三次== 的最长特殊子串长度，没有返回 `-1`',
                 '示例：`"aaaa"` → `2`（三个 `"aa"`）'],
        quote='从最长的特殊子串中取三个长度均为 a[0]-2 的特殊子串；或者从最长和次长中取三个长度一样的；又或者从最长、次长、第三长中各取一个长为 a[2] 的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个字母的连续段分组，长度列表降序排成 `a`',
              '三种取法：只用最长段 / 用前两段 / 用前三段',
              '答案 = `max(a[0]-2, min(a[0]-1, a[1]), a[2])`，对所有字母取最大'],
        summary=['时间 `O(n log n)`，排序可换成堆维护前三大，降到 `O(n)`',
                 '末尾补两个 0，免去长度不足三段的特判',
                 '易错：两段等长时只能取 `a[0]-1`，不等长取 `a[1]`，合并成 `min(a[0]-1, a[1])`',
                 '最后答案为 0 要返回 `-1`；另一种思路是二分长度，本视频用分类讨论'],
    ),
)
