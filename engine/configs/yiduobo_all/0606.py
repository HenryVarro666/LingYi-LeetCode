CONFIG = dict(
    num=606, title='根据二叉树创建字符串', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='前序遍历拼括号',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def tree2str(self, t):
        return self.dfs(t)

    def dfs(self, now):
        if not now:
            return ''

        ret = str(now.val)
        if now.left:
            ret += '(' + self.dfs(now.left) + ')'
            if now.right:
                ret += '(' + self.dfs(now.right) + ')'
        elif now.right:
            ret += '()'
            ret += '(' + self.dfs(now.right) + ')'

        return ret
''',
    call='Solution().tree2str(Tr([1,2,3,None,4]))',
    expect='1(2()(4))(3)',
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, h=280),
        dict(type='text', fn=lambda S: f"本层字符串 `ret = '{S['_inner']['ret']}'`" if 'ret' in S['_inner'] else '', size=28, h=60),
        dict(type='calls', h=230, hide=('t',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('ret', lambda S: S['_inner'].get('ret'), 'green')],
    captions={
        'return self.dfs(t)': '前序遍历：先写自己，再写左子树，最后写右子树',
        'if not now': lambda S, B, r: ('空节点 → 返回空串 `\'\'`，这是==递归边界==' if S.now is None
                                      else f'节点 `{S.now.val}` 非空 → 先写出它的值'),
        "return ''": '空节点什么也不写，返回空串',
        'ret = str': lambda S, B, r: f"先写自己：`ret = '{S.now.val}'`",
        'if now.left:': lambda S, B, r: (f'`{B.now.val}` 有左子树 → 用括号括起来递归写出' if B.now.left else
                                         f'`{B.now.val}` 没有左子树 → 看看有没有右子树'),
        "ret += '(' + self.dfs(now.left)": lambda S, B, r: f"左子树写完，拼上括号：`ret = '{S['_inner']['ret']}'`",
        12: lambda S, B, r: (f'`{B.now.val}` 有右子树 → 同样括起来接在后面' if B.now.right else
                                          f'`{B.now.val}` 没有右子树 → 到此为止，右边什么都不写'),
        "ret += '(' + self.dfs(now.right)": lambda S, B, r: f"右子树写完，拼上括号：`ret = '{S['_inner']['ret']}'`",
        14: lambda S, B, r: (f'`{B.now.val}` 没有左子树但有右子树 → 左边必须留一对空括号 ==()=='
                                           if B.now.right else f'`{B.now.val}` 左右都没有 → 叶子，只写自己的值'),
        "ret += '()'": lambda S, B, r: f"给空的左子树留位置：`ret = '{S['_inner']['ret']}'`，这样右子树的位置才不会错",
        'return ret': lambda S, B, r: f"`{S.now.val}` 这棵子树的字符串是 `'{r}'`，交给上一层",
    },
    skip=['if not now:'],
    cards=dict(
        one_liner='前序遍历，子树用括号包起来；只有右子树时给左边留空括号',
        complexity='时间 `O(n)`，空间 `O(h)`（不计结果字符串）',
        problem=['把二叉树按前序遍历转成字符串，子树用括号括起来',
                 '要省略不必要的空括号对，但不能改变一一对应关系',
                 '示例：`root = [1,2,3,null,4]` → `"1(2()(4))(3)"`'],
        quote='若当前节点有左子树或者右子树，那么就递归处理然后用括号将其括起来。需要注意当只有右子树时，也需要为左子树预留空的括号。',
        quote_src='—— yiduobo 题解',
        idea=['先写自己的值，再处理孩子',
              '有左子树：`(左)`；左右都有再接 `(右)`',
              '只有右子树：先补 `()` 占位，再接 `(右)`',
              '叶子或空节点不加任何括号'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：只有右子树时空括号 `()` 不能省，否则左右会混淆',
                 '只有左子树时右边的空括号可以省略',
                 '前序遍历 + 字符串拼接，递归函数直接返回子树对应的字符串'],
    ),
)
