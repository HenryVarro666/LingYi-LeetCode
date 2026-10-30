TOPS = [2, 1, 2, 4, 2, 2]
BOTS = [5, 2, 6, 2, 3, 2]


def _idx(S):
    f = S.get('_inner') or {}
    if 'x' not in f:
        return None
    for i, p in enumerate(zip(S['tops'], S['bottoms'])):
        if p == (f['x'], f['y']):
            return i
    return None


def _col(row):
    def fn(S, i, v):
        t = (S.get('_inner') or {}).get('target')
        if t is None:
            return None
        if i == _idx(S):
            return 'blue'
        return 'green' if v == t else None
    return fn


def _info(S):
    f = S.get('_inner') or {}
    if 'target' not in f:
        return '先试 `tops[0]` 和 `bottoms[0]` 两个目标值'
    return f"目标值 `target = {f['target']}`：`to_top = {f.get('to_top', 0)}`（转到上半），`to_bottom = {f.get('to_bottom', 0)}`（转到下半）"


def _cmp(S, B, r):
    f = S['_inner']
    x, y, t = f['x'], f['y'], f['target']
    if x != t and y != t:
        return f'`{x}` 和 `{y}` 都不等于 `{t}`：这张牌无论转不转都凑不出 `{t}` → ==无解，返回 inf=='
    if x != t:
        return f'上 `{x}` ≠ `{t}`，下 `{y}` = `{t}`：要让上半是 `{t}`，必须旋转'
    if y != t:
        return f'上 `{x}` = `{t}`，下 `{y}` ≠ `{t}`：要让下半是 `{t}`，必须旋转'
    return f'上下都是 `{t}`：转不转都行 → 不计次数'


CONFIG = dict(
    num=1007, title='行相等的最少多米诺旋转', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='只枚举第一张牌的两个数 · 分类讨论',
    tags=['灵神题单·贪心与思维', '难度分 1541'],
    code='''
class Solution:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        def min_rot(target: int) -> int:
            to_top = to_bottom = 0
            for x, y in zip(tops, bottoms):
                if x != target and y != target:
                    return inf
                if x != target:
                    to_top += 1  # 把 y 旋转到上半
                elif y != target:
                    to_bottom += 1  # 把 x 旋转到下半
            return min(to_top, to_bottom)

        ans = min(min_rot(tops[0]), min_rot(bottoms[0]))
        return -1 if ans == inf else ans
''',
    call=f'Solution().minDominoRotations({TOPS}, {BOTS})',
    expect=2,
    views=[
        dict(type='array', var='tops', label='tops（绿 = 已经是 target，蓝框 = 当前这张牌）', cell=96, h=190, color=_col('t')),
        dict(type='array', var='bottoms', label='bottoms', cell=96, h=190, color=_col('b')),
        dict(type='text', h=80, size=30, fn=_info),
    ],
    watch=[('target', lambda S: (S.get('_inner') or {}).get('target'), 'yellow'),
           ('to_top', lambda S: (S.get('_inner') or {}).get('to_top'), 'blue'),
           ('to_bottom', lambda S: (S.get('_inner') or {}).get('to_bottom'), 'pink'),
           ('ans', 'ans', 'green')],
    captions={
        'ans = min(min_rot(tops[0])': '「所有」必含第一张牌：目标只可能是 `tops[0]` 或 `bottoms[0]`，两种都算，取最小',
        'to_top = to_bottom = 0': '目标 `target = {target}`：分别统计「转到上半」「转到下半」的次数',
        'for x, y in zip': lambda S, B, r: f"取一张牌：上半 `{S.x}`，下半 `{S.y}`" if S.get('x') is not None else '',
        'if x != target and y != target': _cmp,
        'return inf': '这张牌凑不出 `{target}` → 这个目标不可行，返回 `inf`',
        'if x != target': lambda S, B, r: (f'上半 `{S.x}` ≠ `{S.target}`' if S.x != S.target else f'上半 `{S.x}` = `{S.target}`，不用动上半'),
        'to_top += 1': '把下半的 `{y}` 旋转到上半：`to_top = {to_top}`',
        'elif y != target': lambda S, B, r: (f'上半已是 `{S.target}`，下半 `{S.y}` ≠ `{S.target}`' if S.y != S.target else f'上下都是 `{S.target}`，不用转'),
        'to_bottom += 1': '把上半的 `{x}` 旋转到下半：`to_bottom = {to_bottom}`',
        'return min(to_top, to_bottom)': '要么让上排全是 `{target}`（转 `{to_top}` 次），要么让下排全是（转 `{to_bottom}` 次）→ 取小 ==`{ret}`==',
        'return -1 if': lambda S, B, r: ('两种目标都是 inf → 无解 `-1`' if S.ans == inf else f'最小旋转次数 ==`{S.ans}`=='),
    },
    cards=dict(
        one_liner='「所有」必包含第一张牌：目标值只有两个候选',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每张多米诺上下各有一个 1–6 的数，可以旋转交换',
                 '求让 `tops` 全相同或 `bottoms` 全相同的最少旋转次数，不行返回 `-1`',
                 '示例：`tops=[2,1,2,4,2,2]`，`bottoms=[5,2,6,2,3,2]` → `2`'],
        quote='目标是让第一排或者第二排的所有数都相同，这个「所有」必然包含==第一个骨牌中的数==。所以要么都变成 tops[0]，要么都变成 bottoms[0]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['写函数 `min_rot(target)`：把某一排都变成 `target` 的最少次数',
              '遍历每张牌，四种情况：都不是（无解）、只上不是、只下不是、都是',
              '只上不是 → 转到上半；只下不是 → 转到下半；最后 `min(to_top, to_bottom)`',
              '对 `tops[0]` 和 `bottoms[0]` 各算一次，取小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：无解要返回 `inf` 而不是 `-1`，两个目标取 `min` 后再统一转成 `-1`',
                 '`to_top` 和 `to_bottom` 是两种互斥方案（让上排全一样 / 让下排全一样），所以取 `min` 而不是相加',
                 '思考题：允许去掉一张牌，可以枚举去掉哪张'],
    ),
)
