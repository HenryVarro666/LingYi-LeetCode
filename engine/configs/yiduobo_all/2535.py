CONFIG = dict(
    num=2535, title='数组元素和与数字和的绝对差', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='先求元素和 s，再逐位拆出数字和 t', tags=[],
    code='''
class Solution(object):
    def differenceOfSum(self, nums):

        s = sum(nums)
        t = 0
        for x in nums:
            while x:
                t += x % 10
                x //= 10
        
        return abs(s - t)
''',
    call='Solution().differenceOfSum([1, 15, 6, 3])',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=230),
        dict(type='text', h=130, size=32, fn=lambda S: (f"元素和 `s = {S['s']}`，数字和 `t = {S['t']}`" if 't' in S else (f"元素和 `s = {S['s']}`" if 's' in S else ''))),
        dict(type='text', h=130, size=32, fn=lambda S: (f"正在拆的数 `x = {S['x']}`" if 'x' in S else '')),
    ],
    watch=[('s', 's', 'blue'), ('t', 't', 'orange'), ('x', 'x', 'pink')],
    captions={
        's = sum(nums)': '`s`：所有元素直接相加 = =={s}==',
        't = 0': '`t` 用来累计所有数位之和',
        'for x in nums': lambda S, B, r: (f'取下一个元素 `x = {S.x}`' if S.x else '`nums` 里的元素都处理完了'),
        'while x': lambda S, B, r: (f'`x = {S.x}` 还没拆完' if S.x else '`x = 0`：这个数拆完了'),
        't += x % 10': '分离出个位 `{x % 10}`，加到 `t`：{B.t} → =={t}==',
        'x //= 10': '去掉个位：`x` → {x}',
        'return abs': '`|s − t| = |{s} − {t}|` = =={ret}==',
    },
    cards=dict(
        one_liner='分别算出元素和 s 与数字和 t，再取绝对差',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['元素和：所有元素相加；数字和：所有元素的每一位数字相加',
                 '求两者差的绝对值',
                 '示例：`[1,15,6,3]` → `|25 − 16| = 9`'],
        quote='逐位分离数字，计算元素和，然后计算元素和与原数的绝对值之差即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s = sum(nums)` 一步得到元素和',
              '对每个元素不断 `% 10` 取个位、`//= 10` 去掉个位，累加到 `t`',
              '最后返回 `abs(s - t)`'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `x /= 10` 已改为 `x //= 10`',
                 '拆数用的是循环变量 `x`，不会改动 `nums`',
                 '对比灵神：灵神一个变量边加边减，免去 `abs`；这里分开算再取绝对值'],
    ),
)
