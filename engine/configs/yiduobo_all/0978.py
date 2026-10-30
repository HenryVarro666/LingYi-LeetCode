CONFIG = dict(
    num=978, title='最长湍流子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · 记起点和符号',
    tags=[],
    code='''
class Solution(object):
    def maxTurbulenceSize(self, arr):

        n = len(arr)
        start_pos = None
        flag = None
        res = 1
        for index in range(n - 1):
            if arr[index] == arr[index + 1]:
                if start_pos is not None:
                    res = max(res, index - start_pos + 1)
                start_pos = None
                flag = None
            
            elif arr[index] < arr[index + 1]:
                if flag == 1:
                    flag = 1 - flag
                else:
                    if start_pos is not None:
                        res = max(res, index - start_pos + 1) 
                    start_pos = index
                    flag = 0

            else:
                if flag == 0:
                    flag = 1 - flag
                else:
                    if start_pos is not None:
                        res = max(res, index - start_pos + 1) 
                    start_pos = index
                    flag = 1

        if start_pos is not None:
            res = max(res, n - start_pos)

        return res
''',
    call='Solution().maxTurbulenceSize([9,4,2,10,7,8,8,1,9])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"比较 `arr[{S['index']}] = {S['arr'][S['index']]}` 与 `arr[{S['index']+1}] = {S['arr'][S['index']+1]}`，当前 flag = =={S['flag']}==（1 表示上一步是下降，0 表示上一步是上升）") if 'index' in S and 'flag' in S and S['index'] + 1 < len(S['arr']) else '', size=26),
        dict(type='bars', var='arr', h=420,
             pointers={'index': 'blue'},
             window=(lambda S: S['start_pos'] if S.get('start_pos') is not None else S['index'],
                     lambda S: min(S['index'] + 1, len(S['arr']) - 1)),
             dim=lambda S, k, v: S.get('start_pos') is None and 'index' in S and k < S['index']),
    ],
    watch=[('index', 'index', 'blue'), ('start_pos', 'start_pos', 'pink'), ('flag', 'flag', 'purple'), ('res', 'res', 'green')],
    captions={
        7: '`res = 1`：任何单个元素都是湍流子数组，答案初值 ==1==',
        5: '`start_pos`：当前湍流段的起点，`None` 表示还没有段',
        6: '`flag`：上一对的方向，1 = 下降，0 = 上升',
        9: lambda S, B, r: (f"`{S.arr[S.index]} == {S.arr[S.index+1]}` → ==相等，湍流必须断开=="
                            if S.arr[S.index] == S.arr[S.index+1]
                            else f"`{S.arr[S.index]}` 与 `{S.arr[S.index+1]}` 不相等，接着看大小关系"),
        15: lambda S, B, r: (f"`{S.arr[S.index]} < {S.arr[S.index+1]}`：这一对在上升" if S.arr[S.index] < S.arr[S.index+1] else f"`{S.arr[S.index]} > {S.arr[S.index+1]}`：这一对在下降"),
        16: lambda S, B, r: ("上升，且 `flag = 1`（上一对下降）→ 符号交替，段继续" if S.flag == 1 else (f"上升，但 `flag = {S.flag}`，没有交替 → 旧段到此为止" if S.start_pos is not None else "上升，目前没有段 → 从这一对开新段")),
        25: lambda S, B, r: ("下降，且 `flag = 0`（上一对上升）→ 符号交替，段继续" if S.flag == 0 else (f"下降，但 `flag = {S.flag}`，没有交替 → 旧段到此为止" if S.start_pos is not None else "下降，目前没有段 → 从这一对开新段")),
        17: '符号翻转：`flag` → {flag}，段继续延长',
        26: '符号翻转：`flag` → {flag}，段继续延长',
        11: '旧段 `[{start_pos}, {index}]`，长度 `{index - start_pos + 1}`，`res = max({B.res}, {index - start_pos + 1}) = {res}`',
        20: '旧段 `[{start_pos}, {index}]`，长度 `{index - start_pos + 1}`，`res = max({B.res}, {index - start_pos + 1}) = {res}`',
        29: '旧段 `[{start_pos}, {index}]`，长度 `{index - start_pos + 1}`，`res = max({B.res}, {index - start_pos + 1}) = {res}`',
        12: '重置：`start_pos` 清空，相等的这一对不能当新段开头',
        13: '`flag` 也清空',
        21: '新段从 `index = {start_pos}` 开始（`arr[index]`、`arr[index+1]` 是开头）',
        30: '新段从 `index = {start_pos}` 开始（`arr[index]`、`arr[index+1]` 是开头）',
        22: '`flag = 0`：这一对是上升',
        31: '`flag = 1`：这一对是下降',
        34: '扫描完：末尾还有没结算的段 `[{start_pos}, {n-1}]`，长度 `{n - start_pos}`，`res` → {res}',
        36: '最长湍流子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='方向必须一升一降交替，一旦相等或同向就断开重来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['湍流子数组：相邻元素的比较符号一正一负交替变化',
                 '例如 `4 > 2 < 10 > 7 < 8`；相邻相等就不是湍流',
                 '求最长湍流子数组的长度，示例：`[9,4,2,10,7,8,8,1,9]` → `5`'],
        quote='湍流子数组中不会出现两个数相等的情况，同时要求满足符号在不断变化。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `start_pos` 记起点，`flag` 记上一对的方向',
              '相等：结算并清空；方向与上一对相反：段延长；方向相同：结算，再从这一对开始',
              '遍历完还要用末尾的段更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：相等时新段不能从这一对开始，`start_pos`、`flag` 都置空',
                 '易错：循环只到 `n-2`，末尾的段要在循环外结算',
                 '答案初值 1，数组长为 1 时也正确',
                 '原文已是 Python 3 可运行，未做修改'],
    ),
)
