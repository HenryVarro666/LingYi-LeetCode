_COL = {1: 'blue', 2: 'green', 3: 'purple', 4: 'pink', 5: 'orange'}


def _ones(v):
    return bin(v).count('1')


def _top(S):
    if 'i' not in S:
        return ''
    nums = S['nums']
    return '二进制 1 的个数：' + '  '.join(f'`{v}`→=={_ones(v)}==' for v in nums)


def _grp(S, i, v):
    if 'pre_max' not in S:
        return None
    return _COL.get(_ones(v) if _ones(v) in _COL else 5)


def _dim(S, i, v):
    return 'i' in S and 'ones' in S and i < S['i'] and _ones(v) != S['ones'] and S['_line'] not in (6, 7)


def _chk(S, B, ret):
    x, pm = S.x, S.pre_max
    if x < pm:
        return f'`x = {x} < pre_max = {pm}`：比前一组最大的还小，而==组间不能换== → 无法有序'
    return f'`x = {x} ≥ pre_max = {pm}`：不会卡在前一组后面，继续'


CONFIG = dict(
    num=3011, title='判断一个数组是否可以变为有序', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 记录每组最大值',
    tags=['灵神题单', '分组循环', '难度分 1497'],
    code='''
class Solution:
    def canSortArray(self, nums: List[int]) -> bool:
        n = len(nums)
        i = pre_max = 0
        while i < n:
            mx = 0
            ones = nums[i].bit_count()
            while i < n and nums[i].bit_count() == ones:
                x = nums[i]
                if x < pre_max:  # 无法排成有序的
                    return False
                mx = max(mx, x)  # 更新本组最大值
                i += 1
            pre_max = mx
        return True
''',
    call='Solution().canSortArray([8,4,2,30,15])',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（同色 = 1 的个数相同 = 同一组，组内可任意排序）', cell=100,
             pointers={'i': 'pink'}, color=_grp),
        dict(type='text', fn=lambda S: (f"上一组最大 `pre_max = {S['pre_max']}`，本组最大 `mx = {S['mx']}`" if 'mx' in S
                                        else ''), size=28),
    ],
    watch=[('i', 'i', 'pink'), ('ones', 'ones', 'blue'), ('x', 'x'), ('mx', 'mx', 'green'), ('pre_max', 'pre_max', 'orange')],
    captions={
        'i = pre_max = 0': '`i` 是当前组的起点；`pre_max` 是上一组最大值，数都 > 0，初始 0 就行',
        'while i < n:': lambda S, B, r: (f'外层循环：一次处理==一整组=={"，从 `i = " + str(S.i) + "` 开始" if S.i < len(S.nums) else ""}'
                                         if S.i < len(S.nums) else '所有组都处理完了'),
        'mx = 0': '新的一组：本组最大值 `mx` 清零',
        'ones = nums[i]': '本组的特征：`{nums[i]}` 的二进制有 `{ones}` 个 1，==1 的个数相同才能交换==',
        'while i < n and': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}` 的 1 有 `{_ones(S.nums[S.i])}` 个 == `{S.ones}` → 还在本组'
                                            if S.i < len(S.nums) and _ones(S.nums[S.i]) == S.ones
                                            else (f'`nums[{S.i}] = {S.nums[S.i]}` 的 1 有 `{_ones(S.nums[S.i])}` 个 ≠ `{S.ones}` → 本组到此结束'
                                                  if S.i < len(S.nums) else '到数组末尾，本组结束')),
        'x = nums[i]': '取出组内元素 `x = {x}`',
        'if x < pre_max': _chk,
        'return False': '无法排成有序，返回 `False`',
        'mx = max': '本组最大值 `mx = {mx}`',
        'i += 1': '`i` → {i}，继续看下一个',
        'pre_max = mx': '这一组结束，它的最大值成了下一组必须跟上的门槛：`pre_max = {pre_max}`',
        'return True': '每组的数都不小于前一组最大值 → 组内排好序后整体非降序，返回 `True`',
    },
    cards=dict(
        one_liner='按“1 的个数”分组：组内随便排，组间顺序不能变',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['只能交换相邻且二进制 ==1 的个数相同== 的两个数，次数不限',
                 '问能不能把数组变成非降序',
                 '示例：`[8,4,2,30,15]` → `true`'],
        quote='外层循环负责遍历组之前的准备工作（记录开始位置），和遍历组之后的工作；内层循环负责遍历组，找出这一组最远在哪结束。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分组循环：内层 `while` 扫出一组，外层处理这一组前后的事',
              '组内元素可相邻交换 → 按冒泡思想==一定能排成升序==',
              '组间不能交换，所以每组的数都要 `≥` 上一组的最大值 `pre_max`',
              '不用真的排序，只维护每组最大值，`O(n)` 搞定'],
        after=[dict(heading='另一种写法：直接排序', lines=[
            '每组 `nums[start:i] = sorted(nums[start:i])`',
            '最后判断整个数组是否有序，`all(x <= y for x, y in pairwise(nums))`',
            '时间 `O(n log n)`，思路更直白'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '分组循环：内层结束时 `i` 已经是下一组起点，==外层不用再 `i += 1`==',
                 '不需要特判最后一组，这是该写法最大的好处',
                 '`pre_max` 初始 0 依赖 `nums[i] > 0`',
                 '同类：1446、1759、1578、1839 等分组循环题'],
    ),
)
