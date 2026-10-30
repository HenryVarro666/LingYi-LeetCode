def _txt(S):
    if 'num_list' not in S:
        return '`s[k] = k × 10^(k−1)`：==k 位数（允许前导 0）里每个数位==出现 `d` 的总次数，`cnt[k]` 存的就是它'
    L = S.get('length')
    if L is None or 'index' not in S:
        return '把 `now` 拆成数位，从高位向低位逐位处理'
    i = S['index']
    d = S['d']
    rest = L - 1 - i
    if 'v' in S and S.get('_line', 0) in (24, 25, 26, 29, 30):
        return (f'固定前 `{i}` 位不变，这一位填 `v = {S["v"]}`（< `{S["num_list"][i]}`），右边 `{rest}` 位随便填：'
                f'`10^{rest} × (same + delta) + cnt[{rest}]`')
    return f'处理第 `{i}` 位（还剩右边 `{rest}` 位），`same` = 高位里等于 `d = {d}` 的个数'


def _pt(S):
    return S.get('index') if 'num_list' in S and 'length' in S else None


CONFIG = dict(
    num=1067, title='范围内的数字计数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='组合数学 · 逐位枚举 + cnt 预处理',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def digitsCount(self, d, low, high):

        cnt = [0]
        pow10 = [1]
        for index in range(1, len(str(high))):
            cnt.append(index * 10 ** (index - 1))
            pow10.append(pow10[-1] * 10)

        def calc(now):
            if now == 0:
                return 0
            
            num_list = [int(x) for x in str(now)]

            length = len(num_list)
            res = 0
            same = 0
            for index, digit in enumerate(num_list):
                digit = int(digit)
                for v in range(digit):
                    if v == d:
                        delta = 1
                    else:
                        delta = 0

                    if index != 0 or v > 0 or d > 0:
                        res += pow10[length - 1 - index] * (same + delta) + cnt[length - 1 - index]

                if digit == d:
                    same += 1

            if d == 0:
                for index in range(length - 1):
                    res += 9 * cnt[index]

            return res + same

        return calc(high) - calc(low - 1)
''',
    call='Solution().digitsCount(1, 3, 15)',
    expect=7,
    views=[
        dict(type='text', fn=_txt, size=24, h=90),
        dict(type='array', var=lambda S: S['num_list'] if 'num_list' in S else [], label='now 的各个数位 num_list（蓝 = 当前 index）', cell=100,
             pointers={'index': 'blue'}, h=230),
        dict(type='array', var='cnt', label='cnt[k] = k × 10^(k−1)（k 位数里 d 出现的总次数）', cell=100, h=170),
        dict(type='text', fn=lambda S: (f"累计 `res = {S['res']}`，`same = {S['same']}`" if 'res' in S and 'same' in S else ''), size=28, h=70),
    ],
    watch=['d', 'index', 'digit', 'v', 'delta', ('same', 'same', 'yellow'), ('res', 'res', 'green')],
    skip=['digit = int(digit)', 'delta = 1', 'delta = 0', 'now == 0', 'return 0', 'length = len', 'res = 0', 'same = 0',
          'pow10.append', 'cnt = [0]', 'pow10 = [1]', 'for v in range(digit)', 'if index != 0', 'same += 1', 'for index in range(length - 1)'],
    captions={
        'cnt.append': '`cnt[{index}] = {index} × 10^{index-1} = {cnt[index]}`',
        'num_list = [': '`now = {now}` 拆成数位：`{num_list}`',
        'for index, digit': lambda S, B, r: ('所有数位处理完' if B.get('index') == S.get('index') and B.get('digit') == S.get('digit') and 'index' in B and B.index == len(S.num_list) - 1
                                             else f'第 `{S.index}` 位：`digit = {S.digit}`，枚举这一位填 `v < {S.digit}`，右边随便填'),
        'if v == d': lambda S, B, r: (f'这一位填 `v = {S.v}`，等于 `d`：这一位自己多贡献 1 个 `d`' if S.v == S.d
                                      else f'这一位填 `v = {S.v}`，不等于 `d = {S.d}`：这一位不贡献'),
        'res += pow10': '（`index>0` 或 `v>0` 或 `d>0`，不是无效前导 0）右边 `{length-1-index}` 位：`10^{length-1-index} × (same + delta) + cnt[{length-1-index}]` = `{pow10[length-1-index]} × {same+(1 if v==d else 0)} + {cnt[length-1-index]}` → `res = {res}`',
        'if digit == d': lambda S, B, r: (f'`digit = {S.digit}` == `d`：前缀里多了一个 `d`，`same` 加 1' if S.digit == S.d
                                          else f'`digit = {S.digit}` ≠ `d = {S.d}`：`same` 不变'),
        'if d == 0': '`d = {d}`：{"d = 0 要另外补上位数更少的数" if d == 0 else "d 不是 0，不用单独处理前导 0"}',
        'return res + same': '`now` 自己里 `d` 出现 `same` 次，没被前面算进去，要补上：`{res} + {same}` = =={ret}==',
        'return calc(high)': '`calc(high) − calc(low − 1)`：先算 `high = {high}`，再算 `low − 1 = {low-1}`',
    },
    cards=dict(
        one_liner='用 k×10^(k−1) 预处理，逐位枚举“这一位比 now 小”的所有情况',
        complexity='时间 `O(log^2 high)`，空间 `O(log high)`',
        problem=['给定数字 `d`（0–9）和区间 `[low, high]`，求 `d` 在区间所有整数中==一共出现多少次==',
                 '示例：`d = 1, low = 3, high = 15`：`10~15` 里共出现 `7` 次',
                 '先转化为 `calc(high) − calc(low − 1)`'],
        quote='C(n, k) * k = n * C(n - 1, k - 1)……括号中的式子是二项式(9 + 1)^(n - 1)的展开，因此最终就有 s[n] = n * 10^(n - 1)',
        quote_src='—— yiduobo 题解',
        idea=['忽略前导 0，n 位数里有 k 个 d：`C(n,k)·9^(n−k)` 种，推出 ==s[n] = n·10^(n−1)==',
              '逐位枚举：这一位填 `v < digit`，右边随便填，贡献 `s[右边位数]`',
              '`same` 记前缀里 `d` 的个数，`delta` 记这一位 `v` 是否等于 `d`；`d = 0` 另外处理前导 0'],
        summary=['时间 `O(log^2 high)`：每位最多枚举 10 个 `v`',
                 '原文为 Python 2 风格写法，本代码已是 Python 3 可运行，无需改动',
                 '易错：`d = 0` 时前导 0 不能计入，要加 `for index in range(length - 1)` 补位数更少的数',
                 '最后要把 `same` 加上：`now` 自己没被枚举到'],
    ),
)
