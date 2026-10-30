NUMS = [1, 2, 3, 1, 2, 3, 1, 2]
K = 2


def _color(S, i, v):
    if 'right' not in S:
        return None
    if i == S['right']:
        return 'pink'
    if S['left'] <= i <= S['right'] and v == S['x']:
        return 'orange'
    return None


def _dim(S, i, v):
    return 'right' in S and not (S['left'] <= i <= S['right'])


def _top(S):
    if 'right' not in S:
        return f'窗口内每个元素的出现次数都要 ==≤ k = {K}=='
    x, c = S['x'], S['cnt'][S['x']]
    return f"新加入 `x = {x}`，窗口内 `{x}` 出现 `{c}` 次 {'≤' if c <= K else '>'} `{K}` → {'==合法==' if c <= K else '左端右移'}"


def _while(S, B, ret):
    c = S.cnt[S.x]
    if c > S.k:
        return f'`cnt[{S.x}] = {c} > k = {S.k}`：{S.x} 太多了 → 移出左端 `nums[{S.left}] = {S.nums[S.left]}`'
    return f'`cnt[{S.x}] = {c} ≤ {S.k}`：窗口合法（只有 x 可能超标，检查它就够）'


CONFIG = dict(
    num=2958, title='最多 K 个重复元素的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 哈希计数',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for right, x in enumerate(nums):
            cnt[x] += 1
            while cnt[x] > k:
                cnt[nums[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call=f'Solution().maxSubarrayLength({NUMS}, {K})',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口，粉 = 新加入的 x，橙 = 窗口里与 x 相同的数）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, dim=_dim, cell=100, h=300),
        dict(type='map', var='cnt', label='cnt（窗口内各元素出现次数）', fmt=lambda k, v: f'{k}: {v}', font=34, h=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'x', ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans = 0`，窗口左端 `left = 0`',
        'cnt = defaultdict': '`cnt` 统计窗口内每个元素的出现次数',
        'for right, x in': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                            else f'枚举右端点 `right = {S.right}`，`x = {S.x}` 进入窗口'),
        'cnt[x] += 1': '`cnt[{x}]` → {cnt[x]}',
        'while cnt[x] > k': _while,
        'cnt[nums[left]] -= 1': lambda S, B, r: f'`nums[{S.left}] = {S.nums[S.left]}` 离开窗口：`cnt[{S.nums[S.left]}]` → {S.cnt[S.nums[S.left]]}',
        'left += 1': '`left` → {left}',
        'ans = max': '窗口 `[{left}, {right}]` 长 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最长好子数组长度 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='新加入 x 后若 x 超过 k 次，就右移左端直到 x 恰好 k 次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['==好数组==：每个元素出现次数都 `≤ k`',
                 '求 `nums` 中最长好子数组的长度',
                 '示例：`[1,2,3,1,2,3,1,2], k = 2` → `6`（如 `[1,2,3,1,2,3]`）'],
        quote='新加入元素 x=nums[right] 后，如果 x 的出现次数超过 k，则不断右移左指针 left，==直到窗口内的 x 的出现次数等于 k 为止==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['加入 x 之前窗口是好的 → 加入后==只有 x 可能超标==',
              '所以 while 只需检查 `cnt[x] > k`',
              '内层结束后用 `right − left + 1` 更新答案'],
        summary=['时间 `O(n)`：left 只右移；空间 `O(n)` 存哈希表',
                 '离开窗口时减的是 `cnt[nums[left]]`，不是 `cnt[x]`',
                 '先减计数再 `left += 1`，顺序别反',
                 '同类：3. 无重复字符的最长子串就是 `k = 1` 的情况'],
    ),
)
