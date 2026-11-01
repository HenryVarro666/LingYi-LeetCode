CONFIG = dict(
    num=2025, title='分割数组的最多方案数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 两个哈希表（Go 原文转写）',
    tags=['一、前缀和', '§1.2 前缀和与哈希表', '难度分 2218'],
    code='''
class Solution:
    def waysToPartition(self, nums: List[int], k: int) -> int:
        ans = 0
        n = len(nums)
        sum = [0] * n
        sum[0] = nums[0]
        cntR = defaultdict(int)
        for i in range(1, n):
            sum[i] = sum[i - 1] + nums[i]
            cntR[sum[i - 1]] += 1
        tot = sum[n - 1]
        if tot % 2 == 0:
            ans = cntR[tot // 2]  # 不修改
        cntL = defaultdict(int)
        for i, s in enumerate(sum):
            d = k - nums[i]
            if (tot + d) % 2 == 0:
                ans = max(ans, cntL[(tot + d) // 2] + cntR[(tot - d) // 2])  # 修改 nums[i]
            cntL[s] += 1
            cntR[s] -= 1
        return ans
''',
    call='Solution().waysToPartition([3,1,-2,1,1,0], 2)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=150),
        dict(type='array', var=lambda S: S.get('sum'), label='sum：前缀和', h=150,
             color=lambda S, i, v: 'green' if 'tot' in S and S['tot'] % 2 == 0 and v == S['tot'] // 2 and i < len(S['sum']) - 1 else None),
        dict(type='map', var='cntR', label='cntR：右侧分割点前缀和个数', h=140, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='map', var='cntL', label='cntL：左侧分割点前缀和个数', h=140, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='text', h=70, fn=lambda S: (f"改 `nums[{S['i']}]` 为 {S['k']}：`d = {S['d']}`，左找 `(tot+d)/2 = {(S['tot']+S['d'])/2:g}`，右找 `(tot-d)/2 = {(S['tot']-S['d'])/2:g}`" if 'd' in S and 'i' in S and 'tot' in S else (f"总和 `tot = {S['tot']}`" if 'tot' in S else ''))),
    ],
    watch=['i', 'tot', 'd', ('ans', 'ans', 'green')],
    captions={
        'sum = [0] * n': '`sum[i]`：nums 的前缀和，分割点 i 的左边和就是 `sum[i]`',
        'cntR[sum[i - 1]] += 1': '`sum[{i}] = {sum[i]}`；先把 `sum[{i - 1}] = {sum[i - 1]}` 记进 `cntR`：最初所有分割点都在右边',
        'tot = sum[n - 1]': '全部元素之和 `tot = {tot}`',
        'if tot % 2 == 0': '不修改：左和 = 右和，即 `sum[i] = tot / 2`，所以 `tot` 必须是偶数：`{tot} % 2 = {tot % 2}`',
        'ans = cntR[tot // 2]': '不修改时的方案数：`cntR[{tot // 2}] = =={cntR[tot // 2]}==`',
        'cntL = defaultdict': '`cntL` 记录 i 左侧（含 i 之前）的前缀和，从空开始',
        'for i, s in enumerate(sum)': '枚举要修改的位置 `i`，`s = sum[i]`',
        'd = k - nums[i]': '把 `nums[{i}] = {nums[i]}` 改成 `k = {k}`：变化量 `d = {d}`',
        'if (tot + d) % 2 == 0': '修改后总和为 `tot + d = {tot + d}`，要能平分必须是偶数 → {"是" if (tot + d) % 2 == 0 else "否，跳过"}',
        'ans = max(ans, cntL': '左侧前缀和不变，找 `(tot+d)/2 = {(tot + d) // 2}`：`cntL` 有 {cntL[(tot + d) // 2]} 个；右侧前缀和都加了 d，找 `(tot-d)/2 = {(tot - d) // 2}`：`cntR` 有 {cntR[(tot - d) // 2]} 个 → `ans` = =={ans}==',
        'cntL[s] += 1': '`sum[{i}] = {s}` 从右侧移到左侧：`cntL[{s}]` 加 1',
        'cntR[s] -= 1': '同时 `cntR[{s}]` 减 1，下个位置接着用',
    },
    cards=dict(
        one_liner='枚举改哪个数，两个哈希表 O(1) 数出合法分割点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['分割点 pivot：左边和 = 右边和；可把一个数改成 k（或不改）',
                 '求最多能有多少个合法分割点',
                 '本视频：`[3,1,-2,1,1,0], k=2` → `2`'],
        quote='枚举修改的元素，记变化量 d=k-nums[i]，这一修改操作对于 i 左侧的前缀和是没有影响的……而对于 i 右侧的前缀和，每个前缀和都增加了 d。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不修改：满足 `sum[i] = tot / 2` 的位置个数',
              '修改 `nums[i]`：左侧前缀和不变，要等于 `(tot+d)/2`；右侧前缀和各加 d，原值要等于 `(tot-d)/2`',
              '`cntL`、`cntR` 随 i 右移动态维护，每个 i 只查两次表'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`defaultdict` 代替 Go 的 map，Go 里自定义的 `max` 用内置）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：`tot + d` 必须是偶数才能平分；左右两个表对应的目标值不同（`+d` 与 `-d`）',
                 '`cntR` 一开始装的是 `sum[0..n-2]`，最后一个前缀和（总和）不是分割点'],
    ),
)
