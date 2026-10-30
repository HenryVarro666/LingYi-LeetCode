def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1) + (1 if S.get('_line') == 13 else 0)  # 出窗口后左端点右移


def _txt(S):
    if 'i' not in S:
        return '平均值 ≥ threshold  ⇔  ==窗口和 ≥ k × threshold==（k 固定）'
    l = max(0, S['i'] - S['k'] + 1)
    return f"窗口和 `s = {S['s']}`，目标 `k × threshold = {S['k']} × {S['threshold']} = {S['k'] * S['threshold']}`"


def _ge(S, B, ret):
    t = S.k * S.threshold
    w = S.arr[S.i - S.k + 1:S.i + 1]
    if S.s >= t:
        return f'窗口 `{w}` 和 `{S.s} ≥ {t}` → 平均值 ≥ {S.threshold}，==符合要求=='
    return f'窗口 `{w}` 和 `{S.s} < {t}` → 平均值不够，不计数'


CONFIG = dict(
    num=1343, title='大小为 K 且平均值大于等于阈值的子数组数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 入-更新-出',
    tags=['灵神核心路线'],  # 标题较长，只保留一个标签以免与右上角徽章重叠
    code='''
class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        ans = s = 0  # 维护窗口元素和
        for i, x in enumerate(arr):
            # 1. 进入窗口
            s += x
            if i < k - 1:  # 窗口大小不足 k
                continue
            # 2. 更新答案
            if s >= k * threshold:
                ans += 1
            # 3. 离开窗口
            s -= arr[i - k + 1]
        return ans
''',
    call='Solution().numOfSubarrays([2,2,2,2,5,5,5,8], 3, 4)',
    expect=3,
    views=[
        dict(type='bars', var='arr', label='arr（框 = 以 i 为右端点、长为 k 的窗口）', h=430, cell=96,
             pointers={'i': 'blue'}, window=(_wl, 'i'),
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('s', 's', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = 0': '`s` 维护窗口元素和，`ans` 计数',
        'for i, x in enumerate(arr)': lambda S, B, r: (f'右端点 `i = {S.i}`，`x = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        's += x': '==入==：`arr[{i}] = {x}` 进入窗口，`s = {B.s} + {x} = {s}`',
        'if i < k - 1': lambda S, B, r: (f'`i = {S.i} < k − 1 = {S.k - 1}`：窗口还不满 {S.k} 个' if S.i < S.k - 1
                                         else f'`i = {S.i} ≥ k − 1`：窗口满 {S.k} 个了'),
        'continue': '先不更新答案，继续入窗口',
        'if s >= k * threshold': _ge,
        'ans += 1': '==更新==：`ans` → {ans}',
        's -= arr[i - k + 1]': '==出==：左端点 `arr[{i - k + 1}] = {arr[i - k + 1]}` 离开，`s = {s}`',
        'return ans': '共 `{ans}` 个子数组满足要求',
    },
    cards=dict(
        one_liner='平均值 ≥ 阈值，等价于窗口和 ≥ k × 阈值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `arr` 中长度为 `k` 且==平均值 ≥ threshold== 的子数组个数',
                 '示例：`arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4` → `3`',
                 '满足的是 `[2,5,5]`、`[5,5,5]`、`[5,5,8]`'],
        quote='本题由于窗口长度固定为 k，所以平均值 ≥ threshold 相当于窗口元素和 ≥ k·threshold。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三步套路：==入==（s 加 arr[i]）→ ==更新==（判断并计数）→ ==出==（s 减 arr[i−k+1]）',
              '`i < k − 1` 时窗口不满，只入不更新',
              '比较和而不是平均值：==避免除法和浮点误差=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '平均值不是整数：用 `s >= k * threshold` 比较，不要写 `s // k >= threshold`',
                 '离开窗口的是 `arr[i − k + 1]`，即当前窗口的左端点',
                 '同一套模板：1456、2090、2379、2461'],
    ),
)
