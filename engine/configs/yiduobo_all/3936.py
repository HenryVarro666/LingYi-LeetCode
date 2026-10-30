CONFIG = dict(
    num=3936, title='将 0 移到末尾的最少交换次数', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='从后往前 · 与最左侧的 0 交换',
    tags=['难度分 1346'],
    code='''
class Solution(object):
    def minimumSwaps(self, nums):
        
        p = 0
        res = 0
        for index in range(len(nums) - 1, -1, -1):
            if nums[index] != 0:
                while p < index and nums[p] != 0:
                    p += 1
                if p == index:
                    break
                res += 1
                nums[p] = nums[index]
        
        return res
''',
    call='Solution().minimumSwaps([0,1,0,3,12])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"`p` 指向最左侧的 0（或追上 `index`）；已交换 `{S['res']}` 次" if 'res' in S and 'p' in S else ''), size=28),
        dict(type='array', var='nums', pointers={'p': 'green', 'index': 'orange'}, h=300,
             color=lambda S, i, v: ('green' if i == S['p'] else 'orange' if i == S.get('index') else None) if 'p' in S else None),
    ],
    watch=[('p', 'p', 'green'), ('index', 'index', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计交换次数',
        'p = 0': '`p` 记录最左侧 0 的位置（还没找，先从 0 开始）',
        'for index in range': lambda S, B, r: (f"从后往前，`index` = {S.index}，当前元素 `{S.nums[S.index]}`" if B.get('index') != S.index else '遍历结束'),
        'if nums[index] != 0': lambda S, B, r: (f"`nums[{S.index}] = {S.nums[S.index]}` 非 0 → 它应该排在前面，要和左侧的 0 换" if S.nums[S.index] != 0 else f"`nums[{S.index}] = 0` 已经在末尾一侧，不用动"),
        'while p < index': lambda S, B, r: (f"`p = {S.p}`：`nums[{S.p}] = {S.nums[S.p]}` 非 0 → p 右移找 0" if S.p < S.index and S.nums[S.p] != 0 else f"`p = {S.p}` 已指向 0 或追上 `index`，停"),
        'p += 1': '`p` → {p}',
        'if p == index': lambda S, B, r: (f"`p == index = {S.index}`：index 左侧已经没有 0 → 完成，退出" if S.p == S.index else f"`p = {S.p} < index = {S.index}`：左侧还有 0，可以交换"),
        'break': '左边全是非 0，提前结束',
        'res += 1': '这次交换要花 1 步：`res` → {res}',
        'nums[p] = nums[index]': '把 `nums[{index}]` = {nums[index]} 放到最左侧 0 的位置 `p = {p}`（`index` 位置反正马上被越过，不用补 0）',
        'return res': '最少交换次数 `{res}`',
    },
    cards=dict(
        one_liner='从后往前，让每个非 0 元素去换最左侧的 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每步可交换任意两个下标的元素，求把所有 0 移到数组末尾的最少交换次数',
                 '示例：`[0,1,0,3,12]` → `2`',
                 '本视频用同一个示例'],
        quote='从后往前一趟遍历，每碰到一个非0的元素，就让其与最左侧的0进行交换，直到其左侧不存在0为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['为什么选最左侧的 0：右侧的 0 可能已经在正确位置',
              '例如 `[0,0,1]`：换最左 0 一步到位；换右边 0 要两步',
              '`p` 单调右移，`index` 单调左移，相遇就结束'],
        summary=['时间 `O(n)`，空间 `O(1)`（`p` 只会右移）',
                 '`p == index` 时必须 break：左侧已经没有 0',
                 '原文只写了 `nums[p] = nums[index]`，没有把 `index` 处写成 0；因为之后不会再用到，所以不影响答案',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
