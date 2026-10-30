CONFIG = dict(
    num=551, title='学生出勤记录 I', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='计数 + 子串判断',
    tags=[],
    code='''
class Solution:
    def checkRecord(self, s: str) -> bool:
        return s.count('A') < 2 and "LLL" not in s
''',
    call='Solution().checkRecord("PPALLP")',
    expect=True,
    views=[
        dict(type='string', var='s', h=200,
             color=lambda S, i, v: 'pink' if v == 'A' else ('orange' if v == 'L' else None)),
        dict(type='text', size=30,
             fn=lambda S: f"==A== 的个数 = `{S['s'].count('A')}`，是否 `< 2`：=={S['s'].count('A') < 2}=="),
        dict(type='text', size=30,
             fn=lambda S: f"是否含连续三个 L：=={'LLL' in S['s']}==，所以 `\"LLL\" not in s` 为 =={'LLL' not in S['s']}=="),
    ],
    watch=[('A 的个数', "s.count('A')", 'pink'), ('含 LLL', "'LLL' in s", 'orange')],
    captions={
        'return': lambda S, B, ret: f"两个条件同时成立才能拿奖：A 有 `{S['s'].count('A')}` 个，严格小于 2；且没有 LLL（{'LLL' not in S['s']}）→ 返回 =={ret}==",
    },
    cards=dict(
        one_liner='两个条件各用一句内置函数判断',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 由 `A` 缺勤、`L` 迟到、`P` 到场组成',
                 '拿奖要同时满足：==A 严格少于 2 个==，且 ==没有连续 3 个 L==',
                 '示例：`"PPALLP"` → `true`；`"PPALLL"` → `false`'],
        quote='根据题意，如果满足以下两个条件：$s$ 中的 A 低于两个；$s$ 不包含 LLL。则返回 true，否则返回 false。',
        quote_src='—— 灵茶山艾府题解',
        idea=['条件一翻译成 ==`s.count(\'A\') < 2`==',
              '条件二翻译成 ==`"LLL" not in s`==：连续三个 L 就是子串 LLL',
              '两句用 `and` 连起来，一行搞定，不用手写循环'],
        after=[dict(heading='为什么不会漏判', lines=['`LLL` 作为子串，天然要求三个 L ==紧挨着==',
                'A 的个数只看总数，不要求连续，所以用 `count`',
                '两个条件互相独立，分别判断再用 `and` 合并'])],
        before=[dict(heading='拆成两个条件', lines=['条件一：缺勤 A ==少于 2 天==（总数）',
                '条件二：不出现 ==连续 3 个 L==（子串）',
                '两条都成立才返回 `true`'])],
        summary=['时间 `O(n)`：`count` 和子串查找各扫一遍；空间 `O(1)`',
                 '易错点：A 是「严格少于 2」，用 `< 2` 不是 `<= 2`',
                 '迟到是「连续」3 天，不是总共 3 天，所以查子串 LLL',
                 '同类题：551 的进阶 552 要用 DP 计数'],
    ),
)
