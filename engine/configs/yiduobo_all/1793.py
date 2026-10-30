CONFIG = dict(
    num=1793, title='好子数组的最大分数', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针向两侧扩展 · 先扩较大的一侧',
    tags=['滑动窗口与双指针', '单调栈', '难度分 1946'],
    code='''
class Solution(object):
    def maximumScore(self, nums, k):

        res = mi = nums[k]
        l = k - 1
        r = k + 1
        n = len(nums)
        while l >= 0 and r < n:
            if nums[l] > nums[r]:
                if nums[l] < mi:
                    mi = nums[l]
                res = max(res, mi * (r - l))
                l -= 1
            else:
                if nums[r] < mi:
                    mi = nums[r]
                res = max(res, mi * (r - l))
                r += 1

        while l >= 0:
            if nums[l] < mi:
                mi = nums[l]
            res = max(res, mi * (r - l))
            l -= 1
        
        while r < n:
            if nums[r] < mi:
                mi = nums[r]
            res = max(res, mi * (r - l))
            r += 1
        
        return res
''',
    call='Solution().maximumScore([2,9,7,8,8,1,3], 3)',
    expect=28,
    views=[
        dict(type='text', fn=lambda S: (f"已纳入下标 `{S['l']+1}..{S['r']-1}`：最小值 `{S['mi']}` × 长度 `{S['r']-S['l']-1}`" if 'mi' in S and 'r' in S and 'l' in S else '')),
        dict(type='bars', var='nums', h=420, pointers={'l': 'blue', 'r': 'pink'}, window=('l + 1', 'r - 1'),
             dim=lambda S, i, v: 'r' in S and 'l' in S and not (S['l'] < i < S['r']),
             color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'r' in S and 'l' in S else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mi', 'mi', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = mi = nums[k]': '子数组必须含 `nums[k] = {nums[k]}`：最小值 `mi` 和答案都先取它',
        'l = k - 1': '`l` 是下一个要考察的左侧元素：`k-1 = {l}`',
        'r = k + 1': '`r` 是右侧下一个元素：`k+1 = {r}`',
        'while l >= 0 and r < n': '两边都还有元素：比较 `nums[l]` 与 `nums[r]`，选一侧扩张',
        'if nums[l] > nums[r]': '`nums[l] = {nums[l]}` 对 `nums[r] = {nums[r]}`：{"左边更大，先吞左边（较小的右边留到后面）" if nums[l] > nums[r] else "右边不小于左边，先吞右边"}',
        'if nums[l] < mi': '`nums[l] = {nums[l]}` 对当前最小 `{mi}`：{"更小，要更新 mi" if nums[l] < mi else "不更小，mi 不变，只是变长了"}',
        'if nums[r] < mi': '`nums[r] = {nums[r]}` 对当前最小 `{mi}`：{"更小，要更新 mi" if nums[r] < mi else "不更小，mi 不变，只是变长了"}',
        'res = max(res, mi * (r - l))': '纳入新元素后宽度 `r-l = {r-l}`：`{mi}×{r-l}` = {mi*(r-l)}，`res` = =={res}==',
        'l -= 1': '`l` → {l}',
        'r += 1': '`r` → {r}',
        'while l >= 0:': lambda S, B, r: ('`l >= 0`：左侧还有元素，继续向左吞' if S.l >= 0 else '`l = -1`：左侧吞完了'),
        'while r < n:': lambda S, B, r: (f'`r = {S.r} < n`：右侧还有元素，继续向右吞' if S.r < S.n else '`r = n`：右侧也吞完了'),
        'return res': '最大分数 =={ret}==',
    },
    cards=dict(
        one_liner='两指针从 k 向外扩，哪边的数大就先吞哪边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['分数 = 子数组最小值 × 长度，要求子数组包含下标 `k`',
                 '示例：`[1,4,3,7,4,5], k=3` → `15`；本视频：`[2,9,7,8,8,1,3], k=3` → `28`'],
        quote='若最终答案的右边界为 r，左边界 l\' <= l - 1，那么答案中的最小值 mi 必然小于等于 nums[l - 1]。由于 nums[r + 1] > nums[l - 1]，那么此时将 nums[r + 1] 加入到答案中必然是更优的。',
        quote_src='—— yiduobo 题解原文（反证法）',
        idea=['`l`、`r` 指向两侧下一个待考察元素',
              '两个都不小于 `mi`：扩张不降最小值，只会变长 → 随便扩',
              '两个都比 `mi` 小：先扩较大的那一个，较小的留到最后（反证法）',
              '一侧用完后，另一侧逐个吞完并更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`r - l` 是纳入新元素之后的长度：`l`、`r` 都是尚未纳入的边界',
                 '第一个 `while` 结束后，必有一侧还没扫完，要用另外两个 `while` 收尾',
                 '对比灵神：灵神每次比较 `nums[i-1]` 与 `nums[j+1]`，一个循环搞定'],
    ),
)
