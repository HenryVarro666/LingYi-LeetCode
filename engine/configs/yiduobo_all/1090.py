CONFIG = dict(
    num=1090, title='受标签影响的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按值降序贪心 + 标签计数',
    code='''
class Solution(object):
    def largestValsFromLabels(self, values, labels, num_wanted, use_limit):

        used = {}
        n = len(values)
        res = 0
        for value, label in sorted([[values[index], labels[index]] for index in range(n)], key=lambda d:d[0], reverse=True):
            if used.get(label, 0) < use_limit:
                used[label] = used.get(label, 0) + 1
                res += value
                num_wanted -= 1
                if num_wanted == 0:
                    break

        return res
''',
    call='Solution().largestValsFromLabels([5,4,3,2,1], [1,1,2,2,3], 3, 1)',
    expect=9,
    views=[
        dict(type='array', var='values', h=200, label='values'),
        dict(type='array', var='labels', h=200, label='labels'),
        dict(type='map', var='used', h=170, fmt=lambda k, v: f'标签 {k}: 已用 {v}'),
        dict(type='text', fn=lambda S: (f"当前项 `value={S['value']}, label={S['label']}`，还要选 `{S['num_wanted']}` 个" if 'value' in S and 'label' in S else ''), size=34),
    ],
    watch=['value', 'label', 'num_wanted', ('res', 'res', 'green')],
    captions={
        'used = {}': '`used[label]` 记录每种标签已经选了几个',
        'n = len': '`n = {n}`',
        'res = 0': '`res` 累计选中的值之和',
        'for value, label in sorted': '按 value 从大到小看：当前 `value = {value}`，`label = {label}`',
        'if used.get(label, 0) < use_limit': lambda S, B, r: (f"标签 `{S.label}` 已用 `{S.used.get(S.label, 0)}` 次，上限 `{S.use_limit}`：" +
                                                              ("没满 → 可以选，值大的优先" if S.used.get(S.label, 0) < S.use_limit else "已满 → 跳过这一项")),
        'used[label] = ': '标签 `{label}` 的使用次数 +1 → `{used[label]}`',
        'res += value': '选中 `{value}`：`res` = {B.res} + {value} = =={res}==',
        'num_wanted -= 1': '还差 `{num_wanted}` 个',
        'if num_wanted == 0': lambda S, B, r: ('`num_wanted = 0`：选够了 → 提前结束' if S.num_wanted == 0 else f'`num_wanted = {S.num_wanted}`：还没选够，继续'),
        'break': '选够了，退出循环',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='值从大到小排序，标签没满就选，选够为止',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['第 `i` 项的值是 `values[i]`，标签是 `labels[i]`',
                 '最多选 `num_wanted` 项，且每种标签最多选 `use_limit` 项',
                 '求选中项的值之和最大是多少',
                 '示例：`values=[5,4,3,2,1]`，`labels=[1,1,2,2,3]`，`3`，`1` → `9`'],
        quote='对于同样label的两项，显然应当优先选择较大的那一项。对于label不同的两项……也应当优先选择较大的那一项。于是可以按照values从大到小进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['同标签内先选大的；不同标签之间也先选大的',
              '所以把 `(value, label)` 配对后按 value 降序，一路贪心',
              '用哈希表 `used` 数每种标签选了几个，满了就跳过'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '要先把 values 与 labels 配对再排序，不能只排 values',
                 '选够 `num_wanted` 个立即 `break`',
                 '`used.get(label, 0)` 避免标签第一次出现时 KeyError'],
    ),
)
