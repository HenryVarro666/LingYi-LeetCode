NUMS, KEY, KK = [2, 9, 4, 1, 5, 6, 9, 3], 9, 1


def _wl(S):
    if 'i' not in S or 'x' not in S or S['x'] != S['key'] or S['_line'] in (5, 12):
        return None
    return max(S['i'] - S['k'], 0)


def _wr(S):
    if _wl(S) is None:
        return None
    return min(S['i'] + S['k'], len(S['nums']) - 1)


def _color(S, i, v):
    if i in (S.get('ans') or []):
        return 'green'
    if v == S['key']:
        return 'yellow'
    return None


def _txt(S):
    if 'i' not in S:
        return '黄 = 等于 key 的位置；框 = 它能覆盖的下标 `[i−k, i+k]`；绿 = 已加入答案'
    if S['x'] != S['key']:
        return f"`nums[{S['i']}] = {S['x']} ≠ key`，跳过"
    lo, hi = S['i'] - S['k'], min(S['i'] + S['k'], len(S['nums']) - 1)
    return f"`nums[{S['i']}]` 是 key → 下标 `[{max(lo, 0)}, {hi}]` 都是 K 近邻；`j = {S['j']}` 之前的==已经加过=="


CONFIG = dict(
    num=2200, title='找出数组中的所有 K 近邻下标', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举 key · 同向双指针',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def findKDistantIndices(self, nums: List[int], key: int, k: int) -> List[int]:
        ans = []
        j = 0
        for i, x in enumerate(nums):
            if x != key:
                continue
            j = max(j, i - k)  # j 至少是 i-k
            while j <= min(i + k, len(nums) - 1):  # j 至多是 i+k，但不能越界
                ans.append(j)  # 另一种写法见【Python3 写法二】
                j += 1
        return ans
''',
    call=f'Solution().findKDistantIndices({NUMS}, {KEY}, {KK})',
    expect=[0, 1, 2, 5, 6, 7],
    views=[
        dict(type='array', var='nums', label=f'nums（key = {KEY}，k = {KK}）', h=260,
             pointers={'i': 'blue', 'j': 'pink'}, window=(_wl, _wr), color=_color),
        dict(type='array', var='ans', label='ans', h=170, color=lambda S, i, v: 'green'),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集答案，按递增顺序加入',
        'j = 0': '`j`：==还没加入答案的最小下标==',
        'for i, x in': lambda S, B, r: ('遍历结束' if B.get('i') == S.i else f'看 `nums[{S.i}] = {S.x}`'),
        'if x != key': lambda S, B, r: (f'`{S.x} ≠ {S.key}`，它不是 key，不负责覆盖任何下标' if S.x != S.key
                                        else f'`nums[{S.i}] = {S.key}` 是 key：它能覆盖 `[{S.i}−{S.k}, {S.i}+{S.k}]`'),
        'continue': '跳过',
        'j = max(j, i - k)': '`j = max({B.j}, {i - k}) = {j}`：比 `{B.j}` 小的已经加过，比 `i−k` 小的够不着',
        'while j <=': lambda S, B, r: (f'`j = {S.j} ≤ min(i+k, n−1) = {min(S.i + S.k, len(S.nums) - 1)}`：`{S.j}` 在覆盖范围内'
                                       if S.j <= min(S.i + S.k, len(S.nums) - 1)
                                       else f'`j = {S.j}` 超出覆盖范围，留给下一个 key'),
        'ans.append(j)': '下标 `{j}` 离 key 不超过 k → 加入答案 `{ans}`',
        'j += 1': '`j` → {j}，每个下标==只会加入一次==',
        'return ans': '返回 `{ans}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举 key 的位置，把它周围没加过的下标依次加入答案',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['找出所有下标 `i`：存在 `j` 满足 `|i − j| ≤ k` 且 `nums[j] == key`，按递增返回',
                 '示例：`nums = [3,4,9,1,3,9,5], key = 9, k = 1` → `[1,2,3,4,5,6]`',
                 '本视频：`nums = [2,9,4,1,5,6,9,3], key = 9, k = 1` → `[0,1,2,5,6,7]`'],
        quote='也可以枚举 key 的位置，去把邻近的 i 加入答案。由于随着 i 的变大，窗口在右移，我们可以用另一个指针 j ==维护未加入答案的最小下标==。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`nums[i] == key` 时，`[max(i−k, 0), min(i+k, n−1)]` 都是答案',
              '这些区间随 i 右移 → 用 `j` 记录下一个没加入的下标，==不重复加入==',
              '`j = max(j, i−k)` 再一路加到 `min(i+k, n−1)`'],
        summary=['虽然是二重循环，`j += 1` 总共最多 `n` 次 → `O(n)`',
                 '易错：右端点要和 `n−1` 取 min，否则越界',
                 '易错：`j` 要和 `i−k` 取 max，不能直接从 `i−k` 开始（会重复）',
                 '方法一：从左往右枚举 i，记录 key 最后出现的位置 `last`，`last ≥ i−k` 就加入'],
    ),
)
