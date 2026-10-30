CONFIG = dict(
    num=1846, title='减小和重新排列数组后的最大元素', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 维护 last',
    tags=['灵神题单', '贪心与思维', '难度分 1454'],
    code='''
class Solution(object):
    def maximumElementAfterDecrementingAndRearranging(self, arr):
        sorted_arr = sorted(arr)
        last = 1
        for num in sorted_arr[1:]:
            if num - last > 1:
                last += 1
            else:
                last = num

        return last
''',
    call='Solution().maximumElementAfterDecrementingAndRearranging([100,1,1000,2,2,7])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"`last = {S['last']}`：已处理的最后一个数；当前 `num = {S['num']}`" if 'num' in S else '先排序，第一个数变成 1'),
        dict(type='array', var='sorted_arr', pointers={}, h=300, label='sorted_arr（排序后）',
             color=lambda S, i, v: 'green' if 'last' in S and v == S['last'] else None),
    ],
    watch=[('last', 'last', 'green'), 'num'],
    captions={
        'sorted_arr = sorted': '先排序：不得不减一时，==先减较小的数==才能保住较大的。`{sorted_arr}`',
        'last = 1': '答案第一个数必须是 1，最小数一定能减到 1 → `last = 1`',
        'for num in': '取下一个数 `num = {num}`',
        'if num - last > 1': '`num - last = {num} - {last} = {num-last}`，{"大于 1 → 必须缩减" if num-last>1 else "不超过 1 → 可以保持"}',
        'last += 1': '`num` 缩减成 `last + 1`，`last` → ==`{last}`==',
        'last = num': '`num` 不用动，`last` 更新为 ==`{last}`==',
        'return last': '最后一次更新后的 `last` 就是最大值：返回 `{last}`',
    },
    cards=dict(
        one_liner='先减小的数要小，排序后一个个往上接',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['正整数数组 `arr`，可以减小任意元素、重排',
                 '最终第一个数为 1，相邻差的绝对值 `<= 1`，求最大元素',
                 '本视频：`[100,1,1000,2,2,7]` → `5`'],
        quote='为了使得答案最大，在不得已执行减一操作的时候就应该先对较小的数执行减一操作，这样才可能保住较大的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后 `arr[0]` 减成 1，`last` 记录已处理的最后一个数',
              '`num > last + 1` 就必须缩减成 `last + 1`，否则保持不变',
              '处理完后的 `last` 就是答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（排序了副本）',
                 '易错：循环从 `sorted_arr[1:]` 开始，`last` 初值就是 1',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神原地改数组并给出交换论证；这里用变量 last 表达同一个递推'],
    ),
)
