def _txt(S):
    ln = S.get('_line', 0)
    if 'cnt' in S and 'left' in S and 'right' in S and 'res' in S or ('cnt' in S and 'max_length' not in S and 'left' in S and 'right' in S):
        return f"这一侧向左最多扩 `{S['left']}`、向右最多扩 `{S['right']}`（含自身，且各不超过 k）→ 子数组 `{S['left']}×{S['right']}` = {S['left']*S['right']} 个，再减去超长的"
    if 'res' in S:
        return '第三步：每个元素当最大值、当最小值，各数一遍个数'
    if 'left_ma' in S:
        return '第二步：从右往左的两个单调栈，求左边界（带等号，重复值只算最左的）'
    return '第一步：从左往右的两个单调栈，求右边第一个严格更大/更小的位置'


CONFIG = dict(
    num=3430, title='最多 K 个元素的子数组的最值之和', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='贡献法：左右扩展数 − 超长子数组数',
    tags=['难度分 2645'],
    code='''
class Solution(object):
    def minMaxSubarraySum(self, nums, k):
        
        n = len(nums)

        ma_stack = []
        mi_stack = []
        right_ma = [n] * n
        right_mi = [n] * n
        for index in range(n):
            while ma_stack and nums[index] > nums[ma_stack[-1]]:
                right_ma[ma_stack.pop()] = index
            while mi_stack and nums[index] < nums[mi_stack[-1]]:
                right_mi[mi_stack.pop()] = index
            ma_stack.append(index)
            mi_stack.append(index)
        
        ma_stack = []
        mi_stack = []
        left_ma = [-1] * n
        left_mi = [-1] * n
        for index in range(n - 1, -1, -1):
            while ma_stack and nums[index] >= nums[ma_stack[-1]]:
                left_ma[ma_stack.pop()] = index
            while mi_stack and nums[index] <= nums[mi_stack[-1]]:
                left_mi[mi_stack.pop()] = index
            ma_stack.append(index)
            mi_stack.append(index)
        
        def calc(left, right):
            left = min(left, k)
            right = min(right, k)
            cnt = left * right
            max_length = left + right - 1
            if max_length > k:
                cnt -= (max_length - k + 1) * (max_length - k) // 2
            return cnt

        res = 0
        for index, v in enumerate(nums):
            res += v * (calc(index - left_ma[index], right_ma[index] - index) + calc(index - left_mi[index], right_mi[index] - index))
    
        return res
''',
    call='Solution().minMaxSubarraySum([2,1,2], 2)',
    expect=16,
    skip=['ma_stack = []', 'mi_stack = []', 'def calc', 'right_mi = [n]', 'left_mi = [-1]', 'mi_stack.append', 'ma_stack.append', 'max_length = left'],
    max_steps=100,
    views=[
        dict(type='text', h=70, size=26, fn=_txt),
        dict(type='array', var='nums', h=230, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', h=44, size=26, fn=lambda S: f"最大值栈 `{S['ma_stack']}`　最小值栈 `{S['mi_stack']}`　（表：右/左 边界，大=最大值、小=最小值）" if 'ma_stack' in S else ''),
        dict(type='table', h=230, label='', rows=['右·大', '右·小', '左·大', '左·小'], cols=lambda S: list(range(len(S['nums']))),
             var=lambda S: [S.get(v) or ['·'] * len(S['nums']) for v in ('right_ma', 'right_mi', 'left_ma', 'left_mi')] if 'right_ma' in S else None,
             color=lambda S, r, c, v: 'blue' if S.get('index') == c else None),
    ],
    watch=['index', 'left', 'right', ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'while ma_stack and nums[index] > nums': lambda S, B, ret: (
            f"`nums[{S['index']}]` = {S['nums'][S['index']]} 比栈顶 `nums[{S['ma_stack'][-1]}]` = {S['nums'][S['ma_stack'][-1]]} ==严格大==：右边第一个更大的就是它，弹出"
            if S['ma_stack'] and S['nums'][S['index']] > S['nums'][S['ma_stack'][-1]] else '最大值栈：不再弹（相等不算更大）'),
        'while mi_stack and nums[index] < nums': lambda S, B, ret: (
            f"`nums[{S['index']}]` = {S['nums'][S['index']]} 比栈顶 `nums[{S['mi_stack'][-1]}]` = {S['nums'][S['mi_stack'][-1]]} ==严格小==：右边第一个更小的就是它，弹出"
            if S['mi_stack'] and S['nums'][S['index']] < S['nums'][S['mi_stack'][-1]] else '最小值栈：不再弹（相等不算更小）'),
        'right_ma[ma_stack.pop()]': '`right_ma` 记下右边界：严格大于才算',
        'right_mi[mi_stack.pop()]': '`right_mi` 记下右边界：严格小于才算',
        'while ma_stack and nums[index] >= nums': lambda S, B, ret: (
            f"`nums[{S['index']}]` = {S['nums'][S['index']]} `>=` 栈顶 `{S['nums'][S['ma_stack'][-1]]}`：==带等号==，栈顶的左边界就是 `{S['index']}`，相等的值只归最左边那个，弹出"
            if S['ma_stack'] and S['nums'][S['index']] >= S['nums'][S['ma_stack'][-1]] else '最大值栈：不再弹'),
        'while mi_stack and nums[index] <= nums': lambda S, B, ret: (
            f"`nums[{S['index']}]` = {S['nums'][S['index']]} `<=` 栈顶 `{S['nums'][S['mi_stack'][-1]]}`：==带等号==，栈顶的左边界就是 `{S['index']}`，相等的值只归最左边那个，弹出"
            if S['mi_stack'] and S['nums'][S['index']] <= S['nums'][S['mi_stack'][-1]] else '最小值栈：不再弹'),
        'left = min': '向左最多扩 `{left}` 个（超过 k 的用不上）',
        'right = min': '向右最多扩 `{right}` 个（超过 k 的用不上）',
        'cnt = left * right': '先不管长度限制：左端点 `{left}` 种 × 右端点 `{right}` 种 = =={cnt}==',
        'if max_length > k': '最长的子数组把两边全包：`max_length = left+right-1 = {max_length}`，{"大于 k：有超长子数组，要减掉" if max_length > k else "不超过 k：全都合法，不用减"}',
        'cnt -= ': '超长的有 `1+2+…+(max_length-k)` = `({max_length}-{k}+1)×({max_length}-{k})/2` 个，减掉：`cnt = {cnt}`',
        'return cnt': '这个元素在这一侧管辖的合法子数组共 `{cnt}` 个',
        'res += v': '`nums[{index}] = {v}`：分别算它当最大值、当最小值时的合法子数组个数，再乘 `{v}` 累加',
        'for index in range(n - 1': lambda S, B, ret: ('从右往左的遍历结束，左边界都求好了' if S['index'] == B['index'] and S['ma_stack'] else f"从右往左：`index = {S['index']}`"),
        'for index, v in enumerate': '轮到 `nums[{index}] = {v}`，目前 `res = {res}`',
    },
    cards=dict(
        one_liner='每个元素当最大/最小值，数「长度不超过 k」的子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求所有==长度不超过 k==的子数组的「最大值 + 最小值」之和',
                 '示例：`nums=[1,2,3], k=2` → `20`',
                 '视频用 `[2,1,2], k=2` 演示，答案 `16`'],
        quote='若某个子数组中的最大值或者最小值出现了多次，在这里是不应该多次计算的。为了防止这种情况出现，可以先约定……只对首次出现的元素进行计算。',
        quote_src='—— yiduobo 题解',
        idea=['先约定重复值只算首次出现的，一边严格、一边带等号',
              '向左右各扩 `left`、`right`（含自己，截断到 k），共 `left×right` 个子数组',
              '其中超长（> k）的有 `1+2+…+(max_length−k)` 个，减去即可',
              '最大值、最小值各跑一遍同样的 `calc`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：左右边界一边严格、一边带等号，否则重复值重复算',
                 '`left`、`right` 要先截断到 `k`，超长子数组必然包含当前元素',
                 '与 3428（子序列版）不同，这里是子数组，只能数端点'],
    ),
)
