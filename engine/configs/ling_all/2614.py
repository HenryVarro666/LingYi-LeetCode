def _diag(S, i, j, v):
    if 'i' not in S or 'nums' not in S:
        return None
    n = len(S['nums'])
    if S['i'] >= n:
        return None
    if j == S['i'] or j == n - 1 - S['i']:
        return 'blue' if i == S['i'] else None
    return None


CONFIG = dict(
    num=2614, title='对角线上的质数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='试除到 sqrt(n) 判质数',
    tags=['灵神题单', '难度分 1375'],
    code='''
class Solution:
    def is_prime(self, n: int) -> bool:
        for i in range(2, isqrt(n) + 1):
            if n % i == 0:
                return False
        return n >= 2  # 1 不是质数

    def diagonalPrime(self, nums: List[List[int]]) -> int:
        ans = 0
        for i, row in enumerate(nums):
            for x in row[i], row[-1 - i]:
                if x > ans and self.is_prime(x):
                    ans = x
        return ans
''',
    call='Solution().diagonalPrime([[1,2,3],[5,6,7],[9,10,11]])',
    expect=11,
    views=[
        dict(type='text', fn=lambda S: (f"当前检查 `x = {S['x']}`，只试除 `2 ~ isqrt(x)`" if 'x' in S and S.get('_inner', {}).get('n') is None
                                         else (f"判断 `n = {S['_inner']['n']}` 是否为质数" if S.get('_inner', {}).get('n') is not None else '')), size=26),
        dict(type='grid', var='nums', label='nums（蓝 = 当前行的两个对角线位置）', cell=110, h=330,
             color=_diag, cursors=[('i', 'i', 'blue'), ('i', 'len(nums) - 1 - i', 'pink')]),
        dict(type='text', fn=lambda S: f"当前最大质数 `ans = {S['ans']}`" if 'ans' in S else '', size=28),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('ans', 'ans', 'green')],
    captions={
        'for i in range(2, isqrt(n) + 1)': '试除 `i = {i}`（只需枚举到 `isqrt({n}) = {isqrt(n)}`：因子成对出现，较小的那个一定不超过根号 n）',
        'if n % i == 0': '`{n} % {i} = {n % i}` → ' + '{"==能整除，不是质数==" if n % i == 0 else "不能整除，继续"}',
        'return False': '`{n}` 有因子 `{i}` → 不是质数',
        'return n >= 2': lambda S, B, r: (f'没有因子，但 `n = {S.n} < 2`：==1 不是质数== → `False`' if S.n < 2
                                          else f'试除到 `isqrt({S.n})` 都没有因子 → `{S.n}` 是质数'),
        'ans = 0': '`ans` 记录目前见到的最大对角线质数',
        'for i, row in enumerate': '第 `{i}` 行：对角线上的数是 `row[{i}]` 和 `row[{-1 - i}]`',
        'for x in row[i]': '对角线元素轮流检查：`x = {x}`（先主对角线、再副对角线）',
        'if x > ans': lambda S, B, r: (f'`x = {S.x} > ans = {S.ans}`：有可能刷新答案 → 再判断质数' if S.x > S.ans
                                       else f'`x = {S.x} <= ans = {S.ans}`：即使是质数也不会让答案更大 → ==不用判断质数==，省一次试除'),
        'ans = x': '`x` 是质数且更大 → `ans = {ans}`',
        'return ans': '两条对角线都看完，最大质数 `{ans}`',
    },
    cards=dict(
        one_liner='沿两条对角线走一遍，比 ans 大才去试除判质数',
        complexity='时间 `O(n√U)`，空间 `O(1)`',
        problem=['二维数组 `nums`，找出位于==至少一条对角线==上的最大质数，没有则返回 `0`',
                 '主对角线 `nums[i][i]`，副对角线 `nums[i][n-i-1]`',
                 '示例：`[[1,2,3],[5,6,7],[9,10,11]]` → `11`'],
        quote='其实只需枚举 [2, floor(sqrt(n))] 中的整数 i。……如果元素 x 没有超过答案 ans，那么无需判断 x 是否为质数，因为它不会让答案变得更大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['质因子成对出现：有大因子 `j` 就一定有小因子 `n/j < j`，所以试除到根号 n 即可',
              '遍历每行的 `row[i]` 和 `row[-1-i]`，就是两条对角线',
              '先比大小再判质数：不可能刷新答案的数直接跳过'],
        summary=['时间 `O(n√U)`，`U` 为对角线上的最大值，空间 `O(1)`',
                 '易错：==1 不是质数==，所以最后写 `return n >= 2`',
                 '`n` 很小而 `U` 较大（4×10^6），直接试除比筛质数更合适',
                 '奇数 n 时中心格在两条对角线上，会判断两次，不影响结果'],
    ),
)
