def _d(x):
    if not x:
        return '{}'
    return '{' + ', '.join(f'{k}:{v}' for k, v in x.items()) + '}'


def _cap_left(S, B, ret):
    kid = S.get('now')
    par = B['now'].val
    if kid is None:
        return f'`{par}` 的左子树为空 → 返回 `({{}}, 0)`'
    return f'先递归求解左儿子 `{kid.val}` 的 `sum_dict`'


def _cap_right(S, B, ret):
    kid = S.get('now')
    par = B['now'].val
    got = f'左边返回 `left_sum = {_d(B["left_sum"])}`、`left_res = {B["left_res"]}`；'
    if kid is None:
        return got + f'`{par}` 的右子树为空 → 返回 `({{}}, 0)`'
    return got + f'再递归右儿子 `{kid.val}`'


def _cap_for(side):
    word = '左' if side == 'left_sum' else '右'

    def f(S, B, ret):
        k, v = S.get('key'), S.get('val')
        if k is not None and (B.get('key'), B.get('val')) != (k, v):
            kid = getattr(S['now'], 'left' if side == 'left_sum' else 'right')
            return f'{word}儿子 `{kid.val}` 出发、和为 `{k}` 的路径有 `{v}` 条'
        if not S[side]:
            return f'`{side}` 是空的，没有要合并的'
        return f'`{side}` 合并完了'
    return f


def _cap_merge(S, B, ret):
    k, v, nv = S['key'], S['val'], S['now'].val
    return f'接上 `{nv}`：和变成 `{k} + {nv} = {k + nv}`，`sum_dict[{k + nv}]` 加 {v} 条 → `{S["sum_dict"][k + nv]}`'


def _cap_ret(S, B, ret):
    d, res = ret
    t = S['sum']
    mine = d.get(t, 0)
    return (f'以 `{S["now"].val}` 为起点、和为 {t} 的有 `sum_dict.get({t}, 0) = {mine}` 条，'
            f'加上左右子树里的 `{S["left_res"]} + {S["right_res"]}` → 返回答案 =={res}==')


CONFIG = dict(
    num=437, title='路径总和 III', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='树形 DP：每个节点维护以它为起点的路径和字典',
    code='''
class Solution(object):
    def pathSum(self, root, sum):
        return self.dfs(root, sum)[1]

    def dfs(self, now, sum):
        if not now:
            return {}, 0

        left_sum, left_res = self.dfs(now.left, sum)
        right_sum, right_res = self.dfs(now.right, sum)
        sum_dict = {now.val: 1}
        for key, val in left_sum.items():
            sum_dict[key + now.val] = sum_dict.get(key + now.val, 0) + val
        for key, val in right_sum.items():
            sum_dict[key + now.val] = sum_dict.get(key + now.val, 0) + val

        return sum_dict, sum_dict.get(sum, 0) + left_res + right_res
''',
    call='Solution().pathSum(Tr([10,5,-3,3,None,None,11]), 8)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"左儿子出发 `left_sum = {_d(S['left_sum'])}`　右儿子出发 `right_sum = {_d(S['right_sum'])}`"
                                        if 'right_sum' in S else (f"左儿子出发 `left_sum = {_d(S['left_sum'])}`" if 'left_sum' in S else '')), size=26),
        dict(type='map', var='sum_dict', label='sum_dict（以 now 为起点：路径和 → 条数）', fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='tree', pointers={'now': 'blue'}, h=300),
        dict(type='calls', h=150),
    ],
    watch=[('sum', 'sum'), ('left_res', 'left_res', 'blue'), ('right_res', 'right_res', 'pink')],
    captions={
        'return self.dfs(root, sum)[1]': '`dfs(now)` 返回两样：以 `now` 为起点的 `sum_dict`，以及子树里的答案；取 `[1]`',
        'left_sum, left_res = self.dfs': _cap_left,
        'right_sum, right_res = self.dfs': _cap_right,
        'sum_dict = {now.val: 1}': '`sum_dict[v]` = 以 `{now.val}` 为起点、和为 `v` 的向下路径条数；先放只有它自己的一条',
        'for key, val in left_sum': _cap_for('left_sum'),
        'for key, val in right_sum': _cap_for('right_sum'),
        'sum_dict[key + now.val] =': _cap_merge,
        'return sum_dict, sum_dict.get': _cap_ret,
    },
    skip=['if not now', 'return {}, 0'],
    max_steps=60,
    cards=dict(
        one_liner='路径只能向下 → 以 node 为起点的路径 = node + 以儿子为起点的路径',
        complexity='最坏时间 `O(n²)`，空间 `O(n)`',
        problem=['求二叉树里节点值之和等于 `sum` 的==路径==数目',
                 '路径不必从根开始、不必在叶子结束，但方向必须==向下==（父 → 子）',
                 '示例：`root = [10,5,-3,3,null,null,11]`，`sum = 8`',
                 '→ `2` 条：`5→3` 和 `-3→11`'],
        quote='注意到题目中的路径要求方向必须是向下的，那么对于任意节点node而言，一条合法的路径就==不可能同时包含node.left以及node.right==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['每个节点维护 `sum_dict[value]`：==以 node 为起点==、和为 value 的路径条数',
              '先递归求出左右儿子的字典，每条路径往上接一个 `node.val`，再加上只含 node 的一条',
              '`sum_dict[sum]` 就是以 node 为起点的答案，总答案同样递归累加'],
        summary=['每个节点的字典最多有子树大小个键 → 最坏（链）时间 `O(n²)`，空间 `O(n)`',
                 '易错：别忘了只含 `now` 自己的路径 `{now.val: 1}`',
                 '对比灵神的前缀和做法 `O(n)`：枚举终点 + 哈希表计数起点',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
