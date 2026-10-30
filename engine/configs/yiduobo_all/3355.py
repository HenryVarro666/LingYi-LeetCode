CONFIG = dict(
    num=3355, title='零数组变换 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组 · 覆盖次数',
    tags=['灵神题单·常用数据结构', '难度分 1591'],
    code='''
class Solution(object):
    def isZeroArray(self, nums, queries):
        
        n = len(nums)
        f = [0] * n
        for x, y in queries:
            f[x] += 1
            if y + 1 < n:
                f[y + 1] -= 1
        
        now = 0
        for index in range(n):
            now += f[index]
            if now < nums[index]:
                return False
        return True
''',
    call='Solution().isZeroArray([2,1,2,1,2], [[0,2],[0,2],[2,4]])',
    expect=False,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=170, label='nums（要减的次数）'),
        dict(type='array', var='f', pointers={'index': 'blue'}, h=170, label='f（以 index 为起点的覆盖变化）'),
        dict(type='text', fn=lambda S: (f"位置 `{S['index']}`：被覆盖 `now = {S['now']}` 次，需要 `nums[{S['index']}] = {S['nums'][S['index']]}` 次" if 'index' in S and 'now' in S else (f"查询 `[{S['x']}, {S['y']}]`" if 'x' in S else ''))),
    ],
    watch=['x', 'y', 'index', ('now', 'now', 'orange')],
    captions={
        'f = [0] * n': '`f[index]`：以 `index` 为起点的后缀，覆盖次数的变化',
        'f[x] += 1': '区间从 `{x}` 开始：后缀多一层覆盖 → `f[{x}] = {f[x]}`',
        'if y + 1 < n': lambda S, B, r: f'`y + 1 = {S.y + 1}`，' + ('没超出数组，要在这里结束覆盖' if S.y + 1 < len(S.nums) else '已经到数组末尾，不用再记'),
        'f[y + 1] -= 1': '区间在 `{y}` 结束：从 `{y+1}` 起少一层覆盖 → `f[{y+1}] = {f[y+1]}`',
        'now += f[index]': '前缀和：位置 `{index}` 被覆盖的次数 `now = {now}`',
        'if now < nums[index]': lambda S, B, r: f'覆盖 `{S.now}` 次，需要减 `{S.nums[S.index]}` 次：' + ('次数不够 → 变不成 0' if S.now < S.nums[S.index] else '够了'),
        'return False': '有一个位置次数不够 → ==返回 False==',
        'return True': '每个位置都够 → `True`',
    },
    cards=dict(
        one_liner='位置 index 至少要被 nums[index] 个区间盖住',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['每个查询 `[l, r]`：在区间内选一个下标子集，各减 1',
                 '问处理完所有查询后，能不能让 `nums` 全为 0',
                 '示例：`[2,1,2,1,2]`，查询 `[[0,2],[0,2],[2,4]]` → `False`'],
        quote='index至少需要被queries中的nums[index]个区间覆盖住。',
        quote_src='—— yiduobo 题解原文',
        idea=['要减到 0，位置 `index` 就得有 `nums[index]` 次机会 → 被覆盖次数 `≥ nums[index]`',
              '静态区间覆盖用差分：起点 `+1`，终点后一位 `−1`',
              '再扫一遍做前缀和 `now`，`now < nums[index]` 就失败'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`y + 1` 可能等于 `n`，所以先判断 `y + 1 < n`',
                 '只比较次数，不关心具体选哪些下标',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
