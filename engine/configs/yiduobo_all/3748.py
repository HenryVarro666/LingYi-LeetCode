CONFIG = dict(
    num=3748, title='统计稳定子数组的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='分段 + belong + 前缀和',
    tags=['前缀和', '难度分 2209'],
    code='''
class Solution(object):
    def countStableSubarrays(self, nums, queries):
        
        def cnt(length):
            return (1 + length) * length // 2

        parts = []
        p = 0
        s = [0]
        belong = [None] * len(nums)
        while p < len(nums):
            belong[p] = len(parts)
            q = p + 1
            while q < len(nums) and nums[q] >= nums[q - 1]:
                belong[q] = len(parts)
                q += 1
            
            parts.append((p, q - 1))
            s.append(s[-1] + cnt(q - p))
            p = q
        
        res = []
        for x, y in queries:
            if belong[x] == belong[y]:
                res.append(cnt(y - x + 1))
            else:
                res.append(cnt(parts[belong[x]][1] - x + 1) + cnt(y - parts[belong[y]][0] + 1) + s[belong[y]] - s[belong[x] + 1])
        
        return res
''',
    call='Solution().countStableSubarrays([2,3,3,1,3,2], [[0,2],[1,5],[0,5]])',
    expect=[6, 7, 10],
    views=[
        dict(type='array', var='nums', label='nums', h=200,
             pointers={'p': 'blue', 'q': 'pink', 'x': 'green', 'y': 'orange'}),
        dict(type='array', var='belong', label='belong（每个元素属于第几段）', h=200,
             color=lambda S, i, v: ('cyan' if v is not None and v % 2 == 0 else 'purple') if v is not None else None),
        dict(type='array', var='s', label='s（各段子数组数的前缀和，s[0]=0）', h=200),
        dict(type='text', fn=lambda S: ('分好的段 parts = ' + str(S['parts'])) if 'parts' in S and S['parts'] else ''),
    ],
    watch=['p', 'q', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'return (1 + length)': '`cnt({length}) = (1+{length})*{length}//2 = {(1+length)*length//2}`：长 {length} 里的稳定子数组数',
        'belong[p] = len(parts)': '`nums[{p}]` 是新一段的开头，记 `belong[{p}] = {belong[p]}`',
        'while q < len(nums)': lambda S, B, r: (f'`nums[{S.q}] = {S.nums[S.q]} >= nums[{S.q-1}] = {S.nums[S.q-1]}` → 没有逆序对，继续并入当前段'
                                                  if S.q < len(S.nums) and S.nums[S.q] >= S.nums[S.q - 1] else
                                                  (f'`nums[{S.q}] = {S.nums[S.q]} < nums[{S.q-1}] = {S.nums[S.q-1]}` → 出现逆序，这一段到 `{S.q-1}` 为止' if S.q < len(S.nums) else '到数组末尾，这一段结束')),
        'belong[q] = len(parts)': '`belong[{q}] = {belong[q]}`：并入第 {belong[q]} 段',
        'parts.append': '记下这一段 `{parts[-1]}`，长度 `{q-p}`',
        's.append': '这一段共有 `cnt({q-p}) = {cnt(q-p)}` 个稳定子数组，`s` 末尾加入累计值 `{s[-1]}`',
        'if belong[x] == belong[y]': '`belong[{x}] = {belong[x]}`，`belong[{y}] = {belong[y]}` → {"==同一段==，任意子数组都稳定" if belong[x] == belong[y] else "==不同段==，分三部分算"}',
        'res.append(cnt(y - x + 1))': '长度 `{y-x+1}` → `cnt = {cnt(y-x+1)}`',
        'res.append(cnt(parts': '左头 `cnt({parts[belong[x]][1]-x+1})` + 右尾 `cnt({y-parts[belong[y]][0]+1})` + 中间整段 `s[{belong[y]}] − s[{belong[x]+1}]` = =={res[-1]}==',
    },
    cards=dict(
        one_liner='稳定 = 不减；稳定子数组不会跨过两段的交界',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['子数组里没有逆序对就是稳定的',
                 '每个询问 `[left, right]`：数 `nums[left..right]` 中稳定子数组的个数',
                 '示例：`nums=[3,1,2]`，查询 `[0,2]` → `4`'],
        quote='稳定子数组实际上就是单调不减的子数组，于是可以先一趟遍历，尽可能长地分离出nums中所有的单调不减子数组，不妨将这些子数组记为parts。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻两段交界处必有逆序对，所以稳定子数组只会落在某一段里面',
              '长为 `length` 的段里有 `(1+length)*length//2` 个，记作 `cnt(length)`',
              '`belong[i]` 记每个下标属于哪段；跨段时 = 左头 + 右尾 + 中间整段（前缀和之差）'],
        summary=['预处理 `O(n)`，每次询问 `O(1)`',
                 '`s[0] = 0` 使下标有 1 的偏移：中间段之和是 `s[belong[y]] - s[belong[x]+1]`，不是 `s[belong[y]-1] - s[belong[x]]`',
                 '同一段和跨段要分开算',
                 '对比灵神：灵神用 `nxt` 数组直接找 `l` 右边下一段的起点，yiduobo 用 `belong` 记归属'],
    ),
)
