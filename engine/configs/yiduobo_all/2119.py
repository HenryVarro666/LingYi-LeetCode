CONFIG = dict(
    num=2119, title='反转两次的数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='判断是否有后缀 0', tags=[],
    code='''
class Solution(object):
    def isSameAfterReversals(self, num):

        if num == 0:
            return True

        return num % 10 != 0
''',
    call='Solution().isSameAfterReversals(1800)',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: f"`num = {S['num']}`，`num % 10 = {S['num'] % 10}`", size=30),
        dict(type='text', fn=lambda S: f"反转 `{S['num']}` → `{str(S['num'])[::-1].lstrip('0') or '0'}` → 再反转 `{(str(S['num'])[::-1].lstrip('0') or '0')[::-1].lstrip('0') or '0'}`", size=28),
    ],
    watch=[('num', 'num', 'blue'), ('num % 10', 'num % 10', 'pink')],
    captions={
        'if num == 0': '`num = {num}`：{"是 0，特殊情况" if num == 0 else "不是 0，往下判断"}',
        'return True': '`0` 反转两次还是 `0` → True',
        'return num % 10': '`num % 10 = {num % 10}` → {"有后缀 0，反转后前导 0 被去掉，信息丢了" if num % 10 == 0 else "没有后缀 0"} → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='只有原数带后缀 0，反转时才会丢位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['反转整数：倒置所有位，去掉前导 0；`1800` → `81`',
                 '反转两次，结果还是原数吗？',
                 '示例：`526` → `true`；`1800` → `false`；`0` → `true`'],
        before=[dict(heading='先看例子', lines=['`526` → `625` → `526`：相同', '`1800` → `0081` 去零成 `81` → `18`：==不同==', '`0` → `0` → `0`：相同']), dict(heading='为什么', lines=['原数没有前导 0；反转后若没有前导 0，再反转就回到原数', '丢位只发生在：原数末尾的 0 变成前导 0 被去掉', '`0` 是特例：反转还是 `0`，答案是 true'])],
        quote='只有去除前导0再翻转这种情况可能使得数字发生改变，由于原数字是没有前导0的，因此翻转后就没有后缀0，再次翻转也不会有前导0。',
        quote_src='—— yiduobo 题解原文',
        idea=['原数没有前导 0，第二次反转不会丢位',
              '第一次反转：原数的后缀 0 变成前导 0 被去掉',
              '所以只需检查 `num % 10 != 0`，再单独处理 `0`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`0` 的 `0 % 10 == 0`，但答案是 true，所以先单独判断',
                 '代码与原文一致，Python 3 下可直接运行（无需修改）'],
    ),
)
