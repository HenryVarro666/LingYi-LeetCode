def _top(S):
    if 'staple' not in S or 'drinks' not in S:
        return ''
    s = S.get('s')
    p = S.get('p')
    if s is None or p is None:
        return f"主食升序 `{S['staple']}`，饮料降序 `{S['drinks']}`"
    return f"主食 `{s}`，从 p = `{p}` 起的饮料都能搭：`{len(S['drinks']) - p}` 款；res ==`{S['res']}`=="


def _sidx(S):
    if 's' not in S or 'res' not in S:
        return None
    return S['staple'].index(S['s'])


CONFIG = dict(
    num='LCP 18', title='早餐组合', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 单调双指针 · 主食升序、饮料降序',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def breakfastNumber(self, staple, drinks, x):

        staple.sort()
        drinks.sort(reverse=True)

        res = 0
        p = 0
        mod = 10 ** 9 + 7
        for s in staple:
            if s > x:
                break
            while p < len(drinks) and drinks[p] + s > x:
                p += 1

            if p == len(drinks):
                break
            
            res += len(drinks) - p
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().breakfastNumber([10,20,5,12], [5,5,2,8], 17)',
    expect=10,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='array', var='staple', label='staple（升序）', h=230,
             color=lambda S, i, v: 'blue' if 's' in S and 'res' in S and S['staple'].index(S['s']) == i else None),
        dict(type='array', var='drinks', label='drinks（降序，p 之后都能搭）', pointers={'p': 'pink'}, h=230,
             color=lambda S, i, v: 'green' if 'p' in S and 's' in S and i >= S['p'] and 'res' in S else None,
             dim=lambda S, i, v: 'p' in S and 's' in S and i < S['p']),
    ],
    watch=[('s', 's', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green'), 'x'],
    captions={
        'staple.sort()': '主食价格从小到大：==越贵的主食，能配的饮料越便宜==',
        'drinks.sort': '饮料从大到小：下标越大越便宜，`p` 之后的饮料都能配',
        'res = 0': '`res` 累计搭配数',
        'p = 0': '`p`：当前主食能选的==最贵饮料==的下标，从 0 开始',
        'mod =': '答案对 `10^9 + 7` 取模',
        'for s in': '遍历主食 `s = {s}`：主食越来越贵，所以 p 只会往后走',
        'if s > x': lambda S, B, r: (f'`s = {S.s} > x = {S.x}`：主食本身就买不起，后面更贵 → break' if S.s > S.x
                                     else f'`s = {S.s} <= x = {S.x}`：买得起，继续'),
        'while p <': lambda S, B, r: (f'`p = {S.p} == len(drinks)`：所有饮料都太贵，停止' if S.p >= len(S.drinks)
                                      else (f'`drinks[{S.p}] + s = {S.drinks[S.p]} + {S.s} = {S.drinks[S.p] + S.s} > x = {S.x}`：太贵 → p 后移，换更便宜的饮料'
                                            if S.drinks[S.p] + S.s > S.x else f'`drinks[{S.p}] + s = {S.drinks[S.p] + S.s} <= x = {S.x}`：买得起，p 停在这里')),
        'p += 1': '这款饮料配 `s` 太贵，对更贵的主食也太贵 → `p` = {p}',
        'if p == len': lambda S, B, r: ('`p == len(drinks)`：没有饮料能配这款主食，更贵的更不行 → break' if S.p == len(S.drinks)
                                        else '`p` 在范围内，这款主食有饮料可配'),
        'res += len': '`p` 及之后共 `len(drinks) − p = {len(drinks)} − {p} = {len(drinks) - p}` 款饮料可配 → `res` = =={res}==',
        'if res >= mod': lambda S, B, r: (f'`res = {S.res} >= mod`：减去 mod' if S.res >= S.mod else f'`res = {S.res} < mod`：不用取模'),
        'res -= mod': '`res` 减去 mod → {res}',
        'return res': '搭配总数 `{res}`',
    },
    cards=dict(
        one_liner='主食越贵，能配的饮料越便宜：p 只增不减',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`（不计排序）',
        problem=['`staple[i]` 是主食价格，`drinks[j]` 是饮料价格，各选一样，总价不超过 `x`',
                 '求方案数，对 `10^9 + 7` 取模',
                 '本视频：`staple=[10,20,5,12]`、`drinks=[5,5,2,8]`、`x=17` → `10`'],
        quote='选择越贵的主食，就只能选择越便宜的饮料。于是可以将主食和饮料分别按从小到大和从大到小进行排序，使用一个变量p表示对于当前主食可以选择的最贵的饮料的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['主食升序、饮料降序：饮料下标越大越便宜',
              '`p` 之后的饮料都能搭配，共 `len(drinks) − p` 款',
              '主食变贵，`p` 只会往后走 → 均摊 `O(1)`'],
        summary=['时间主要是排序 `O(n log n + m log m)`，双指针部分 `O(n+m)`',
                 '`s > x` 要先判断，主食本身买不起就直接 break',
                 '`p == len(drinks)` 时 break，否则下标越界',
                 '每次累加后检查是否 `>= mod`，减一次即可',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
