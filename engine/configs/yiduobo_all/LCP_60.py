

def _t_levels(S):
    if 'level_sum' not in S:
        return ''
    return f"层和 `level_sum = {S['level_sum']}`，层节点数 `level_size = {S['level_size']}`" 


def _cur_tab(S, name):
    n = S['_inner'].get('now') if isinstance(S.get('_inner'), dict) else None
    if n is None or name not in S:
        return None
    v = _dv(S, name, n)
    if v is None:
        return None
    return '{' + ', '.join(f'{a}: {b}' for a, b in sorted(v.items())) + '}' if isinstance(v, dict) else '{' + ', '.join(map(str, sorted(v))) + '}' if v else 'set()'


def _t_delta(S):
    d, r = _cur_tab(S, 'delta'), _cur_tab(S, 'remove_size')
    if d is None and r is None:
        return '`delta[now][层]`：删掉 now 后，该层层和的变化（还没算到 now）'
    return f"`delta[now]` = {d or '（无）'}（层: 层和变化）；`remove_size[now]` = {r or '（无）'}（层: 删掉个数）"


def _t_need(S):
    nr = _cur_tab(S, 'need_refresh')
    if nr is None:
        return ''
    return f"`need_refresh[now]` = {nr}：还没结算的层"


def _dv(S, name, node):
    for k, v in S[name].items():
        if k.val == node.val:
            return v
    return None


_RUN = {'best': None}   # res 是全局变量，追踪器看不到；字幕按顺序渲染，这里手动记一份当前最优


def _cand(S, n, lv, what):
    c = S['level_sum'][lv] + _dv(S, 'delta', n)[lv]
    old = _RUN['best']
    _RUN['best'] = max(old, c)
    keep = '更新为' if c > old else '不变，仍为'
    return f"{what} `{n.val}` 后第 `{lv}` 层层和 = `{S['level_sum'][lv]} + ({_dv(S, 'delta', n)[lv]})` = {c}；和当前最优 `res = {old}` 比，`res` {keep} =={_RUN['best']}=="


def _nv(S, k='now'):
    n = S['_inner'].get(k)
    return None if n is None else n.val


CODE = '''
class Solution(object):
    def getMaxLayerSum(self, root):

        level_sum = []
        level_size = []

        q = [root]
        head = 0
        tail = 1
        while head < tail:
            level_sum.append(0)
            level_size.append(tail - head)
            for now in q[head : tail]:
                level_sum[-1] += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        global res
        res = max(level_sum)
        
        delta = {}
        need_refresh = {}
        remove_size = {}

        def dfs(now, level):
            global res
            if now.left is None:
                if now.right is None:
                    remove_size[now] = {level: 1}
                    need_refresh[now] = set()
                    if level_size[level] == 1:
                        delta[now] = {}
                    else:
                        delta[now] = {level: -now.val}
                        res = max(res, level_sum[level] + delta[now][level])
                else:
                    dfs(now.right, level + 1)
                    delta[now] = delta[now.right]
                    delta[now][level] = now.right.val - now.val
                    remove_size[now] = remove_size[now.right]
                    remove_size[now][level] = 1
                    need_refresh[now] = need_refresh[now.right]
                    need_refresh[now].add(level)

                    for lv in need_refresh[now]:
                        if remove_size[now][lv] < level_size[lv]:
                            res = max(res, level_sum[lv] + delta[now][lv])
                    need_refresh[now] = set()

            elif now.right is None:
                dfs(now.left, level + 1)
                delta[now] = delta[now.left]
                delta[now][level] = now.left.val - now.val
                remove_size[now] = remove_size[now.left]
                remove_size[now][level] = 1
                need_refresh[now] = need_refresh[now.left]
                need_refresh[now].add(level)

                for lv in need_refresh[now]:
                    if remove_size[now][lv] < level_size[lv]:
                        res = max(res, level_sum[lv] + delta[now][lv])
                need_refresh[now] = set()
            
            else:
                dfs(now.left, level + 1)
                dfs(now.right, level + 1)
                
                if len(need_refresh[now.left]) > len(need_refresh[now.right]):
                    refresh_min, refresh_max = need_refresh[now.right], need_refresh[now.left]
                else:
                    refresh_min, refresh_max = need_refresh[now.left], need_refresh[now.right]
                
                need_refresh[now] = refresh_max
                for lv in refresh_min:
                    need_refresh[now].add(lv)
                need_refresh[now].add(level)

                if len(delta[now.left]) > len(delta[now.right]):
                    delta_min, delta_max = delta[now.right], delta[now.left]
                else:
                    delta_min, delta_max = delta[now.left], delta[now.right]
                
                delta[now] = delta_max
                for lv in delta_min:
                    delta[now][lv] = delta[now].get(lv, 0) + delta_min[lv]
                    need_refresh[now].add(lv)
                delta[now][level] = now.left.val + now.right.val - now.val
                

                if len(remove_size[now.left]) > len(remove_size[now.right]):
                    remove_min, remove_max = remove_size[now.right], remove_size[now.left]
                else:
                    remove_min, remove_max = remove_size[now.left], remove_size[now.right]
                
                remove_size[now] = remove_max
                for lv in remove_min:
                    remove_size[now][lv] += remove_min[lv]
                remove_size[now][level] = 1

        dfs(root, 0)
        return res
'''

