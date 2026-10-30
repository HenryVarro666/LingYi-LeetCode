CONFIG = dict(
    num=3740, title='三个相等元素之间的最小距离 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表记上两次位置', tags=[],
    code='''
class Solution(object):
    def minimumDistance(self, nums):
        
        p1 = {}
        p2 = {}
        res = -1

        for index, v in enumerate(nums):
            if p2.get(v, None) is not None:
                dis = (index - p2[v]) * 2
                if res == -1 or res > dis:
                    res = dis
            
            p2[v], p1[v] = p1.get(v, None), index
        
        return res
''',
    call='Solution().minimumDistance([1,2,1,1,3])',
    expect=6,
    views=[
        dict(type='array', var='nums', h=200, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and 'v' in S and v == S['v'] and i <= S['index'] else None),
        dict(type='map', var='p1', h=160, label='p1：每个值上一次出现的位置'),
        dict(type='map', var='p2', h=160, label='p2：每个值上上次出现的位置'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('dis', 'dis', 'orange'), ('res', 'res', 'green')],
    captions={
        'p1 = {}': '`p1` 记每个值上一次的位置',
        'p2 = {}': '`p2` 记每个值上上次的位置',
        'res = -1': '`res = -1` 表示还没找到有效三元组',
        'if p2.get': lambda S, B, r: (f'`p2[{S.v}]` = `{S.p2.get(S.v)}`：已有两次出现，加上当前共三个 → 能组成三元组' if S.p2.get(S.v) is not None
                                      else f'`{S.v}` 之前出现不足两次，凑不成三个'),
        'dis = (': '最左 `{p2[v]}`、最右 `{index}`：距离 = `({index} − {p2[v]}) × 2` = =={dis}==',
        'if res == -1': lambda S, B, r: f'`res = {S.res}`，`dis = {S.dis}`：' + ('还没有答案或更小 → 更新' if (S.res == -1 or S.res > S.dis) else '不比现有答案小 → 保持'),
        'res = dis': '`res` 更新为 `{res}`',
        'p2[v], p1[v]': '把 `{v}` 的记录往后挪：上上次 `{p2[v]}`，上一次 `{p1[v]}`',
        'return res': '最小距离 `{res}`',
    },
    cards=dict(
        one_liner='距离 = 2×(最右−最左)，只看同值的连续三个位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['三个下标 `i,j,k` 不同且值相等，距离为 `|i−j|+|j−k|+|k−i|`',
                 '求所有有效三元组的最小距离，没有则 `-1`',
                 '示例：`[1,2,1,1,3]` → `6`（下标 0, 2, 3）'],
        quote='将三个绝对值拆开，就可以得到三元组的距离为……2 * (k - i)，即三元组中最左侧和最右侧距离的两倍。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `i<j<k`，拆绝对值后距离 `= 2(k−i)`，中间的 `j` 不影响',
              '要让 `k−i` 小，三个下标必须是该值所有下标中 ==连续的三个==',
              '用 `p1`、`p2` 存上一次、上上次位置，遍历时直接算'],
        summary=['时间 `O(n)`，空间 `O(n)`；II 数据更大，同样的做法也能过',
                 '更新顺序：先用旧的 `p2[v]` 算距离，再挪动 `p2`、`p1`',
                 '`res = -1` 作为「未找到」标记，所以比较时要先判 `res == -1`',
                 '距离是 `2×(index − p2[v])`，别忘了乘 2'],
    ),
)
