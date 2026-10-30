def _sc(S):
    return S.get('s')


CONFIG = dict(
    num=798, title='得分最高的最小轮调', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 每个数贡献一段轮调区间',
    tags=['灵神题单·常用数据结构', '难度分 2130'],
    code='''
class Solution:
    def bestRotation(self, nums: List[int]) -> int:
        n = len(nums)
        diff = [0] * (n + 1)
        for i, x in enumerate(nums):
            # 把 x 轮调到 [x, n-1] 中，就能得到 1 分
            if i < x:  # i 在 [x, n-1] 左侧
                # 需要轮调 [i+1, i+n-x] 次
                diff[i + 1] += 1
                diff[i + 1 + n - x] -= 1
            else:  # i 在 [x, n-1] 中
                # 先把每个 score[k] 都加一
                diff[0] += 1
                # 轮调 [i+1-x, i] 次无法得分，减掉
                diff[i + 1 - x] -= 1
                diff[i + 1] += 1

        max_sum = best_k = s = 0
        for i, d in enumerate(diff):
            s += d
            # 此时 s 为轮调 i 次后的得分
            if s > max_sum:
                max_sum = s
                best_k = i
        return best_k
''',
    call='Solution().bestRotation([2,3,1,4,0])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（x = nums[i]）', pointers={'i if _line < 18 else None': 'blue'}, pointer_labels={'i if _line < 18 else None': 'i'}, h=210,
             color=lambda S, i, v: 'blue' if S.get('s') is None and i == S.get('i') else None),
        dict(type='array', var='diff', label='diff（差分数组，下标 = 轮调次数 k）', pointers={'i': 'pink'}, h=250,
             color=lambda S, i, v: ('green' if i == S.get('best_k') and S.get('s') is not None and i < S.get('i', 0) + 1 else None)),
        dict(type='text', size=30, h=90, fn=lambda S: (
            f"前缀和 `s` = 轮调 `{S['i']}` 次后的得分 = =={S['s']}==，目前最高 `{S['max_sum']}`（k = {S['best_k']}）"
            if S.get('s') is not None and 'max_sum' in S else
            (f"x = `{S['x']}`：{'i < x，在 [x, n-1] 左侧' if S['i'] < S['x'] else 'i ≥ x，已在 [x, n-1] 中'}"
             if 'x' in S and 'i' in S else ''))),
    ],
    watch=['i', 'x', 's', ('max_sum', 'max_sum', 'green'), ('best_k', 'best_k', 'orange')],
    captions={
        'diff = [0]': '`diff` 长 `n+1`：差分数组，最后一位留给 `r+1` 越界',
        'if i < x': '`i = {i}`，`x = {x}`：{"i < x，下标 i 在 [x, n-1] 左侧，要往右轮到 [x, n-1] 才得分" if i < x else "i ≥ x，下标 i 本来就在 [x, n-1] 中，已经有 1 分"}',
        9: '区间起点：`diff[{i+1}] += 1`，从轮调 `{i+1}` 次起得分',
        16: '`diff[{i+1}] += 1`：轮调 `{i+1}` 次后 x 到了 n-1 这一端，又得分，抵消上一步的减一',
        'diff[i + 1 + n - x] -= 1': '区间终点：轮调到 `{i+n-x}` 次为止，`diff[{i+1+n-x}] -= 1`',
        'diff[0] += 1': '先给所有 k 都加 1 分：`diff[0] += 1`',
        'diff[i + 1 - x] -= 1': '轮调 `[{i+1-x}, {i}]` 次，x 被转出 [x, n-1]，丢分：`diff[{i+1-x}] -= 1`',
        'max_sum = best_k = s': '`s` 累加前缀和，`max_sum` 记最高分，`best_k` 记最小的 k',
        's += d': '前缀和 `s += {d}` → =={s}==（轮调 `{i}` 次的得分）',
        'if s > max_sum': '`{s} > {max_sum}` → {"更高，更新" if s > max_sum else "不更高，保留较小的 k"}',
        'best_k = i': '最高分 `{max_sum}`，对应 `k = {best_k}`（严格大于才更新，所以 k 最小）',
        'return best_k': '返回得分最高的最小 `k = {best_k}`',
    },
    cards=dict(
        one_liner='横看成岭侧成峰：单看每个数，它给哪些 k 加 1 分',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组轮调 `k` 次，值 `<=` 下标的项得 1 分',
                 '返回得分最高的最小 `k`',
                 '示例：`[2,3,1,4,0]` → `3`（此时得分 4）'],
        quote='横看成岭侧成峰，单看 nums[i]，它会如何影响数组 score？哪些 score[k] 会增加 1？',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x = nums[i]`：只要把它轮到下标 `[x, n-1]` 就得 1 分',
              '`i < x`：轮调 `[i+1, i+n-x]` 次可得分，是一段区间 +1',
              '`i >= x`：先全体 +1，再把 `[i+1-x, i]` 这段减掉',
              '区间加一用差分，前缀和就是每个 k 的得分'],
        summary=['时间 `O(n)`，空间 `O(n)`，暴力是 `O(n^2)`',
                 '差分数组开 `n+1`，`i+1+n-x` 可能等于 `n`',
                 '用 `s > max_sum` 严格大于，保证返回最小的 k',
                 '同类题：1674 使数组互补的最少操作次数'],
    ),
)
