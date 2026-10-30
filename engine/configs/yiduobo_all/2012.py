def _beauty(a, i):
    if max(a[:i]) < a[i] < min(a[i + 1:]):
        return 2
    return 1 if a[i - 1] < a[i] < a[i + 1] else 0


def _color(S, i, v):
    if 'res' not in S:
        return None
    cur = S['index']
    if i == cur:
        return 'blue'
    if 1 <= i < cur:
        b = _beauty(S['nums'], i)
        return 'green' if b == 2 else 'yellow' if b == 1 else None
    return None


def _txt(S):
    if 'res' not in S:
        return '先正反两趟遍历，算出 `l_max` 和 `r_min`'
    i = S['index']
    return f"`l_max[{i-1}] = {S['l_max'][i-1]}`　`nums[{i}] = {S['nums'][i]}`　`r_min[{i+1}] = {S['r_min'][i+1]}`　已得 `res = {S['res']}`"


CONFIG = dict(
    num=2012, title='数组美丽值求和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='正反两趟预处理 l_max / r_min 数组',
    tags=['灵神题单', '动态规划', '难度分 1468'],
    code='''
class Solution(object):
    def sumOfBeauties(self, nums):

        n = len(nums)

        l_max = [nums[0]]
        for index in range(1, n):
            l_max.append(max(l_max[-1], nums[index]))
        
        r_min = [nums[-1]]
        for index in range(n - 2, -1, -1):
            r_min.append(min(r_min[-1], nums[index]))
        r_min.reverse()

        res = 0
        for index in range(1, n - 1):
            if l_max[index - 1] < nums[index] < r_min[index + 1]:
                res += 2
            elif nums[index - 1] < nums[index] < nums[index + 1]:
                res += 1
        
        return res
''',
    call='Solution().sumOfBeauties([1,3,2,4,5,6,5,7,8])',
    expect=5,
    max_steps=80,
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='array', var='nums', label='nums（蓝 = 当前，绿 = 美丽值 2，黄 = 美丽值 1）', h=200, color=_color),
        dict(type='array', var='l_max', label='l_max[i]：nums[0..i] 的最大值', h=200, pointers={'index - 1 if _line >= 16 else -1': 'cyan'}, pointer_labels={'index - 1 if _line >= 16 else -1': 'index-1'}),
        dict(type='array', var='r_min', label='r_min[i]：nums[i..n-1] 的最小值', h=200, pointers={'index + 1 if _line >= 16 else -1': 'pink'}, pointer_labels={'index + 1 if _line >= 16 else -1': 'index+1'}),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'l_max = [nums[0]]': '`l_max` 放前缀最大值，先放 `nums[0] = {nums[0]}`',
        'for index in range(1, n)': lambda S, B, r: (f'正序扫描，`index = {S.index}`' if len(S.l_max) < S.n else '前缀最大值算完了'),
        'l_max.append': '`l_max` 追加 `max({l_max[-2]}, nums[{index}])` = =={l_max[-1]}==',
        'r_min = [nums[-1]]': '`r_min` 放后缀最小值，先放 `nums[-1] = {nums[-1]}`',
        'for index in range(n - 2': lambda S, B, r: (f'倒序扫描，`index = {S.index}`' if len(S.r_min) < S.n else '后缀最小值算完了'),
        'r_min.append': '`r_min` 追加 `min({r_min[-2]}, nums[{index}])` = =={r_min[-1]}==（倒着存的）',
        'r_min.reverse': '翻转后 `r_min[i]` 才对应 `nums[i..n-1]` 的最小值',
        'res = 0': '两个数组备好了，开始逐个下标算美丽值',
        'for index in range(1, n - 1)': lambda S, B, r: ('全部枚举完了' if S.index == B.get('index') else f'枚举 `index = {S.index}`'),
        'if l_max': '`l_max[{index-1}] = {l_max[index-1]}` < `nums[{index}] = {nums[index]}` < `r_min[{index+1}] = {r_min[index+1]}`？ → {"==成立，左小右大=="  if l_max[index-1] < nums[index] < r_min[index+1] else "不成立"}',
        'res += 2': '得分 2：`res` → =={res}==',
        'elif': '退一步只看相邻：`{nums[index-1]} < {nums[index]} < {nums[index+1]}`？ → {"==成立=="  if nums[index-1] < nums[index] < nums[index+1] else "不成立，得 0"}',
        'res += 1': '得分 1：`res` → =={res}==',
        'return res': '美丽值总和 =={res}==',
    },
    cards=dict(
        one_liner='左小右大 = 大于左侧最大、小于右侧最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`1 <= i <= n-2` 的每个 `nums[i]`：左边全更小且右边全更大得 2 分',
                 '否则只要比相邻两个数都夹在中间得 1 分，其余 0 分',
                 '本视频：`[1,3,2,4,5,6,5,7,8]` → `5`'],
        quote='就是要求nums[index]左侧的最大值小于nums[index]，同时nums[index]右侧的最小值大于nums[index]，问题就转化成了前缀最大值和后缀最小值问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['得 1 分的条件只看邻居，一趟遍历就能判断',
              '得 2 分要看整侧：先正反各扫一趟，存好 `l_max` 和 `r_min` 两个数组',
              '最后再扫一趟：先判 2 分，不满足再判 1 分'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个数组）',
                 '`r_min` 是倒着追加的，==必须 reverse== 才能按下标用',
                 '判 2 分用 `l_max[index-1]` 和 `r_min[index+1]`，不含 `nums[index]` 自己',
                 '对比灵神：灵神只存后缀数组，前缀最大值用一个变量；这里是两个数组',
                 '原文代码无需改动，已是 Python 3 可运行'],
    ),
)
