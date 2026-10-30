CONFIG = dict(
    num=3748, title='统计稳定子数组的数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 下一个递增段左端点',
    tags=['前缀和', '难度分 2209'],
    code='''
class Solution:
    def countStableSubarrays(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # 计算递增子数组个数的前缀和
        s = [0] * (n + 1)
        cnt = 0
        for i, x in enumerate(nums):
            if i > 0 and x < nums[i - 1]:
                cnt = 0
            cnt += 1
            # 现在 cnt 表示以 i 为右端点的递增子数组个数
            s[i + 1] = s[i] + cnt

        # nxt[i] 表示 i 右边下一个递增段的左端点，若不存在则为 n
        nxt = [0] * n
        nxt[-1] = n
        for i in range(n - 2, -1, -1):
            nxt[i] = nxt[i + 1] if nums[i] <= nums[i + 1] else i + 1

        ans = []
        for l, r in queries:
            l2 = nxt[l]
            if l2 > r:  # l 和 r 在同一个区间
                m = r - l + 1
                ans.append(m * (m + 1) // 2)
            else:  # l 和 r 在不同区间
                # 分成 [l, l2) + [l2, r]
                # 由于 [l2, r] 中的每个右端点所在递增段的左端点都在 [l2, r] 内，所以可以用前缀和计算
                m = l2 - l
                ans.append(m * (m + 1) // 2 + s[r + 1] - s[l2])
        return ans
''',
    call='Solution().countStableSubarrays([2,3,3,1,3,2], [[0,2],[1,5],[0,5]])',
    expect=[6, 7, 10],
    views=[
        dict(type='array', var='nums', label='nums', h=210,
             pointers={'i': 'blue', 'l': 'green', 'r': 'pink'},
             window=('l', 'r')),
        dict(type='array', var='s', label='s（前缀和，s[i+1] = 以 i 结尾的递增子数组总数）', h=210, pointers={'i + 1': 'blue'}),
        dict(type='array', var='nxt', label='nxt（右边下一个递增段的左端点）', h=210,
             pointers={'i': 'blue', 'l2': 'orange'}),
        dict(type='text', fn=lambda S: (
            f"查询 `[{S['l']}, {S['r']}]`：`l2 = nxt[{S['l']}] = {S['l2']}`"
            + (f"，`l2 > r` → 同一段" if S['l2'] > S['r'] else f"，`l2 <= r` → 分成 `[{S['l']}, {S['l2']})` + `[{S['l2']}, {S['r']}]`")
            if 'l2' in S and 'l' in S and 'r' in S and S.get('_line', 0) >= 23 else '')),
    ],
    skip=['cnt = 0'],
    watch=['i', 'cnt', 'l', 'r', 'l2', ('ans', 'ans', 'green')],
    captions={
        'if i > 0 and x < nums[i - 1]': '`nums[{i}] = {x}` 比前一个小？{"是 → 递增段断开，`cnt` 清零" if i > 0 and x < nums[i-1] else "否 → 还在同一个递增段"}',
        'cnt += 1': '以 `{i}` 为右端点的递增子数组有 `{cnt}` 个（`[i]`、`[i-1,i]`……）',
        's[i + 1] = s[i] + cnt': '`s[{i+1}] = s[{i}] + {cnt} = {s[i+1]}`：前缀和累加',
        'nxt[-1] = n': '最后一个位置右边没有递增段，`nxt[-1] = n = {n}`',
        'nxt[i] = nxt[i + 1] if': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} <= nums[{S.i+1}] = {S.nums[S.i+1]}` → 同一段，沿用 `nxt[{S.i+1}]` → `nxt[{S.i}] = {S.nxt[S.i]}`'
                                                  if S.nums[S.i] <= S.nums[S.i+1] else
                                                  f'`nums[{S.i}] = {S.nums[S.i]} > nums[{S.i+1}] = {S.nums[S.i+1]}` → 在这里断开，`nxt[{S.i}] = {S.i+1}`'),
        'l2 = nxt[l]': '查询 `[{l}, {r}]`：`l` 右边下一个递增段从 `l2 = {l2}` 开始',
        'if l2 > r': '`l2 = {l2}` {">" if l2 > r else "<="} `r = {r}` → {"==同一个递增段==，整段任意子数组都递增" if l2 > r else "==跨段=="}',
        'm = r - l + 1': '长 `m = {m}` 的段里有 `1+2+…+m = {m*(m+1)//2}` 个递增子数组',
        'm = l2 - l': '左半段 `[l, l2)` 长 `m = {m}`，里面全是递增子数组',
        'ans.append(m * (m + 1) // 2 + s[r + 1] - s[l2])': '左段 `{m*(m+1)//2}` + 右段前缀和差 `s[{r+1}] − s[{l2}] = {s[r+1] - s[l2]}` = =={ans[-1]}==',
    },
    cards=dict(
        one_liner='没有逆序对 = 递增段；整段数 m(m+1)/2，跨段用前缀和',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['子数组没有逆序对（`i<j` 且 `nums[i]>nums[j]`）就叫稳定，也就是==不减的子数组==',
                 '每次查询 `[l, r]`，数 `nums[l..r]` 里稳定子数组的个数',
                 '示例：`[3,1,2]`，`[[0,1],[1,2],[0,2]]` → `[2,3,4]`'],
        quote='没有逆序对意味着子数组是**递增**的（允许元素相等）。把 nums 分成若干递增段。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums=[2,3,3,1,3,2]` 分成 `[2,3,3]+[1,3]+[2]` 三段',
              '`l`、`r` 在同一段：长 `m` 的段有 `m(m+1)/2` 个',
              '不在同一段：`[l, nxt[l])` 单独算，`[nxt[l], r]` 的每个右端点所在段的左端点都在里面，直接用前缀和 `s`'],
        summary=['时间 `O(n+q)`：预处理两趟，每次查询 `O(1)`',
                 '`s[i+1]` 存的是以 `i` 结尾的递增子数组数的前缀和，所以取 `s[r+1] - s[l2]`',
                 '`nxt` 要倒着算：`nxt[i]` 依赖 `nxt[i+1]`',
                 '方法一用 `bisect_right` 在递增段左端点里二分，复杂度 `O(n+q log n)`，本视频讲方法二'],
    ),
)
