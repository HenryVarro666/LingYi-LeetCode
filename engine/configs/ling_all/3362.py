def _q(S):
    q = S.get('queries')
    return None if q is None else [f'{a}~{b}' for a, b in q]


CONFIG = dict(
    num=3362, title='零数组变换 III', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='贪心 · 最大堆选右端点 + 差分维护',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 2424'],
    code='''
class Solution:
    def maxRemoval(self, nums: List[int], queries: List[List[int]]) -> int:
        queries.sort(key=lambda q: q[0])  # 按照左端点从小到大排序
        h = []
        diff = [0] * (len(nums) + 1)
        sum_d = j = 0
        for i, x in enumerate(nums):
            sum_d += diff[i]
            # 维护左端点 <= i 的区间
            while j < len(queries) and queries[j][0] <= i:
                heappush(h, -queries[j][1])  # 取相反数表示最大堆
                j += 1
            # 选择右端点最大的区间
            while sum_d < x and h and -h[0] >= i:
                sum_d += 1
                diff[-heappop(h) + 1] -= 1
            if sum_d < x:
                return -1
        return len(h)
''',
    call='Solution().maxRemoval([2,0,2], [[0,2],[0,2],[1,1]])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（i = 当前位置，x 要被减到 0）', pointers={'i': 'blue'}, h=215),
        dict(type='array', var=_q, label='queries（l~r，按 l 排序，j = 下一个待入堆）', pointers={'j': 'pink'}, h=215, cell=110,
             dim=lambda S, i, v: S.get('j') is not None and i < S['j']),
        dict(type='heap', var='h', label='h（存右端点）', fmt=lambda x: f'r={-x}', h=150),
        dict(type='array', var='diff', label='diff（区间选中后在 r+1 处减一）', h=190),
    ],
    watch=['i', 'x', ('sum_d', 'sum_d', 'blue'), 'j', ('len(h)', 'len(h) if "h" in S else None', 'green')],
    captions={
        'queries.sort': '按左端点排序：这样可以用指针 `j` 依次取出「左端点 ≤ i」的区间',
        'h = []': '`h` 放右端点（取负数变最大堆）：右端点越大，后面能帮的越多',
        'diff = [0]': '`diff` 记录选中的区间在哪里失效',
        'sum_d = j = 0': '`sum_d` = 当前位置已被选中的区间覆盖的次数；`j` = 已入堆的区间数',
        'sum_d += diff[i]': '差分前缀和：`sum_d += diff[{i}]` → {sum_d}（走过右端点的区间不再覆盖 i）',
        'while j < len': '`j = {j}`：{"左端点 ≤ " + str(i) + " 的区间继续入堆" if j < len(queries) and queries[j][0] <= i else "没有更多左端点 ≤ " + str(i) + " 的区间了"}',
        'heappush': '区间 `[{queries[j][0]}, {queries[j][1]}]` 入堆，右端点 `{queries[j][1]}`（堆里存 `-{queries[j][1]}`）',
        'j += 1': '`j` → {j}',
        'while sum_d < x': lambda S, B, r: (f'`sum_d = {S.sum_d}` < `x = {S.x}` 且堆顶右端点 `{-S.h[0]} >= {S.i}` → 还要选一个区间' if S.sum_d < S.x and S.h and -S.h[0] >= S.i
                                       else (f'`sum_d = {S.sum_d} >= x = {S.x}`，覆盖够了，不再选' if S.sum_d >= S.x else '堆空了或堆顶右端点太小，选不了')),
        'sum_d += 1': '选中堆顶区间（右端点最大）：它覆盖 `i`，`sum_d` → =={sum_d}==',
        'diff[-heappop': '弹出堆顶，在 `r+1` 处差分减一：`diff[{B.h and -B.h[0] + 1}] -= 1`，过了右端点它就失效',
        'if sum_d < x': lambda S, B, r: (f'`{S.sum_d} < {S.x}`：选完所有可用区间仍不够 → 无法变成零数组，返回 -1' if S.sum_d < S.x
                                      else f'`{S.sum_d} >= {S.x}`：位置 {S.i} 满足，继续往右'),
        'return len(h)': '堆里剩下的都是没用上的区间 → 最多能删 `{len(h)}` 个',
    },
    cards=dict(
        one_liner='从左到右补覆盖，缺一个就从可用区间里挑右端点最大的，剩下的全能删',
        complexity='时间 `O(n + q log q)`，空间 `O(n + q)`',
        problem=['`queries[i] = [l, r]`：可把 `nums[l..r]` 里每个数最多减 1',
                 '删掉尽量多的 query，剩下的仍能把 `nums` 变成全 0',
                 '无法变成零数组返回 -1',
                 '示例：`nums=[2,0,2]`，`queries=[[0,2],[0,2],[1,1]]` → `1`'],
        quote='贪心地想，区间的右端点越大越好，后面的元素越小，后续操作就越少。所以选两个左端点为 0，且右端点最大的区间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右遍历：`nums[i] = x` 就需要 `x` 个覆盖 `i` 的区间',
              '缺的部分，从左端点 `<= i` 且没选的区间里选==右端点最大==的',
              '用最大堆装右端点；选中区间的覆盖数用差分 `diff` 维护',
              '最后堆里没被选的区间数 = 最多能删的个数'],
        summary=['时间 `O(n + q log q)`，空间 `O(n + q)`',
                 '先按左端点排序，用指针 `j` 把区间依次入堆',
                 '堆顶右端点 `< i` 时区间已失效，选不了，直接判无解',
                 '`diff` 开 `n+1`：区间右端点 `r = n-1` 时 `r+1 = n`',
                 '前置题：3355 零数组变换 I；同类反悔贪心：871 最低加油次数'],
    ),
)
