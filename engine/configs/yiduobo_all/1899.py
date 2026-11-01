def _rows(S):
    return [list(r) for r in S['triplets']] + [list(S['target'])]


def _color(S, i, j, v):
    a, t = S['triplets'], S['target']
    if i == len(a):
        return 'purple'
    if 'x' in S and [S['x'], S['y'], S['z']] == list(a[i]) and S.get('_line', 0) >= 7:
        ok = all(a[i][k] <= t[k] for k in range(3))
        return ('green' if v == t[j] else 'blue') if ok else 'red'
    return None


CONFIG = dict(
    num=1899, title='合并若干三元组以形成目标三元组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历，三个维度各设一个标记',
    tags=['灵神题单', '贪心算法', '难度分 1636'],
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
        dict(type='grid', var=_rows, label='triplets（红 = 有维度超标，绿 = 命中目标，紫 = target）',
             color=_color, rows=lambda S: [f'[{i}]' for i in range(len(S['triplets']))] + ['T'], cols=['x', 'y', 'z'], h=330),
        dict(type='text', fn=lambda S: '标记：' + '  '.join(f"flag{k} = ==%s==" % S[f'flag{k}'] for k in (1, 2, 3)) if 'flag3' in S else '', size=34),
    ],
    watch=['flag1', 'flag2', 'flag3'],
    captions={
        'flag1 = flag2': '三个标记：对应 x、y、z 三个维度是否已被某个可用三元组「恰好命中」',
        'for x, y, z': '取下一个三元组 `({x}, {y}, {z})`',
        'if x == target[0]': lambda S, B, ret: (f'`x = {S.x}` 等于 `target[0] = {S.target[0]}`，且 `y <= {S.target[1]}`、`z <= {S.target[2]}` → ' + ('==成立==，x 维度命中' if (S.x == S.target[0] and S.y <= S.target[1] and S.z <= S.target[2]) else '不成立')),
        'if x <= target[0] and y ==': lambda S, B, ret: (f'`y = {S.y}` 等于 `target[1] = {S.target[1]}`，且 `x <= {S.target[0]}`、`z <= {S.target[2]}` → ' + ('==成立==，y 维度命中' if (S.x <= S.target[0] and S.y == S.target[1] and S.z <= S.target[2]) else '不成立')),
        'if x <= target[0] and y <= target[1] and z ==': lambda S, B, ret: (f'`z = {S.z}` 等于 `target[2] = {S.target[2]}`，且 `x <= {S.target[0]}`、`y <= {S.target[1]}` → ' + ('==成立==，z 维度命中' if (S.x <= S.target[0] and S.y <= S.target[1] and S.z == S.target[2]) else '不成立')),
        'flag1 = True': 'x 维度满足：`flag1` = True',
        'flag2 = True': 'y 维度满足：`flag2` = True',
        'flag3 = True': 'z 维度满足：`flag3` = True',
        'return flag1': '三个标记：`{flag1}`、`{flag2}`、`{flag3}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='某一维超过 target 的三元组，直接当它不存在',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['用一个三元组去更新另一个，取逐位较大值；问能否得到 `target`',
                 '示例：`[[2,5,3],[1,8,4],[1,7,5]]`，目标 `[2,7,5]` → `true`'],
        quote='如果某个三元组在其中一个维度上的值大于target中对应维度的值，那么就不能使用这个三元组来更新其他三元组。',
        quote_src='—— yiduobo 题解原文',
        idea=['更新取的都是较大值：超标的三元组一用就废，先排除',
              '对可用的三元组，若某一维恰好等于 target，这一维就被满足了',
              '一趟遍历后三个标记都为真，答案就是 true'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '每个 `if` 都要同时检查另外两维不超标',
                 '原文行尾的分号 `;` 保留未动',
                 '对比灵神：灵神先整体判断可用，再记录命中，一次判断；这里三个 `if` 各写一遍'],
    ),
)
