CONFIG = dict(
    num=2936, title='包含相等值数字块的数量', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分找块的最后位置', tags=['灵神题单'],
    setup='''
class BigArray:
    def __init__(self, a):
        self.a = a
    def size(self):
        return len(self.a)
    def at(self, i):
        return self.a[i]
''',
    code='''
class Solution(object):
    def countBlocks(self, nums):
        
        n = nums.size()
        p = 0
        res = 0
        while p < n:
            left, right = p, n - 1
            v = nums.at(p)
            while left < right:
                mid = (left + right + 1) // 2
                if nums.at(mid) == v:
                    left = mid
                else:
                    right = mid - 1
                
            res += 1
            p = left + 1
        
        return res
''',
    call='Solution().countBlocks(BigArray([1,1,2,2,2,2,3,3,3,3]))',
    expect=3,
    max_steps=90,
    views=[
        dict(type='text', fn=lambda S: (f"块的值 `v = {S['v']}`：在 `[{S['left']}, {S['right']}]` 里二分，找 `v` 最后一次出现的下标" if 'v' in S and 'left' in S and S['p'] < S['n'] else '')),
        dict(type='array', var=lambda S: S['nums'].a, label='nums（只能 at(i) 访问）', pointers={'p': 'cyan', 'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, h=320,
             window=('left', 'right'),
             color=lambda S, k, v: ('green' if 'v' in S and v == S['v'] and k < S['p'] else None),
             dim=lambda S, k, v: 'p' in S and k < S['p']),
    ],
    watch=[('p', 'p', 'cyan'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', ('res', 'res', 'green')],
    captions={
        'n = nums.size()': '`n = {n}`：数组只能用 `size/at` 访问',
        'p = 0': '`p` 是剩余数组的最左端，也就是当前块的起点',
        'res = 0': '`res` 计数块数',
        'while p < n': lambda S, B, r: (f'`p = {S.p} < n = {S.n}`：还剩数字块没分离' if S.p < S.n else f'`p = {S.p} = n`：全部分离完'),
        'left, right = p, n - 1': '在剩余数组 `[{p}, {n-1}]` 里找块的右端点',
        'v = nums.at(p)': '最左侧元素就是块的数值：`v = {v}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：区间没缩完，继续二分' if S.left < S.right else f'`left = right = {S.left}`：找到 `{S.v}` 的最后一个下标'),
        'mid = (left + right + 1)': '取上中位数 `mid = {mid}`（因为 `left = mid` 要防死循环）',
        'if nums.at(mid) == v': lambda S, B, r: (f'`nums[{S.mid}] = {S.nums.at(S.mid)}` == `{S.v}` → 最后一个 v 在 mid 或更右' if S.nums.at(S.mid) == S.v else f'`nums[{S.mid}] = {S.nums.at(S.mid)}` != `{S.v}` → 最后一个 v 一定在 mid 左边'),
        'left = mid': '`left = mid = {left}`',
        'right = mid - 1': '`right = mid - 1 = {right}`',
        'res += 1': '这一块 `[{p}, {left}]` 分离出来，`res = {res}`',
        'p = left + 1': '剩余数组从 `left + 1 = {p}` 开始',
        'return res': '块数 `{res}`',
    },
    cards=dict(
        one_liner='从左到右逐块分离：二分找出这块数值最后一次出现的位置',
        complexity='时间 `O(块数 × log n)`，空间 `O(1)`',
        problem=['有序（单调不减）数组 `nums` 只能通过 `size()` 和 `at(i)` 访问',
                 '相同数值连续出现形成数字块，求数字块的个数',
                 '本视频：`[1,1,2,2,2,2,3,3,3,3]` → `3`'],
        quote='对于最左侧的数字块，最开始可以确定的就是这个数字块中的数值是多少，也就是剩余数组中最左侧元素的数值。',
        quote_src='—— yiduobo 题解原文',
        idea=['块的数值 `v` = 剩余数组最左侧元素',
              '数组单调不减 → `v` 的最后一个下标可以二分：`nums[mid] == v` 往右找，否则往左',
              '分离掉这一块，`p = left + 1`，对剩下的重复，直到分离完'],
        summary=['时间：块数 × `O(log n)`；空间 `O(1)`',
                 '原文为 Python 2 风格，其中 `(left + right + 1) // 2` 已是整除写法，代码无需改动',
                 '`left = mid` 的二分要用上中位数 `+1`，否则 `left+1==right` 时死循环',
                 '对比灵神：灵神直接二分「第一个不等于 cur」的位置跳到下一块，yiduobo 二分块尾再 +1'],
    ),
)
