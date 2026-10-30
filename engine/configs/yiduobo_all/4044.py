def _win(S):
    if 'index' not in S:
        return []
    i, k, n = S['index'], S['k'], S['n']
    ln = S.get('_line', 0)
    if ln == 8:
        return list(range(0, i))
    if ln == 9:
        return list(range(0, i + 1))
    if ln < 15:
        return list(range(0, k))
    if ln == 15:
        a, b = i - k, i - 1
    elif ln == 16:
        a, b = i - k, i
    else:
        a, b = i - k + 1, i
    return [j % n for j in range(a, b + 1)]


def _col(S, j, v):
    return 'cyan' if j in _win(S) else None


def _txt(S):
    w = _win(S)
    if 'total' not in S:
        return '前半和 `>` 后半和 ⇔ 前半和 ×2 `>` 总和'
    if not w:
        return f"总和 `total = {S['total']}`，一半是 `{S['total'] / 2:g}`"
    vals = '+'.join(str(S['nums'][j]) for j in w)
    return f"窗口 `{vals}` = `s = {S['s']}`，`s × 2 = {S['s'] * 2}` vs `total = {S['total']}`"


def _rb(S):
    return S['index'] % S['n'] if 'index' in S and 'n' in S else None


CONFIG = dict(
    num=4044, title='统计好循环移位的数量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一个循环滑窗 · 和与总和一半比较',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1418'],
    code='''
class Solution(object):
    def countGoodRotations(self, nums):

        n = len(nums)
        k = n // 2
        s = 0
        total = sum(nums)
        for index in range(k):
            s += nums[index]

        res = 0
        if s * 2 > total:
            res += 1

        for index in range(k, n + k - 1):
            s += nums[index % n]
            s -= nums[index - k]
            if s * 2 > total:
                res += 1

        return res
''',
    call='Solution().countGoodRotations([1,2,3,4,5,6])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（青 = 长为 n/2 的循环窗口 = 前半部分）', h=250, cell=110,
             pointers={_rb: 'blue'}, pointer_labels={_rb: 'index % n'}, color=_col),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=['n', 'k', ('index', 'index', 'blue'), ('s', 's', 'cyan'), ('total', 'total', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'k = n // 2': '窗口长度 `k = n // 2 = {k}`',
        6: '`s`：窗口（也就是移位后前半部分）的和',
        'total = sum': '`total = {total}`：后半和 = total − s，所以只要比较 `s × 2 > total`',
        'for index in range(k)': lambda S, B, ret: (f'初始化窗口 `0..{S.k - 1}`：加入 `nums[{S.index}]`'
                                                    if 'index' not in B or S.index != B.index else '第一个窗口建好了'),
        's += nums[index]': '`s` → {s}',
        'res = 0': '`res`：好循环移位个数',
        'if s * 2 > total': lambda S, B, ret: (f'`{S.s} × 2 = {S.s * 2} > {S.total}`：前半==严格大于==后半 → 好循环移位' if S.s * 2 > S.total
                                               else f'`{S.s} × 2 = {S.s * 2} ≤ {S.total}`：不是好循环移位'),
        'res += 1': '`res` → {res}',
        'for index in range(k, n + k - 1)': lambda S, B, ret: (f'窗口右移：起点变成 `{S.index - S.k + 1}`'
                                                               if B.get('index') != S.index else '起点 0 到 n−1 都检查完了'),
        's += nums[index % n]': lambda S, B, ret: (f'右边界 `index % n = {S.index % S.n}`' + ('（==超过 n−1，从 0 再来==）' if S.index >= S.n else '')
                                                   + f'：`s += {S.nums[S.index % S.n]}` → `{S.s}`'),
        's -= nums[index - k]': '左边界移出 `nums[{index - k}] = {nums[index - k]}` → `s = {s}`',
        'return res': '好循环移位共 =={res}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='前半和大于后半和 ⇔ 前半和超过总和的一半',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长度数组 `nums`，把一个前缀移到末尾得到循环移位',
                 '若前 `n/2` 个元素之和==严格大于==后 `n/2` 个之和，就是好循环移位，求个数',
                 '示例：`[1,2,3,4,5,6]` → `3`'],
        quote='题目实际上问的是对于起点从0到n - 1，且长度为n // 2的循环子数组中元素之和，==是否大于数组总和的一半==。',
        quote_src='—— yiduobo 题解原文',
        idea=['后半和 = 总和 − 前半和，比较 `s × 2 > total` 即可',
              '只需一个长 `n // 2` 的窗口，起点从 0 滑到 n−1',
              '窗口是循环的：右边界超出 n−1 后对 n 取模'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用 `s * 2 > total` 避免除法和浮点数',
                 '第二个循环到 `n + k − 2`：起点 1 到 n−1，加上初始窗口共 n 个',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神同时维护前后两个窗口 `sum1`、`sum2`'],
    ),
)
