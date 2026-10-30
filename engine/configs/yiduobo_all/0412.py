CONFIG = dict(
    num=412, title='Fizz Buzz', difficulty='Easy', category='模拟',
    author='yiduobo', technique='枚举 + 先判 3 再判 5',
    code='''
class Solution(object):
    def fizzBuzz(self, n):

        res = []
        for index in range(1, n + 1):
            if index % 3 == 0:
                if index % 5 == 0:
                    res.append('FizzBuzz')
                else:
                    res.append('Fizz')
            elif index % 5 == 0:
                res.append('Buzz')
            else:
                res.append(str(index))

        return res
''',
    call='Solution().fizzBuzz(15)',
    expect=["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"],
    views=[
        dict(type='text', fn=lambda S: f"`{S['index']} % 3 = {S['index'] % 3}`，`{S['index']} % 5 = {S['index'] % 5}`" if 'index' in S else '', size=30),
        dict(type='array', var='res', label='res（结果）', cell=76,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('index', 'index', 'blue'), ('index % 3', 'index % 3', 'cyan'), ('index % 5', 'index % 5', 'orange')],
    captions={
        'res = []': '`res` 用来收集每个数对应的字符串',
        'for index in range': '枚举 `index = {index}`',
        'if index % 3 == 0': lambda S, B, r: (f'`{S.index} % 3 = 0` → 是 3 的倍数，还要看是不是 5 的倍数' if S.index % 3 == 0 else f'`{S.index} % 3 = {S.index % 3}` ≠ 0 → 不是 3 的倍数，去看 5'),
        7: lambda S, B, r: (f'`{S.index} % 5 = 0` → 同时是 3 和 5 的倍数' if S.index % 5 == 0 else f'`{S.index} % 5 = {S.index % 5}` → 只是 3 的倍数'),
        11: lambda S, B, r: (f'`{S.index} % 5 = 0` → 只是 5 的倍数' if S.index % 5 == 0 else f'`{S.index}` 既不是 3 也不是 5 的倍数'),
        "'FizzBuzz'": '3、5 都整除 → 加入 `FizzBuzz`',
        "'Fizz'": '只整除 3 → 加入 `Fizz`',
        "'Buzz'": '只整除 5 → 加入 `Buzz`',
        'str(index)': '都不整除 → 数字本身转成字符串 `"{index}"`',
        'return res': '15 个结果收集完毕',
    },
    cards=dict(
        one_liner='枚举每个数，看它模 3 和模 5 的余数',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['返回 1 到 n 的字符串数组：3 的倍数写 `Fizz`，5 的倍数写 `Buzz`',
                 '同时是 3 和 5 的倍数写 `FizzBuzz`，其余写数字本身',
                 '示例：`n = 15` → `["1","2","Fizz","4","Buzz",...,"FizzBuzz"]`'],
        quote='比较基础的题目，直接枚举每个数然后判断其模3以及模5的余数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看 `index % 3`：整除时再嵌套判断 `% 5`，决定 `FizzBuzz` 还是 `Fizz`',
              '不被 3 整除再看 `% 5`：整除是 `Buzz`，否则是数字本身'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：同时是 3、5 倍数的情况必须最先处理，否则会被 `Fizz` 抢走',
                 '这里用嵌套 if 实现，灵神则用 `% 15` 一次判断'],
    ),
)
