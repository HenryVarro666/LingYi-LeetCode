F, C = [5, 3, 3, 3, 5, 5], 2


def _color(S, i, v):
    if 'index' not in S or 'p' not in S:
        return None
    if S['p'] <= i <= S['index']:
        if S['_line'] == 15:
            return 'green'
        if v == F[S['index']] and S['cnt_dict'].get(v, 0) > C:
            return 'red'
        return 'blue'
    return None


def _top(S):
    if 'index' not in S:
        return f'`cnt = {C}`：初始窗口只有 `flowers[0]`，`res = 1`'
    p, i = S['p'], S['index']
    v = F[i]
    n = S['cnt_dict'].get(v, 0)
    return (f"窗口 `[{p}, {i}]`，新加入的花 `{v}` 有 `{n}` 朵 → "
            + (f'超过 {C}，左边界要右移' if n > C else '==美观=='))


def _while(S, B, ret):
    v = S.flowers[S.index]
    n = S.cnt_dict[v]
    if n > S.cnt:
        return f'`cnt_dict[{v}] = {n} > {S.cnt}`：这种花太多，==缩小窗口=='
    return f'`cnt_dict[{v}] = {n} ≤ {S.cnt}`：窗口 `[{S.p}, {S.index}]` 美观'


CONFIG = dict(
    num='LCP 68', title='美观的花束', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 累加窗口长度',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def beautifulBouquet(self, flowers, cnt):

        p = 0
        cnt_dict = {}
        cnt_dict[flowers[0]] = 1
        res = 1
        mod = 10 ** 9 + 7

        for index in range(1, len(flowers)):
            cnt_dict[flowers[index]] = cnt_dict.get(flowers[index], 0) + 1
            while cnt_dict[flowers[index]] > cnt:
                cnt_dict[flowers[p]] -= 1
                p += 1

            res += index - p + 1
            if res >= mod:
                res -= mod

        return res
''',
    call=f'Solution().beautifulBouquet({F}, {C})',
    expect=15,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='flowers', label='flowers（框 = 窗口 [p, index]，红 = 超量的花，绿 = 本轮累加）',
             pointers={'p': 'cyan', 'index': 'orange'}, window=('p', 'index'), color=_color, cell=120, h=300),
        dict(type='map', var='cnt_dict', label='cnt_dict（窗口内每种花出现的次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('p', 'p', 'cyan'), ('index', 'index', 'orange'), ('res', 'res', 'green')],
    skip=['mod = 10', 'if res >= mod'],
    captions={
        'p = 0': '左边界 `p = 0`',
        'cnt_dict = {}': '`cnt_dict` 记录窗口内每种花出现的次数',
        'cnt_dict[flowers[0]] = 1': '先把第 0 朵花 `{flowers[0]}` 放进窗口',
        'res = 1': '区间 `[0, 0]` 一定美观：`res = 1`',
        'for index in range': lambda S, B, r: ('右边界走到末尾，结束' if 'index' in B and B.index == S.index
                                               else f'右边界移到 `index = {S.index}`，花 `{S.flowers[S.index]}` 加入窗口'),
        'cnt_dict[flowers[index]] = cnt_dict.get': '更新这种花的次数：`cnt_dict[{flowers[index]}]` → {cnt_dict[flowers[index]]}',
        'while cnt_dict[flowers[index]] > cnt': _while,
        'cnt_dict[flowers[p]] -= 1': '左边界的花 `{flowers[p]}` 移出：`cnt_dict[{flowers[p]}]` → {cnt_dict[flowers[p]]}',
        'p += 1': '`p` → {p}',
        'res += index - p + 1': '以 `{p}..{index}` 为起点、`{index}` 为终点都美观：`res += {index - p + 1}` → =={res}==',
        'return res': '一共 =={ret}== 个美观区间',
    },
    cards=dict(
        one_liner='右边界加一朵花，超量就收左边界，然后累加窗口长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一排花 `flowers[i]` 是品种编号，选一段连续区间',
                 '每个品种都==不超过 cnt 朵==，就是美观的；求美观区间数',
                 '示例：`[5,3,3,3], cnt = 2` → `8`；本视频 `[5,3,3,3,5,5], cnt = 2` → `15`'],
        quote='以窗口中任意位置为起点，窗口右边界为终点的区间都是美观的区间，也就是说此时能带来==数量等于窗口长度==的美观区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['新花加入后，若它的次数超过 cnt，就右移 p 直到不再超过',
              '窗口里的花都没超量 → 窗口的每个后缀也美观',
              '所以每个右边界贡献 `index − p + 1` 个区间'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '写法细节：先把 `flowers[0]` 放入窗口、`res = 1`，循环从下标 1 开始',
                 '原文保留了对 `10^9 + 7` 取模的防溢出写法，本题其实不需要（视频里跳过这两行）',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
