SPELLS = [5, 1, 3]
POTIONS = [1, 2, 3, 4, 5]
SUCCESS = 7


def _q(S):
    return 'x' in S


def _ccol(S, i, v):
    if _q(S):
        low = S.get('low')
        if low is not None and i >= low:
            return 'green'
        return None
    if 'cnt' in S and 'y' in S and S['_line'] in (5, 6) and 'i' not in S and i == S['y']:
        return 'yellow'
    if 'i' in S and not _q(S) and S['_line'] in (9, 10) and (i > S['i'] or i == S['i'] and S['_line'] == 10):
        return 'cyan'
    return None


def _top(S):
    if _q(S) and 'low' in S:
        x, low = S['x'], S['low']
        return f"`x = {x}`：需要药水 `≥ ceil({SUCCESS}/{x})` = `({SUCCESS}−1)//{x} + 1` = =={low}=="
    if 'i' in S and S['_line'] in (9, 10):
        return f"后缀和：`cnt[{S['i']}]` 变成 `potions` 中 ==≥ {S['i']}== 的个数"
    if 'cnt' in S:
        return '先统计每种药水强度==出现几次=='
    return f'`x · y ≥ {SUCCESS}` ⇔ `y ≥ ceil({SUCCESS}/x)`：只需数出 ==≥ 某个值== 的药水个数'


CONFIG = dict(
    num=2300, title='咒语和药水的成功对数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='计数 + 值域后缀和',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1477'],
    code='''
class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        mx = max(potions)
        cnt = [0] * (mx + 1)
        for y in potions:
            cnt[y] += 1  # 统计每种药水的出现次数

        # 计算 cnt 的后缀和
        for i in range(mx - 1, -1, -1):
            cnt[i] += cnt[i + 1]
        # 计算完毕后，cnt[i] 就是 potions 值 >= i 的药水个数

        for i, x in enumerate(spells):
            low = (success - 1) // x + 1
            spells[i] = cnt[low] if low <= mx else 0
        return spells
''',
    call=f'Solution().successfulPairs({SPELLS}, {POTIONS}, {SUCCESS})',
    expect=[4, 0, 3],
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='potions', label='potions', cell=90,
             color=lambda S, i, v: 'yellow' if 'y' in S and not _q(S) and 'i' not in S and S['_line'] in (5, 6) and v == S['y'] else None,
             h=170),
        dict(type='array', var='cnt', label='cnt（下标 = 药水强度；计数 → 后缀和 cnt[i] = ≥ i 的个数）', color=_ccol,
             pointers={'i if _line in (9, 10) else None': 'cyan', 'low': 'green'},
             pointer_labels={'i if _line in (9, 10) else None': 'i'}, cell=90, h=230),
        dict(type='array', var='spells', label='spells（原地改成答案）', cell=90,
             color=lambda S, i, v: ('yellow' if _q(S) and i == S['i'] else None),
             h=170),
    ],
    watch=['mx', 'success', ('x', 'x', 'yellow'), ('low', 'low', 'green')],
    captions={
        'mx = max': '`mx = max(potions) = {mx}`：值域上限',
        'cnt = [0]': '`cnt` 开 `mx + 1 = {mx + 1}` 个位置，下标就是药水强度',
        'for y in potions': lambda S, B, r: ('统计完毕' if B.get('y') == S.y else f'药水 `y = {S.y}`'),
        'cnt[y] += 1': '统计每种药水的出现次数：`cnt[{y}]` → {cnt[y]}',
        'for i in range(mx - 1': lambda S, B, r: (f'倒着遍历：`i = {S.i}`' if B.get('i') != S.i else '后缀和算完'),
        'cnt[i] += cnt[i + 1]': '`cnt[{i}] += cnt[{i + 1}]` → =={cnt[i]}==：≥ {i} 的个数 = 等于 {i} 的 + ≥ {i + 1} 的',
        'for i, x in enumerate': lambda S, B, r: ('spells 处理完毕' if B.get('x') == S.x and 'low' in B and B.i == S.i
                                                  else f'第 `{S.i}` 个咒语 `x = {S.x}`'),
        'low = (success': '`x · y ≥ {success}` ⇔ `y ≥ ({success} − 1) // {x} + 1 = {low}`：==只用整数==，不用浮点',
        'spells[i] = cnt': lambda S, B, r: (f'`low = {S.low} ≤ mx`：`cnt[{S.low}]` = =={S.spells[S.i]}== 瓶药水够强'
                                            if S.low <= S.mx else f'`low = {S.low} > mx = {S.mx}`：没有这么强的药水 → ==0=='),
        'return spells': '复用 `spells` 作为答案：`{ret}`',
    },
    cards=dict(
        one_liner='把 x·y ≥ success 变成 y ≥ 下界，再用值域后缀和 O(1) 回答',
        complexity='时间 `O(n + m + U)`，空间 `O(U)`，`U = max(potions)`',
        problem=['咒语强度 `spells[i]`，药水强度 `potions[j]`；相乘 `≥ success` 就是一对成功组合',
                 '返回每个咒语能和多少瓶药水成功组合',
                 '示例：`spells = [5,1,3], potions = [1,2,3,4,5], success = 7` → `[4,0,3]`'],
        quote='借鉴前缀和的思想，我们可以倒着遍历 cnt，原地计算 cnt 的==后缀和==，把 cnt[i] 更新为 ≥ i 的药水的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['对正整数，`x·y ≥ success` ⇔ `y ≥ floor((success − 1)/x) + 1`',
              '`cnt[v]` 先记 v 出现次数，倒着累加后变成 ==≥ v 的个数==',
              '每个咒语只算一次下界 `low`，查 `cnt[low]` 即可；`low > mx` 时答案为 0'],
        summary=['时间 `O(n + m + U)`，空间 `O(U)`',
                 '上取整用 `(a − 1) // b + 1`，避免浮点误差',
                 '`low` 可能超过 `mx`，要先判断再访问 `cnt[low]`',
                 '方法一：`potions` 排序后 `m − bisect_right(potions, (success − 1) // x)`，`O((n+m) log m)`'],
    ),
)
