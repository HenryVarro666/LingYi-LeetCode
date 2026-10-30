NUMS = [3, 1, 2]


def _thr(S):
    return S['left'] + 1 if 'res' in S else S['mid']


def _grow(S, B, r):
    t = _thr(S)
    nums = S.nums
    cond = S.p < len(nums) and (not S.ma or nums[S.ma[0]] - nums[S.mi[0]] < t)
    if cond:
        return f'窗口极差还 `< {t}`（或窗口为空）→ 右端 `p = {S.p}` 继续扩'
    return '窗口已经合格（或右端到头），不再扩'


def _chk(S, B, r):
    t = _thr(S)
    nums = S.nums
    if not S.ma:
        return '窗口为空'
    d = nums[S.ma[0]] - nums[S.mi[0]]
    if d < t:
        return f'窗口极差 `{d} < {t}`：右端扩到头也不够 → 后面的左端点更不行，==break=='
    return f'窗口极差 `{d} ≥ {t}`：左端点 `{S.index}` 对应的最短合格窗口是 `[{S.index}, {S.p})`'


def _info(S):
    L = S.get('_line', 0)
    if 'mid' not in S and 'left' not in S:
        return '二分第 k 大的子数组值；滑动窗口 + 单调队列数出「值 ≥ mid」的子数组有几个'
    ma, mi = S.get('ma'), S.get('mi')
    nums = S['nums']
    win = ''
    if ma and mi:
        win = f"；窗口 `[{S.get('index', '?')}, {S.get('p', '?')})` 极差 = {nums[ma[0]]} − {nums[mi[0]]} = =={nums[ma[0]] - nums[mi[0]]}=="
    return f"二分范围 `[{S['left']}, {S['right']}]`" + (f"，猜 `mid = {S['mid']}`" if 'mid' in S else '') + f"，已数到 `cnt = {S.get('cnt', 0)}`（目标 k = {S['k']}）" + win


