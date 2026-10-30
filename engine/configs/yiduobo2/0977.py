def _used(S, k):
    # nums[l..r] 还没扫描，两侧已经加入 res
    return 'l' in S and 'r' in S and (k < S['l'] or k > S['r'])


def _squares(S):
    return [v * v for v in S['nums']]


def _par(v):
    return f'({v})' if v < 0 else str(v)


def _text(S):
    if 'r' not in S:
        return '|nums| 先==单调递减==再==单调递增== → 平方最大的数必在头部或尾部'
    l, r = S['l'], S['r']
    if S.get('_line') == 14:
        return f'res 从大到小 `{S["res"]}` → 倒转 `res[::-1]` = =={S["res"][::-1]}=='
    if l > r:
        return '`l > r`：扫描结束，res 里是==从大到小==的平方'
    return f'未扫描 `nums[{l}..{r}]`：其中平方最大的数==必然在头部或尾部=='


def _while(S, B, ret):
    l, r = S['l'], S['r']
    if l <= r:
        return f'`l = {l} ≤ r = {r}`：还有 {r - l + 1} 个数没扫描，继续'
    return f'`l = {l} > r = {r}`：所有数都扫描完了 → 结束循环'


def _if(S, B, ret):
    l, r, nums = S['l'], S['r'], S['nums']
    a, b = nums[l] ** 2, nums[r] ** 2
    head = f'`{_par(nums[l])}² = {a}` vs `{_par(nums[r])}² = {b}`'
    if l == r:
        return f'`l = r = {l}`，只剩一个数，比较结果不重要 → 走 else'
    if a > b:
        return f'{head}：==头部更大== → 加入 `nums[{l}]` 的平方'
    if a == b:
        return f'{head}：相等，走 else 加入尾部的'
    return f'{head}：==尾部更大== → 走 else'


CONFIG = dict(
    num=977, title='有序数组的平方', difficulty='Easy', category='双指针',
    author='yiduobo', technique='两端扫描 + 最后倒转',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def sortedSquares(self, nums):
        l = 0
        r = len(nums) - 1
        res = []
        while l <= r:
            if nums[l] ** 2 > nums[r] ** 2:
                res.append(nums[l] ** 2)
                l += 1
            else:
                res.append(nums[r] ** 2)
                r -= 1

        return res[::-1]
''',
    call='Solution().sortedSquares([-7, -3, 2, 3, 11])',
    expect=[4, 9, 9, 49, 121],
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（框 = 未扫描的 nums[l..r]，暗 = 已加入 res）', cell=96,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), dim=_used, h=210),
        dict(type='array', var=_squares, label='平方（辅助观察，青 = 两端正在比较）', cell=96, dim=_used,
             color=lambda S, k, v: 'cyan' if 'r' in S and S['l'] <= S['r'] and k in (S['l'], S['r']) else None,
             h=170),
        dict(type='array', var='res', label='res（从大到小依次追加）', cell=96,
             color=lambda S, k, v: 'green' if k == len(S['res']) - 1 and S.get('_line') in (8, 11) else None,
             h=190),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('len(res)', 'len(res)', 'green')],
    captions={
        'l = 0': '左指针 `l` 从==头部==开始',
        'r = len(nums) - 1': '右指针 `r = {r}` 从==尾部==开始，两个指针向中间扫描',
        'res = []': '`res` 用来按==从大到小==的顺序收集平方',
        'while l <= r': _while,
        'if nums[l] ** 2': _if,
        'res.append(nums[l]': '`res` 追加 `{res[-1]}`：它是剩下数里==最大的平方==',
        'l += 1': '`nums[{l - 1}]` 处理完了，`l` 向后移一位 → {l}',
        'res.append(nums[r]': '`res` 追加 `{res[-1]}`：它是剩下数里==最大的平方==',
        'r -= 1': '`nums[{r + 1}]` 处理完了，`r` 向前移一位 → {r}',
        'return res[::-1]': 'res 是从大到小的，==倒转==后就是答案 → {ret}',
    },
    cards=dict(
        one_liner='平方最大的数只在两端：从两端向中间扫，收集完再倒转',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`nums` 按==非递减==顺序排列（可能有负数）',
                 '返回每个数的平方组成的新数组，也要==非递减==',
                 '示例：`[-4,-1,0,3,10]` → `[0,1,9,16,100]`',
                 '本视频：`[-7,-3,2,3,11]` → `[4,9,9,49,121]`'],
        quote='对于一个数而言，其绝对值越大平方就越大。在这里，nums是呈现出一个==绝对值单调递减然后再单调递增==的过程，因此当前nums中平方最大的数==必然出现在头部或者尾部==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l`、`r` 从两端向中间扫描，比较 `nums[l]²` 和 `nums[r]²`',
              '更大的那个加入答案，对应指针往里走一步',
              '`l > r` 时结束：res 是==从大到小==的平方，倒转后返回'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '循环条件是 `l <= r`：`l == r` 时还剩最后一个数要加入',
                 '易错：res 是从大到小收集的，别忘了 `res[::-1]`',
                 '对比灵神：预开长 n 的数组，从右往左填，省掉倒转',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
