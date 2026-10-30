CONFIG = dict(
    num=1968, title='构造元素不等于两相邻元素平均值的数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序后一小一大交错',
    tags=['灵神题单·数学算法', '难度分 1499'],
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
    call='Solution().rearrangeArray([1,5,2,4,3])',
    expect=[3, 4, 2, 5, 1],
    views=[
        dict(type='array', var='sorted_nums', label='sorted_nums（蓝 = l 取最小，粉 = r 取最大）', h=190, cell=90,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'),
             dim=lambda S, i, v: 'l' in S and 'r' in S and not (S['l'] <= i <= S['r'])),
        dict(type='array', var='res', label='res（一小一大交错）', h=170, cell=90,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'sorted_nums = sorted': '先排序：小的在左、大的在右 `{sorted_nums}`',
        'res = []': '`res` 用来存交错排布的结果',
        'l = 0': '`l` 指向最小的',
        'r = len': '`r` 指向最大的 `r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}` → 还有一对小大可取' if S.l < S.r else f'`l = {S.l}` 不再小于 `r = {S.r}`，取完了'),
        9: '先放最小的 `{sorted_nums[l]}`：它排在==偶数位==，比两边邻居都小',
        'res.append(sorted_nums[r])': '再放最大的 `{sorted_nums[r]}`：它排在==奇数位==，比两边邻居都大',
        'l += 1': '`l` 右移 → {l}',
        'r -= 1': '`r` 左移 → {r}',
        'if l == r': lambda S, B, r: (f'`l = r = {S.l}`：剩一个数（奇数长度）→ 接在末尾' if S.l == S.r else '两指针没有重合，不用补'),
        14: '补上中间剩下的 `{sorted_nums[l]}`',
        'if res == nums': lambda S, B, r: ('构造结果和原数组一样 → 题目要“重排”，翻转一下得到另一个合法答案' if S.res == S.nums else '和原数组不同，直接返回'),
        'res.reverse()': '翻转后仍是一小一大交替，依然合法：`{res}`',
        'return res': '返回 `{ret}`：每个“大”夹在两个“小”之间，必然不是平均值',
    },
    cards=dict(
        one_liner='排序后一小一大交错放，大的总比两边大，小的总比两边小',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组里的数互不相同，重排使每个元素都不等于左右两邻居的平均值',
                 '返回任意一种合法重排',
                 '本视频：`[1,5,2,4,3]` → `[3,4,2,5,1]`'],
        quote='一种最简单的构造思路就是按数值大小，一小一大依次混合排布，合法性也很好证明。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数位的数比左右两个邻居都大，所以不可能等于它们的平均值',
              '偶数位的数比左右两个邻居都小，同理',
              '用双指针从排好序的两端取：左边取小、右边取大，交替放进 `res`',
              '特殊情况：构造结果恰好和原数组一样，翻转一下就行'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：长度为奇数时 `l == r` 剩一个数，要补在末尾',
                 '易错点：构造结果与原数组相同时翻转，翻转后仍然合法',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（没有 Python 2 专有语法需要修改）'],
    ),
)
