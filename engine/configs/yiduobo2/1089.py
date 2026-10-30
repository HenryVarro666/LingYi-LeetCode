ARR = [1, 0, 2, 3, 0, 4]
NEW = [y for x in ARR for y in ([0, 0] if x == 0 else [x])]   # 复写后（不截断）的新数组，仅用于对照


def _phase2(S):
    return 'index' in S


def _arr_color(S, k, v):
    if _phase2(S):
        t, ln = S['index'] + S['zero_cnt'], S['_line']
        if (ln == 17 and k == t) or (ln == 22 and k == t - 1):
            return 'green'                      # 这一步刚写入
        lo = t + 1 if ln == 16 else (t - 1 if ln == 22 else t)
        if k >= lo:
            return 'cyan'
        return None
    if 'cut_pos' in S and k == S['cut_pos']:
        return 'blue'
    return None


def _new_color(S, k, v):
    if k >= len(ARR):
        return None
    if not _phase2(S) and 'cut_pos' in S:
        pos = S['cut_pos'] + S['zero_cnt']
        if k <= pos:
            return 'purple'
    return None


def _new_ptr(S):
    if 'cut_pos' in S and not _phase2(S):
        return S['cut_pos'] + S['zero_cnt']
    return None


def _text(S):
    if _phase2(S):
        i, z = S['index'], S['zero_cnt']
        return f'`arr[{i}]` 在新数组中的位置：`index + zero_cnt = {i} + {z} = {i + z}`'
    if 'cut_pos' in S:
        return f'`arr[{S["cut_pos"]}]` 落在新数组第 `cut_pos + zero_cnt = {S["cut_pos"] + S["zero_cnt"]}` 位；新数组只保留前 `{len(ARR)}` 个'
    return '第一趟：从左往右，找新数组最后一个数在原数组中的下标 `cut_pos`'


def _if_end(S, B, ret):
    z, c, n = S.zero_cnt, S.cut_pos, len(S.arr)
    if z + c == n - 1:
        return f'`zero_cnt + cut_pos = {z} + {c} = {n - 1}`：`arr[{c}]` 正好是新数组的==最后一个数=='
    return f'`{z} + {c} = {z + c}` < `{n - 1}`：还没到新数组末尾'


def _if_zero1(S, B, ret):
    c = S.cut_pos
    if S.arr[c] == 0:
        return f'最后一个数是 `0`，但它的==复写那份被截掉了== → `ignore_last = True`'
    return f'最后一个数 `{S.arr[c]}` 不是 0'


def _if_zero2(S, B, ret):
    c = S.cut_pos
    if S.arr[c] == 0:
        return f'`arr[{c}] = 0`：要复写，新数组多占一位'
    return f'`arr[{c}] = {S.arr[c]}` 不是 0'


def _if_end2(S, B, ret):
    z, c, n = S.zero_cnt, S.cut_pos, len(S.arr)
    if z + c == n - 1:
        return f'复写后 `{z} + {c} = {n - 1}`：两个 0 正好填满新数组 → 结束'
    return f'`{z} + {c} < {n - 1}`：继续'


def _copy(S, B, ret):
    i, z = S.index, S.zero_cnt
    return f'`arr[{i}] = {S.arr[i + z]}` 搬到新位置 `arr[{i + z}]`（==从后往前搬==，不会覆盖还没搬的数）'


def _ign(S, B, ret):
    if B.ignore_last:
        return '这个 0 是新数组的最后一个数，它的复写被截掉了 → ==不复写=='
    return '`ignore_last = False` → 正常复写'


