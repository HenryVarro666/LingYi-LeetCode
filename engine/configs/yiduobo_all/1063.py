CONFIG = dict(
    num=1063, title='有效子数组的数目', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='单调栈求下一个更小值', tags=['灵神题单'],
    code='''
class Solution(object):
    def validSubarrays(self, nums):

        n = len(nums)
        stack = []
        pos = [n] * n
        for index, num in enumerate(nums):
            while stack and num < nums[stack[-1]]:
                pos[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        res = 0
        for index, p in enumerate(pos):
            res += p - index
        
        return res
''',
    call='Solution().validSubarrays([1,4,2,5,3])',
    expect=11,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（蓝 = 当前 index；粉 = 栈顶）', h=230,
             color=lambda S, i, v: 'pink' if S.get('stack') and S['stack'][-1] == i else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}', label='stack（存下标，对应值从栈底到栈顶递增）', h=150),
        dict(type='array', var='pos', label='pos[i]：右侧第一个更小值的下标（n = 没有）', h=170, cell=70,
             pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: f"以 `{S['index']}` 为左端的有效子数组：`pos − index = {S['p']} − {S['index']}` = =={S['p']-S['index']}==，累计 =={S['res']}=="
             if 'p' in S and 'res' in S and S.get('_line', 0) >= 15 else '', h=70),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'pink'), ('pos', 'pos', 'orange'), ('res', 'res', 'green')],
    captions={
        'pos = [n] * n': '`pos[i]` 先填 `n`：右边没有更小的数时，所有右端点都合法',
        'while stack and num < nums[stack[-1]]': lambda S, B, r: (
            '栈是空的 → 没有等待结果的位置，不弹' if not S.stack else
            f'当前 `{S.num}` < 栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` → ==当前就是它右边第一个更小的数==，它的范围到此为止'
            if S.num < S.nums[S.stack[-1]] else
            f'当前 `{S.num}` ≥ 栈顶 `{S.nums[S.stack[-1]]}` → 栈顶还没遇到更小的数，保持不动'),
        'pos[stack[-1]] = index': '`pos[{stack[-1]}] = {index}`：以 `{stack[-1]}` 为左端，右端点只能到 `{index - 1}`',
        'stack.pop()': '栈顶的 `pos` 已确定，弹出',
        'stack.append(index)': '`index = {index}` 入栈，等待后面第一个比它小的数',
        'res = 0': '第二趟：把每个左端点能延伸的个数加起来',
        'res += p - index': '左端 `{index}`：右端点可取 `{index}` 到 `{p - 1}`，共 `{p} − {index} = {p - index}` 个 → `res = {res}`',
        'return res': '全部左端点加完，总数 `{res}`',
    },
    cards=dict(
        one_liner='左端固定，右端点能延伸到下一个更小值之前',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有效子数组：==第一个元素不大于子数组里其他元素==的非空连续子数组',
                 '求有效子数组的数目；`n` 很大，不能 `O(n^2)` 暴力',
                 '例：`[1,4,2,5,3]` → `11`'],
        quote='对于左边界为left的子数组而言，不妨设p是left右侧最小的，且满足nums[p] > nums[left]的下标，那么当子数组的右边界right满足left <= right < p时，子数组[left, right]都是有效子数组。',
        quote_src='—— yiduobo 题解原文（其中不等号方向按题意应为 nums[p] < nums[left]）',
        idea=['固定左端 `left`：只要右端没碰到比它小的数，就都有效',
              '所以个数是 `p - left`，`p` = 右侧第一个更小值的下标',
              '问题变成“下一个更小值”，一趟单调栈全部求出'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '没有更小值时 `p = n`，个数是 `n - left`，初始值正好是 `n`',
                 '比较用严格小于：相等的数不会截断子数组',
                 '符号与 496 题（下一个更大）相反，别抄错',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
