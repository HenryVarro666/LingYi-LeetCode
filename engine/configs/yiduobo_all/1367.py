def _nv(x):
    return '空' if x is None else str(x.val)


def _u(x):
    return None if x is None else x._uid


def _info(S):
    I = S.get('_inner', {})
    if 'now_root' not in I:
        return ''
    return f"树节点 `now_root = {_nv(I['now_root'])}`，链表节点 `now_head = {_nv(I['now_head'])}`"


def _cap_dfs_line(S, B, ret):
    r = B.get('now_root')
    if ret is not None:
        return f'`dfs` 这一层（起点 `{_nv(r)}`）返回 =={ret}=='
    return f'起点 `{_nv(r)}`：先 `check` 从它往下匹配；不行再 `dfs` 左儿子，再 `dfs` 右儿子'


def _cap_check_line(S, B, ret):
    r = B.get('now_root')
    if ret is not None:
        return f'`check` 这一层（`{_nv(r)}`）返回 =={ret}=='
    return f'`{_nv(r)}` 值相同：链表走到下一个，树先试左儿子，不行再试右儿子'


def _cap_false(S, B, ret):
    if S.now_root is None:
        return '树走到了空节点，链表还没匹配完 → 返回 `False`'
    if S.now_root.val != S.now_head.val:
        return '值不相同 → 返回 `False`'
    return '返回 `False`：这个节点上没有可用的起点'


CONFIG = dict(
    num=1367, title='二叉树中的链表', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 枚举起点 + check 匹配',
    tags=['二叉树', '链表', '难度分 1650'],
    code='''
class Solution(object):
    def isSubPath(self, head, root):

        return self.dfs(root, head)
    
    def dfs(self, now_root, now_head):
        if now_head is None:
            return True
        if now_root is None:
            return False
        
        return self.check(now_root, now_head) or self.dfs(now_root.left, now_head) or self.dfs(now_root.right, now_head)
    
    def check(self, now_root, now_head):
        if now_head is None:
            return True
        if now_root is None:
            return False
        
        if now_root.val != now_head.val:
            return False
        
        return self.check(now_root.left, now_head.next) or self.check(now_root.right, now_head.next)
''',
    call='Solution().isSubPath(L([4,2,8]), Tr([1,4,4,2,None,None,2,None,None,None,8]))',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=24, h=46),
        dict(type='tree', label='二叉树（蓝 = now_root）', pointers={'now_root': 'blue'}, path=False, h=230),
        dict(type='linked', label='链表（蓝 = now_head，粉 = head）', pointers={'now_head': 'blue', 'head': 'pink'}, h=150),
        dict(type='calls', h=210, hide=('head', 'root')),
    ],
    watch=[('now_root', lambda S: S['_inner']['now_root'].val if S['_inner'].get('now_root') is not None else '空', 'blue'),
           ('now_head', lambda S: S['_inner']['now_head'].val if S['_inner'].get('now_head') is not None else '空', 'pink')],
    max_steps=80,
    skip=['if now_head is None', 'if now_root is None'],
    captions={
        'return self.dfs(root, head)': '外层只做一件事：在树里枚举起点，从 `root` 开始 `dfs`',
        'or self.dfs(now_root.right': _cap_dfs_line,
        'now_head.next)': _cap_check_line,
        'if now_root.val != now_head.val': lambda S, B, r: (
            f'`{S.now_root.val}` ≠ `{S.now_head.val}` → 值不同，匹配失败' if S.now_root.val != S.now_head.val
            else f'`{S.now_root.val}` == `{S.now_head.val}` → 值相同，可以继续匹配'),
        'return False': _cap_false,
        'return True': '链表走完了（`now_head` 为空）→ 全部匹配上 → 返回 `True`',
    },
    cards=dict(
        one_liner='dfs 枚举起点，check 判断从这个起点能否一路匹配到链表尾',
        complexity='时间 `O(n·m)`，空间 `O(m)`（n 为链表长、m 为树节点数，空间为递归栈）',
        problem=['给你二叉树根 `root` 和链表头 `head`',
                 '树里是否存在一条==一直向下==的路径，节点值与链表逐个对应？',
                 '本视频：`head = [4,2,8]`，`root = [1,4,4,2,null,null,2,null,null,null,8]` → `True`'],
        quote='没有什么特别好的思路，我选择的做法是在树中进行dfs，枚举答案的起点。对于每个起点，我们同样是进行dfs来判断从当前点开始是否能与链表进行匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个函数分工：`dfs` 负责==选起点==，`check` 负责==从该起点往下匹配==',
              '`check`：值不同 → 失败；相同 → 链表走下一个，树分别走左右儿子',
              '`now_head` 走到空 → 链表匹配完 → 成功',
              '`dfs`：当前起点不行，就换成左儿子或右儿子当起点'],
        summary=['时间 `O(n·m)`，空间 `O(m)`：每个起点最多匹配链表那么长',
                 '易错：`check` 里要先判链表空（成功）再判树空（失败），顺序不能反',
                 '对比灵神：灵神把两个递归合并成一个，靠 `s is head` 区分“重启”；yiduobo 写成 dfs + check 两个函数，更直观',
                 '原文为 Python 2 风格，本题代码无需修改，直接在 Python 3 运行'],
    ),
)
