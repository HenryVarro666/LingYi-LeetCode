CODE = '''
class Solution(object):
    def maxNumber(self, nums1, nums2, k):

        res = []

        for first_len in range(k + 1):
            if k - first_len > len(nums2):
                continue
            if first_len > len(nums1):
                break

            del_num = len(nums1) - first_len
            choose_num1 = []
            for num in nums1:
                while del_num > 0 and choose_num1 and num > choose_num1[-1]:
                    choose_num1.pop()
                    del_num -= 1
                choose_num1.append(num)
            
            del_num = len(nums2) - (k - first_len)
            choose_num2 = []
            for num in nums2:
                while del_num > 0 and choose_num2 and num > choose_num2[-1]:
                    choose_num2.pop()
                    del_num -= 1
                choose_num2.append(num)

            choose_num = []
            pos1 = pos2 = 0

            while pos1 < first_len or pos2 < k - first_len:
                l = 0
                while pos1 + l < first_len and pos2 + l < k - first_len and choose_num1[pos1 + l] == choose_num2[pos2 + l]:
                    l += 1
                if pos1 + l == first_len:
                    choose_num.append(choose_num2[pos2])
                    pos2 += 1
                elif pos2 + l == k - first_len or choose_num1[pos1 + l] > choose_num2[pos2 + l]:
                    choose_num.append(choose_num1[pos1])
                    pos1 += 1
                else:
                    choose_num.append(choose_num2[pos2])
                    pos2 += 1

            if not res:
                res = choose_num[:]
            else:
                flag = False
                for index in range(k):
                    if res[index] > choose_num[index]:
                        break
                    if res[index] < choose_num[index]:
                        flag = True
                        break
                if flag:
                    res = choose_num[:]

        return res
'''
_L = CODE.strip('\n').split('\n')


def _ln(txt, nth=0):
    return [i for i, l in enumerate(_L, 1) if txt in l][nth]


LN_C1 = _ln('choose_num1 = []')
LN_C2 = _ln('choose_num2 = []')
LN_CN = _ln('choose_num = []')
LN_M0 = _ln('while pos1 < first_len or')
LN_M1 = _ln('if not res:')


def _merging(S):
    return LN_M0 <= S['_line'] < LN_M1 and 'pos1' in S


def _ptr1(S):
    return S['pos1'] if _merging(S) and S['pos1'] < len(S['choose_num1']) else None


def _ptr2(S):
    return S['pos2'] if _merging(S) and S['pos2'] < len(S['choose_num2']) else None


def _look1(S):
    if _merging(S) and S.get('l', 0) > 0 and S['pos1'] + S['l'] < len(S['choose_num1']):
        return S['pos1'] + S['l']


def _look2(S):
    if _merging(S) and S.get('l', 0) > 0 and S['pos2'] + S['l'] < len(S['choose_num2']):
        return S['pos2'] + S['l']


def _show(S):
    ln = S['_line']
    if 'first_len' not in S:
        return '拆成两个子序列：从 nums1 取 `k1` 个、从 nums2 取 `k2 = k − k1` 个，再合并'
    if _merging(S) and 'choose_num2' in S:
        a, b = S['choose_num1'][S['pos1']:], S['choose_num2'][S['pos2']:]
        return f'剩余 `{a}` 与 `{b}`：比较后缀，谁的字典序大先取谁'
    if 'choose_num' in S and ln >= LN_M1 and S.get('res'):
        return f'本轮拼出 `{S["choose_num"]}`　当前最优 `res = {S["res"]}`'
    return f'`k1 = first_len = {S["first_len"]}`，`k2 = {S["k"] - S["first_len"]}`'


def _while(S, B, ret):
    if S.pos1 < S.first_len or S.pos2 < S.k - S.first_len:
        return f'两个数组还没取完（`pos1 = {S.pos1}`，`pos2 = {S.pos2}`）→ 再取一个'
    return '两个数组都取完了，合并结束'


def _inner(S, B, ret):
    ok = (S.pos1 + S.l < S.first_len and S.pos2 + S.l < S.k - S.first_len
          and S.choose_num1[S.pos1 + S.l] == S.choose_num2[S.pos2 + S.l])
    if ok:
        return (f'`{S.choose_num1[S.pos1 + S.l]}` == `{S.choose_num2[S.pos2 + S.l]}`，==相等，不能随便选==：'
                '往后比下一位')
    if S.pos1 + S.l >= S.first_len or S.pos2 + S.l >= S.k - S.first_len:
        return '有一边比到头了，停止往后比'
    return f'`{S.choose_num1[S.pos1 + S.l]}` ≠ `{S.choose_num2[S.pos2 + S.l]}`，在第 `{S.l}` 位分出大小'


