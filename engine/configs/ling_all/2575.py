CONFIG = dict(
    num=2575, title='找出字符串的可整除数组', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='前缀取模',
    tags=[],
    code='''
class Solution:
    def divisibilityArray(self, word: str, m: int) -> List[int]:
        ans = []
        x = 0
        for d in map(int, word):
            x = (x * 10 + d) % m
            ans.append(0 if x else 1)
        return ans
''',
    call='Solution().divisibilityArray("998244353", 3)',
    expect=[1, 1, 0, 0, 0, 1, 1, 0, 0],
    views=[
        dict(type='string', var='word', label='word（蓝 = 正在读入的数字）', color=lambda S, i, v: 'blue' if 'd' in S and i == len(S['ans']) - (1 if S['_line'] == 7 else 0) else None, h=170),
        dict(type='array', var='ans', label='ans（1 = 前缀能被 m 整除）', h=170,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', fn=lambda S: f"`x = (x×10 + d) % m` ，当前余数 x = =={S['x']}==，m = {S['m']}" if 'x' in S else '', h=70),
    ],
    watch=['d', ('x', 'x', 'yellow'), 'm'],
    captions={
        'x = 0': '`x` 保存「当前前缀 % m」，空前缀余数为 0',
        'for d in map': '读入下一个数字',
        'x = (x * 10': '前缀接上数字 `{d}`：新前缀 = 旧前缀×10 + {d}；==取模后再算也不影响余数==：`({B.x}×10+{d}) % {m} = {x}`',
        'ans.append': lambda S, B, r: (f'余数 `x = {S.x}` ≠ 0 → 不能整除，记 `0`' if S.x else f'余数 `x = 0` → 前缀能被 `{S.m}` 整除，记 `1`'),
        'return ans': '遍历完，返回 `ans`',
    },
    cards=dict(
        one_liner='边读数字边取模，前缀再大也只存一个余数',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['数字串 `word` 和正整数 `m`，`div[i] = 1` 当且仅当 `word[0..i]` 表示的数能被 `m` 整除',
                 '前缀可能有 `10^5` 位，不能直接转成整数',
                 '示例：`"998244353"`，`m=3` → `[1,1,0,0,0,1,1,0,0]`'],
        quote='从左到右遍历 word。初始化 x=0，每遇到一个数字 d，就把 x 更新为 (10x+d) mod m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新前缀 = 旧前缀 ×10 + 新数字，同样的递推在模 `m` 意义下也成立',
              '所以只需维护 `x` = 当前前缀 `% m`',
              '`x == 0` 就是能整除'],
        summary=['时间 `O(n)`，空间 `O(1)`，返回值不计',
                 '易错：不要先转整数再取模，大数会很慢；每一步都取模',
                 '`ans.append(0 if x else 1)`：余数为 0 才记 1，别写反',
                 '同类：边遍历边维护余数的前缀题'],
    ),
)
