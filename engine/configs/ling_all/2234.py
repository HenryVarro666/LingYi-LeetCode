CONFIG = dict(
    num=2234, title='花园的最大总美丽值', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 枚举种满的后缀 + 前缀倒水双指针',
    tags=['灵神题单', '难度分 2562'],
    code='''
class Solution:
    def maximumBeauty(self, flowers: List[int], newFlowers: int, target: int, full: int, partial: int) -> int:
        n = len(flowers)
        for i in range(n):
            flowers[i] = min(flowers[i], target)

        # 如果全部种满，还剩下多少朵花？
        left_flowers = newFlowers - (target * n - sum(flowers))

        # 没有种花，所有花园都已种满
        if left_flowers == newFlowers:
            return n * full  # 答案只能是 n*full（注意不能减少花的数量）

        # 可以全部种满
        if left_flowers >= 0:
            # 两种策略取最大值：留一个花园种 target-1 朵花，其余种满；或者，全部种满
            return max((target - 1) * partial + (n - 1) * full, n * full)

        flowers.sort()  # 时间复杂度的瓶颈在这，尽量写在后面

        ans = pre_sum = j = 0
        # 枚举 i，表示后缀 [i, n-1] 种满（i=0 的情况上面已讨论）
        for i in range(1, n + 1):
            # 撤销，flowers[i-1] 不变成 target
            left_flowers += target - flowers[i - 1]
            if left_flowers < 0:  # 花不能为负数，需要继续撤销
                continue

            # 满足以下条件说明 [0, j] 都可以种 flowers[j] 朵花
            while j < i and flowers[j] * j <= pre_sum + left_flowers:
                pre_sum += flowers[j]
                j += 1

            # 计算总美丽值
            # 在前缀 [0, j-1] 中均匀种花，这样最小值最大
            avg = (left_flowers + pre_sum) // j  # 由于上面特判了，这里 avg 一定小于 target
            total_beauty = avg * partial + (n - i) * full
            ans = max(ans, total_beauty)

        return ans
''',
    call='Solution().maximumBeauty([1,3,1,1], 7, 6, 12, 1)',
    expect=14,
    views=[
        dict(type='text', size=27, h=90, fn=lambda S: (
            f"后缀 `[{S['i']}, {S['n']-1}]` 种满（{S['n']-S['i']} 个 × {S['full']}），前缀 `[0, {S['j']-1}]` 均匀种到 `{S['avg']}`" + (f" → 总分 =={S['total_beauty']}==" if S['_line'] >= 37 else '')
            if 'avg' in S and S['_line'] >= 36 and S['_line'] <= 38
            else ('先看能不能提前返回' if 'pre_sum' not in S else '枚举种满的后缀，剩余的花往前缀里「倒水」'))),
        dict(type='array', var='flowers', h=250, label='flowers（排序后）：粉 = 种满的后缀，蓝 = 被抬高的前缀',
             pointers={'i': 'pink', 'j': 'blue'},
             color=lambda S, k, v: ('pink' if 'pre_sum' in S and 'i' in S and k >= S['i'] else 'blue' if 'pre_sum' in S and k < S.get('j', 0) else None)),
    ],
    skip=['for i in range(n)', 'flowers[i] = min'],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), 'left_flowers', 'pre_sum', ('ans', 'ans', 'green')],
    captions={
        'left_flowers = newFlowers': '假设 ==全部种满==，还剩 `{B.newFlowers} − ({target}×{n} − {sum(flowers)})` = =={left_flowers}== 朵',
        'if left_flowers == newFlowers': '`left_flowers == newFlowers` 吗（{left_flowers} vs {newFlowers}）？不成立：说明有花园还没种满',
        'if left_flowers >= 0': '`left_flowers >= 0` 吗（{left_flowers}）？为负：花不够种满所有花园，要枚举',
        'flowers.sort()': '排序：==后缀就是原有花多的花园==，优先种满它们',
        'ans = pre_sum = j = 0': '`ans`、`pre_sum`（前缀和）、`j`（前缀长度）都从 0 开始',
        'for i in range(1, n + 1)': lambda S, B, r: ("枚举结束" if 'i' in B and B.i == S.i and S.i > 1 else f"枚举 `i = {S.i}`：后缀 `[{S.i}, {S.n-1}]` 种满" if S.i < S.n else f"枚举 `i = {S.i} = n`：后缀为空，==没有花园种满==，花全给前缀"),
        'left_flowers += target - flowers[i - 1]': '`flowers[{i-1}] = {flowers[i-1]}` 不再种满，退回 `{target} − {flowers[i-1]}` 朵 → `left_flowers = {left_flowers}`',
        'if left_flowers < 0': lambda S, B, r: (f"`left_flowers = {S.left_flowers} < 0`：花不够种满后缀 `[{S.i}, ...]` → 跳过，继续撤销" if S.left_flowers < 0 else f"`left_flowers = {S.left_flowers} >= 0` → 这个后缀种得起，往前缀倒水"),
        'continue': '花不够，换下一个 `i`（后缀缩短，花会回来）',
        'while j < i and flowers[j] * j': lambda S, B, r: (f"`flowers[{S.j}]×{S.j} = {S.flowers[S.j]*S.j} <= {S.pre_sum} + {S.left_flowers}` 成立 → 前缀长度 `{S.j+1}` 也能抬到 `flowers[{S.j}]`" if S.j < S.i and S.flowers[S.j] * S.j <= S.pre_sum + S.left_flowers else (f"`j = {S.j} == i`，前缀已到后缀边界" if S.j >= S.i else f"`flowers[{S.j}]×{S.j} = {S.flowers[S.j]*S.j} > {S.pre_sum + S.left_flowers}` → 花不够把前缀都抬到 `{S.flowers[S.j]}`，==前缀停在 j = {S.j}==")),
        'pre_sum += flowers[j]': '`pre_sum` += `flowers[{j}]` → {pre_sum}',
        'j += 1': '前缀多容纳一个花园：`j` → {j}（`j` 只增不减，随 `i` 变大而变长）',
        'avg = (left_flowers': '前缀 `[0, {j-1}]` 一共 `{pre_sum}` 朵 + 剩余 `{left_flowers}`，平均 `({left_flowers}+{pre_sum}) // {j}` = =={avg}==（最小值最大）',
        'total_beauty = avg': '总美丽值 = `{avg}×{partial} + ({n}−{i})×{full}` = =={total_beauty}==',
        'ans = max(ans, total_beauty)': '`ans = max({B.ans}, {total_beauty}) = {ans}`',
        'return ans': '枚举完所有后缀，最大总美丽值 =={ans}==',
    },
    cards=dict(
        one_liner='先枚举种满哪些园子（后缀），剩下的花往最矮的前缀里「倒水」',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['有 `n` 个花园，花数 `flowers[i]`，最多再种 `newFlowers` 朵',
                 '花数 `>= target` 为完善：每个得 `full`；另外「最少花数」的不完善园子得 `最少花数×partial`',
                 '本视频：`[1,3,1,1]`，新花 7，target 6，full 12，partial 1 → `14`'],
        quote='枚举把多少个花园种满，剩余的花种其他花园，让最小花朵数最大。……把这个过程想象成我们在往前缀中倒水。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，种满的是==花最多的后缀==，这样剩下的花最多',
              '剩余的花从最小的园子开始「倒水」抬高：前缀 `[0, j-1]` 均匀种',
              '后缀越短，剩余花越多，前缀 `j` 只增不减 → 双指针，免去每次重算'],
        after=[dict(heading='提前返回与另一种写法', lines=[
            '排序前先特判：全部已满 → `n × full`；花够全部种满 → 取两种策略的最大值',
            '这样把排序（瓶颈）放在特判之后，常数更小',
            '也可以对前缀用二分查 `j`，本视频展示的是更快的双指针']),],
        summary=['时间 `O(n log n)`，空间 `O(1)`，瓶颈在排序',
                 '`i = 0`（全种满）已经在前面特判，所以循环从 `i = 1` 开始',
                 '先把超过 `target` 的值压成 `target`，`avg` 才一定 `< target`',
                 '`left_flowers < 0` 时用 `continue`：后缀缩短时花会回来'],
    ),
)
