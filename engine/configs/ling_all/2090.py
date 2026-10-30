def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - 2 * S['k']) + (1 if S.get('_line') == 13 else 0)  # 出窗口后左端点右移


def _ctr(S):
    i = S.get('i')
    if i is None or i < 2 * S['k']:
        return None
    return i - S['k']


CONFIG = dict(
    num=2090, title='半径为 k 的子数组平均值', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='长为 2k+1 的定长滑窗',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1358'],
    code='''
class Solution:
    def getAverages(self, nums: List[int], k: int) -> List[int]:
        avgs = [-1] * len(nums)
        s = 0  # 维护窗口元素和
        for i, x in enumerate(nums):
            # 1. 进入窗口
            s += x
            if i < k * 2:  # 窗口大小不足 2k+1
                continue
            # 2. 记录答案
            avgs[i - k] = s // (k * 2 + 1)
            # 3. 离开窗口
            s -= nums[i - k * 2]
        return avgs
''',
    call='Solution().getAverages([7,4,3,9,1,8,5,2,6], 3)',
    expect=[-1, -1, -1, 5, 4, 4, -1, -1, -1],
    views=[
        dict(type='array', var='nums', label='nums（框 = 长 2k+1 的窗口，橙 = 中心）', h=250, cell=96,
             pointers={'i': 'blue', _ctr: 'orange'}, pointer_labels={_ctr: '中心 i−k'}, window=(_wl, 'i'),
             color=lambda S, i, v: 'orange' if _ctr(S) == i else None),
        dict(type='array', var='avgs', label='avgs（答案写在窗口中心）', h=200, cell=96,
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 `s = {S['s']}`，窗口长 `2k+1 = {2 * S['k'] + 1}`" if 's' in S
                           else '右端点为 `i` 的窗口，中心是 ==i − k==')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('s', 's', 'orange')],
    captions={
        'avgs = [-1]': '先全填 `-1`：两端不足 k 个邻居的位置就保持 -1',
        's = 0': '`s` 维护窗口元素和',
        'for i, x in enumerate(nums)': lambda S, B, r: (f'右端点 `i = {S.i}`，`x = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        's += x': '==入==：`s = {B.s} + {x} = {s}`',
        'if i < k * 2': lambda S, B, r: (f'`i = {S.i} < 2k = {2 * S.k}`：窗口不足 {2 * S.k + 1} 个' if S.i < 2 * S.k
                                         else f'窗口 `nums[{S.i - 2 * S.k}..{S.i}]` 凑满 {2 * S.k + 1} 个'),
        'continue': '继续入窗口',
        'avgs[i - k] = s': '==记录==：中心是 `i − k = {i - k}`，`avgs[{i - k}] = {s} // {k * 2 + 1} = {avgs[i - k]}`',
        's -= nums[i - k * 2]': '==出==：左端点 `nums[{i - k * 2}] = {nums[i - k * 2]}` 离开，`s = {s}`',
        'return avgs': '返回 `{avgs}`',
    },
    cards=dict(
        one_liner='半径 k 就是长 2k+1 的定长窗口，答案写在中心',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['对每个 `i`，求 `nums[i−k..i+k]` 的平均值（整除）；两侧不足 k 个则为 `-1`',
                 '示例：`nums = [7,4,3,9,1,8,5,2,6], k = 3`',
                 '→ `[-1,-1,-1,5,4,4,-1,-1,-1]`'],
        quote='本题相当于一个长为 2k+1 的滑动窗口。……avgs[i−k] = floor(s/(2k+1))。其中 i−k 是因为 i 对应的是子数组右端点，而记录答案的位置是子数组的正中间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['还是三步：==入== `s += x` → ==记录== `avgs[i−k]` → ==出== `s -= nums[i−2k]`',
              '`i < 2k` 时窗口不满，跳过',
              '`avgs` 预先填 -1，没被记录的位置自然就是 -1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：答案下标是==中心 i−k==，不是右端点 i',
                 '离开窗口的是 `nums[i − 2k]`',
                 '窗口和可能超过 32 位整数（其他语言要用 64 位）'],
    ),
)
