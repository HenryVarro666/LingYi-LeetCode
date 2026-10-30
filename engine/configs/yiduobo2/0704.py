def _dim(S, i, v):
    return 'l' in S and not (S['l'] <= i <= S['r'])


def _color(S, i, v):
    if 'mid' in S and i == S['mid'] and 'l' in S and S['l'] <= i <= S['r']:
        return 'green' if v == S['target'] else 'yellow'
    return None


def _state(S):
    if 'l' not in S:
        return f"在有序数组里找 `target = {S['target']}`" if 'target' in S else ''
    l, r = S['l'], S['r']
    s = f"target = =={S['target']}==   ·   搜索范围 `[{l}, {r}]`" + ('（空）' if l > r else f'，还剩 {r - l + 1} 个数')
    if 'mid' in S and l <= S['mid'] <= r:
        m = S['mid']
        x = S['nums'][m]
        op = '==' if x == S['target'] else ('<' if x < S['target'] else '>')
        s += f"   ·   `nums[{m}] = {x} {op} {S['target']}`"
    return s


def _cmp_eq(S, B, ret):
    x, t, m = S.nums[S.mid], S.target, S.mid
    if x == t:
        return f'`nums[{m}] = {x} == {t}`：==找到了=='
    return f'`nums[{m}] = {x} ≠ {t}`'


def _cmp_lt(S, B, ret):
    x, t, m = S.nums[S.mid], S.target, S.mid
    if x < t:
        return f'`nums[{m}] = {x} < {t}`：target 只可能在 ==mid 右边=='
    return f'`nums[{m}] = {x} > {t}`：target 只可能在 ==mid 左边==（走 else）'


CONFIG = dict(
    num=704, title='二分查找', difficulty='Easy', category='二分查找',
    author='yiduobo', technique='经典闭区间二分 · 找到即返回',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def search(self, nums, target):
        l = 0
        r = len(nums) - 1
        while l <= r:
            mid = (l + r) >> 1
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1
''',
    call='[Solution().search([-1, 0, 3, 5, 9, 12], 9), Solution().search([-1, 0, 3, 5, 9, 12], 2)]',
    expect=[4, -1],
    views=[
        dict(type='text', fn=_state, size=28),
        dict(type='array', var='nums', label='nums（暗 = 已排除，黄 = mid，绿 = 命中）',
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r'), window_color='cyan',
             color=_color, dim=_dim, cell=110, h=300),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('nums[mid]', 'nums[mid]'),
           ('target', 'target')],
    captions={
        'l = 0': '搜索范围是闭区间 `[l, r]`：`l = 0`',
        'r = len(nums) - 1': '`r = len(nums) − 1 = {r}`：一开始整个数组都可能',
        'while l <= r': lambda S, B, ret: (f'`l = {B.l} ≤ r = {B.r}`：范围里还有数 → 继续找' if B.l <= B.r
                                           else f'`l = {B.l} > r = {B.r}`：范围空了，==target 不在数组里=='),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`（右移一位就是整除 2）',
        'if nums[mid] == target': _cmp_eq,
        'return mid': '直接返回下标 =={ret}==',
        'elif nums[mid] < target': _cmp_lt,
        'l = mid + 1': '扔掉 `[{B.l}, {mid}]`：`l = mid + 1 = {l}`',
        'r = mid - 1': lambda S, B, ret: f'扔掉 `[{S.mid}, {B.r}]`：`r = mid − 1 = {S.r}`' + ('（==范围空了==）' if S.l > S.r else ''),
        'return -1': '没找到，返回 `-1`',
    },
    cards=dict(
        one_liner='没有任何变形的二分：看中间，相等就返回，否则扔掉一半',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['升序、元素互不相同的数组 `nums`，找 `target` 的下标，不存在返回 `-1`；要求 `O(log n)`',
                 '示例：`[-1,0,3,5,9,12]`，`target = 9` → `4`；`target = 2` → `-1`'],
        quote='==没有任何变形的二分查找问题==，直接按经典的做法来做即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`[l, r]` 是 target 可能在的范围，`mid = (l + r) >> 1`',
              '`nums[mid] == target` 直接返回；`<` 说明在右半边，`>` 说明在左半边',
              '范围为空（`l > r`）还没找到 → 返回 `-1`'],
        result='`target = 9` → `4`；`target = 2` → `-1` ✓',
        summary=['时间 `O(log n)`：每次范围减半；空间 `O(1)`',
                 '闭区间要配 `while l <= r` 和 `l = mid + 1`、`r = mid − 1`，否则可能死循环或漏掉',
                 '`>> 1` 等价于 `// 2`；Python 整数不会溢出，不用写 `l + (r − l) // 2`',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神找「第一个 ≥ target」再判断，能推广到有重复元素的 34 题'],
    ),
)
