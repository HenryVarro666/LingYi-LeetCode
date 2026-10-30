def _sums(S):
    nums = S['nums']
    s1 = sum(x for x in nums if x < 10)
    s2 = sum(x for x in nums if x >= 10)
    return s1, s2


def _txt(S):
    s1, s2 = _sums(S)
    return f'个位数之和 `s1 = {s1}`，两位数之和 `s2 = {s2}`，`s1 − s2 = {s1 - s2}` → ' + ('==s1 ≠ s2，Alice 能赢==' if s1 != s2 else '==相等，Alice 赢不了==')


CONFIG = dict(
    num=3232, title='判断是否可以赢得数字游戏', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='差值 s1−s2 ≠ 0',
    code='''
class Solution:
    def canAliceWin(self, nums: List[int]) -> bool:
        return sum(x if x < 10 else -x for x in nums) != 0
''',
    call='Solution().canAliceWin([1,2,3,4,5,14])',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=30, h=120),
        dict(type='array', var='nums', label='nums（绿 = 个位数，橙 = 两位数）', h=260,
             color=lambda S, i, v: 'green' if v < 10 else 'orange'),
    ],
    watch=[('s1 个位和', lambda S: _sums(S)[0], 'green'), ('s2 两位和', lambda S: _sums(S)[1], 'orange'),
           ('s1 − s2', lambda S: _sums(S)[0] - _sums(S)[1], 'blue')],
    captions={
        'return sum': '个位数取正、两位数取负，累加得 `s = s1 − s2`；Alice 要赢只需 `s ≠ 0` → ==返回 {ret}==',
    },
    cards=dict(
        before=[dict(heading='三个示例怎么想', lines=[
            '`[1,2,3,4,10]`：`s1 = 10`，`s2 = 10` → 相等，Alice 选哪边都只是平手，==输==',
            '`[1,2,3,4,5,14]`：`s1 = 15 > s2 = 14` → 选个位数赢',
            '`[5,5,5,25]`：`s1 = 15 < s2 = 25` → 选两位数赢',
            '共同点：只要两边不等，选大的那边就赢'])],
        one_liner='谁大选谁：只要 s1 ≠ s2，Alice 就能赢',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 选所有个位数或所有两位数，其余归 Bob，和严格更大者赢',
                 '`nums` 只含 1~99，问 Alice 能不能赢',
                 '示例：`[1,2,3,4,5,14]` → `true`（选个位数 15 > 14）'],
        quote='小红若要获胜，必须满足 s1 > s2 或者 s2 > s1，即 s1 ≠ s2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Alice 可以挑大的那堆，所以只会输在 ==两堆相等==',
              '令 `s = s1 − s2`：个位数加、两位数减，一次遍历',
              '最后只判断 `s != 0`，一行搞定'],
        after=[dict(heading='为什么不用分别比大小', lines=[
            '`s1 > s2` 或 `s2 > s1` 合起来就是 `s1 != s2`',
            '把两位数记成负数累加，得到的就是 `s1 − s2`',
            '所以不用建两个变量，也不用写 if，一行表达式即可'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '关键结论：Alice 获胜 ⇔ `s1 ≠ s2`，不必分别比大小',
                 '易错：题目要求严格大于，所以相等时 Alice 输',
                 '生成器表达式里 `x if x < 10 else -x` 把两位数变成相反数'],
    ),
)
