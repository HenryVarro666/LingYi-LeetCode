def _idx(S):
    if 'cnt' not in S or 'x' not in S:
        return -1
    n = sum(S['cnt'].values())
    return n - 1 if S['_line'] >= 6 else n


def _col(S, i, v):
    k = _idx(S)
    if k < 0:
        return None
    if i == k:
        return 'blue'
    if i < k:
        return 'green' if S['cnt'].get(v, 0) == S.get('max_cnt', 0) and S.get('max_cnt', 0) > 0 else None
    return None


def _dim(S, i, v):
    return _idx(S) >= 0 and i > _idx(S)


def _txt(S):
    if 'max_cnt' not in S:
        return '边遍历边统计：`cnt` 记次数，`max_cnt` 记目前最大次数，`ans` 记答案'
    return f"`max_cnt = {S['max_cnt']}`：绿色 = 当前次数等于最大次数的元素，`ans = {S['ans']}` = 它们的总个数"


CONFIG = dict(
    num=3005, title='最大频率元素计数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表一次遍历 · 维护最大次数',
    code='''
class Solution:
    def maxFrequencyElements(self, nums: List[int]) -> int:
        cnt = defaultdict(int)
        ans = max_cnt = 0
        for x in nums:
            cnt[x] += 1
            c = cnt[x]
            if c > max_cnt:
                ans = max_cnt = c
            elif c == max_cnt:
                ans += c
        return ans
''',
    call='Solution().maxFrequencyElements([1,2,2,3,1,4])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', color=_col, dim=_dim, h=200),
        dict(type='map', var='cnt', h=240, fmt=lambda k, v: f'{k} : {v}'),
    ],
    watch=[('x', 'x', 'blue'), 'c', ('max_cnt', 'max_cnt', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 统计每个数出现的次数',
        'ans = max_cnt = 0': '`ans`（答案）和 `max_cnt`（最大次数）都从 0 开始',
        'for x in nums': lambda S, B, r: ('`nums` 遍历完了，准备返回' if sum(S.cnt.values()) == len(S.nums)
                                          else f'取下一个数 `x = {S.x}`'),
        'cnt[x] += 1': '`x = {x}` 出现一次：`cnt[{x}] = {cnt[x]}`',
        'c = cnt[x]': '取出 `x` 当前的次数 `c = {c}`',
        'if c > max_cnt': lambda S, B, r: (f'`c = {S.c} > max_cnt = {S.max_cnt}`：==出现了更高的频率== → 之前的答案作废'
                                           if S.c > S.max_cnt else f'`c = {S.c} > max_cnt = {S.max_cnt}`？不成立，再看是否相等'),
        'ans = max_cnt = c': '重置：`max_cnt = {max_cnt}`，`ans = {ans}`（目前只有 `x` 这一个数达到最大次数）',
        'elif c == max_cnt': lambda S, B, r: (f'`c = {S.c} == max_cnt`：==又一个数达到最大次数=='
                                              if S.c == S.max_cnt else f'`c = {S.c} < max_cnt = {S.max_cnt}`：还没追上，不影响答案'),
        'ans += c': '`ans += {c}` → {ans}（这个数的全部 {c} 个都算上）',
        'return ans': '答案：`{ans}`',
    },
    cards=dict(
        one_liner='边数边维护：更大就重置答案，一样大就累加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['统计每个元素的出现次数，找到 ==最大频率==',
                 '返回所有达到最大频率的元素的 ==总个数==（不是元素种数）',
                 '示例：`[1,2,2,3,1,4]` → 1 和 2 都出现 2 次 → `4`'],
        quote='遍历 nums，同时用哈希表统计每个元素的出现次数，并维护出现次数的最大值 maxCnt：如果出现次数 c > maxCnt，那么更新 maxCnt = c，答案 ans = c。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`c > max_cnt`：出现新的最高频率，答案重置为 `c`',
              '`c == max_cnt`：又一个元素追平，答案增加 `c`',
              '次数只会逐个增加，所以不用最后再扫一遍哈希表'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`ans += c` 加的是次数 `c`，不是 1',
                 '次数 +1 后才比较，所以同一个元素不会被重复累加',
                 '也可以先 `Counter` 再扫一遍，这里是一次遍历的写法'],
    ),
)
