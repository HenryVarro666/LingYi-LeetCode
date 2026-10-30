NUMS = [1, 2, 3, 4]


def _isp(v):
    if v < 2:
        return False
    return all(v % d for d in range(2, int(v ** 0.5) + 1))


def _line(S):
    return list(range(0, 11))


def _color(S, i, v):
    return 'green' if _isp(v) else None


def _txt(S):
    if 'x' not in S or 'i' not in S:
        return '先用埃氏筛标记质数（预处理，不计入时间），再逐个位置检查'
    i, x = S['i'], S['x']
    need = '质数' if i % 2 == 0 else '非质数'
    now = '质数' if _isp(x) else '非质数'
    return f'下标 `{i}` 要 =={need}==；当前 `x = {x}` 是{now}；已操作 `ans = {S["ans"]}` 次'


CONFIG = dict(
    num=3896, title='将数组转换为交替质数数组的最少操作次数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='埃氏筛 + 暴力找下一个',
    tags=['灵神题单·数学算法', '难度分 1435'],
    code='''
MX = 100_004  # 1e5 的下一个质数是 1e5 + 3
is_prime = [0, 0] + [1] * (MX - 2)
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = 0

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        ans = 0
        for i, x in enumerate(nums):
            # 如果 i 是偶数，那么循环直到 is_prime[x] == 1（x 是质数）
            # 如果 i 是奇数，那么循环直到 is_prime[x] == 0（x 不是质数）
            while is_prime[x] == i % 2:
                ans += 1
                x += 1
        return ans
''',
    call=f'Solution().minOperations({NUMS})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=230, label='nums（蓝箭头 = 当前下标 i）'),
        dict(type='array', var=_line, pointers={'x': 'pink'}, color=_color, h=220, label='数轴 0..10（绿 = 质数，粉箭头 = 当前的 x）'),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计操作次数',
        'for i, x in enumerate': lambda S, B, r: ('`nums` 枚举完了，循环结束' if 'x' in B and B.i == S.i and S.i == len(S.nums) - 1 and B.x == S.x
                                                  else f'枚举下标 `{S.i}` 和值 `x = {S.x}`：偶数下标要质数，奇数下标要非质数'),
        'while is_prime[x]': lambda S, B, r: (
            f'`is_prime[{S.x}] = {1 if _isp(S.x) else 0}`，`i % 2 = {S.i % 2}`：相等 → ==不满足要求==，还得加 1'
            if (1 if _isp(S.x) else 0) == S.i % 2 else
            f'`is_prime[{S.x}] = {1 if _isp(S.x) else 0}`，`i % 2 = {S.i % 2}`：不相等 → 已满足，看下一个位置'),
        'ans += 1': '加 1 一次要 1 次操作：`ans` → {ans}',
        'x += 1': '`x` 加 1 变成 {x}，再回去检查是否满足',
        'return ans': '全部检查完，最少操作 `{ans}` 次',
    },
    cards=dict(
        one_liner='筛出质数表，不满足就一直加 1',
        complexity='时间 `O(nG)`，空间 `O(1)`（不计预处理）',
        problem=['偶数下标要 ==质数==，奇数下标要 ==非质数==；一次操作把某元素加 1',
                 '求最少操作次数',
                 '示例：`[1,2,3,4]` → `3`（1→2 一次，2→4 两次）'],
        quote='用埃氏筛预处理每个数是不是质数。如何找下一个质数（非质数）？可以暴力枚举，也可以在质数列表中二分查找。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个位置互相独立：各自往后加到满足条件的最近的数',
              '`while is_prime[x] == i % 2`：偶数位要 1、奇数位要 0，相等就说明还不对',
              '质数间隔很小（≤ 72），所以暴力加 1 就够快'],
        summary=['预处理 `is_prime` 要多筛到 `1e5 + 3`，因为 `1e5` 本身可能要变成下一个质数',
                 '时间 `O(nG)`，`G ≤ 72` 是最大质数间隔',
                 '易错：`1` 不是质数，偶数下标放 1 要加到 2',
                 '也可以在质数列表里二分找下一个'],
    ),
)
