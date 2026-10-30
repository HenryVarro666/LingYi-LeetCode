def _seg(S, i, v):
    if 'p' in S and 'q' in S and S['p'] <= i < S['q']:
        return 'green' if v > 0 else 'pink'
    return None


def _text(S):
    if 'diff' not in S:
        return ''
    if 'res' in S and 'p' in S:
        return f"当前累计操作次数 `res = {S['res']}`"
    return ''


CONFIG = dict(
    num=3229, title='使数组等于目标数组所需的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按正负分段 · 每段累加上升量',
    tags=['灵神题单', '常用数据结构', '难度分 2067'],
    code='''
class Solution(object):
    def minimumOperations(self, nums, target):

        diff = [x - y for x, y in zip(nums, target)]
        p = 0
        res = 0

        def calc(start, end):
            p = start
            res = abs(diff[p])
            for index in range(p + 1, q):
                if abs(diff[index]) > abs(diff[index - 1]):
                    res += abs(diff[index]) - abs(diff[index - 1])
            
            return res

        while p < len(diff):
            while p < len(diff) and diff[p] == 0:
                p += 1
            
            if p == len(diff):
                break
            
            if diff[p] > 0:
                q = p + 1
                while q < len(diff) and diff[q] > 0:
                    q += 1
            else:
                q = p + 1
                while q < len(diff) and diff[q] < 0:
                    q += 1

            res += calc(p, q)
            p = q
        
        return res
''',
    call='Solution().minimumOperations([3,5,1,2,2,6], [4,3,2,4,1,6])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', h=130, index=False),
        dict(type='array', var='target', label='target', h=130, index=False),
        dict(type='array', var='diff', label='diff = nums - target（蓝 p 段起点，粉 q 段终点不含，黄 index）', h=190,
             pointers={'p': 'blue', 'q': 'pink', 'index': 'yellow'}, color=_seg),
        dict(type='text', fn=_text, h=50),
    ],
    watch=['p', 'q', 'index', ('res', 'res', 'green')],
    captions={
        'diff = [x - y': '`diff[i] = nums[i] - target[i]`：要把 `diff` 每个位置都变成 0',
        'p = 0': '`p` 从左往右扫描，每次找一段同号的区间',
        'res = 0': '`res` 累计总操作次数',
        'def calc': '`calc(start, end)`：求一段同号区间 `[start, end)` 要多少次操作',
        'while p < len(diff):': lambda S, B, r: (f'`p = {S.p}` 还没到末尾，继续找下一段' if S.p < len(S.diff) else '`p` 到末尾，所有段都处理完'),
        'while p < len(diff) and diff[p] == 0': lambda S, B, r: (f'`diff[{S.p}] = 0`：已经是 0，跳过' if S.p < len(S.diff) and S.diff[S.p] == 0 else (f'`diff[{S.p}] = {S.diff[S.p]}` 非 0：这是一段的起点' if S.p < len(S.diff) else '`p` 到末尾')),
        'p += 1': '跳过 0，`p` → {p}',
        'if p == len(diff)': lambda S, B, r: ('全是 0 了 → 结束' if S.p == len(S.diff) else f'`p = {S.p}` 还没到末尾，继续'),
        'if diff[p] > 0': lambda S, B, r: (f'`diff[{S.p}] = {S.diff[S.p]} > 0`：这段是正数，向右找连续的正数' if S.diff[S.p] > 0 else f'`diff[{S.p}] = {S.diff[S.p]} < 0`：这段是负数，向右找连续的负数'),
        'q = p + 1': '段至少包含 `p`，从 `q = {q}` 往右扩',
        'q += 1': '下一个同号，`q` 右移到 {q}',
        'while q < len(diff) and diff[q] > 0': lambda S, B, r: (f'`diff[{S.q}] = {S.diff[S.q]}` 同号，继续扩' if S.q < len(S.diff) and S.diff[S.q] > 0 else f'同号区间结束：段为 `[{S.p}, {S.q})`'),
        'while q < len(diff) and diff[q] < 0': lambda S, B, r: (f'`diff[{S.q}] = {S.diff[S.q]}` 同号，继续扩' if S.q < len(S.diff) and S.diff[S.q] < 0 else f'同号区间结束：段为 `[{S.p}, {S.q})`'),
        'res += calc(p, q)': '这一段单独算：调用 `calc({p}, {q})`',
        'p = start': '段起点 `p = {p}`',
        'res = abs(diff[p])': '起点要变 0，至少 `|diff[{p}]| = {abs(diff[p])}` 次操作：`res = {res}`',
        'for index in range': lambda S, B, r: (f'看下一个位置 `index = {S.index}`' if 'index' in S and 'index' not in B or ('index' in B and B.index != S.index) else '这一段看完了'),
        'if abs(diff[index]) >': lambda S, B, r: (f'`|diff[{S.index}]| = {abs(S.diff[S.index])}` 比前一个 `{abs(S.diff[S.index - 1])}` 大 → 多出来的要额外补' if abs(S.diff[S.index]) > abs(S.diff[S.index - 1]) else f'`|diff[{S.index}]| = {abs(S.diff[S.index])}` 不比前一个 `{abs(S.diff[S.index - 1])}` 大 → 前面的操作顺带就够了'),
        'res += abs(diff[index])': '额外补 `{abs(diff[index])} - {abs(diff[index - 1])}` 次：`res` → {res}',
        'return res': lambda S, B, r: (f'这一段需要 `{r}` 次' if 'start' in S else f'总共需要 `{r}` 次操作'),
        'p = q': '这一段处理完，总次数 `res = {res}`；`p` 跳到段尾 `{q}`',
    },
    cards=dict(
        one_liner='同号分段，段内只有「上升」的部分要额外补操作',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选 `nums` 的一个子数组，整体加 1 或减 1',
                 '求把 `nums` 变成 `target` 的最少操作次数',
                 '示例：`nums=[3,5,1,2,2,6], target=[4,3,2,4,1,6]` → `6`'],
        quote='不应该对一个既有正数又有负数的子数组执行操作……可以将diff划分成若干段全正或者全负的子数组，然后分别对这些子数组进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先逐位相减得到 `diff`，目标变成把 `diff` 全部变 0',
              '跨正负的操作不划算，所以按正、负、0 切成若干段，各算各的',
              '一段内：第一个数要 `|diff[i]|` 次；后面的数变大才要补差值，变小可以「蹭」前面的操作'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '每段的次数 = 首个绝对值 + 之后每次「上升」的量',
                 '`calc` 里用到的 `q` 来自外层函数（闭包），`start`、`end` 参数其实没用上',
                 '对比灵神：他直接用差分里正数和、负数和取 max，不必分段',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
