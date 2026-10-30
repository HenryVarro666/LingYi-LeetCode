def _txt(S):
    if 's1' not in S or 'right' not in S:
        if 'c' in S and 'pos' in S and 'size' not in S:
            return f'最长连续 1（≤3）：`c = {S["c"]}`；`c` 个 1 用 `c−1` 次操作，其余 1 各 2 次'
        return '1 的位置 `pos` 上，枚举长为 `k − max_changes` 的窗口，货仓选址选中位数'
    if S.get('_line', 0) < 30:
        return f'下一个窗口：`right = {S["right"]}`，取 `pos` 中长 `{S["size"]}` 的一段'
    if S.get('_line', 0) < 32:
        return f'窗口 `pos[{S["left"]}:{S["right"]}]`，中位数 `pos[{S["i"]}] = {S["pos"][S["i"]]}`'
    return (f'窗口 `pos[{S["left"]}:{S["right"]}]` 到中位数 `pos[{S["i"]}] = {S["pos"][S["i"]]}` 的距离和 = '
            f'`{S["s1"]} + {S["s2"]}` = =={S["s1"] + S["s2"]}==')


def _wcol(S, i, v):
    if S.get('_line', 0) >= 30 and 'right' in S and 'left' in S and 'i' in S and 'size' in S and 'pre_sum' in S:
        if i == S['i'] and S['left'] <= i < S['right']:
            return 'yellow'
        if S['left'] <= i < S['right']:
            return 'blue'
    return None


CONFIG = dict(
    num=3086, title='拾起 K 个 1 需要的最少行动次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分类讨论 + 中位数贪心 + 前缀和',
    tags=['前缀和', '中位数贪心', '难度分 2673'],
    code='''
class Solution:
    def minimumMoves(self, nums: List[int], k: int, max_changes: int) -> int:
        pos = []
        c = 0  # nums 中连续的 1 长度
        for i, x in enumerate(nums):
            if x == 0:
                continue
            pos.append(i)  # 记录 1 的位置
            c = max(c, 1)
            if i > 0 and nums[i - 1] == 1:
                if i > 1 and nums[i - 2] == 1:
                    c = 3  # 有 3 个连续的 1
                else:
                    c = max(c, 2)  # 有 2 个连续的 1

        c = min(c, k)
        if max_changes >= k - c:
            # 其余 k-c 个 1 可以全部用两次操作得到
            return max(c - 1, 0) + (k - c) * 2

        n = len(pos)
        pre_sum = list(accumulate(pos, initial=0))

        ans = inf
        # 除了 max_changes 个数可以用两次操作得到，其余的 1 只能一步步移动到 pos[i]
        size = k - max_changes
        for right in range(size, n + 1):
            # s1+s2 是 j 在 [left, right) 中的所有 pos[j] 到 pos[(left+right)/2] 的距离之和
            left = right - size
            i = left + size // 2
            s1 = pos[i] * (i - left) - (pre_sum[i] - pre_sum[left])
            s2 = pre_sum[right] - pre_sum[i] - pos[i] * (right - i)
            ans = min(ans, s1 + s2)
        return ans + max_changes * 2
''',
    call='Solution().minimumMoves([1,1,0,0,1,0,1], 4, 1)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在扫描的位置）', h=170, pointers={'_none': 'blue'},
             color=lambda S, i, v: 'blue' if 'size' not in S and S.get('i') == i else None),
        dict(type='array', var='pos', label='pos：1 的位置（蓝 = 窗口，黄 = 中位数）', h=190,
             color=_wcol),
        dict(type='array', var='pre_sum', label='pre_sum：pos 的前缀和', h=150),
        dict(type='text', fn=_txt, h=70),
    ],
    watch=['c', 'size', 'left', 'right', ('s1', 's1', 'cyan'), ('s2', 's2', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'c = max(c, 1)': '有 1：至少有 `1` 个连续的 1，`c = {c}`',
        'c = 3': '`nums[{i-2}..{i}]` 三个连续的 1：站在中间，`c = 3`',
        'c = max(c, 2)': '`nums[{i-1}..{i}]` 两个连续的 1，`c = {c}`',
        'pos.append(i)': '位置 `{i}` 是 1，记入 `pos = {pos}`',
        'c = min(c, k)': '`c` 最多只需要 `k` 个：`c = {c}`',
        'if max_changes >= k - c': lambda S, B, r: (f'`max_changes = {S.max_changes}` ≥ `k − c = {S.k - S.c}`？'
                                                    + ('成立 → 其余的 1 全用 2 次操作造出来' if S.max_changes >= S.k - S.c
                                                       else '不成立：造的 1 不够，剩下的要一步步挪过来')),
        'pre_sum = ': '前缀和 `pre_sum = {pre_sum}`：以后任意一段 `pos` 的和 `O(1)` 出',
        'size = k': '造 `max_changes = {max_changes}` 个 1 各花 2 次，其余 `size = {size}` 个 1 要自己挪过来',
        'for right in range': lambda S, B, r: ('窗口都枚举完了' if 'right' in B and B.right == S.right
                                               else f'窗口 `pos[{S.right - S.size}:{S.right}]`：一共 {S.size} 个 1'),
        'left = right - size': '窗口左端 `left = {left}`',
        'i = left': '货仓选址：窗口的中位数下标 `i = {i}`，位置 `pos[{i}] = {pos[i]}`',
        's1 = ': '左边距离和：`pos[i]×(i−left) − (前缀和之差)` = `{pos[i]}×{i - left} − {pre_sum[i] - pre_sum[left]}` = =={s1}==',
        's2 = ': '右边距离和：`(前缀和之差) − pos[i]×(right−i)` = `{pre_sum[right] - pre_sum[i]} − {pos[i]}×{right - i}` = =={s2}==',
        'ans = min': '窗口代价 `{s1} + {s2}` = {s1 + s2}，`ans = min({B.ans}, {s1 + s2}) = {ans}`',
        'return ans + max_changes': '最少行动 = 挪 1 的最小代价 `{ans}` + 造 1 的 `{max_changes}×2` = =={ans + max_changes * 2}==',
    },
    cards=dict(
        one_liner='造 1 花 2 次，其余的 1 挪过来，货仓选址取中位数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是 0/1 数组，Alice 站在某处拾起 `k` 个 1',
                 '动作：最多 `maxChanges` 次把 0 变成 1；或交换相邻的 1 和 0（挪到 Alice 处就拾起）',
                 '示例：`[1,1,0,0,0,1,1,0,0,1]`，`k=3`，`maxChanges=1` → `3`',
                 '视频用 `[1,1,0,0,1,0,1]`，`k=4`，`maxChanges=1` → `6`（造的 1 不够，要走窗口）'],
        quote='贪心地把和 aliceIndex 相邻的 0 变成 1……然后结合第二种操作，把相邻的 1 移动到 aliceIndex，只需 2 次操作就可以得到一个 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一种操作 + 第二种操作：2 次得一个 1；站在连续 1 上，旁边的 1 只要 0/1 次',
              '`max_changes` 够大：`max(c−1,0) + (k−c)×2`',
              '否则造满 `max_changes` 个，其余 `k − max_changes` 个 1 一步步挪：货仓选址，取窗口中位数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`c` 是长度不超过 3 的最长连续 1，要和 `k` 取 `min`',
                 '窗口 `[left, right)` 长 `size`，中位数下标 `left + size//2`，距离和 = `s1 + s2`',
                 '无需再关心 `aliceIndex`：站在中位数的 1 上最优',
                 '灵神注：也有不用前缀和的滑窗做法（见 2968 题解法二）'],
    ),
)
