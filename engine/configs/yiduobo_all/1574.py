def _txt(S):
    if 'res' not in S:
        return '先找第一处逆序和最后一处逆序'
    if 'i' in S and 'j' in S:
        return f"保留 `arr[0..{S['i']}]` 和 `arr[{S['j']}..]`，共 {S['i'] + 1 + len(S['arr']) - S['j']} 个；==res 目前最多保留 {S['res']}== 个"
    return f"保底：只保留一侧，==res = {S['res']}== 个"


def _col(S, k, v):
    if 'i' in S and 'j' in S:
        return 'cyan' if k == S['i'] else 'orange' if k == S['j'] else None
    return None


CONFIG = dict(
    num=1574, title='删除最短的子数组使剩余数组有序', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='找两处逆序 + 双路归并式双指针',
    tags=['滑动窗口与双指针', '难度分 1932'],
    code='''
class Solution(object):
    def findLengthOfShortestSubarray(self, arr):

        l = 1
        n = len(arr)
        while l < n and arr[l] >= arr[l - 1]:
            l += 1
        
        if l == n:
            return 0
        
        l -= 1

        r = n - 2
        while r >= 0 and arr[r] <= arr[r + 1]:
            r -= 1

        r += 1

        res = max(l + 1, n - r)

        i = 0
        j = r
        while i <= l and j < n:
            if arr[i] <= arr[j]:
                res = max(res, i + 1 + n - j)
                i += 1
            else:
                j += 1
        
        return n - res
''',
    call='Solution().findLengthOfShortestSubarray([1,3,5,4,2,2,6,7])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='arr', pointers={'l': 'blue', 'r': 'pink', 'i': 'cyan', 'j': 'orange'}, h=330,
             color=lambda S, k, v: (_col(S, k, v) if 'i' in S and 'j' in S else ('blue' if 'l' in S and k == S['l'] and 'r' not in S else 'pink' if 'r' in S and k == S['r'] else None))),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('i', 'i', 'cyan'), ('j', 'j', 'orange'), ('res', 'res', 'green')],
    captions={
        'l = 1': '从头向后扫，找第一处逆序：`l` 从 1 开始',
        'while l < n and': lambda S, B, ret: ((f'`arr[{S.l}] = {S.arr[S.l]}` >= `arr[{S.l - 1}] = {S.arr[S.l - 1]}`：还是不减 → `l` 后移' if (S.l < len(S.arr) and S.arr[S.l] >= S.arr[S.l - 1]) else (f'`arr[{S.l}] = {S.arr[S.l]}` < `arr[{S.l - 1}] = {S.arr[S.l - 1]}`：出现逆序，停' if S.l < len(S.arr) else '`l` 走到末尾：整个数组都不减'))),
        'if l == n': lambda S, B, ret: ('`l == n`：本来就不减，不用删，答案 0' if S.l == len(S.arr) else '`l < n`：数组里有逆序，必须删'),
        'l -= 1': '`l` 退回逆序前的最后一个位置：`arr[0..{l}]` 是不减的前缀',
        'r = n - 2': '再从后向前扫，找最后一处逆序',
        'while r >= 0 and': lambda S, B, ret: ((f'`arr[{S.r}] = {S.arr[S.r]}` <= `arr[{S.r + 1}] = {S.arr[S.r + 1]}`：还是不减 → `r` 前移' if (S.r >= 0 and S.arr[S.r] <= S.arr[S.r + 1]) else (f'`arr[{S.r}] = {S.arr[S.r]}` > `arr[{S.r + 1}] = {S.arr[S.r + 1]}`：出现逆序，停' if S.r >= 0 else '`r` 走出左端'))),
        'r += 1': '`r` 回到逆序后的第一个位置：`arr[{r}..]` 是不减的后缀',
        'res = max(l + 1': '最差也能只留一侧：前缀 `{l + 1}` 个或后缀 `{n - r}` 个 → `res = {res}`（`res` 是保留的个数）',
        'i = 0': '`i` 扫前缀',
        'j = r': '`j` 扫后缀，从 `r` 开始',
        'while i <= l and j': lambda S, B, ret: (f'`i = {S.i}`，`j = {S.j}`：前缀和后缀各走一路，像归并' if (S.i <= S.l and S.j < len(S.arr)) else (f'`i = {S.i}` > `l = {S.l}`：前缀用完了 → 结束' if S.i > S.l else '`j` 走到末尾 → 结束')),
        'if arr[i] <= arr[j]': lambda S, B, ret: (f'`arr[i] = {S.arr[S.i]}` <= `arr[j] = {S.arr[S.j]}`：能拼起来，保留 `0..i` 和 `j..` 两段' if S.arr[S.i] <= S.arr[S.j] else f'`arr[i] = {S.arr[S.i]}` > `arr[j] = {S.arr[S.j]}`：后缀这个数太小 → `j` 右移'),
        'res = max(res, i + 1': '保留 `{i} + 1 + {n} - {j}` = {i + 1 + n - j} 个 → `res = {res}`',
        'i += 1': '前缀多留一个，`j` 不用回头：`i` → {i}',
        'j += 1': '`j` → {j}：这一个要删掉',
        'return n - res': '保留最多 `{res}` 个，删 `{n} - {res}` = =={n - res}== 个',
    },
    cards=dict(
        one_liner='先量出不减的前缀和后缀，再用归并的方式拼最长保留数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除一个子数组（可为空），使剩下的元素不减',
                 '求最短删多长',
                 '本视频：`[1,3,5,4,2,2,6,7]` → `3`'],
        quote='一旦出现了两处逆序对，那么最初的逆序对以及最后的逆序对之间的部分都必须全部删去。……这实际上就是一个二路归并的场景。',
        quote_src='—— yiduobo 题解原文',
        idea=['换个角度：要删得最短，就是==保留得最多==，用 `res` 记保留个数',
              '前扫得到最长不减前缀 `[0..l]`，后扫得到最长不减后缀 `[r..n-1]`',
              '两段拼接要求 `arr[i] <= arr[j]`：像归并一样，`i`、`j` 都只往右走'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`l` 扫完要 `l -= 1`、`r` 扫完要 `r += 1`，才是前缀/后缀的边界',
                 '兜底 `max(l + 1, n - r)` 对应只留一侧',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，已原样使用',
                 '对比灵神：灵神直接算删除区间长度并枚举 `right`；yiduobo 转成「保留最多」再归并'],
    ),
)
