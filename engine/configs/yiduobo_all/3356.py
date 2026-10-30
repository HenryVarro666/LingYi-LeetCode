def _txt(S):
    if 'mid' not in S:
        return '二分操作个数 `k`：越多越可能变成零数组 → ==单调=='
    if 'now' in S and 'index' in S and S.get('_line', 0) >= 12:
        return f"检查前 `{S['mid']}` 个询问：下标 `{S['index']}` 能减的量 `now = {S['now']}`，`nums[{S['index']}] = {S['nums'][S['index']]}`"
    return f"区间 `[left, right) = [{S['left']}, {S['right']})`，试 `mid = {S['mid']}`：前 `{S['mid']}` 个询问够不够？"


CONFIG = dict(
    num=3356, title='零数组变换 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二分答案 + 差分检查',
    tags=['难度分 1913'],
    code='''
class Solution(object):
    def minZeroArray(self, nums, queries):
        
        n = len(nums)

        def check(mid):
            f = [0] * n
            for x, y, v in queries[:mid]:
                f[x] += v
                if y + 1 < n:
                    f[y + 1] -= v
        
            now = 0
            for index in range(n):
                now += f[index]
                if now < nums[index]:
                    return False
            return True
        
        left = 0
        right = len(queries) + 1
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        if left == len(queries) + 1:
            return -1
        return left
''',
    call='Solution().minZeroArray([2,0,3], [[0,2,1],[0,0,1],[2,2,2]])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=190,
             color=lambda S, i, v: ('red' if 'now' in S and i == S.get('index') and S.get('_line') in (16, 17) and S['now'] < v else None)),
        dict(type='array', var='f', label='f（差分：前 mid 个询问的累计）', pointers={'index': 'blue'}, h=190),
        dict(type='table', var='queries', label='queries [l, r, val]（绿 = 前 mid 个，参与检查）',
             rows=lambda S: [f'#{j}' for j in range(len(S['queries']))], cols=['l', 'r', 'val'], h=220,
             color=lambda S, i, j, v: ('green' if 'mid' in S and i < S['mid'] and 'f' in S else None)),
    ],
    watch=['left', 'right', ('mid', 'mid', 'pink'), 'now'],
    captions={
        'def check': '`check(mid)`：只用前 `mid` 个询问，能不能把 `nums` 全减到 0？',
        'f = [0] * n': '新建差分数组 `f`，从零开始累计前 `mid = {mid}` 个询问',
        'for x, y, v in': lambda S, B, r: (f'取一个询问：`[{S.x}, {S.y}]` 每个下标最多减 `{S.v}`（相当于 `{S.v}` 次「减 1」）' if 'x' not in B or (S.x, S.y, S.v) != (B.x, B.y, B.v) else f'前 `{S.mid}` 个询问都装进差分了'),
        'f[x] += v': '区间起点 `f[{x}]` += `{v}`',
        'if y + 1 < n': lambda S, B, r: (f'`y + 1 = {S.y + 1}` 在数组内 → 要在终点后一位抵消' if S.y + 1 < len(S.nums) else f'`y + 1 = {S.y + 1}` 已越过数组末尾 → 不用抵消，省去越界'),
        'f[y + 1] -= v': '终点后一位 `f[{y + 1}]` -= `{v}`：区间在这里结束',
        'now = 0': '`now` 扫描时累计 `f` 的前缀和 = 该下标最多能减的量',
        'for index in range(n)': lambda S, B, r: (f'检查下标 `{S.index}`' if S.index != B.get('index') or 'now' not in B or B.get('now') is None else '全部下标检查完'),
        'now += f[index]': '`now` {B.now} → =={now}==：下标 `{index}` 最多能减 `{now}`',
        'if now < nums[index]': lambda S, B, r: (f'`now = {S.now} < nums[{S.index}] = {S.nums[S.index]}`：减不到 0 → `check` 失败' if S.now < S.nums[S.index] else f'`now = {S.now} >= nums[{S.index}] = {S.nums[S.index]}`：够了'),
        'return False': '前 `{mid}` 个询问不够 → 返回 ==False==',
        'return True': '每个下标都够 → 前 `{mid}` 个询问足够，返回 ==True==',
        'left = 0': '二分下界 `left = 0`',
        'right = len': '上界 `right = {right}`：`len(queries) + 1` 表示==不存在 k==',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：答案还在 `[{S.left}, {S.right}]`' if S.left < S.right else f'`left = {S.left} == right`：二分结束，最小的可行 `k` 就是 `{S.left}`'),
        'mid = (left + right) // 2': '取中间 `mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：只用前 `{mid}` 个询问，够不够？通过说明答案 ≤ {mid}，不通过说明答案 > {mid}',
        'right = mid': '可行：`right = mid = {right}`，继续往小找',
        'left = mid + 1': '不可行：`left = mid + 1 = {left}`',
        'if left == len(queries) + 1': lambda S, B, r: ('`left` 停在 `len + 1`：全部询问都不够 → 返回 -1' if S.left == len(S.queries) + 1 else f'`left = {S.left}` 在合法范围，不是 `len + 1`'),
        'return left': '最少需要前 =={left}== 个询问',
    },
    skip=['n = len'],
    cards=dict(
        one_liner='询问越多越容易归零 → 二分 k，用差分数组检查',
        complexity='时间 `O((n + q) log q)`，空间 `O(n)`',
        problem=['`queries[i] = [l, r, val]`：`nums[l..r]` 中每个数各自可以减去 `0 ~ val` 的任意值',
                 '求最小的 `k`，使前 `k` 个询问能把 `nums` 变成全 0，不存在返回 `-1`',
                 '示例：`nums=[2,0,3]`，`queries=[[0,2,1],[0,0,1],[2,2,2]]` → `3`'],
        quote='每个下标减去的值都可以独立选择，那么实际上这里的queries[i]就可以认为是执行了val[i]次3355题中的操作……操作没有负面效果，操作的数量越多就越有可能让nums变为全0，符合单调性。',
        quote_src='—— yiduobo 题解原文',
        idea=['3355 题：每次减 1，用差分数组判断覆盖次数够不够；本题一个询问等价于 `val` 次',
              '不选下标的操作没有副作用，所以 `k` 越大越容易成功：==可以二分 k==',
              '二分上界取 `len(queries) + 1`，用它表示「无解」，最后统一判断'],
        summary=['时间 `O((n + q) log q)`，空间 `O(n)`',
                 '上界要 `len(queries) + 1`，这样 `len(queries)` 本身也会被 `check`',
                 '`if y + 1 < n` 防止差分越界',
                 '原文是 Python 2 风格，仅删去了类型说明，代码无需其他修改',
                 '对比灵神：灵神方法三用双指针一次扫描 `O(n + q)`，无需二分'],
    ),
)
