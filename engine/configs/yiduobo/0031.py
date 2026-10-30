def _scan1(S, B, ret):
    a, k = B.nums, S.index
    if a[k] > a[k - 1]:
        return f'`nums[{k}] = {a[k]} > nums[{k - 1}] = {a[k - 1]}`：后 `{len(a) - k + 1}` 位能交换出更靠后的排列 → 记下 `pos = {k}`'
    return f'`nums[{k}] = {a[k]} ≤ nums[{k - 1}] = {a[k - 1]}`：这一段仍是逆序，继续往前'


def _scan2(S, B, ret):
    a, k, p = B.nums, S.index, B.pos
    if a[k] > a[p]:
        return f'`nums[{k}] = {a[k]} > nums[pos] = {a[p]}`：是候选'
    return f'`nums[{k}] = {a[k]} ≤ {a[p]}`：不能换到 pos 上'


def _color(S, i, v):
    p, sp = S.get('pos'), S.get('sawp_pos')
    if S.get('_line', 0) >= 14 and isinstance(p, int) and i == p:
        return 'blue'
    if S.get('_line', 0) >= 14 and isinstance(sp, int) and i == sp:
        return 'pink'
    return None


CONFIG = dict(
    num=31, title='下一个排列', difficulty='Medium', category='技巧',
    author='yiduobo', technique='找规律 · 交换 + 翻转',
    code='''
class Solution(object):
    def nextPermutation(self, nums):
        pos = 0
        for index in range(len(nums) - 1, 0, -1):
            if nums[index] > nums[index - 1]:
                pos = index
                break
        if pos == 0:
            for index in range(len(nums) // 2):
                tmp = nums[index]
                nums[index] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
        else:
            pos -= 1
            sawp_pos = None
            sawp_num = None
            for index in range(len(nums) - 1, pos, -1):
                if nums[index] > nums[pos]:
                    if sawp_num is None or sawp_num > nums[index]:
                        sawp_num = nums[index]
                        sawp_pos = index

            tmp = nums[pos]
            nums[pos] = nums[sawp_pos]
            nums[sawp_pos] = tmp

            for index in range((len(nums) - pos - 1) // 2):
                tmp = nums[pos + index + 1]
                nums[pos + index + 1] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
''',
    call='''nums = [2, 3, 6, 5, 4, 1]
Solution().nextPermutation(nums)
nums''',
    expect=[2, 4, 1, 3, 5, 6],
    views=[
        dict(type='array', var='nums', label='nums', h=250, cell=110,
             pointers={'index': 'cyan', 'pos': 'blue', 'sawp_pos': 'pink'},
             pointer_labels={'sawp_pos': 'sawp_pos'},
             window=(lambda S: S['pos'] + 1 if S.get('_line', 0) >= 14 and isinstance(S.get('pos'), int) else None,
                     lambda S: len(S['nums']) - 1 if S.get('_line', 0) >= 14 and isinstance(S.get('pos'), int) else None),
             color=_color),
        dict(type='text', fn=lambda S: ('规律 (1)：前 k 位相同时，第 k+1 位小的排在前面' if S.get('_line', 0) < 14
                                        else '==青框== = `nums[pos+1:]`：交换前后都是==逆序==的'), size=26, h=60),
        dict(type='text', fn=lambda S: '规律 (2)：`a[i] < a[j]` 且 `i < j`，交换后一定得到更靠后的排列', size=26, h=60),
        dict(type='text', fn=lambda S: (f"候选：`sawp_num = {S.get('sawp_num')}`（大于 `nums[pos]` 的数中最小的）"
                                        if 'sawp_num' in S else ''), size=28, h=60),
    ],
    watch=[('index', 'index', 'cyan'), ('pos', 'pos', 'blue'), ('sawp_pos', 'sawp_pos', 'pink'), ('sawp_num', 'sawp_num'), ('tmp', 'tmp')],
    captions={
        'pos = 0': '`pos = 0` 表示“还没找到”',
        'for index in range(len(nums) - 1, 0, -1)': '从后往前扫描：`index = {index}`',
        'if nums[index] > nums[index - 1]': _scan1,
        'sawp_pos = index': '`sawp_pos = {sawp_pos}`',
        'pos = index': '`pos = {pos}`',
        'break': '找到了就停：再往前加入交换序列只会变得更靠后（规律 1）',
        'if pos == 0': lambda S, B, ret: ('`pos == 0`：整个数组逆序，整体翻转' if S.pos == 0
                                          else f'`pos = {S.pos}` ≠ 0：存在 `a[pos] > a[pos-1]`'),
        'pos -= 1': '`pos - 1 = {pos}` 就是我们应该交换的数：`nums[{pos}] = {nums[pos]}`',
        'sawp_pos = None': '准备在 `pos` 后面找“大于 `nums[pos]` 的数中最小的那个”',
        'sawp_num = None': '`sawp_num` 记录它的值',
        'for index in range(len(nums) - 1, pos, -1)': lambda S, B, ret: (
            f'扫描 `index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`' if B.get('index') != S.index or B.get('sawp_pos', 0) is None and S.index == len(S.nums) - 1
            else f'扫描结束：大于 `nums[pos]` 的最小数是 `nums[{S.sawp_pos}] = {S.sawp_num}`'),
        'if nums[index] > nums[pos]': _scan2,
        'if sawp_num is None': lambda S, B, ret: ('还没有候选 → 记下它' if B.sawp_num is None
                                                  else (f'`{S.nums[S.index]}` 比当前候选 `{B.sawp_num}` 更小 → 更新'
                                                        if B.sawp_num > S.nums[S.index]
                                                        else f'`{S.nums[S.index]}` 不比候选 `{B.sawp_num}` 小')),
        'sawp_num = nums[index]': '`sawp_num = {sawp_num}`',
        'tmp = nums[pos]': '交换 `nums[pos]` 与 `nums[sawp_pos]`：先存 `tmp = {tmp}`',
        'nums[pos] = nums[sawp_pos]': '`nums[{pos}] = {nums[pos]}`',
        'nums[sawp_pos] = tmp': '`nums[{sawp_pos}] = {tmp}`：交换完成，`nums[pos+1:]` 依然是逆序',
        'for index in range((len(nums) - pos - 1) // 2)': lambda S, B, ret: (
            f'翻转 `nums[pos+1:]`：第 `{S.index}` 对' if B.get('tmp') is None or B.get('index') != S.index
            else '翻转完成，得到下一个排列'),
        'tmp = nums[pos + index + 1]': '`tmp = nums[{pos + index + 1}] = {tmp}`',
        'nums[pos + index + 1] = nums[len(nums) - index - 1]': '`nums[{pos + index + 1}] = nums[{len(nums) - index - 1}] = {nums[pos + index + 1]}`',
        'nums[len(nums) - index - 1] = tmp': '`nums[{len(nums) - index - 1}] = {tmp}`：这一对交换完毕 → `{nums}`',
    },
    cards=dict(
        one_liner='从后往前找能交换出更靠后排列的位置，换上最小的更大数，再翻转',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` ==原地==改成字典序中的下一个排列',
                 '已经是最大排列（如 `[3,2,1]`）则改成最小排列 `[1,2,3]`',
                 '示例：`[1,2,3]` → `[1,3,2]`，`[1,1,5]` → `[1,5,1]`'],
        quote='对于一个排列a，如果能通过交换最后p位中的数字形成靠后的排列，那么就==不应该把倒数第p + 1加入到交换的序列中==。',
        quote_src='—— yiduobo 题解',
        idea=['规律 (1)：前 `k` 位相同，第 `k+1` 位小的排在前面',
              '规律 (2)：`a[i] < a[j]` 且 `i < j`，交换后一定更靠后',
              '从后往前找第一个 `a[pos] > a[pos-1]`；`pos-1` 换成后面大于它的最小数，再翻转'],
        result='`[2,3,6,5,4,1]` 的下一个排列是 `[2,4,1,3,5,6]` ✓',
        summary=['三次扫描：找 `pos`、找 `sawp_pos`、翻转，时间 `O(n)`',
                 '找最小的更大数时扫描了整个后缀；其实后缀逆序，从右往左第一个更大的就是',
                 '变量名 `sawp_pos/sawp_num` 照原文保留（原文拼写）',
                 '原文为 Python 2 写法：两处 `/ 2` 改为 `// 2`，并删去文档字符串'],
    ),
)
