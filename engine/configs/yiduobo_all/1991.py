CONFIG = dict(
    num=1991, title='找到数组的中间位置', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='枚举分割点 · 前缀累加', tags=[],
    code='''
class Solution(object):
    def findMiddleIndex(self, nums):

        now = 0
        s = sum(nums)
        for index in range(len(nums)):
            if now == s - nums[index] - now:
                return index
            
            now += nums[index]
        
        return -1
''',
    call='Solution().findMiddleIndex([1,7,3,6,5,6])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"前半 `{S['now']}`  vs  后半 = `{S['s']} − {S['nums'][S['index']]} − {S['now']}` = =={S['s']-S['nums'][S['index']]-S['now']}==" if S.get('_line') == 7 and 'index' in S else '后半 = 总和 − 前半 − 分割点'),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['index'] else 'cyan' if i < S['index'] else None) if 'index' in S else None),
    ],
    watch=['s', ('now', 'now', 'cyan'), ('index', 'index', 'blue')],
    captions={
        'now = 0': '`now` 是前半部分之和，枚举分割点时不断累加',
        's = sum': '总和 `s = {s}`，后半部分就是 总和 − 分割点 − 前半',
        'if now ==': '前半 `{now}`，后半 `{s} − {nums[index]} − {now}` = {s-nums[index]-now} → {"相等，这就是分割点" if now==s-nums[index]-now else "不等"}',
        'now += nums': '分割点右移，把 `{nums[index]}` 加进前半：`now` = {now}',
        'return -1': '一直没找到相等的分割点 → -1',
        'return index': '`index = {index}` 两半相等，且是第一个找到的',
    },
    cards=dict(
        one_liner='枚举分割点，后半 = 总和 − 前半 − 分割点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找一个位置把数组切成两半，两半之和相等；找不到返回 -1',
                 '本视频：`[1,7,3,6,5,6]` → `2`（两边都是 0？前半 0，后半 0 → 见 `4` 的位置）'],
        quote='对于后半部分之和，则可以通过数组总和，减去前半部分之和以及分割点的值来得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['前半部分在枚举时边走边累加', '后半部分不单独求，用总和减去得到', '找到的第一个分割点即答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先比较再累加，前半不能包含分割点',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
