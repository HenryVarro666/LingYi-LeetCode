CONFIG = dict(
    num=4038, title='计算单个区间中出现的整数数量', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 一次遍历',
    tags=['灵神题单'],
    code='''
class Solution:
    def countSpecialIntegers(self, nums: list[int]) -> int:
        cnt = defaultdict(int)
        ans = 0
        for i, x in enumerate(nums):
            if i == 0 or x != nums[i - 1]:  # x 是这一段的第一个数
                cnt[x] += 1
                if cnt[x] == 1:  # 首次遇到 x，暂时认为 x 是特殊整数
                    ans += 1
                elif cnt[x] == 2:  # x 不是特殊整数，撤销之前的 ans += 1
                    ans -= 1
        return ans
''',
    call='Solution().countSpecialIntegers([3,3,1,2,2,1])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: ('yellow' if 'i' in S and i == S['i'] and (i == 0 or v != S['nums'][i-1]) else None)),
        dict(type='map', var='cnt', label='cnt（x 作为「段首」出现的次数）', fmt=lambda k, v: f"{k}: {v}", h=190, font=34),
        dict(type='text', h=80, fn=lambda S: f"当前答案 ans = =={S['ans']}==" if 'ans' in S else ''),
    ],
    watch=['i', 'x', ('ans', 'ans', 'green')],
    captions={
        'if i == 0 or x != nums[i - 1]': lambda S, B, r: (f'`x = {S.x}` 与前一个数相同 → 还在同一段里，跳过' if not (S.i == 0 or S.x != S.nums[S.i-1])
                                                           else f'`x = {S.x}` 是新一段的开头（段首）→ 数一次'),
        'cnt[x] += 1': '`cnt[{x}]` 记录 {x} 作为段首出现了几次 → {cnt[x]}',
        'if cnt[x] == 1': lambda S, B, r: f'`cnt[{S.x}] = {S.cnt[S.x]}`：' + ('首次出现段首' if S.cnt[S.x] == 1 else '不是第一次'),
        9: '首次遇到 {x}，先当它是特殊整数：`ans` → =={ans}==',
        'elif cnt[x] == 2': lambda S, B, r: f'`cnt[{S.x}] = {S.cnt[S.x]}`：' + ('第二次成段 → 被别的数隔开了' if S.cnt[S.x] == 2 else '不是第二次'),
        11: '{x} 又以新的一段出现 → 位置不连续，撤销之前的加一：`ans` → =={ans}==',
        'return ans': '剩下的都是只成一段的数：答案 `{ans}`',
    },
    cards=dict(
        one_liner='只看每段的段首：同一个数第二次成段，就撤销',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['若 `x` 的所有出现位置都在同一个连续区间内，`x` 就是特殊整数',
                 '求 `nums` 中不同特殊整数的个数',
                 '示例：`[3,3,1,2,2,1]` → `2`（3 和 2 是）'],
        quote='如果首次遇到 x，那么暂时认为 x 是特殊整数，把答案加一。如果第二次遇到 x，那么 x 不是特殊整数，撤销之前的加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只考虑每个连续相同段的第一个数，同一段内的重复不用管',
              '一个数只成一段 → 保持计入；又成第二段 → 撤销一次',
              '第三段及以后 `cnt` 已大于 2，不会再重复撤销'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：只在段首计数，同一段内的重复不能算',
                 '撤销只在 `cnt[x] == 2` 时做一次，否则会减多',
                 '另一种写法：记录每个数的出现位置列表 `p`，若 `p[-1]-p[0]+1 == len(p)` 则连续'],
    ),
)
