NUMS = [4, 3, 2, 7, 8, 2, 3, 1]


def _tgt(S):
    """第一趟里：nums[index] 应该去的下标"""
    if S.get('_line') in (3, 4, 5) and 'index' in S:
        return S['nums'][S['index']] - 1
    return None


def _color(S, i, v):
    ln = S.get('_line', 0)
    if ln >= 7 and 'res' in S:
        return 'green' if v == i + 1 else 'red'
    if v == i + 1:
        return 'green'
    return None


def _formula(S):
    ln = S.get('_line', 0)
    if ln in (3, 4, 5) and 'index' in S:
        a, k = S['nums'], S['index']
        v = a[k]
        t = v - 1
        if a[t] == v:
            return (f"`nums[{k}] = {v}` 该去下标 `{t}`：那里已经是 `{v}`" +
                    ('（就是它自己）' if t == k else ' → ==重复了==，先放着'))
        return f"`nums[{k}] = {v}` 该去下标 `{t}`，那里是 `{a[t]}` → 交换"
    if ln >= 7:
        return '第二趟：位置不对（`nums[p] != p + 1`）的数，==就是出现两次的数=='
    return '原地哈希：把数 `v` 放到下标 `v - 1`（绿 = 已归位）'


def _while(S, B, ret):
    a, k = B.nums, B.index
    v = a[k]
    t = v - 1
    if a[t] != v:
        return f'`nums[{t}] = {a[t]}` ≠ `{v}`：`{v}` 还没归位 → 交换'
    if t == k:
        return f'`{v}` 就在下标 `{t}`，已归位 → 处理下一个'
    return f'下标 `{t}` 上已经有一个 `{v}` 了：手上这个 `{v}` 是==多出来的==，停止交换'


def _swap(S, B, ret):
    v = B.nums[B.index]
    return f'交换：`{v}` 归位到下标 `{v - 1}`，换回来的 `{S.nums[S.index]}` 放到下标 `{S.index}`，继续处理它'


def _if(S, B, ret):
    if S.num != S.index + 1:
        return f'`nums[{S.index}] = {S.num}` ≠ `{S.index + 1}`：`{S.index + 1}` 的位置被占了，`{S.num}` ==出现了两次=='
    return f'`nums[{S.index}] = {S.num}` 在自己的位置上'


CONFIG = dict(
    num=442, title='数组中重复的数据', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='原地哈希 · 把 v 换到下标 v-1',
    tags=['热题173'],
    code='''
class Solution(object):
    def findDuplicates(self, nums):
        for index in range(len(nums)):
            while nums[nums[index] - 1] != nums[index]:
                nums[nums[index] - 1], nums[index] = nums[index], nums[nums[index] - 1]

        res = []
        for index, num in enumerate(nums):
            if num != index + 1:
                res.append(num)

        return res
''',
    call=f'Solution().findDuplicates({NUMS})',
    expect=[3, 2],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 已归位：nums[p] = p + 1）', cell=96, h=230,
             pointers={'index': 'blue', _tgt: 'pink'}, pointer_labels={_tgt: 'nums[index]-1'}, color=_color),
        dict(type='text', fn=_formula, h=64, size=25),
        dict(type='array', var='res', label='res（出现两次的数）', cell=96, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('nums[index]', 'nums[index]', 'pink'), ('res', 'res', 'green')],
    captions={
        'for index in range': lambda S, B, r: (f'处理下标 `index = {S.index}`' if 'index' not in B or S.index != B.index
                                               else '第一趟结束：能归位的数都归位了'),
        'while nums[nums[index] - 1]': _while,
        'nums[nums[index] - 1], nums[index] =': _swap,
        'res = []': '第二趟扫描，收集答案',
        'for index, num in': lambda S, B, r: (f'看 `nums[{S.index}] = {S.num}`' if 'num' not in B or S.index != B.index
                                              else '第二趟结束'),
        'if num != index + 1': _if,
        'res.append(num)': '`{num}` 加入答案 → `res = {res}`',
        'return res': '返回 `{ret}`',
    },
    skip=['for index, num in'],
    max_steps=70,
    cards=dict(
        one_liner='把每个数 v 交换到下标 v-1，最后没在自己位置上的就是重复的',
        complexity='时间 `O(n)`，额外空间 `O(1)`',
        problem=['长度为 `n` 的整数数组 `nums`，所有整数都在 `[1, n]` 内，每个数出现==一次或两次==',
                 '找出所有出现两次的数；要求 `O(n)` 时间、只用常量额外空间',
                 '示例：`[4,3,2,7,8,2,3,1]` → `[2,3]`'],
        quote='完成上面的步骤之后，对于所有出现一次的数a[p]，其必然等于p + 1。而对于出现两次的数，由于某个数占据了对应的位置，那么另一个数就==必然不满足== `a[p] = p + 1`',
        quote_src='—— yiduobo 题解',
        idea=['数都在 `1..n`：把 `v` 换到下标 `v - 1`，相当于==用数组本身当哈希表==',
              '一直交换，直到目标位置已经是这个数（归位了，或者遇到重复）',
              '每次交换都让一个数到达最终位置 → 看着是二重循环，总共仍是 `O(n)`'],
        result='返回 `[3, 2]` ✓（顺序任意）',
        summary=['时间 `O(n)`：交换最多 `n` 次；额外空间 `O(1)`（原地修改）',
                 '易错：多重赋值必须==先写目标位置== `nums[nums[index]-1]`，写反了会先改掉 `nums[index]`',
                 '`while` 条件同时覆盖「已归位」和「遇到重复」两种停止情况',
                 '同类：41 缺失的第一个正数、448 找到所有数组中消失的数字',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
