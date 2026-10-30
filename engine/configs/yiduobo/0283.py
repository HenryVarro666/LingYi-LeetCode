def _color(S, i, v):
    fz = S.get('fisrt_zero')
    if 'index' not in S:
        return None
    if fz is not None and i >= fz and i <= S['index'] and v == 0:
        return 'purple'
    return None


def _state_text(S):
    if 'index' not in S:
        return '形如 `X, 0, 0, …, 0, Y`：把 `Y` 和==最左侧的 0== 交换'
    fz = S.get('fisrt_zero')
    if fz is None:
        return '`fisrt_zero = None`：还没遇到 0，非零数原地不动'
    return f"第一个零的位置 `fisrt_zero = {fz}`：后面遇到非零数，就和它交换"


def _is_zero(S, B, ret):
    if S.num == 0:
        return f'`nums[{S.index}] = 0`'
    return f'`nums[{S.index}] = {S.num}` 不是 0'


def _first_none(S, B, ret):
    if S.fisrt_zero is None:
        return '还没有记录过 0 → 这就是==第一个零=='
    return f'第一个零已记录在 `{S.fisrt_zero}`，这个 0 只是让 0 串变长'


def _has_zero(S, B, ret):
    if S.fisrt_zero is None:
        return '前面没有 0（`fisrt_zero is None`），不用移动'
    return f'存在第一个零 `{S.fisrt_zero}` → 当前数前方==必然存在一段 0==，交换'


CONFIG = dict(
    num=283, title='移动零', difficulty='Easy', category='双指针',
    author='yiduobo', technique='一趟扫描 · 与第一个零交换',
    code='''
class Solution(object):
    def moveZeroes(self, nums):
        fisrt_zero = None
        for index, num in enumerate(nums):
            if num == 0:
                if fisrt_zero is None:
                    fisrt_zero = index
            else:
                if fisrt_zero is not None:
                    nums[fisrt_zero], nums[index] = nums[index], nums[fisrt_zero]
                    fisrt_zero += 1
''',
    call='''nums = [2, 0, 0, 3, 0, 4]
Solution().moveZeroes(nums)
nums''',
    expect=[2, 3, 4, 0, 0, 0],
    views=[
        dict(type='text', fn=_state_text, size=29),
        dict(type='array', var='nums', pointers={'fisrt_zero': 'pink', 'index': 'blue'}, color=_color, h=300, cell=100,
             dim=lambda S, i, v: 'index' in S and i > S['index'],
             label='nums（紫 = 从第一个零开始的那串 0，暗 = 还没扫到）'),
    ],
    watch=[('index', 'index', 'blue'), 'num', ('fisrt_zero', 'fisrt_zero', 'pink')],
    captions={
        'fisrt_zero = None': '`fisrt_zero` 维护==第一个零的位置==；还没遇到 0，先设为 `None`',
        'for index, num in': lambda S, B, r: ('扫描结束' if 'index' in B and B.index == S.index
                                              else f'从左往右扫：`nums[{S.index}] = {S.num}`'),
        'if num == 0': _is_zero,
        'if fisrt_zero is None': _first_none,
        'fisrt_zero = index': '记下第一个零的位置：`fisrt_zero = {fisrt_zero}`',
        'if fisrt_zero is not None': _has_zero,
        'nums[fisrt_zero], nums[index] =': lambda S, B, r: (
            f'`nums[{S.fisrt_zero}]` ↔ `nums[{S.index}]`：`{", ".join(map(str, B.nums[max(0, S.fisrt_zero - 1):S.index + 1]))}`'
            f' → `{", ".join(map(str, S.nums[max(0, S.fisrt_zero - 1):S.index + 1]))}`，即 `X,0,…,0,Y` → `X,Y,0,…,0`'),
        'fisrt_zero += 1': '交换后，第一个零的位置往后移一位：`fisrt_zero` → {fisrt_zero}',
    },
    cards=dict(
        one_liner='遇到非零数，就和最左侧的那个 0 交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组中所有 `0` 移到末尾，==非零元素保持相对顺序==',
                 '必须==原地==修改，不能拷贝数组',
                 '示例：`[0,1,0,3,12]` → `[1,3,12,0,0]`',
                 '本视频：`[2,0,0,3,0,4]` → `[2,3,4,0,0,0]`'],
        quote='对于数组中X，0，0，0，...，0，Y的形式，我们需要将Y移动到这一串0的左侧，变成X，Y，0，0，...，0。可以发现，==只需要将Y与最左侧的0交换即可==。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右一趟扫描，维护住==第一个零的位置==',
              '当前数不为零且存在第一个零 → 它前方必然有一段 0，与第一个零互换',
              '交换后，第一个零的位置也对应地往后移动一位'],
        summary=['时间 `O(n)` 一趟扫描，空间 `O(1)`',
                 '`None` 表示还没遇到 0：开头的非零数不用动',
                 '变量名 `fisrt_zero` 是原文拼写，照录；原文为 Python 2 风格，只删去了文档字符串',
                 '对比灵神：同样是"与最左边的空位交换"，灵神用 `start0 = 0` 免去 `None` 判断（自己换自己）'],
        result='扫描结束：`nums = [2,3,4,0,0,0]`，原地完成',
    ),
)
