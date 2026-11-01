CONFIG = dict(
    num=2025, title='分割数组的最多方案数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 左右哈希表',
    tags=['一、前缀和', '§1.2 前缀和与哈希表', '难度分 2218'],
    code='''
class Solution(object):
    def waysToPartition(self, nums, k):

        s = [nums[0]]
        n = len(nums)
        for num in nums[1:]:
            s.append(s[-1] + num)
        
        left_cnt = {}
        for index in range(n - 1):
            left_cnt[s[index]] = left_cnt.get(s[index], 0) + 1
        
        if s[-1] % 2 == 0:
            res = left_cnt.get(s[-1] // 2, 0)
        else:
            res = 0
        
        if (s[-1] + k - nums[-1]) % 2 == 0:
            res = max(res, left_cnt.get((s[-1] + k - nums[-1]) // 2, 0))

        right_cnt = {}
        for index in range(n - 2, -1, -1):
            left_cnt[s[index]] -= 1
            right_cnt[s[index]] = right_cnt.get(s[index], 0) + 1
            delta = k - nums[index]

            if (s[-1] + delta) % 2 == 0:
                res = max(res, left_cnt.get((s[-1] + delta) // 2, 0) + right_cnt.get((s[-1] + delta) // 2 - delta, 0))
        
        return res
''',
    call='Solution().waysToPartition([3,1,-2,1,1,0], 2)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=150),
        dict(type='array', var='s', label='s：前缀和', h=150),
        dict(type='map', var='left_cnt', label='left_cnt：index 之前的前缀和个数', h=140, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='map', var='right_cnt', label='right_cnt：index 及之后的原始前缀和个数', h=140, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='text', h=70, fn=lambda S: (f"改 `nums[{S['index']}]` 为 {S['k']}：`delta = {S['delta']}`，左找 `{(S['s'][-1]+S['delta'])/2:g}`，右找 `{(S['s'][-1]+S['delta'])/2-S['delta']:g}`" if 'delta' in S and 'index' in S else (f"总和 `s[-1] = {S['s'][-1]}`" if 's' in S and len(S['s']) == len(S.get('nums', [])) else ''))),
    ],
    watch=['index', 'delta', ('res', 'res', 'green')],
    captions={
        's = [nums[0]]': '`s` 是前缀和数组：`s[i]` = nums[0..i] 之和，分割点 pivot 的左边和是 `s[pivot-1]`',
        'for num in nums[1:]': '依次累加：当前前缀和 `s[-1] + num`',
        'for index in range(n - 2': '下标从 `n - 2` 往左枚举，依次当作被修改的位置',
        'left_cnt = {}': '`left_cnt` 先装下 `s[0..n-2]` 的出现次数（`s[-1]` 是总和，不是分割点）',
        'if s[-1] % 2 == 0': '不修改：需要 `s[pivot-1] = sum / 2`，总和 `{s[-1]}` 必须是偶数 → {"是" if s[-1] % 2 == 0 else "否，res = 0"}',
        'res = left_cnt.get(s[-1] //': '不修改的方案数：`left_cnt[{s[-1] // 2}]` → =={res}==',
        'if (s[-1] + k - nums[-1]) % 2 == 0': '先试修改最后一个数：新总和 `{s[-1] + k - nums[-1]}`，偶数才可能平分',
        'res = max(res, left_cnt.get((s[-1] + k': '改最后一个数：所有分割点都在它左边，前缀和不变，只数目标 `{(s[-1] + k - nums[-1]) // 2}` → `res` = =={res}==',
        'right_cnt = {}': '再从右往左枚举被修改的下标，`right_cnt` 从空开始',
        'left_cnt[s[index]] -= 1': '`s[{index}] = {s[index]}` 不再属于 index 之前，从 `left_cnt` 里减掉',
        'right_cnt[s[index]] = ': '把 `s[{index}] = {s[index]}` 加入 `right_cnt`（修改后它要加上 delta）',
        'delta = k - nums[index]': '修改 `nums[{index}]` 为 `{k}`：`delta = {delta}`',
        'if (s[-1] + delta) % 2 == 0': '新总和 `{s[-1] + delta}`：{"偶数，可以平分" if (s[-1] + delta) % 2 == 0 else "奇数，无解，跳过"}',
        'res = max(res, left_cnt.get((s[-1] + delta)': '目标 `target = {(s[-1] + delta) // 2}`：左边 `left_cnt` 有 {left_cnt.get((s[-1] + delta) // 2, 0)} 个；右边前缀和多了 delta，找 `target - delta = {(s[-1] + delta) // 2 - delta}`，有 {right_cnt.get((s[-1] + delta) // 2 - delta, 0)} 个 → `res` = =={res}==',
    },
    cards=dict(
        one_liner='先看不改的情况，再从右往左枚举改哪个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['分割点 pivot：左边和 = 右边和；可把一个数改成 k（或不改）',
                 '求最多合法分割点数',
                 '本视频：`[3,1,-2,1,1,0], k=2` → `2`'],
        quote='对于index - 1以及之前的所有位置，对应的前缀和都不会发生变化。而对于s[index]以及之后的s，则都会在原始s的基础上加上k - nums[index]。',
        quote_src='—— yiduobo 题解原文',
        idea=['不改数：数一数前缀和等于 `sum/2` 的个数',
              '改 `nums[index]`：目标变成 `(sum + delta)/2`，左边前缀和不变，右边的原始前缀和要等于 `target - delta`',
              '用 `left_cnt` 和 `right_cnt` 在下标从右往左移动时一减一加，查表即得方案数'],
        summary=['原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 3 处）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：新总和必须是偶数；`s[-1]` 不是分割点，所以只统计 `s[0..n-2]`',
                 '最后一个下标单独处理：改它时没有右边的前缀和需要平移',
                 '对比灵神：灵神从左到右扫，yiduobo 从右到左扫，思路等价'],
    ),
)
