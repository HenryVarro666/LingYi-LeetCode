CONFIG = dict(
    num=3101, title='交替子数组计数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举右端点 · 维护 cnt', tags=[],
    code='''
class Solution:
    def countAlternatingSubarrays(self, nums: List[int]) -> int:
        ans = cnt = 0
        for i in range(len(nums)):
            if i > 0 and nums[i] != nums[i - 1]:
                cnt += 1
            else:
                cnt = 1
            ans += cnt  # 有 cnt 个右端点下标为 i 的交替子数组
        return ans
''',
    call='Solution().countAlternatingSubarrays([0,1,1,0,1,1])',
    expect=10,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if 'i' in S and S['i'] - S['cnt'] < i <= S['i'] else None) if 'cnt' in S and 'i' in S else None),
        dict(type='text', size=34, fn=lambda S: (f"以 `{S['i']}` 为右端点的交替子数组：`cnt` = =={S['cnt']}==，累计 `ans = {S['ans']}`") if 'i' in S and S.get('cnt') else ''),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt = 0': '`ans` 累计答案，`cnt` 记录以当前下标为右端点的交替子数组个数',
        'if i > 0 and': lambda S, B, r: (f"`nums[{S.i}] = {S.nums[S.i]}`，是第一个数，只能自己成一个子数组" if S.i == 0 else
                                         f"`nums[{S.i}] = {S.nums[S.i]}` 与前一个 `{S.nums[S.i-1]}` " + ('不同 → 能接在前面所有交替子数组后面' if S.nums[S.i] != S.nums[S.i-1] else '相同 → 前面的都接不上了')),
        'cnt += 1': '相邻不同：新增 1 个（整段接上 `nums[i]`），`cnt` → =={cnt}==',
        'cnt = 1': '相邻相同：只剩 `nums[i]` 单独一个，`cnt` 重置为 =={cnt}==',
        'ans += cnt': '右端点为 `{i}` 的交替子数组有 `{cnt}` 个 → `ans` = =={ans}==',
        'return ans': '所有右端点的个数加起来：=={ans}==',
    },
    cards=dict(
        one_liner='枚举右端点，以它结尾的交替子数组个数 cnt 递推',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `nums`，子数组中没有相邻相同的元素就叫交替子数组', '统计交替子数组的个数',
                 '示例：`[0,1,1,1]` → `5`；本视频：`[0,1,1,0,1,1]` → `10`'],
        quote='枚举交替子数组的右端点下标 i，统计交替子数组的个数，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[i] != nums[i-1]`：把 `nums[i]` 接到以 `i-1` 结尾的每个交替子数组后，再加单独一个 → `cnt + 1`',
              '否则前面都接不上，`cnt` 重置为 1',
              '每个右端点的 `cnt` 累加就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：相等时 `cnt` 要重置为 1，不是 0',
                 '另有 pairwise 写法，`ans = cnt = 1` 起步，思路相同',
                 '同类：以右端点为准的计数，如 `1695`、`713`'],
    ),
)
