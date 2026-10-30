CONFIG = dict(
    num=2789, title='合并后数组中的最大元素', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='倒序遍历 · now 保存合并结果',
    tags=['灵神题单', '贪心与思维', '难度分 1485'],
    code='''
class Solution(object):
    def maxArrayValue(self, nums):
        now = nums[-1]
        n = len(nums)
        for index in range(n - 2, -1, -1):
            if now >= nums[index]:
                now += nums[index]
            else:
                now = nums[index]

        return now
''',
    call='Solution().maxArrayValue([4,30,3,3,9,2,7])',
    expect=34,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"合并结果 `now = {S['now']}`" + (f"，前一个数 `{S['nums'][S['index']]}`" if 'index' in S else '')) if 'now' in S else ''),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=300),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'green')],
    captions={
        'now = nums[-1]': '倒着合并：`now` 先取最后一个数 `{now}`',
        'n = len': '`n = {n}`',
        'for index in range': '看前一个数 `nums[{index}] = {nums[index]}`',
        'if now >= nums[index]': lambda S, B, r: (f'`now = {S.now} >= {S.nums[S.index]}`：能合并' if S.now >= S.nums[S.index] else f'`now = {S.now} < {S.nums[S.index]}`：合不动了'),
        'now += nums[index]': '合并：`now` → =={now}==，值变大了，往前合并只会更容易',
        'now = nums[index]': '前一个数更大，后面的合并结果不可能是答案 → 从它重新向前合并，`now` = =={now}==',
        'return now': '最大元素 `{now}`',
    },
    cards=dict(
        one_liner='反向合并越合越容易，合不动就从前一个数重来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['若 `nums[i] <= nums[i+1]`，可把 `nums[i+1]` 换成两者之和并删掉 `nums[i]`',
                 '操作任意次，求最终数组中的最大元素',
                 '本视频：`[4,30,3,3,9,2,7]` → `34`'],
        quote='当nums[i + 1]合并了nums[i]后，其再往前合并nums[i - 1]是更容易的，也就是说如果反向合并就能越合并越容易继续合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['正向合并会让数值变大，后面的数更难合并它',
              '反过来：倒序遍历，能合并就尽量合并',
              '合不了时前一个数大于后面的合并结果，后面的结果不可能是答案 → 用变量 `now` 从前一个数继续'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`now >= nums[index]` 才合并，相等也可以',
                 '不需要真的修改数组，`now` 就够了',
                 '原文为 Python 2 风格，只删去了空行里的多余缩进，逻辑未改',
                 '对比灵神：灵神先讲暴力 `O(n^2)` 再优化；yiduobo 直接从合并方向入手'],
    ),
)
