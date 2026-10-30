def _ex(nd):
    """子树 -> 带括号的中缀字符串"""
    if nd is None:
        return '?'
    if nd.left is None and nd.right is None:
        return nd.v
    return f'({_ex(nd.left)}{nd.v}{_ex(nd.right)})'


def _idx(S):
    return S['postfix'].index(S['v']) if 'v' in S else -1


CONFIG = dict(
    num=1628, title='设计带解析函数的表达式树', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='后缀表达式建树 + 递归求值',
    tags=['常用数据结构', '链表树与回溯'],
    code='''
import abc 
from abc import ABCMeta, abstractmethod 

class Node:
    __metaclass__ = ABCMeta
    # define your fields here

    def __init__(self, v):
        self.v = v
        self.left = None
        self.right = None

    @abstractmethod
    def evaluate(self):
        if self.v.isdigit():
            return int(self.v)
        
        left_res = self.left.evaluate()
        right_res = self.right.evaluate()

        if self.v == '+':
            return left_res + right_res
        elif self.v == '-':
            return left_res - right_res
        elif self.v == '*':
            return left_res * right_res
        else:
            return left_res // right_res

class TreeNode(Node):

    def __init__(self, v):
        super(TreeNode, self).__init__(v)
    
    def evaluate(self):
        return super(TreeNode, self).evaluate()

class TreeBuilder(object):
    def buildTree(self, postfix):

        stack = []
        for v in postfix:
            node = TreeNode(v)
            if node.v.isdigit():
                stack.append(node)
            else:
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
        
        return stack[-1]
''',
    call='TreeBuilder().buildTree(["3", "4", "+", "2", "*"]).evaluate()',
    expect=14,
    views=[
        dict(type='array', var='postfix', label='postfix（后缀表达式，蓝 = 当前 v）', cell=80, h=170,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'v'},
             dim=lambda S, i, v: 'v' in S and i < _idx(S)),
        dict(type='stack', var='stack', label='stack（子树，栈顶在右；括号 = 子树的中缀写法）', h=130, font=26, fmt=_ex),
        dict(type='calls', h=300, hide=('postfix',)),
    ],
    watch=[('v', lambda S: S['_inner'].get('v'), 'blue'),
           ('stack', lambda S: [_ex(x) for x in S['_inner'].get('stack', [])], 'green')],
    skip=['import abc', 'from abc import', 'node = TreeNode(v)', 'for v in postfix', 'super(TreeNode, self).__init__',
          'self.v = v', 'self.left = None', 'self.right = None', "if self.v == '+'", "elif self.v == '-'", "elif self.v == '*'"],
    captions={
        'stack = []': '栈里放==子树==：数字是只有一个节点的树',
        'if node.v.isdigit()': lambda S, B, r: (f'`v = "{S.v}"` 是数字 → 它自己就是一棵==叶子树==，入栈' if S.v.isdigit()
                                                else f'`v = "{S.v}"` 是运算符 → 它要吃掉栈顶两棵子树'),
        'stack.append(node)': lambda S, B, r: (f'叶子 `{S.node.v}` 入栈：`{[_ex(x) for x in S.stack]}`' if S.node.left is None
                                               else f'新子树 `{_ex(S.node)}` 压回栈：`{[_ex(x) for x in S.stack]}`'),
        'node.right = stack.pop()': '先弹出的是后入栈的 → 当==右孩子==（根为 `{node.right.v}` 的子树）',
        'node.left = stack.pop()': '再弹出的是先入栈的 → 当==左孩子==（根为 `{node.left.v}` 的子树）；顺序不能反，减除法会错',
        'return stack[-1]': '扫完后栈里只剩一棵树，它的根就是表达式树的根 `{ret.v}`',
        'if self.v.isdigit()': lambda S, B, r: (f'`self.v = "{S.self.v}"` 是数字 → 叶子，直接返回数值' if S.self.v.isdigit()
                                                else f'`self.v = "{S.self.v}"` 是运算符 → 先递归求左右子树，再运算'),
        'return int(self.v)': '叶子：返回 `{ret}`',
        'left_res = self.left.evaluate()': '递归求==左子树==',
        'right_res = self.right.evaluate()': '递归求==右子树==',
        'return left_res + right_res': '`{left_res} + {right_res}` = =={ret}==',
        'return left_res - right_res': '`{left_res} - {right_res}` = =={ret}==',
        'return left_res * right_res': '`{left_res} * {right_res}` = =={ret}==',
        'return left_res // right_res': '`{left_res} // {right_res}` = =={ret}==',
        'return super(TreeNode, self).evaluate()': '`TreeNode.evaluate` 只是转交给父类 `Node.evaluate`，真正的逻辑在那里',
    },
    max_steps=110,
    cards=dict(
        one_liner='后缀表达式用栈建树：运算符吃掉栈顶两棵子树',
        complexity='建树 `O(n)`，求值 `O(n)`，空间 `O(n)`',
        problem=['设计表达式树：`TreeBuilder.buildTree(postfix)` 由后缀表达式建树',
                 '返回的树根 `Node` 要有 `evaluate()`，递归求出整个表达式的值',
                 '本视频：`["3","4","+","2","*"]` → `(3+4)*2 = 14`'],
        quote='将所有的数值以及运算符都视为树中的节点。对于遍历到的运算符，就将参与运算的两个节点视为这个运算符节点的左右孩子。',
        quote_src='—— yiduobo 题解原文',
        idea=['后缀表达式求值：数字入栈，运算符弹两个数算完压回',
              '建树同理：栈里放节点，运算符节点弹两个节点当右、左孩子',
              '求值：叶子返回数字，内部节点先递归左右子树，再按根的符号运算'],
        result='表达式树根为 `*`，递归求值得 14 ✓',
        summary=['建树 `O(n)`，求值 `O(n)`，空间 `O(n)`（栈和递归栈）',
                 '易错：先弹出的是右孩子，后弹出的才是左孩子',
                 '`TreeNode.evaluate` 只是转调父类 `Node.evaluate`，题目要求保留 `Node` 接口',
                 '原文为 Python 2 写法：除法 `/` 已改为 `//`；删去了两段说明用的文档字符串',
                 '同类题：1597 用中缀表达式建树；150 逆波兰表达式求值'],
    ),
)