def _take1(S, B, ret):
    if S.pos1 + S.l == S.first_len:
        return f'第一个数组先比到头 → 取第二个数组的 `{S.choose_num2[S.pos2]}`'
    return None


def _elif(S, B, ret):
    l = S.l
    if S.pos2 + l == S.k - S.first_len:
        return '第二个数组先比到头 → 取第一个数组的数'
    a, b = S.choose_num1[S.pos1 + l], S.choose_num2[S.pos2 + l]
    if a > b:
        return f'`{a} > {b}`：第一个数组的后缀更大 → ==取第一个数组的 `{S.choose_num1[S.pos1]}`=='
    return f'`{a} < {b}`：第二个数组的后缀更大 → 取第二个数组的数'


CONFIG = dict(
    num=321, title='拼接最大数', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='枚举拆分 + 单调栈选数 + 归并',
    tags=['单调栈', '最大字典序'][1:],
    code=CODE,
    call='Solution().maxNumber([6,7], [6,4], 3)',
    expect=[7, 6, 4],
    views=[
        dict(type='text', fn=lambda S: f"`nums1 = {S['nums1']}`　`nums2 = {S['nums2']}`　`k = {S['k']}`", size=26, h=60),
        dict(type='array', var=lambda S: S.get('choose_num1') if S['_line'] >= LN_C1 else None, label='choose_num1（nums1 里选出的 k1 个）', cell=76, h=190,
             pointers={_ptr1: 'blue', _look1: 'yellow'}, pointer_labels={_ptr1: 'pos1', _look1: 'pos1+l'}),
        dict(type='array', var=lambda S: S.get('choose_num2') if S['_line'] >= LN_C2 else None, label='choose_num2（nums2 里选出的 k2 个）', cell=76, h=190,
             pointers={_ptr2: 'pink', _look2: 'yellow'}, pointer_labels={_ptr2: 'pos2', _look2: 'pos2+l'}),
        dict(type='array', var=lambda S: S.get('choose_num') if S['_line'] >= LN_CN else None, label='choose_num（本轮合并结果；res 见下方）', cell=76, h=140),
        dict(type='text', fn=_show, size=26, h=70),
    ],
    skip=['res = []', 'choose_num1 = []', 'choose_num2 = []', 'choose_num = []', 'pos1 = pos2 = 0', 'l = 0', 'flag = False', 'pos1 += 1', 'pos2 += 1', 'del_num -= 1', 'l += 1', 'choose_num1.pop()', 'choose_num2.pop()'],
    max_steps=130,
    watch=[('first_len', 'first_len', 'blue'), ('del_num', 'del_num', 'orange'), ('l', 'l', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 保存目前拼出的最大数',
        'for first_len in range(k + 1)': lambda S, B, ret: (f'枚举 nums1 出 `{S.first_len}` 个、nums2 出 `{S.k - S.first_len}` 个'
                                                              if 'first_len' in S and S.first_len <= S.k else '枚举结束'),
        'if k - first_len > len(nums2)': lambda S, B, ret: (f'nums2 要出 `{S.k - S.first_len}` 个但只有 `{len(S.nums2)}` 个 → ==这种拆法不可能==，跳过'
                                                            if S.k - S.first_len > len(S.nums2) else
                                                            f'nums2 要出 `{S.k - S.first_len}` 个，够 → 可行'),
        'if first_len > len(nums1)': lambda S, B, ret: (f'nums1 要出 `{S.first_len}` 个但只有 `{len(S.nums1)}` 个 → 再大更不行，==结束枚举==' if S.first_len > len(S.nums1)
                                                         else f'nums1 要出 `{S.first_len}` 个，够 → 可行'),
        'del_num = len(nums1)': '从 nums1 取 `{first_len}` 个 = 删掉 `{del_num}` 个：用单调栈保字典序最大',
        'del_num = len(nums2)': '从 nums2 取 `{k - first_len}` 个 = 删掉 `{del_num}` 个',
        'for num in nums1': lambda S, B, ret: (f'扫描 nums1 的 `{S.num}`' if 'num' in S and B.get('num') != S.num or S.choose_num1 == [] else '扫描完 nums1，剩下的就是 nums1 里最大的 k1 个'),
        'for num in nums2': lambda S, B, ret: (f'扫描 nums2 的 `{S.num}`' if S.choose_num2 == [] or B.get('num') != S.num else '扫描完 nums2'),
        'while del_num > 0 and choose_num1': lambda S, B, ret: (
            f'`{S.num} > {S.choose_num1[-1]}` 且还要删 `{S.del_num}` 个 → ==弹出栈顶更小的数==，名额 −1' if S.del_num > 0 and S.choose_num1 and S.num > S.choose_num1[-1]
            else ('还要删的数量是 0 → 不再弹' if S.del_num <= 0 else ('栈空，不弹' if not S.choose_num1 else f'`{S.num} ≤ {S.choose_num1[-1]}`，不弹'))),
        'while del_num > 0 and choose_num2': lambda S, B, ret: (
            f'`{S.num} > {S.choose_num2[-1]}` 且还要删 `{S.del_num}` 个 → ==弹出栈顶更小的数==，名额 −1' if S.del_num > 0 and S.choose_num2 and S.num > S.choose_num2[-1]
            else ('还要删的数量是 0 → 不再弹' if S.del_num <= 0 else ('栈空，不弹' if not S.choose_num2 else f'`{S.num} ≤ {S.choose_num2[-1]}`，不弹'))),
        'choose_num1.pop()': '弹出 `{B.choose_num1[-1]}`',
        'choose_num2.pop()': '弹出 `{B.choose_num2[-1]}`',
        'del_num -= 1': '还要删的个数减一：`del_num = {del_num}`',
        'choose_num1.append(num)': '`{num}` 入栈 → `choose_num1 = {choose_num1}`',
        'choose_num2.append(num)': '`{num}` 入栈 → `choose_num2 = {choose_num2}`',
        'while pos1 < first_len or': _while,
        'while pos1 + l < first_len and': _inner,
        'l += 1': '前 `{l}` 位都相同，继续往后看',
        'if pos1 + l == first_len': lambda S, B, ret: (_take1(S, B, ret) or f'第一个数组没有先比到头 → 看下一个分支'),
        'elif pos2 + l == k - first_len': _elif,
        'choose_num.append(choose_num2[pos2])': '取 `{choose_num[-1]}` → `choose_num = {choose_num}`；`pos2` 后移',
        'choose_num.append(choose_num1[pos1])': '取 `{choose_num[-1]}` → `choose_num = {choose_num}`；`pos1` 后移',
        'if not res': lambda S, B, ret: ('`res` 还是空 → 直接把本轮结果当作最优' if not S.res
                                           else '已有 `res` → 逐位比较本轮结果和 `res`'),
        'res = choose_num[:]': '`res = {res}`',
        'for index in range(k)': lambda S, B, ret: f'比较第 `{S.index}` 位：`res[{S.index}] = {S.res[S.index]}`，`choose_num[{S.index}] = {S.choose_num[S.index]}`',
        'if res[index] > choose_num[index]': lambda S, B, ret: (f'`{S.res[S.index]} > {S.choose_num[S.index]}`：res 更大 → ==本轮不要=='
                                                               if S.res[S.index] > S.choose_num[S.index] else f'`{S.res[S.index]} > {S.choose_num[S.index]}` 不成立，继续看'),
        'if res[index] < choose_num[index]': '`{res[index]} < {choose_num[index]}`：本轮更大 → ==换成本轮==',
        'flag = True': '`flag = True`',
        'if flag': lambda S, B, ret: ('本轮更大 → 更新 `res`' if S.flag else '本轮不更大 → 保留 `res`'),
        'return res': '所有拆法试完，最大数 `{ret}`',
    },
    cards=dict(
        one_liner='枚举拆分，各自选最大，再归并（相等看后缀）',
        complexity='时间 `O(k·(m+n+k))`，空间 `O(k)`',
        problem=['从 `nums1`、`nums2` 的数字里共选 `k` 个，拼成最大的数',
                 '同一数组里选出的数字，相对顺序不能变',
                 '示例：`[6,7]`，`[6,0,4]`，`k = 5` → `[6,7,6,0,4]`',
                 '本视频：`[6,7]`，`[6,4]`，`k = 3` → `[7,6,4]`'],
        quote='对于最后拼接长答案的两个数组，设其长度分别为k1与k2，那么这两个数组在nums1和nums2中一定是字典序最大的，于是可以从0到k枚举k1',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举 `k1`，`k2 = k − k1`：两边各取字典序最大的子序列',
              '取最大子序列 = 删掉 `len − k1` 个数：沿用 316 的单调栈，弹栈条件是栈顶更小且还能删',
              '合并像归并排序，但相等时要往后比：谁的后缀大，先取谁'],
        summary=['时间 `O(k·(m+n+k))`，空间 `O(k)`',
                 '易错：`k1 > len(nums1)` 时要 `break`，`k2 > len(nums2)` 时只能 `continue`',
                 '易错：两数相等不能随便取，如 `[6,7]` 和 `[6,0,4]` 要先取第一个 6',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '栈没删够时多出的数不会被用到：合并时有 `k1`、`k2` 作边界',
                 '最后逐位比较，取字典序最大的那一轮'],
    ),
)
