NUMS1 = [4, 1, 2, 3]
NUMS2 = [4, 1, 2, 6, 3]
XI = 'nums2.index(x)'


def _xi(S):
    return S['nums2'].index(S['x']) if 'x' in S and 'nums2' in S else -1


def _while(S, B, ret):
    st, x = B.st, B.x
    if st and x > st[-1]:
        return f'`x = {x} > 栈顶 {st[-1]}`：==栈顶等到了比它大的数== → 它的答案就是 `{x}`'
    if st:
        return f'`x = {x} < 栈顶 {st[-1]}`：栈顶还没等到更大的数，停止弹栈'
    return '栈为空：没有待办的数，不用弹栈'


def _in(S, B, ret):
    if S.x in S.idx:
        return f'`{S.x}` 在 nums1 中（`idx[{S.x}] = {S.idx[S.x]}`）→ 它也要找下一个更大元素，==入栈等待=='
    return f'`{S.x}` 不在 nums1 中 → 没人问它的答案，==不入栈=='


def _show(S):
    if 'x' not in S:
        return '栈 = 还没算出「下一个更大元素」的 nums1 元素（todolist）'
    ln = S.get('_line')
    st = S.get('st') or []
    if ln == 10:
        return f'`{S["x"]}` 是刚弹出元素的下一个更大元素，==写进 ans=='
    if st:
        return f'栈中元素从底到顶==递减==：`{st}`，都在等一个更大的数'
    return '栈为空：之前的元素都已经找到答案'


CONFIG = dict(
    num=496, title='下一个更大元素 I', difficulty='Easy', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 从左到右（栈 = todolist）',
    tags=['labuladong', '灵神题单·单调栈'],
    code='''
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        idx = {x: i for i, x in enumerate(nums1)}
        ans = [-1] * len(nums1)
        st = []
        for x in nums2:
            while st and x > st[-1]:
                # x 是栈顶的下一个更大元素
                # 既然栈顶已经算出答案，弹出
                ans[idx[st.pop()]] = x  # 记录答案
            if x in idx:  # x 在 nums1 中
                st.append(x)  # 只需把在 nums1 中的元素入栈
        return ans
''',
    call=f'Solution().nextGreaterElement({NUMS1}, {NUMS2})',
    expect=[6, 2, 6, -1],
    views=[
        dict(type='array', var='nums2', label='nums2（蓝 = 当前 x，紫 = 在栈里等答案）', cell=96,
             pointers={XI: 'blue'}, pointer_labels={XI: 'x'},
             dim=lambda S, i, v: 'x' in S and i < _xi(S) and v not in (S.get('st') or []),
             color=lambda S, i, v: 'blue' if i == _xi(S) else ('purple' if v in (S.get('st') or []) else None)),
        dict(type='array', var='nums1', label='nums1（下标就是 idx 里的值）', cell=96),
        dict(type='array', var='ans', label='ans（与 nums1 一一对应）', cell=96,
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='stack', var='st', label='st（todolist）', h=125, font=30),
        dict(type='text', fn=_show, size=26, h=70),
    ],
    watch=[('x', 'x', 'blue'), ('st', 'st', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'idx = {': '哈希表 `idx`：nums1 的==值 → 下标==，算出答案后写回 `ans` 的对应位置',
        'ans = [-1]': '`ans` 先全填 `-1`：找不到下一个更大元素的就保持 `-1`',
        'st = []': '栈 `st` 当 todolist：存==还没算出答案==的数',
        'for x in nums2': lambda S, B, ret: (f'从左到右遍历 nums2：`x = {S.x}`' if 'x' not in B or B.x != S.x
                                             else '遍历结束'),
        'while st and x > st[-1]': _while,
        'ans[idx[st.pop()]] = x': lambda S, B, ret: (f'弹出栈顶 `{B.st[-1]}`，它在 nums1 的下标是 `{S.idx[B.st[-1]]}`'
                                                     f' → `ans[{S.idx[B.st[-1]]}] = {S.x}`'),
        'if x in idx': _in,
        'st.append(x)': '`{x}` 入栈，等待它右边第一个比它大的数',
        'return ans': '栈里剩下的数右边没有更大元素，答案保持 `-1` → 返回 =={ans}==',
    },
    cards=dict(
        one_liner='栈是 todolist：遇到更大的数，就把栈顶的答案填上',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`nums1` 是 `nums2` 的子集，元素互不相同',
                 '对 `nums1` 每个数 `x`：找它在 `nums2` 中==右侧第一个比它大==的数，没有则 `-1`',
                 '示例：`nums1 = [4,1,2]`，`nums2 = [1,3,4,2]` → `[-1,3,-1]`',
                 '本视频：`nums1 = [4,1,2,3]`，`nums2 = [4,1,2,6,3]` → `[6,2,6,-1]`'],
        quote='栈中记录还没算出「下一个更大元素」的那些数。可以把栈视作一个 todolist。只要遍历到比栈顶元素更大的数，就意味着栈顶元素找到了答案，记录答案，并弹出栈顶。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['先用哈希表 `idx` 记下 nums1 每个数的下标，答案才能写回原位',
              '从左到右扫 nums2：`x` 比栈顶大，栈顶的答案就是 `x`，弹出',
              '==只把 nums1 中的数入栈==，栈的大小不超过 `n`'],
        summary=['时间 `O(n + m)`：每个数最多入栈、出栈各一次',
                 '空间 `O(n)`：只有 nums1 的数入栈，比「从右到左」写法更省',
                 '栈从底到顶递减；元素互不相同，所以用 `>` 即可',
                 '另一种写法：从右到左遍历，栈里存「下一个更大元素」的候选项'],
    ),
)
