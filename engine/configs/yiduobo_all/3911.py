CONFIG = dict(
    num=3911, title='移除子数组元素后第 K 小偶数', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 前缀偶数个数 + 内层二分',
    tags=['灵神题单·二分算法', '难度分 2156'],
    code='''
class Solution(object):
    def kthRemainingInteger(self, nums, queries):
        
        even = [0]
        for v in nums:
            even.append(even[-1])
            if v % 2 == 0:
                even[-1] += 1

        res = []
        for l, r, k in queries:
            lo = k
            hi = k + even[r + 1] - even[l]

            while lo < hi:
                m = (lo + hi) // 2

                v = m * 2

                if v < nums[l]:
                    removed = 0
                else:
                    left, right = l, r
                    while left < right:
                        mid = (left + right + 1) // 2
                        if v < nums[mid]:
                            right = mid - 1
                        else:
                            left = mid

                    removed = even[left + 1] - even[l]

                if m - removed < k:
                    lo = m + 1
                else:
                    hi = m

            res.append(lo * 2)
        
        return res
''',
    call='Solution().kthRemainingInteger([2,5,8], [[0,1,2],[1,2,1],[0,2,4]])',
    expect=[6, 2, 12],
    views=[
        dict(type='array', var='nums', label='nums', h=190,
             color=lambda S, i, v: ('green' if 'l' in S and S['l'] <= i <= S['r'] and v % 2 == 0 else None),
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r']),
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='array', var='even', label='even（前缀偶数个数）', h=130),
        dict(type='text', h=70, fn=lambda S: (f"试探第 `{S['m']}` 个正偶数 `v={S['v']}`：被移除 `{S['removed']}` 个，剩 `{S['m']-S['removed']}` 个，要 `>= {S['k']}`" if 'removed' in S and 'm' in S and 18 < S['_line'] < 37 else (f"答案范围：第 `{S['lo']}` ~ `{S['hi']}` 个正偶数" if 'hi' in S else ''))),
        dict(type='array', var='res', label='res', h=130),
    ],
    watch=['l', 'r', 'k', 'lo', 'hi', 'm', 'v', ('removed', 'removed', 'green')],
    captions={
        'even = [0]': '`even[i]` 记录 `nums` 前 `i` 个数里的偶数个数，先放 `0`',
        'even.append': '先把上一个前缀的计数抄过来',
        'even[-1] += 1': '`{v}` 是偶数 → 前缀偶数个数 +1，现在 `even = {even}`',
        'for l, r, k': lambda S, B, r_: (f'处理询问 `[l, r, k] = [{S.l}, {S.r}, {S.k}]`' if len(S.res) < len(S.queries) else '询问都处理完了，循环结束'),
        'lo = k': '答案至少是第 `k = {k}` 个正偶数：`lo = {lo}`',
        'hi = k +': '最多再被挡住 `e` 个偶数，`e = even[r+1] - even[l]` → `hi = {hi}`',
        'while lo < hi': lambda S, B, r: f'`lo = {S.lo} < hi = {S.hi}`，继续二分' if S.lo < S.hi else f'`lo = hi = {S.lo}`：外层二分结束',
        'm = (lo + hi)': '外层二分：试第 `m = {m}` 个正偶数',
        'v = m * 2': '它对应的正偶数 `v = {m} × 2 = {v}`',
        'if v < nums[l]': lambda S, B, r: f'`v = {S.v}` 比 `nums[l] = {S.nums[S.l]}` 还小 → 子数组里没有数能挡住它' if S.v < S.nums[S.l] else f'`v = {S.v} >= nums[l] = {S.nums[S.l]}`：要数子数组里有多少偶数 `<= v`',
        'removed = 0': '没有被移除的数：`removed = 0`',
        'left, right = l, r': '内层二分：在 `nums[l..r]` 里找最后一个 `<= v` 的位置',
        'while left < right': lambda S, B, r: f'`left = {S.left} < right = {S.right}`，继续' if S.left < S.right else f'`left = right = {S.left}`：内层二分结束',
        'mid = (left + right + 1)': '取上中位数 `mid = {mid}`（左边界上移，避免死循环）',
        'if v < nums[mid]': lambda S, B, r: f'`{S.v} < nums[{S.mid}] = {S.nums[S.mid]}` → ==成立==，`nums[mid]` 太大' if S.v < S.nums[S.mid] else f'`{S.v} < nums[{S.mid}] = {S.nums[S.mid]}` → 不成立，`nums[mid]` 还在 `v` 以内',
        'right = mid - 1': '`nums[mid]` 太大，往左：`right = {right}`',
        'left = mid': '`nums[mid] <= v`，它可能就是最后一个：`left = {left}`',
        'removed = even[left + 1]': '`nums[l..{left}]` 里的偶数个数 `even[{left}+1] - even[{l}]` = ==`{removed}`==，它们都被移除',
        'if m - removed < k': lambda S, B, r: f'剩余 `{S.m} - {S.removed} = {S.m - S.removed}`，{"小于" if S.m - S.removed < S.k else "不小于"} `k = {S.k}`' + ('：v 不够大' if S.m - S.removed < S.k else '：v 够了'),
        'lo = m + 1': '`v` 还不够大，下界上移：`lo = {lo}`',
        'hi = m': '`v` 够了，但可能还能更小：`hi = {hi}`',
        'res.append': '询问答案是第 `{lo}` 个正偶数 → `{lo} × 2` = =={lo*2}==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='二分「第几个正偶数」，再二分算被移除的个数',
        complexity='时间 `O(n + q log^2 n)`，空间 `O(n)`',
        problem=['`nums` 严格递增；每个询问 `[l, r, k]`：从 `2, 4, 6, ...` 里删掉 `nums[l..r]` 里出现的数',
                 '求剩下序列的第 `k` 个数',
                 '示例：`nums=[2,5,8]`，`[[0,1,2],[1,2,1],[0,2,4]]` → `[6,2,12]`'],
        quote='对于一组询问[l, r, k]，其最终答案必然处于2到2 * (k + e)之间，这里的e表示nums[l]到nums[r]之间偶数的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案随 `k` 增大而增大，二分第 `m` 个正偶数 `v = 2m`',
              '剩余个数 = `m` 减去被移除的偶数个数 `removed`',
              '`removed`：在 `nums[l..r]` 内再二分出最后一个 `<= v` 的位置，用前缀数组 `even` 相减'],
        summary=['时间 `O(n + q log^2 n)`，空间 `O(n)`',
                 '`剩余 < k` 就抬 `lo`，否则收 `hi`，最后 `lo` 就是第几个正偶数',
                 '内层二分用上中位数 `(left+right+1)//2`，否则会死循环',
                 '原文为 Python 2 风格，已删去 `:type` 说明',
                 '对比灵神：灵神把偶数除以 2 转成 1539 题，单次二分 `O(log n)`'],
    ),
)
