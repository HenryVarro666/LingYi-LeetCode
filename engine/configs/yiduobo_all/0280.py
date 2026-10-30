def _cmp(S, B, ret):
    i = S.index
    a, b = S.nums[i - 1], S.nums[i]
    return f'`nums[{i}] = {b}`，`nums[{i-1}] = {a}`：`{b} < {a}` → {"成立：前面反而更大，要交换" if b < a else "不成立：已满足前小后大，不动"}'


def _cmp2(S, B, ret):
    i = S.index
    a, b = S.nums[i - 1], S.nums[i]
    return f'`nums[{i}] = {b}`，`nums[{i-1}] = {a}`：`{b} > {a}` → {"成立：前面反而更小，要交换" if b > a else "不成立：已满足前大后小，不动"}'


CONFIG = dict(
    num=280, title='摆动排序', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 相邻交换',
    tags=['贪心', '数组'],
    code='''
class Solution(object):
    def wiggleSort(self, nums):

        flag = True
        for index in range(1, len(nums)):
            if flag:
                if nums[index] < nums[index - 1]:
                    nums[index], nums[index - 1] = nums[index - 1], nums[index]
            else:
                if nums[index] > nums[index - 1]:
                    nums[index], nums[index - 1] = nums[index - 1], nums[index]
            
            flag = not flag
''',
    call='nums = [3, 5, 2, 1, 6, 4]\nSolution().wiggleSort(nums)\nnums',
    expect=[3, 5, 1, 6, 2, 4],
    views=[
        dict(type='text', fn=lambda S: ('目标：`nums[0] <= nums[1] >= nums[2] <= nums[3] >= ...`，已经摆好的前缀不再改动' if 'index' not in S else
                                        f"当前检查 `nums[{S['index']-1}]` 与 `nums[{S['index']}]`，flag = =={S['flag']}==（True 要求前小后大）")),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=300,
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('flag', 'flag', 'yellow')],
    captions={
        'flag = True': '`flag = True`：表示==当前这一对要前小后大==（下标 0 要小于下标 1）',
        'for index': '`index = {index}`：检查 `nums[{index-1}]` 和 `nums[{index}]` 这一对',
        'if flag:': lambda S, B, r: f'`flag = {S.flag}`：' + ('这一对要求 ==前小后大==' if S.flag else '这一对要求 ==前大后小==，走 else'),
        'if nums[index] < nums[index - 1]': _cmp,
        'if nums[index] > nums[index - 1]': _cmp2,
        'nums[index], nums[index - 1] =': '顺序反了 → 交换这一对：`{nums}`。交换不会破坏前一对，因为 ==新的 nums[index-1] 比旧的更小（或更大）==，前一对的大小关系保持',
        'flag = not flag': '下一对的要求相反：`flag = {flag}`',
    },
    cards=dict(
        one_liner='一趟遍历，看一对、修一对：错了就交换，前面不会被破坏',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['原地重排 `nums`，使 `nums[0] <= nums[1] >= nums[2] <= nums[3] ...`',
                 '示例：`[3,5,2,1,6,4]` → `[3,5,1,6,2,4]`（答案不唯一）'],
        quote='当前的nums[index]以及nums[index - 1]，如果这二者不符合题目的要求，那么将二者交换位置就能符合题目要求了',
        quote_src='—— yiduobo 题解原文',
        idea=['最直观：排序后把大的一半放奇数位、小的一半放偶数位',
              '更好：==交换后 nums[index-1] 只会往“更利于前一对”的方向变==，前面不用回头检查',
              '用 `flag` 记录当前这一对该前小后大还是前大后小，每轮取反'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`flag` 每轮都要取反，不管有没有发生交换',
                 '相等时不交换（`<` / `>` 都是严格比较），仍满足 `<=` / `>=`',
                 '原文为 Python 2 风格，该代码在 Python 3 下无需修改'],
    ),
)
