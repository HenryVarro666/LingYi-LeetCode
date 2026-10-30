CONFIG = dict(
    num=3925, title='连接逆序数组', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='切片拼接',
    tags=[],
    code='''
class Solution:
    def concatWithReverse(self, nums: list[int]) -> list[int]:
        return nums + nums[::-1]
''',
    call='Solution().concatWithReverse([1,2,3,4])',
    expect=[1, 2, 3, 4, 4, 3, 2, 1],
    views=[
        dict(type='text', size=28, fn=lambda S: '`nums[::-1]` 是 `nums` 的逆序，`+` 把两个列表首尾拼起来'),
        dict(type='array', var='nums', label='nums（前 n 个：原样）', h=170, cell=100,
             color=lambda S, i, v: 'blue'),
        dict(type='array', var='nums[::-1]', label='nums[::-1]（后 n 个：逆序）', h=170, cell=100,
             color=lambda S, i, v: 'pink'),
        dict(type='array', var='nums + nums[::-1]', label='ans = nums + nums[::-1]（长度 2n）', h=170, cell=100,
             color=lambda S, i, v: 'blue' if i < len(S['nums']) else 'pink'),
    ],
    watch=[('n', 'len(nums)', 'blue'), ('2n', 'len(nums) * 2', 'green')],
    captions={
        'return nums': '`nums` = `{nums}`，`nums[::-1]` = `{nums[::-1]}`，拼接得 =={nums + nums[::-1]}==（长度 `{2 * len(nums)}`）',
    },
    cards=dict(
        one_liner='原数组后面直接接上它的逆序，一行切片搞定',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`（返回值不计入）',
        problem=['给长度 `n` 的数组 `nums`，造一个长 `2n` 的 `ans`',
                 '前 `n` 个和 `nums` 相同，后 `n` 个是 `nums` 的逆序',
                 '示例：`[1,2,3]` → `[1,2,3,3,2,1]`；本视频：`[1,2,3,4]`'],
        quote='return nums + nums[::-1]',
        quote_src='—— 灵茶山艾府题解代码（原文只有这一行代码）',
        idea=['`nums[::-1]`：步长 `-1` 的切片，得到逆序的新列表',
              '列表相加 `a + b`：生成新列表，先放 `a` 再放 `b`',
              '对照题意：`ans[i + n] = nums[n - i - 1]`，正是逆序'],
        before=[dict(heading='先看下标关系', lines=[
            '`ans[i] = nums[i]`：前 `n` 位原样照抄',
            '`ans[i + n] = nums[n - i - 1]`：后 `n` 位从 `nums` 末尾往前读',
            '`i = 0` 读最后一个，`i = n-1` 读第一个 → 就是逆序'])],
        after=[dict(heading='手写循环 vs 切片', lines=[
            '手写：循环 `i` 从 `0` 到 `n-1`，每次 `ans.append(nums[n - i - 1])`',
            '切片 `nums[::-1]` 一步做完同样的事，而且更快',
            '边界：`n = 1` 时 `[x]` → `[x, x]`，逆序保持不变'])],
        summary=['时间、空间都是 `O(n)`',
                 '`nums[::-1]` 和 `+` 都会生成新列表，不会改动原数组',
                 '易错：别写成 `nums.reverse()`，它原地修改并返回 `None`',
                 '同类写法：`ans = nums.copy(); ans.extend(reversed(nums))`'],
    ),
)
