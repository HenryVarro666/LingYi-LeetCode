def _present(S):
    return {k: v for k, v in S['pos_dict'].items() if k in set(S['nums'])}


def _txt(S):
    if 'x' not in S:
        return '`pos_dict[v][i]` = nums[0..i] 里 v 出现的次数（只显示 nums 里出现过的值；其余值全是 0）'
    r = f"查询 `[{S['x']}, {S['y']}]`：`cnt = pos_dict[v][{S['y']}] − pos_dict[v][{S['x']}-1]`"
    if S.get('now') is not None:
        r += f"　当前最小差 ==now = {S['now']}=="
    return r


CONFIG = dict(
    num=1906, title='查询差绝对值的最小值', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='值域很小 · 每个数一个前缀和',
    tags=[],
    code='''
class Solution:
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
    call='Solution().minDifference([4, 5, 2, 2, 7], [[0, 2], [2, 3], [1, 4]])',
    expect=[1, -1, 2],
    skip=['pos_dict[num] = [0]', 'for num in range(1, 101)', '.append(pos_dict[num][-1])', 'cnt = pos_dict', 'if x > 0',
          'cnt -= ', 'if cnt > 0'],
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前查询区间 [x, y]）', cell=84, h=150,
             pointers={'index if _line < 13 else None': 'blue'}, pointer_labels={'index if _line < 13 else None': 'index'}, window=('x', 'y')),
        dict(type='map', var=_present, label='pos_dict（每个值的前缀次数数组）', h=250, font=30,
             fmt=lambda k, v: f"{k}: {v}"),
        dict(type='array', var='res', label='res（每个查询的答案）', cell=84, h=120),
        dict(type='text', size=28, h=100, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('num', 'num', 'purple'),
           ('last', 'last', 'orange'), ('now', 'now', 'green')],
    captions={
        'pos_dict = {}': '`pos_dict[v]` 将保存值 `v` 的==前缀出现次数==，v 从 1 到 100',
        'pos_dict[nums[0]][0] = 1': '下标 0 处：`nums[0] = {nums[0]}` 出现 1 次，其余值 0 次',
        'for index in range': lambda S, B, ret: (f'处理 `nums[{S.index}] = {S.nums[S.index]}`：先让所有值的前缀数组都延长一格' if S.get('index') != B.get('index') or 'index' not in B else '`nums` 处理完了'),
        '[-1] += 1': '延长后 `nums[{index}] = {nums[index]}` 的这一格加一 → `{pos_dict[nums[index]]}`',
        'res = []': '前缀数组建好了，开始回答查询',
        'for x, y in queries': lambda S, B, ret: (f'查询区间 `[{S.x}, {S.y}]`，从 1 到 100 枚举值，看哪些值在区间里' if 'x' not in B or (S.x, S.y) != (B.x, B.y) else '查询都处理完了'),
        'last = None': '`last` 记录区间里==上一个出现的值==',
        'now = None': '`now` 是目前最小的相邻差，还没有',
        'if last is not None': lambda S, B, ret: (
            f'值 `{S.num}` 在区间里（前缀差 = {S.pos_dict[S.num][S.y] - (S.pos_dict[S.num][S.x - 1] if S.x > 0 else 0)} > 0）'
            + (f'，它与上一个值 `{S.last}` 的差 `{S.num - S.last}`' if S.last is not None else '，是区间里最小的值，还没有上一个')
            + (f'，比 now 小就更新' if S.last is not None else '')),
        'now = num - last': '只有==相邻==的两个值才可能成为答案：`now = {num} − {last} = {now}`',
        'last = num': '`last` 更新为 `{num}`，下一个值只和它比',
        'if now is None': lambda S, B, ret: ('区间里只有一种值，没有差可算' if S.now is None
                                             else f'区间里最接近的两个值差 `{S.now}`'),
        'res.append(-1)': '所有元素都相同 → 答案 `-1`',
        'res.append(now)': '答案 `{now}` 加入 `res` → `{res}`',
        'return res': '全部查询完毕，返回 `{res}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='值域只有 100：每个值一个前缀和，枚举值找相邻差',
        complexity='时间 `O((n+q)·100)`，空间 `O(n·100)`',
        problem=['子数组的==差绝对值最小值==：其中两个不相等元素差的绝对值的最小值，全相同则为 `-1`',
                 '`queries[i] = [l, r]`，对每个查询求子数组 `nums[l..r]` 的答案',
                 '示例：`[4,5,2,2,7]`，查询 `[0,2]` → `1`，`[2,3]` → `-1`'],
        quote='每个数只可能跟存在于区间中且最近的数形成答案，例如3,5,6都存在于区间中，那么只需要考虑3和5以及5和6，3是没有理由越过5去和6组队的。',
        quote_src='—— yiduobo 题解',
        idea=['区间内最接近的两数：线段树合并答案不好抽象，放弃',
              '`nums[i] <= 100`：从 1 到 100 枚举值，只看区间里存在的值，和上一个存在的值求差',
              '"存在" 用前缀和判断：`pos_dict[v][y] − pos_dict[v][x−1] > 0`'],
        summary=['时间 `O((n+q)·100)`，空间 `O(n·100)`',
                 '`x == 0` 时没有 `x − 1`，要单独处理（代码里的 `if x > 0`）',
                 '只比较==相邻==存在的值，且差为 0 的情形不会出现（值互不相同）',
                 '演示里略去了 100 次的纯循环行（建表、枚举到不存在的值），只留有意义的步骤'],
    ),
)
