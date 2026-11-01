def _letters(S):
    cnt = S.get('cnt')
    if cnt is None:
        return ''
    nz = [f"{chr(97 + i)}:{c}" for i, c in enumerate(cnt) if c]
    return '非零字母 ' + (('  '.join(nz)) if nz else '无') + '（正 = s 多，负 = t 多）'


CONFIG = dict(
    num=2186, title='制造字母异位词的最小步骤数 II', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='26 字母计数差（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def minSteps(self, s: str, t: str) -> int:
        ans = 0
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        for ch in t:
            cnt[ord(ch) - ord('a')] -= 1
        for c in cnt:
            ans += abs(c)
        return ans
''',
    call='Solution().minSteps("abca", "bcd")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=120),
        dict(type='string', var='t', label='t', cell=80, h=120),
        dict(type='array', var='cnt', label='cnt[0..25]，下标 0 = a，1 = b …', cell=36, h=170, pointers={'ord(ch) - 97': 'pink'}, pointer_labels={'ord(ch) - 97': 'ch'},
             color=lambda S, i, v: 'green' if v > 0 else ('orange' if v < 0 else None)),
        dict(type='text', fn=_letters, size=26),
    ],
    watch=[('ch', 'ch', 'blue'), ('c', 'c', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计需要追加的字符数',
        'cnt = [0] * 26': '26 个小写字母各一个计数器，初始 0',
        'cnt[ord(ch) - ord(\'a\')] += 1': "s 里的 `'{ch}'` 记一次：`cnt[{ord(ch) - 97}] = {cnt[ord(ch) - 97]}`",
        'cnt[ord(ch) - ord(\'a\')] -= 1': "t 里的 `'{ch}'` 抵消一次：`cnt[{ord(ch) - 97}] = {cnt[ord(ch) - 97]}`",
        'for c in cnt': '取下一个字母的计数差 `c = {c}`',
        'ans += abs(c)': lambda S, B, ret: (f'差值 `{S.c}`，要补 `abs({S.c}) = {abs(S.c)}` 个 → `ans` = {S.ans}' if S.c else f'差值 `0`，不用补 → `ans` = {S.ans}'),
        'return ans': '各字母差的绝对值之和 = `{ans}`，就是最少步数',
    },
    skip=['cnt = [0] * 26'],
    max_steps=70,
    cards=dict(
        one_liner='每个字母缺多少补多少，总数就是计数差的绝对值之和',
        complexity='时间 `O(n+m+26)`，空间 `O(26)`',
        problem=['每步可以给 `s` 或 `t` 末尾追加==任一字符==，求让两串互为字母异位词的最少步数',
                 '示例：`s = "leetcode"`，`t = "coats"` → `7`',
                 '本视频：`s = "abca"`，`t = "bcd"` → `3`'],
        quote='cnt := [26]int{}  for _, ch := range s { cnt[ch-\'a\']++ }  for _, ch := range t { cnt[ch-\'a\']-- }  for _, c := range cnt { ans += abs(c) }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['s 中加、t 中减，`cnt[x]` 就是 x 在两串里的次数差',
              '差为正：t 要补这么多个 x；差为负：s 要补',
              '每个字母要补的个数 = `abs(cnt[x])`，加起来即可'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（Go 里自定义的 `abs` 用 Python 内置 `abs`）',
                 '时间 `O(n+m)`，空间 `O(26)`',
                 '易错：只能追加不能删除，所以两边都要补，差的绝对值都要累加',
                 '同类题：1347、2186 都是字母计数差'],
    ),
)
