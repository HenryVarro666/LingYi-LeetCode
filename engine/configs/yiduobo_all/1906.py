def _present(S):
    nums = S.get('nums') or []
    return {k: v for k, v in S['pos_dict'].items() if k in nums}


CONFIG = dict(
    num=1906, title='查询差绝对值的最小值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='每个值一份前缀个数 · 枚举 1..100 找相邻值',
    tags=[],
    code='''
class Solution(object):
    def minDifference(self, nums, queries):

        pos_dict = {}
        for num in range(1, 101):
            pos_dict[num] = [0]
        pos_dict[nums[0]][0] = 1
        for index in range(1, len(nums)):
            for num in range(1, 101):
                pos_dict[num].append(pos_dict[num][-1])
            pos_dict[nums[index]][-1] += 1

        res = []        
        for x, y in queries:
            last = None
            now = None
            for num in range(1, 101):
                cnt = pos_dict[num][y]
                if x > 0:
                    cnt -= pos_dict[num][x - 1]
                if cnt > 0:
                    if last is not None and ((now is None) or (now > num - last)):
                        now = num - last
                    last = num
        
            if now is None:
                res.append(-1)
            else:
                res.append(now)
        
        return res
''',
    call='Solution().minDifference([4,5,2,2,7], [[0,2],[2,3]])',
    expect=[1, -1],
    skip=[5, 6, 9, 10, 17, 18, 19, 20, 21],
    views=[
        dict(type='array', var='nums', h=190, cell=90, label='nums',
             window=('x', 'y')),
        dict(type='map', var=_present, h=280, label='pos_dict[值] = 前缀个数（只画 nums 里出现的值）',
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=30, h=100, fn=lambda S: (
            f"查询 `[{S['x']}, {S['y']}]`：上一个出现的值 `last = {S['last']}`，最小差 `now = {S['now']}`" if 'x' in S and 'last' in S else '')),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('num', 'num', 'cyan'), ('cnt', 'cnt', 'yellow'), ('last', 'last', 'purple'), ('now', 'now', 'green'), 'res'],
    captions={
        'pos_dict = {}': '`pos_dict[v][i]`：`nums[0..i]` 里值 `v` 出现了几次（前缀和），下面先建表',
        'pos_dict[nums[0]][0] = 1': '`nums[0] = {nums[0]}`：值 `{nums[0]}` 在第 0 位的个数记 1，其余值都是 0（1 到 100 的 100 个值都先建好了）',
        '[-1] += 1': '值 `{nums[index]}` 在第 {index} 位多出现一次：`pos_dict[{nums[index]}]` = =={pos_dict[nums[index]]}==',
        'res = []': '`res` 收集每个查询的答案',
        'last = None': '`last` = 上一个出现在区间里的值，还没有',
        'now = None': '`now` = 目前最小的相邻差，还没有',
        'if last is not None': lambda S, B, r: (
            f'枚举到值 `{S.num}`：在 `[{S.x}, {S.y}]` 里出现 {S.pos_dict[S.num][S.y] - (S.pos_dict[S.num][S.x - 1] if S.x > 0 else 0)} 次（`pos_dict[{S.num}][{S.y}]'
            + (f' − pos_dict[{S.num}][{S.x - 1}]`' if S.x > 0 else '`')
            + ') → 存在，'
            + ('它是第一个存在的值，没有上一个可比' if B.last is None else f'与上一个存在的值 `{B.last}` 作差 `{S.num} − {B.last} = {S.num - B.last}`'
               + ('，比 now 更小 → 更新' if (B.now is None or B.now > S.num - B.last) else '，不比 now 小 → 不更新'))),
        'now = num - last': '`now = {num} − {last}` = =={now}==',
        'last = num': '`last = {num}`，继续找下一个存在的值（相邻的值才可能产生最小差）',
        'if now is None': lambda S, B, r: ('`now` 还是 None：区间里没有两个不同的值 → 答案 -1' if S.now is None
                                           else f'`now = {S.now}`：枚举完 1..100，这就是最小差'),
        'res.append(-1)': '答案 -1，`res` = =={res}==',
        'res.append(now)': '答案 `{now}`，`res` = =={res}==',
        'return res': '所有查询答案：=={res}==',
    },
    cards=dict(
        one_liner='值域只有 100：每个值一份前缀个数，枚举值找相邻差',
        complexity='时间 `O(100·(n+q))`，空间 `O(100·n)`',
        problem=['每个查询 `[x, y]`：求子数组里任意两个不同元素差的绝对值的最小值',
                 '元素全相同则答案 `-1`；`nums[i] <= 100`',
                 '本视频：`nums=[4,5,2,2,7]`，查询 `[0,2]`、`[2,3]` → `[1, -1]`'],
        quote='每个数只可能跟存在于区间中且最近的数形成答案，例如3,5,6都存在于区间中，那么只需要考虑3和5以及5和6，3是没有理由越过5去和6组队的。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间合并没法用线段树：答案可能出在任意位置，所以换思路看值域小（≤100）',
              '从 1 到 100 枚举值，只和「上一个存在于区间里的值」作差',
              '「值 `v` 是否在 `[x, y]` 里」用每个值各一份前缀个数：`pos_dict[v][y] − pos_dict[v][x−1]`'],
        summary=['原文为 Python 2 风格，仅需删去类型说明文档字符串，其余原样可运行',
                 '时间 `O(100·(n+q))`，空间 `O(100·n)`',
                 '易错点：`x = 0` 时不能减 `pos_dict[v][x−1]`（会变成 `[-1]`），原文用 `if x > 0` 隔开',
                 '视频里为了简洁，建表和扫描值域时跳过了对每个值的重复步骤，只演示出现在区间里的值',
                 '对比灵神：灵神用 `bisect` 在每个值的下标列表里二分，空间 `O(n)`；yiduobo 用前缀个数表，查询 `O(1)`'],
    ),
)
