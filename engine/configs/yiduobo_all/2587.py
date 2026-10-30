CONFIG = dict(
    num=2587, title='重排数组以得到最大前缀分数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='降序排序 · 累加到非正为止',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1337'],
    code='''
class Solution(object):
    def maxScore(self, nums):

        now = 0
        res = 0
        for v in sorted(nums, reverse=True):
            now += v
            if now > 0:
                res += 1
            else:
                break
        
        return res
''',
    call='Solution().maxScore([2,-1,0,1,-3,3,-3])',
    expect=6,
    views=[
        dict(type='array', var=lambda S: sorted(S['nums'], reverse=True), label='降序后的 nums（绿 = 已算入分数）', h=240,
             pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if 'v' in S and i < S['res'] else None),
        dict(type='text', size=26, fn=lambda S: (f"前缀和 `now = {S['now']}`，分数 `res = {S['res']}`" if 'now' in S else '')),
    ],
    watch=[('v', 'v', 'blue'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now` 是当前前缀和',
        'res = 0': '`res` 是前缀和 `> 0` 的个数',
        'for v in sorted': '降序取下一个数 `v = {v}`：正数在前，负数按从大到小排在后面',
        'now += v': '`now` {B.now} + `{v}` = =={now}==',
        'if now > 0': lambda S, B, r: (f'`now = {S.now} > 0` → 这个前缀算一分' if S.now > 0 else f'`now = {S.now} <= 0`：前缀和已经不正'),
        'res += 1': '`res` = =={res}==',
        'break': '后面都是更小的数，前缀和不会再回到正数 → ==break==',
        'return res': '最大分数 `{res}`',
    },
    cards=dict(
        one_liner='问最长的和大于 0 的前缀有多长',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['任意重排 `nums`，`prefix[i]` 是重排后前 `i+1` 个数之和',
                 '分数 = `prefix` 中正整数的个数，求最大分数',
                 '示例：`[2,-1,0,1,-3,3,-3]` → `6`'],
        quote='所谓的最大前缀分数实际上就是问最长的和大于0的前缀有多长，那么很明显就应该将正数全部放到数组的头部，然后将负数按从大到小的顺序排在正数的后面。',
        quote_src='—— yiduobo 题解原文',
        idea=['把题意翻译成：最长的和 `> 0` 的前缀',
              '正数全放头部，负数按从大到小排在后面 = 降序排序',
              '一趟累加，和变成 `<= 0` 就停，因为之后只会更小'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`now <= 0` 之后直接 break，不要继续数',
                 '易错：`0` 不算正数，`0` 之后的前缀可能还是 0 或负',
                 '对比灵神：灵神用 `accumulate` 一次数完，yiduobo 手写累加并提前 break'],
    ),
)
