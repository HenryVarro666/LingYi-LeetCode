def _paths(nd, pre=()):
    out = []
    if nd.weight:
        out.append(f"{list(pre)} ×{nd.weight}")
    for k, c in nd.childs.items():
        out += _paths(c, pre + (k,))
    return out


def _trie_txt(S):
    if 'root' not in S:
        return ''
    ps = _paths(S['root'])
    return 'trie 里存的行（路径 × 出现次数）：' + ('；'.join(ps) if ps else '（空）') + (f"　当前节点 weight = =={S['now'].weight}==" if 'now' in S else '')


CONFIG = dict(
    num=2352, title='相等行列对', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='Trie 树（行入树，列查树）',
    tags=[],
    code='''
class Node(object):

    def __init__(self):
        self.childs = {}
        self.weight = 0

class Solution(object):
    def equalPairs(self, grid):
        n = len(grid)
        root = Node()
        for i in range(n):
            now = root
            for j in range(n):
                if grid[i][j] not in now.childs:
                    now.childs[grid[i][j]] = Node()
                now = now.childs[grid[i][j]]
            
            now.weight += 1
        
        res = 0
        for j in range(n):
            now = root
            for i in range(n):
                if grid[i][j] not in now.childs:
                    break
                now = now.childs[grid[i][j]]
            
            res += now.weight
        
        return res
''',
    call='Solution().equalPairs([[2,1,2],[1,3,3],[2,1,2]])',
    expect=2,
    views=[
        dict(type='grid', var='grid', label='grid', h=230, cell=100,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='text', h=150, size=28, fn=_trie_txt),
        dict(type='text', h=70, size=30, fn=lambda S: f"`res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'root = Node()': '建一棵空 trie：每个数字是一条边，一整行 = 一条从根出发的路径',
        14: '第 `{i}` 行第 `{j}` 个数 `{grid[i][j]}`：{"这条边还不存在 → 新建一个节点" if grid[i][j] not in now.childs else "边已存在 → 共用前缀"}，再沿它往下走',
        18: '第 `{i}` 行走完，在终点记一笔：这种行共出现 `{now.weight}` 次',
        24: '第 `{j}` 列的第 `{i}` 个数 `{grid[i][j]}`：{"这条边不存在 → 没有与这一列相同的行，break" if grid[i][j] not in now.childs else "边存在 → 沿着往下走"}',
        25: '没有这条边：此列不匹配任何行，`now` 停在中间节点，`weight` 为 0',
        28: '这一列贡献 `{now.weight}` 对（终点的 weight），`res` = =={res}==',
    },
    skip=['self.childs = {}', 'self.weight = 0', 'for i in range', 'for j in range', 'now = root', 'now = Node', 'now.childs[grid[i][j]] = Node()', 'now = now.childs', 'res = 0'],
    max_steps=110,
    cards=dict(
        one_liner='把每行当字符串塞进 trie，再让每一列去 trie 里走一遍',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n x n` 矩阵，求行 `R_i` 与列 `C_j` 完全相同的 `(i, j)` 对数',
                 '相同 = 元素和顺序都一样',
                 '示例：`[[2,1,2],[1,3,3],[2,1,2]]` → `2`（第 0、2 行与第 0 列相同）'],
        quote='我在这里采用的是trie树，同样是枚举行，将行视为字符串，每个格子上的数字视为字符，然后将其加入到trie树中。接下来再枚举列，通过trie树判断与其相同的行的数目并更新答案。',
        quote_src='—— yiduobo 题解',
        idea=['行入树：每行是一条从根出发的路径，终点 `weight` 加 1',
              '列查树：按列从上到下走，沿途边不存在就 `break`',
              '走到终点时的 `weight` 就是与这一列相同的行数'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错点：中途 `break` 后 `now` 停在内部节点，其 `weight` 为 0，所以直接累加是安全的',
                 '原文提到也可以暴力枚举或用哈希表，作者选择了 trie'],
    ),
)
