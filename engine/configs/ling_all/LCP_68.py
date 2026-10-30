F, C = [1, 2, 3, 2, 1, 3], 1


def _color(S, i, v):
    if 'right' not in S:
        return None
    if S['left'] <= i <= S['right']:
        if S['_line'] == 10:
            return 'green'
        if S['_line'] in (6, 7) and v == S['x'] and S['c'].get(S['x'], 0) > C:
            return 'red'
        return 'blue'
    return None


def _top(S):
    if 'right' not in S:
        return f'`cnt = {C}`：每种花不超过 {C} 朵 → 区间==越短越合法=='
    l, r, x = S['left'], S['right'], S['x']
    n = S['c'].get(x, 0)
    over = n > C
    return (f"窗口 `[{l}, {r}]`：品种 `{x}` 有 `{n}` 朵 "
            + (f'> {C}，==太多了==' if over else f'≤ {C}，合法'))


def _while(S, B, ret):
    x = S.x
    if S.c[x] > S.cnt:
        return f'`c[{x}] = {S.c[x]} > {S.cnt}`：刚进来的 `{x}` 太多了 → 左端点右移'
    return f'`c[{x}] = {S.c[x]} ≤ {S.cnt}`：窗口 `[{S.left}, {S.right}]` 合法'


CONFIG = dict(
    num='LCP 68', title='美观的花束', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 越短越合法',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def beautifulBouquet(self, flowers: List[int], cnt: int) -> int:
        ans = left = 0
        c = defaultdict(int)
        for right, x in enumerate(flowers):
            c[x] += 1
            while c[x] > cnt:  # x 太多了
                c[flowers[left]] -= 1
                left += 1  # 缩小窗口
            ans += right - left + 1
        return ans
''',
    call=f'Solution().beautifulBouquet({F}, {C})',
    expect=14,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='flowers', label='flowers（框 = 窗口，红 = 超量的品种，绿 = 本轮计入的左端点）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_color, cell=120, h=300),
        dict(type='map', var='c', label='c（窗口内每种花的数量）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'x', ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '`ans = 0`，窗口左端点 `left = 0`',
        'c = defaultdict': '`c` 记录窗口内每个品种的数量',
        'for right, x': lambda S, B, r: ('右端点枚举完毕' if 'right' in B and B.right == S.right
                                         else f'枚举右端点 `right = {S.right}`，品种 `{S.x}` 进入窗口'),
        'c[x] += 1': '`c[{x}]` → {c[x]}',
        'while c[x] > cnt': _while,
        'c[flowers[left]] -= 1': '移出左端的 `flowers[{left}] = {flowers[left]}`：`c[{flowers[left]}]` → {c[flowers[left]]}',
        'left += 1': '`left` → {left}：只有 `x` 可能超量，盯着它缩到合法即可',
        'ans += right': '左端点取 `{left}..{right}` 都美观：`ans += {right - left + 1}` → =={ans}==',
        'return ans': '共有 =={ret}== 种美观的区间',
    },
    cards=dict(
        one_liner='枚举右端点，x 太多就缩左端点；每次加上窗口长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一排花 `flowers[i]` 是品种编号，选一段连续区间做插花',
                 '每个品种都==不超过 cnt 朵==就是美观的，求美观区间的数量',
                 '示例：`[1,2,3,2], cnt = 1` → `8`；本视频 `[1,2,3,2,1,3], cnt = 1` → `14`'],
        quote='`while c[x] > cnt:  # x 太多了` …… `left += 1  # 缩小窗口`，然后 `ans += right - left + 1`',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['区间越短，每种花越少 → ==越短越合法==，可以滑窗',
              '加入 x 后只有 x 可能超量，所以 while 只需判断 `c[x]`',
              '窗口 `[left, right]` 合法，它的每个后缀也合法 → 加 `right − left + 1`'],
        summary=['时间 `O(n)`：left 最多右移 n 次；空间 `O(n)` 存哈希表',
                 '易错：while 判断的是刚进来的 `c[x]`，不是 `c[flowers[left]]`',
                 '题目保证结果在 int32 内，无需取模',
                 '同类：713 乘积小于 K 的子数组、3258 K 约束子串'],
    ),
)
