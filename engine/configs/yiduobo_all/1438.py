NUMS = [10, 1, 2, 4, 7, 2]

CONFIG = dict(
    num=1438, title='绝对差不超过限制的最长连续子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='双指针 + 数组模拟单调双向队列',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1672'],
    code='''
class Solution(object):
    def longestSubarray(self, nums, limit):

        mi_q = []
        ma_q = []
        mi_l = 0
        mi_r = 0
        ma_l = 0
        ma_r = 0
        
        l = 0
        r = 0
        n = len(nums)
        res = 0

        while l < n:
            if mi_l < mi_r and mi_q[mi_l] == l - 1:
                mi_l += 1
            if ma_l < ma_r and ma_q[ma_l] == l - 1:
                ma_l += 1
            
            while r < n:
                num = nums[r]
                while mi_r > mi_l and nums[mi_q[mi_r - 1]] >= num:
                    mi_q.pop()
                    mi_r -= 1

                mi_q.append(r)
                mi_r += 1

                while ma_r > ma_l and nums[ma_q[ma_r - 1]] <= num:
                    ma_q.pop()
                    ma_r -= 1

                ma_q.append(r)
                ma_r += 1

                if nums[ma_q[ma_l]] - nums[mi_q[mi_l]] <= limit:
                    r += 1
                    res = max(res, r - l)
                else:
                    break

            if r == n:
                break
            
            l += 1
        
        return res
''',
    call='Solution().longestSubarray([10,1,2,4,7,2], 5)',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r - 1'), h=190,
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i < S['r'])),
        dict(type='queue', var=lambda S: S['ma_q'][S['ma_l']:] if 'ma_q' in S else [], label='ma_q（队首 ma_l 起；存下标:值，递减）', fmt=lambda k: f'{k}:{NUMS[k]}', h=105),
        dict(type='queue', var=lambda S: S['mi_q'][S['mi_l']:] if 'mi_q' in S else [], label='mi_q（队首 mi_l 起；存下标:值，递增）', fmt=lambda k: f'{k}:{NUMS[k]}', h=105),
        dict(type='text', h=60, fn=lambda S: (f"窗口 [l, r) 最大 `{S['nums'][S['ma_q'][S['ma_l']]]}` − 最小 `{S['nums'][S['mi_q'][S['mi_l']]]}` = =={S['nums'][S['ma_q'][S['ma_l']]] - S['nums'][S['mi_q'][S['mi_l']]]}==，k = {S['limit']}" if S.get('ma_q') and S.get('mi_q') and S['ma_l'] < len(S['ma_q']) and S['mi_l'] < len(S['mi_q']) else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('limit', 'limit'), ('res', 'res', 'green')],
    captions={
        'mi_q = []': '两个单调队列：`mi_q` 递增（队首最小），`ma_q` 递减（队首最大），都存==下标==',
        6: '用 `mi_l / mi_r` 手动记录队列的头和尾',
        11: '双指针 `l`、`r`：窗口是 `[l, r)`，`r` 能走多远是==单调不回头==的',
        'while l < n': '换一个左边界 `l = {l}`',
        'if mi_l < mi_r and mi_q[mi_l] == l - 1': lambda S, B, r: ('`mi_q` 队首正是上一轮的左端点 `{}`，已滑出窗口 → 出队'.format(S.l - 1)
                                                                    if S.mi_l < S.mi_r and S.mi_q[S.mi_l] == S.l - 1 else '`mi_q` 队首还在窗口里，不用动'),
        'if ma_l < ma_r and ma_q[ma_l] == l - 1': lambda S, B, r: ('`ma_q` 队首正是上一轮的左端点 `{}`，已滑出窗口 → 出队'.format(S.l - 1)
                                                                    if S.ma_l < S.ma_r and S.ma_q[S.ma_l] == S.l - 1 else '`ma_q` 队首还在窗口里，不用动'),
        'mi_l += 1': '`mi_q` 队首后移：`mi_l` = {mi_l}',
        'ma_l += 1': '`ma_q` 队首后移：`ma_l` = {ma_l}',
        'while r < n': lambda S, B, r: ('右端点 `r = {}` 尝试加入窗口'.format(S.r) if S.r < S.n else '`r` 已到末尾，不能再扩'),
        'mi_r = 0': '`mi_r` 是队尾位置（开区间）',
        'ma_l = 0': '`ma_q` 同样用 `ma_l / ma_r`',
        'ma_r = 0': '`ma_r` 是队尾位置',
        'num = nums[r]': '新来的数 `num = {num}`',
        'while mi_r > mi_l and nums[mi_q[mi_r - 1]] >= num': lambda S, B, r: ('`mi_q` 队尾 `{}` >= `{}`：队尾不可能再当最小值 → 弹出'.format(S.nums[B.mi_q[B.mi_r - 1]], S.num)
                                                                              if B.mi_r > B.mi_l and S.nums[B.mi_q[B.mi_r - 1]] >= S.num else '`mi_q` 队尾更小（或为空），停止弹出'),
        'mi_q.pop()': '队尾出队',
        'mi_q.append(r)': '`r` 进入 `mi_q` 队尾：队首最小值 `{nums[mi_q[mi_l]]}`',
        'while ma_r > ma_l and nums[ma_q[ma_r - 1]] <= num': lambda S, B, r: ('`ma_q` 队尾 `{}` <= `{}`：队尾不可能再当最大值 → 弹出'.format(S.nums[B.ma_q[B.ma_r - 1]], S.num)
                                                                              if B.ma_r > B.ma_l and S.nums[B.ma_q[B.ma_r - 1]] <= S.num else '`ma_q` 队尾更大（或为空），停止弹出'),
        'ma_q.pop()': '队尾出队',
        'ma_q.append(r)': '`r` 进入 `ma_q` 队尾：队首最大值 `{nums[ma_q[ma_l]]}`',
        'if nums[ma_q[ma_l]] - nums[mi_q[mi_l]] <= limit': lambda S, B, r: ('最大 `{}` − 最小 `{}` = `{}` <= `{}`：合法，窗口可以继续扩'.format(S.nums[S.ma_q[S.ma_l]], S.nums[S.mi_q[S.mi_l]], S.nums[S.ma_q[S.ma_l]] - S.nums[S.mi_q[S.mi_l]], S.limit)
                                                                           if S.nums[S.ma_q[S.ma_l]] - S.nums[S.mi_q[S.mi_l]] <= S.limit
                                                                           else '最大 `{}` − 最小 `{}` = `{}` > `{}`：不合法，`r` 这个数放不进来'.format(S.nums[S.ma_q[S.ma_l]], S.nums[S.mi_q[S.mi_l]], S.nums[S.ma_q[S.ma_l]] - S.nums[S.mi_q[S.mi_l]], S.limit)),
        39: '接受 `nums[{r-1}]`：`r` → {r}',
        'res = max(res, r - l)': '窗口长度 `{r} − {l} = {r-l}`，`res = max({B.res}, {r-l})` = =={res}==',
        42: '停止扩张，回到外层把 `l` 右移',
        44: lambda S, B, r: ('`r` 到了末尾：之后 `l` 更大，窗口只会更短，==不可能超过当前答案== → 结束' if S.r == S.n else '`r` 还没到末尾，继续'),
        47: '左边界右移：`l` → {l}',
        'return res': '最长合法子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='左边界右移时右边界不回头：双指针 + 两个单调队列',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和 `limit`，求最长连续子数组，其中任意两元素之差 `<= limit`',
                 '即窗口的 ==最大值 − 最小值 <= limit==',
                 '示例：`[10,1,2,4,7,2]`，`limit = 5` → `4`'],
        quote='对于当前的左边界l，不妨设其最大的符合题目要求的右边界为r，那么对于任意l\' = l + 1而言，其对应的最大右边界r\'必然大于等于r。',
        quote_src='—— yiduobo 题解原文',
        idea=['先证明单调性：左边界右移，窗口最大值只会变小、最小值只会变大，原来的 `r` 仍然合法 → 双指针',
              '窗口最大 / 最小用==单调双向队列==：新数进来，把队尾不可能再当最值的数弹掉',
              '每次 `l` 右移，只需检查队首是否恰好是被移出的下标'],
        summary=['时间 `O(n)`：每个数在每个队列里进出各一次',
                 '队列用 list + 头尾下标 `x_l / x_r` 模拟，注意尾部弹出要同步 `x_r -= 1`',
                 '小 trick：`r` 到末尾后 `l` 再右移只会更短，直接 `break`',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串；对比灵神：用 deque 存下标，窗口不合法时才收缩左端点'],
    ),
)
