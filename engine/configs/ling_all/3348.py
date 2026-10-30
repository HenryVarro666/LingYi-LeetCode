NUM, T = '126', 24


def _digits(S):
    s = S.get('s')
    if s is None:
        return list(NUM)
    return [int(c) for c in s]


def _txt(S):
    if 'left_t' not in S:
        return f'目标：找 `≥ {NUM}` 的最小无零数，数位乘积是 `t = {T}` 的倍数；`t` 只能含质因子 2、3、5、7'
    if 'i' not in S or not isinstance(S.get('s'), list):
        return '`left_t[i]`：不改 `s` 的前 `i` 位时，后面还需要凑出的乘积（`t` 去掉已有的因子）'
    i = S['i']
    tt = S.get('tt')
    if tt is None:
        return f'从右往左试着增大 `s[{i}]`，它右边的位置就能随便填'
    return f'前 `{i}` 位不动，`s[{i}] = {S["s"][i]}`，后面还需凑出乘积 `tt = {tt}` 的倍数'


def _col(S, j, v):
    if 'i' not in S or not isinstance(S.get('s'), list):
        return None
    if j == S['i']:
        return 'blue'
    if j > S['i'] and S.get('_line', 0) >= 26:
        return 'green' if j >= S.get('j', 99) else None
    return None


