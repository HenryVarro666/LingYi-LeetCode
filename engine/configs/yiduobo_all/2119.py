CONFIG = dict(
    num=2119, title='反转两次的数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='只看末尾是否为 0',
    tags=[],
    code='''
class Solution(object):
    def isSameAfterReversals(self, num):

        if num == 0:
            return True

        return num % 10 != 0
''',
    call='[Solution().isSameAfterReversals(x) for x in (526, 1800, 0, 90)]',
    expect=[True, False, True, False],
    views=[
        dict(type='text', size=34, h=110,
             fn=lambda S: f"`num = {S['num']}`，反转一次 `{int(str(S['num'])[::-1])}`，再反转 `{int(str(int(str(S['num'])[::-1]))[::-1])}`"),
        dict(type='string', var=lambda S: str(S['num']), label='num 的每一位（黄 = 个位，末尾是 0 就会丢失）', cell=100, h=190,
             color=lambda S, i, v: ('red' if v == '0' and i == len(str(S['num'])) - 1 and S['num'] != 0 else 'yellow' if i == len(str(S['num'])) - 1 else None)),
        dict(type='text', size=34, h=110,
             fn=lambda S: f"`num % 10 = {S['num'] % 10}`" + ('，末尾是 0 → ==False==' if S['num'] % 10 == 0 and S['num'] != 0 else '')),
    ],
    watch=[('num', 'num', 'blue'), ('num % 10', 'num % 10', 'yellow')],
    captions={
        'if num == 0': lambda S, B, r: ('`num == 0`：0 反转还是 0，特殊情况' if S.num == 0 else f'`num = {S.num}` 不是 0，继续判断'),
        'return True': '0 两次反转都不变 → 返回 `True`',
        'return num % 10 != 0': lambda S, B, r: (f'`{S.num} % 10 = {S.num % 10}`：末尾是 0，反转后前导 0 被丢掉，再反转就变了 → ==`{r}`==' if S.num % 10 == 0
                                                  else f'`{S.num} % 10 = {S.num % 10}`：末尾不是 0，反转不丢位，两次后还原 → ==`{r}`=='),
    },
    cards=dict(
        one_liner='只有末尾带 0 的数，两次反转后才会变',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['反转整数的各位，不保留前导 0；反转两次后是否等于原数',
                 '示例：`526` → `true`；`1800` → `false`（1800 → 81 → 18）；`0` → `true`',
                 "本视频依次运行 `526`、`1800`、`0`、`90`"],
        quote='只有去除前导0再翻转这种情况可能使得数字发生改变……因此只需检测原数字是否有后缀0，即检测原数字模10是否等于0就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['原数没有前导 0，所以第一次反转不会丢位，除非原数末尾有 0',
              '末尾的 0 反转后变成前导 0 被去掉，数位少了，再反转就回不去',
              '所以看 `num % 10` 是否为 0 即可；`0` 单独特判'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：`0 % 10 == 0`，但 0 两次反转不变，必须先特判',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
