CONFIG = dict(
    num=3708, title='最长斐波那契子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='扩展到不能扩为止',
    tags=['分组循环', '难度分 1381'],
    code='''
class Solution(object):
    def longestSubarray(self, nums):
        
        res = 2
        p = 2
        while p < len(nums):
            q = p
            while q < len(nums) and nums[q] == nums[q - 1] + nums[q - 2]:
                q += 1
            
            res = max(res, q - p + 2)
            if p == q:
                p += 1
            else:
                p = q
        
        return res
''',
    call='Solution().longestSubarray([1,1,2,3,5,1,6,7,13,20])',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"当前段 `[{S['p']-2}, {S['q']-1}]`，长度 `q − p + 2` = =={S['q']-S['p']+2}==") if 'q' in S and 'p' in S else '', size=30),
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink'},
             window=(lambda S: S['p'] - 2, lambda S: max(S['q'] - 1, S['p'] - 1)) , h=300, cell=90,
             dim=lambda S, k, v: 'p' in S and k < S['p'] - 2),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 2': '长度 1、2 的子数组一定合法，答案初值 ==2==',
        'p = 2': '`p` 是第一个需要检查的下标（前两个数天然合法）',
        'q = p': '从 `p` 出发往右扩，`q` 是候选的“下一个能否加入”的位置',
        'while q < len': lambda S, B, r: ((f"`nums[{S.q}] = {S.nums[S.q]}`，`{S.nums[S.q-1]} + {S.nums[S.q-2]} = {S.nums[S.q-1]+S.nums[S.q-2]}` → 相等，能加入，继续扩" if S.q < len(S.nums) and S.nums[S.q] == S.nums[S.q-1]+S.nums[S.q-2]
                                          else ('`q` 到末尾，停止扩展' if S.q >= len(S.nums) else f"`nums[{S.q}] = {S.nums[S.q]}` 不等于前两数之和 → 扩展停止"))
                                         if S.q < len(S.nums) else '`q` 到末尾，停止扩展'),
        'q += 1': '`nums[q]` 加入子数组，`q` → {q}',
        'res = max': '子数组是 `[{p-2}, {q-1}]`，长度 `q - p + 2 = {q - p + 2}`，`res` → {res}',
        'if p == q': lambda S, B, r: ('`p == q`：连一个都没扩出来，`p` 只能后移一格' if S.p == S.q
                                       else f'扩出过结果：新的检查从停下的位置 `q = {S.q}` 开始，不回头'),
        'p += 1': '`p` → {p}',
        'p = q': '`p` 直接跳到 {p}：中间的起点只会得到更短的段',
        'return res': '最长斐波那契子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='能加入就一定加入，扩不动了再另起一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['斐波那契子数组：连续，且第 3 项起每项等于前两项之和',
                 '求 `nums` 中最长的这种子数组长度',
                 '示例：`[1,1,2,3,5,1,6,7,13,20]` → `6`'],
        quote='如果能加入到当前的子数组中，就应该加入进去，不存在选或者不选的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['求最长，所以满足条件的元素一路加入，没有取舍',
              '`p` 为起点后第三项位置，`q` 向右扩到不满足为止',
              '停下后用 `q - p + 2` 更新答案，再从停下的位置另起一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`p == q` 表示一项都没扩出来，要 `p += 1` 避免死循环',
                 '长度是 `q - p + 2`：别忘了前面两个起始数',
                 '原文已是 Python 3 可运行，未做修改'],
    ),
)
