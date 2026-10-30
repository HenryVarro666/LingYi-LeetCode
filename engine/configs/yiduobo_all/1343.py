def _win(S):
    if 'now' not in S:
        return None
    idx = S.get('index')
    if idx is None or 'res' not in S or ('index' in S and S['_line'] in (5, 6, 7, 8)):
        return (0, S['k'] - 1)
    return (idx - S['k'] + 1, idx)


def _ge(S, B, ret):
    t = S.threshold * S.k
    if S.now >= t:
        return f'`now = {S.now} ≥ {t}`：平均值 ≥ {S.threshold}，==这个窗口算一个=='
    return f'`now = {S.now} < {t}`：平均值不到 {S.threshold}，不算'


CONFIG = dict(
    num=1343, title='大小为 K 且平均值大于等于阈值的子数组数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='窗口和比较 K × threshold',
    tags=['灵神核心路线'],  # 标题较长，只保留一个标签以免与右上角徽章重叠
    code='''
class Solution(object):
    def numOfSubarrays(self, arr, k, threshold):

        now = sum(arr[:k])
        res = 0
        if now >= threshold * k:
            res = 1
        
        for index in range(k, len(arr)):
            now = now + arr[index] - arr[index - k]
            if now >= threshold * k:
                res += 1
        
        return res
''',
    call='Solution().numOfSubarrays([11,13,17,23,29,31,7,5,2,3], 3, 5)',
    expect=6,
    views=[
        dict(type='bars', var='arr', label='arr（框 = 当前窗口）', h=430, cell=90,
             pointers={'index': 'blue'},
             window=(lambda S: (_win(S) or (None,))[0], lambda S: (_win(S) or (None, None))[1])),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"窗口和 `now = {S['now']}`，门槛 `threshold × k = {S['threshold']} × {S['k']} = {S['threshold'] * S['k']}`"
                           if 'now' in S else '平均值 ≥ threshold  ⇔  ==子数组和 ≥ K × threshold==')),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = sum(arr[:k])': '窗口初始覆盖 `arr[0..{k - 1}]`：`now = sum({arr[:k]}) = {now}`',
        'res = 0': '先把 `res` 置 0',
        'if now >= threshold * k': _ge,
        'res = 1': '第一个窗口满足 → `res` 初始化为 1',
        'for index in range(k, len(arr))': lambda S, B, r: (f'窗口右移：`arr[{S.index}]` 进来，`arr[{S.index - S.k}]` 出去'
                                                            if 'index' not in B or S.index != B.index else '窗口滑到数组末尾，结束'),
        'now = now + arr[index]': '`now = {B.now} + {arr[index]} − {arr[index - k]} = {now}`',
        'res += 1': '`res` → {res}',
        'return res': '共有 `{res}` 个子数组',
    },
    cards=dict(
        one_liner='平均值的条件转化成窗口和 ≥ K × threshold',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `arr` 中长度为 `k` 且平均值 ≥ `threshold` 的子数组个数',
                 '示例：`arr = [11,13,17,23,29,31,7,5,2,3], k = 3, threshold = 5` → `6`',
                 '前 6 个长度为 3 的子数组平均值都 > 5（平均值不一定是整数）'],
        quote='转化一下，就是要找出长度为K，且子数组的和大于等于K * threshold的子数组的数目。由于这里的子数组长度是固定的，那么可以使用一个大小为K的滑动窗口。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算第一个窗口 `now = sum(arr[:k])`，满足就让 `res = 1`',
              '窗口右移一格：`now` 加上新进来的 `arr[index]`，减去出去的 `arr[index − k]`',
              '一行完成更新，再和 `threshold * k` 比较'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '比较和而不是平均值，避免小数（Python 2 里 `/` 还是整除，更容易错）',
                 '出去的是 `arr[index − k]`，新窗口是 `[index−k+1, index]`',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神一个循环「入-更新-出」，yiduobo 先建初始窗口再滑动'],
    ),
)
