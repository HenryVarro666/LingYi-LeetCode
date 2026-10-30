CONFIG = dict(
    num=2454, title='下一个更大元素 IV', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='两个单调栈 · 找两次下一个更大',
    tags=['灵神题单', '难度分 2175'],
    code='''
class Solution(object):
    def secondGreaterElement(self, nums):

        stack_for_first = []
        stack_for_second = []

        res = [-1] * len(nums)
        for index, num in enumerate(nums):
            while stack_for_second and nums[stack_for_second[-1]] < num:
                res[stack_for_second[-1]] = num
                stack_for_second.pop()
            
            p = len(stack_for_first) - 1
            while p >= 0 and nums[stack_for_first[p]] < num:
                p -= 1
            
            for pos in stack_for_first[p + 1 : len(stack_for_first)]:
                stack_for_second.append(pos)

            while len(stack_for_first) > p + 1:
                stack_for_first.pop()
            
            stack_for_first.append(index)
        
        return res
''',
    call='Solution().secondGreaterElement([2,4,0,9,6])',
    expect=[9,6,6,-1,-1],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='stack', var='stack_for_first', label='stack_for_first（等第一个更大数）', h=130, font=28),
        dict(type='stack', var='stack_for_second', label='stack_for_second（已有第一个，等第二个）', h=130, font=28),
        dict(type='array', var='res', label='res', h=160,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num', 'blue'), ('first', 'stack_for_first', 'yellow'),
           ('second', 'stack_for_second', 'orange'), ('p', 'p', 'pink')],
    captions={
        'stack_for_first = []': '第一个栈：下标还在等==第一个==更大的数（同 496 的做法）',
        'stack_for_second = []': '第二个栈：==已经找到第一个==更大数的下标，等第二个',
        'res = [-1]': '`res` 默认 -1',
        'for index, num': '看 `nums[{index}] = {num}`',
        'while stack_for_second and': lambda S, B, ret: (
            f'第二个栈顶对应 `{S.nums[S.stack_for_second[-1]]}` < `{S.num}`：这是它的第二个更大数'
            if S.stack_for_second and S.nums[S.stack_for_second[-1]] < S.num else
            ('第二个栈空了' if not S.stack_for_second else f'栈顶 `{S.nums[S.stack_for_second[-1]]}` ≥ `{S.num}`：还要继续等 → 停')),
        'res[stack_for_second[-1]] = num': '记录答案：下标 `{B.stack_for_second[-1]}` 的答案是 `{num}`',
        'stack_for_second.pop()': '这个下标结算完毕，弹出',
        'p = len(stack_for_first) - 1': '`p` 指向第一个栈的栈顶，准备往下找',
        'while p >= 0 and nums': lambda S, B, ret: (
            f'`{S.nums[S.stack_for_first[S.p]]}` < `{S.num}`：`{S.num}` 是它的第一个更大数 → `p` 往下'
            if S.p >= 0 and S.nums[S.stack_for_first[S.p]] < S.num else
            ('第一个栈全被超过' if S.p < 0 else f'`{S.nums[S.stack_for_first[S.p]]}` ≥ `{S.num}`：不再弹 → 停在 `p = {S.p}`')),
        'p -= 1': '`p` → {p}',
        'for pos in stack_for_first': lambda S, B, ret: ('`p+1` 之后这一段已经找到第一个更大数 → 一个个搬到第二个栈（保持原来的顺序）' if len(S.stack_for_first) > S.p + 1 else '没有要搬的下标'),
        'stack_for_second.append(pos)': '下标 `{pos}` 进入第二个栈，开始等第二个',
        'while len(stack_for_first) > p + 1': lambda S, B, ret: ('把已搬走的下标从第一个栈弹掉' if len(S.stack_for_first) > S.p + 1 else '第一个栈只剩保留的部分'),
        'stack_for_first.pop()': '弹出一个',
        'stack_for_first.append(index)': '当前下标 `{index}` 进第一个栈',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='找到第一个更大数的元素，再找一次下一个更大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找每个数右边第二个比它大的数，没有就是 -1',
                 '示例：`[2,4,0,9,6]` → `[9,6,6,-1,-1]`',
                 '这是 496 下一个更大元素的强化版'],
        quote='对于这些利用496题中的方法找到了下一个更大元素的数而言，只需再执行一次相同的算法就可以找到本题所需的答案了。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：单调栈找下一个更大数',
              '找到的那批数，另起一个栈接着再找一次',
              '新栈里的顺序必须和老栈一致，其余细节照搬 496'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '每轮先处理第二个栈，再把第一个栈弹出的段搬过去，顺序不能反',
                 '栈里存下标，比较用 `nums[...]`',
                 '对比灵神：灵神用 `t += s[j+1:]` 和 `del` 一步搬完，这里用 for + while 循环'],
    ),
)
