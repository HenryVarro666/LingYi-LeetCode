NUMS2 = [1, 3, 4, 2]
QP = 'len(nums2) - pos_dict[num]'


def _while(S, B, ret):
    st, i, a = B.stack, B.index, B.nums2
    if st and a[i] >= a[st[-1]]:
        if st[-1] == i:
            return f'栈顶就是初始化时压入的 `{i}` 自己：`{a[i]} ≥ {a[i]}` → 弹出'
        return (f'`nums2[{i}] = {a[i]} ≥ 栈顶值 {a[st[-1]]}`：栈顶位置更靠后、值又更小'
                f' → ==不可能再成为答案==，弹出')
    if st:
        return f'`{a[i]} < 栈顶值 {a[st[-1]]}`：停止弹栈，栈顶就是它的下一个更大元素'
    return '栈已经空了，停止弹栈'


def _if(S, B, ret):
    if S.stack:
        return f'栈不空 → `nums2[{S.index}] = {S.nums2[S.index]}` 的答案是栈顶的值 `{S.nums2[S.stack[-1]]}`'
    return f'栈为空 → 右边没有比 `{S.nums2[S.index]}` 大的数，答案 `-1`'


def _show(S):
    if 'num' in S and 'pos_dict' in S and S['num'] in S['pos_dict']:
        n, p = len(S['nums2']), S['pos_dict'][S['num']]
        return f'查询 `{S["num"]}`：位置 `{p}` → `pos_list[{n} − {p}] = pos_list[{n - p}]` = =={S["pos_list"][n - p]}=='
    if 'index' in S:
        return f'从后往前扫描，栈里存==可能成为答案==的下标（从底到顶值递减）'
    return '先在 nums2 上求出每个元素的下一个更大元素，再回答 nums1'


CONFIG = dict(
    num=496, title='下一个更大元素 I', difficulty='Easy', category='单调栈',
    author='yiduobo', technique='单调栈 · 从后往前扫描',
    tags=['labuladong', '灵神题单·单调栈'],
    code='''
class Solution(object):
    def nextGreaterElement(self, nums1, nums2):

        if not nums2:
            return [-1] * len(nums1)

        if not nums1:
            return []

        stack = [len(nums2) - 1]
        pos_list = [-1]
        pos_dict = {nums2[-1] : len(nums2) - 1}
        for index in range(len(nums2) - 1, -1, -1):
            while stack and nums2[index] >= nums2[stack[-1]]:
                stack.pop()
            if stack:
                pos_list.append(nums2[stack[-1]])
            else:
                pos_list.append(-1)
            stack.append(index)
            pos_dict[nums2[index]] = index

        res = []
        for num in nums1:
            if num not in pos_dict:
                res.append(-1)
            else:
                res.append(pos_list[len(nums2) - pos_dict[num]])

        return res
''',
    call=f'Solution().nextGreaterElement([4, 1, 2], {NUMS2})',
    expect=[-1, 3, -1],
    views=[
        dict(type='array', var='nums2', label='nums2（蓝 = 当前 index，紫 = 在栈里，粉 = 查询的位置）', cell=80,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('pink' if i == S['pos_dict'].get(S['num']) else None) if 'num' in S
             else ('blue' if i == S.get('index') else ('purple' if i in (S.get('stack') or []) else None))),
        dict(type='stack', var='stack', label='stack（存下标  下标:值）', fmt=lambda i: f'{i}:{NUMS2[i]}', h=105, font=28),
        dict(type='array', var='pos_list', label='pos_list（倒序：pos_list[k] 是 nums2[len−k] 的答案）', cell=80,
             pointers={QP: 'pink'}, pointer_labels={QP: 'len − pos'},
             dim=lambda S, i, v: i == 0),
        dict(type='map', var='pos_dict', label='pos_dict（值 → 在 nums2 中的位置）', fmt=lambda k, v: f'{k} → {v}', h=90, font=22),
        dict(type='text', fn=_show, size=26, h=56),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'purple'), ('num', 'num', 'pink'), ('res', 'res', 'green')],
    captions={
        'if not nums2': '特判：`nums2` 不为空，继续',
        'if not nums1': '特判：`nums1` 不为空，继续',
        'stack = [': '最后一个元素右边没有元素：先把它的下标 `{stack[0]}` 压栈',
        'pos_list = [-1]': '`pos_list` 倒着记录答案，先放一个 `-1`',
        'pos_dict = {': '`pos_dict`：记录每个值在 nums2 中的位置',
        'for index in range': lambda S, B, ret: (f'从后往前扫描：`index = {S.index}`，当前元素 `{S.nums2[S.index]}`'
                                                 if 'index' not in B or B.index != S.index else '扫描结束'),
        'while stack and': _while,
        'stack.pop()': '弹出下标 `{B.stack[-1]}`',
        'if stack:': _if,
        'pos_list.append(nums2[stack[-1]])': '`pos_list` 追加 `{pos_list[-1]}`',
        'pos_list.append(-1)': '`pos_list` 追加 `-1`',
        'stack.append(index)': '当前下标 `{index}` 压栈：它可能成为==左边元素==的答案',
        'pos_dict[nums2[index]] = index': '记录位置 `pos_dict[{nums2[index]}] = {index}`',
        'res = []': 'nums2 处理完毕，开始回答 nums1 的查询',
        'for num in nums1': lambda S, B, ret: (f'查询 `num = {S.num}`' if 'num' not in B or B.num != S.num else '查询结束'),
        'if num not in pos_dict': '`{num}` 在 nums2 中的位置是 `pos_dict[{num}] = {pos_dict[num]}`',
        'res.append(pos_list[': '倒序换算：`pos_list[{len(nums2)} − {pos_dict[num]}]` = =={res[-1]}==',
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='先在 nums2 上用单调栈求出所有答案，nums1 只是查表',
        complexity='时间 `O(n + m)`，空间 `O(m)`',
        problem=['`nums1` 是 `nums2` 的子集，元素互不相同',
                 '对 `nums1` 每个数，求它在 `nums2` 中==右侧第一个更大的数==，没有则 `-1`',
                 '示例：`nums1 = [4,1,2]`，`nums2 = [1,3,4,2]` → `[-1,3,-1]`'],
        quote='若当前元素大于栈顶元素，那么此时的栈顶元素位置比当前元素更靠后，且值更小，说明==栈顶元素不可能再成为答案==，应当将其弹出。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 dict 保存位置后，问题就变成：==对 nums2 求每个元素的下一个更大元素==',
              '从后往前扫，栈里存可能成为答案的数；弹完后栈顶就是答案，栈空则 `-1`',
              '答案按扫描顺序（倒序）存进 `pos_list`，查询时用 `len − 位置` 换算'],
        summary=['时间 `O(n + m)`：每个下标最多入栈、出栈各一次',
                 '弹栈条件是 `>=`：相等的也不可能成为答案',
                 '初始化压入的最后一个下标会在第一轮被自己弹出，`pos_list[0]` 只是占位',
                 '`pos_list` 是倒序的，下标要换算成 `len(nums2) − pos`',
                 '原文代码可直接在 Python 3 运行，未做修改'],
    ),
)
