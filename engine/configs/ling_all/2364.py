NUMS = [4, 1, 3, 3, 6, 5, 9]


def _txt(S):
    if 'i' not in S:
        return '坏数对 = ==全部数对== − 好数对；好数对 ⇔ `nums[i] − i == nums[j] − j`'
    i, x = S['i'], S['x']
    return f"`x − i = {x} − {i}` = =={x - i}==：左边已有 `{S['cnt'].get(x - i, 0) - (1 if S['_line'] == 7 else 0)}` 个相同的 → 都是好数对"


CONFIG = dict(
    num=2364, title='统计坏数对的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='正难则反 + 枚举右，维护左',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1622'],
    code='''
class Solution:
    def countBadPairs(self, nums: List[int]) -> int:
        ans = comb(len(nums), 2)
        cnt = defaultdict(int)
        for i, x in enumerate(nums):
            ans -= cnt[x - i]
            cnt[x - i] += 1
        return ans
''',
    call=f'Solution().countBadPairs({NUMS})',
    expect=18,
    views=[
        dict(type='array', var='nums', label='nums', h=190, pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('i') else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='array', var=lambda S: [v - k for k, v in enumerate(S['nums'])], label='nums[i] − i（相等 ⇔ 好数对）', h=190,
             color=lambda S, i, v: ('blue' if i == S['i'] else 'green' if i < S['i'] and v == S['x'] - S['i'] else None) if 'i' in S else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='map', var='cnt', label='cnt（左边每种 nums[i] − i 的个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('ans', 'ans', 'green')],
    captions={
        'ans = comb(': '正难则反：先假设全是坏数对，`C({len(nums)}, 2)` = =={ans}==',
        'cnt = defaultdict': '`cnt` 统计左边每个 `nums[i] − i` 出现的次数',
        'for i, x in enumerate': lambda S, B, r: (f'枚举右边的 `j = {S.i}`，`nums[j] = {S.x}`' if B.get('i') != S.i else '遍历结束'),
        'ans -= cnt[x - i]': lambda S, B, r: (f'左边有 `{B.ans - S.ans}` 个 `nums[i] − i = {S.x - S.i}` → 都是==好数对==，`ans` 减去 → {S.ans}' if B.ans != S.ans
                                             else f'左边没有 `nums[i] − i = {S.x - S.i}` 的数，`ans` 不变'),
        'cnt[x - i] += 1': '维护左：`cnt[{x - i}]` → `{cnt[x - i]}`（==先减答案再计数==，不和自己配对）',
        'return ans': '坏数对共 `{ans}` 个',
    },
    cards=dict(
        one_liner='移项成 nums[i] − i ≠ nums[j] − j，正难则反数相等的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`i < j` 且 `j − i ≠ nums[j] − nums[i]` 的 `(i, j)` 是==坏数对==，求个数',
                 '示例：`[4,1,3,3]` → `5`',
                 f'本视频：`{NUMS}` → `18`'],
        quote='移项得 nums[i] − i ≠ nums[j] − j。==正难则反==，用总数对个数 n(n−1)/2 减去满足 nums[i] − i = nums[j] − j 的数对个数，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `a[i] = nums[i] − i`，好数对就是 `a[i] == a[j]`，和 1512 题一样',
              '枚举右边的 `j`，左边有 `cnt[a[j]]` 个和它相等 → 从总数里减掉',
              '为什么先更新 `ans` 再更新 `cnt`？避免 `j` 和自己配对'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '“不等”难数，“相等”好数：==正难则反==',
                 '移项把 `i`、`j` 分到两边，才能用哈希表',
                 '前置题：1512. 好数对的数目'],
    ),
)
