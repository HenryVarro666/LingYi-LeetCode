def _txt(S, B):
    if 'cnt' not in S:
        return '把数组看成环：反转、旋转都不拆开相邻关系'
    if 'ans' in S and S['ans'] != inf and S['_line'] >= 14:
        return f"递增方案的候选答案 ==`{S['ans']}`=="
    return f"`cnt = {S['cnt']}` 个断点，最近的断点位置 `p = {S['p']}`"


CONFIG = dict(
    num=3942, title='排序排列的最少操作数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='环形数组 · 找断点分类讨论', tags=['灵神题单', '难度分 1855'],
    code='''
class Solution:
    def minOperations(self, nums: list[int]) -> int:
        n = len(nums)
        cnt = p = 0
        for i in range(1, n):
            if nums[i - 1] > nums[i]:
                cnt += 1
                if cnt > 1:
                    break
                p = i

        if cnt == 0:  # 已是递增
            return 0
        if cnt == 1 and nums[0] > nums[-1]:  # 两个递增段
            ans = min(p, n - p + 2)
        else:
            ans = inf

        cnt = p = 0
        for i in range(1, n):
            if nums[i - 1] < nums[i]:
                cnt += 1
                if cnt > 1:
                    break
                p = i

        if cnt == 0:  # 已是递减
            return 1
        if cnt == 1 and nums[0] < nums[-1]:  # 两个递减段
            ans = min(ans, p + 1, n - p + 1)

        return -1 if ans == inf else ans
''',
    call='Solution().minOperations([1,2,3,4,0])',
    expect=3,
    skip=['for i in range'],
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'p': 'pink'}, h=330, cell=100,
             color=lambda S, i, v: 'pink' if 'p' in S and S['p'] and i == S['p'] and S['_line'] >= 8 else None),
        dict(type='text', fn=_txt, size=28, h=120),
    ],
    watch=['n', ('cnt', 'cnt', 'yellow'), ('p', 'p', 'pink'), ('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`，数组是 `0` 到 `n-1` 的排列',
        4: '`cnt` 数「下降」的次数，`p` 记下降处的下标；先检查能否由递增排列旋转得到',
        19: '再检查能否由递减排列旋转得到：这次数「上升」的次数 `cnt` 和位置 `p`',
        'if nums[i - 1] > nums[i]': lambda S, B, r: (f'`{S.nums[S.i-1]} > {S.nums[S.i]}`：出现下降，这里是递增段的断点' if S.nums[S.i - 1] > S.nums[S.i]
                                                      else f'`{S.nums[S.i-1]} < {S.nums[S.i]}`：仍在递增'),
        'cnt += 1': '断点数 `cnt = {cnt}`',
        'if cnt > 1': lambda S, B, r: ('断点多于 1 个：不是「一个递增排列旋转」，不用再数' if S.cnt > 1 else '只有 1 个断点，继续往后看'),
        'p = i': '记下断点位置 `p = {p}`',
        'if cnt == 0': lambda S, B, r: ('没有任何下降：已是递增 → 不需要操作' if S.cnt == 0 else '有断点，继续分析'),
        'if cnt == 1 and nums[0] > nums[-1]': lambda S, B, r: (f'一个断点且 `nums[0]={S.nums[0]} > nums[-1]={S.nums[-1]}`：首尾能接上 → 是两个递增段，可以旋转成递增'
                                                              if (S.cnt == 1 and S.nums[0] > S.nums[-1]) else '不满足 → 不可能由递增排列旋转得到'),
        'ans = min(p': '两种做法：只左旋 `p = {p}` 次；或反转 + 左旋 `n-p = {n-p}` 次 + 再反转，共 `n-p+2 = {n-p+2}` 次 → `ans` = =={ans}==',
        'ans = inf': '递增这一类不成立：`ans = inf`',
        'if cnt == 0:  # 已是递减': lambda S, B, r: ('没有任何上升：已是递减 → 反转 1 次' if S.cnt == 0 else '有一个上升断点，继续看是否是递减环'),
        'if nums[i - 1] < nums[i]': lambda S, B, r: (f'`{S.nums[S.i-1]} < {S.nums[S.i]}`：出现上升，递减段的断点' if S.nums[S.i - 1] < S.nums[S.i]
                                                      else f'`{S.nums[S.i-1]} > {S.nums[S.i]}`：仍在递减'),
        'if cnt == 1 and nums[0] < nums[-1]': lambda S, B, r: (f'一个断点且 `nums[0] < nums[-1]`：两个递减段' if (S.cnt == 1 and S.nums[0] < S.nums[-1])
                                                              else f'断点数 `cnt = {S.cnt}`：不是「一个递减排列旋转」→ 递减这一类不成立'),
        'ans = min(ans': '递减两种做法：左旋 `p` 次再反转共 `p+1`；或先反转再左旋 `n-p`，共 `n-p+1` → `ans` = =={ans}==',
        'return -1 if': lambda S, B, r: ('两类都不行：返回 `-1`' if S.ans == inf else f'取最小 `ans = {S.ans}`，返回它'),
    },
    cards=dict(
        one_liner='数组当成环：只有「旋转后的递增或递减」才可能排好序',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是 `0` 到 `n-1` 的排列，可以「整体反转」或「左旋一位」',
                 '求让数组变成递增的最少操作次数，不可能返回 `-1`',
                 '示例：`[1,2,3,4,0]` → `3`（反转、左旋 1 次、再反转）'],
        quote='想象你有一串念珠，操作 1 是把念珠翻个面，操作 2 是旋转念珠，都不会拆开念珠。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作不改变元素的相邻关系，所以 `nums` 必须是递增排列的旋转，或递减排列的旋转',
              '数下降处：递增旋转只能有 1 个下降点，且首尾要能接上 `nums[0] > nums[-1]`',
              '递增类：只左旋 `p` 次，或「反转 + 左旋 `n-p` + 反转」共 `n-p+2` 次',
              '递减类同理：`p+1` 或 `n-p+1`；四种取最小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：下降点个数为 0 → 递增，返回 0；上升点个数为 0 → 递减，返回 1',
                 '易错：只有一个断点还不够，首尾也要能接上',
                 '循环里断点超过 1 个就 `break`，不必扫完整个数组'],
    ),
)
