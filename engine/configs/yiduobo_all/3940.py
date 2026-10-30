CONFIG = dict(
    num=3940, title='限制有序数组中的元素出现次数', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='计数 cnt + 写指针 p',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def limitOccurrences(self, nums, k):
        
        p = 0
        cnt = 0
        pre = None
        for v in nums:
            if v == pre:
                cnt += 1
            else:
                cnt = 1
            
            if cnt <= k:
                nums[p] = v
                p += 1
            
            pre = v
        
        while len(nums) > p:
            nums.pop()
        
        return nums
''',
    call='Solution().limitOccurrences([1,1,1,1,2,2,2,3], 2)',
    expect=[1, 1, 2, 2, 3],
    views=[
        dict(type='text', fn=lambda S: (f"当前值 `{S['v']}`，已连续出现 `cnt = {S['cnt']}` 次（上限 k = {S['k']}）" if 'v' in S and S['cnt'] else '')),
        dict(type='array', var='nums', pointers={'p': 'pink'}, h=300,
             color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None),
    ],
    watch=[('v', 'v', 'blue'), ('cnt', 'cnt', 'yellow'), ('p', 'p', 'pink'), 'pre', 'k'],
    captions={
        'for v in nums': '`for` 读取下一个元素；没有了就结束循环',
        'p = 0': '`p` 是写指针：`nums[:p]` 是已确认保留的部分',
        'cnt = 0': '`cnt` 记录当前这个数连续出现了几次',
        'pre = None': '`pre` 记录上一个元素，用来判断是不是同一个数',
        'if v == pre': '`v = {v}`，`pre = {pre}`：{"相同 → 连续次数加一" if v == pre else "不同 → 新的数，次数重置为 1"}',
        'cnt += 1': '同一个数又出现一次：`cnt` → {cnt}',
        'cnt = 1': '遇到新的数：`cnt = 1`',
        'if cnt <= k': '`cnt = {cnt}` 与 `k = {k}`：{"不超过 k → 该保留" if cnt <= k else "超过 k 次 → 该删掉，不写入"}',
        'nums[p] = v': '把 `{v}` 填到 `nums[{p}]`，`p` 右移',
        'p += 1': '`p` → {p}',
        'pre = v': '`pre` 更新为 `{pre}`',
        'while len(nums) > p': '`len(nums) = {len(nums)}`，`p = {p}`：{"还有多余元素，要删" if len(nums) > p else "长度等于 p，删完了"}',
        'nums.pop()': '弹掉末尾一个多余元素',
        'return nums': '返回 `{nums}`',
    },
    cards=dict(
        one_liner='数一数当前数出现几次，不超过 k 就写到 p 位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['升序数组 `nums` 和整数 `k`，每个不同元素最多保留 `k` 次',
                 '示例：`[1,1,1,2,2,3], k=2` → `[1,1,2,2,3]`',
                 '本视频：`[1,1,1,1,2,2,2,3], k=2`'],
        quote='相同的元素在nums中是连续出现的，以此可以从左到右对nums进行一趟遍历，同时使用一个变量cnt记录当前元素出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前元素与前一个相同 `cnt += 1`，否则 `cnt = 1`',
              '`cnt <= k` 就保留：填到 `nums[p]`，`p += 1`',
              '遍历完，用 `pop` 把 `p` 之后的元素都删掉'],
        summary=['时间 `O(n)`，空间 `O(1)`（原地修改）',
                 '写指针 `p` 永远不会超过读到的位置，覆盖是安全的',
                 '`pre` 要放在判断之后更新',
                 '对比灵神：灵神与栈倒数第 k 个比较，yiduobo 显式计数'],
    ),
)
