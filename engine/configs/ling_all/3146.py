CONFIG = dict(
    num=3146, title='两个字符串的排列差', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='哈希表记下标',
    code='''
class Solution:
    def findPermutationDifference(self, s: str, t: str) -> int:
        pos = {c: i for i, c in enumerate(s)}
        return sum(abs(i - pos[c]) for i, c in enumerate(t))
''',
    call="Solution().findPermutationDifference('abcde', 'edbac')",
    expect=12,
    views=[
        dict(type='string', var='s', label='s', cell=96, h=140),
        dict(type='string', var='t', label='t', cell=96, h=140),
        dict(type='map', var='pos', label='pos（字符 → 在 s 中的下标）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=32),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c')],
    captions={
        'pos = {': '遍历 `s`，记下每个字母的下标：`pos = {pos}`（字母不重复，所以不会覆盖）',
        'return sum': '遍历 `t`，把每个字母在 `t` 中的下标 `i` 与 `pos[c]` 作差取绝对值再求和，结果 ==`{ret}`==',
    },
    cards=dict(
        after=[dict(heading='逐项算一遍（t = "edbac"）', lines=['`e`：`|0 − 4| = 4`，`d`：`|1 − 3| = 2`，`b`：`|2 − 1| = 1`', '`a`：`|3 − 0| = 3`，`c`：`|4 − 2| = 2`', '合计 `4 + 2 + 1 + 3 + 2` = ==12==', '生成器边遍历 `t` 边求和，不用额外存数组'])],
        one_liner='先记下 s 里每个字母的位置，再扫 t 累加位置差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`t` 是 `s` 的排列，字母都不重复',
                 '排列差 = 每个字母在两串中下标之差的绝对值之和',
                 '示例：`s = "abcde", t = "edbac"` → `12`'],
        quote='遍历 s，用哈希表（或者数组）记录字母 c=s[i] 的下标 pos[c] = i。注意 s 和 t 中没有重复字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字母不重复，所以每个字母在 `s` 里只有一个下标，哈希表一一对应',
              '再扫 `t`：当前下标 `i` 减去 `pos[c]`，取绝对值累加',
              '两步都是一趟遍历，合起来 `O(n)`'],
        summary=['时间 `O(n)`，空间 `O(n)`（字母只有 26 个，也可用数组）',
                 '易错：差要取==绝对值==，不能直接相减',
                 '原文两步都写成一行：字典推导式 + 生成器求和'],
    ),
)
