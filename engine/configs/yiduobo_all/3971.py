CONFIG = dict(
    num=3971, title='最大总价值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分最后一次选的价值 · 超出 m 的扣掉',
    tags=['二分算法', '难度分 2195'],
    code='''
class Solution(object):
    def maxTotalValue(self, value, decay, m):
        
        left = 0
        right = max(value)

        while left < right:
            mid = (left + right + 1) // 2
            cnt = 0
            for v, d in zip(value, decay):
                if v >= mid:
                    delta = v - mid
                    cnt += delta // d + 1
                    if cnt >= m:
                        break

            if cnt >= m:
                left = mid
            else:
                right = mid - 1
        
        mod = 10 ** 9 + 7
        res = 0
        cnt = 0
        for v, d in zip(value, decay):
            if v >= left:
                delta = v - left
                x = delta // d + 1
                cnt += x
                res = (res + (v + v - d * (x - 1)) * x // 2) % mod

        res = (res - (cnt - m) * left % mod + mod) % mod
        return res
''',
    call='Solution().maxTotalValue([6, 5, 4], [2, 1, 1], 4)',
    expect=19,
    views=[
        dict(type='array', var='value', label='value（蓝 = 当前遍历的下标）', cell=84, h=140,
             color=lambda S, i, x: 'blue' if S.get('v') == x else None),
        dict(type='array', var='decay', label='decay', cell=84, h=140,
             color=lambda S, i, x: 'blue' if S.get('d') == x and S.get('v') == S['value'][i] else None),
        dict(type='text', size=28, fn=lambda S: (
            f"二分最后一次选的价值：`[{S['left']}, {S['right']}]`" + (f"，`mid = {S['mid']}`" if 'mid' in S and not S.get('res') else '')
            if 'left' in S and 'right' in S else '')),
        dict(type='text', size=28, fn=lambda S: (
            f"累计价值 `res = {S['res']}`，已统计的个数 `cnt = {S['cnt']}`（要求 m = {S['m']}）" if 'res' in S and 'cnt' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('cnt', 'cnt', 'orange'), ('m', 'm', 'cyan'), ('res', 'res', 'green')],
    skip=['cnt = 0', 'delta = v', 'for v, d in zip', 'if v >= mid', 'if v >= left', 'mod = 10'],
    max_steps=100,
    captions={
        'left = 0': '二分「最后一次选的价值」`mid`：下界 `left = 0`',
        'right = max(value)': '上界 `right = max(value) = {right}`：最大的价值不会比它更大',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}` → 区间 `[{S.left}, {S.right}]` 还没收缩完' if S.left < S.right
                                               else f'`left = right = {S.left}` → 最后一次选的价值就是 =={S.left}=='),
        'mid = (left + right + 1)': '取上中位数 `mid = ({left} + {right} + 1) // 2` = =={mid}==（`left = mid` 时不会死循环）',
        'cnt += delta // d + 1': '该下标价值 `>= {mid}` 的次数：`({v} - {mid}) // {d} + 1` = =={(v-mid)//d+1}==，`cnt` → {cnt}',
        'if cnt >= m': lambda S, B, r: (
            (f'`cnt = {S.cnt} >= m = {S.m}`：价值 ≥ {S.mid} 的操作已经够 m 次 → 不用再数了' if S.cnt >= S.m
             else f'`cnt = {S.cnt} < m = {S.m}` → 还没够，看下一个下标') if S['_line'] == 14 else
            (f'`cnt = {S.cnt} >= m = {S.m}`：价值 ≥ {S.mid} 的操作够 m 次 → mid 可行，==往大处找==' if S.cnt >= S.m
             else f'`cnt = {S.cnt} < m = {S.m}`：价值 ≥ {S.mid} 的操作不够 m 次 → mid 太大，==往小处找==')),
        'break': '够 m 次了，跳出 for 循环',
        'left = mid': '操作次数够 m 次 → mid 还可以更大：`left` → {left}',
        'right = mid - 1': '操作次数不够 m 次 → mid 太大了：`right` → {right}',
        'x = delta // d + 1': '这个下标一直选到价值 `< {left}` 为止，共 `x = ({v} - {left}) // {d} + 1` = =={x}== 次',
        'cnt += x': '累计总操作数 `cnt` → {cnt}',
        'res = (res +': '等差数列求和 `({v} + {v} - {d}·({x}-1)) · {x} // 2`，`res` → =={res}==',
        'res = (res - (cnt - m)': lambda S, B, r: (f'价值等于 `left = {S.left}` 的操作被多算了 `cnt - m = {S.cnt - S.m}` 次 → 扣掉 `{S.cnt - S.m} × {S.left}`，`res` → =={S.res}==' if S.cnt > S.m
                                                   else f'`cnt = m = {S.cnt}`，没有多算的操作，`res` 保持 =={S.res}=='),
        'return res': '最大总价值（取模后）= =={ret}==',
    },
    cards=dict(
        one_liner='二分「最后一次选的价值」，多算的次数最后扣掉',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['每次操作选一个下标，把 `value[index]` 计入总价值，再让它减去 `decay[index]`',
                 '最多 m 次，求最大总价值，对 `10^9 + 7` 取模',
                 '本视频：`value=[6,5,4], decay=[2,1,1], m=4` → `19`'],
        quote='在这里不妨考虑最后一次添加到总价值中的元素值，这个值越小，可能执行的操作次数就越多，反之若这个值越大，可能执行的操作次数就越少。换言之，在这里可以直接二分这个最小元素值。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次都选当前最大的正数；m 太大不能模拟 → 二分最后选到的价值 `left`',
              '对每个下标算「价值 ≥ mid 要选几次」，次数之和 ≥ m 就把下界抬高',
              '确定 `left` 后用等差数列求和，==等于 left 的价值可能多算==，用 `(cnt - m) × left` 扣掉'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`mid` 取上中位数 `(left + right + 1) // 2`，因为分支是 `left = mid`',
                 '多算的次数 `cnt - m` 都恰好价值为 `left`，所以直接减 `(cnt - m) * left`',
                 '取模后相减要 `+ mod` 再取模，避免出现负数',
                 '原文为 Python 2 写法，本身已是 `//` 整除，无需改动'],
    ),
)
