CONFIG = dict(
    num=625, title='最小因式分解', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='从 9 到 2 贪心分离因子',
    tags=[],
    code='''
class Solution(object):
    def smallestFactorization(self, num):

        if num == 1:
            return 1

        digit_list = [0] * 10
        for digit in range(9, 1, -1):
            while num % digit == 0:
                digit_list[digit] += 1
                num //= digit
        
        if num != 1:
            return 0

        res = 0
        for digit in range(2, 10):
            for _ in range(digit_list[digit]):
                res = res * 10 + digit
        
        if res > 2147483647:
            return 0

        return res
''',
    call='Solution().smallestFactorization(60)',
    expect=256,
    skip=['for _ in range'],
    views=[
        dict(type='text', fn=lambda S: f"剩余 `num` = =={S['num']}==，已分离的因子个数见下表" if 'digit_list' in S else ''),
        dict(type='array', var='digit_list', pointers={'digit': 'blue'}, label='digit_list[d] = 因子 d 的个数（下标 = 数字）', h=300),
        dict(type='text', fn=lambda S: f"拼出的数 `res` = =={S['res']}==" if 'res' in S else '', size=40),
    ],
    watch=[('num', 'num', 'yellow'), ('digit', 'digit', 'blue'), ('res', 'res', 'green')],
    captions={
        'digit_list = [0]': '`digit_list[d]` 记录数字 `d`（2~9）要用几个',
        'for digit in range(9, 1, -1)': '`digit` = {digit}：从大到小试，大因子先拿走，剩下的更小、可以放高位',
        'while num % digit': lambda S, B, r: (f'`{S.num} % {S.digit} == 0`：{S.digit} 还能再分出一个' if S.num % S.digit == 0
                                              else f'`{S.num} % {S.digit} != 0`：分不出 {S.digit} 了，换下一个更小的数'),
        'digit_list[digit] += 1': '`digit_list[{digit}]` = {digit_list[digit]}',
        'num //= digit': '`num` 除掉 {digit}，剩 =={num}==',
        'if num != 1': lambda S, B, r: ('`num = 1`：全被 2~9 分干净了' if S.num == 1 else f'`num = {S.num}`：还有 2、3、5、7 以外的质因子 → 无解返回 0'),
        'res = res * 10 + digit': '把 {digit} 接到末尾：`res` = =={res}==（按 2→9 升序拼，小数字在高位）',
        'if res > 2147483647': '`res = {res}`：{"超过 2^31 - 1 → 返回 0" if res > 2147483647 else "没超过 2^31 - 1，合法"}',
        'return res': '最小的数是 =={res}==',
    },
    cards=dict(
        one_liner='质因子只能是 2、3、5、7，先凑大数字再升序拼',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['给正整数 `num`，找最小的正整数 `b`，使 `b` 的各位数字相乘等于 `num`',
                 '不存在或 `b` 超过 32 位有符号整数，返回 `0`',
                 '示例：`48` → `68`；`15` → `35`；本视频：`60` → `256`'],
        quote='对于2和3，则应该尽量使用8、9，如果构不成8也可以使用4，这样可以使得b的位数更少，从而达到题目要求的最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字乘积 = num，所以 num 只能含 2、3、5、7 这几种质因子',
              '位数越少数越小：从 9 到 2 倒序，能分就分，每个数字尽量大',
              '分完 `num` 若不是 1 → 无解；否则按 2 到 9 升序拼接，小数字放高位'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '`num == 1` 要单独返回 1，否则循环里什么都分不出',
                 '最后要判断是否超过 `2^31 - 1`，超过返回 0',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`'],
    ),
)