CONFIG = dict(
    num=3348, title='最小可整除数位乘积 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='从右到左枚举修改位 + 贪心凑因子',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 3101'],
    code='''
class Solution:
    def smallestNumber(self, s: str, t: int) -> str:
        tmp = t
        for i in range(9, 1, -1):
            while tmp % i == 0:
                tmp //= i
        if tmp > 1:  # t 包含大于 7 的质因子
            return "-1"

        n = len(s)
        left_t = [0] * (n + 1)
        left_t[0] = t
        i0 = n - 1
        for i, c in enumerate(s):
            if c == '0':
                i0 = i
                break
            left_t[i + 1] = left_t[i] // gcd(left_t[i], int(c))
        if left_t[n] == 1:  # s 的数位之积已经是 t 的倍数
            return s

        # 假设答案和 s 一样长
        s = list(map(int, s))
        for i in range(i0, -1, -1):
            for s[i] in range(s[i] + 1, 10):
                tt = left_t[i] // gcd(left_t[i], s[i])
                k = 9
                for j in range(n - 1, i, -1):
                    while tt % k:
                        k -= 1
                    tt //= k
                    s[j] = k
                if tt == 1:
                    return ''.join(map(str, s))

        # 答案一定比 s 长
        ans = []
        for i in range(9, 1, -1):
            while t % i == 0:
                ans.append(str(i))
                t //= i
        return ''.join(ans[::-1]).rjust(n + 1, '1')  # 前面补 1
''',
    call=f'Solution().smallestNumber({NUM!r}, {T})',
    expect='138',
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var=_digits, label='s（蓝 = 正在增大的位 i，绿 = 右边已经凑好的位）', cell=100,
             pointers={'i': 'blue'}, color=_col, h=230),
        dict(type='array', var=lambda S: S.get('left_t', []), label='left_t[i]（前 i 位不动时，后面还要凑的乘积）', cell=100,
             pointers={'i': 'blue'}, h=230),
    ],
    watch=['t', 'i', 'tt', 'k', 'j'],
    skip=['tmp = t', 'for i in range(9, 1, -1)', 'while tmp % i == 0', 'tmp //= i', 'n = len(s)', 'left_t = [0]', 'left_t[0] = t',
          'i0 = n - 1', 'for i, c in enumerate(s)', "if c == '0'", 'while tt % k', 'k -= 1', 'for j in range(n - 1, i, -1)'],
    captions={
        'if tmp > 1': '把 `t` 里的 9..2 都除干净，剩下的 `tmp = {tmp}` 为 1，说明只含质因子 2、3、5、7 → 答案存在',
        'left_t[i + 1] =': '`left_t[{i + 1}] = {left_t[i]} / gcd({left_t[i]}, {c})` = {left_t[i + 1]}：`s[{i}] = {c}` 带来的因子先抵消掉',
        'if left_t[n] == 1': lambda S, B, r: (f'`left_t[{S.n}] = {S.left_t[S.n]}` ≠ 1：`s` 的数位乘积还不是 `t` 的倍数，必须改' if S.left_t[S.n] != 1
                                              else '`left_t[n] = 1`：`s` 自己就满足 → 直接返回'),
        'return s': '无需修改，直接返回 `s`',
        's = list(map(int, s))': '假设答案和 `s` 一样长：转成数字列表，从右往左找==最靠右的可增大位==',
        'for i in range(i0': lambda S, B, r: (f'尝试增大第 `i = {S.i}` 位：改得越靠右，答案越小；右边的位可以随便填' if S.i != B.get('i') or 'tt' not in B
                                              else '所有位都试过，答案一定比 `s` 长'),
        'for s[i] in range': lambda S, B, r: (f'把 `s[{S.i}]` 增大到 `{S.s[S.i]}`' if S.s[S.i] != B.s[S.i]
                                              else f'`s[{S.i}]` 增大到 9 都不行 → 放弃这一位，往左找'),
        'tt = left_t[i]': '前 `{i}` 位不动、`s[{i}] = {s[i]}` 后，还差乘积 `{tt}` 的倍数（`left_t[{i}] / gcd(left_t[{i}], {s[i]})`），右边有 `{n - 1 - i}` 位可以填',
        'k = 9': '右边的位从右往左填：从 9 往下找能整除 `tt` 的数（大数放右边答案才小）',
        'tt //= k': '找到 `k = {k}` 能整除 `tt = {B.tt}`：`tt = {B.tt} / {k}` = {tt}',
        's[j] = k': '`s[{j}] = {k}`：大数放在右边，让数字尽量小',
        'if tt == 1': lambda S, B, r: ('`tt = 1`：右边凑齐了，整串乘积是 `t` 的倍数 → 找到答案' if S.tt == 1
                                       else f'`tt = {S.tt}` ≠ 1：' + (f'右边 {S.n - 1 - S.i} 位凑不够' if S.n - 1 - S.i else '右边没有位置可填了') + ' → 这个值不行，试更大的'),
        "return ''.join(map(str, s))": '把列表拼成字符串返回：=={ret}==',
    },
    cards=dict(
        one_liner='从右往左找最靠右能增大的位，右边的位用大数凑因子',
        complexity='时间 `O(n + D log² t)`，空间 `O(n)`',
        problem=['给定正整数字符串 `num` 和整数 `t`，找 `≥ num` 的==最小无零整数==（不含数字 0）',
                 '要求各数位的乘积能被 `t` 整除；找不到返回 `"-1"`',
                 '示例：`num = "1234", t = 256` → `"1488"`；视频用 `num = "126", t = 24` → `"138"`'],
        quote='倒着枚举 i，尝试增加 s[i]……然后在 j=n−1,n−2,n−3,…,i+1 中填入数字，填入的方式是枚举 s[j]=9,8,7,…,1，如果发现 s[j] 可以整除 t，则更新 t 为 t/s[j]。这种填法可以保证我们把大的数字填在了右边，从而使答案尽量小。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['数位乘积只有质因子 2、3、5、7，`t` 含别的质因子就无解',
              '`left_t[i]`：`s` 的前 `i` 位不动时，剩下还要凑的乘积',
              '从右往左找第一个能把 `s[i]` 增大的位，右边的位随便填：用 9、8、…、1 贪心凑，大数放右边'],
        summary=['时间 `O(n + D log² t)`，空间 `O(n)`；方法一是带 `isLimit` 的暴搜，更直观但慢一些',
                 '`s` 中有 `0` 时必须修改，所以从最左边的 `0` 开始往左枚举（`i0`）',
                 '都不行时答案比 `s` 长：把 `t` 分解成 9..2，倒序后左边补 `1`',
                 '易错：`gcd` 抵消的是已有的因子；填数时要从大到小找能整除 `tt` 的数'],
    ),
)
