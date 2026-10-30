CONFIG = dict(
    num=3759, title='统计合格元素的数目', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='降序排序 + 找第一个严格变小的位置',
    code='''
class Solution(object):
    def countElements(self, nums, k):
        
        nums.sort(reverse=True)
        pre = nums[0] + 1
        for index, v in enumerate(nums):
            if v < pre:
                if index >= k:
                    return len(nums) - index
        
            pre = v

        return 0
''',
    call='Solution().countElements([5,7,5,2,9,4], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（降序）', h=200, cell=90, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if S.get('_line') == 9 and i >= S.get('index', 99) else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i < S['index']),
        dict(type='text', size=28, h=70, fn=lambda S: (f"前面 `index = {S['index']}` 个元素都 ≥ 当前值；要求至少 `k = {S['k']}` 个严格更大" if 'index' in S else '')),
    ],
    watch=['k', ('index', 'index', 'blue'), ('v', 'v', 'yellow'), ('pre', 'pre', 'pink')],
    captions={
        'nums.sort': '从大到小排序：`{nums}`。合格元素 = 排除掉前 `k` 大之后、且严格小于它们的元素',
        'pre = nums[0]': '`pre` 记“上一个元素”，初值取 `nums[0] + 1 = {pre}`，保证第一个元素一定“比 pre 小”',
        'for index': '看第 `{index}` 个元素 `v = {v}`',
        'if v < pre': lambda S, B, r: (f'`v = {S.v} < pre = {S.pre}`：严格变小 → 前面 `{S.index}` 个元素都严格大于它' if S.v < S.pre
                                       else f'`v = {S.v}` 和前一个 `{S.pre}` 相同：它前面并没有 `{S.index}` 个“严格更大”的 → 继续往后'),
        'if index >= k': lambda S, B, r: (f'`index = {S.index} >= k = {S.k}`：至少 k 个元素严格更大 → ==从这里起全是合格元素==' if S.index >= S.k
                                          else f'`index = {S.index} < k = {S.k}`：严格更大的元素还不够 k 个 → 继续'),
        'return len': '合格元素是 nums[{index}:] 共 `{len(nums)} − {index}` = =={ret}== 个',
        'pre = v': '`pre = {pre}`，留给下一个元素比较',
        'return 0': '遍历完也没有 → 没有合格元素，返回 0',
    },
    cards=dict(
        one_liner='降序排好，找第一个“严格变小且下标 ≥ k”的位置',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['元素 `x` 合格：`nums` 里至少有 `k` 个元素严格大于 `x`',
                 '返回合格元素的个数',
                 '本视频：`nums = [5,7,5,2,9,4]`，`k = 3` → `2`'],
        quote='题目实际上就是要从nums中排除掉前k大的元素，因此在这里可以先将nums按从大到小的顺序排序，接下来一趟遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['降序后，`nums[index]` 前面有 `index` 个元素',
              '只有当 `nums[index]` ==严格小于== 前一个元素时，前 `index` 个才都严格更大',
              '此时若 `index >= k`，从它开始到末尾全部合格，答案 `len(nums) - index`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`（不计排序栈）',
                 '易错：相同的值不能算“更大”，所以要用 `v < pre` 而不是直接 `index >= k`',
                 '`k = 0` 时第一个元素就满足 index >= k，答案是整个数组长度',
                 '对比灵神：灵神升序排序后用 `bisect_left` 一步定位“小于第 k 大”的个数'],
    ),
)
