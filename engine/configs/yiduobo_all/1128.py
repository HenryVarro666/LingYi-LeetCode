DOM = [[1, 2], [2, 1], [3, 4], [1, 2], [2, 2], [4, 3]]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('dominoes'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _cells(S):
    d = S.get('dominoes')
    if d is None:
        return None
    return [f'{a}|{b}' for a, b in d]


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    return None


def _dim(S, i, v):
    k = _k(S)
    if 'res' in S:
        return True
    return k is not None and i > k


def _txt(S):
    if 'res' in S:
        c = S.get('cnt')
        if isinstance(c, int) and S.get('_line') in (12, 13):
            return f"`{c}` 张等价骨牌两两配对：`C({c}, 2) = {c} × {c - 1} // 2 = {c * (c - 1) // 2}`"
        return f"第二步：按种类算对数，`res = {S['res']}`"
    if 'f' not in S:
        return '第一步：哈希表统计==每种骨牌==出现几次'
    if 'key' in S and S.get('_line') in (7, 8):
        return f"`x = {S['x']}, y = {S['y']}` → `key = {S['x']} × 10 + {S['y']} = {S['key']}`"
    return '第一步：哈希表统计==每种骨牌==出现几次'


CONFIG = dict(
    num=1128, title='等价多米诺骨牌对的数量', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希计数 · k×(k−1)/2',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def numEquivDominoPairs(self, dominoes):

        f = {}
        for x, y in dominoes:
            if x > y:
                x, y = y, x
            key = x * 10 + y
            f[key] = f.get(key, 0) + 1

        res = 0
        for cnt in f.values():
            res += (cnt - 1) * cnt // 2
        return res
''',
    setup=TRACK,
    call=f'Solution().numEquivDominoPairs(TList({DOM}))',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var=_cells, h=280, cell=130, pointers={_k: 'blue'}, pointer_labels={_k: '当前'},
             color=_color, dim=_dim, label='dominoes'),
        dict(type='map', var='f', label='f（key = 小数 × 10 + 大数 → 出现次数）',
             fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
    ],
    watch=['x', 'y', 'key', 'cnt', ('res', 'res', 'green')],
    captions={
        'f = {}': '`f`：每种骨牌出现的次数',
        'for x, y in dominoes': lambda S, B, r: (f'取出骨牌 `[{S.x}, {S.y}]`' if _k(S) is not None
                                                 else '统计完毕，接下来按种类计算'),
        'if x > y': lambda S, B, r: (f'`{S.x} > {S.y}`：需要交换，保证 ==a ≤ b==' if S.x > S.y
                                     else f'`{S.x} ≤ {S.y}`：已经是小数在前'),
        'x, y = y, x': '交换 → `[{x}, {y}]`，旋转后的骨牌和原来变成同一种',
        'key = x * 10 + y': '数值都在 1–9：`key = {x} × 10 + {y} = {key}`，==一个两位数==唯一表示一种骨牌',
        'f[key] = f.get': '`f[{key}]` 计数加一 → {f[key]}',
        'res = 0': '`res = 0`',
        'for cnt in f.values()': lambda S, B, r: (f'这一种骨牌有 `cnt = {S.cnt}` 张' if S.cnt != B.get('cnt') or S.res == 0 and B.get('cnt') is None
                                                  else '所有种类都算完了'),
        'res += (cnt - 1)': lambda S, B, r: (f'`{S.cnt}` 张两两配对：`({S.cnt} − 1) × {S.cnt} // 2 = {S.res - B.res}`，'
                                             f'`res` = =={S.res}=='),
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='先统计每种骨牌的张数，k 张能组成 k(k−1)/2 对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['骨牌 `[a,b]` 与 `[c,d]` 等价：==相同或旋转 180° 后相同==',
                 '求 `i < j` 且 `dominoes[i]`、`dominoes[j]` 等价的对数',
                 '示例：`[[1,2],[2,1],[3,4],[5,6]]` → `1`'],
        quote='设其等价的多米诺骨牌一共有k张，那么就可以形成==k * (k - 1) / 2组==等价的多米诺骨牌对。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表统计每种骨牌出现的次数，最后按种类算组合数',
              '哈希方式：数值在 1–9，用 `a × 10 + b` 当 key，并==确保 a ≤ b==',
              '`[2,1]` 交换成 `[1,2]`，key 都是 `12`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两遍：先计数，再对每种求 `C(k, 2)`',
                 '`a × 10 + b` 只在数值 ≤ 9 时不冲突',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`'],
    ),
)
