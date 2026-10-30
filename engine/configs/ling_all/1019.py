VALS = [2, 7, 4, 3, 5]


def _info(S):
    h = S.get('head')
    st = S.get('st')
    if st is None:
        return ''
    if h is None:
        return f'链表走完：栈里剩下的下标 `{st}` 没有更大元素 → 置 0'
    top = f'栈顶 `{VALS[st[-1]]}`' if st else '栈为空'
    return f'当前节点 ==`{h.val}`==，{top}（栈内值从底到顶递减）'


CONFIG = dict(
    num=1019, title='链表中的下一个更大节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='单调栈（栈存下标，用当前值更新答案）',
    tags=['单调栈', '链表树与回溯', '难度分 1571'],
    code='''
class Solution:
    def nextLargerNodes(self, head: Optional[ListNode]) -> List[int]:
        ans = []
        st = []  # 单调栈（节点下标）
        while head:
            while st and ans[st[-1]] < head.val:
                ans[st.pop()] = head.val  # ans[st.pop()] 后面不会再访问到了
            st.append(len(ans))  # 当前 ans 的长度就是当前节点的下标
            ans.append(head.val)
            head = head.next
        for i in st:
            ans[i] = 0  # 没有下一个更大元素
        return ans
''',
    call='Solution().nextLargerNodes(L([2,7,4,3,5]))',
    expect=[7, 0, 5, 5, 0],
    views=[
        dict(type='text', fn=_info),
        dict(type='linked', label='链表（head 指向当前节点）', pointers={'head': 'blue'}, h=170),
        dict(type='array', var='ans', label='ans（先记节点值，被更大值更新后变成答案）', h=170,
             color=lambda S, i, v: 'green' if S.get('st') is not None and i not in S['st'] and S.get('head') is not None and i < len(S['ans']) - 1 else None),
        dict(type='stack', var='st', label='单调栈（下标:节点值，栈底到栈顶值递减）', fmt=lambda i: f'{i}:{VALS[i]}', h=260),
    ],
    watch=[('head', 'head.val if head else None', 'blue'), ('st', 'st', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'st = []': '栈里存==还没找到答案==的节点下标',
        'while st and ans[st[-1]] < head.val': lambda S, B, ret: (
            f'栈顶下标 `{S.st[-1]}` 的值 `{S.ans[S.st[-1]]}` < 当前 `{S.head.val}` → 当前节点就是它的下一个更大节点' if S.st and S.ans[S.st[-1]] < S.head.val
            else ('栈为空，没有等待答案的节点' if not S.st else f'栈顶值 `{S.ans[S.st[-1]]}` ≥ 当前 `{S.head.val}` → 不用弹，栈保持递减')),
        'ans[st.pop()] = head.val': '弹出栈顶下标，把答案==写成当前值 `{head.val}`==：`ans = {ans}`',
        'st.append(len(ans))': '当前节点下标 = `len(ans)` = `{len(ans)}`，它还在等更大的数 → 入栈',
        'ans.append(head.val)': '`ans` 先放节点值占位，等后面的更大值来覆盖',
        'head = head.next': '`head` 走到下一个节点',
        'for i in st': '遍历完了：栈里剩下的下标一直没人比它大',
        'ans[i] = 0': '下标 `{i}` 没有下一个更大节点 → ==置 0==',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='用每个数去更新栈里「还在等答案」的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['链表每个节点，找它右边==第一个严格更大==的节点值，没有就是 0',
                 '示例：`[2,1,5]` → `[5,5,0]`',
                 '本视频：`[2,7,4,3,5]` → `[7,0,5,5,0]`'],
        quote='把第 i 个节点的值记录到 ans[i]，这样栈中就可以只保存下标了。在循环结束后，栈中下标对应元素是没有下一个更大元素的，所以要把栈中的下标对应的 ans 置为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正向遍历，栈里的值从底到顶递减，都是「还没遇到更大数」的节点',
              '来了更大的数，就把栈顶一个个弹出并写上答案',
              '再把自己入栈；循环结束栈里剩下的置 0'],
        after=[dict(heading='灵神的另外两种写法', lines=['方法一：递归到链表尾，在「归」时从右往左做单调栈', '反转链表再倒着遍历，最后把答案反转', '方法二的第一版：栈里存（值，下标）二元组'])],
        summary=['每个元素最多入栈、出栈各一次，总时间 `O(n)`',
                 '比较是 ==严格大于==：`<` 而不是 `<=`，相等的数不会弹出',
                 '先弹栈再入栈；答案写入 `ans[i]` 后不会再被读到',
                 '循环结束后别忘了把栈里剩余下标置 0'],
    ),
)
