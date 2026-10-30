def _info(S):
    if 'digits' not in S or 'left' not in S:
        return '枚举前半部分 `left`，翻转拼接出整个回文数 `v`'
    if 'v' not in S or S['_line'] < 15:
        return f'前半部分 `{S["left"]}`，拼接中……'
    n, k = S['n'], S['k']
    v = S['v']
    s = f'回文数 `v = {v}`，`{v} % {k} = {v % k}`' + ('，是 k 的倍数' if v % k == 0 else '，不是倍数 → 跳过')
    return s


CONFIG = dict(
    num=3272, title='统计好整数的数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举回文前半 · 排序去重 · 阶乘去重复',
    tags=['组合数学', '难度分 2382'],
    code='''
class Solution(object):
    def countGoodIntegers(self, n, k):

        m = (n + 1) // 2
        start = 10 ** (m - 1)
        end = 10 ** m
        vis = set()
        fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
        res = 0
        for left in range(start, end):

            digits = list(str(left))
            right_digits = digits[::-1]
            if n % 2 == 0:
                digits.extend(right_digits)
            else:
                digits.extend(right_digits[1:])
            
            v = int(''.join(digits))

            if v % k == 0:
                h = int(''.join(sorted(digits, reverse=True)))
                if h in vis:
                    continue
                vis.add(h)

                
                cnt = {}
                for char in digits:
                    cnt[char] = cnt.get(char, 0) + 1

                if '0' in cnt:
                    x = fact[n - 1] * (n - cnt['0'])
                else:
                    x = fact[n]

                for c in cnt.values():
                    x //= fact[c]
                
                res += x
    
        return res
''',
    call='Solution().countGoodIntegers(4, 3)',
    expect=84,
    skip=['continue', 'for left in range', 'digits = list', 'right_digits =', 'digits.extend', 'for char in digits', 'cnt[char] =',
          'x //= fact[c]', 'for c in cnt.values()', 'start = 10', 'if n % 2 == 0', 'end = 10', 'fact = ['],
    max_steps=66,
    views=[
        dict(type='array', var='digits', label='digits：当前回文数的数位', h=150, cell=70),
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='set', var='vis', label='vis：已处理过的「排序后最大数」h', h=170, fmt=lambda x: str(x)),
        dict(type='map', var='cnt', label='cnt：数位 → 出现次数', h=140),
    ],
    watch=[('left', 'left', 'blue'), ('v', 'v', 'pink'), ('x', 'x', 'yellow'), ('res', 'res', 'green')],
    captions={
        'm = (n + 1) // 2': '要枚举的位数 `m = {m}`：偶数取一半，奇数多带中间一位',
        'vis = set()': '`vis` 去重：同一批数位只算一次',
        'res = 0': '`res` 累计好整数个数',
        'v = int(': '拼成整个回文数 `v = {v}`（前半 `{left}` + 翻转）',
        'if v % k == 0': lambda S, B, r: (f'`{S.v} % {S.k} = {S.v % S.k}` → ==是 k 的倍数，是 k 回文整数==' if S.v % S.k == 0
                                          else f'`{S.v} % {S.k} = {S.v % S.k}` → 不是倍数，下一个'),
        'h = int(': '数位从大到小排序得 `h = {h}`：数位相同的回文数，`h` 一定相同',
        'if h in vis': lambda S, B, r: (f'`{S.h}` 已在 `vis` → 这批数位的排列之前算过了，==跳过==' if S.h in S.vis else f'`{S.h}` 第一次见 → 要计算'),
        'vis.add(h)': '把 `{h}` 记进 `vis`',
        "cnt = {}": '`cnt` 统计每个数位出现的次数',
        "if '0' in cnt": lambda S, B, r: ('有 0：最高位不能是 0，选法 `n - cnt[0]`，其余位全排 `(n-1)!`' if '0' in S.cnt else '没有 0：最高位随便选，直接 `n!`'),
        'x = fact[n - 1]': '`x = {fact[n - 1]} × {n - cnt["0"]}` = =={x}==（含 0：最高位 {n - cnt["0"]} 种选择）',
        'x = fact[n]': '`x = n!` = =={x}==（没有 0，最高位 n 种选择）',
        'res += x': lambda S, B, r: ('再除以每个数位次数的阶乘 `' + ' × '.join(f'{c}!' for c in S.cnt.values()) + f'`：这批数位可形成 `x` = {S.x} 个整数；`res` = {B.res} + {S.x} = =={S.res}=='),
        'return res': '一共 `{ret}` 个好整数',
    },
    cards=dict(
        one_liner='反过来想：先造 k 回文数，再数它们数位能排成几个数',
        complexity='时间 `O(10^m · n log n)`，空间 `O(10^m)`',
        problem=['回文数且是 `k` 的倍数 → k 回文整数；数位重排能得到它的整数 → 好整数',
                 '前导 0 在重排前后都不允许',
                 '求 `n` 位好整数的个数；本视频 `n=4, k=3`'],
        quote='题目要求计算n位好整数的数目，而好整数是某个k回文整数数位重组后的结果，那么在这里不妨反过来，先找出n位的k回文整数，然后计算这些k回文整数在打乱数位后可以形成多少个不同的整数。',
        quote_src='—— yiduobo 题解原文',
        idea=['前半部分枚举 `10^(m-1)` ~ `10^m`，翻转拼接成回文数，判断 `% k`',
              '把数位排序后当哈希值 `h`，同一批数位只算一次',
              '计数：最高位 `n - cnt[0]` 种 × `(n-1)!`，再除以每个 `cnt[x]!`'],
        summary=['时间 `O(10^m · n log n)`，`m = (n+1)//2`',
                 '最高位不能为 0，次高位及以后不受影响',
                 '除以 `cnt[x]!` 是因为相同数位互换位置会算重',
                 '原文已用 `//` 整数除法，代码无需改动；对比灵神：灵神用 `factorial` 预处理、Counter 计数，yiduobo 直接手写阶乘表'],
    ),
)
