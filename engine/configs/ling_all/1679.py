NUMS, K = [3, 1, 3, 4, 3, 2, 3], 6

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


def _sim(m):
    """前 m 个数处理完后：哪些下标已被配对"""
    cnt, wait, used = {}, {}, set()
    for i, x in enumerate(NUMS[:m]):
        if cnt.get(K - x, 0):
            cnt[K - x] -= 1
            used.add(wait[K - x].pop(0))
            used.add(i)
        else:
            cnt[x] = cnt.get(x, 0) + 1
            wait.setdefault(x, []).append(i)
    return used


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _done(S):
    k = _k(S)
    if k is None:
        return len(NUMS) if 'ans' in S and S.get('_line') != 4 else 0
    return k + 1 if S.get('_line') in (7, 8, 10) else k


def _color(S, i, v):
    k = _k(S)
    if k is not None and i == k:
        return 'blue'
    if i in _sim(_done(S)):
        return 'green'
    return None


def _dim(S, i, v):
    k = _k(S)
    return k is not None and i > k


def _txt(S):
    k = _k(S)
    if k is None or 'x' not in S:
        return f'`k = {K}`：每个数先找哈希表里有没有能和它凑成 k 的 =={K} − x=='
    x = S['x']
    return f"`x = {x}`，需要 `k − x = {K - x}`；哈希表里有 `{S['cnt'].get(K - x, 0)}` 个，已配成 `{S['ans']}` 对"


CONFIG = dict(
    num=1679, title='K 和数对的最大数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希表计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1346'],
    code='''
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        ans = 0
        for x in nums:
            if cnt[k - x]:
                cnt[k - x] -= 1
                ans += 1
            else:
                cnt[x] += 1
        return ans
''',
    setup=TRACK,
    call=f'Solution().maxOperations(TList({NUMS}), {K})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=280, cell=110, pointers={_k: 'blue'}, pointer_labels={_k: 'x'},
             color=_color, dim=_dim, label='nums（蓝 = 当前 x，绿 = 已经配对移出）'),
        dict(type='map', var='cnt', label='cnt（还没配上对的数 → 个数；值为 0 的键是 defaultdict 查询时建的）',
             fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
    ],
    watch=[('x', 'x', 'blue'), 'k', ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt`：左边==还没配上对==的数及其个数',
        'ans = 0': '`ans`：操作次数',
        'for x in nums': lambda S, B, r: (f'遍历到 `x = {S.x}`' if _k(S) is not None else '遍历结束'),
        'if cnt[k - x]': lambda S, B, r: (f'`cnt[{S.k} − {S.x}] = cnt[{S.k - S.x}] = {S.cnt[S.k - S.x]}`：左边有 {S.k - S.x} 在等 → ==配对=='
                                          if S.cnt[S.k - S.x] else
                                          f'`cnt[{S.k - S.x}] = 0`：左边没有 {S.k - S.x}，配不上'),
        'cnt[k - x] -= 1': '从哈希表中去掉一个 `{k - x}`：`cnt[{k - x}] = {cnt[k - x]}`',
        'ans += 1': '`{k - x} + {x} = {k}`，移出这一对，`ans = {ans}`；==x 不进哈希表==',
        'cnt[x] += 1': '把 `{x}` 放进哈希表等后面的数：`cnt[{x}] = {cnt[x]}`',
        'return ans': '最多操作 =={ans}== 次',
    },
    cards=dict(
        one_liner='和两数之和一样：先查 k − x，有就配对删掉，没有就把 x 存起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次从 `nums` 中选出==和为 k== 的两个数移出数组',
                 '求最多能执行多少次操作',
                 '示例：`[3,1,3,4,3], k = 6` → `1`；本视频 `[3,1,3,4,3,2,3]` → `3`'],
        quote='每次先看看哈希表中是否有 k−nums[i]，有就==去掉哈希表中的一个 k−nums[i]==，同时把答案加一，没有就把 nums[i] 加入哈希表。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右遍历，哈希表存「还没配对」的数及个数',
              '配上对时 `x` 不加入哈希表：它已经被用掉了',
              '每个数只会被用一次，贪心配对即可得到最大次数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：配对后==不要==再 `cnt[x] += 1`',
                 '`defaultdict` 查询 `cnt[k - x]` 会建出值为 0 的键，不影响结果',
                 '同类：1. 两数之和、题单「§0.1 枚举右，维护左」'],
    ),
)
