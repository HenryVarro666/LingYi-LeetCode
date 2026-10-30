CONFIG = dict(
    num=2265, title='统计值等于子树平均值的节点数', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归返回 (数量, 个数, 和)',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1473'],
    code='''
class Solution(object):
    def averageOfSubtree(self, root):
        def dfs(now):
            res = 0
            cnt = 1
            s = now.val
            if now.left:
                left_res, left_cnt, left_s = dfs(now.left)
                res += left_res
                cnt += left_cnt
                s += left_s

            if now.right:
                right_res, right_cnt, right_s = dfs(now.right)
                res += right_res
                cnt += right_cnt
                s += right_s

            if s // cnt == now.val:
                res += 1

            return res, cnt, s

        return dfs(root)[0]
''',
    call='Solution().averageOfSubtree(Tr([4,8,5,0,1,None,6]))',
    expect=5,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, h=300),
        dict(type='text', fn=lambda S: (f"本子树：满足 `res = {S['_inner']['res']}`，节点数 `cnt = {S['_inner']['cnt']}`，和 `s = {S['_inner']['s']}`"
                                         if 'cnt' in S['_inner'] else ''), size=26, h=60),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow'),
           ('s', lambda S: S['_inner'].get('s'), 'yellow')],
    captions={
        'res = 0': '新的一层：满足条件的数 `res = 0`',
        'cnt = 1': '节点数先算上自己：`cnt = 1`',
        's = now.val': '和先算上自己：`s = {now.val}`',
        'if now.left:': lambda S, B, r: (f'`{B.now.val}` 有左孩子 → 先递归求左子树' if B.now.left
                                         else f'`{B.now.val}` 没有左孩子 → 跳过'),
        'if now.right:': lambda S, B, r: (f'`{B.now.val}` 有右孩子 → 再递归求右子树' if B.now.right
                                          else f'`{B.now.val}` 没有右孩子 → 跳过'),
        'left_res, left_cnt, left_s': '左子树返回：满足 `{left_res}` 个，节点 `{left_cnt}` 个，和 `{left_s}`',
        'right_res, right_cnt, right_s': '右子树返回：满足 `{right_res}` 个，节点 `{right_cnt}` 个，和 `{right_s}`',
        'res += left_res': '累加左子树里满足条件的数：`res = {res}`',
        'cnt += left_cnt': '节点数加上左子树：`cnt = {cnt}`',
        's += left_s': '和加上左子树：`s = {s}`',
        'res += right_res': '累加右子树里满足条件的数：`res = {res}`',
        'cnt += right_cnt': '节点数加上右子树：`cnt = {cnt}`',
        's += right_s': '和加上右子树：`s = {s}`',
        'if s // cnt': lambda S, B, r: (f'平均值 `{S.s} // {S.cnt} = {S.s // S.cnt}` 等于 `{S.now.val}` → ==当前节点满足条件=='
                                        if S.s // S.cnt == S.now.val else
                                        f'平均值 `{S.s} // {S.cnt} = {S.s // S.cnt}` != `{S.now.val}` → 当前节点不满足'),
        'res += 1': '算上自己：`res = {B.res} + 1 = {res}`',
        'return res, cnt, s': '把 `(res, cnt, s) = ({res}, {cnt}, {s})` 交给父节点',
        'return dfs(root)[0]': '从根开始递归，最后只取返回三元组的第 0 项 = ==满足条件的节点数==',
    },
    cards=dict(
        one_liner='一次递归同时求：满足数、节点数、数值和',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['找出节点值 ==等于其子树平均值== 的节点数',
                 '平均值 = 和 ÷ 节点数，向下取整',
                 '示例：`root = [4,8,5,0,1,null,6]` → `5`'],
        quote='以node为根节点的树中所有节点数值之和，就等于以node.left为根节点的子树中所有节点数值之和，加上以node.right为根节点的子树中所有节点数值之和，再加上node自身的数值。',
        quote_src='—— yiduobo 题解',
        idea=['子树的和、节点数都能由左右子树推出来',
              '`dfs(now)` 返回 `(res, cnt, s)`',
              '先累加两边，再用 `s // cnt` 判断自己是否满足'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '原文为 Python 2 写法，整数除法 `s / cnt` 已改为 `s // cnt`；删去了 docstring',
                 '先判断孩子存在再递归，不用处理空节点',
                 '`res` 要先累加两边再判断自己'],
    ),
)
