def _run(S):
    """当前这段升序子数组的 (起, 止)；取决于正在执行哪一行"""
    nums = S['nums']
    if 'index' not in S:
        return 0, 0
    ln = S['_line']
    i = S['index']
    e = i if ln in (12, 14) else i - 1
    if ln == 10:
        return i, i
    s = e
    while s > 0 and nums[s - 1] < nums[s]:
        s -= 1
    return s, e


def _txt(S):
    if 'now' not in S:
        return '`now` = 当前升序段的和；`res` = 已结束的升序段中的最大和'
    s, e = _run(S)
    seg = '+'.join(str(x) for x in S['nums'][s:e + 1])
    return f"当前升序段 `[{s}..{e}]`：`now = {seg} = {S['now']}`，历史最大 `res = {S['res']}`"


CONFIG = dict(
    num=1800, title='最大升序子数组和', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 累加升序段',
    tags=[],
    code='''
class Solution(object):
    def maxAscendingSum(self, nums):

        now = nums[0]
        res = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index - 1] >= nums[index]:
                res = max(res, now)
                now = nums[index]
            else:
                now += nums[index]
        
        return max(res, now)
''',
    call='Solution().maxAscendingSum([10, 20, 30, 5, 10, 50])',
    expect=65,
    views=[
        dict(type='text', h=70, fn=_txt),
        dict(type='array', var='nums', pointers={'index': 'blue'}, window=(lambda S: _run(S)[0], lambda S: _run(S)[1]), h=300,
             color=lambda S, i, v: ('green' if 'now' in S and _run(S)[0] <= i <= _run(S)[1] else None)),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'green'), ('res', 'res', 'orange')],
    captions={
        'now = nums[0]': '第一个数自己就是一段升序：`now = nums[0] = {now}`',
        'res = 0': '`res` 记录已结束的升序段里的最大和，先设为 0',
        'n = len': '`n = {n}`',
        'for index': lambda S, B, ret: ('所有下标都看完了，循环结束' if B.get('index') == S.index and S.index == len(S.nums) - 1 else f"看 `nums[{S.index}] = {S.nums[S.index]}`，和前一个 `nums[{S.index-1}] = {S.nums[S.index-1]}` 比"),
        'if nums[index - 1] >= nums[index]': lambda S, B, ret: (
            f"`{S.nums[S.index-1]} >= {S.nums[S.index]}` → 不再严格升序，==当前段到此结束==" if S.nums[S.index - 1] >= S.nums[S.index]
            else f"`{S.nums[S.index-1]} < {S.nums[S.index]}` → 仍是升序，接着累加"),
        'res = max': '先用刚结束的段更新答案：`res = max({B.res}, {B.now}) = {res}`',
        'now = nums[index]': '新的一段从 `nums[{index}]` 开始：`now` 重置为 {now}',
        'now += nums[index]': '升序延续：`now += {nums[index]}` → =={now}==',
        'return max(res, now)': '==最后一段没有“下一个更小的数”触发更新==，所以返回 `max({res}, {now}) = {ret}`',
    },
    cards=dict(
        one_liner='遍历一趟：升序就累加，断开就结算并重置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，返回==严格递增连续子数组==的最大元素和',
                 '长度为 1 的子数组也算升序',
                 '示例：`[10,20,30,5,10,50]` → `65`（`5+10+50`）'],
        quote='若其大于nums[index - 1]，那么将其加入到当前子数组和当中，否则使用当前子数组和更新答案，然后将当前子数组和重置为nums[index]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 是当前升序段的和，每个元素只看一次',
              '断开时才用 `now` 去更新 `res`，并从当前数重新开始',
              '遍历完还要再比一次：最后一段没被结算过'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环结束后==必须==再用最后一段更新答案（`max(res, now)`）',
                 '相等也算断开：判断用 `>=`，因为要求严格升序',
                 '同类：最长连续递增序列（674）、最大子数组和'],
    ),
)
