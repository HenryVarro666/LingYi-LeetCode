def _txt(S):
    if 'mid' in S and 's' in S:
        if 'x' in S and 'c' in S:
            ok = S['s'] >= S['mid']
            return f"累计出现次数 `s = {S['s']}`，要到 `mid = {S['mid']}`：{'==到了，x 就是加权中位数==' if ok else '还没到，继续累加'}"
        return f"总次数 `{sum(c for _, c in S['a'])}`，上取整的一半 `mid = {S['mid']}`"
    if 'a' in S:
        return '把 `cost[i]` 当成 `nums[i]` 出现的次数'
    return ''


CONFIG = dict(
    num=2448, title='使数组相等的最小开销', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='加权中位数贪心',
    tags=['贪心与思维', '难度分 2005'],
    code='''
class Solution:
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        a = sorted(zip(nums, cost))
        s, mid = 0, (sum(cost) + 1) // 2
        for x, c in a:
            s += c
            if s >= mid:
                return sum(abs(y - x) * c for y, c in a)  # 把所有数都变成 x
''',
    call='Solution().minCost([1,3,5,2,7], [2,3,1,4,3])',
    expect=22,
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='array', var=lambda S: [x for x, c in S['a']] if 'a' in S else None, h=215, label='nums（按值排序）',
             color=lambda S, i, v: ('green' if S['s'] >= S['mid'] else 'yellow') if 'x' in S and 'c' in S and S['a'][i][0] == S['x'] and S['a'][i][1] == S['c'] else None),
        dict(type='array', var=lambda S: [c for x, c in S['a']] if 'a' in S else None, h=215, label='cost（= 出现次数）',
             color=lambda S, i, v: ('green' if S['s'] >= S['mid'] else 'yellow') if 'x' in S and 'c' in S and S['a'][i][0] == S['x'] and S['a'][i][1] == S['c'] else None),
    ],
    watch=['s', 'mid', ('x', 'x', 'yellow'), ('c', 'c', 'pink')],
    captions={
        'a = sorted': '`nums` 和 `cost` 绑在一起按 `nums` 排序：`a = {a}`',
        's, mid =': '`cost` 总和 `{sum(cost)}`，`mid = ({sum(cost)} + 1) // 2 = {mid}`：==上取整==，累加到它就越过了一半',
        's += c': '累加出现次数：`s` → {s}（`x = {x}` 这个值出现了 `{c}` 次）',
        'if s >= mid': '`s = {s}` {">=" if s >= mid else "<"} `mid = {mid}` → {"==找到中位数 x=" + str(x) + "==" if s >= mid else "还没过一半，看下一个数"}',
        'return sum': '全变成 `x = {x}`：每个数代价 `|y − {x}| × cost` 加起来 = =={ret}==',
    },
    cards=dict(
        one_liner='把 cost 当出现次数，所有数都变成加权中位数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次可把 `nums` 中任一元素 ±1，第 `i` 个元素每次开销 `cost[i]`',
                 '求让所有元素相等的最小总开销',
                 '示例：`nums=[1,3,5,2], cost=[2,3,1,14]` → `8`',
                 '本视频：`[1,3,5,2,7], [2,3,1,4,3]` → `22`'],
        quote='把 cost[i] 理解成 nums[i] 的出现次数。根据中位数贪心及其证明，把所有数变成中位数是最优的。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`cost[i]` 就是 `nums[i]` 出现的次数，问题变成「重复数组」求中位数',
              '排序后不断累加 `cost`，首次 `>= ceil(sum/2)` 的那个数就是中位数',
              '再按定义算一遍总开销即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`mid = (sum(cost) + 1) // 2` 要上取整，否则可能提前停',
                 '方法一：排序后枚举目标值，用变化量 `(sum_cost − 2·cost) × 差` 递推 total，也是 `O(n log n)`',
                 '同类题：2033（单位开销）、462'],
    ),
)
