CONFIG = dict(
    num=2764, title='数组是否表示某二叉树的前序遍历', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='栈模拟搜索回溯',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def isPreorder(self, nodes):

        if nodes[0][1] != -1:
            return False
        
        stack = [nodes[0][0]]
        for nid, pid in nodes[1:]:
            while stack and stack[-1] != pid:
                stack.pop()
            
            if stack:
                stack.append(nid)
            else:
                return False
        
        return True
''',
    call='Solution().isPreorder([[0,-1],[1,0],[2,1],[3,0],[4,3]])',
    expect=True,
    views=[
        dict(type='array', var='nodes', label='nodes = [节点 id, 父节点 id]（黄 = 当前处理）', cell=130, h=210,
             fmt=lambda v: f'{v[0]},{v[1]}' if isinstance(v, list) else str(v),
             color=lambda S, i, v: ('yellow' if 'nid' in S and v[0] == S['nid'] else ('green' if 'nid' in S and v[0] < S['nid'] else None))),
        dict(type='text', fn=lambda S: (f"当前 `nid = {S['nid']}`，要找的父节点 `pid = {S['pid']}`；栈顶 = `{S['stack'][-1] if S['stack'] else '空'}`" if 'nid' in S else ''), size=26, h=60),
        dict(type='stack', var='stack', label='stack（当前 dfs 路径，右 = 栈顶）', h=200),
    ],
    watch=[('nid', 'nid', 'yellow'), ('pid', 'pid', 'pink'), ('stack', 'stack', 'blue')],
    captions={
        'if nodes[0][1] != -1': lambda S, B, r: ('根的父节点必须是 `-1`：`{nodes[0][1]} == -1`，通过'.replace('{nodes[0][1]}', str(S.nodes[0][1])) if S.nodes[0][1] == -1 else '第一个节点的父节点不是 -1 → 它不是根，直接 False'),
        'stack = [nodes[0][0]]': '栈里先放根 `{stack}`：栈 = 从根到当前节点的路径',
        'for nid, pid': lambda S, B, r: ('所有节点都处理完，循环结束' if 'nid' in B and B.nid == S.nid else f'取下一个节点 `{S.nid}`，它的父亲应是 `{S.pid}`'),
        'while stack and stack[-1] != pid': lambda S, B, r: (f'栈顶 `{S.stack[-1]}` ≠ 父节点 `{S.pid}` → 这棵子树已搜完，要==回溯==' if S.stack and S.stack[-1] != S.pid
                                                            else (f'栈顶就是父节点 `{S.pid}`，不用再弹' if S.stack else '栈空了，没找到父节点')),
        'stack.pop()': '弹出栈顶（回溯到上一层）→ `{stack}`',
        'if stack': lambda S, B, r: (f'栈非空，栈顶 `{S.stack[-1]}` 就是父节点 → 可以挂上去' if S.stack else '栈空 → 前面没有父节点可挂，dfs 序不合法'),
        'stack.append(nid)': '`{nid}` 入栈，往它的子树里搜 → `{stack}`',
        'return False': lambda S, B, r: '返回 `False`',
        'return True': '全部节点都找到父亲 → 合法的前序遍历 ==True==',
    },
    skip=[],
    cards=dict(
        one_liner='前序遍历就是 dfs 序：用栈模拟搜索与回溯',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nodes[i] = [id, parentId]`，根的父亲是 `-1`',
                 '判断 `nodes` 是否是某棵二叉树前序遍历的结果',
                 '本视频：`[[0,-1],[1,0],[2,1],[3,0],[4,3]]` → `True`'],
        quote='前序遍历是按照根-左-右的顺序进行，恰好能与标准的搜索回溯完全对应上，也就是说题目相当于给出了dfs序，那么只需使用一个栈模拟搜索回溯的过程。',
        quote_src='—— yiduobo 题解原文',
        idea=['栈里存当前 dfs 路径；新节点的父亲必须在路径上',
              '栈顶不是父亲 → 说明栈顶那棵子树搜完了，弹出（回溯），直到栈顶是父亲',
              '栈弹空还没找到父亲 → 非法，返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：==先检查第一个节点的父亲是 `-1`==，否则它不是根',
                 '每个节点最多入栈出栈一次，所以虽然有 `while`，总体仍是线性',
                 '原文本来就是 Python 3 可跑的写法，未做修改'],
    ),
)
