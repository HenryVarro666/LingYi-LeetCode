CONFIG = dict(
    num=1945, title='字符串转化后的各位数字之和', difficulty='Easy', category='模拟',
    author='yiduobo', technique='直接模拟 · 省掉拼数字串',
    tags=[],
    code='''
class Solution(object):
    def getLucky(self, s, k):

        now = 0
        for char in s:
            num = ord(char) - 96
            now += num % 10 + num // 10
        
        for _ in range(k - 1):
            tmp = now
            now = 0
            while tmp:
                now += tmp % 10
                tmp //= 10
        
        return now
''',
    call="Solution().getLucky('leetcode', 2)",
    expect=6,
    views=[
        dict(type='string', var='s', label='s', cell=60, h=200),
        dict(type='text', fn=lambda S: (f"字母 `{S['char']}` → `{S['num']}` → 数位和 `{S['num'] % 10 + S['num'] // 10}`" if 'num' in S and 'char' in S else ''), h=70),
        dict(type='text', fn=lambda S: (f"累计 `now = {S['now']}`" + (f"，正在拆 `tmp = {S['tmp']}`" if 'tmp' in S and S['tmp'] else '')) if 'now' in S else '', h=70),
    ],
    watch=['char', 'num', 'tmp', ('now', 'now', 'green')],
    captions={
        'now = 0\n': '`now` 累计数位和',
        'num = ord': '`{char}` 是第 `{num}` 个字母（`ord - 96`）',
        'now += num % 10': '`{num}` 的数位和 = `{num % 10} + {num // 10}`：`now` → =={now}==（第一次转换顺带完成）',
        'for _ in range': '再做 `k - 1 = {k - 1}` 次数位和',
        'tmp = now': '取出 `now = {tmp}` 准备拆位',
        'while tmp': lambda S, B, r: (f"`tmp = {S.tmp}` 还没拆完" if S.tmp else "拆完了，本轮结果 ==now=={}".format(S.now)),
        'now += tmp % 10': '取个位 `{tmp % 10}`：`now` → {now}',
        'tmp //= 10': '去掉个位：`tmp` → {tmp}',
        'return now': '结果 `{now}`',
    },
    cards=dict(
        one_liner='第一次数位和可以边拆字母边算，不用真的拼出那个大整数',
        complexity='时间 `O(|s| + k·log)`，空间 `O(1)`',
        problem=['把字符串 `s` 里每个字母换成字母表位置（`a`=1…`z`=26），拼成一个整数',
                 '然后重复 `k` 次「各位数字之和」，返回最终结果',
                 '示例：`s = "leetcode"`，`k = 2` → `6`'],
        quote='因此至少会执行一次数位和，所以一开始就没必要将字符串转化为数字串，而是直接将每个字符拆出来之后计算数位和，然后再执行剩下的k - 1次数位和即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个字母对应 1–26，数位和 = `num % 10 + num // 10`',
              '`k ≥ 1`，第一次数位和直接对每个字母累加',
              '剩下 `k - 1` 次对 `now` 做普通拆位求和'],
        summary=['时间 `O(|s|)` 加 `O(k log)`，空间 `O(1)`',
                 '易错点：转化那一步本身不算一次「转换」，之后还要做 `k` 次数位和',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（两处）'],
    ),
)
