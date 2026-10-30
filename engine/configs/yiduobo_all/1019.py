VALS = [2, 7, 4, 3, 5]


def _info(S):
    n = S.get('now')
    st = S.get('stack')
    if st is None:
        return ''
    if n is None:
        return f'链表走完：栈里剩下的位置 `{[p for _, p in st]}` 找不到答案，保持 0'
    top = f'栈顶 `{st[-1][0]}`' if st else '栈为空'
    return f'当前节点 ==`{n.val}`==，{top}（栈里的值单调不增）'


CONFIG = dict(
    num=1019, title='链表中的下一个更大节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='单调栈（保存还没找到答案的位置）',
    tags=['单调栈', '链表树与回溯', '难度分 1571'],
    code='''
class Solution(object):
    def nextLargerNodes(self, head):
        
        stack = []
        res = []

        now = head
        l = 0
        while now:
            res.append(0)
            while stack and stack[-1][0] < now.val:
                res[stack[-1][1]] = now.val
                stack.pop()
            stack.append([now.val, l])
            now = now.next
            l += 1

        return res
''',
    call='Solution().nextLargerNodes(L([2,7,4,3,5]))',
    expect=[7, 0, 5, 5, 0],
    views=[
        dict(type='text', fn=_info),
        dict(type='linked', label='链表（now 指向当前节点）', pointers={'now': 'blue'}, h=170),
        dict(type='array', var='res', label='res（初始全是 0，找到答案就覆盖）', h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='stack', var='stack', label='单调栈 [值, 位置]', fmt=lambda x: f'{x[0]}@{x[1]}', h=260),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('l', 'l', 'cyan'), ('stack', 'stack', 'yellow'), ('res', 'res', 'green')],
    captions={
        'stack = []': '栈里放==还没找到答案==的数，同时记下它的位置',
        'res = []': '`res` 每个位置先占一个 0，没找到答案就保持 0',
        'now = head': '像遍历数组一样，从头向后扫描链表',
        'while now': lambda S, B, ret: ('`now` 不为空，处理当前节点' if S.now else '`now` 为空，链表走完'),
        'res.append(0)': '先给当前节点 `{now.val}` 占位：`res = {res}`',
        'while stack and stack[-1][0] < now.val': lambda S, B, ret: (
            f'栈顶 `{S.stack[-1][0]}` < 当前 `{S.now.val}` → 当前节点就是栈顶位置 `{S.stack[-1][1]}` 的答案' if S.stack and S.stack[-1][0] < S.now.val
            else ('栈为空 → 没有在等答案的位置' if not S.stack else f'栈顶 `{S.stack[-1][0]}` ≥ 当前 `{S.now.val}` → 栈顶还要继续等')),
        'res[stack[-1][1]] = now.val': '位置 `{stack[-1][1]}` 的答案 = ==`{now.val}`==：`res = {res}`',
        'stack.pop()': '这个位置已有答案，==弹出==',
        'stack.append': '当前节点自己的答案还不知道 → 连同位置 `{l}` 入栈',
        'now = now.next': '`now` 走到下一个节点',
        'l += 1': '位置计数 `l` → {l}',
        'return res': '栈里剩下的就是没有答案的，本来就是 0：`{res}`',
    },
    cards=dict(
        one_liner='把还没找到答案的位置存进单调栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['链表每个节点，向后找第一个==严格更大==的节点值，没有就是 0',
                 '示例：`[2,1,5]` → `[5,5,0]`',
                 '本视频：`[2,7,4,3,5]` → `[7,0,5,5,0]`'],
        quote='保存下来的还没找到答案的这些位置上的数必然是单调不增的……很自然就想到使用单调栈来维护这些没有找到答案的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['链表只能从头向后走，就先想数组怎么做',
              '位置 i 若还没答案，后面的数一定不比它大，否则早就有答案了',
              '所以栈里单调不增：新数来了，弹出所有比它小的并写答案'],
        summary=['时间 `O(n)`，每个节点最多入栈、出栈一次',
                 '`res` 先全部占位为 0，所以栈里剩下的不用再处理',
                 '弹栈条件是 `<`（严格更大），相等的数留在栈里',
                 '原文为 Python 2 风格，代码无需改动即可运行'],
    ),
)
