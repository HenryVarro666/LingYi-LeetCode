CONFIG = dict(
    num=2234, title='花园的最大总美丽值', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 倒序枚举种满 + 前缀「补平」数组二分',
    tags=['灵神题单', '难度分 2562'],
    code='''
class Solution(object):
    def maximumBeauty(self, flowers, newFlowers, target, full, partial):

        sorted_flowers = sorted(flowers)
        need_flowers = []
        full_cnt = 0
        for index in range(len(sorted_flowers)):
            if sorted_flowers[index] >= target:
                full_cnt += 1
            elif len(need_flowers) == 0:
                need_flowers.append(0)
            else:
                need_flowers.append(need_flowers[-1] + index * (sorted_flowers[index] - sorted_flowers[index - 1]))
        
        m = len(need_flowers)
        if m == 0:
            return full_cnt * full

        def find(r):
            if newFlowers >= need_flowers[r]:
                return r
            else:
                l = 0
                while l < r:
                    mid = (l + r + 1) >> 1
                    if newFlowers >= need_flowers[mid]:
                        l = mid
                    else:
                        r = mid - 1
                return l
        
        p = find(m - 1)
        delta = (newFlowers - need_flowers[p]) // (p + 1)
        if sorted_flowers[p] + delta >= target:
            res = full_cnt * full + (target - 1) * partial
        else:
            res = full_cnt * full + (sorted_flowers[p] + delta) * partial

        for index in range(m - 1, 0, -1):
            if newFlowers < target - sorted_flowers[index]:
                return res
            
            newFlowers -= (target - sorted_flowers[index])
            full_cnt += 1
            p = find(index - 1)
            delta = (newFlowers - need_flowers[p]) // (p + 1)
            if sorted_flowers[p] + delta >= target:
                res = max(res, full_cnt * full + (target - 1) * partial)
            else:
                res = max(res, full_cnt * full + (sorted_flowers[p] + delta) * partial)

        if newFlowers >= target - sorted_flowers[0]:
            res = max(res, (full_cnt + 1) * full)
        
        return res
''',
    call='Solution().maximumBeauty([1,3,1,1], 7, 6, 12, 1)',
    expect=14,
    views=[
        dict(type='text', size=27, h=90, fn=lambda S: (
            f"种满 `{S['full_cnt']}` 个 × {S['full']}；剩 `{S['newFlowers']}` 朵把前 `{S['p']+1}` 个抬到 `{S['sorted_flowers'][S['p']] + S['delta']}` → 本轮 res = =={S['res']}=="
            if 'res' in S and 'delta' in S and 'p' in S else
            ('need_flowers[i] = 把前 i+1 个都抬到 sorted_flowers[i] 要多少花' if 'full_cnt' in S else ''))),
        dict(type='array', var='sorted_flowers', h=260, label='sorted_flowers（粉箭头 = 尝试种满的下标，蓝 = 被抬高的前缀 0..p）',
             pointers={'index': 'pink', 'p': 'blue'},
             color=lambda S, k, v: ('blue' if 'p' in S and 'delta' in S and k <= S['p'] else None)),
        dict(type='array', var='need_flowers', h=170, label='need_flowers[k]：把前 k+1 个抬到 sorted_flowers[k] 所需的花'),
    ],
    watch=['newFlowers', 'full_cnt', ('p', 'p', 'blue'), 'delta', ('res', 'res', 'green')],
    captions={
        'sorted_flowers = sorted': '先排序，花少的在前，花多的在后',
        'need_flowers = []': '`need_flowers[k]`：把最小的 `k+1` 个花园都补到 `sorted_flowers[k]` 要的花',
        'full_cnt = 0': '`full_cnt` 记已经 `>= target` 的花园数',
        'for index in range(len(sorted_flowers))': lambda S, B, r: (f"看 `sorted_flowers[{S.index}] = {S.sorted_flowers[S.index]}`" if not ('index' in B and B.index == S.index) else "预处理完毕"),
        'if sorted_flowers[index] >= target': lambda S, B, r: (f"`{S.sorted_flowers[S.index]} >= {S.target}` 成立 → 本来就完善" if S.sorted_flowers[S.index] >= S.target else f"`{S.sorted_flowers[S.index]} >= {S.target}` 不成立 → 不完善的花园，要算需求"),
        'full_cnt += 1': '本来就完善的花园，`full_cnt` → {full_cnt}',
        'elif len(need_flowers) == 0': lambda S, B, r: ("`need_flowers` 还是空 → 这是第一个不完善花园" if len(S.need_flowers) == 0 else f"`need_flowers = {S.need_flowers}` 非空 → 要在前面基础上累加"),
        'need_flowers.append(0)': '最小的园子不用补：`need_flowers = [0]`',
        'need_flowers.append(need_flowers[-1]': '前 `{index}` 个已补到 `{sorted_flowers[index-1]}`，再补到 `{sorted_flowers[index]}`：每个多 `{sorted_flowers[index]-sorted_flowers[index-1]}` 朵 × `{index}` 个 + 之前的 → `{need_flowers[-1]}`',
        'm = len(need_flowers)': '不完善的花园共 `{m}` 个，`need_flowers` 单调不减，可以二分',
        'if m == 0': '`m == 0` 吗？不成立，还有不完善的花园',
        'p = find(m - 1)': '先假设==一个都不种满==：用 `{newFlowers}` 朵花二分找最大的 `p`，使 `need_flowers[p] <= {newFlowers}`，得 `p = {p}`',
        'delta = (newFlowers': '补平到 `sorted_flowers[{p}]` 后剩下的花，平均分给前 `{p+1}` 个：每个再加 `delta = {delta}`',
        'if sorted_flowers[p] + delta >= target': lambda S, B, r: (f"`{S.sorted_flowers[S.p]} + {S.delta} >= {S.target}`？" + ("成立：最小值不能超过 `target-1`" if S.sorted_flowers[S.p] + S.delta >= S.target else "不成立：最小值就是它")),
        'res = full_cnt * full + (target - 1)': '最小值封顶 `target - 1`：`res = {full_cnt}×{full} + {target-1}×{partial}` = =={res}==',
        'res = full_cnt * full + (sorted_flowers[p]': '`res = {full_cnt}×{full} + ({sorted_flowers[p]}+{delta})×{partial}` = =={res}==',
        'for index in range(m - 1, 0, -1)': lambda S, B, r: (f"倒序枚举：尝试把 `sorted_flowers[{S.index}] = {S.sorted_flowers[S.index]}` 也种满（花多的先种满）" if not ('index' in B and B.index == S.index and S.index == 1) else "枚举完了"),
        'if newFlowers < target - sorted_flowers[index]': lambda S, B, r: (f"剩 `{S.newFlowers}` 朵 < 种满需要的 `{S.target} − {S.sorted_flowers[S.index]} = {S.target - S.sorted_flowers[S.index]}`？" + ("成立：种不起，==后面的更种不起，直接返回 res==" if S.newFlowers < S.target - S.sorted_flowers[S.index] else "不成立：种得起")),
        'return res': '`res` = =={res}== 就是最大总美丽值',
        'newFlowers -= (target': '种满它：花从 `newFlowers` 里扣掉 `{target} − {sorted_flowers[index]}` → 剩 `{newFlowers}`',
        'full_cnt += 1\n            p': '完善花园 +1 → `full_cnt = {full_cnt}`',
        'p = find(index - 1)': '剩下的花只能给下标 `0 … {index-1}` 的 `{index}` 个园子：对它们重新二分 `find({index-1})`',
        'res = max(res, full_cnt * full + (target - 1)': '`res = max(..., {full_cnt}×{full} + {target-1}×{partial})` → =={res}==',
        'res = max(res, full_cnt * full + (sorted': '`res = max(旧, {full_cnt}×{full} + ({sorted_flowers[p]}+{delta})×{partial})` → =={res}==',
        'if newFlowers >= target - sorted_flowers[0]': '连最小的园子也种满：只有花够才可能，此时没有不完善花园',
    },
    cards=dict(
        one_liner='花多的先种满，剩下的花补平最矮的那堆；用「补平所需」数组二分',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['花数 `>= target` 的花园叫完善，每个得 `full` 分',
                 '其余花园里「花最少」的数量 × `partial` 也算分；最多再种 `newFlowers` 朵',
                 '本视频：`[1,3,1,1]`，新花 7，target 6，full 12，partial 1 → `14`'],
        quote='一个自然的想法是应该先将当前花较多的花园变为第二部分的花园……先提前预处理出将第三部分花园中最小值变为sorted_flowers[0]、sorted_flowers[1]、...所需要的花的数目。很明显，这个数目是单调不减的，因此……可以在里面二分。',
        quote_src='—— yiduobo 题解原文',
        idea=['花园分三类：本来就完善、补花后完善、最终仍不完善',
              '证明：要种满，选==花多的==更省，所以排序后从后往前枚举种满的个数',
              '`need_flowers` 记「把前 k+1 个补平」的花数，剩余花数二分得 `p`',
              '补平后还有剩，平均分给前 `p+1` 个，上限 `target-1`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（排序 + 预处理数组）',
                 '最小值最多 `target - 1`，否则就成了完善花园',
                 '剩余花不够种满当前园子时可以直接 `return`：花更少的更种不起',
                 '原文为 Python 2 写法，两处整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神用双指针边撤销边维护前缀和，yiduobo 用预处理数组 + 二分'],
    ),
)
