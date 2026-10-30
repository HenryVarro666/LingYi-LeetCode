CONFIG = dict(
    num=1798, title='你能构造出连续值的最大数目', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 归纳', tags=['灵神题单', '难度分 1931'],
    code='''
class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        m = 0  # 一开始只能构造出 0
        coins.sort()
        for c in coins:
            if c > m + 1:  # coins 已排序，后面没有比 c 更小的数了
                break  # 无法构造出 m+1，继续循环没有意义
            m += c  # 可以构造出区间 [0,m+c] 中的所有整数
        return m + 1  # [0,m] 中一共有 m+1 个整数
''',
    call='Solution().getMaximumConsecutive([1,4,10,3,1])',
    expect=20,
    views=[
        dict(type='text', fn=lambda S: f"已能构造 ==[0, {S['m']}]== 的所有整数" if 'm' in S else '', size=34),
        dict(type='array', var='coins', label='coins（排序后）', h=220),
        dict(type='text', fn=lambda S: f"当前硬币 c = {S['c']}，需要 c <= m + 1 = {S['m']+1}" if 'c' in S else '', size=30),
    ],
    watch=[('m', 'm', 'cyan'), 'c'],
    captions={
        'm = 0': '一开始只能构造出 `0`，所以 `m = 0`',
        'coins.sort()': '先排序：==有序是强大的性质==，后面没有比 `c` 更小的了 → `{coins}`',
        'for c in coins': '取最小的未用硬币 `c = {c}`',
        'if c > m + 1': lambda S, B, r: (f'`c = {S.c} > m + 1 = {S.m+1}`：构造不出 `m+1`，后面的更大也不行 → 成立' if S.c > S.m + 1
                                         else f'`c = {S.c} <= m + 1 = {S.m+1}`：没有缺口，继续'),
        'break': '无法构造出 `m+1`，继续循环没有意义，退出',
        'm += c': '`[0,m]` 整体平移 `c` 得 `[c,m+c]`，与 `[0,m]` 接上 → 能构造 `[0, {m}]`',
        'return m + 1': '`[0, {m}]` 共 `{m} + 1 = {ret}` 个整数',
    },
    cards=dict(
        one_liner='排序后从小到大加硬币，只要不超过 m+1 区间就连续',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数组 `coins` 里选出一部分硬币求和，就能「构造」出这个和',
                 '求从 `0` 开始最多能构造出多少个连续整数',
                 '示例：`[1,4,10,3,1]` → `20`'],
        quote='有序是一个强大的性质，如果对数组排序不影响答案的话，可以尝试将数组排序后，再重新思考，看看能否发现新的思路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m` 表示 `[0,m]` 都能构造；排序后依次看硬币 `c`',
              '`c <= m+1`：平移后能接上，`m += c`',
              '`c > m+1`：`m+1` 永远造不出（后面更大），直接 `break`'],
        summary=['时间 `O(n log n)`，瓶颈在排序',
                 '易错：返回的是个数 `m + 1`，因为 0 也算',
                 '条件是 `c > m + 1` 才断，不是 `c > m`',
                 '同类题：330 按要求补齐数组'],
    ),
)
