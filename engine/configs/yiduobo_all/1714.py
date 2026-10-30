def _color(S, i, v):
    if 'seq_begin' not in S or S.get('_line', 0) < 6 or 'x' not in S:
        return None
    y, sb, x = S['y'], S['seq_begin'], S['x']
    if i % y == sb:
        if i >= x and S.get('_line', 0) >= 19:
            return 'orange'
        return 'blue'
    return None


def _txt(S):
    if 'seq_begin' not in S or S.get('_line', 0) < 6 or 'x' not in S:
        return ''
    ln = S['_line']
    x, y, sb = S['x'], S['y'], S['seq_begin']
    seq = [S['nums'][j] for j in range(sb, len(S['nums']), y)]
    t = f'询问 `({x}, {y})`：下标模 {y} 余 {sb} 的数 `{seq}`'
    if ln >= 19 and 'query_begin' in S:
        t += f'，从第 `{S["query_begin"]}` 项起（橙）'
    return t


CONFIG = dict(
    num=1714, title='数组中特殊等间距元素的和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按余数分组 · 前缀和 + 缓存',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def solve(self, nums, queries):
        s_dict = {}
        res = []
        mod = 10 ** 9 + 7
        for x, y in queries:
            seq_begin = x % y
            key = (y, seq_begin)
            if key not in s_dict:
                s_dict[key] = []
                now = 0
                for index in range(seq_begin, len(nums), y):
                    now += nums[index]
                    if now >= mod:
                        now -= mod
                    s_dict[key].append(now)
            
            res.append(s_dict[key][-1])
            query_begin = x // y
            if query_begin > 0:
                res[-1] -= s_dict[key][query_begin - 1]
                if res[-1] < 0:
                    res[-1] += mod
        return res
''',
    call='Solution().solve([0, 1, 2, 3, 4, 5, 6, 7], [[1, 3], [4, 3], [5, 2]])',
    expect=[12, 11, 12],
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='nums', label='nums（蓝 = 同余序列，橙 = 询问要加的后缀）', h=190, color=_color),
        dict(type='map', var='s_dict', fmt=lambda k, v: f'(y={k[0]}, 余{k[1]}) → {v}', h=230),
        dict(type='array', var='res', label='res', h=130, cell=70),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('seq_begin', 'seq_begin', 'yellow'), ('query_begin', 'query_begin', 'orange')],
    captions={
        's_dict = {}': '`s_dict[(y, 余数)]`：缓存每条同余序列的==前缀和==，重复询问不用重算',
        'mod = ': '结果对 `10^9 + 7` 取模',
        'for x, y in queries': lambda S, B, r: (f'询问 `({S.x}, {S.y})`：要加 `nums[x], nums[x+y], nums[x+2y] …`' if len(S.res) < len(S.queries) and not (S.x, S.y) == tuple(S.queries[-1]) or len(S.res) < len(S.queries) else '询问都处理完了'),
        'seq_begin = x % y': '这些下标模 `{y}` 都等于 `x % y = {seq_begin}` → 它们在同一条序列里，序列从下标 `{seq_begin}` 起',
        'key = (y, seq_begin)': '序列的名字 `key = {key}`',
        'if key not in s_dict': lambda S, B, r: ('这条序列还没算过 → 现在算前缀和' if S.key not in S.s_dict else f'`{S.key}` 已经在缓存里 → 直接用，不重算'),
        's_dict[key] = []': '新建 `{key}` 的前缀和列表',
        'now += nums[index]': '沿序列（下标每次 +{y}）走到 `{index}`：加上 `nums[{index}] = {nums[index]}` → 前缀和 `now = {now}`',
        'now >= mod': '', 
        's_dict[key].append(now)': '前缀和记入 `{key}`：`{s_dict[key]}`',
        'res.append(s_dict[key][-1])': '先取整条序列的总和 `{s_dict[key][-1]}`（相当于从第 0 项开始加）',
        'query_begin = x // y': '`x` 是序列里的第 `x // y = {query_begin}` 项（从 0 数）：前面 {query_begin} 项不该加',
        'if query_begin > 0': lambda S, B, r: (f'`query_begin = {S.query_begin} > 0` → 要减去前 {S.query_begin} 项的前缀和' if S.query_begin > 0 else '`query_begin = 0`：从头开始加，不用减'),
        'res[-1] -= s_dict[key][query_begin - 1]': '减去前缀和 `s_dict[key][{query_begin - 1}] = {s_dict[key][query_begin - 1]}` → `res[-1] = {res[-1]}`（前缀和之差 = 后缀和）',
        'if res[-1] < 0': lambda S, B, r: (f'`{S.res[-1]} < 0` → 加回 `mod` 保持非负' if S.res[-1] < 0 else '结果非负，不用补'),
        'res[-1] += mod': '`res[-1] = {res[-1]}`',
        'return res': '返回 `{res}`',
    },
    skip=['for index in range(seq_begin', 'now >= mod', 'now -= mod', 'now = 0', 'res = []', 'mod = '],
    max_steps=80,
    cards=dict(
        one_liner='按余数分组：一条序列算一次前缀和，询问用前缀和之差',
        complexity='时间 `O(n·√n)`，空间 `O(n·√n)`（最坏）',
        problem=['`queries[i] = [x, y]`：求 `nums[j]` 的和，`j ≥ x` 且 `(j - x) % y == 0`，结果对 `10^9+7` 取模',
                 '也就是从下标 `x` 起，每隔 `y` 取一个数再求和',
                 '示例：`nums=[0,1,2,3,4,5,6,7]`，`[[1,3],[4,3],[5,2]]` → `[12, 11, 12]`'],
        quote='对于一个给定的y而言，按照对y的余数一共可以分成y条序列，而每一组询问(x, y)就是询问所有对y取余的值为x % y的数的某个后缀和。对于这个问题，可以直接计算后缀和，也可以计算前缀和然后通过前缀和之差得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(y, x % y)` 唯一决定一条序列，用哈希表缓存它的前缀和',
              '`x` 是序列里的第 `x // y` 项：总和减去前 `x // y` 项就是答案',
              '最坏复杂度：`y` 越大序列越短，所有 `y` 加起来 `O(n·√n)`'],
        summary=['缓存键 `(y, x % y)`；同一条序列的多个询问只算一次',
                 '减出负数要加回 `mod`，别忘了取模',
                 '原文为 Python 2 写法，`x / y` 整数除法已改为 `x // y`',
                 '这是 VIP 题，思路与「根号分治」同类：`y` 小用缓存，`y` 大直接跳着加'],
    ),
)
