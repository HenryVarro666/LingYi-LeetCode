CONFIG = dict(
    num=1625, title='执行操作后字典序最小的字符串', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='裴蜀定理 + 枚举轮转', tags=['灵神题单', '数学算法', '难度分 1992'],
    code='''
class Solution:
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        s = list(map(int, s))
        n = len(s)
        step = gcd(b, n)
        g = gcd(a, 10)
        ans = [inf]

        def modify(start: int) -> None:
            ch = t[start]  # 最靠前的数字，越小越好
            # ch 可以变成的最小值为 ch%g
            # 例如 ch=5，g=2，那么 ch+2+2+2（模 10）后变成 1，不可能变得更小
            # 从 ch 到 ch%g，需要增加 inc（循环中会 %10 保证结果在 [0,9] 中）
            inc = ch % g - ch
            if inc:  # 优化：inc 为 0 时，t[j] 不变，无需执行 for 循环
                for j in range(start, n, 2):
                    t[j] = (t[j] + inc) % 10

        for i in range(0, n, step):
            t = s[i:] + s[:i]  # 轮转
            modify(1)  # 累加操作（所有奇数下标）
            if step % 2:  # 能对偶数下标执行累加操作
                modify(0)  # 累加操作（所有偶数下标）
            ans = min(ans, t)

        return ''.join(map(str, ans))
''',
    call='Solution().findLexSmallestString("5525", 9, 2)',
    expect='2050',
    views=[
        dict(type='array', var='s', h=170, label='s（数字）', cell=70),
        dict(type='array', var='t', h=170, label='t（当前轮转后 + 累加）', cell=70,
             pointers={'start': 'blue'}),
        dict(type='array', var='ans', h=170, label='ans（目前最小）', cell=70),
        dict(type='text', h=70, fn=lambda S: f"`step = gcd(b, n)` = =={S['step']}==，`g = gcd(a, 10)` = =={S['g']}==" if 'g' in S else ''),
    ],
    watch=['step', 'g', 'i', 'start', 'ch', 'inc'],
    captions={
        'step = gcd': '能轮转到最左边的下标必须是 `gcd(b, n)` 的倍数（裴蜀定理）：`step = {step}`',
        'g = gcd': '累加 `a` 若干次，数字只能变到同模 `gcd(a,10)` 的值：`g = {g}`',
        'ch = t[start]': '看最靠前的数字 `ch = {ch}`，它越小越好；它定了，同奇偶位的数也就定了',
        'inc = ch % g': '`ch` 最小能变成 `{ch} % {g} = {ch % g}`，需要增加 `inc = {inc}`',
        'if inc': lambda S, B, r: ('`inc` 不为 0，要对这一类下标统一累加' if S.inc else '`inc = 0`：已经最小，不用动'),
        't[j] = ': '`t[{j}]` 加上 `inc`（模 10）→ `{t[j]}`',
        'modify(1)': '对所有奇数下标做累加操作',
        'modify(0)': '`step` 是奇数：偶数下标也能轮到奇数位，所以偶数下标同样可以累加',
        'if step % 2': lambda S, B, r: ('`step` 为奇数，可以对偶数下标累加' if S.step % 2 else '`step` 为偶数，只能累加奇数下标'),
        't = s[i:]': '枚举轮转到最左边的下标 `i = {i}`，得到 `t = {t}`',
        'ans = min': '`ans = min(ans, t)` → `{ans}`：字典序更小的留下',
        'return': '最小字符串：=={ret}==',
    },
    cards=dict(
        one_liner='累加和轮转都只能到「模 gcd」的位置，枚举轮转即可',
        complexity='时间 `O(n^2 / gcd(b,n))`，空间 `O(n)`',
        problem=['数字串 `s`（偶数长），操作：奇数下标都加 `a`（模 10）、整体右移 `b` 位',
                 '可任意次、任意顺序，求字典序最小的结果',
                 '示例：`s="5525", a=9, b=2` → `"2050"`'],
        quote='[裴蜀定理] 指出，该方程有解，当且仅当 r−s1 是 g=gcd(a,10) 的倍数，所以 s1 可以变成的最小值为 s1 mod g。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从特殊到一般：先只累加。最靠前的数最小，其余同奇偶位跟着确定',
              '`ch` 能变成的最小值是 `ch % gcd(a,10)`',
              '再看轮转：只有下标是 `gcd(b,n)` 的倍数的位置能转到最左；`gcd` 为奇数时偶数位也能累加'],
        summary=['时间 `O(n^2 / gcd(b,n))`，空间 `O(n)`',
                 '易错：`inc` 要 `%10` 保持在 `[0,9]`；`gcd(b,n)` 为奇数时别忘了偶数下标',
                 '另一种写法：枚举累加值，配合最小表示法，时间 `O(D^2 n)`'],
    ),
)
