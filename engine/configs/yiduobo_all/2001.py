def _cur(S):
    if 'w' not in S or 'res' in S:
        return None
    k = sum(S['rec_dict'].values()) - (1 if S['_line'] == 17 else 0)
    return k if k < len(S['rectangles']) else None


def _gcd_txt(S):
    if 'res' in S:
        return '每种最简比出现 `k` 次 → 贡献 `k × (k − 1) // 2` 对'
    if 'y' not in S:
        return '辗转相除求 `gcd(w, h)`，再约分成最简分数'
    if S['y']:
        return f"辗转相除：`gcd(x, y)` 当前 `x = {S['x']}, y = {S['y']}` → 下一步 `({S['y']}, {S['x']} % {S['y']} = {S['x'] % S['y']})`"
    return f"`y = 0`：最大公约数 =={S['x']}==，`(w, h)` 除以它得到最简分数"


CONFIG = dict(
    num=2001, title='可互换矩形的组数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='约分成最简分数 + 哈希计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1436'],
    code='''
class Solution(object):
    def interchangeableRectangles(self, rectangles):

        rec_dict = {}

        for w, h in rectangles:
            if w > h:
                x, y = w, h
            else:
                x, y = h, w

            while y:
                x, y = y, x % y
            
            w //= x
            h //= x
            rec_dict[(w, h)] = rec_dict.get((w, h), 0) + 1

        res = 0
        for v in rec_dict.values():
            res += v * (v - 1) // 2
        
        return res
''',
    call='Solution().interchangeableRectangles([[4,8],[3,6],[10,20],[2,3],[6,9]])',
    expect=4,
    views=[
        dict(type='array', var='rectangles', label='rectangles（[宽, 高]）', h=200, cell=150, font=30,
             color=lambda S, i, v: 'blue' if i == _cur(S) else None,
             dim=lambda S, i, v: _cur(S) is not None and i > _cur(S)),
        dict(type='text', h=90, size=28, fn=_gcd_txt),
        dict(type='map', var='rec_dict', label='rec_dict（最简分数 (w, h) → 出现次数）',
             fmt=lambda k, v: f'{k[0]}/{k[1]}: {v}', h=170, font=34),
    ],
    watch=['w', 'h', ('x', 'x', 'blue'), ('y', 'y', 'pink'), 'v', ('res', 'res', 'green')],
    captions={
        'rec_dict = {}': '`rec_dict` 记录每种宽高比（最简分数）出现的次数',
        'for w, h in rectangles': lambda S, B, r: (f'取出矩形 `{S.w} × {S.h}`' if sum(S.rec_dict.values()) < len(S.rectangles) else '所有矩形都约分完了'),
        'if w > h': lambda S, B, r: ('`w > h`：让 `x` 取较大的数' if S.w > S.h else '`w ≤ h`：让 `x` 取较大的 `h`'),
        'x, y = w, h': '`x = {x}, y = {y}`，准备求最大公约数',
        'x, y = h, w': '`x = {x}, y = {y}`，准备求最大公约数',
        'while y': lambda S, B, r: (f'`y = {S.y} ≠ 0`，继续辗转相除' if S.y else f'`y = 0`：`gcd = {S.x}`'),
        'x, y = y, x % y': '`(x, y) ← (y, x % y)` = `({x}, {y})`',
        'w //= x': '宽除以 gcd：`w = {w}`',
        'h //= x': '高除以 gcd：`h = {h}`，最简分数 ==`{w}/{h}`==',
        'rec_dict[(w, h)] =': '比值 `{w}/{h}` 的次数 +1 → `{rec_dict[(w, h)]}`：==用二元组哈希==，避免浮点误差',
        'res = 0': '开始统计：同一种比值里任选两个都能互换',
        'for v in rec_dict': lambda S, B, r: (f'这种比值出现了 `v = {S.v}` 次' if B.get('v') is not S.v or 'res' not in B else '统计完毕'),
        'res += v * (v - 1)': '`C({v}, 2) = {v * (v - 1) // 2}` 组 → `res = {res}`',
        'return res': '共 `{res}` 组可互换矩形',
    },
    cards=dict(
        one_liner='宽高比约分成最简分数当键，k 个同比矩形贡献 C(k,2) 对',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['矩形 `[w, h]`，两个矩形 ==`w/h` 相等==（实数除法）就可互换',
                 '求可互换的矩形对数 `(i < j)`',
                 '示例：`[[4,8],[3,6],[10,20],[15,30]]` → `6`',
                 '本视频：`[[4,8],[3,6],[10,20],[2,3],[6,9]]` → `4`'],
        quote='在这里宽高之比不一定是整数，不方便直接哈希，那么可以先对宽和高进行==约分==，然后以二元组的形式保存这个最简分数。',
        quote_src='—— yiduobo 题解原文',
        idea=['比值相同 ⇔ 约分后的 `(w, h)` 完全相同',
              '辗转相除求 gcd，宽、高同时除掉它',
              '某种比值出现 `k` 次 → 贡献 `k × (k − 1) / 2` 组'],
        summary=['时间 `O(n log U)`（辗转相除），空间 `O(n)`',
                 '用浮点数 `w / h` 当键可能有精度问题，二元组最稳',
                 '原文为 Python 2 写法，`w /= x`、`/ 2` 等整数除法已改为 `//`',
                 '也可以边遍历边累加（枚举右、维护左），结果相同'],
    ),
)
