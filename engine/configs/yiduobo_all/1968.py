CONFIG = dict(
    num=1968, title='构造元素不等于两相邻元素平均值的数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='排序后 一小一大交替',
    tags=['贪心与思维', '难度分 1499'],
    code='''
class Solution(object):
    def rearrangeArray(self, nums):

        sorted_nums = sorted(nums)
        res = []
        l = 0
        r = len(nums) - 1
        while l < r:
            res.append(sorted_nums[l])
            res.append(sorted_nums[r])
            l += 1
            r -= 1
            if l == r:
                res.append(sorted_nums[l])
                
        if res == nums:
            res.reverse()
        
        return res
''',
    call='Solution().rearrangeArray([5,1,8,3,9,2,7])',
    expect=[1, 9, 2, 8, 3, 7, 5],
    views=[
        dict(type='array', var='sorted_nums', label='sorted_nums', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), h=260,
             dim=lambda S, i, v: 'l' in S and 'r' in S and not (S['l'] <= i <= S['r'])),
        dict(type='array', var='res', label='res（小、大、小、大 …）', h=200,
             color=lambda S, i, v: ('green' if i % 2 == 0 else 'cyan')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'sorted_nums = sorted': '先排序：`sorted_nums = {sorted_nums}`',
        'res = []': '`res` 用来存构造结果',
        'l = 0': '`l` 指向最小的数',
        'r = len': '`r` 指向最大的数：`r = {r}`',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`：两头还有数 → 继续交替取' if S.l < S.r else f'`l = {S.l}`、`r = {S.r}`：两头取完了 → 结束'),
        'res.append(sorted_nums[l])': lambda S, B, r_: (f'先放小的 `sorted_nums[{S.l}] = {S.sorted_nums[S.l]}`（偶数位，比两侧都小）' if len(S.res) % 2 == 1 and S.l < S.r else f'`l == r`：把落单的 `sorted_nums[{S.l}] = {S.sorted_nums[S.l]}` 补在末尾'),
        'res.append(sorted_nums[r])': '再放大的 `sorted_nums[{r}] = {sorted_nums[r]}`（奇数位，比两侧都大）',
        'l += 1': '`l` → {l}',
        'r -= 1': '`r` → {r}',
        'if l == r': lambda S, B, r_: (f'`l == r == {S.l}`：奇数个数，==剩一个落单的数== → 成立' if S.l == S.r else f'`l = {S.l}`、`r = {S.r}`：没有落单的数，不用处理'),
        'if res == nums': lambda S, B, r_: ('`res` 恰好和原数组一样 → 翻转一下得到另一种合法结果' if S.res == S.nums else '`res` 和原数组 `nums` 不一样，不用翻转'),
        'return res': '一小一大交替排好，返回 `{res}`',
    },
    cards=dict(
        one_liner='排序后，一小一大交替摆放，奇数位全是峰，偶数位全是谷',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把互不相同的整数重排，使每个位置都不等于左右两数的平均值',
                 '返回任意一种合法重排',
                 '本视频：`[5,1,8,3,9,2,7]`'],
        quote='一种最简单的构造思路就是按数值大小，一小一大依次混合排布，合法性也很好证明。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l` 取最小、`r` 取最大，轮流放进 `res`',
              '奇数位 `nums[i]` 比左右都大，偶数位比左右都小',
              '所以它们都不可能是两侧的平均值'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`l == r` 时剩一个数，要单独补进去',
                 '若构造结果恰好等于原数组，原文把结果翻转一下',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（代码无需改动）'],
    ),
)
