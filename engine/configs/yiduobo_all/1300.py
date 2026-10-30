def _text(S):
    if 'mid_v' not in S:
        return '把大于 `value` 的数都改成 `value`：`value` 越大，数组和越大 → 二分 `value`'
    mv, tgt = S['mid_v'], S['target']
    arr = S['arr']
    capped = sum(min(a, mv) for a in arr)
    parts = ' + '.join(str(min(a, mv)) for a in arr)
    return f'`value = {mv}`：变换后 `{parts}` = ==`{capped}`==，目标 `{tgt}`，差 `{abs(capped - tgt)}`'


def _col(S, i, v):
    if 'mid_v' not in S:
        return None
    return 'orange' if v > S['mid_v'] else None


CONFIG = dict(
    num=1300, title='转变数组后最接近目标值的数组和', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 value + 前缀和',
    code='''
class Solution(object):
    def findBestValue(self, arr, target):

        arr = sorted(arr)
        n = len(arr)
        s = [arr[0]]
        for num in arr[1:]:
            s.append(s[-1] + num)
        l_v = 0
        r_v = arr[-1]
        diff = None
        while l_v <= r_v:
            mid_v = (l_v + r_v + 1) >> 1
            if mid_v >= arr[-1]:
                tmp = s[-1]
            elif mid_v <= arr[0]:
                tmp = mid_v * n
            else:
                l_p = 0
                r_p = n - 1
                while l_p < r_p:
                    mid_p = (l_p + r_p + 1) >> 1
                    if arr[mid_p] <= mid_v:
                        l_p = mid_p
                    else:
                        r_p = mid_p - 1
                
                tmp = s[l_p] + mid_v * (n - l_p - 1)

            if diff is None or diff > abs(tmp - target):
                diff = abs(tmp - target)
                res = mid_v
            elif diff == abs(tmp - target) and res > mid_v:
                res = mid_v

            if tmp <= target:
                l_v = mid_v + 1
            else:
                r_v = mid_v - 1
        
        return res
''',
    call='Solution().findBestValue([4, 9, 3], 10)',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='bars', var='arr', color=_col, pointers={'l_p': 'blue', 'r_p': 'pink'}, h=330, label='arr（排序后；橙色 = 大于 value，会被压成 value）'),
        dict(type='array', var='s', label='s（前缀和）', h=170),
    ],
    skip=['s.append', 'l_p = 0', 'r_p = n - 1', 'diff = None'],
    watch=['l_v', 'r_v', 'mid_v', 'tmp', ('diff', 'diff', 'orange'), ('res', 'res', 'green')],
    captions={
        'arr = sorted': '先排序：这样「小于等于 `mid`」的元素就是一段前缀',
        's = [arr[0]]': '`s` 是排序后 `arr` 的前缀和，`s[p]` = 前 `p+1` 个数之和',
        'l_v = 0': '`value` 的下界是 `0`',
        'r_v = arr[-1]': '上界 `r_v = {r_v}` = `max(arr)`：再大的 `value` 不会改变任何数，没有意义',
        'diff = None': '`diff` 记录目前最小的 `|和 − target|`，`res` 记录对应的 `value`',
        'while l_v <= r_v': lambda S, B, r: (f'`value` 的范围 `[{S.l_v}, {S.r_v}]` 里还有候选' if S.l_v <= S.r_v else f'`l_v = {S.l_v} > r_v = {S.r_v}`：二分结束'),
        'mid_v = ': '试 `mid_v = ({l_v} + {r_v} + 1) >> 1 = {mid_v}`（向上取整，避免死循环）',
        'if mid_v >= arr[-1]': '`mid_v = {mid_v}` {">= " if mid_v >= arr[-1] else "< "}最大值 `{arr[-1]}`' + '{" → 没有数会被改变，和就是 s[-1]" if mid_v >= arr[-1] else ""}',
        'tmp = s[-1]': '数组没变，`tmp = s[-1] = {tmp}`',
        'elif mid_v <= arr[0]': '`mid_v = {mid_v}` {"<= " if mid_v <= arr[0] else "> "}最小值 `{arr[0]}`' + '{" → 所有数都被压成 mid_v" if mid_v <= arr[0] else " → 只有一部分数会被压"}',
        'tmp = mid_v * n': '所有数都变成 `{mid_v}`：`tmp = {mid_v} × {n} = {tmp}`',
        'while l_p < r_p': lambda S, B, r: (f'部分被压：二分找最后一个 `<= mid_v` 的位置 `p`，搜索区间 `[{S.l_p}, {S.r_p}]`' if (S.l_p < S.r_p and S.l_p == 0 and S.r_p == S.n - 1) else f'区间收缩为 `[{S.l_p}, {S.r_p}]`' if S.l_p < S.r_p else f'`l_p = r_p = {S.l_p}`：找到位置 `p = {S.l_p}`'),
        'mid_p = ': '`mid_p = {mid_p}`，`arr[{mid_p}] = {arr[mid_p]}`',
        'if arr[mid_p] <= mid_v': '`arr[{mid_p}] = {arr[mid_p]}` {"<= " if arr[mid_p] <= mid_v else "> "}`mid_v = {mid_v}`' + '{" → 这个数保持原样，p 至少是 mid_p" if arr[mid_p] <= mid_v else " → 它要被压，p 在左边"}',
        'l_p = mid_p': '`l_p` → {l_p}',
        'r_p = mid_p - 1': '`r_p` → {r_p}',
        'tmp = s[l_p]': '前缀和 `s[{l_p}] = {s[l_p]}` 加上 `{n - l_p - 1}` 个被压成 `{mid_v}` 的数：`tmp = {tmp}`',
        'if diff is None': '`|tmp − target| = |{tmp} − {target}| = {abs(tmp - target)}`，当前最优 `diff = {B.diff}`' + '{"（还没有）" if B.diff is None else ""}',
        'diff = abs': '更新：`diff = {diff}`',
        32: '对应的 `res = {res}`',
        33: lambda S, B, r: (f'差一样大（都是 {S.diff}）：取更小的 `value`' if S.diff == abs(S.tmp - S.target) else f'`diff = {S.diff}` ≠ `{abs(S.tmp - S.target)}`：这个 `value` 没有更接近，不更新'),
        34: '差一样大且 `{mid_v}` 更小 → `res = {res}`',
        'if tmp <= target': '`tmp = {tmp}` {"<= " if tmp <= target else "> "}`target = {target}`' + '{" → 和偏小，value 要加大" if tmp <= target else " → 和偏大，value 要减小"}',
        'l_v = mid_v + 1': '往大处找：`l_v = {l_v}`',
        'r_v = mid_v - 1': '往小处找：`r_v = {r_v}`',
        'return res': '最接近 `target` 的 `value` 是 `{res}`',
    },
    cards=dict(
        one_liner='和随 value 单调变化：二分 value，前缀和算和',
        complexity='时间 `O(n log max)`，空间 `O(n)`',
        problem=['给整数数组 `arr` 和 `target`，选整数 `value`，把 `arr` 中大于 `value` 的数都改成 `value`',
                 '让改后数组之和最接近 `target`，返回这个 `value`；差一样大时取较小的',
                 '示例：`arr=[4,9,3], target=10` → `3`（改成 `[3,3,3]`，和 9）'],
        quote='随着value的减小，数组之和也会减小，而随着value的增大，数组之和也会增大，因此可以使用二分来寻找最终的value。',
        quote_src='—— yiduobo 题解原文',
        idea=['`value` 越大，改后的和越大（单调），所以二分 `value`，范围 `[0, max(arr)]`',
              '和 = 「小于等于 `mid` 的元素之和」+ `mid × 大于 `mid` 的个数`',
              '先排序、做前缀和 `s`；再二分出 `mid` 在 `arr` 里的位置 `p`，和就是 `s[p] + mid × (n-p-1)`'],
        summary=['时间 `O(n log max)`（外层二分 `log max`，内层二分 `log n`），空间 `O(n)`',
                 '`mid_v = (l + r + 1) >> 1` 向上取整；`diff` 相同要取更小的 `value`',
                 '`mid_v >= arr[-1]` 与 `mid_v <= arr[0]` 要单独处理，避免内层二分越界',
                 '原文为 Python 2 写法，本题除代码无需改动（题解标题里的编号 1330 是笔误）'],
    ),
)
