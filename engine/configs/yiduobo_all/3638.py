CONFIG = dict(
    num=3638, title='平衡装运的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='DP 简化为贪心 · 维护最大值',
    tags=['贪心算法', '思维题', '难度分 1463'],
    code='''
class Solution(object):
    def maxBalancedShipments(self, weight):
        
        res = 0
        ma = None
        for w in weight:
            if ma is None or w >= ma:
                ma = w
            else:
                res += 1
                ma = None

        return res
''',
    call='Solution().maxBalancedShipments([2,5,1,4,3,7,6])',
    expect=3,
    views=[
        dict(type='array', var='weight', h=260, label='weight',
             color=lambda S, i, v: ('blue' if 'w' in S and S['weight'].index(S['w']) == i else None) if 'w' in S else None,
             dim=lambda S, i, v: 'w' in S and S['weight'].index(S['w']) < i),
        dict(type='text', h=110, fn=lambda S: (f"当前开头候选的最大值：`ma = {S['ma']}`" if S.get('ma') is not None else '没有未完成的装运：`ma = None`') if 'ma' in S else ''),
    ],
    watch=[('w', 'w', 'blue'), ('ma', 'ma', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计装运数；`ma` 是当前这段里最大的数',
        'ma = None': '`ma = None`：目前没有可以当“开头”的数',
        'if ma is None or w >= ma': lambda S, B, r: (
            f'`ma` 是 None → `{S.w}` 当新的最大值' if B.ma is None else
            (f'`{S.w} >= ma = {B.ma}` → 它不会是装运的末尾，==舍掉前一个最大值，改用 {S.w} 当开头==' if S.w >= B.ma
             else f'`{S.w} < ma = {B.ma}` → 末尾比最大值小，==这是一组平衡装运==')),
        'ma = w': '`ma` 更新为 `{ma}`',
        'res += 1': '收下这组装运，`res` → {res}',
        'return res': '一共 `{res}` 组装运',
    },
    cards=dict(
        one_liner='用 DP 推出“上一个更大的数”，再简化成一趟贪心',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['装运 = 连续子数组；最后一个包裹重量严格小于该装运最大重量，就是平衡装运',
                 '选若干不重叠的平衡装运，求最大数量（可以有包裹不装运）',
                 '示例：`[2,5,1,4,3]` → `2`；本视频：`[2,5,1,4,3,7,6]` → `3`'],
        quote='对于当前的weight[index]，若其小于weight[index - 1]，那么就直接将这两个元素形成一组装运；反之，weight[index - 1]不可能越过weight[index]与后面的元素形成装运，因此在这里直接舍弃掉weight[index - 1]就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想 DP：`f[index]` 表示前 index 个包裹的最多装运，装运末尾选“上一个更大元素”`p`，`f[p-1]+1`',
              '`f` 单调不减，所以 `p` 越靠右越好，中间元素怎么选都不影响答案',
              '于是不用 DP：一趟遍历，维护最大值 `ma`，遇到更小的就切一组，`ma` 清空'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`w >= ma`（含等于）时不能成组：末尾必须==严格小于==最大值',
                 '成组后 `ma = None`：已用的包裹不能再被后面装运重用',
                 '对比灵神：灵神直接比较相邻两数；yiduobo 维护运行最大值，用 DP 论证为什么能贪心',
                 '原文为 Python 2 风格，除类型说明外代码无需改动'],
    ),
)
