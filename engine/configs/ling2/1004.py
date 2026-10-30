def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['left'] <= i <= S['right']:
        return 'orange' if v == 0 else 'green'
    return None


def _top(S):
    if 'right' not in S:
        return '窗口内最多有 ==k = 2== 个 0（把它们翻成 1）'
    l, r = S['left'], S['right']
    c = S['cnt0']
    flag = '合法' if c <= S['k'] else '==不合法=='
    return f'窗口 `[{l}, {r}]`：长度 `{r - l + 1}`，里面有 `cnt0 = {c}` 个 0 → {flag}'


def _in(S, B, ret):
    r, x = S.right, S.x
    if x == 0:
        return f'`nums[{r}] = 0` 进入窗口：0 变成 1 要用掉一次翻转，`cnt0` → =={S.cnt0}=='
    return f'`nums[{r}] = 1` 进入窗口：`1 - x = 0`，`cnt0` 不变（{S.cnt0}）'


def _while(S, B, ret):
    if S.cnt0 > S.k:
        return f'`cnt0 = {S.cnt0} > k = {S.k}`：0 太多翻不完 → ==移动左端点缩小窗口=='
    return f'`cnt0 = {S.cnt0} ≤ k = {S.k}`：窗口合法'


def _out(S, B, ret):
    v = S.nums[S.left]
    if v == 0:
        return f'`nums[{S.left}] = 0` 移出窗口：`cnt0` → {S.cnt0}'
    return f'`nums[{S.left}] = 1` 移出窗口：`cnt0` 不变，还得继续缩'


CONFIG = dict(
    num=1004, title='最大连续1的个数 III', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='不定长滑动窗口 · 统计窗口内 0 的个数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        ans = left = cnt0 = 0
        for right, x in enumerate(nums):
            cnt0 += 1 - x  # 0 变成 1，用来统计 cnt0
            while cnt0 > k:
                cnt0 -= 1 - nums[left]
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().longestOnes([1, 0, 0, 1, 1, 0, 1, 1], 2)',
    expect=6,
    skip=['for right, x in'],
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var='nums', h=300, cell=96, window=('left', 'right'), color=_color,
             pointers={'left': 'blue', 'right': 'pink'},
             label='nums（窗口内：绿 = 1，橙 = 要翻转的 0）'),
        dict(type='text', size=26, fn=lambda S: (
            f"目前最长：`ans = {S['ans']}`" if 'ans' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cnt0', 'cnt0', 'orange'), ('k', 'k'),
           ('ans', 'ans', 'green')],
    captions={
        'ans = left = cnt0': '翻转 ≤ k 个 0 ⇔ 窗口内 ==0 的个数 cnt0 ≤ k==，求这样的窗口最长多长',
        'cnt0 += 1 - x': _in,
        'while cnt0 > k': _while,
        'cnt0 -= 1 - nums[left]': _out,
        'left += 1': '`left` → {left}',
        'ans = max': '窗口 `[{left}, {right}]` 合法，长度 `{right - left + 1}` → `ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最长 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右端点，窗口内 0 的个数超过 k 就移动左端点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你 0/1 数组 `nums` 和整数 `k`，最多可以把 `k` 个 0 翻转成 1',
                 '返回翻转后数组中==连续 1 的最大个数==',
                 '示例：`[1,1,1,0,0,0,1,1,1,1,0], k = 2` → `6`',
                 '本视频：`[1,0,0,1,1,0,1,1], k = 2` → `6`'],
        quote='统计窗口内 0 的个数 cnt0，则问题转化成在 cnt0 ≤ k 的前提下，窗口大小的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['翻转哪些 0 不用真的去翻：只要窗口里 ==0 不超过 k 个==，整段都能变成 1',
              '右端点每次右移一格；`cnt0 > k` 时左端点右移，直到合法',
              '`cnt0 += 1 - x`：x 是 0 时加 1，x 是 1 时加 0，==不用写 if=='],
        summary=['时间 `O(n)`：left 和 right 都只右移，每个元素最多进出窗口各一次；空间 `O(1)`',
                 '先把 `right` 加进窗口，再用 `while` 收缩，最后才更新 `ans`',
                 '用 `while` 不是 `if`：移出的可能是 1，要一直缩到 `cnt0 ≤ k`',
                 '同类模板：不定长滑动窗口求最长（如 3. 无重复字符的最长子串）'],
    ),
)
