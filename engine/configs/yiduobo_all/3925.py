CONFIG = dict(
    num=3925, title='连接逆序数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='直接模拟 · 反转后拼接',
    tags=[],
    code='''
class Solution(object):
    def concatWithReverse(self, nums):
        
        return nums + nums[::-1]
''',
    call='Solution().concatWithReverse([2,5,1])',
    expect=[2, 5, 1, 1, 5, 2],
    views=[
        dict(type='text', size=28, fn=lambda S: '按题意：前半是 `nums`，后半是 `nums` 反转'),
        dict(type='array', var='nums', label='nums', h=170, cell=100, color=lambda S, i, v: 'blue'),
        dict(type='array', var='nums[::-1]', label='nums 反转', h=170, cell=100, color=lambda S, i, v: 'pink'),
        dict(type='array', var='nums + nums[::-1]', label='拼接后的 ans（长 2n）', h=170, cell=100,
             color=lambda S, i, v: 'blue' if i < len(S['nums']) else 'pink'),
    ],
    watch=[('n', 'len(nums)', 'blue')],
    captions={
        'return nums': '反转得 `{nums[::-1]}`，接在 `{nums}` 后面 → =={nums + nums[::-1]}==',
    },
    cards=dict(
        one_liner='题目怎么说就怎么做：反转一份，接在后面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长度 `n` 的数组 `nums`，构造长度 `2n` 的 `ans`',
                 '前 `n` 个与 `nums` 相同，后 `n` 个为 `nums` 的逆序',
                 '本视频：`[2,5,1]` → `[2,5,1,1,5,2]`'],
        quote='直接按照题目要求，将nums反转后拼接在nums后方就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[::-1]` 得到反转后的新列表',
              '`nums + 反转列表` 就是长度 `2n` 的答案',
              '回头验证：`ans[i + n] = nums[n - i - 1]` 成立'],
        before=[dict(heading='先看下标关系', lines=[
            '`ans[i] = nums[i]`：前 `n` 位原样照抄',
            '`ans[i + n] = nums[n - i - 1]`：后 `n` 位从 `nums` 末尾往前读',
            '`i = 0` 读最后一个，`i = n-1` 读第一个 → 就是逆序'])],
        after=[dict(heading='手写循环 vs 切片', lines=[
            '手写：循环 `i` 从 `0` 到 `n-1`，每次 `ans.append(nums[n - i - 1])`',
            '切片 `nums[::-1]` 一步做完同样的事，而且更快',
            '边界：`n = 1` 时 `[x]` → `[x, x]`，逆序保持不变'])],
        summary=['时间、空间 `O(n)`',
                 '`[::-1]` 返回新列表，不修改 `nums`',
                 '原文已是 Python 3 可运行写法，代码未改',
                 '对比灵神：两人代码相同，灵神题解只有这一行，这里多了按题意验证的推理'],
    ),
)
