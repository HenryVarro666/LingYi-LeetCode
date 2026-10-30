CONFIG = dict(
    num=2460, title='对数组执行操作', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='先模拟再把非零前移', tags=['灵神题单'],
    code='''
class Solution(object):
    def applyOperations(self, nums):

        n = len(nums)
        for index in range(n - 1):
            if nums[index] == nums[index + 1]:
                nums[index] += nums[index]
                nums[index + 1] = 0
        
        p = 0
        for index in range(n):
            if nums[index] == 0 and p < n:
                if p <= index:
                    p = index + 1
                while p < n and nums[p] == 0:
                    p += 1
                
                if p < n:
                    nums[index], nums[p] = nums[p], nums[index]
                    p += 1
        
        return nums
''',
    call='Solution().applyOperations([1,2,2,1,1,3,0])',
    expect=[1, 4, 2, 3, 0, 0, 0],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, h=300,
             label='nums（蓝 index = 当前位置，粉 p = 往后找的非零数）',
             dim=lambda S, k, v: v == 0),
        dict(type='text', size=26, fn=lambda S: ('第一趟：按题意翻倍并清零' if S['_line'] <= 9 else '第二趟：遇到 0，就从后面找最近的非零数换过来')),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'for index in range(n - 1)': lambda S, B, r: (f'第一趟，第 `{S.index}` 步操作：比较 `nums[{S.index}]` 与 `nums[{S.index + 1}]`' if S.index != B.get('index') else '第一趟结束：翻倍和清零都做完了'),
        'if nums[index] == nums[index + 1]': lambda S, B, r: (f'`{S.nums[S.index]} == {S.nums[S.index + 1]}` → 相等，要翻倍' if S.nums[S.index] == S.nums[S.index + 1] else f'`{S.nums[S.index]} != {S.nums[S.index + 1]}` → 不相等，跳过'),
        'nums[index] += nums[index]': '`nums[{index}]` 翻倍成 =={nums[index]}==',
        'nums[index + 1] = 0': '后一个变成 0',
        'p = 0': '第二趟：`p` 是往后找非零数的指针',
        'for index in range(n)': lambda S, B, r: (f'第二趟，看位置 `{S.index}`' if S.index != B.get('index') or B.get('p') is None else '第二趟结束'),
        'if nums[index] == 0 and p < n': lambda S, B, r: (f'`nums[{S.index}] = 0` 是空位，需要从后面找个非零数填进来' if S.nums[S.index] == 0 and S.p < S.n else (f'`nums[{S.index}] = {S.nums[S.index]}` 已是非零，不动' if S.nums[S.index] else '`p` 已走出数组，后面没有非零数可换，剩下的就是 0')),
        'if p <= index': lambda S, B, r: ('`p` 落后于当前位置，只能从 `index + 1` 开始找' if S.p <= S.index else '`p` 已在 `index` 后面，直接用'),
        'p = index + 1': '`p` → {p}',
        'while p < n and nums[p] == 0': lambda S, B, r: (f'`nums[{S.p}] = 0` 还是 0 → `p` 继续往后' if S.p < S.n and S.nums[S.p] == 0 else (f'`nums[{S.p}] = {S.nums[S.p]}` 非零 → `p` 停在这里' if S.p < S.n else '`p` 走到末尾，后面没有非零数了')),
        'p += 1': lambda S, B, r: f'`p` → {S.p}',
        'if p < n': lambda S, B, r: (f'`p = {S.p}` 还在数组内，找到了可换的非零数' if S.p < S.n else '`p` 走出数组：后面全是 0，不用换'),
        'nums[index], nums[p] =': '把非零数换到空位上：`nums[{index}]` 和 `nums[{p}]` 互换',
        'return nums': '非零在前、0 在后：`{nums}`',
    },
    cards=dict(
        one_liner='先照题意模拟翻倍清零，再把 0 逐个换到后面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['依次对每个 `i`：若 `nums[i] == nums[i+1]`，`nums[i]` 翻倍，`nums[i+1]` 置 0',
                 '全部操作完后，把所有 0 移到末尾',
                 '示例：`[1,2,2,1,1,0]` → `[1,4,2,0,0,0]`'],
        quote='首先一趟遍历，按照题目的要求完成翻倍和清零操作，接下来再一趟遍历，将所有非零的值移动到数组靠前的位置即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：照题意模拟，相等就翻倍并清零',
              '第二趟：遇到 0，用 `p` 往后找最近的非零数',
              '找到就交换，`p` 只增不减，整体仍是线性'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '第一趟要从左到右依次做，翻倍后的值可能影响下一个比较',
                 '`p` 要保证在 `index` 后面：`p <= index` 时先拨到 `index + 1`',
                 '对比灵神：灵神一趟合并边写前面，这里分成「模拟」「搬 0」两趟'],
    ),
)
