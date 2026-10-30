CONFIG = dict(
    num=2547, title='拆分数组的最小代价', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP · 哈希表倒序计数',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def minCost(self, nums, k):

        f = [0]
        n = len(nums)
        for i in range(n):
            mi = None
            s = 0
            cnt = {}
            for j in range(i, -1, -1):
                if nums[j] not in cnt:
                    cnt[nums[j]] = 1
                else:
                    if cnt[nums[j]] == 1:
                        s += 2
                    else:
                        s += 1
                    
                    cnt[nums[j]] += 1
                
                if mi is None or mi > f[j] + s + k:
                    mi = f[j] + s + k
            
            f.append(mi)

        return f[-1]
''',
    call='Solution().minCost([1,2,1,1], 2)',
    expect=5,
    max_steps=85,
    skip=['n = len(nums)', 's = 0', 'cnt = {}'],
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 最后一段 nums[j..i]）', window=('j', 'i'), pointers={'j': 'blue', 'i': 'pink'}, h=210),
        dict(type='map', var='cnt', label='cnt：最后一段里每个数出现几次', h=190),
        dict(type='array', var='f', label='f[t]：前 t 个数的最小代价', pointers={'j': 'blue'}, h=200),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('s', 's（trimmed 长度）', 'cyan'), ('mi', 'mi', 'orange')],
    captions={
        'f = [0]': '`f[t]` = 前 `t` 个数的最小代价，`f[0] = 0`',
        'for i in range': lambda S, B, r: (f'算 `f[{S.i+1}]`：枚举最后一段的左边界 `j`' if len(S.f) == S.i + 1 else '所有 `i` 都算完了'),
        'mi = None': '新一轮：`mi` 记录 `f[i+1]` 的最小值，`s` 清零（trimmed 长度），`cnt` 清空（出现次数）',
        'if nums[j] not in cnt': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]}` 第一次出现 → 落单，不影响 `s`' if S.nums[S.j] not in S.cnt else f'`nums[{S.j}] = {S.nums[S.j]}` 之前出现过'),
        'cnt[nums[j]] = 1': '记下 `{nums[j]}` 出现 1 次，`s` 不变 = {s}',
        'if cnt[nums[j]] == 1': lambda S, B, r: (f'`{S.nums[S.j]}` 之前只出现 1 次，现在变成 2 次' if S.cnt[S.nums[S.j]] == 1 else f'`{S.nums[S.j]}` 之前已出现 {S.cnt[S.nums[S.j]]} 次'),
        's += 2': '1 次 → 2 次：落单的数变成两个都保留，`s` += `2` → {s}',
        's += 1': '出现次数已经 ≥ 2：又多一个要保留的数，`s` += `1` → {s}',
        'cnt[nums[j]] += 1': '`{nums[j]}` 出现 {cnt[nums[j]]} 次',
        'if mi is None': lambda S, B, r: (f'候选 `f[{S.j}] + s + k = {S.f[S.j]} + {S.s} + {S.k} = {S.f[S.j]+S.s+S.k}`' + (' ，第一个候选' if S.mi is None else f'，和 `mi = {S.mi}` 比较')),
        'mi = f[j] + s + k': '更新最小值：`mi = {mi}`',
        'f.append(mi)': '`f[{i+1}] = {mi}`：前 {i+1} 个数的最小代价',
        'return f[-1]': '`f[n]` 就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='f[i] = min(f[j] + cost(j, i))，用哈希表增量维护 cost',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把数组拆成若干子数组，代价 = 每段的 `k + trimmed长度`',
                 '`trimmed` 去掉只出现一次的数，剩下的个数就是 `trimmed` 的长度',
                 '本视频：`nums = [1,2,1,1]`，`k = 2` → `5`'],
        quote='落单数字并不会影响到cost的计算，而当某个数字出现次数由1变成2时，其对cost的影响则会从0变为2。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 表示划分前 `i` 个数的最小代价，枚举最后这段的左边界 `j`',
              '`j` 从 `i` 往左扫，哈希表 `cnt` 记录每个数出现次数，`cost` 增量更新',
              '次数 `0→1`：`s` 不变；`1→2`：`s` +2；`≥2`：`s` +1'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`s` 就是 trimmed 的长度，别忘了每段还要加 `k`',
                 '`f[0] = 0` 表示没有元素，不需要代价',
                 '原文已经是 Python 3 可运行的写法，未做修改'],
    ),
)
