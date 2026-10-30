def _bits(S):
    arr = S['arr']
    if 'step' not in S:
        return '`arr[i]` = 第 i 步把第 `arr[i]` 位变成 1'
    on = set(arr[:S['step'] + 1])
    s = ''.join('1' if k + 1 in on else '0' for k in range(len(arr)))
    return f'前 `{S["step"] + 1}` 步后的二进制串：`{s}`；长度为 `{S["m"]}` 的 1 段有 ==`{S["cnt_list"][S["m"]]}`== 个'


CONFIG = dict(
    num=1562, title='查找大小为 M 的最新分组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='只维护区间边界 + 长度计数',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def findLatestStep(self, arr, m):

        n = len(arr)
        left = [None] * n
        right = [None] * n
        cnt_list = [0] * (n + 1)
        res = -1
        for step, num in enumerate(arr):
            num -= 1
            if num == 0 or left[num - 1] is None:
                new_left = None
            else:
                new_left = left[num - 1]
            
            if num == n - 1 or right[num + 1] is None:
                new_right = None
            else:
                new_right = right[num + 1]
            
            if new_left is None:
                if new_right is None:
                    left[num] = right[num] = num
                    cnt_list[1] += 1
                else:
                    left[num] = left[new_right] = num
                    right[num] = new_right
                    cnt_list[new_right - num] -= 1
                    cnt_list[new_right - num + 1] += 1
            elif new_right is None:
                right[num] = right[new_left] = num
                left[num] = new_left
                cnt_list[num - new_left] -= 1
                cnt_list[num - new_left + 1] += 1
            else:
                left[new_right] = new_left
                right[new_left] = new_right
                cnt_list[new_right - num] -= 1
                cnt_list[num - new_left] -= 1
                cnt_list[new_right - new_left + 1] += 1

            if cnt_list[m] > 0:
                res = step + 1
        
        return res
''',
    call='Solution().findLatestStep([1,2,4,3], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_bits, h=50),
        dict(type='array', var='arr', label='arr（第 step 步翻成 1 的位置，从 1 起）', h=150,
             color=lambda S, i, v: 'blue' if i == S.get('step') else None,
             dim=lambda S, i, v: S.get('step') is not None and i > S['step']),
        dict(type='array', var='left', pointers={'num': 'blue'}, label='left[i]：i 所在区间的左边界', h=170),
        dict(type='array', var='right', pointers={'num': 'blue'}, label='right[i]：i 所在区间的右边界', h=170),
        dict(type='array', var='cnt_list', pointers={'m': 'cyan'}, label='cnt_list[k]：长度为 k 的区间有几个', h=170,
             color=lambda S, i, v: 'green' if i == S.get('m') and v > 0 else None),
    ],
    skip=['right = [None]', 'cnt_list = [0]', 'res = -1'],
    watch=['step', 'num', 'new_left', 'new_right', ('m', 'm', 'cyan'), ('res', 'res', 'green')],
    captions={
        'num -= 1': '把位置换成 0 起：`num = {num}`（原文第 {num + 1} 位变成 1）',
        'if num == 0 or left[num - 1] is None': '左边有没有紧挨着的 1 段？`num-1` 处没有记录 → ==左侧无区间==；有就取它的左边界',
        'new_left = None': '左侧没有紧挨的区间：`new_left = None`',
        'new_left = left[num - 1]': '左侧区间的右端正好是 `num-1`，它的左边界 `left[num-1]` = ==`{new_left}`==',
        'if num == n - 1 or right[num + 1] is None': '右边有没有紧挨着的 1 段？看 `right[num+1]`',
        'new_right = None': '右侧没有紧挨的区间：`new_right = None`',
        'new_right = right[num + 1]': '右侧区间的左端正好是 `num+1`，它的右边界 `right[num+1]` = ==`{new_right}`==',
        'if new_left is None': '四种情况：先看左侧有没有区间',
        22: '左右都没有区间？是就新开一个长度 1 的区间',
        'left[num] = right[num] = num': '孤立的新区间：只记边界 `left[{num}] = right[{num}] = {num}`，`cnt_list[1]` 加 1',
        'left[num] = left[new_right] = num': '只有右侧有区间：它向左扩 1 格，新左边界 = `{num}`',
        'right[num] = new_right': '`num` 的右边界 = 原区间右端 `{new_right}`',
        28: '右侧原区间长 `{new_right - num}`，被扩大了 → `cnt_list[{new_right - num}]` 减 1',
        29: '扩成长度 `{new_right - num + 1}`：`cnt_list[{new_right - num + 1}]` 加 1',
        30: lambda S, B, r: ('左侧有、右侧没有 → 左区间向右扩 1 格' if S.new_right is None else '右侧也有区间，不是这一种，看最后一种'),
        'right[num] = right[new_left] = num': '左区间右扩：`right[{new_left}] = right[{num}] = {num}`，只改两端边界',
        'left[num] = new_left': '`num` 的左边界 = 原区间左端 `{new_left}`',
        33: '左侧原区间长 `{num - new_left}`，被扩大 → `cnt_list[{num - new_left}]` 减 1',
        34: '新长度 `{num - new_left + 1}` 多一个 → `cnt_list[{num - new_left + 1}]` 加 1',
        'left[new_right] = new_left': '==左右都有区间==：`num` 把两段连起来，新区间 `[{new_left}, {new_right}]`',
        'right[new_left] = new_right': '只更新新区间的两个端点，中间不用管',
        38: '右边那段（长 `{new_right - num}`）被并掉：`cnt_list[{new_right - num}]` 减 1',
        39: '左边那段（长 `{num - new_left}`）也被并掉：`cnt_list[{num - new_left}]` 减 1',
        40: '合并后长 `{new_right - new_left + 1}` 的多一个',
        'if cnt_list[m] > 0': lambda S, B, r: (f'`cnt_list[{S.m}] = {S.cnt_list[S.m]} > 0`：此刻==存在长度恰为 m 的 1 段== → 记下步数'
                                               if S.cnt_list[S.m] > 0 else f'`cnt_list[{S.m}] = 0`：此刻没有长度为 m 的段，答案不更新'),
        'res = step + 1': '`res = step + 1 = {res}`：步数从 1 数起，越晚越好，所以直接覆盖',
        'return res': '最后一次出现长度为 m 的段发生在第 `{res}` 步',
    },
    cards=dict(
        one_liner='把 1 段看成区间，只维护两端边界 + 各长度的个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长度 n 的二进制串开始全 0，`arr` 是 1..n 的排列，第 i 步把位置 `arr[i]` 翻成 1',
                 '求最后一个「恰好存在长度为 m 的连续 1」的步数，没有则 `-1`',
                 '示例：`arr=[3,5,1,2,4], m=1` → `4`', '本视频：`arr=[1,2,4,3], m=2` → `3`'],
        quote='在更新区间时，只需要更新区间的边界，也就是说可以在O(1)的时间内完成上述三种操作中的某一种。',
        quote_src='—— yiduobo 题解原文',
        idea=['新位置只会：新开 1 段 / 接到一段的端点 / 连起两段',
              '数组 `left`、`right` 只在区间端点记录对侧边界，`cnt_list[k]` 记长度为 k 的段数',
              '每步更新后 `cnt_list[m] > 0` 就把答案记成当前步数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：下标从 0 起，先 `num -= 1`；答案是 `step + 1`',
                 '合并时：旧的两段长度各减一，新长度 `new_right - new_left + 1` 加一',
                 '只更新边界即可，中间位置的 left/right 不再被访问',
                 '原文已是 Python 3 可运行的写法，未做改动；灵神把它归在「数组上的并查集」'],
    ),
)
