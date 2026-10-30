CONFIG = dict(
    num=728, title='自除数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举 + 逐位检查',
    tags=[],
    code='''
class Solution(object):
    def selfDividingNumbers(self, left, right):

        res = []
        for num in range(left, right + 1):
            tmp = num
            flag = True
            while tmp:
                x = tmp % 10
                tmp //= 10
                if x == 0 or num % x != 0:
                    flag = False
                    break
            if flag:
                res.append(num)

        return res
''',
    call='Solution().selfDividingNumbers(10, 15)',
    expect=[11, 12, 15],
    views=[
        dict(type='text', fn=lambda S: ('' if 'num' not in S else
              (f"检查 `{S['num']}`：当前剩余 `tmp = {S['tmp']}`" + (f"，取出个位 `x = {S['x']}`" if 'x' in S and S.get('_line', 0) > 9 else '')) if 'tmp' in S else f"枚举 `{S['num']}`"), size=34),
        dict(type='array', var='res', h=200, cell=110, label='res（自除数）', color=lambda S, i, v: 'green'),
    ],
    watch=[('num', 'num', 'blue'), ('tmp', 'tmp', 'purple'), ('x', 'x', 'pink'), ('flag', 'flag', 'orange')],
    captions={
        'res = []': '`res` 保存所有自除数',
        'for num in range': '枚举 `num = {num}`',
        'tmp = num': '`tmp` 是 `num` 的拷贝，用来一位位拆',
        'flag = True': '先假设 `{num}` 是自除数',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}`，还有数位没检查' if S.tmp else '每一位都检查完了，没有出问题'),
        'x = tmp % 10': '取出最低位：`x = {tmp} % 10 = {x}`',
        'tmp //= 10': '去掉最低位：`tmp` → {tmp}',
        'if x == 0 or': lambda S, B, r: (f'`x = 0`：==不能做除数== → 不是自除数' if S.x == 0 else (f'`{S.num} % {S.x} = {S.num % S.x}` ≠ 0：不能被这一位整除 → 不是自除数' if S.num % S.x else f'`{S.num} % {S.x} = 0`：能整除，继续看下一位')),
        'flag = False': '`flag = False`，直接 `break`，不用看剩下的位',
        'if flag': lambda S, B, r: (f'`{S.num}` 每一位都整除 → 是自除数' if S.flag else f'`{S.num}` 不是自除数，跳过'),
        'res.append(num)': '`{num}` 加入答案：`res = {res}`',
        'return res': '枚举完毕，返回 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='范围只到 10000：直接枚举，每个数拆位检查',
        complexity='时间 `O((right-left) · log right)`，空间 `O(1)`（不计答案）',
        problem=['自除数：能被它的==每一位数字==整除，且不含 `0`',
                 '返回 `[left, right]` 内所有自除数',
                 '本视频：`[10, 15]` → `[11, 12, 15]`'],
        quote='由于题目给出的上界最多也只到10000，那么可以直接从left枚举到right，对于当前处理的数num，通过模10分离出每一位x，然后判断x是否非0且num模x是否为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`tmp % 10` 取最低位，`tmp //= 10` 去掉最低位',
              '某一位是 0 或不整除，立即 `flag = False` 并 `break`',
              '`flag` 一直为真才加入 `res`'],
        summary=['时间 `O(n log right)`，空间 `O(1)`',
                 '先判 `x == 0` 再取模，避免除以 0（`or` 短路）',
                 '要用 `num` 做被除数，`tmp` 才是被拆的那个',
                 '原文为 Python 2 写法，整数除法 `tmp /= 10` 已改为 `tmp //= 10`'],
    ),
)
