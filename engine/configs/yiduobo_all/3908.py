CONFIG = dict(
    num=3908, title='有效数字整数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 分离数位 · flag 标记',
    code='''
class Solution(object):
    def validDigit(self, n, x):
        
        flag = False
        while n >= 10:
            if n % 10 == x:
                flag = True
            n //= 10
        
        return flag and n != x
''',
    call='Solution().validDigit(7050, 5)',
    expect=True,
    views=[
        dict(type='string', var=lambda S: str(S['n']), label='n 的各位数字（右端是当前末位）', h=200, cell=110,
             color=lambda S, i, v: ('green' if v == str(S['x']) else 'blue') if i == len(str(S['n'])) - 1 else None),
        dict(type='text', size=34, fn=lambda S: f"n = =={S['n']}==，x = `{S['x']}`" if 'n' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('flag = ==' + str(S['flag']) + '==') if 'flag' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('剩下的 n 小于 10，就是 ==开头那一位==' if S['n'] < 10 else '末位还要继续分离') if 'n' in S else ''),
    ],
    watch=['n', 'x', ('flag', 'flag', 'green')],
    captions={
        'flag = False': '`flag` 记录“分离过程中见没见过 x”，一开始没见过',
        'while n >= 10': lambda S, B, r: (f'`n = {S.n} >= 10`：继续分离' if S.n >= 10 else f'`n = {S.n} < 10`：分离结束，剩下的就是==首位=='),
        'if n % 10 == x': '`n % 10 = {n % 10}`，和 `x = {x}` 比较 → ' + '{"相等" if n % 10 == x else "不相等"}',
        'flag = True': '分离出了 `x`：`flag = True`',
        'n //= 10': '除以 10 去掉末位，`n = {n}`',
        'return': lambda S, B, r: f'`flag = {S.flag}`，首位 `{S.n}` 与 `x = {S.x}` 比较 → 返回 =={r}==',
    },
    cards=dict(
        one_liner='模 10 分离数位，剩下的那一位就是首位',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给整数 `n` 和数字 `x`：数字里至少有一个 `x`，且不以 `x` 开头才算有效',
                 '示例：`n=101, x=0` → `true`；`n=5, x=1` → `false`',
                 '本视频：`n=7050, x=5` → `true`'],
        quote='通过模10除以10的方法分离n中的所有数位，直到其小于10为止。若分离过程中出现了x，且最后剩下的元素不等于x，那么就说明n是有效的。',
        quote_src='—— yiduobo 题解原文',
        idea=['分离过程中见过 `x` → `flag` 置真',
              '直到 `n < 10` 停下，此时 `n` 是首位',
              '首位不能是 `x`，所以返回 `flag and n != x`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：首位不在循环里检查，只在最后和 `x` 比较',
                 '原文为 Python 2 风格，只写成 `class Solution(object)`，代码无需改动'],
    ),
)
