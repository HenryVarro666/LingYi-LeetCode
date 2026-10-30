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
    if i < k and isinstance(S.get('d'), tuple) and tuple(sorted(DOM[i])) == S['d']:
        return 'green'
    return None


def _dim(S, i, v):
    k = _k(S)
    return k is not None and i > k


def _txt(S):
    if 'cnt' not in S:
        return '旋转后相等 = ==排序后相等==：`[2,1]` 和 `[1,2]` 都变成 `(1, 2)`'
    k = _k(S)
    if k is None:
        return f"遍历结束，共 `ans = {S['ans']}` 对"
    d = S.get('d')
    if isinstance(d, tuple):
        return f"`{DOM[k]}` 排序后是 `{d}`，左边已有 `{S['cnt'].get(d, 0) - (S.get('_line') == 8)}` 张和它等价"
    return f"枚举右：`dominoes[{k}] = {d}`"


CONFIG = dict(
    num=1128, title='等价多米诺骨牌对的数量', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='排序归一 · 枚举右，维护左',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        ans = 0
        cnt = defaultdict(int)
        for d in dominoes:
            d = tuple(sorted(d))  # 只有两个数，排序是 O(1) 的
            ans += cnt[d]
            cnt[d] += 1
        return ans
''',
    setup=TRACK,
    call=f'Solution().numEquivDominoPairs(TList({DOM}))',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var=_cells, h=280, cell=130, pointers={_k: 'blue'}, pointer_labels={_k: 'd'},
             color=_color, dim=_dim, label='dominoes（蓝 = 当前骨牌 j，绿 = 左边和它等价的骨牌 i）'),
        dict(type='map', var='cnt', label='cnt（排序后的骨牌 → 出现次数）',
             fmt=lambda k, v: f'({k[0]},{k[1]}): {v}', h=170, font=34),
    ],
    watch=[('d', 'd', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans`：等价骨牌对的数量',
        'cnt = defaultdict': '`cnt[d]`：左边（已遍历）每种骨牌的出现次数',
        'for d in dominoes': lambda S, B, r: (f'枚举右：`d = dominoes[{_k(S)}] = {S.d}`' if _k(S) is not None
                                              else '所有骨牌遍历完毕'),
        'd = tuple(sorted(d))': lambda S, B, r: (f'排序：`{B.d}` → `{S.d}`，旋转 180° 的骨牌变成同一个 key'
                                                 if list(S.d) != B.d else f'`{B.d}` 已经有序 → `{S.d}`'),
        'ans += cnt[d]': lambda S, B, r: (f'左边有 `cnt[{S.d}] = {S.ans - B.ans}` 张等价骨牌，各配一对 → `ans` = =={S.ans}=='
                                          if S.ans != B.ans else f'左边没有 `{S.d}`，`ans` 不变'),
        'cnt[d] += 1': '==再==把自己记进去：`cnt[{d}] = {cnt[d]}`（先加会和自己配对）',
        'return ans': '返回 =={ans}==',
    },
    cards=dict(
        one_liner='把每张骨牌排好序，就变成 1512 好数对的数目',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['骨牌 `[a,b]` 与 `[c,d]` 等价：==相同或旋转 180° 后相同==',
                 '求 `i < j` 且 `dominoes[i]`、`dominoes[j]` 等价的对数',
                 '示例：`[[1,2],[1,2],[1,1],[1,2],[2,2]]` → `3`'],
        quote='本题要求 i<j，如果==先更新 cnt，再更新答案==，就把 dominoes[j] 自己也统计进来了，相当于把 i=j 的情况也认为是好数对。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`[1,2]` 和 `[2,1]` 本质相等：保证 `a ≤ b`（排序）后用作 key',
              '思路同 49. 字母异位词分组：排序后相等就是一类',
              '枚举右 `j`，`ans += cnt[d]`，再 `cnt[d] += 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：==先加答案，再更新 cnt==，否则多算了 `i = j`',
                 '数值 ≤ 9，也可以用 `10 × 10` 的数组代替哈希表',
                 '同类：1512 好数对的数目、题单「§0.1 枚举右，维护左」'],
    ),
)
