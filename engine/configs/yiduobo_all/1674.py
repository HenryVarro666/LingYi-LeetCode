CONFIG = dict(
    num=1674, title='使数组互补的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分标记 · 入口/出口数组',
    tags=['灵神题单·常用数据结构', '难度分 2333'],
    code='''
class Solution(object):
    def minMoves(self, nums, limit):
        n = len(nums)
        left = [0] * (limit + limit + 1)
        right = [0] * (limit + limit + 1)
        for index in range(n // 2):
            x = nums[index]
            y = nums[n - index - 1]
            left[min(x, y) + 1] += 1
            if max(x, y) + 1 <= limit:
                right[max(x, y) + limit + 1] += 1
            
            left[x + y] += 1
            if x + y + 1 <= limit + limit:
                right[x + y + 1] += 1
        
        now = n
        res = now
        for target in range(2, limit + limit + 1):
            now += right[target] - left[target]
            res = min(res, now)
        
        return res
''',
    call='Solution().minMoves([1,2,1,3], 4)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（成对：index 与 n-index-1）', h=170,
             pointers={'index if _line < 17 else None': 'blue', 'n - index - 1 if _line < 17 else None': 'pink'},
             pointer_labels={'index if _line < 17 else None': 'x', 'n - index - 1 if _line < 17 else None': 'y'}),
        dict(type='array', var='left', label='left[k]：入口标记（到这里操作次数 -1）', h=170,
             pointers={'target if _line > 17 else None': 'orange'}, pointer_labels={'target if _line > 17 else None': 'target'},
             color=lambda S, i, v: 'yellow' if v else None),
        dict(type='array', var='right', label='right[k]：出口标记（从这里操作次数 +1）', h=150,
             window=('target if _line > 17 else None', 'target if _line > 17 else None'),
             color=lambda S, i, v: 'pink' if v else None),
        dict(type='text', size=28, h=80, fn=lambda S: (
            f"目标和 `{S['target']}`：`now` = 全部配对要改的次数 = =={S['now']}==，最小 `res` = {S['res']}"
            if 'target' in S and 'now' in S else
            (f"一对 `({S['x']}, {S['y']})`：和 `{S['x']+S['y']}`，改 1 次的和域 `[{min(S['x'], S['y'])+1}, {max(S['x'], S['y'])+S['limit']}]`"
             if 'y' in S else ''))),
    ],
    watch=['x', 'y', ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'left = [0]': '`left`：区间减一的入口标记，下标是目标和 `s`',
        'right = [0]': '`right`：区间减一的出口标记（`y+1` 处结束）',
        'x = nums[index]': '取第 `{index}` 对：`x = {x}`',
        'y = nums[n': '`y = nums[{n-index-1}] = {y}`：这一对原来的和是 `{x+y}`',
        'left[min(x, y) + 1] += 1': '改一次的和域从 `min+1 = {min(x,y)+1}` 开始：入口 `left[{min(x,y)+1}] += 1`（操作数 2 → 1）',
        'if max(x, y) + 1 <= limit': '出口 `max+limit+1 = {max(x,y)+limit+1}` 要在数组范围内才记：`{max(x,y)+1} <= {limit}` → {"成立" if max(x,y)+1 <= limit else "不成立，越界不用记"}',
        'right[max(x, y) + limit + 1]': '和域到 `max+limit` 结束，`right[{max(x,y)+limit+1}] += 1`（操作数 1 → 2）',
        'left[x + y] += 1': '和刚好是 `{x+y}` 时一次都不用改：再减一，入口 `left[{x+y}] += 1`',
        'if x + y + 1 <= limit': '`{x+y+1} <= {limit+limit}` → {"成立" if x+y+1 <= limit+limit else "不成立，不用记"}',
        'right[x + y + 1] += 1': '`{x+y}` 一个点就结束：出口 `right[{x+y+1}] += 1`',
        'now = n': '初始每对都要改 2 次，共 `n/2` 对 → `now = n = {n}`',
        'now += right': '`now += right[{target}] - left[{target}]` → =={now}==：目标和为 `{target}` 的总操作数',
        'res = min': '`res = min({B.res}, {now}) = {res}`',
        'return res': '最少操作数 `{res}`',
    },
    cards=dict(
        one_liner='先试贪心行不通，改为枚举目标和，用差分叠出每个和的代价',
        complexity='时间 `O(n + limit)`，空间 `O(limit)`',
        problem=['偶数长数组，每次可把一个数改成 `[1, limit]` 内的数',
                 '要让 `nums[i] + nums[n-1-i]` 全部相等，求最少操作数',
                 '本视频：`nums=[1,2,1,3], limit=4` → `1`'],
        quote='若此时cnt_c最大，那么按上面贪心的做法，就要将a和b都变成c……只要cnt_a + cnt_b > cnt_c，上面贪心的做法就是不成立的。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心「向出现最多的和靠拢」不对：靠近边界要改 2 次',
              '一对 `(x, y)`：和域 `[min+1, max+limit]` 内改 1 次，原和改 0 次，其余 2 次',
              '用 `left/right` 两个标记数组记入口、出口，一遍扫描得到每个目标和的总代价',
              '`now` 初值 `n`（每对先算 2 次），取最小'],
        summary=['时间 `O(n + limit)`，空间 `O(limit)`',
                 '原文为 Python 2 写法，`n / 2` 已改为 `n // 2`',
                 '出口下标可能越界，所以有 `if ... <= limit` 的判断，越界的出口不影响结果',
                 '对比灵神：灵神一个 `diff` 数组合并正负标记，yiduobo 拆成 `left`、`right` 两个'],
    ),
)
