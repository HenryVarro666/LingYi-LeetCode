CONFIG = dict(
    num=3698, title='分割数组得到最小绝对差', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='定位峰顶 · 累计差值 s',
    tags=['灵神题单', '动态规划', '难度分 1649'],
    code='''
class Solution(object):
    def splitArray(self, nums):
        
        s = nums[0]
        p = 0
        while p + 1 < len(nums) and nums[p + 1] > nums[p]:
            p += 1
            s += nums[p]

        if p + 1 < len(nums) and nums[p + 1] == nums[p]:
            s -= nums[p + 1]
            p += 2
            while p < len(nums) and nums[p] < nums[p - 1]:
                s -= nums[p]
                p += 1
            
            if p != len(nums):
                return -1
            
            return abs(s)
        
        ma_p = p
        s -= nums[p]
        while p + 1 < len(nums) and nums[p + 1] < nums[p]:
            p += 1
            s -= nums[p]

        if p != len(nums) - 1:
            return -1
        
        if ma_p == 0:
            return abs(s + nums[ma_p])
        elif ma_p == len(nums) - 1:
            return abs(s - nums[ma_p])
        else:
            return min(abs(s + nums[ma_p]), abs(s - nums[ma_p]))
''',
    call='Solution().splitArray([1,3,5,4,2])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=330, cell=90, label='nums：左边上升，右边下降',
             pointers={'p': 'blue', 'ma_p': 'orange'}),
        dict(type='text', h=90, fn=lambda S: f"`s` = 左边和 − 右边和 = =={S['s']}==" if 's' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('s', 's', 'green'), ('ma_p', 'ma_p', 'orange')],
    captions={
        's = nums[0]': '`s` 记录「左子数组和 − 右子数组和」，先放入 `nums[0]` = {s}',
        'p = 0': '`p` 从头开始，扫过递增的部分，目标是定位最大值',
        'while p + 1 < len(nums) and nums[p + 1] > nums[p]': lambda S, B, r: (f"`nums[{S.p+1}] = {S.nums[S.p+1]} > nums[{S.p}] = {S.nums[S.p]}`，还在上升" if S.p + 1 < len(S.nums) and S.nums[S.p+1] > S.nums[S.p] else ("到了数组末尾" if S.p + 1 >= len(S.nums) else f"`nums[{S.p+1}] = {S.nums[S.p+1]}` 不大于 `nums[{S.p}] = {S.nums[S.p]}` → 上升结束，`nums[{S.p}]` 是最大值")),
        'p += 1': '`p` → {p}',
        's += nums[p]': '上升部分归左边：`s` += `{nums[p]}` → =={s}==',
        'if p + 1 < len(nums) and nums[p + 1] == nums[p]': lambda S, B, r: (f"`nums[{S.p+1}] == nums[{S.p}]`：峰顶有两个相等的值，划分唯一" if S.p + 1 < len(S.nums) and S.nums[S.p+1] == S.nums[S.p] else f"`nums[{S.p}]` 是唯一的最大值：它归左还是归右，要看哪边差更小"),
        's -= nums[p + 1]': '第二个峰顶归右边：`s` −= `{nums[p+1]}`→ =={s}==',
        'p += 2': '跳过两个峰顶，`p` → {p}',
        'while p < len(nums) and nums[p] < nums[p - 1]': lambda S, B, r: (f"`nums[{S.p}] = {S.nums[S.p]} < nums[{S.p-1}] = {S.nums[S.p-1]}`，还在下降" if S.p < len(S.nums) and S.nums[S.p] < S.nums[S.p-1] else ("下降扫完整个数组" if S.p >= len(S.nums) else "不再下降")),
        17: lambda S, B, r: ('`p` 走到末尾：右半一路递减' if S.p == len(S.nums) else '`p` 没走到末尾 → 剩下的不是递减，返回 -1'),
        14: '右半归右边：`s` −= `{nums[p]}` → =={s}==',
        26: '右半归右边：`s` −= `{nums[p]}` → =={s}==',
        'return abs(s)': '返回 `|s|` = =={abs(s)}==',
        'ma_p = p': '记下峰顶下标 `ma_p = {ma_p}`，它先不算进任何一边',
        23: '`s` 里先扣掉峰顶（它在上面被加进了左边）：`s` = =={s}==',
        'while p + 1 < len(nums) and nums[p + 1] < nums[p]': lambda S, B, r: (f"`nums[{S.p+1}] = {S.nums[S.p+1]} < nums[{S.p}] = {S.nums[S.p]}`，还在下降" if S.p + 1 < len(S.nums) and S.nums[S.p+1] < S.nums[S.p] else ("到了数组末尾" if S.p + 1 >= len(S.nums) else "不再下降")),
        'if p != len(nums) - 1': lambda S, B, r: ("`p` 没到最后一个 → 后半不是递减，返回 -1" if S.p != len(S.nums) - 1 else "`p` 正好停在最后一个：整个数组是山峰，能分割"),
        'if ma_p == 0': '峰顶在最左端？ `ma_p = {ma_p}`',
        'elif ma_p == len(nums) - 1': '峰顶在最右端？',
        'return min(': lambda S, B, r: f"峰顶 `{S.nums[S.ma_p]}` 可左可右：`|{S.s}+{S.nums[S.ma_p]}|` 与 `|{S.s}−{S.nums[S.ma_p]}|` 取小 =={r}==",
    },
    cards=dict(
        one_liner='先找到峰顶，再把峰顶分给差更小的那一边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 分成非空的 `left`、`right`：`left` 严格递增，`right` 严格递减',
                 '返回两边元素和之差的最小绝对值；无法分割返回 `-1`',
                 '本视频：`[1,3,5,4,2]` → `3`'],
        quote='无论是上面哪种情况，在一开始都应该先想办法定位到这个最大值的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['峰顶只有两种：两个相等的峰顶（划分唯一），或唯一峰顶（可左可右）',
              '变量 `s` 直接记录两边之差：左边加、右边减',
              '先扫上升，再确认剩下的部分一路下降；中途不满足就 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '唯一峰顶先被算进左边，之后 `s -= nums[p]` 扣掉，最后再用 `s ± 峰顶` 决定归属',
                 '峰顶在最左端只能归左边，在最右端只能归右边',
                 '对比灵神：灵神同时求前缀与后缀再分类，yiduobo 用一个 `s` 一趟推进',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
