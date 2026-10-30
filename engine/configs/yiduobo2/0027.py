# ---- for num in nums 没有下标变量：用字幕回调按步骤顺序数出"读到第几个"，存到 POS（键 = 这一步 nums 快照的 id）
NUMS = [3, 2, 2, 3, 5, 3, 1]
VAL = 3
POS = {}
CUR = [-1]
WRITE_LINE = 9   # nums[now] = num


def _p(S):
    return POS.get(id(S.get('nums')))


def _rd(S):
    p = _p(S)
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


def _k(S):
    """res 的长度：刚执行完 nums[now] = num 时，新写入的那个也算进来"""
    return S['now'] + (S.get('_line') == WRITE_LINE)


def _color(S, i, v):
    if 'now' not in S:
        return None
    if i < _k(S):
        return 'cyan'
    r = _rd(S)
    if r is not None and i == r:
        return 'red' if v == VAL else 'blue'
    return None


def _dim(S, i, v):
    p = _p(S)
    if 'now' not in S or p is None or p < 0:
        return False
    if p >= len(NUMS):
        return i >= S['now']
    return _k(S) <= i < p


def _for(S, B, ret):
    r = CUR[0]
    if r < len(NUMS):
        return f'扫描下一个数：`num = nums[{r}] = {S.num}`'
    return f'扫描结束：res 就是 `nums` 的前 `{S.now}` 个'


def _if(S, B, ret):
    if S.num != S.val:
        return f'`{S.num} ≠ {S.val}`：属于答案 → 加入 `res`（也就是写到 `nums[now]`）'
    return f'`{S.num} == val`：不要它，什么都不做'


def _write(S, B, ret):
    r, k = CUR[0], B.now
    if r == k:
        return f'`nums[{k}] = {S.num}`：res 和 nums 在这里重合，值没变'
    return f'从头部开始覆盖：`nums[{k}] = {S.num}`，被盖掉的 `{B.nums[k]}` ==已经扫描过==，不影响答案'


CONFIG = dict(
    num=27, title='移除元素', difficulty='Easy', category='双指针',
    author='yiduobo', technique='res 重叠到 nums 头部 · 原地覆盖',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def removeElement(self, nums, val):
        if not nums:
            return 0

        now = 0
        for num in nums:
            if num != val:
                nums[now] = num
                now += 1

        return now
''',
    call=f'Solution().removeElement({NUMS}, {VAL})',
    expect=4,
    views=[
        dict(type='array', var=lambda S: S['nums'][:_k(S)] if 'now' in S else None, min_slots=len(NUMS), h=170, cell=100,
             color=lambda S, i, v: 'cyan',
             label='res（假如用额外数组：不等于 val 的数依次加入）'),
        dict(type='array', var='nums', h=300, cell=100,
             pointers={'now': 'pink', READ: 'blue'}, pointer_labels={READ: 'num'},
             color=_color, dim=_dim, label='nums（青 = res 重叠在 nums 头部，暗 = 扫描过、可覆盖）'),
        dict(type='text', fn=lambda S: (f"`res` 长度 = `now` = {S['now']}，扫描位置走在 `now` ==前面或同一格== → 覆盖不会丢数据")
             if 'now' in S else ''),
    ],
    watch=[('num', 'num', 'blue'), 'val', ('now', 'now', 'pink')],
    captions={
        'if not nums': '先特判：`nums` 为空就直接返回 0；这里不为空，继续',
        'now = 0': trk('`now`：res 的长度，也是 res 下一个要写的位置', reset=True),
        'for num in nums': trk(_for, step=True),
        'if num != val': trk(_if),
        'nums[now] = num': trk(_write),
        'now += 1': trk(lambda S, B, r: f'res 变长：`now = {S.now}`'),
        'return now': trk(lambda S, B, r: f'res 的长度就是答案：返回 =={r}=='),
    },
    cards=dict(
        one_liner='先想用额外数组 res 怎么做，再把 res 重叠到 nums 头部',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==原地==移除 `nums` 中所有等于 `val` 的元素，返回剩下的个数 `k`',
                 '`nums` 前 `k` 个要是剩下的元素（顺序任意）',
                 '示例：`nums = [3,2,2,3], val = 3` → `2`，`nums = [2,2,_,_]`',
                 '本视频：`nums = [3,2,2,3,5,3,1], val = 3` → `4`'],
        quote='如果把res直接==重叠到nums中也不会影响到最后的答案==，因此从头开始扫描，找到不等于的val的数就从头部开始覆盖nums中的数即可。',
        quote_src='—— yiduobo 题解',
        idea=['允许额外空间时：扫描 `nums`，不等于 `val` 的加入 `res`',
              '`res` 的长度 `now` 永远 ≤ 已扫描的个数 → 写到 `nums[now]` 只会盖掉扫过的数',
              '所以 `res` 可以直接放在 `nums` 头部，省掉额外数组'],
        result='返回 `4`，`nums` 前 4 个是 `[2,2,5,1]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`if not nums: return 0` 是保险的特判；不写也对（循环不执行，返回 0）',
                 '和第 26 题同一个套路：先想额外空间的做法，再“重叠”回原数组',
                 '对比灵神：灵神叫它“栈”，yiduobo 叫它“重叠的 res”，代码一样',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
