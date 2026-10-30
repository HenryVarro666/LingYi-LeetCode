def _txt(S):
    if 'j' not in S or 'a' not in S or 'right' not in S:
        return '同一个值的下标分成一组，每组内部用前缀和求「到其他下标的距离和」'
    a, j, t, s = S['a'], S['j'], S['target'], S['s']
    n = len(a)
    return (f'下标 `{t}`：左边 `{t}×{j} − {s[j]}` = =={S["left"]}==，'
            f'右边 `{s[n]} − {s[j]} − {t}×{n - j}` = =={S["right"]}== ，合计 =={S["left"] + S["right"]}==')


def _col(S, i, v):
    a = S.get('a')
    if a is not None and 'j' in S and i in a:
        return 'blue' if i == a[S['j']] else 'cyan'
    return None


CONFIG = dict(
    num=2615, title='等值距离和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='分组 + 前缀和',
    tags=['前缀和', '难度分 1793'],
    code='''
class Solution:
    def distance(self, nums: List[int]) -> List[int]:
        groups = defaultdict(list)
        for i, x in enumerate(nums):
            groups[x].append(i)  # 相同元素分到同一组，记录下标
        ans = [0] * len(nums)
        for a in groups.values():
            n = len(a)
            s = list(accumulate(a, initial=0))  # 前缀和
            for j, target in enumerate(a):
                left = target * j - s[j]  # 蓝色面积
                right = s[n] - s[j] - target * (n - j)  # 绿色面积
                ans[target] = left + right
        return ans
''',
    call='Solution().distance([1,3,1,1,3])',
    expect=[5, 3, 3, 4, 3],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前下标，青 = 同组）', h=130,
             color=lambda S, i, v: _col(S, i, v)),
        dict(type='map', var='groups', label='groups（值 → 下标列表）', h=110,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='s', label='s：当前组的下标前缀和', h=170,
             pointers={'j': 'pink'}),
        dict(type='array', var='ans', label='ans', h=130,
             color=lambda S, i, v: 'blue' if S.get('target') == i and 'right' in S else None),
        dict(type='text', fn=_txt, h=60),
    ],
    watch=['target', 'j', 'left', 'right', ('ans', 'ans', 'green')],
    captions={
        'groups[x].append(i)': '值 `{x}` 的下标 `{i}` 放进它的组：`groups[{x}] = {groups[x]}`',
        'ans = [0] * len(nums)': '先全填 0：没有相同元素的位置答案就是 0',
        'for a in groups.values()': lambda S, B, r: ('所有组都处理完了' if 'a' in B and B.a == S.a
                                                    else f'逐组处理：这一组的下标是 `{S.a}`，组内互相算距离'),
        's = list(accumulate': '`s[j]` = 组内前 j 个下标之和：`{s}`，以后区间和就是两个前缀和相减',
        'left = ': '左边 `{j}` 个下标都比 `{target}` 小：距离和 = `{target}×{j} − s[{j}]` = =={left}==（蓝色面积）',
        'right = ': '右边 `{n - j}` 个下标都比 `{target}` 大：距离和 = `s[{n}] − s[{j}] − {target}×{n - j}` = =={right}==（绿色面积）',
        'ans[target] = ': '左右相加：`ans[{target}] = {left} + {right}` = =={ans[target]}==',
        'return ans': '所有位置都填好：`{ans}`',
    },
    cards=dict(
        one_liner='相同的值分一组，组内用前缀和拆掉绝对值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr[i]` = 所有满足 `nums[j]==nums[i]`、`j≠i` 的 `|i−j|` 之和',
                 '没有相同元素则为 `0`',
                 '示例：`[1,3,1,1,2]` → `[5,0,3,4,0]`；视频用 `[1,3,1,1,3]`'],
        quote='按照相同元素分组后再计算。……由于目标位置就是数组中的下标，无需二分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同值的下标组 `a` 是升序的：`a[j]` 左边的都更小，右边的都更大',
              '左边距离和 = `a[j]×j − 前缀和`，右边 = `后缀和 − a[j]×(n−j)`',
              '前缀和 `s` 让每个位置 `O(1)` 出答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`accumulate(a, initial=0)` 让 `s[0]=0`，`s` 比 `a` 长 1',
                 '左边有 `j` 个、右边有 `n−j` 个（含自己，自己距离为 0）',
                 '灵神方法二：相邻下标之间用增量 `(2i−n)×(a[i]−a[i−1])` 递推'],
    ),
)