CONFIG = dict(
    num=1089, title='复写零', difficulty='Easy', category='双指针',
    author='yiduobo', technique='两趟扫描 · 先定截断点，再从后往前搬',
    tags=['字节30天'],
    code='''
class Solution(object):
    def duplicateZeros(self, arr):

        zero_cnt = 0
        ignore_last = False
        for cut_pos in range(len(arr)):
            if zero_cnt + cut_pos == len(arr) - 1:
                if arr[cut_pos] == 0:
                    ignore_last = True
                break
            if arr[cut_pos] == 0:
                zero_cnt += 1
                if zero_cnt + cut_pos == len(arr) - 1:
                    break

        for index in range(cut_pos, -1, -1):
            arr[index + zero_cnt] = arr[index]
            if arr[index] == 0:
                if ignore_last:
                    ignore_last = False
                else:
                    arr[index + zero_cnt - 1] = arr[index]
                    zero_cnt -= 1
''',
    call=f'''arr = {ARR}
Solution().duplicateZeros(arr)
arr''',
    expect=[1, 0, 0, 2, 3, 0],
    views=[
        dict(type='text', fn=_text, size=26),
        dict(type='array', var=lambda S: NEW, label=f'对照：复写后的完整新数组（只保留前 {len(ARR)} 个，紫 = 已确定）', h=200, cell=80,
             pointers={_new_ptr: 'purple'}, pointer_labels={_new_ptr: 'cut_pos+zero_cnt'}, color=_new_color,
             dim=lambda S, k, v: k >= len(ARR)),
        dict(type='array', var='arr', label='arr（原地修改；青 = 已搬到最终位置）', h=240, cell=96,
             pointers={'cut_pos': 'blue', 'index': 'orange', 'index + zero_cnt': 'pink'},
             pointer_labels={'index + zero_cnt': '新位置'}, color=_arr_color),
    ],
    watch=[('cut_pos', 'cut_pos', 'blue'), ('zero_cnt', 'zero_cnt', 'pink'), ('ignore_last', 'ignore_last', 'yellow'),
           ('index', 'index', 'orange')],
    captions={
        'zero_cnt = 0': '`zero_cnt`：扫描过程中有几个 0 被复写了',
        5: '`ignore_last`：新数组最后一个 0 是否==没被复写==',
        'for cut_pos in range': lambda S, B, ret: f'看 `arr[{S.cut_pos}] = {S.arr[S.cut_pos]}`',
        7: _if_end,
        8: _if_zero1,
        9: '记下：倒着搬时，这个 0 当作非 0 处理',
        10: '`cut_pos = {cut_pos}`：新数组的最后一个数就是 `arr[{cut_pos}]`',
        11: _if_zero2,
        12: '`zero_cnt` → {zero_cnt}',
        13: _if_end2,
        14: '`cut_pos = {cut_pos}`：新数组以复写的 `0, 0` 结尾',
        'for index in range(cut_pos, -1, -1)': lambda S, B, ret: (f'第二趟：从 `cut_pos` 往前，`index = {S.index}`'
                                                                 if B.get('index') != S.index else '搬完了'),
        'arr[index + zero_cnt] = arr[index]': _copy,
        'if arr[index] == 0': lambda S, B, ret: (f'`arr[{S.index}] = 0` → 可能要复写' if S.arr[S.index] == 0 else f'`{S.arr[S.index]}` 不是 0，不用复写'),
        'if ignore_last': _ign,
        20: '只用一次：把标记清掉',
        'arr[index + zero_cnt - 1] = arr[index]': '复写：在它前一格 `arr[{index + zero_cnt - 1}]` 再填一个 `0`',
        'zero_cnt -= 1': '这个 0 复写完，前面的数少偏移一位：`zero_cnt` → {zero_cnt}',
    },
    cards=dict(
        one_liner='先算出截断点 cut_pos 和复写的 0 的个数，再从后往前搬',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组中每个 `0` 复写一遍，其余元素右移；==超出原长度的部分丢弃==',
                 '必须原地修改，不返回任何值',
                 '示例：`[1,0,2,3,0,4,5,0]` → `[1,0,0,2,3,0,0,4]`',
                 '本视频：`[1,0,2,3,0,4]` → `[1,0,0,2,3,0]`（最后的 0 没被复写）'],
        quote='对于当前的arr[index]，其在新数组中的位置就应该是==index + zero_cnt==。……需要注意一种特殊情况是==新数组的最后一个数为0，但这个0不是被重写的==。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟从左往右：统计被复写的 0 的个数 `zero_cnt`，找到新数组最后一个数的下标 `cut_pos`',
              '第二趟从 `cut_pos` 往前：`arr[index]` 搬到 `index + zero_cnt`，遇 0 再填一个并 `zero_cnt -= 1`',
              '若最后一个数是 0 但复写那份被截掉，用 `ignore_last` 让它不复写'],
        result='`arr = [1,0,0,2,3,0]` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：从前往后搬会覆盖还没处理的数，必须从后往前',
                 '易错：截断处的 0 只放得下一份（`ignore_last`）',
                 '原文为 Python 2 风格，只删去了文档字符串'],
    ),
)
