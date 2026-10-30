NUMS = [4, 3, 2, 7, 8, 2, 3, 1]

CODE = '''
class Solution(object):
    def findDisappearedNumbers(self, nums):
        for index in range(len(nums)):
            while nums[nums[index] - 1] != nums[index]:
                nums[nums[index] - 1], nums[index] = nums[index], nums[nums[index] - 1]

        res = []
        for index in range(len(nums)):
            if nums[index] != index + 1:
                res.append(index + 1)

        return res
'''
_LINES = CODE.strip('\n').split('\n')
L_FOR1 = [i + 1 for i, s in enumerate(_LINES) if 'for index in range' in s][0]
L_SWAP = [i + 1 for i, s in enumerate(_LINES) if 'nums[nums[index] - 1], nums[index] =' in s][0]
L_RES = [i + 1 for i, s in enumerate(_LINES) if 'res = []' in s][0]


def _phase1(S):
    return S.get('_line', 0) < L_RES


def _target(S):
    if not _phase1(S) or 'index' not in S:
        return None
    return S['nums'][S['index']] - 1


def _color(S, i, v):
    if v == i + 1:
        return 'green'
    if not _phase1(S) and isinstance(S.get('index'), int) and 'res' in S and i <= S['index']:
        return 'red'
    return None


def _while(S, B, ret):
    nums, i = B.nums, B.index
    v = nums[i]
    t = v - 1
    if nums[t] != v:
        return f'`nums[{i}] = {v}` 应该放在下标 `{t}`，那里现在是 `{nums[t]}` ≠ `{v}` → ==交换=='
    if t == i:
        return f'`nums[{i}] = {v}` 已经在自己的位置 `{t}` 上 → 停止'
    return f'下标 `{t}` 上已经是 `{v}`（==重复的数==）→ 不用再换，停止'


def _swap(S, B, ret):
    i = B.index
    v = B.nums[i]
    t = v - 1
    return f'`{v}` 归位到下标 `{t}`，原来的 `{B.nums[t]}` 换到下标 `{i}`，继续检查它'


CONFIG = dict(
    num=448, title='找到所有数组中消失的数字', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='原地交换归位（同 442 题）',
    tags=['字节30天', '热题173'],
    code=CODE,
    call=f'Solution().findDisappearedNumbers({NUMS})',
    expect=[5, 6],
    views=[
        dict(type='text', fn=lambda S: ('第一趟：把每个数 `v` 换到下标 `v - 1` 上（绿 = 已归位）' if _phase1(S)
                                        else '第二趟：`nums[i] ≠ i + 1` 的位置，说明 ==i + 1 缺失==（红）'), h=60),
        dict(type='array', var='nums', label='nums（蓝 = index，粉 = 当前数应去的位置 nums[index]−1）', cell=96,
             pointers={'index': 'blue', _target: 'pink'}, pointer_labels={_target: 'nums[index]−1'}, color=_color),
        dict(type='array', var=lambda S: [i + 1 for i in range(len(NUMS))], label='每个下标应该放的数 i + 1', cell=96,
             color=lambda S, i, v: 'green' if S['nums'][i] == v else (
                 'red' if not _phase1(S) and 'res' in S and isinstance(S.get('index'), int) and i <= S['index'] else None),
             index=False),
        dict(type='array', var='res', label='res（消失的数字）', cell=96, min_slots=8),
    ],
    watch=[('index', 'index', 'blue'), ('nums[index]', lambda S: S['nums'][S['index']], 'pink'), ('res', 'res', 'green')],
    captions={
        L_FOR1: lambda S, B, ret: (f'第一趟：处理下标 `index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`'
                                   if S.get('index') != B.get('index') or 'index' not in B else '第一趟结束：能归位的数都归位了'),
        'while nums[nums[index] - 1] != nums[index]': _while,
        L_SWAP: _swap,
        'res = []': '第二趟扫描：哪个位置上的数不对，那个位置对应的数就缺失了',
        'if nums[index] != index + 1': lambda S, B, ret: (
            f'`nums[{S.index}] = {S.nums[S.index]}` ≠ `{S.index + 1}` → `{S.index + 1}` ==没出现过=='
            if S.nums[S.index] != S.index + 1 else f'`nums[{S.index}] = {S.index + 1}`，位置正确'),
        'res.append(index + 1)': '`{index + 1}` 加入答案',
        'return res': '返回消失的数字 =={ret}==',
    },
    skip=[L_FOR1 + 5],
    max_steps=70,
    cards=dict(
        one_liner='把每个数 v 换到下标 v−1 上，最后位置不对的地方就是缺失的数',
        complexity='时间 `O(n)`，额外空间 `O(1)`',
        problem=['长度为 `n` 的数组 `nums`，元素都在 `[1, n]` 内（有的出现两次、有的没出现）',
                 '找出 `[1, n]` 中所有==没有出现==的数字；进阶：不用额外空间、`O(n)` 时间',
                 '示例：`[4,3,2,7,8,2,3,1]` → `[5,6]`'],
        quote='可以先按同样的做法调换位置，然后一趟扫描，对于第index个数，==如果其不等于index + 1，那么index + 1就缺失了==。',
        quote_src='—— yiduobo 题解（与 442 题同样的做法）',
        idea=['数字 `v` 的「家」是下标 `v − 1`：不断把 `nums[index]` 换回家，直到换回来的数已经在家',
              '`nums[v-1] == v` 时停止：要么 `v` 已归位，要么遇到了重复的 `v`',
              '第二趟：位置 `i` 上不是 `i + 1`，说明 `i + 1` 从没出现过'],
        result='下标 4、5 上是重复的 3、2 → 缺失 `[5, 6]` ✓',
        summary=['时间 `O(n)`：每次交换都让一个数归位，最多 `n` 次交换；额外空间 `O(1)`',
                 '交换写法 `a[a[i]-1], a[i] = a[i], a[a[i]-1]` 的==左边顺序不能反==：先改 `a[a[i]-1]`，再改 `a[i]`',
                 '`while` 用 `nums[v-1] != v` 判断，而不是 `v != i+1`，否则遇到重复数会死循环',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
