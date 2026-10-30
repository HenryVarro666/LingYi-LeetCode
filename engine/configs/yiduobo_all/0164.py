def _pd(S):
    p = S.get('part_dict')
    if p is None:
        return '桶还没建'
    if not p:
        return '桶（编号 → [最小, 最大]）：暂无'
    return '桶（编号 → [最小, 最大]）：' + '   '.join(f'{k} → {v}' for k, v in sorted(p.items()))


CONFIG = dict(
    num=164, title='最大间距', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='鸽笼原理 + 桶排序', tags=[],
    code='''
class Solution(object):
    def maximumGap(self, nums):

        if len(nums) < 2:
            return 0

        min_num = min(nums)
        max_num = max(nums)

        part_dict = {}
        gap = (max_num - min_num) // (len(nums) - 1) + 1

        for num in nums:
            part = (num - min_num + 1) // gap
            if part not in part_dict:
                part_dict[part] = [num, num]
            else:
                part_min, part_max = part_dict[part]
                part_min = min(part_min, num)
                part_max = max(part_max, num)
                part_dict[part] = [part_min, part_max]

        now = None
        res = 0
        for part in range(0, len(nums)):
            if part in part_dict:
                if now is not None:
                    res = max(res, part_dict[part][0] - now)

                now = part_dict[part][1]

        return res
''',
    call='Solution().maximumGap([3,6,9,1,15,12])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=190, color=lambda S, i, v: 'blue' if v == S.get('num') else None),
        dict(type='text', size=30, h=80, fn=lambda S: f"桶宽 gap = (max−min)//(n−1) + 1 = ({S['max_num']}−{S['min_num']})//{len(S['nums'])-1} + 1 = =={S['gap']}==" if 'gap' in S else ''),
        dict(type='text', size=30, h=110, fn=_pd),
        dict(type='text', size=30, h=80, fn=lambda S: f"num = {S['num']} → 桶号 `({S['num']}−{S['min_num']}+1)//{S['gap']}` = =={(S['num']-S['min_num']+1)//S['gap']}==" if 'num' in S and 'gap' in S and 'now' not in S else ''),
        dict(type='text', size=30, h=80, fn=lambda S: f"上一个非空桶的最大值 now = {S['now']}" if S.get('now') is not None else ''),
    ],
    watch=[('min_num', 'min_num'), ('max_num', 'max_num'), ('gap', 'gap', 'orange'), ('part', 'part', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'if len(nums) < 2': '不足 2 个数，没有相邻元素 → 返回 0；否则继续',
        'min_num = min': '`min_num = {min_num}`',
        'max_num = max': '`max_num = {max_num}`',
        'gap = ': '桶宽取向上取整：`({max_num} − {min_num}) // {len(nums)-1} + 1` = =={gap}==；最大间隔一定 ≥ 平均间隔，所以同桶两数的差不可能是答案',
        'part = (': '`{num}` 放入第 `({num} − {min_num} + 1) // {gap} = {part}` 号桶',
        'if part not in part_dict': '桶 `{part}` {"还没有数 → 新建" if part not in part_dict else "已有数 → 更新最小最大值"}',
        'part_dict[part] = [num, num]': '桶 `{part}` 的最小最大都是 `{num}`',
        'part_min, part_max': '取出桶里原有的 `[{part_min}, {part_max}]`',
        'part_min = min': '最小值：`{part_min}`',
        'part_max = max': '最大值：`{part_max}`',
        'part_dict[part] = [part_min': '桶 `{part}` 更新为 `{part_dict[part]}`',
        'for part in range': '按桶号从小到大扫描：桶 `{part}`',
        'if part in part_dict': '桶 `{part}` {"非空" if part in part_dict else "是空桶，跳过"}',
        'if now is not None': '{"前面已有非空桶，可以算间隔" if now is not None else "这是第一个非空桶，没有前一个桶"}',
        'res = max': '后桶最小 − 前桶最大 = `{part_dict[part][0]} − {now} = {part_dict[part][0]-now}`，`res = {res}`',
        'now = part_dict': '记下本桶最大值 `now = {now}`',
        'return res': '最大间距 `{res}`',
    },
    cards=dict(
        one_liner='最大间隔不小于平均间隔：分桶后只比相邻桶的最值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无序数组 `nums`，求排序后相邻元素的最大差，要求线性时间',
                 '示例：`[3,6,9,1]` → `3`',
                 '本视频：`[3,6,9,1,15,12]` → `3`'],
        quote='由于最大间隔一定会大于等于桶的容量，那么若两个数位于同一个桶中，那么其间隔一定是小于桶容量的，因此不可能是最终的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['鸽笼原理：`n` 个数有 `n-1` 个间隔，最大间隔 ==≥ 平均间隔==',
              '按桶宽 `gap` 分桶，只记每桶的最大、最小值',
              '答案 = 相邻两个非空桶：==后桶最小 − 前桶最大==；用 `now` 记前桶最大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '向上取整写成 `(max-min)//(n-1) + 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 2 处）',
                 '只比较相邻非空桶，空桶要跳过'],
    ),
)
