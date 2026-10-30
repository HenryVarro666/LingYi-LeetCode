CONFIG = dict(
    num=1150, title='检查一个数是否在数组中占绝大多数', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='二分找首次出现 · 再看 left+n//2',
    tags=['二分查找', '有序数组'],
    code='''
class Solution(object):
    def isMajorityElement(self, nums, target):

        if target < nums[0]:
            return False
        
        n = len(nums)
        left = 0
        right = n - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] >= target:
                right = mid
            else:
                left = mid + 1
        
        if nums[left] != target:
            return False
        
        if left + n // 2 < len(nums) and nums[left + n // 2] == target:
            return True
        
        return False
''',
    call='Solution().isMajorityElement([2,4,5,5,5,5,5,6,6], 5)',
    expect=True,
    views=[
        dict(type='text', size=26, fn=lambda S: (
            f"区间 `[{S['left']}, {S['right']}]`：找最小的 `>= {S['target']}` 的下标" if 'right' in S and 'left' in S and S['left'] < S['right'] else
            (f"首次出现 `left = {S['left']}`，再看 `nums[{S['left']} + {S['n'] // 2}]`" if 'left' in S and 'right' in S else ''))),
        dict(type='array', var='nums', h=330, pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             window=('left', 'right'),
             color=lambda S, i, v: 'green' if v == S['target'] else None,
             dim=lambda S, i, v: 'right' in S and 'left' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('target', 'target'), ('n', 'n'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'if target < nums[0]': '`target = {target}` < 最小值 `{nums[0]}`？不成立，target 还有可能出现',
        'right = n - 1': '二分范围 `[0, {right}]`：目标是==最小的 `>= target` 的下标==',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`，区间还没缩成一个点，继续' if S.left < S.right
                                                else f'`left = right = {S.left}`：二分结束，`left` 就是首个 `>= target` 的位置'),
        'mid = (left + right)': '取中点 `mid = ({left} + {right}) // 2 = {mid}`',
        'if nums[mid] >= target': lambda S, B, r: (f'`nums[{S.mid}] = {S.nums[S.mid]} >= {S.target}` → 成立：mid 可能就是首个，==保留 mid=='
                                                    if S.nums[S.mid] >= S.target else
                                                    f'`nums[{S.mid}] = {S.nums[S.mid]} < {S.target}` → mid 及左边都太小，==丢掉=='),
        'right = mid': '`right = mid = {right}`：右边界收到 mid（mid 仍可能是答案）',
        'left = mid + 1': '`left = mid + 1 = {left}`：左边界跳过 mid',
        'if nums[left] != target': lambda S, B, r: (f'`nums[{S.left}] = {S.nums[S.left]}` ≠ `{S.target}` → 数组里根本没有 target'
                                                     if S.nums[S.left] != S.target else
                                                     f'`nums[{S.left}] = {S.nums[S.left]}` == target：{S.left} 是 target 首次出现的位置'),
        'if left + n // 2': lambda S, B, r: (f'从首位往后数 `n // 2 = {S.n // 2}` 位 → 下标 `{S.left + S.n // 2}`；若它还是 target，则个数 `> n // 2`'
                                             if S.left + S.n // 2 < len(S.nums) else
                                             f'下标 `{S.left + S.n // 2}` 越界：target 个数不足一半 → False'),
        'return True': '`nums[{left + n // 2}]` 依然是 target：target 出现超过一半 → ==True==',
        'return False': '不满足 → ==False==',
    },
    cards=dict(
        one_liner='有序数组：找首次出现的位置，再往后跳 n//2 看是不是还等于它',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['有序数组 `nums` 和整数 `target`，判断 target 是否出现超过 `n/2` 次',
                 '示例：`[2,4,5,5,5,5,5,6,6]`，`target = 5` → `True`（出现 5 次，n = 9）'],
        quote='只需找出其首次出现的下标left，然后判断从left往后数数组长度一半加1的下标是否依然是target就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历计数也行，但数组有序 → ==二分==能更快',
              '不必找最后一次出现：从首次下标 `left` 往后数 `n // 2`，还是 target 就说明个数 `> n // 2`',
              '可能没有 target，所以二分求的是==最小的 `>= target`==，再检查 `nums[left] == target`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '先判 `nums[left] != target`（不存在），再判 `left + n // 2` 是否越界',
                 '二分条件是 `nums[mid] >= target` → `right = mid`，否则 `left = mid + 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
