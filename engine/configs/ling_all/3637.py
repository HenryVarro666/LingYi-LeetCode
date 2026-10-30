def _seg(S, j, v):
    a = S['nums']
    last = S['i'] if 'i' in S else 1
    if j == 0 or j > last:
        return 'green' if j == 0 and a[0] < a[1] else None
    seg = 0
    for t in range(2, j + 1):
        if (a[t - 2] < a[t - 1]) != (a[t - 1] < a[t]):
            seg += 1
    return ('green', 'orange', 'green', 'red')[min(seg, 3)]


CONFIG = dict(
    num=3637, title='三段式数组 I', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='一次遍历 · 统计拐弯次数', tags=[],
    code='''
class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        if nums[0] >= nums[1]:  # 一开始必须是递增的
            return False
        cnt = 1
        for i in range(2, len(nums)):
            if nums[i - 1] == nums[i]:
                return False
            if (nums[i - 2] < nums[i - 1]) != (nums[i - 1] < nums[i]):
                cnt += 1
        return cnt == 3  # 一定是增减增
''',
    call='Solution().isTrionic([1,3,5,4,2,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 增，橙 = 减）', h=300,
             pointers={'i - 1': 'blue', 'i': 'pink'}, color=_seg),
        dict(type='text', h=90, size=30, fn=lambda S: (f"拐弯次数 `cnt = ` ==" + str(S['cnt']) + "== （一开始是递增段，算 1 段）") if 'cnt' in S else ''),
    ],
    watch=['i', 'cnt'],
    captions={
        'if nums[0] >= nums[1]': '第一段必须递增：`{nums[0]} >= {nums[1]}`？ → {"不满足，直接 False" if nums[0] >= nums[1] else "是递增开头，继续"}',
        'cnt = 1': '已经在「增」这一段里了：`cnt = 1`（统计的是段数）',
        'for i in range': lambda S, B, r: ('从 `i = 2` 开始，每次看三个相邻的数 `nums[i-2], nums[i-1], nums[i]`' if S.i == 2 and S.cnt == 1 and B.get('i') is None else '`i` 已是最后一个，循环结束' if S.i == B.get('i') else f'`i` 右移到 {S.i}，继续看三个相邻的数'),
        'if nums[i - 1] == nums[i]': lambda S, B, r: (f'`{S.nums[S.i-1]} == {S.nums[S.i]}`：相等不是严格单调 → ==直接 False==' if S.nums[S.i-1] == S.nums[S.i]
                                                      else f'`{S.nums[S.i-1]} != {S.nums[S.i]}`：不相等，可以比大小'),
        'if (nums[i - 2]': lambda S, B, r: (
            f'前一步 `{S.nums[S.i-2]} → {S.nums[S.i-1]}` 是{"增" if S.nums[S.i-2] < S.nums[S.i-1] else "减"}，'
            f'这一步 `{S.nums[S.i-1]} → {S.nums[S.i]}` 是{"增" if S.nums[S.i-1] < S.nums[S.i] else "减"}：'
            + ('==方向变了，拐弯=='  if (S.nums[S.i-2] < S.nums[S.i-1]) != (S.nums[S.i-1] < S.nums[S.i]) else '方向没变，同一段')),
        'cnt += 1': '拐弯了，进入新的一段：`cnt` → =={cnt}==',
        'return cnt == 3': '`cnt = {cnt}`：三段（增减增）才对 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='不用写三个循环：数一数方向变了几次，恰好 3 段就对',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 要能分成三段：严格增 → 严格减 → 严格增',
                 '每段至少两个数，相邻两段共用拐点',
                 '本视频：`[1,3,5,4,2,6]` → `true`（p=2, q=4）'],
        quote='如果题目改成「增减增减增」，难道要写五个循环吗？改成统计拐弯的次数，可以推广到更一般的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一开始必须是递增，所以段数从 `cnt = 1` 起步',
              '遇到相等直接失败；方向和前一步不同就是拐弯，`cnt += 1`',
              '出现 增→减→增 共 3 段，`cnt` 恰好等于 3；一定是「增减增」'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：相等要单独判 False；只数拐弯，结尾不用再检查增减',
                 '开头已保证递增，`cnt == 3` 必然是增减增',
                 '另一种写法：三个循环，每段至少两个数，不如拐弯计数好推广'],
    ),
)
