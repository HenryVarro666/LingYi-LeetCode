CONFIG = dict(
    num=2068, title='检查两个字符串是否几乎相等', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='频率差数组（Go 原文转写）', tags=[],
    code='''
class Solution:
    def checkAlmostEquivalent(self, word1: str, word2: str) -> bool:
        diff = [0] * 26  # 统计每个字符的频率差值
        for ch in word1:
            diff[ord(ch) - ord('a')] += 1
        for ch in word2:
            diff[ord(ch) - ord('a')] -= 1
        for d in diff:
            if d < -3 or d > 3:
                return False
        return True
''',
    call="Solution().checkAlmostEquivalent('aabbc', 'cccab')",
    expect=True,
    skip=['for ch in word1', 'for ch in word2', 'for d in diff'],
    views=[
        dict(type='string', var='word1', label='word1（+1）', cell=70, h=130,
             color=lambda S, i, v: 'blue' if S.get('_line') == 5 and S.get('ch') == v and False else None),
        dict(type='string', var='word2', label='word2（−1）', cell=70, h=130),
        dict(type='array', var='diff', label='diff[0..25] = 字母 a..z 的频率差（红 = 超过 3）', cell=36, h=210,
             color=lambda S, i, v: 'red' if abs(v) > 3 else ('yellow' if v != 0 else None)),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"当前字符 `{S['ch']}` → `diff[{ord(S['ch'])-97}]` = {S['diff'][ord(S['ch'])-97]}" if 'ch' in S and 'diff' in S and S['_line'] in (5, 7) else (f"检查 `d = {S['d']}`，范围 [-3, 3]" if 'd' in S else '')),
    ],
    watch=[('ch', 'ch'), ('d', 'd', 'orange')],
    captions={
        'diff = [0]': '开一个长为 26 的数组 `diff`，每个字母一格，记频率差（word1 − word2）',
        'diff[ord(ch) - ord(\'a\')] += 1': 'word1 的字符 `{ch}` 出现一次 → `diff[{ord(ch)-97}]` 加 1，变成 {diff[ord(ch)-97]}',
        'diff[ord(ch) - ord(\'a\')] -= 1': 'word2 的字符 `{ch}` 出现一次 → `diff[{ord(ch)-97}]` 减 1，变成 {diff[ord(ch)-97]}',
        'for d in diff': '检查下一个字母的频率差 `d = {d}`',
        'if d < -3': '`d = {d}`，是否超出 [-3, 3] → {"==超出，不是几乎相等==" if d < -3 or d > 3 else "没超出，继续"}',
        'return False': '有字母频率差超过 3，直接返回 ==False==',
        'return True': '26 个字母的差都在 [-3, 3] 内 → 返回 ==True==',
    },
    cards=dict(
        one_liner='word1 里 +1，word2 里 −1，看每个字母的差是否在 [-3, 3]',
        complexity='时间 `O(n+26)`，空间 `O(26)`',
        problem=['两个字符串每个字母的出现次数之差都 ==不超过 3==，就称几乎相等',
                 '示例：`"aaaa"` 与 `"bccb"` → `false`（`a` 差 4）',
                 '本视频：`"aabbc"` 与 `"cccab"` → `true`'],
        quote='diff := [26]int{} // 统计每个字符的频率差值',
        quote_src='—— 灵茶山艾府题解代码注释（Go）',
        idea=['不必分别统计两个字符串，用一个数组 `diff` 同时记差值',
              'word1 的字符加一，word2 的字符减一，最后每格就是频率差',
              '最后扫一遍 26 格，有 `d < -3` 或 `d > 3` 就返回 `False`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`ch-\'a\'` → `ord(ch) - ord(\'a\')`）',
                 '时间 `O(n+|Σ|)`，空间 `O(|Σ|)`，|Σ| = 26',
                 '易错点：差可以是负数，所以要判 `d < -3` 和 `d > 3` 两边',
                 '视频里 diff 数组只展示一次，同类题：242 有效的字母异位词'],
    ),
)
