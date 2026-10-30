def _txt(S):
    if 'now' not in S:
        return '把 0 当成 −1：区间和 > 0 ⇔ 1 比 0 多'
    return (f"前缀和 `now = {S['now']}`（树状数组下标 = now + n = {S['now'] + S['n']}），"
            f"左侧更小的前缀和共 `res = {S['res']}` 个")


def _hl(S, i, v):
    # 树状数组 f 中，当前正在 add / get 经过的位置
    x = S.get('_inner', {}).get('x') if isinstance(S.get('_inner'), dict) else None
    return 'yellow' if x is not None and i == x else None


CONFIG = dict(
    num=2031, title='1比0多的子数组个数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='0 变 −1 · 前缀和 + 树状数组',
    tags=['常用数据结构', '前缀和'],
    code='''
class Solution(object):
    def subarraysWithMoreZerosThanOnes(self, nums):

        n = len(nums)
        f = [0] * (n + n + 2)
        mod = 10 ** 9 + 7

        def add(x):
            while x <= n + n + 1:
                f[x] += 1
                if f[x] >= mod:
                    f[x] -= mod
                x += x & -x

        def get(x):
            res = 0
            while x > 0:
                res += f[x]
                if res >= mod:
                    res -= mod
                x -= x & -x
            return res

        res = 0
        now = 0
        add(n + 1)
        for v in nums:
            if v == 0:
                now -= 1
            else:
                now += 1
            
            res += get(now + n)
            if res >= mod:
                res -= mod
            add(now + n + 1)
        
        return res
''',
    call='Solution().subarraysWithMoreZerosThanOnes([0,1,1])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（0 当成 −1）', cell=84, h=150),
        dict(type='array', var='f', label='f：树状数组，下标 = 前缀和 + n + 1（f[0] 不用）', cell=62, h=210,
             color=_hl),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    skip=['for v in nums', 'if f[x] >= mod', 'f[x] -= mod', 'if res >= mod', 'res -= mod'],
    watch=[('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [0] *': '前缀和范围是 `[-n, n]`，整体加 `n + 1` 当树状数组下标，所以开 `2n + 2` 个格子',
        'add(n + 1)': '先放入空前缀：`now = 0` → 下标 `n + 1`',
        'now -= 1': '读到 `0`，当作 −1：`now` = {now}',
        'now += 1': '读到 `1`，当作 +1：`now` = {now}',
        'res += get': '查 `get({now + n})`：左边下标 ≤ `{now + n}`（即前缀和 ==严格小于== `{now}`）的有几个？沿树状数组向前跳着累加',
        'add(now + n + 1)': '此时 `res` = =={res}==；把当前前缀和登记进树状数组：下标 `{now + n + 1}` 加 1，沿父节点向上更新',
        'x += x & -x': '往上跳到父节点：`x` = {x}',
        'x -= x & -x': '去掉最低位，跳到前面一段：`x` = {x}',
        'f[x] += 1': '`f[{x}] += 1`：这个节点管的区间包含新前缀和',
        'res += f[x]': '累加 `f[{x}]` = {f[x]}，`res` = {res}',
        22: '`get` 返回 `{res}`：左侧有 `{res}` 个前缀和比当前更小，各对应一个合格子数组',
        38: '1 比 0 多的子数组共 `{res}` 个',
    },
    cards=dict(
        one_liner='0 当 −1，数「左边比我小的前缀和」，用树状数组数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给 0/1 数组 `nums`，数有多少个子数组里 `1` 的个数多于 `0` 的个数',
                 '答案对 `10^9 + 7` 取模',
                 '示例：`[0,1,1]` → `4`（`[1]`×2、`[1,1]`、`[0,1,1]`）'],
        quote='将0视为-1，那么区间[l, r]的和就相当于区间中1的数量减去区间中0的数量，于是本题就转化成了找出所有区间和大于0的区间数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和 = 前缀和之差：`s[r] > s[l]` 才合格',
              '遍历到 r，问左侧有多少个前缀和比 `s[r]` 小 → 树状数组前缀查询',
              '前缀和可为负，整体加 `n + 1` 当下标；`get(now + n)` 恰好查「< now」'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '下标偏移：`get` 用 `now + n`，`add` 用 `now + n + 1`，别搞混',
                 '树状数组下标从 1 开始，所以 `n + 1` 起步而不是 `n`',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
