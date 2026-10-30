def _row(S):
    if 'x' not in S:
        return None
    t = [S['x'], S['y'], S['z']]
    for k, r in enumerate(S['triplets']):
        if r == t:
            return k
    return None


def _color(S, i, j, v):
    tg = S['target'][j]
    if i == _row(S):
        if v > tg:
            return 'red'
        return 'green' if v == tg else 'yellow'
    return None


CONFIG = dict(
    num=1899, title='合并若干三元组以形成目标三元组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='筛掉超标的三元组 · 三个维度各找一次',
    tags=['灵神题单', '难度分 1636'],
    code='''
class Solution(object):
    def mergeTriplets(self, triplets, target):

        flag1 = flag2 = flag3 = False;

        for x, y, z in triplets:
            if x == target[0] and y <= target[1] and z <= target[2]:
                flag1 = True
            if x <= target[0] and y == target[1] and z <= target[2]:
                flag2 = True
            if x <= target[0] and y <= target[1] and z == target[2]:
                flag3 = True
        
        return flag1 and flag2 and flag3
''',
    call='Solution().mergeTriplets([[2,5,3],[1,8,4],[1,7,5]], [2,7,5])',
    expect=True,
    views=[
        dict(type='table', var='triplets', label='triplets（当前行：红 = 超过 target，绿 = 恰好等于 target，黄 = 小于 target）',
             h=300, cell=90, color=_color, cols=['x', 'y', 'z']),
        dict(type='text', size=28, h=80, fn=lambda S: f"target = `{S['target']}`   已满足：x ==" + ('是' if S.get('flag1') else '否')
             + "==，y ==" + ('是' if S.get('flag2') else '否') + "==，z ==" + ('是' if S.get('flag3') else '否') + "==" if 'flag1' in S else ''),
    ],
    watch=[('flag1', 'flag1', 'green'), ('flag2', 'flag2', 'green'), ('flag3', 'flag3', 'green')],
    captions={
        'flag1 = flag2': '三个标记：目标的 x、y、z 三个维度各自==能不能凑出来==',
        'for x, y, z': '看第 `{triplets.index([x, y, z])}` 个三元组 `({x}, {y}, {z})`，目标 `{target}`',
        'if x == target[0]': lambda S, B, r: (f'`x = {S.x}` 等于 `{S.target[0]}`，且 `y ≤ {S.target[1]}`、`z ≤ {S.target[2]}` 都没超 → ==可用，x 维度满足=='
                                              if S.x == S.target[0] and S.y <= S.target[1] and S.z <= S.target[2]
                                              else '这个三元组 x 不等于目标，或者 y / z 超标（取 max 会把目标搞坏）'),
        'if x <= target[0] and y == target[1]': lambda S, B, r: (f'`y = {S.y}` 等于 `{S.target[1]}`，且 x、z 都没超 → ==y 维度满足=='
                                                                  if S.x <= S.target[0] and S.y == S.target[1] and S.z <= S.target[2]
                                                                  else 'y 不等于目标，或者 x / z 超标，不能用来满足 y'),
        'if x <= target[0] and y <= target[1] and z ==': lambda S, B, r: (f'`z = {S.z}` 等于 `{S.target[2]}`，且 x、y 都没超 → ==z 维度满足=='
                                                                           if S.x <= S.target[0] and S.y <= S.target[1] and S.z == S.target[2]
                                                                           else 'z 不等于目标，或者 x / y 超标，不能用来满足 z'),
        'flag1 = True': 'x 维度有了：`flag1 = True`',
        'flag2 = True': 'y 维度有了：`flag2 = True`',
        'flag3 = True': 'z 维度有了：`flag3 = True`',
        'return flag1': '三个维度 `{flag1}`、`{flag2}`、`{flag3}` → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='某一维超过目标的三元组不能用，其余的看三个维度能不能各凑出一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可以用三元组 `i` 把三元组 `j` 更新为逐维取较大值',
                 '问能否让 `target` 成为 `triplets` 中的一个元素',
                 '示例：`[[2,5,3],[1,8,4],[1,7,5]]`，`target = [2,7,5]` → `true`'],
        quote='如果某个三元组在其中一个维度上的值大于target中对应维度的值，那么就不能使用这个三元组来更新其他三元组。',
        quote_src='—— yiduobo 题解原文',
        idea=['取 max 只会越变越大：某一维超过目标，这个三元组就废了',
              '剩下可用的三元组里，只要某一维恰好等于目标，这一维就能满足',
              '一趟遍历，用三个标记记录三个维度，最后全为真才返回 `true`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：判断「等于」的同时，另外两维必须 `<=` 目标',
                 '三个维度互相独立，所以合并起来一定能得到目标',
                 '对比灵神：灵神先筛掉超标的，再看各维是否出现过目标值；yiduobo 把筛选和判断写进同一个条件'],
    ),
)
