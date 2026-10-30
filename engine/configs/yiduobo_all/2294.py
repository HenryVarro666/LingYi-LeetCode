def _col(S, i, v):
    if 'l' not in S or 'r' not in S:
        return None
    if i == S['l']:
        return 'blue'
    if i == S['r']:
        return 'pink'
    return None


def _txt(S):
    if 'l' not in S:
        return '排序后，从最小值出发，向右吞下所有 `<= 最小值 + k` 的数'
    a = S['sorted_nums']
    if S['l'] >= len(a):
        return f"全部划分完，共 ==`{S['res']}`== 组"
    return f"当前组从 `l = {S['l']}`（最小值 {a[S['l']]}）出发，上限 `{a[S['l']]} + k = {a[S['l']] + S['k']}`"


def _grow(S, B, ret):
    a, l, r, k = S.sorted_nums, S.l, S.r, S.k
    if r + 1 < len(a) and a[r + 1] - a[l] <= k:
        return f"`{a[r + 1]} - {a[l]} = {a[r + 1] - a[l]} <= {k}` → `a[{r + 1}]` 还能进这一组"
    if r + 1 >= len(a):
        return '`r + 1` 已越界 → 右边没有数了，这一组到此为止'
    return f"`{a[r + 1]} - {a[l]} = {a[r + 1] - a[l]} > {k}` → 再加就超了，这一组到此为止"


CONFIG = dict(
    num=2294, title='划分数组使最大差为 K', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 双指针划分',
    tags=['贪心算法', '划分型贪心', '难度分 1416'],
    code='''
class Solution(object):
    def partitionArray(self, nums, k):

        sorted_nums = sorted(nums)
        l = 0
        r = 0
        res = 0
        while l < len(sorted_nums):
            while r + 1 < len(sorted_nums) and sorted_nums[r + 1] - sorted_nums[l] <= k:
                r += 1
            
            res += 1
            l = r + 1
            r = l
        
        return res
''',
    call='Solution().partitionArray([3,6,1,2,5,9], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='sorted_nums', label='sorted_nums（蓝 = l 最小值，粉 = r 本组最大值）', cell=90,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), color=_col, h=320),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('k', 'k'), ('res', 'res', 'green')],
    captions={
        'sorted_nums = sorted': '先排序：以后每一组都是排序数组里连续的一段',
        'l = 0': '`l` 指向当前剩余数中的==最小值==',
        'r = 0': '`r` 指向本组能取到的最大下标',
        'res = 0': '`res` 统计组数',
        'while l < len': lambda S, B, ret: (f'`l = {S.l} < {len(S.sorted_nums)}`，还有数没分组' if S.l < len(S.sorted_nums)
                                            else f'`l = {S.l}` 越界，所有数都分完了'),
        'while r + 1 <': _grow,
        'r += 1': '`r` → {r}：把 `{sorted_nums[r]}` 并入本组',
        'res += 1': '本组确定为 `[{l}, {r}]`，`res` → =={res}==',
        'l = r + 1': '下一组从 `r + 1` 开始：`l` → {l}',
        'r = l': '`r` 先和 `l` 对齐，再重新向右扩',
        'return res': '一共 =={res}== 组',
    },
    cards=dict(
        one_liner='每次拿剩余的最小值，把不超过它加 k 的数全划进同一组',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组划分成若干子序列，各子序列最大最小值之差 `<= k`，求最少子序列数',
                 '示例：`[3,6,1,2,5], k=2` → `2`',
                 '本视频：`[3,6,1,2,5,9], k=2` → `3`'],
        quote='对于数组中的最小值nums[p]，其所在的子序列中所有的数都是大于等于nums[p]的，同时这些数都必须小于等于nums[p] + k。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小值所在的组：吃掉所有 `<= 最小值 + k` 的数',
              '剩下的数再取最小值，重复以上过程',
              '排序后用 `l`、`r` 两个指针圈出每一组，`l` 跳到 `r + 1`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新数组）',
                 '外层 `l = r + 1` 之后要把 `r` 重置成 `l`',
                 '内层循环要先判断 `r + 1 < len` 防止越界',
                 '对比灵神：灵神只维护 `mn` 一次遍历，yiduobo 显式圈出每一组的区间',
                 '原文本身是 Python 3 可运行的写法，未改动'],
    ),
)
