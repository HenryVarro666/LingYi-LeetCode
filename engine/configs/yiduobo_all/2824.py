def _txt(S):
    if 'i' not in S or 'j' not in S:
        return '数据很小（n ≤ 50），直接两两枚举'
    a, b, t = S['nums'][S['i']], S['nums'][S['j']], S['target']
    return f'`nums[{S["i"]}] + nums[{S["j"]}] = {a} + {b} = {a+b}`，{"==< target，计数==" if a+b < t else ">= target，不算"}'


def _color(S, i, v):
    if 'i' in S and 'j' in S:
        if i == S['i']:
            return 'blue'
        if i == S['j']:
            return 'pink'
    return None


CONFIG = dict(
    num=2824, title='统计和小于目标的下标对数目', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='暴力枚举下标对',
    tags=['滑动窗口与双指针', '三、单序列双指针'],
    code='''
class Solution(object):
    def countPairs(self, nums, target):

        n = len(nums)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] < target:
                    res += 1
        
        return res
''',
    call='Solution().countPairs([-1,1,2,3,1], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=300, color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'target', ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'for i in range': lambda S, B, r: ('外层枚举完了 → 结束' if B.get('i') == S.i and 'i' in B else f'`i = {S.i}`：固定较左的一个数'),
        'for j in range': lambda S, B, r: ('内层枚举完了，回到外层' if B.get('j') == S.j and 'j' in B else f'`j = {S.j}`：配对的另一个数，保证 `i < j`'),
        'if nums[i] + nums[j] < target': '`{nums[i]} + {nums[j]} = {nums[i]+nums[j]}` 与 `target = {target}` → {"小于，计数" if nums[i]+nums[j] < target else "不小于，跳过"}',
        'res += 1': '又找到一对 `({i}, {j})`，`res` = =={res}==',
        'return res': '一共 =={res}== 对',
    },
    cards=dict(
        one_liner='数据规模很小，两两枚举下标对即可',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['数组 `nums` 和整数 `target`，数满足 `i < j` 且 `nums[i] + nums[j] < target` 的下标对个数',
                 '示例：`nums=[-1,1,2,3,1]`，`target=2` → `3`（(0,1)、(0,2)、(0,4)）'],
        quote='由于数据规模非常小，我在这里直接使用的暴力法，两两枚举下标对然后判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层 `i` 从 0 到 n-2，内层 `j` 从 `i+1` 到 n-1，保证 `i < j` 且每对只看一次',
              '和小于 `target` 就 `res += 1`',
              '原文提到：排序后双指针也行（同第一题思路），但这里 n ≤ 50 不必'],
        summary=['时间 `O(n^2)`，空间 `O(1)`；n ≤ 50 足够',
                 '易错：`j` 从 `i + 1` 开始，避免重复和自己配对；严格小于',
                 '数据更大时改成排序 + 相向双指针 `O(n log n)`',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
