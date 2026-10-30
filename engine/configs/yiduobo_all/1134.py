CONFIG = dict(
    num=1134, title='阿姆斯特朗数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐位分离再求幂和',
    code='''
class Solution(object):
    def isArmstrong(self, n):

        num_list = []
        tmp = n
        while tmp:
            num_list.append(tmp % 10)
            tmp //= 10
        
        s = 0
        for digit in num_list:
            s += digit ** len(num_list)
        
        return s == n
''',
    call='Solution().isArmstrong(153)',
    expect=True,
    views=[
        dict(type='array', var='num_list', h=190, label='num_list（从个位开始的各位数字）'),
        dict(type='text', fn=lambda S: (f"位数 `k = {len(S['num_list'])}`；累加 `s = {S['s']}`，目标 `n = {S['n']}`" if 's' in S else (f"当前剩余 `tmp = {S['tmp']}`" if 'tmp' in S else ''))),
    ],
    watch=['n', 'tmp', 's', ('digit', 'digit', 'blue')],
    captions={
        'num_list = []': '`num_list` 存 n 的每一位数字',
        'tmp = n': '拷贝一份 `tmp = {tmp}`，原来的 n 留着最后比较',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}` 非 0，还有数位要取' if S.tmp else '`tmp` 变成 0：数位取完了'),
        'num_list.append': '`tmp % 10 = {num_list[-1]}` 是最低位，加入 num_list',
        'tmp //= 10': '去掉最低位：`tmp` → {tmp}',
        's = 0': '`s` 累加每位数字的 k 次方，k 是位数',
        's += digit': '`s += {digit} ** {len(num_list)}`，`s` → {s}',
        'return s == n': '`s = {s}` 与 `n = {n}` 比较 → =={ret}==',
    },
    cards=dict(
        one_liner='把每一位数字取 k 次方求和，等于自己就是阿姆斯特朗数',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['`n` 的位数为 `k`，若每位数字的 `k` 次方之和等于 `n`，则 `n` 是阿姆斯特朗数',
                 '判断给定的 `n` 是不是',
                 '示例：`153` → `True`，因为 `1³ + 5³ + 3³ = 153`'],
        quote='逐位分离n的每一位数字，并记录下数字的数位k。接下来遍历这些数字，按照题目给出的定义判断n是否为阿姆斯特朗数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`% 10` 取最低位，`// 10` 去掉最低位，循环到 0',
              '列表长度就是位数 k',
              '再逐位求 k 次方累加，与 n 比较'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '位数 k 要等全部分离完才知道，所以先存列表再求幂',
                 '原文为 Python 2 写法，`tmp /= 10` 已改为 `tmp //= 10`，并删去类型文档字符串',
                 '要用 `tmp` 副本，别把 n 本身除没了'],
    ),
)
