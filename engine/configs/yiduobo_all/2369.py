def _cap_a(S, B, ret):
    i = S.index
    if i < 2:
        return f'`index = {i} < 2`：不够两个数 → 这条不适用'
    ok = S.f[i - 2]
    eq = S.nums[i - 1] == S.nums[i - 2]
    if ok and eq:
        return f'`f[{i-2}]` 为真，且 `nums[{i-1}] = nums[{i-2}] = {S.nums[i-1]}` → 这两个数组成一段 → ==`f[{i}] = True`=='
    return f'`f[{i-2}] = {ok}`，`nums[{i-1}] == nums[{i-2}]`：{S.nums[i-1]} 与 {S.nums[i-2]} {"相等" if eq else "不等"} → 这条不成立'


def _cap_b(S, B, ret):
    i = S.index
    if i < 3:
        return f'`index = {i} < 3`：不够三个数 → 这条不适用'
    ok = S.f[i - 3]
    a, b, c = S.nums[i - 3], S.nums[i - 2], S.nums[i - 1]
    if ok and (a == b == c or c == b + 1 == a + 2):
        return f'`f[{i-3}]` 为真，且 `{a},{b},{c}` ' + ('三个相等' if a == b == c else '连续递增') + f' → ==`f[{i}] = True`=='
    return f'`f[{i-3}] = {ok}`，三个数 `{a},{b},{c}`：' + ('不满足相等或连续递增' if ok else '前面划分不了') + ' → 这条不成立'


CONFIG = dict(
    num=2369, title='检查数组是否存在有效划分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分型 DP（前 i 个数能否划分）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1780'],
    code='''
class Solution(object):
    def validPartition(self, nums):

        f = [True]
        for index in range(1, len(nums) + 1):
            f.append(False)
            if index >= 2 and f[index - 2] and nums[index - 1] == nums[index - 2]:
                f[index] = True
            elif index >= 3 and f[index - 3] and ((nums[index - 1] == nums[index - 2] == nums[index - 3]) or (nums[index - 1] == nums[index - 2] + 1 == nums[index - 3] + 2)):
                f[index] = True
        
        return f[-1]
''',
    call='Solution().validPartition([4,4,4,5,6])',
    expect=True,
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (f"`f[{S['index']}]`：前 {S['index']} 个数（到 `nums[{S['index']-1}]`）能否划分？看结尾 2 个或 3 个" if 'index' in S else '`f[i]` = 前 `i` 个数能否有效划分，`f[0] = True`')),
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             color=lambda S, k, v: ('yellow' if k == S['index'] - 1 else 'blue' if S['index'] - 3 <= k < S['index'] - 1 else None) if 'index' in S else None,
             pointers={'index': 'yellow'}),
        dict(type='array', var='f', label='f（f[i]：前 i 个数能否有效划分）', h=190, cell=96,
             color=lambda S, k, v: 'green' if v is True else ('yellow' if 'index' in S and k == S['index'] else None)),
    ],
    watch=['index', ('f[index]', "f[index] if 'index' in S and index < len(f) else None", 'green')],
    captions={
        'f = [True]': '`f[0] = True`：前 0 个数（空）算作可以划分',
        'for index in range': lambda S, B, r: ('`index` 从 1 到 n 都算完了' if 'index' in B and B.index == S.index else f'计算 `f[{S.index}]`：前 {S.index} 个数能否有效划分'),
        'f.append(False)': '先假设 `f[{index}] = False`，后面找到合法划分再改成 True',
        'if index >= 2': _cap_a,
        'elif index >= 3': _cap_b,
        'f[index] = True': '`f[{index}] = True`',
        'return f[-1]': '`f[-1] = {f[-1]}`：整个数组{"能" if f[-1] else "不能"}有效划分',
    },
    cards=dict(
        one_liner='f[i] 表示前 i 个数能否划分，从 f[i-2]、f[i-3] 接过来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把数组切成连续段：`[a,a]`、`[a,a,a]` 或 `[a,a+1,a+2]`',
                 '示例：`[4,4,4,5,6]` → `true`',
                 '示例：`[1,1,1,2]` → `false`'],
        quote='令f[i]表示数组中前i个数是否能形成有效划分，首先初始化f[0] = true，接下来一趟遍历',
        quote_src='—— yiduobo 题解原文',
        idea=['`i >= 2`、`f[i-2]` 为真、最后两个数相等：把它们划成一段，`f[i] = True`',
              '`i >= 3`、`f[i-3]` 为真、最后三个数相等或连续递增：同理',
              '其他情况 `f[i] = False`；最后看 `f[-1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这里 `f[i]` 是「前 i 个」，对应 `nums[i-1]`，下标差一位',
                 '先判断 `index >= 2`、`index >= 3` 再取 `f[index - k]`，避免越界',
                 '原文本身是合法的 Python 3 代码，未做修改'],
    ),
)
