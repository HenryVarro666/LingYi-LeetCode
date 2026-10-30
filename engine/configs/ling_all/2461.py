def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1) + (1 if S.get('_line') in (20, 21, 22, 23) else 0)  # 出窗口后左端点右移


def _upd(S, B, ret):
    if len(S.cnt) == S.k:
        return f'`len(cnt) = {S.k}`：窗口 {S.k} 个数==两两不同==，可以更新答案'
    return f'`len(cnt) = {len(S.cnt)} < k = {S.k}`：窗口里==有重复==，不能用'


CONFIG = dict(
    num=2461, title='长度为 K 子数组中的最大和', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 + 哈希表计数',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1553'],
    code='''
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        ans = s = 0
        cnt = defaultdict(int)
        for i, x in enumerate(nums):
            # 1. 进入窗口
            s += x
            cnt[x] += 1

            left = i - k + 1
            if left < 0:  # 窗口大小不足 k
                continue

            # 2. 更新答案
            if len(cnt) == k:
                ans = max(ans, s)

            # 3. 离开窗口
            out = nums[left]
            s -= out
            cnt[out] -= 1
            if cnt[out] == 0:
                del cnt[out]  # 保证 len(cnt) 不计入出现 0 次的元素

        return ans
''',
    call='Solution().maximumSubarraySum([1,5,4,2,9,9,9], 3)',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums（框 = 长 k 的窗口）', h=240, cell=100,
             pointers={'i': 'blue', 'left': 'pink'}, window=(_wl, 'i')),
        dict(type='map', var='cnt', label='cnt（窗口内每个数的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 `s = {S['s']}`，不同元素 `len(cnt) = {len(S['cnt'])}`，需要 `= k = {S['k']}`"
                           if 'cnt' in S else '==len(cnt) == k== ⇔ 窗口内元素两两不同')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('left', 'left', 'pink'), ('s', 's', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = 0': '`s`：窗口元素和；`ans`：答案（没有合法子数组时返回 0）',
        'cnt = defaultdict': '`cnt` 记录窗口里每个数出现几次',
        'for i, x in enumerate(nums)': lambda S, B, r: (f'右端点 `i = {S.i}`，`x = {S.x}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        's += x': '==入==：`s = {B.s} + {x} = {s}`',
        'cnt[x] += 1': '`cnt[{x}]` → {cnt[x]}',
        'left = i - k + 1': '窗口左端点 `left = {i} − {k} + 1 = {left}`',
        'if left < 0': lambda S, B, r: (f'`left = {S.left} < 0`：窗口不足 {S.k} 个' if S.left < 0
                                        else f'窗口 `{S.nums[S.left:S.i + 1]}` 长度为 {S.k}'),
        'continue': '继续入窗口',
        'if len(cnt) == k': _upd,
        'ans = max(ans, s)': '==更新==：`ans = max({B.ans}, {s}) = {ans}`',
        'out = nums[left]': '==出==：左端点 `nums[{left}] = {out}` 离开窗口',
        's -= out': '`s = {B.s} − {out} = {s}`',
        'cnt[out] -= 1': '`cnt[{out}]` → {cnt[out]}',
        'if cnt[out] == 0': lambda S, B, r: (f'`cnt[{S.out}] = 0`：{S.out} 已不在窗口里' if S.cnt[S.out] == 0
                                             else f'`cnt[{S.out}] = {S.cnt[S.out]}`：窗口里还有 {S.out}，保留'),
        'del cnt[out]': '删掉键 `{out}`，==否则 len(cnt) 会把它算进去==',
        'return ans': '最大和为 `{ans}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='用哈希表的大小判断窗口里有没有重复',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['求长度为 `k` 且==元素各不相同==的子数组的最大和，不存在返回 `0`',
                 '示例：`nums = [1,5,4,2,9,9,9], k = 3` → `15`（`[4,2,9]`）'],
        quote='同 2841. 几乎唯一子数组的最大和，把 ≥ m 改成 = k 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定长滑窗三步：入（`s`、`cnt` 加）→ 更新 → 出（`s`、`cnt` 减）',
              '`cnt` 的键数 = 窗口里不同元素个数；==等于 k 就说明没有重复==',
              '计数减到 0 要 `del`，`len(cnt)` 才准确'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '易错：忘记 `del cnt[out]`，`len(cnt)` 偏大会误判',
                 '和 2841 是同一模板：「至少 m 种」改成「恰好 k 种」',
                 '答案初值为 0，正好对应「不存在返回 0」'],
    ),
)
