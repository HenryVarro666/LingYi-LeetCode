CONFIG = dict(
    num=412, title='Fizz Buzz', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='分类讨论 · % 15',
    code='''
class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        ans = []
        for i in range(1, n + 1):
            if i % 15 == 0:
                ans.append("FizzBuzz")
            elif i % 3 == 0:
                ans.append("Fizz")
            elif i % 5 == 0:
                ans.append("Buzz")
            else:
                ans.append(str(i))
        return ans
''',
    call='Solution().fizzBuzz(15)',
    expect=["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"],
    views=[
        dict(type='text', fn=lambda S: f"`{S['i']} % 15 = {S['i'] % 15}`　`% 3 = {S['i'] % 3}`　`% 5 = {S['i'] % 5}`" if 'i' in S else '', size=30),
        dict(type='array', var='ans', label='ans（结果）', cell=76,
             color=lambda S, i, v: 'green' if i == len(S['ans']) - 1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('i % 15', 'i % 15', 'pink'), ('i % 3', 'i % 3', 'cyan'), ('i % 5', 'i % 5', 'orange')],
    captions={
        'ans = []': '`ans` 收集答案',
        'for i in range': '枚举 `i = {i}`',
        'if i % 15 == 0': lambda S, B, r: (f'`{S.i} % 15 = 0` → 同时是 3 和 5 的倍数（即 15 的倍数）' if S.i % 15 == 0 else f'`{S.i} % 15 = {S.i % 15}` → 不是 15 的倍数'),
        'elif i % 3 == 0': lambda S, B, r: (f'`{S.i} % 3 = 0` → 是 3 的倍数' if S.i % 3 == 0 else f'`{S.i} % 3 = {S.i % 3}` → 不是 3 的倍数'),
        'elif i % 5 == 0': lambda S, B, r: (f'`{S.i} % 5 = 0` → 是 5 的倍数' if S.i % 5 == 0 else f'`{S.i} % 5 = {S.i % 5}` → 不是 5 的倍数'),
        '"FizzBuzz"': '加入 `FizzBuzz`',
        '"Fizz"': '加入 `Fizz`',
        '"Buzz"': '加入 `Buzz`',
        'str(i)': '都不满足 → 加入数字本身 `"{i}"`',
        'return ans': '返回 `ans`',
    },
    cards=dict(
        one_liner='3 和 5 的倍数，等价于 15 的倍数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['返回 1 到 n 的字符串数组：3 的倍数 `Fizz`，5 的倍数 `Buzz`',
                 '同时是 3 和 5 的倍数 `FizzBuzz`，否则是数字本身',
                 '示例：`n = 15` → `["1","2","Fizz",...,"FizzBuzz"]`'],
        quote='按照题目要求，分类讨论，生成字符串。注意，i 是 3 和 5 的倍数，等价于 i 是 LCM(3,5)=15 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i % 15 == 0` 一次判断「同时是 3 和 5 的倍数」',
              '然后按顺序判断 3、5，最后兜底为 `str(i)`',
              '分支互斥，从最特殊的 15 开始判'],
        summary=['时间 `O(n log n)`：数字转字符串要 `O(log n)`；空间 `O(1)`（返回值不计）',
                 '易错：`% 15` 必须放最前，否则 15 会被 `Fizz` 抢走',
                 '写法二：`match (i % 3, i % 5)` 用 `case (0, 0)` 等四种情况分类'],
    ),
)
