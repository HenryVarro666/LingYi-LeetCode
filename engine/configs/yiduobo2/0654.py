NUMS = [3, 2, 1, 6, 0, 5]   # 示例 1


def _uids(S, name='stack'):
    return {n._uid for n in (S.get(name) or [])}


def _in_loop(S):
    return S.get('_line', 0) <= 15


def _idx(S):
    return S['nums'].index(S['num']) if 'num' in S and _in_loop(S) else -1


def cap_while(S, B, ret):
    st, num = B.stack, B.num
    if not st:
        return f'栈空 → `{num}` 左侧没有更大的数，不用弹'
    t = st[-1].val
    if t < num:
        return f'栈顶 `{t}` < `{num}`：`{t}` 右侧最近的更大值就是 `{num}` → ==左右两侧都找齐了==，弹出处理'
    return f'栈顶 `{t}` > `{num}`：它就是 `{num}` ==左侧最近的更大值==，停止弹栈'


def cap_if(S, B, ret):
    st, num, t = B.stack, B.num, B.tmp.val
    if st and st[-1].val < num:
        return f'左侧更大值 `{st[-1].val}` < 右侧更大值 `{num}` → 选==较小==的 `{st[-1].val}` 当 `{t}` 的父亲'
    if st:
        return f'左侧更大值 `{st[-1].val}` > 右侧更大值 `{num}` → 选==较小==的 `{num}` 当 `{t}` 的父亲'
    return f'`{t}` 左侧没有更大值 → 父亲只能是右侧的 `{num}`'


def cap_while2(S, B, ret):
    st = B.stack
    if st:
        return f'栈里还有 `{st[-1].val}`：它比 `{B.now.val}` 大且在左边 → 继续往下挂'
    return f'栈空了：最后出栈的 `{B.now.val}` 左右都没有更大值 → ==它就是根=='


def node_color(S, n):
    if n._uid in _uids(S):
        return 'purple'
    return None


def show(S):
    ln = S.get('_line', 0)
    if ln >= 16:
        return '扫描结束：栈中元素右侧都没有更大值 → 从栈顶起，依次挂成==下一个的右子树=='
    return '父亲 = 左右两侧==离得最近的更大值==中较小的那个'


CONFIG = dict(
    num=654, title='最大二叉树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='单调栈 · 找两侧最近的更大值',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def constructMaximumBinaryTree(self, nums):
        stack = []
        left = {}
        right = {}
        for num in nums:
            now = TreeNode(num)
            while stack and stack[-1].val < num:
                tmp = stack.pop()
                if stack and stack[-1].val < num:
                    stack[-1].right = tmp
                else:
                    now.left = tmp

            stack.append(now)

        if stack:
            now = stack.pop()
            while stack:
                stack[-1].right = now
                now = stack.pop()

        return now
''',
    call=f'Solution().constructMaximumBinaryTree({NUMS})',
    result_fn=tree_list,
    expect=[6, 3, 5, None, 2, 0, None, None, 1],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 num）', cell=80,
             pointers={'nums.index(num) if _line <= 15 else None': 'blue'},
             pointer_labels={'nums.index(num) if _line <= 15 else None': 'num'},
             color=lambda S, i, v: 'blue' if i == _idx(S) else None,
             dim=lambda S, i, v: _idx(S) >= 0 and i > _idx(S)),
        dict(type='stack', var=lambda S: [n.val for n in S['stack']] if 'stack' in S else None,
             label='stack（单调递减：还没找到右侧更大值的节点）', h=120, font=30),
        dict(type='tree', label='已建好的子树（紫 = 在栈中）', h=330, path=False,
             pointers={'now': 'blue', 'tmp': 'pink'}, color=node_color),
        dict(type='text', fn=show, size=24, h=70),
    ],
    watch=[('num', 'num', 'blue'), ('now', 'now.val', 'blue'), ('tmp', 'tmp.val', 'pink'),
           ('stack', '[n.val for n in stack]', 'purple')],
    skip=['left = {}', 'right = {}'],
    captions={
        'stack = []': '单调栈：存==还没找到右侧更大值==的节点（`left`/`right` 两个字典原文未用到）',
        'for num in nums': lambda S, B, ret: (f'扫描到 `num = {S.num}`' if 'num' not in B or B.num != S.num
                                              else '一趟扫描结束'),
        'now = TreeNode(num)': '为 `{num}` 新建节点 `now`',
        'while stack and': cap_while,
        'tmp = stack.pop()': lambda S, B, ret: (f'弹出 `tmp = {S.tmp.val}`：左侧更大值是新栈顶 `{S.stack[-1].val}`，右侧更大值是 `{S.num}`'
                                                if S.stack else f'弹出 `tmp = {S.tmp.val}`：右侧更大值是 `{S.num}`，左侧没有了'),
        'if stack and stack[-1].val < num': cap_if,
        'stack[-1].right = tmp': '`{tmp.val}` 在 `{stack[-1].val}` 的右边 → 挂成 `{stack[-1].val}` 的==右孩子==',
        'now.left = tmp': '`{tmp.val}` 在 `{num}` 的左边 → 挂成 `{num}` 的==左孩子==',
        'stack.append(now)': lambda S, B, ret: (f'`{S.num}` 入栈：' + (f'栈顶 `{B.stack[-1].val}` 是它左侧最近的更大值，' if B.stack else '')
                                               + '它的右侧更大值==还没出现=='),
        'if stack:': '扫描结束，栈里还剩 `{[n.val for n in stack]}`：它们右侧都没有更大值',
        18: '从栈顶开始：`now = {now.val}`',
        21: '`now` 上移到 `{now.val}`，继续给它找父亲',
        'while stack:': cap_while2,
        'stack[-1].right = now': '`{now.val}` 挂成 `{stack[-1].val}` 的==右子树==',
        'return now': '返回根节点 =={ret.val}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个数的父亲 = 两侧最近更大值中较小的那个，用单调栈一趟找出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 无重复元素，按规则递归建树：',
                 '根是区间最大值，最大值==左边==建左子树，==右边==建右子树',
                 '示例：`[3,2,1,6,0,5]` → `[6,3,5,null,2,0,null,null,1]`'],
        quote='对于数组中的某个值nums[index]，若其不是根节点，那么其父亲节点的值必然是离index最近的，且值大于nums[index]的某个数……此时我们应当选择较小的那一个作为index的父亲。',
        quote_src='—— yiduobo 知乎题解',
        idea=['朴素做法每次找区间最大值再递归，`O(n²)`',
              '结论：父亲是左右两侧==最近的更大值==里较小的那个；左侧较小 → 当它的右孩子，否则当右侧的左孩子',
              '单调递减栈：元素被弹出时，新栈顶是左侧更大值，当前 num 是右侧更大值'],
        result='树 `[6,3,5,null,2,0,null,null,1]` ✓ 与示例一致',
        summary=['时间 `O(n)`：每个元素最多进出栈一次；空间 `O(n)`',
                 '易错：弹出 `tmp` 后比较的是==新栈顶==与 `num`，谁小谁当父亲',
                 '扫描结束后栈里剩下的从栈顶起依次挂成下一个的右子树，栈底是根',
                 '原文为 Python 2 风格，已删去文档字符串和注释掉的 TreeNode 定义，代码未改'],
    ),
)
