LEAVE = 13  # 「3. 离开窗口」那一行的行号


def _wl(S):
    if 'i' not in S:
        return None
    i, k = S['i'], S['k']
    lo = i - k + 1 + (1 if S.get('_line') == LEAVE else 0)
    return max(0, lo)


def _wr(S):
    if 'i' not in S:
        return None
    return S['i'] - 1 if S.get('_line') == 5 else S['i']


def _color(S, i, v):
    if 'i' not in S:
        return None
    if S.get('_line') == LEAVE and i == S['i'] - S['k'] + 1:
        return 'red'
    if i == S['i'] and S.get('_line') in (6, 7):
        return 'green'
    return None


def show(S):
    if 'i' not in S:
        return '定长滑窗三步：==入== → ==更新== → ==出=='
    ms = S['max_s']
    ms = '-∞' if ms == float('-inf') else ms
    return f"窗口和 `s = {S['s']}`，最大窗口和 `max_s = {ms}`"


def hist(S):
    if 'i' not in S:
        return ''
    i, k, a = S['i'], S['k'], S['nums']
    done = [j for j in range(k - 1, i + 1) if j < i or S.get('_line') in (11, 13)]
    if not done:
        return '窗口还没凑满 k 个数，暂不更新答案'
    parts = [f"`[{j - k + 1}..{j}] = {sum(a[j - k + 1:j + 1])}`" for j in done]
    return '已更新过的窗口和：' + '，'.join(parts)


def cap_if(S, B, ret):
    i, k = S.i, S.k
    if i < k - 1:
        return f'窗口里才 `{i + 1}` 个数，大小不足 `k = {k}` → 跳过更新，继续入'
    return f'窗口 `[{i - k + 1}, {i}]` 恰好 `{k}` 个数 → 可以更新答案'


CONFIG = dict(
    num=643, title='子数组最大平均数 I', difficulty='Easy', category='滑动窗口',
    author='灵茶山艾府', technique='定长滑动窗口 · 入-更新-出',
    tags=['字节30天'],
    code='''
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        max_s = -inf  # 窗口元素和的最大值
        s = 0  # 维护窗口元素和
        for i, x in enumerate(nums):
            # 1. 进入窗口
            s += x
            if i < k - 1:  # 窗口大小不足 k
                continue
            # 2. 更新答案
            max_s = max(max_s, s)
            # 3. 离开窗口
            s -= nums[i - k + 1]
        return max_s / k
''',
    call='Solution().findMaxAverage([1,12,-5,-6,50,3], 4)',
    expect=12.75,
    views=[
        dict(type='array', var='nums', label='nums（k = 4，青框 = 当前窗口，绿 = 刚进入，红 = 要离开）', cell=110,
             pointers={'i': 'blue'}, window=(_wl, _wr), color=_color, h=215),
        dict(type='text', fn=show, size=30, h=80),
        dict(type='text', fn=lambda S: hist(S), size=26, h=130, lines=3),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('s', 's', 'cyan'), ('max_s', 'max_s', 'green')],
    skip=['continue'],
    captions={
        'max_s = -inf': '`max_s` 记录窗口元素和的最大值：==nums 有负数，要初始化成 -inf==',
        's = 0': '`s` 维护窗口元素和，窗口每次只变动两个数',
        's += x': '1. ==入==：`nums[{i}] = {x}` 进入窗口，`s = {s}`',
        'if i < k - 1': cap_if,
        'max_s = max': lambda S, B, ret: f"2. ==更新==：`max_s = max({'-inf' if B.max_s == float('-inf') else B.max_s}, {S.s}) = {S.max_s}`",
        's -= nums': '3. ==出==：`nums[{i - k + 1}] = {nums[i - k + 1]}` 离开窗口，`s = {s}`，为下一个窗口做准备',
        'return max_s / k': '最后再除以 `k`：`{max_s} / {k}` = =={ret}==',
    },
    cards=dict(
        one_liner='定长滑窗三步走：入 - 更新 - 出，维护窗口元素和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你整数数组 `nums` 和整数 `k`，找出==长度为 k== 的连续子数组的最大平均数',
                 '示例：`nums = [1,12,-5,-6,50,3]`，`k = 4` → `12.75`',
                 '解释：`(12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75`'],
        quote='我总结成三步：==入-更新-出==。……以上三步适用于所有定长滑窗题目。',
        quote_src='—— 灵茶山艾府题解「定长滑窗套路」',
        idea=['入：下标 `i` 进入窗口，`s += nums[i]`；若 `i < k-1`，窗口还不够长，继续入',
              '更新：窗口长度固定为 `k`，统计窗口和的最大值，==最后再除以 k==',
              '出：下标 `i-k+1` 离开窗口，`s -= nums[i-k+1]`'],
        result='最大窗口和是 `51`（下标 1~4），`51 / 4 = 12.75` ✓',
        summary=['时间 `O(n)`：每个数入窗口、出窗口各一次；空间 `O(1)`',
                 '易错：`nums` 有负数，`max_s` 要初始化成 `-inf`，不能是 `0`',
                 '技巧：比较窗口和而不是平均数，只在最后除一次 `k`',
                 '同一模板：1456 定长子串中元音的最大数目、2090 半径为 k 的子数组平均值'],
    ),
)
