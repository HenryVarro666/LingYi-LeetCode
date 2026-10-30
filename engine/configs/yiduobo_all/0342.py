def _info(S):
    n = S.get('num')
    if not isinstance(n, int):
        return ''
    if n <= 0:
        return f'`num = {n}`'
    return f'`num = {n}`，`1073741824 % {n} = {1073741824 % n}`，`{n} % 10 = {n % 10}`'


CONFIG = dict(
    num=342, title='4的幂', difficulty='Easy', category='位运算',
    author='yiduobo', technique='最大 4 的幂取模 + 末位',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def isPowerOfFour(self, num):

        if num <= 0:
            return False

        if num == 1:
            return True

        if 1073741824 % num == 0 and num % 10 in (4, 6):
            return True

        return False
''',
    call='[Solution().isPowerOfFour(n) for n in (16, 8, 1, 5)]',
    expect=[True, False, True, False],
    views=[
        dict(type='text', fn=lambda S: '最大的 4 的幂：`4^15 = 1073741824`；4 的幂（除 1 外）末位只能是 ==4== 或 ==6==', h=90),
        dict(type='array', var=lambda S: [4 ** k for k in range(6)], label='4 的幂：末位 1, 4, 6, 4, 6 ...', h=230, cell=120,
             color=lambda S, i, v: 'green' if 'num' in S and S['num'] == v else None),
        dict(type='array', var=lambda S: [2 * 4 ** k for k in range(5)], label='2 × 4 的幂：末位 2, 8, 2, 8 ... （要排除）', h=230, cell=120,
             color=lambda S, i, v: 'pink' if 'num' in S and S['num'] == v else None),
        dict(type='text', fn=_info, h=80),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        'if num <= 0': lambda S, B, r: f'`num = {S.num}`：4 的幂一定是正数，`num <= 0` 不成立，继续',
        'if num == 1': lambda S, B, r: ('`num == 1`：`4^0 = 1` 是 4 的幂，单独处理（1 的末位不是 4 或 6）→ True' if S.num == 1
                                       else '`num` 不是 1，继续往下判断'),
        '1073741824 % num': lambda S, B, r: (
            f'`1073741824 % {S.num} = {1073741824 % S.num}`'
            + ('，==整除== → num 是 2 的幂；' if 1073741824 % S.num == 0 else '，不能整除 → num 不是 2 的幂 → False')
            + (f'末位 `{S.num} % 10 = {S.num % 10}`' + ('，在 (4, 6) 里 → ==是 4 的幂== True' if S.num % 10 in (4, 6)
                                                    else '，不在 (4, 6)：是 2·4^k 形式（末位 2 或 8）→ 不是 4 的幂') if 1073741824 % S.num == 0 else '')),
        'return True': '返回 `True`',
        'return False': '返回 `False`',
    },
    cards=dict(
        one_liner='用最大的 4 的幂做整除，再用末位排除 2·4^k',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['判断整数是不是 4 的幂（`n == 4^x`）',
                 '例：`16` → `true`，`5` → `false`，`1` → `true`',
                 '本视频依次判断 `16, 8, 1, 5`'],
        quote='对于所有4的幂，除了4^0=1之外，其他幂都必然以4或者6结尾，那么对于4^k * 2这种形式就必然以2或者8结尾，于是在上面1073741824模n的基础上，再判断n%10是否等于4或者6即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算出 int 范围内最大的 4 的幂 `1073741824 = 4^15`',
              '它能被 `num` 整除，说明 `num` 是 2 的幂：4^k 或 2·4^k',
              '4^k 末位是 4 或 6（k≥1），2·4^k 末位是 2 或 8，用 `num % 10` 区分'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`num <= 0` 和 `num == 1` 要先单独处理',
                 '只靠整除不够：8 也整除 `4^15`，所以要再看末位',
                 '对比灵神：灵神用 `n & (n-1) == 0` 判 2 的幂，再用掩码或模 3 区分'],
    ),
)
