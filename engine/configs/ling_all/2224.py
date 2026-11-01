CONFIG = dict(
    num=2224, title='转化时间需要的最少操作数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='从大到小贪心（Go 原文转写）', tags=[],
    code='''
def parseTime(s: str) -> int:
    return ((ord(s[0]) & 15) * 10 + (ord(s[1]) & 15)) * 60 + (ord(s[3]) & 15) * 10 + (ord(s[4]) & 15)

class Solution:
    def convertTime(self, current: str, correct: str) -> int:
        ans = 0
        diff = parseTime(correct) - parseTime(current)
        for inc in [60, 15, 5, 1]:  # 从大往小贪心
            ans += diff // inc
            diff %= inc
        return ans
''',
    call='Solution().convertTime("02:30", "04:35")',
    expect=3,
    views=[
        dict(type='string', var='current', label='current', h=110),
        dict(type='string', var='correct', label='correct', h=110),
        dict(type='array', var='[60, 15, 5, 1]', label='可加的分钟数', pointers={}, h=130),
        dict(type='text', fn=lambda S: (f"还差 ==`{S['diff']}`== 分钟，已用 ==`{S['ans']}`== 步") if 'diff' in S and 'ans' in S else '', size=36, h=100),
    ],
    watch=['diff', 'inc', ('ans', 'ans', 'green')],
    captions={
        'return (ord': '`HH:MM` 转成分钟：`(时 × 10 位 + 个位) × 60 + 分`，得到 `{ret}`',
        'ans = 0': '`ans` 累计操作次数',
        'diff = parseTime': '两个时间换成分钟再相减：`diff = {diff}`',
        'for inc in': lambda S, B, r: f'试第一个面额：`inc = {S.inc}`' if S.inc == 60 else f'换更小的面额：`inc = {S.inc}`',
        'ans += diff // inc': '`{B.diff} // {inc} = {B.diff // inc}` 个 `{inc}` 分钟 → `ans` = =={ans}==',
        'diff %= inc': '用不完的余数留给更小面额：`diff` = =={diff}==',
        'return ans': '余数用完，最少 `{ret}` 步',
    },
    cards=dict(
        one_liner='60、15、5、1 互为倍数，大的能用就用',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每步可把时间加 `1`、`5`、`15` 或 `60` 分钟',
                 '求把 `current` 变成 `correct` 的最少步数',
                 '示例：`"02:30"` → `"04:35"` 答案 `3`'],
        quote='for _, inc := range []int{60, 15, 5, 1} { // 从大往小贪心',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['两个时间先转成分钟，只需关心差值 `diff`',
              '从 `60` 到 `1`：能整除几个就用几个，余数交给下一个面额',
              '后一个面额都能整除前一个，所以大面额优先不会吃亏'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`/` 整除写成 `//`）',
                 '`s[0]&15` 取字符对应的数字，Python 里写成 `ord(s[0]) & 15`',
                 '时间 `O(1)`，空间 `O(1)`',
                 '易错：贪心成立依赖面额互为倍数，换成别的面额就不一定对'],
    ),
)
