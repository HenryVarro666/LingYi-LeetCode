CONFIG = dict(
    num=3814, title='预算下的最大总容量', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针 + 前缀最大值',
    tags=['滑动窗口与双指针', '单调栈', '难度分 1796'],
    code='''
class Solution:
    def maxCapacity(self, costs: List[int], capacity: List[int], budget: int) -> int:
        # 把 costs[i] 和 capacity[i] 绑在一起排序
        a = [(cost, cap) for cost, cap in zip(costs, capacity) if cost < budget]  # 太贵的机器直接忽略
        a.sort(key=lambda p: p[0])  # 按照价格从小到大排序

        pre_max = [0] * (len(a) + 1)
        ans = l = 0
        # 枚举买机器 r
        for r in range(len(a) - 1, -1, -1):
            while l < r and a[l][0] + a[r][0] < budget:
                pre_max[l + 1] = max(pre_max[l], a[l][1])
                l += 1
            # 循环结束后，下标在范围 [0, min(l-1, r-1)] 中的机器都可以买
            ans = max(ans, pre_max[min(l, r)] + a[r][1])
        return ans
''',
    call='Solution().maxCapacity([4,8,5,3,6], [1,5,2,7,4], 9)',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"买 r={S['r']}（价 {S['a'][S['r']][0]}，容量 {S['a'][S['r']][1]}）+ 左边最大容量 `pre_max[{min(S['l'], S['r'])}]` = =={S['pre_max'][min(S['l'], S['r'])]}==" if 'r' in S and 'l' in S and 'a' in S else '')),
        dict(type='array', var=lambda S: [p[0] for p in S['a']] if 'a' in S else [], label='价格（已排序）',
             pointers={'l': 'blue', 'r': 'pink'}, h=170,
             color=lambda S, i, v: ('blue' if i == S.get('l') else 'pink' if i == S.get('r') else None) if 'r' in S else None),
        dict(type='array', var=lambda S: [p[1] for p in S['a']] if 'a' in S else [], label='容量', h=150,
             color=lambda S, i, v: 'pink' if i == S.get('r') else None),
        dict(type='array', var='pre_max', label='pre_max（pre_max[k] = 前 k 台中最大容量）', h=170,
             color=lambda S, i, v: 'green' if 'l' in S and 'r' in S and i == min(S['l'], S['r']) else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'a = [(cost': '把价格和容量绑成 `(cost, cap)`，`cost >= budget` 的机器连一台都买不起，直接丢掉：剩 `{len(a)}` 台',
        'a.sort': '按价格从小到大排序，价格便宜的机器都挤在左边：`{a}`',
        'pre_max = [0]': '`pre_max[k]` 表示前 `k` 台里的最大容量，`pre_max[0] = 0` 当哨兵（等于不买第二台）',
        'for r in range': '枚举“最贵的那台” `r = {r}`：另一台只能在它左边',
        'while l < r and': lambda S, B, ret: (f"`a[l] + a[r]` = `{S.a[S.l][0]} + {S.a[S.r][0]}` = {S.a[S.l][0] + S.a[S.r][0]} < {S.budget}：`l` 这台买得起 → 继续右移" if S.l < S.r and S.a[S.l][0] + S.a[S.r][0] < S.budget else (f"`l = {S.l}` 追上 `r`：左边的机器都能买，停" if S.l >= S.r else f"`{S.a[S.l][0]} + {S.a[S.r][0]}` = {S.a[S.l][0] + S.a[S.r][0]} >= {S.budget}：再往右就买不起了，停")),
        'pre_max[l + 1] =': '`l` 这台已经确认能和 `r` 搭配，并入前缀最大值：`pre_max[{l+1}] = {pre_max[l+1]}`',
        'l += 1': '`l` 右移到 {l}：价格只会越来越大，==r 变小时 l 不用回头==',
        'ans = max': '`ans = max({B.ans}, pre_max[{min(l, r)}] + {a[r][1]}) = =={ans}==`：`l` 左边都能买，取其中最大容量',
        'return ans': '最大总容量 `{ans}`',
    },
    cards=dict(
        one_liner='排序后用相向双指针，前缀最大值直接给出另一台的最优容量',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['最多买两台机器，总成本必须 ==严格小于== `budget`，让总容量最大',
                 '示例：`costs=[4,8,5,3]`，`capacity=[1,5,2,7]`，`budget=8` → `8`',
                 '本视频：`costs=[4,8,5,3,6]`，`capacity=[1,5,2,7,4]`，`budget=9` → `9`'],
        quote='把机器按照价格从小到大==排序==，那么价格小于 budget - costs[i] 的机器在数组中是==连续==的，方便处理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举买的机器 `r`（当作价格较高那台），另一台必须在它左边，且价格 `< budget - 价格(r)`',
              '`r` 变小 → 允许的价格上限变大 → 左指针 `l` 只增不减，用相向双指针',
              '`l` 左边的机器容量不是有序的，所以维护前缀最大值 `pre_max`'],
        after=[dict(heading='另外两种写法', lines=['二分：对每个 `i` 在 `[0, i-1]` 二分，同样配合 `pre_max`',
                                                '单调栈：容量不比栈顶大的机器又贵又差，直接丢弃'])],
        summary=['时间 `O(n log n)`，瓶颈在排序；双指针本身 `O(n)`',
                 '`l` 与 `r` 取 `min(l, r)`：保证不会选到同一台机器',
                 '`pre_max[0] = 0` 对应只买一台；价格必须严格小于 `budget`',
                 '同类题：2824 统计和小于目标的下标对数目'],
    ),
)
