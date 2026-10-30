# ---- for x in nums 没有下标变量：用字幕回调按步骤顺序数出"读到第几个"，存到 POS（键 = 这一步 nums 快照的 id）
NUMS = [0, 1, 2, 2, 3, 0, 4, 2]
VAL = 2
POS = {}
CUR = [-1]


def _rd(S):
    p = POS.get(id(S.get('nums')))
    return p if p is not None and 0 <= p < len(NUMS) else None


def trk(fn, step=False, reset=False):
    def cap(S, B, ret):
        if reset:
            CUR[0] = -1
        if step:
            CUR[0] += 1
        POS[id(S.nums)] = CUR[0]
        return fn(S, B, ret) if callable(fn) else fn
    return cap


READ = lambda S: _rd(S)  # noqa: E731


def _color(S, i, v):
    if 'stack_size' not in S:
        return None
    if i < S['stack_size'] or (S.get('_line') == 6 and i == S['stack_size']):
        return 'green'
    r = _rd(S)
    if r is not None and i == r:
        return 'red' if v == VAL else 'blue'
    return None


def _dim(S, i, v):
    p = POS.get(id(S.get('nums')))
    if 'stack_size' not in S or p is None or p < 0:
        return False
    if p >= len(NUMS):
        return i >= S['stack_size']
    if S.get('_line') == 6 and i == S['stack_size']:
        return False
    return S['stack_size'] <= i < p


def _for(S, B, ret):
    r = CUR[0]
    if r < len(NUMS):
        return f'读下一个数：`x = nums[{r}] = {S.x}`'
    return '`nums` 读完了，循环结束'


def _if(S, B, ret):
    if S.x != S.val:
        return f'`{S.x} ≠ {S.val}`：要保留 → ==入栈=='
    return f'`{S.x} == val`：要移除 → ==不入栈==，直接看下一个'


def _push(S, B, ret):
    r, k = CUR[0], B.stack_size
    if r == k:
        return f'把 x 入栈：`nums[{k}] = {S.x}`（读写同一格，相当于不动）'
    return f'把 x 入栈：`nums[{k}] = {S.x}`，覆盖的 `{B.nums[k]}` ==早就读过了==，覆盖安全'


CONFIG = dict(
    num=27, title='移除元素', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='把 nums 当成栈 · 原地入栈',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        stack_size = 0
        for x in nums:
            if x != val:
                nums[stack_size] = x  # 把 x 入栈
                stack_size += 1
        return stack_size
''',
    call=f'Solution().removeElement({NUMS}, {VAL})',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"栈 = `nums[0:{S['stack_size']}]`，大小 `stack_size = {S['stack_size']}`；"
                                        f"写入位置 `{S['stack_size']}` ==永远不超过== 读取位置")
             if 'stack_size' in S else ''),
        dict(type='array', var='nums', h=300, cell=100,
             pointers={'stack_size': 'pink', READ: 'blue'}, pointer_labels={READ: 'x 在这'},
             color=_color, dim=_dim, label='nums（绿 = 栈内元素，暗 = 已读过、可被覆盖）'),
        dict(type='stack', var=lambda S: S['nums'][:S['stack_size'] + (S.get('_line') == 6)] if 'stack_size' in S else None,
             label='栈（就是 nums[0 : stack_size]）', h=170, font=32),
    ],
    watch=[('x', 'x', 'blue'), 'val', ('stack_size', 'stack_size', 'pink')],
    captions={
        'stack_size = 0': trk('把 `nums` 自己当成==栈==：`stack_size = 0`，一开始栈是空的', reset=True),
        'for x in nums': trk(_for, step=True),
        'if x != val': trk(_if),
        'nums[stack_size] = x': trk(_push),
        'stack_size += 1': trk(lambda S, B, r: f'栈大小加一 → `stack_size = {S.stack_size}`'),
        'return stack_size': trk(lambda S, B, r: f'栈的大小 = 不等于 `val` 的元素个数 → 返回 =={r}=='),
    },
    cards=dict(
        one_liner='把 nums 当成栈，不等于 val 的数依次入栈',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==原地==移除数组 `nums` 中所有等于 `val` 的元素，返回剩下的个数 `k`',
                 '`nums` 的前 `k` 个元素要是不等于 `val` 的数，顺序任意，后面的不管',
                 '示例：`nums = [0,1,2,2,3,0,4,2], val = 2` → `5`'],
        quote='把 nums 视作一个==栈==，把不等于 val 的元素入栈，最后返回栈的大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['入栈 = `nums[stack_size] = x`，然后 `stack_size += 1`',
              '栈顶位置 `stack_size` ==不会超过==当前读到的位置，覆盖的都是读过的数',
              '所以不用额外数组，原地就能完成'],
        result='返回 `5`，`nums` 前 5 个是 `[0,1,3,0,4]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：返回的是==个数== `stack_size`，不是数组',
                 '“原地栈”是通用套路：26 删除有序数组重复项、283 移动零都能这么写',
                 '同类：题单「单序列双指针 · §3.5 原地修改」'],
    ),
)
