ENV = [[5, 4], [6, 4], [6, 7], [2, 3], [4, 5], [4, 6]]


def _cur(S):
    if '_' not in S or 'h' not in S or 'envelopes' not in S:
        return -1
    try:
        return S['envelopes'].index([S['_'], S['h']])
    except ValueError:
        return -1


def _hcol(S, i, v):
    return 'yellow' if i == _cur(S) else None


def _text(S):
    if 'g' not in S:
        return '先排序：==宽度升序==；宽度相同时==高度降序=='
    if 'j' not in S or 'h' not in S or S.get('_line') not in (9, 10, 11, 13):
        return '`g[k]` = 长为 `k+1` 的严格递增子序列的==最小末尾=='
    g, h, j = S['g'], S['h'], S['j']
    return f'`h = {h}`：`bisect_left(g, {h})` = =={j}==（g 中第一个 `≥ {h}` 的位置）'


def _if(S, B, ret):
    j, g, h = S.j, S.g, S.h
    if j < len(g):
        if g[j] == h:
            return f'`j = {j} < len(g)`：`g[{j}]` 已经等于 {h} → 替换后不变（严格递增不能接在相等的后面）'
        return f'`j = {j} < len(g) = {len(g)}`：`g[{j}] = {g[j]} ≥ {h}` → 用更小的 {h} ==替换==，末尾越小越好接'
    return f'`j = {j} == len(g)`：{h} 比 g 里所有数都大 → 接在最后，==LIS 变长=='


def _for(S, B, ret):
    if 'h' in S and (B.get('h') != S['h'] or B.get('_') != S['_']):
        return f'取出信封 `[{S["_"]}, {S["h"]}]`：只看高度 `h = {S["h"]}`'
    return '所有信封处理完毕'


CONFIG = dict(
    num=354, title='俄罗斯套娃信封问题', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='双关键字排序 + LIS 二分',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        # 双关键字排序：宽度升序，高度降序
        envelopes.sort(key=lambda e: (e[0], -e[1]))

        # 300. 最长递增子序列
        g = []
        for _, h in envelopes:
            j = bisect_left(g, h)
            if j < len(g):
                g[j] = h
            else:
                g.append(h)
        return len(g)
''',
    call=f'Solution().maxEnvelopes({ENV!r})',
    expect=3,
    views=[
        dict(type='array', var=lambda S: [e[0] for e in S['envelopes']], label='宽度 w（排序后升序）', h=150, cell=80,
             color=lambda S, i, v: 'yellow' if i == _cur(S) else None),
        dict(type='array', var=lambda S: [e[1] for e in S['envelopes']], label='高度 h（同宽时降序 → 同宽至多选一个）', h=150, cell=80,
             color=_hcol),
        dict(type='text', fn=_text, size=26, h=60),
        dict(type='array', var='g', label='g：g[k] = 长为 k+1 的递增子序列的最小末尾', h=200, cell=80, min_slots=6,
             pointers={'j': 'pink'}, color=lambda S, i, v: 'green' if S.get('_line') in (11, 13) and i == S.get('j') else None),
    ],
    watch=[('w', '_'), ('h', 'h'), ('j', 'j', 'pink'), ('len(g)', 'len(g)', 'green')],
    captions={
        'envelopes.sort': '宽度升序；==同宽度按高度降序== → 同宽的高度在 h 里是降序，LIS 至多选一个',
        'g = []': '剩下的就是对 h 求==严格==递增子序列（300 题），`g` 存最小末尾',
        'for _, h in': _for,
        'j = bisect_left': '`bisect_left(g, {h})` = `{j}`：==严格递增==所以找第一个 `≥ h` 的位置',
        'if j < len(g)': _if,
        'g[j] = h': '`g[{j}] = {h}`：同样长度，末尾变小，后面更容易接上',
        'g.append(h)': '`g` 末尾加入 {h}，最长长度变成 =={len(g)}==',
        'return len(g)': '`g` 的长度就是最多能套的信封数：=={ret}==',
    },
    cards=dict(
        one_liner='宽度升序、同宽高度降序，再对高度求最长严格递增子序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['信封 `[w, h]`：宽和高都==严格更大==才能装进去，不能旋转',
                 '求最多能套几层',
                 '示例：`[[5,4],[6,4],[6,7],[2,3]]` → `3`（`[2,3]→[5,4]→[6,7]`）',
                 f'本视频：`{ENV}` → `3`'],
        quote='对于相同的 w，如果按照 h ==降序排序==，就可以保证至多有一个信封出现在最长递增子序列中了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从特殊到一般：宽度互不相同时，按宽排序后就是对 h 求 ==LIS==',
              '宽度相同不能都选：同宽高度降序，降序段里严格递增最多取一个',
              '`n ≤ 10^5`，LIS 用 `g` 数组 + 二分，`O(n log n)`'],
        summary=['时间 `O(n log n)`：排序 + n 次二分',
                 '易错：同宽若按高度==升序==，会把多个同宽信封算进 LIS',
                 '严格递增用 `bisect_left`；若是非严格要用 `bisect_right`',
                 '`g` 不是真正的 LIS，只有它的==长度==有意义'],
    ),
)