CONFIG = dict(
    num='LCP 60', title='力扣泡泡龙', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='层序统计 + DFS 小到大合并哈希表',
    tags=['链表树与回溯'],
    code=CODE,
    call='Solution().getMaxLayerSum(Tr([1,3,2,-7,None,None,6]))',
    expect=9,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=250),
        dict(type='text', fn=_t_levels, size=22, h=50),
        dict(type='text', fn=_t_delta, size=22, h=60),
        dict(type='text', fn=_t_need, size=22, h=44),
        dict(type='calls', h=130),
    ],
    watch=[('now', lambda S: _nv(S), 'blue'), ('level', lambda S: S['_inner'].get('level'), 'cyan')],
    captions={
        'level_sum = []': '先不删：层序遍历统计每层的 `level_sum`（层和）和 `level_size`（节点数）',
        'level_size.append': '这一层有 `{level_size[-1]}` 个节点。==节点数用来防止删光一整层==（负数层和也不能靠删空变成 0）',
        'level_sum[-1] += now.val': '`level_sum[{len(level_sum)-1}]` 加上 `{now.val}` → {level_sum[-1]}',
        'res = max(level_sum)': lambda S, B, r: (_RUN.update(best=max(S['level_sum'])), f"不删任何节点就有一个答案：`res = max(level_sum) = {max(S['level_sum'])}`")[1],
        'delta = {}': '三张哈希表：`delta[now][lv]` = 删 now 后第 lv 层层和的变化；`need_refresh` = 待结算的层；`remove_size` = 被删的节点数',
        'dfs(root, 0)': '从根开始自底向上 DFS，用孩子的表来合成父亲的表',
        'if now.left is None': lambda S, B, r: (lambda n: f"节点 `{n.val}`（第 {S['_inner'].get('level')} 层）：" + ('叶子，没有孩子 → 可以直接删' if n.left is None and n.right is None else '只有右孩子 → 删它，右孩子顶上来' if n.left is None else '只有左孩子 → 删它，左孩子顶上来' if n.right is None else '有两个孩子 → 不能删，但要先递归算出孩子们的表'))(S['_inner']['now']),
        'remove_size[now] = {level: 1}': '叶子：删掉它，这一层少 1 个节点',
        'if level_size[level] == 1': lambda S, B, r: ('这一层只有它一个节点，删了整层变空 → 不合法，`delta = {}`' if S['level_size'][S['_inner']['level']] == 1 else '这一层还有别的节点，可以删'),
        'delta[now] = {level: -now.val}': lambda S, B, r: f"删叶子 `{_nv(S)}`：这一层层和变化 `{-_nv(S)}`",
        'res = max(res, level_sum[level] + delta[now][level])': lambda S, B, r: _cand(S, S['_inner']['now'], S['_inner']['level'], '删掉叶子'),
        'delta[now] = delta[now.right]': '只有一个孩子：直接==挪用==孩子的 `delta`（浅拷贝，不复制），避免 O(n²)',
        'delta[now] = delta[now.left]': '只有一个孩子：直接==挪用==孩子的 `delta`（浅拷贝，不复制），避免 O(n²)',
        'delta[now][level] = now.right.val - now.val': '删 `now`，右孩子 `{now.right.val}` 顶上来：这一层变化 `{now.right.val} - {now.val} = {now.right.val - now.val}`',
        'delta[now][level] = now.left.val - now.val': '删 `now`，左孩子 `{now.left.val}` 顶上来：这一层变化 `{now.left.val} - {now.val} = {now.left.val - now.val}`',
        'need_refresh[now].add(level)': '本层也要结算（孩子的 `need_refresh` 里只有更深的层）',
        'for lv in need_refresh[now]': lambda S, B, r: f"逐层结算：`now` 是==能删的节点==（至多一个孩子），待结算的层 `{sorted(S['need_refresh'][S['_inner']['now']])}`",
        'if remove_size[now][lv] < level_size[lv]': lambda S, B, r: (lambda n, lv: f"结算第 `{lv}` 层：共 `{S['level_size'][lv]}` 个节点，删掉 `{_dv(S, 'remove_size', n)[lv]}` 个：" + ('没删光 → 层和有效' if _dv(S, 'remove_size', n)[lv] < S['level_size'][lv] else '整层删光 → 不合法，跳过'))(S['_inner']['now'], S['lv']),
        'res = max(res, level_sum[lv] + delta[now][lv])': lambda S, B, r: _cand(S, S['_inner']['now'], S['lv'], '删掉'),
        'need_refresh[now] = set()': '这些层已经结算过了：清空，往上不用重复算',
        'dfs(now.left, level + 1)': '先递归左孩子',
        'dfs(now.right, level + 1)': '再递归右孩子',
        'need_refresh[now] = refresh_max': '两个孩子：把==较大的集合据为己有==，只遍历较小的那个 → 小到大合并 `O(n log n)`',
        'delta[now] = delta_max': '`delta` 同样：大的直接用，小的逐项合并进来',
        'delta[now][level] = now.left.val + now.right.val - now.val': '`{now.val}` 有两个孩子不能删；但它上面若有节点被删、子树上移，本层变化就是 `{now.left.val} + {now.right.val} - {now.val} = {now.left.val + now.right.val - now.val}`',
        'remove_size[now] = remove_max': '`remove_size` 也是大的挪用、小的累加',
        'return res': '全部合成完毕：最大层和 `res = {ret}`',
    },
    skip=['for now in q[head', 'if now.left:', 'if now.right:', 'level_sum.append(0)', 'q.append', 'global res', 'tail = 1', 'head = 0',
          'need_refresh = {}', 'remove_size = {}', 'if now.right is None', 'remove_size[now] = {level: 1}', 'need_refresh[now] = set()',
          'remove_size[now] = remove_size[now.', 'remove_size[now][level] = 1', 'need_refresh[now] = need_refresh[now.', 'need_refresh[now].add(level)',
          'if len(', 'refresh_min, refresh_max', 'delta_min, delta_max', 'remove_min, remove_max', 'for lv in refresh_min', 'need_refresh[now].add(lv)',
          'for lv in delta_min', 'delta[now][lv] = delta[now].get', 'for lv in remove_min', 'remove_size[now][lv] +=', 'else:', 'level_size = []', 'for lv in need_refresh[now]'],
    max_steps=80,
    cards=dict(
        one_liner='暴力是 O(n²)：用「大的挪用、小的合并」的哈希表优化到 O(n log n)',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给你一棵二叉树，每个节点有一个整数值（可为负）',
                 '最多可以做一次操作：删除一个==至多有一个孩子==的节点，它的孩子（子树）顶上来',
                 '删除后不能让某一层变成空；求操作后==所有层的层和的最大值==',
                 '本视频：`[1,3,2,-7,null,null,6]`，删掉节点 `2`，`6` 顶上来：第 1 层 `3+6=9`（原来最大是 5）'],
        quote='首先，对于不修改的情况，只需从根节点向下做一次层序遍历就行了。……记delta[now][level]为删除now之后对level这一层层和的影响，……可以直接使用浅拷贝，原封不动地将影响层数较多的那一侧的delta据为now所有。',
        quote_src='—— yiduobo 题解原文',
        idea=['不删：层序遍历得到 `level_sum`、`level_size`，作为初始答案',
              '删：对每个节点记 `delta`（各层层和的变化）、`need_refresh`（还没结算的层）、`remove_size`（各层被删数量）',
              '合并时把更大的哈希表直接据为己有，只遍历较小的 → 总共 `O(n log n)`',
              '`level_size` 用来排除「整层被删光」的非法情况'],
        result='运行结束，最大层和 `res = 9`',
        summary=['时间 `O(n log n)`（小到大合并），空间 `O(n)`',
                 '易错：删光整层不合法，所以要 `remove_size[now][lv] < level_size[lv]`',
                 '易错：有两个孩子的节点不能删，它的 `need_refresh` 要留到上面某个单孩子节点再结算',
                 '易错：直接 `delta[now] = delta[child]` 是引用不是拷贝，这正是复杂度优化所在',
                 '原文已是 Python 3 可运行的写法，未改动'],
    ),
)