CONFIG = dict(
    num=3691, title='最大子数组总值 II', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分第 k 大 + 滑窗单调队列 + 补足',
    tags=['常用数据结构', '难度分 2469'],
    code='''
class Solution(object):
    def maxTotalValue(self, nums, k):
        
        right = max(nums) - min(nums)
        left = 0
        while left < right:
            mid = (left + right + 1) // 2
            p = 0
            cnt = 0
            ma = deque()
            mi = deque()
            for index, v in enumerate(nums):
                while p < len(nums) and (not ma or nums[ma[0]] - nums[mi[0]] < mid):
                    while ma and nums[p] > nums[ma[-1]]:
                        ma.pop()
                    ma.append(p)

                    while mi and nums[p] < nums[mi[-1]]:
                        mi.pop()
                    mi.append(p)

                    p += 1

                if not ma or nums[ma[0]] - nums[mi[0]] < mid:
                    break

                cnt += len(nums) - p + 1
                if cnt >= k:
                    break
                
                if ma and ma[0] == index:
                    ma.popleft()
                if mi and mi[0] == index:
                    mi.popleft()
            
            if cnt >= k:
                left = mid
            else:
                right = mid - 1

        res = 0
        p = 0
        cnt = 0
        ma = deque()
        mi = deque()
        for index, v in enumerate(nums):
            while p < len(nums) and (not ma or nums[ma[0]] - nums[mi[0]] < left + 1):
                while ma and nums[p] > nums[ma[-1]]:
                    ma.pop()
                ma.append(p)

                while mi and nums[p] < nums[mi[-1]]:
                    mi.pop()
                mi.append(p)

                p += 1
            
            if not ma or nums[ma[0]] - nums[mi[0]] < left + 1:
                break

            res += nums[ma[0]] - nums[mi[0]]
            cnt += 1
            q = p
            rest_ma = nums[ma[0]]
            rest_mi = nums[mi[0]]
            while q < len(nums):
                rest_ma = max(rest_ma, nums[q])
                rest_mi = min(rest_mi, nums[q])
                res += rest_ma - rest_mi
                cnt += 1
                q += 1

            if ma and ma[0] == index:
                ma.popleft()
            if mi and mi[0] == index:
                mi.popleft()

        return res + (k - cnt) * left
''',
    call='Solution().maxTotalValue([3, 1, 2], 3)',
    expect=5,
    views=[
        dict(type='array', var='nums', h=130, cell=80, window=('index', 'p - 1'), label='nums（框 = 当前窗口 [index, p)）'),
        dict(type='queue', var='ma', h=110, fmt=lambda i: f'{i}:{NUMS[i]}', label='ma：窗口最大值的单调队列（下标:值）'),
        dict(type='queue', var='mi', h=110, fmt=lambda i: f'{i}:{NUMS[i]}', label='mi：窗口最小值的单调队列（下标:值）'),
        dict(type='text', fn=_info, size=24, h=110),
    ],
    watch=['left', 'right', 'mid', 'index', 'p', ('cnt', 'cnt', 'green'), 'res'],
    skip=['break', 'mi.append(p)', 'p += 1', 'p = 0', 'ma = deque()', 'mi = deque()', 'cnt = 0', 'right = max(nums) - min(nums)', 'left = 0', 'for index, v in enumerate(nums)',
          'while ma and nums[p] > nums[ma[-1]]', 'while mi and nums[p] < nums[mi[-1]]', 'ma.pop()', 'mi.pop()',
          'if ma and ma[0] == index', 'if mi and mi[0] == index', 'q = p', 'rest_ma = nums[ma[0]]', 'rest_mi = nums[mi[0]]',
          'while q < len(nums)', 'while left < right', 'q += 1', 'rest_ma = max', 'rest_mi = min'],
    captions={
        'mid = (left + right + 1) // 2': '二分猜「第 k 大的子数组值」`mid = {mid}`（向上取整，因为 `left = mid` 会保留 mid）',
        'while p < len(nums) and (not ma or': _grow,
        'ma.append(p)': '`nums[{p}] = {nums[p]}` 同时进两个队列（队首始终是窗口的最大 / 最小值）：`ma = {list(ma)}`',
        'if not ma or nums[ma[0]] - nums[mi[0]] < mid': _chk,
        'if not ma or nums[ma[0]] - nums[mi[0]] < left + 1': _chk,
        'cnt += len(nums) - p + 1': '左端点 `{index}`：右端点从 `p-1` 到 `n-1` 的子数组极差都 ≥ mid → 共 `{len(nums) - p + 1}` 个，`cnt = {cnt}`',
        28: lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}`：已经够 k 个，不用再数，==break==' if S.cnt >= S.k else f'`cnt = {S.cnt} < k = {S.k}`，还不够，继续下一个左端点'),
        36: lambda S, B, r: (f'这一轮数完：`cnt = {S.cnt} ≥ k = {S.k}` → 值 ≥ {S.mid} 的子数组够 k 个' if S.cnt >= S.k else f'这一轮数完：`cnt = {S.cnt} < k = {S.k}` → 值 ≥ {S.mid} 的子数组不够 k 个'),
        'ma.popleft()': '左端点 `{index}` 离开窗口：它正是最大值队首 → 出队，`ma` = {list(ma)}',
        'left = mid': '值 ≥ {mid} 的子数组至少 k 个 → 第 k 大 ≥ mid → ==`left = mid`==',
        'right = mid - 1': '值 ≥ {mid} 的不够 k 个 → 第 k 大 < mid → ==`right = mid - 1`==',
        'res = 0': '二分结束：第 k 大的值 `v = left = {left}`。再把「值 ≥ v+1」的子数组暴力累加，不够的 `k − cnt` 个用 `v` 补',
        'res += nums[ma[0]] - nums[mi[0]]': '先加窗口 `[{index}, {p})` 的极差：`res` = {res}',
        'res += rest_ma - rest_mi': '右端继续往右：`res` = {res}',
        'cnt += 1': '计数 +1：`cnt` = {cnt}',
        'return res + (k - cnt) * left': '值 ≥ {left + 1} 的子数组共 `{cnt}` 个，还差 `{k - cnt}` 个，用恰好等于 `{left}` 的补上 → `{res} + {k - cnt} × {left}` = =={ret}==',
    },
    max_steps=100,
    cards=dict(
        one_liner='二分第 k 大的值，滑窗数个数，再用「刚好等于它」的补足',
        complexity='时间 `O(n log U + k)`，空间 `O(n)`',
        problem=['选恰好 `k` 个不同子数组，值 = 最大值 − 最小值，求总值最大',
                 '先二分「第 k 大的子数组值」，再把前 k 大加起来',
                 '本视频：`[3,1,2], k=3` → `5`（极差 2,2,1）'],
        quote='对于一个固定了左边界的子数组而言，且右边界越大，子数组中的最大值就最大，最小值就越小，也就是说这个子数组的值就越大。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分 `mid`：数值 ≥ mid 的子数组有几个，用变长滑窗 + 单调队列',
              '固定左端点，最小的合格右端点 `p-1`，右边的全合格 → 一次加 `n-p+1`',
              '求和时把门槛抬到 `v+1`：合格的少于 k 个可暴力累加，缺的用 `v` 补'],
        summary=['`mid` 向上取整：`(left + right + 1) // 2`，对应 `left = mid`',
                 '单调队列：队首是窗口最值，左端点过了队首就弹出',
                 '值 ≥ v+1 的子数组数 `< k`，所以暴力累加不会超时',
                 '原文为 Python 2 风格，整数除法 `//` 本来就是 Python 3 写法，无需改动',
                 '对比灵神：灵神用堆 + ST 表按值从大到小取 k 个；yiduobo 二分值再补足，复杂度与 k 弱相关'],
    ),
)
