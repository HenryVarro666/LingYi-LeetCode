SETUP = '''
MX = 100_001
mu = [0] * MX
mu[1] = 1
for i in range(1, MX):
    for j in range(i * 2, MX, i):
        mu[j] -= mu[i]
divisors = [[] for _ in range(MX)]
for i in range(2, MX):
    if mu[i]:
        for j in range(i, MX, i):
            divisors[j].append(i)
'''


def _mu(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            r = -r
        p += 1
    return -r if n > 1 else r


def _txt(S):
    sv = S.get('selected_value')
    if sv is None or 'cost' not in S or 'max_num' not in S:
        return '`cnt_multi[d]` = nums 中是 d 的倍数的个数；与 sv 不互质 = 含 sv 的某个质因子'
    ds = [d for d in range(2, sv + 1) if sv % d == 0 and _mu(d) != 0 and d <= S['max_num']]
    return f"sv = =={sv}==，无平方因子的因子 d = {ds}；不互质个数 = −Σ μ(d)·cnt_multi(d)；cost = =={S['cost']}=="


CONFIG = dict(
    num=3953, title='互质元素的最大得分', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举选中的值 · 莫比乌斯容斥',
    tags=['灵神题单', '数学算法', '难度分 2390'],
    setup=SETUP,
    code='''
class Solution:
    def maxScore(self, nums: list[int], maxVal: int) -> int:
        max_num = max(nums)
        cnt = [0] * (max_num + 1)
        for x in nums:
            cnt[x] += 1

        cnt_multi = [0] * (max_num + 1)
        for i in range(2, max_num + 1):
            for j in range(i, max_num + 1, i):
                cnt_multi[i] += cnt[j]  # 统计 nums 中有多少个数是 i 的倍数

        # 单独计算 selected_value = 1 时的得分
        ans = 1 if cnt[1] > 0 else 0

        # 从大到小枚举 selected_value
        for selected_value in range(max(max_num, maxVal), 1, -1):
            # 优化：如果 selected_value <= ans，那么 ans 不会变大，跳出循环
            if selected_value <= ans:
                break

            if selected_value > maxVal and cnt[selected_value] == 0:
                continue  # 无法改成 selected_value

            # 与 selected_value 不互质的数，其中一个数改成 selected_value，其余数都改成 1
            cost = 0
            for d in divisors[selected_value]:
                if d > max_num:
                    break
                cost -= mu[d] * cnt_multi[d]

            if selected_value <= max_num and cnt[selected_value] > 0:
                cost -= 1  # 如果某个 nums[i] 恰好等于 selected_value，可以少改一次
            elif cost == 0:
                cost = 1  # 至少要有一个数改成 selected_value

            ans = max(ans, selected_value - cost)

        return ans
''',
    call='Solution().maxScore([2,3,3,6,5], 6)',
    expect=5,
    views=[
        dict(type='array', var='cnt', label='cnt[x]：x 在 nums 中出现几次', h=150, cell=70,
             pointers={'selected_value': 'pink'}),
        dict(type='array', var='cnt_multi', label='cnt_multi[d]：nums 中 d 的倍数有几个', h=150, cell=70,
             color=lambda S, i, v: 'cyan' if 'd' in S and i == S['d'] else None),
        dict(type='text', h=130, size=28, fn=_txt),
    ],
    watch=[('selected_value', 'selected_value', 'pink'), ('d', 'd', 'cyan'), ('cost', 'cost', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'max_num = max(nums)': '数组下标最大到 `max_num = {max_num}`',
        'cnt[x] += 1': '`cnt[{x}]` → {cnt[x]}',
        'cnt_multi[i] += cnt[j]': '`{j}` 是 `{i}` 的倍数，有 `{cnt[j]}` 个 → `cnt_multi[{i}] = {cnt_multi[i]}`',
        'ans = 1 if cnt[1] > 0 else 0': 'selected=1：有 1 就不用改，得分 1；否则改一个数为 1，得分 0 → `ans = {ans}`',
        'for selected_value in': '枚举选中的值 `selected_value = {selected_value}`（从大到小）',
        'if selected_value <= ans': lambda S, B, r: (f'`{S.selected_value} <= ans = {S.ans}`：得分最多 selected_value，不可能更大 → ==提前结束==' if S.selected_value <= S.ans
                                                     else f'`{S.selected_value} > ans = {S.ans}`：还有可能超过，继续'),
        'if selected_value > maxVal and': lambda S, B, r: (f'`{S.selected_value} > maxVal` 且 nums 里没有它 → 没法变成它，跳过' if S.selected_value > S.maxVal and S.cnt[S.selected_value] == 0
                                                           else '可以得到这个值（<= maxVal，或本来就在 nums 里）'),
        'cost = 0': '`cost` = 修改次数。思路：与它不互质的数，一个改成它，其余都改成 1',
        'for d in divisors': lambda S, B, r: ('因子都看完了：cost 就是“与它不互质的数的个数”' if 'd' in B and B.d == S.d and S.cost == B.cost else
                                              f'看无平方因子的因子 `d = {S.d}`（μ(d) = {_mu(S.d)}）'),
        'if d > max_num': '`d <= max_num`，继续',
        'cost -= mu[d] * cnt_multi[d]': lambda S, B, r: f'容斥：`cost -= μ({S.d}) × cnt_multi[{S.d}]` = `-({_mu(S.d)} × {S.cnt_multi[S.d]})` → `cost = {S.cost}`',
        'if selected_value <= max_num and cnt[selected_value] > 0': lambda S, B, r: (
            f'nums 里本来就有 `{S.selected_value}`，它自己不用改 → `cost -= 1`' if S.selected_value <= S.max_num and S.cnt[S.selected_value] > 0
            else f'nums 里没有 `{S.selected_value}`，看是否 `cost == 0`'),
        'cost -= 1': '少改一次：`cost = {cost}`',
        'elif cost == 0': lambda S, B, r: (f'`cost = 0`：所有数都与它互质但没有它 → 至少要改一个数' if S.cost == 0 else f'`cost = {S.cost}`：已经有要改的数（其中一个改成它）'),
        'cost = 1': '`cost = 1`：必须把一个数改成 selected_value',
        'ans = max(ans, selected_value - cost)': '得分 `{selected_value} - {cost} = {selected_value - cost}` → `ans = {ans}`',
        'return ans': '最大得分：`{ans}`',
    },
    skip=['for j in range(i'],
    max_steps=80,
    cards=dict(
        one_liner='枚举选中的值，用莫比乌斯容斥数出需要改成 1 的数',
        complexity='时间 `O(n + U log U)`（不计预处理），空间 `O(U)`',
        problem=['可把任意元素改成 `<= maxVal` 的正整数，每次代价 1',
                 '最后选一个下标 i，使 `nums[i]` 与其他数都互质',
                 '得分 = 选中的值 − 修改次数，求最大得分',
                 '示例：`nums=[3,4,6], maxVal=5` → `4`；本视频：`[2,3,3,6,5], maxVal=6` → `5`'],
        quote='与 6 不互质的数，必须包含质因子 2,3 中的至少一个。……如果直接计算 2+3=5，会多算一次交集（6 的倍数）的大小，所以要减去 1。这个计算过程叫做容斥原理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举选中的值 `sv`：与它不互质的数，一个改成 sv，其余改成 1（1 与谁都互质）',
              '不互质的个数 = 含质因子 p 的个数做容斥 = `-Σ μ(d)·cnt_multi(d)`',
              '特判：nums 里有 sv 少改一次；没有且都互质也得改一次；sv = 1 单独算'],
        summary=['时间 `O(n + U log U)`，U = max(max(nums), maxVal)',
                 'μ 和“无平方因子的因子列表”在函数外预处理（视频里放在 setup，不演示），按原文 `MX = 100_001`',
                 '从大到小枚举，`selected_value <= ans` 就可以 break',
                 '易错：`sv > maxVal` 时只能选 nums 里已有的；`cnt_multi[d]` 要先判 `d > max_num`'],
    ),
)
