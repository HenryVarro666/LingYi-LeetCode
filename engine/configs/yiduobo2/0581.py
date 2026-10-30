NUMS = [2, 6, 4, 8, 10, 9, 15]


def _bar_color(S, i, v):
    if i == S.get('index') and S.get('_line') not in (21, 22, 24):
        return 'yellow'
    if i in (S.get('stack') or []) and S.get('_line') not in (21, 22, 24):
        return 'purple'
    lo, hi = S.get('left'), S.get('right')
    if S.get('_line', 0) >= 21 and lo is not None and hi is not None and lo <= i <= hi:
        return 'orange'
    return None


def _text(S):
    ln = S.get('_line', 0)
    if ln >= 21:
        return f"答案区间 `[left, right] = [{S.get('left')}, {S.get('right')}]`：把这段排好序，整个数组就有序"
    if ln >= 12:
        return '第二趟（从右往左）：栈底→栈顶==值不增==；遇到更大的数，栈顶和它是逆序对 → 更新==最右==的位置 `right`'
    return '第一趟（从左往右）：栈底→栈顶==值不减==；遇到更小的数，栈顶和它是逆序对 → 更新==最左==的位置 `left`'


def _cap_while1(S, B, ret):
    st, i, n = B.stack, B.index, B.nums
    if not st:
        return '栈空了 → 停止弹栈'
    j = st[-1]
    if n[j] > n[i]:
        return f'`nums[{i}] = {n[i]}` 比栈顶 `nums[{j}] = {n[j]}` 小：==逆序对== `({j}, {i})` → 下标 {j} 必在答案里'
    return f'`nums[{i}] = {n[i]}` ≥ 栈顶 `nums[{j}] = {n[j]}`：栈里没有能和它构成逆序对的了 → 停'


def _cap_while2(S, B, ret):
    st, i, n = B.stack, B.index, B.nums
    if not st:
        return '栈空了 → 停止弹栈'
    j = st[-1]
    if n[j] < n[i]:
        return f'`nums[{i}] = {n[i]}` 比栈顶 `nums[{j}] = {n[j]}` 大：==逆序对== `({i}, {j})` → 下标 {j} 必在答案里'
    return f'`nums[{i}] = {n[i]}` ≤ 栈顶 `nums[{j}] = {n[j]}`：没有逆序对了 → 停'


def _cap_if_left(S, B, ret):
    j = B.stack[-1]
    if B.left is None:
        return f'`left` 还是 `None` → 记下 {j}'
    if B.left > j:
        return f'`{j}` 比当前 `left = {B.left}` 更靠左 → 更新'
    return f'`{j}` 不比 `left = {B.left}` 更靠左，不更新'


def _cap_if_right(S, B, ret):
    j = B.stack[-1]
    if B.right is None:
        return f'`right` 还是 `None` → 记下 {j}'
    if B.right < j:
        return f'`{j}` 比当前 `right = {B.right}` 更靠右 → 更新'
    return f'`{j}` 不比 `right = {B.right}` 更靠右，不更新'


CONFIG = dict(
    num=581, title='最短无序连续子数组', difficulty='Medium', category='栈',
    author='yiduobo', technique='两趟单调栈找最左/最右逆序对',
    tags=['热题173'],
    code='''
class Solution(object):
    def findUnsortedSubarray(self, nums):
        stack = [0]
        left = None
        for index in range(1, len(nums)):
            while stack and nums[stack[-1]] > nums[index]:
                if left is None or left > stack[-1]:
                    left = stack[-1]
                stack.pop()
            stack.append(index)

        stack = [len(nums) - 1]
        right = None
        for index in range(len(nums) - 2, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                if right is None or right < stack[-1]:
                    right = stack[-1]
                stack.pop()
            stack.append(index)

        if left is None:
            return 0
        else:
            return right - left + 1
''',
    call=f'Solution().findUnsortedSubarray({NUMS})',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=96, size=25),
        dict(type='bars', var='nums', label='nums（黄 = index，紫 = 栈中下标，橙 = 答案区间）', h=380, vmax=16,
             pointers={'index': 'yellow', 'left': 'green', 'right': 'pink'}, color=_bar_color),
        dict(type='stack', var='stack', label='stack（存下标 i:值）', fmt=lambda i: f'{i}:{NUMS[i]}', h=120),
    ],
    watch=[('index', 'index', 'yellow'), ('stack', 'stack', 'purple'), ('left', 'left', 'green'), ('right', 'right', 'pink')],
    captions={
        'stack = [0]': '第一趟从左往右：先把下标 0 放进栈',
        'left = None': '`left`：所有逆序对里==最左边==那个数的下标',
        'for index in range(1,': lambda S, B, r: (f"看 `nums[{S.index}] = {S.nums[S.index]}`" if B.get('index') != S.index
                                                  else '第一趟扫描结束'),
        'while stack and nums[stack[-1]] > nums[index]': _cap_while1,
        'if left is None or': _cap_if_left,
        'left = stack[-1]': '`left = {left}`',
        'stack = [len(nums) - 1]': '第二趟从右往左找==最右==的逆序对位置：先放入最后一个下标 `{stack[0]}`',
        'right = None': '`right`：所有逆序对里==最右边==那个数的下标',
        'for index in range(len(nums) - 2': lambda S, B, r: (f"看 `nums[{S.index}] = {S.nums[S.index]}`"
                                                             if B.get('index') != S.index else '第二趟扫描结束'),
        'while stack and nums[stack[-1]] < nums[index]': _cap_while2,
        'if right is None or': _cap_if_right,
        'right = stack[-1]': '`right = {right}`',
        'stack.pop()': '弹出 `{B.stack[-1]}`，继续看栈里更早的元素',
        'stack.append(index)': lambda S, B, r: (f'`{S.index}` 入栈，留给后面的元素比较（栈底→栈顶'
                                                + ('值不减）' if S['_line'] < 12 else '值不增）')),
        'if left is None:': '`left = {left}` 不是 `None` → 数组本来不是有序的',
        'return right - left + 1': '答案 `right − left + 1 = {right} − {left} + 1` = =={ret}==',
    },
    skip=['for index in range'],   # 当前看的是谁，在 while 的字幕里说
    max_steps=70,
    cards=dict(
        one_liner='答案必须盖住所有逆序对：找逆序对里最左和最右的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找一个==最短==的连续子数组，只要把它升序排序，整个数组就变成升序',
                 '返回它的长度；数组本来有序就返回 0',
                 '示例：`[2,6,4,8,10,9,15]` → `5`（排序 `[6,4,8,10,9]` 即可）'],
        quote='对于数组中的任意逆序对nums[i]，nums[j]，其中i < j，那么最终答案(x, y)必然要满足 `x <= i < j <= y`，否则nums[i]和nums[j]这一对逆序对就无法得到修正。',
        quote_src='—— yiduobo 题解原文',
        idea=['所以只要找到所有逆序对中==最左侧的数==和==最右侧的数==，这个区间就是答案',
              '找最左：单调栈从左往右扫，栈顶比当前大就是逆序对，用栈顶下标更新 `left`，并弹栈',
              '找最右：从右往左再扫一趟，大小关系反过来'],
        summary=['时间 `O(n)`（每个下标最多进出栈一次），空间 `O(n)`',
                 '易错：要==不断弹栈==，栈里更早的元素也可能和当前元素构成逆序对',
                 '易错：相等不算逆序对，弹栈条件是严格的 `>` / `<`',
                 '还有 `O(1)` 空间做法：从左往右维护最大值找右边界，从右往左维护最小值找左边界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
