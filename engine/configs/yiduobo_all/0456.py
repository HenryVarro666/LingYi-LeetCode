NUMS = [3, 5, 0, 3, 4]
P1 = 'len(min_num) if _line == 8 and len(min_num) < len(nums) else (len(min_num) - 1 if _line == 9 else None)'


def _hint(S):
    ln = S['_line']
    if 'index' not in S:
        if 'min_num' in S and ln >= 8:
            return f"前缀最小值 `min_num = {S['min_num']}`：`min_num[i]` = nums[0..i] 的最小值，就是“1”的最优取值"
        return '先预处理“1”的最优取值：前缀最小值'
    i = S['index']
    now, mn = S['nums'][i], S['min_num'][i]
    st = S['stack']
    top = st[-1] if st else '无'
    if ln >= 15:
        return f'“1” = `{mn}`，“3” = `{now}`，栈顶（“2”的候选）= `{top}`'
    return f'枚举“3” = `nums[{i}]` = `{now}`，前面最小的“1” = `min_num[{i}]` = `{mn}`'


def _cell(S, i, v):
    if 'index' in S and i == S['index'] and S.get('_line', 0) >= 12:
        return 'blue'
    return None


CONFIG = dict(
    num=456, title='132模式', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='枚举“3” · 前缀最小值 + 单调栈',
    tags=['灵神核心路线', '灵神题单·单调栈'],
    code='''
class Solution(object):
    def find132pattern(self, nums):

        if len(nums) < 3:
            return False

        min_num = [nums[0]]
        for num in nums[1:]:
            min_num.append(min(min_num[-1], num))

        stack = [nums[-1]]
        for index in range(len(nums) - 2, -1, -1):
            now = nums[index]
            if now > min_num[index]:
                while stack and stack[-1] <= min_num[index]:
                    stack.pop()

                if stack and stack[-1] < now:
                    return True

                stack.append(now)

        return False
''',
    call=f'Solution().find132pattern({NUMS})',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前枚举的“3”，从后往前）', cell=96, h=220,
             pointers={'index': 'blue', P1: 'cyan'}, pointer_labels={P1: 'num'},
             color=_cell),
        dict(type='array', var='min_num', label='min_num（前缀最小值 = “1”的最优取值）', cell=96, h=165,
             color=_cell),
        dict(type='stack', var='stack', label='stack（“2”的候选，栈顶在右，栈底到栈顶不增）', h=150, font=30),
        dict(type='text', fn=_hint, size=26, h=100),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'),
           ('min_num[index]', 'min_num[index]', 'cyan'), ('stack', 'stack', 'green')],
    captions={
        'len(nums) < 3': '“132”要三个数，不到 3 个直接 `False`；这里 `len = {len(nums)}`，继续',
        'min_num = [nums[0]]': '`min_num[i]` 记 `nums[0..i]` 的最小值：先放 `nums[0] = {nums[0]}`',
        'for num in nums[1:]': lambda S, B, r: (f'预处理第一趟：从前往后扫，`num = {S.num}`' if 'num' not in B or S.num != B.num or len(S.min_num) == 1
                                               else '预处理结束'),
        'min_num.append': '`min(min_num[-1], num)`：前缀最小值往后延伸一格 → `{min_num}`',
        'stack = [nums[-1]]': '从后往前枚举“3”，栈里放“2”的候选。先放 `nums[-1] = {stack[-1]}`',
        'for index in range': lambda S, B, r: (f'枚举“3”的位置 `index = {S.index}`' if 'index' in S and S._line == 12 and S.index >= 0
                                               else '全部枚举完'),
        'now = nums[index]': '当前“3”候选 `now = {now}`；它前面最小的数（“1”）是 `min_num[{index}] = {min_num[index]}`',
        'if now > min_num[index]': lambda S, B, r: (
            f'`{S.now} > {S.min_num[S.index]}`：“3”比“1”大，才有可能当“3”' if S.now > S.min_num[S.index]
            else f'`{S.now} <= {S.min_num[S.index]}`：它不比前面的最小值大，当不了“3” → 跳过'),
        'while stack and stack[-1] <= min_num[index]': lambda S, B, r: (
            f'栈顶 `{S.stack[-1]}` ≤ “1” `{S.min_num[S.index]}`：它当不了“2”（要比“1”大），'
            f'而且“1”往前移只会变大、不会变小 → 以后更没用，==弹出=='
            if S.stack and S.stack[-1] <= S.min_num[S.index]
            else (f'栈顶 `{S.stack[-1]}` > “1” `{S.min_num[S.index]}`：停止弹出，栈顶是大于“1”的最小候选' if S.stack
                  else '栈空了，没有可用的“2”')),
        'stack.pop()': '弹出：栈顶太小，不可能比“1”大 → `stack = {stack}`',
        'if stack and stack[-1] < now': lambda S, B, r: (
            f'栈顶“2” `{S.stack[-1]}` < “3” `{S.now}`，又比“1” `{S.min_num[S.index]}` 大 → 凑齐 `{S.min_num[S.index]} < {S.stack[-1]} < {S.now}`'
            if S.stack and S.stack[-1] < S.now
            else (f'栈顶 `{S.stack[-1]}` 不小于 `now = {S.now}`：“2”必须比“3”小，还没凑齐' if S.stack else '栈空：没有“2”')),
        'return True': lambda S, B, r: (f'找到“132”：“1” = `{S.min_num[S.index]}`，“3” = `{S.now}`，“2” = `{S.stack[-1]}` → `True`'),
        'stack.append(now)': '凑不齐：`now = {now}` 自己成为新的“2”候选入栈 → `{stack}`',
        'return False': '所有位置都枚举完也没凑齐 → `False`',
    },
    cards=dict(
        one_liner='枚举“3”：前缀最小当“1”，单调栈里找“2”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 里找下标 `i < j < k`，满足 `nums[i] < nums[k] < nums[j]`（“132”）',
                 '有就返回 `True`，没有返回 `False`',
                 '示例：`[3,5,0,3,4]` → `True`（`3,5,4`）'],
        quote="若栈顶元素小于等于'1'，那么弹出栈顶元素，直到栈为空或者栈顶元素大于'1'。此时，栈顶元素就是nums[index + 1]到nums[-1]中大于'1'的数里面最小的那一个。",
        quote_src='—— yiduobo 题解原文',
        idea=['枚举“1”或“2”都要再扫一趟；枚举==“3”==时“1”取前缀最小就能一步定下',
              '从后往前枚举“3”，栈里存它后面“2”的候选',
              '候选从栈底到栈顶不增（否则早已凑成 132）；小于等于“1”的从栈顶清掉'],
        summary=['时间 `O(n)`：每个数最多入栈、出栈各一次',
                 '`now > min_num[index]` 不成立时直接跳过，不入栈',
                 '易错：先弹出 `<= min_num[index]` 的栈顶，再和 `now` 比较',
                 '原文是 Python 2 风格，但可直接在 Python 3 运行，代码未改'],
    ),
)
