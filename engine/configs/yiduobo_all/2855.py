def _seg(S, i, v):
    p = S.get('p')
    if p is None or p == -1:
        return None
    return 'blue' if i < p else 'pink'


def _txt(S):
    if 'n' not in S:
        return ''
    p, n = S.get('p'), S['n']
    if p is None:
        return ''
    if p == -1:
        return '还没找到下降处 `p`'
    return f'下降处 `p = {p}`：左段 `nums[0..{p - 1}]`，右段 `nums[{p}..{n - 1}]`，右段长 `n − p = {n - p}`'


CONFIG = dict(
    num=2855, title='使数组成为递增数组的最少右移次数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='找下降点 p + 首尾比较',
    code='''
class Solution(object):
    def minimumRightShifts(self, nums):

        p = -1
        n = len(nums)
        for i in range(1, n):
            if nums[i] < nums[i - 1]:
                p = i
                break
        
        if p == -1:
            return 0
        
        for i in range(p + 1, n):
            if nums[i] < nums[i - 1]:
                return -1
        
        if nums[0] > nums[-1]:
            return n - p
        
        return -1
''',
    call='Solution().minimumRightShifts([3,4,5,1,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, color=_seg, h=300),
        dict(type='text', fn=_txt, h=70),
    ],
    watch=['p', 'n', 'i'],
    captions={
        'p = -1': '`p` 记录第一个满足 `nums[p] < nums[p-1]` 的下标，先设 `-1` 表示没找到',
        'for i in range(1, n)': '扫描 `i = {i}`，找第一处下降',
        'if nums[i] < nums[i - 1]': lambda S, B, r: (
            f'`nums[{S.i}] = {S.nums[S.i]}` < `nums[{S.i - 1}] = {S.nums[S.i - 1]}`：下降了，这就是断点'
            if S.nums[S.i] < S.nums[S.i - 1] else f'`{S.nums[S.i]}` > `{S.nums[S.i - 1]}`：还在递增，继续'),
        'p = i': '第一个下降处 `p = {p}`：`nums[{p}..]` 就是要搬到最前面的那部分',
        'if p == -1': '`p == -1`？→ {"没有下降，本来就递增，返回 0" if p == -1 else "有下降，继续检查后半段"}',
        'for i in range(p + 1, n)': lambda S, B, r: ('`p` 之后的下标都检查完，没有再下降' if B.get('i') == S.i else f'检查 `p` 之后也必须递增：当前 `i = {S.i}`'),
        'return -1': '`-1`：后半段又出现下降（或首尾不满足），无法拼成递增',
        'if nums[0] > nums[-1]': '右段最后一个元素要小于左段第一个：`nums[0] = {nums[0]}` vs `nums[-1] = {nums[-1]}` → {"成立，可拼成递增" if nums[0] > nums[-1] else "不成立 → -1"}',
        'return n - p': '右移的元素个数就是 `n - p` = `{n} - {p}` = =={ret}==',
    },
    cards=dict(
        one_liner='原数组 = 两段递增拼成，且首元素大于尾元素',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 元素互不相同，一次右移把下标 `i` 的元素移到 `(i+1) % n`',
                 '求让数组变成递增的最少右移次数，不可能则返回 `-1`',
                 '示例：`[3,4,5,1,2]` → `2`'],
        quote='原数组由两个单调递增的数组拼成，同时原数组的最左侧的元素要大于最右侧的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['右移 k 次：末尾 k 个元素原样搬到最前，未移动的部分顺序不变',
              '所以两部分各自必须递增，且右段末尾 < 左段开头',
              '一趟遍历找第一个下降下标 `p`，答案就是 `n - p`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：没有下降点（`p == -1`）答案是 0，不是 -1',
                 '`p` 之后若再出现下降，说明至少三段，返回 -1',
                 '原文为 Python 2 风格，代码逐字保留，只删去了空行里的说明',
                 '对比灵神：灵神用 while 先后扫两段并记 mid；这里用 for 找下降点 p，再单独检查后半段'],
    ),
)
