CONFIG = dict(
    num=941, title='有效的山脉数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 状态标记',
    tags=[],
    code='''
class Solution(object):
    def validMountainArray(self, arr):

        if len(arr) < 3:
            return False
        
        flag = 0
        for index in range(1, len(arr)):
            if arr[index] == arr[index - 1]:
                return False
            if flag == 0:
                if arr[index] < arr[index - 1]:
                    return False
                else:
                    flag = 1
            elif flag == 1:
                if arr[index] < arr[index - 1]:
                    flag = 2
            elif arr[index] > arr[index - 1]:
                    return False

        return flag == 2
''',
    call='Solution().validMountainArray([1,3,5,4,2,0])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: ('状态 `flag = ' + str(S['flag']) + '`：' + {0: '尚未开始', 1: '上升中', 2: '下降中'}[S['flag']]) if 'flag' in S else ''),
        dict(type='bars', var='arr', h=420, pointers={'index': 'blue'},
             color=lambda S, i, v: ('blue' if i == S.get('index') else None)),
    ],
    watch=['index', ('flag', 'flag', 'yellow')],
    captions={
        'len(arr) < 3': '山脉至少要有上升和下降各一段，`len = {len(arr)}`：{"太短 → False" if len(arr) < 3 else "够长"}',
        'flag = 0': '`flag`：0 = 还没确定，1 = 上升，2 = 下降',
        'for index': '比较 `arr[{index}] = {arr[index]}` 与前一个 `arr[{index - 1}] = {arr[index - 1]}`',
        'arr[index] == arr[index - 1]': '`{arr[index]}` 与 `{arr[index - 1]}`：{"相等 → 山脉必须严格升降 → False" if arr[index] == arr[index - 1] else "不相等，继续"}',
        'if flag == 0': '`flag = {flag}`：{"刚开始，看第一步方向" if flag == 0 else "已经确定方向，走别的分支"}',
        'if arr[index] < arr[index - 1]': '`{arr[index]} < {arr[index - 1]}`：{"成立" if arr[index] < arr[index - 1] else "不成立"}',
        'return False': '不满足山脉 → `False`',
        'flag = 1': '第一步是上升，`flag = 1`',
        'elif flag == 1': '`flag = {flag}`：{"正在上升，看有没有拐点" if flag == 1 else "不在上升，转入下降分支"}',
        'flag = 2': '下降了：前一个就是山顶，`flag = 2`',
        'elif arr[index] > arr[index - 1]': '下降阶段：`{arr[index]} > {arr[index - 1]}`？{"又上升了 → False" if arr[index] > arr[index - 1] else "仍在下降"}',
        'return flag == 2': '`flag = {flag}`：{"出现过下降 → True" if flag == 2 else "没有下降段 → False"}',
    },
    cards=dict(
        one_liner='用一个标记记住：上升中还是下降中',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组先严格递增到山顶，再严格递减，且山顶不在两端，才是有效山脉',
                 '判断 `arr` 是否为有效的山脉数组',
                 '本视频：`[1,3,5,4,2,0]` → `True`'],
        quote='采用一个标记表示当前数组是上升还是下降的，然后一趟遍历考察当前处理的数字arr[index]与arr[index - 1]的大小关系与当前的标记。',
        quote_src='—— yiduobo 题解原文',
        idea=['相等：直接不是山脉', '`flag = 0` 时第一步必须上升，否则一开始就在下降；之后 `flag = 1`',
              '上升中遇到下降 → 山顶，`flag = 2`；下降中又上升 → 不是山脉；最后 `flag` 必须是 2'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：长度小于 3、只升不降（`flag` 停在 1）、一开始就下降、相邻相等',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串'],
    ),
)
