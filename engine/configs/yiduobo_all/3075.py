CONFIG = dict(
    num=3075, title='幸福值最大化的选择方案', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='前 k 大 · 交换论证',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1326'],
    code='''
class Solution(object):
    def maximumHappinessSum(self, happiness, k):

        return sum([max(v - index, 0) for index, v in enumerate(sorted(happiness, reverse=True)[:k])])
''',
    call='Solution().maximumHappinessSum([1,5,1,4,3], 4)',
    expect=9,
    views=[
        dict(type='array', var=lambda S: sorted(S['happiness'], reverse=True), label='降序后的 happiness（前 k 个参与，灰 = 落选）', h=240,
             dim=lambda S, i, v: i >= S['k']),
        dict(type='text', size=26, fn=lambda S: ('第 index 个付出代价 index：' + ' + '.join(f'max({v}−{i}, 0)' for i, v in enumerate(sorted(S['happiness'], reverse=True)[:S['k']])) + ' = ' + str(sum(max(v - i, 0) for i, v in enumerate(sorted(S['happiness'], reverse=True)[:S['k']])))) if S['_line'] >= 4 else '最终和 = 前 k 大的 max(v − index, 0) 之和'),
    ],
    watch=['k', ('happiness', 'happiness', 'blue')],
    captions={
        'return sum': lambda S, B, r: f'降序取前 `{S.k}` 个 `{sorted(S.happiness, reverse=True)[:S.k]}`，第 `index` 个减去 `index`（最低为 0）求和 → =={r}=='
    },
    cards=dict(
        one_liner='前 k 大里，大的对应小代价，小的对应大代价',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`happiness[i]` 是孩子的幸福值，选 `k` 轮，每选一个其余孩子幸福值减 1（不低于 0）',
                 '求选中孩子幸福值之和的最大值',
                 '本视频：`[1,5,1,4,3], k=4` → `9`'],
        quote='最终选择的必然是初始幸福值最大的k个，理由是如果其中存在前k大之外的，就可以用初始幸福值前k大中落选的，来替换掉这个前k大之外的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用替换论证：选的必是前 `k` 大，二者衰减相同，换大的不会更差',
              '选的顺序下标 `p`：和 = `Σ max(h[p[j]] − j, 0)`',
              '总和固定，要让==付出的代价最小==：小的值去应对大的代价 → 从大到小选'],
        after=[dict(heading='交换论证（原文思路）', lines=['设第 `k` 大的值为 `x`，若它没对应 `k−1`，对应 `k−1` 的是 `y > x`', '分 `y` 与 `k−1`、`x` 与 `t` 的大小四种情况', '每种情况交换 `x`、`y` 后代价和都不增', '依次类推：第 `k−1` 大对应 `k−2`……即降序选取'])],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新列表）',
                 '易错：下标从 0 开始，第一个孩子不减',
                 '易错：`max(…, 0)` 不能省，幸福值不能为负',
                 '对比灵神：灵神 `x <= i` 直接 break，yiduobo 一行用 `max` 兜底，并给出了交换论证'],
    ),
)
