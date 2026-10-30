ARR = [1, 2, 3, 3, 3, 4, 3]


def _wl(S):
    if 'i' not in S:
        return None
    return max(0, S['i'] - S['w'] + 1)


def _acol(S, i, v):
    if 'i' not in S or i > S['i']:
        return None
    if v == 0:
        return 'red'
    return 'cyan' if i >= _wl(S) else None


def _adim(S, i, v):
    return 'i' in S and i < _wl(S)


def _ccol(S, i, v):
    if 'x' in S and i == S['x'] and i > 0:
        return 'orange' if v >= S['m'] else 'yellow'
    return None


def _txt(S):
    if 'i' not in S:
        return '规则：任意连续 `w` 天里，每种物品最多保留 `m` 个'
    l = _wl(S)
    kept = [v for v in S['arrivals'][l:S['i'] + 1] if v]
    return f"窗口第 `{l + 1}..{S['i'] + 1}` 天保留的物品：`{kept}`，已丢弃 =={S['ans']}== 个"


CONFIG = dict(
    num=3679, title='使库存平衡的最少丢弃次数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='贪心（能留就留）+ 定长滑窗',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1639'],
    code='''
class Solution:
    def minArrivalsToDiscard(self, arrivals: List[int], w: int, m: int) -> int:
        cnt = [0] * (max(arrivals) + 1)  # 或者用 defaultdict(int)
        ans = 0
        for i, x in enumerate(arrivals):
            # x 进入窗口
            if cnt[x] == m:  # x 的个数已达上限
                # 注意 x 在未来要离开窗口，但由于已经丢弃，不能在离开窗口时修改 cnt
                # 这里直接置为 0，未来离开窗口就是 cnt[0]--，不影响判断条件
                arrivals[i] = 0  # 丢弃 arrivals[i]
                ans += 1
            else:
                cnt[x] += 1

            # 左端点元素离开窗口，为下一个循环做准备
            left = i + 1 - w
            if left >= 0:
                cnt[arrivals[left]] -= 1
        return ans
''',
    call=f'Solution().minArrivalsToDiscard({ARR}, 3, 2)',
    expect=1,
    views=[
        dict(type='array', var='arrivals', label='arrivals（框 = 最近 w 天，红 0 = 已丢弃）', h=240, cell=100,
             pointers={'i': 'blue', 'left': 'pink'}, window=(_wl, 'i'), color=_acol, dim=_adim),
        dict(type='array', var='cnt', label='cnt[类型] = 窗口内保留的个数（cnt[0] 记丢弃的，不用管）', h=200, cell=90,
             color=_ccol),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('left', 'left', 'pink'), ('m', 'm'), ('ans', 'ans', 'red')],
    captions={
        'cnt = [0]': '`cnt[x]`：窗口中类型 x ==保留下来==的个数',
        'ans = 0': '`ans`：丢弃次数',
        'for i, x in enumerate': lambda S, B, ret: (f'第 `{S.i + 1}` 天到达物品 `x = {S.x}`，进入窗口'
                                                    if 'i' not in B or S.i != B.i else '遍历结束'),
        'if cnt[x] == m': lambda S, B, ret: (f'`cnt[{S.x}] = {S.cnt[S.x]} == m`：窗口里 {S.x} 已经满了，==不得不丢==' if S.cnt[S.x] == S.m
                                             else f'`cnt[{S.x}] = {S.cnt[S.x]} < m = {S.m}`：还能放，==能留就留==（晚丢更好）'),
        'arrivals[i] = 0': '把 `arrivals[{i}]` 改成 0：将来它离开窗口时只会改 `cnt[0]`，==不影响真实计数==',
        'ans += 1': '丢弃次数 `ans = {ans}`',
        'cnt[x] += 1': '保留它：`cnt[{x}]` → `{cnt[x]}`',
        'left = i + 1 - w': '下一轮窗口要去掉左端点 `left = {i} + 1 − {w} = {left}`',
        'if left >= 0': lambda S, B, ret: (f'`left = {S.left} < 0`：窗口还不满 {S.w} 天，没人离开' if S.left < 0
                                           else (f'第 `{S.left + 1}` 天的物品已被丢弃（标记为 0），离开窗口' if S.arrivals[S.left] == 0
                                                 else f'第 `{S.left + 1}` 天的物品 `{S.arrivals[S.left]}` 离开窗口')),
        'cnt[arrivals[left]] -= 1': lambda S, B, ret: (f'`cnt[{S.arrivals[S.left]}]` 减一 → `{S.cnt[S.arrivals[S.left]]}`'
                                                       + ('（它早被丢弃，减的是 `cnt[0]`）' if S.arrivals[S.left] == 0 else '')),
        'return ans': '最少丢弃 =={ans}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='能留就留，非丢不可时才丢：晚丢更好',
        complexity='时间 `O(n + U)`，空间 `O(n + U)`（U = max(arrivals)）',
        problem=['`arrivals[i]` 是第 i+1 天到达的物品类型，只能在到达当天决定保留或丢弃',
                 '要求任意连续 `w` 天里，每种类型最多保留 `m` 个；求最少丢弃数',
                 '示例：`[1,2,3,3,3,4], w = 3, m = 2` → `1`（丢第 5 天的 3）',
                 '本视频：`[1,2,3,3,3,4,3], w = 3, m = 2` → `1`'],
        quote='晚丢更好，如果后面还有更多的 x，那么==晚丢会让窗口中的 x 的个数比早丢更少==，后面丢弃的物品数更少。',
        quote_src='—— 灵茶山艾府题解',
        idea=['x 进窗口时 `cnt[x] == m`：丢掉它，`ans += 1`',
              '否则保留，`cnt[x] += 1`；左端点离开时 `cnt` 减一',
              '易错：被丢弃的物品离开窗口时==不能==再减 `cnt[x]` → 把它改成 0'],
        summary=['时间 `O(n + U)`，空间 `O(n + U)`；也可以用 `defaultdict(int)`',
                 '一开始长度 `1..w−1` 的窗口也要检查是否需要丢弃',
                 '`arrivals[i] = 0` 是「标记删除」，也可以另开布尔数组',
                 '定长滑窗模板：入 → 更新答案 → 出'],
    ),
)
