NUMS = [2, 5, 7, 3, 4, 6, 8, 1, 9]


def _f():
    f = [1] * len(NUMS)
    for i in range(1, len(NUMS)):
        if NUMS[i] > NUMS[i - 1]:
            f[i] = f[i - 1] + 1
    return f


F = _f()


def _end(S):
    """当前这段递增序列的末尾下标（已经算出 f 的最后一个位置）"""
    line = S.get('_line')
    if line == 17:
        return len(NUMS) - 1
    if 'num' not in S:
        return 0 if 'now' in S else None
    i = NUMS.index(S['num'])
    if line in (9, 10):
        if S.get('now') == S['num']:  # for 循环结束
            return i
        return i - 1
    return i


def _cnt_now(S):
    e = _end(S)
    return None if e is None else F[e]


def _best(S):
    """到目前为止最长的一段 (l, r)"""
    e = _end(S)
    if e is None:
        return None
    best, bl = 0, None
    for r in range(e + 1):
        if F[r] > best:
            best, bl = F[r], (r - F[r] + 1, r)
    return bl


def _cap_for(S, B, ret):
    if B.get('num') == S.num and 'num' in B:
        return '所有数都看完，循环结束'
    i = NUMS.index(S.num)
    return f'看下一个数 `num = {S.num}`（下标 {i}），上一个数 `now = {S.now}`'


CONFIG = dict(
    num=674, title='最长连续递增序列', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='DP · 滚动变量',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findLengthOfLCIS(self, nums):
        if not nums:
            return 0

        now = nums[0]
        cnt = res = 1

        for num in nums[1:]:
            if num > now:
                cnt += 1
                res = max(res, cnt)
            else:
                cnt = 1
            now = num

        return res
''',
    call=f'Solution().findLengthOfLCIS({NUMS})',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（框 = 以当前数结尾的连续递增段，绿 = 目前最长）', cell=96,
             window=(lambda S: _end(S) - _cnt_now(S) + 1 if _end(S) is not None else None, _end),
             color=lambda S, i, v: 'green' if _best(S) and _best(S)[0] <= i <= _best(S)[1] else None,
             pointers={'nums.index(num) if now != num else None': 'pink',
                       'nums.index(now)': 'blue'},
             pointer_labels={'nums.index(num) if now != num else None': 'num',
                             'nums.index(now)': 'now'}, h=260),
        dict(type='array', var=lambda S: [F[k] if _end(S) is not None and k <= _end(S) else '' for k in range(len(NUMS))],
             label='f[i]：以 nums[i] 结尾的连续递增长度（原文省掉了它，cnt 就是当前的 f[i]）', cell=96,
             color=lambda S, i, v: 'yellow' if i == _end(S) and S.get('_line') in (11, 12, 14, 15) else None, h=170),
        dict(type='text', fn=lambda S: (f"`res` = 目前最长 = =={S['res']}==" if 'res' in S else ''), h=56),
    ],
    watch=[('now', 'now', 'blue'), ('num', 'num', 'pink'), ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if not nums': '数组非空，继续',
        'now = nums[0]': '`now` 记录==上一个数==，先取 `nums[0] = {now}`',
        'cnt = res = 1': '`cnt` = 以当前数结尾的连续递增长度（就是 `f[i]`）；`res` 是答案。都从 1 开始',
        'for num in nums[1:]': _cap_for,
        'if num > now': lambda S, B, r: (f'`{S.num} > {S.now}` → 能接在上一个数后面，递增继续' if S.num > S.now
                                         else f'`{S.num} ≤ {S.now}` → 递增==断了=='),
        'cnt += 1': lambda S, B, r: f'`f[{NUMS.index(S.num)}] = f[{NUMS.index(S.num) - 1}] + 1`：`cnt = {S.cnt}`',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'cnt = 1': lambda S, B, r: f'`f[{NUMS.index(S.num)}] = 1`：从 `{S.num}` ==重新开始==一段',
        'now = num': '`now = {num}`，留给下一个数比较',
        'return res': '最长连续递增序列的长度 = =={ret}==（`3, 4, 6, 8`）',
    },
    cards=dict(
        one_liner='f[i] = 以 nums[i] 结尾的连续递增长度；只依赖上一个数，用一个变量滚动',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定未经排序的整数数组，找到==最长且连续递增==的子序列，返回其长度',
                 '要求严格递增，且必须是==连续==的一段（子数组）',
                 '示例：`[1,3,5,4,7]` → `3`（`[1,3,5]`）；`[2,2,2,2]` → `1`',
                 f'本视频：`{NUMS}` → `4`'],
        quote='f[i]表示以nums[i]结尾的连续递增序列的长度……注意到这里的状态转移==只跟上一个数有关==，因此可以省略掉f数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['若 `nums[i] > nums[i-1]`，则 `f[i] = f[i-1] + 1`',
              '若 `nums[i] <= nums[i-1]`，则 `f[i] = 1`：从当前数重新开始',
              '只用到上一个数：`now` 记上一个数，`cnt` 记 `f[i]`，`res` 取最大'],
        result='`res = 4`：最长的一段是 `[3, 4, 6, 8]`',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '严格递增：相等时也要重置 `cnt = 1`（`[2,2,2]` → 1）',
                 '易错：空数组单独返回 0；`res` 只在 `cnt` 变大时更新即可',
                 '对比 300 题：那里不要求连续，要看前面所有数；这里只看前一个数',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
