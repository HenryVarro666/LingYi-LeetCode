def _txt(S):
    if 'index' in S and 'd' in S:
        i = S['index']
        if i >= 2:
            return f'`arr[{i}] − arr[{i-1}] = {S["arr"][i]} − {S["arr"][i-1]}` = =={S["arr"][i] - S["arr"][i-1]}==，公差 `d = {S["d"]}`'
    if 'd' in S:
        return f'公差 `d = arr[1] − arr[0] = {S["d"]}`'
    return ''


CONFIG = dict(
    num=1502, title='判断能否形成等差数列', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='排序后扫一趟比差值',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def canMakeArithmeticProgression(self, arr):

        arr = sorted(arr)
        d = arr[1] - arr[0]
        for index in range(2, len(arr)):
            if arr[index] - arr[index - 1] != d:
                return False
        
        return True
''',
    call='Solution().canMakeArithmeticProgression([10,1,16,7,13,4])',
    expect=True,
    views=[
        dict(type='array', var='arr', pointers={'index': 'blue'}, label='arr（排序后）', h=300,
             color=lambda S, i, v: None),
        dict(type='text', fn=_txt, size=32, h=130),
    ],
    watch=['index', 'd'],
    captions={
        'arr = sorted': '等差数列一定有序，先排序：`arr` = =={arr}==',
        'd = arr[1]': '前两项定下公差：`d = {arr[1]} − {arr[0]}` = =={d}==',
        'for index': '检查第 `{index}` 项和前一项的差',
        'if arr[index]': '`arr[{index}] − arr[{index - 1}] = {arr[index] - arr[index - 1]}`，和 `d = {d}` {"不同 → 返回 False" if arr[index] - arr[index - 1] != d else "相同 → 继续"}',
        'return True': '每一对相邻项的差都等于 `d` → ==是等差数列==',
    },
    cards=dict(
        one_liner='排好序，一趟扫描比较相邻项的差是否都一样',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`arr` 能否重新排列成等差数列',
                 '示例：`[3,5,1]` → `true`；`[1,2,4]` → `false`',
                 '本视频：`[10,1,16,7,13,4]` → `true`'],
        quote='比较基础的题目。直接一趟扫描，计算相邻项之间的差值，并对比这个差值是否相同即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['能重排成等差数列，排序后一定就是它',
              '用前两项算出公差 `d`',
              '后面每个相邻差都和 `d` 比较，不同就返回 `False`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 新建列表）',
                 '`range(2, len(arr))` 从 2 开始，因为前两项已经定了 `d`',
                 '对比灵神：灵神主推 `O(n)` 的公差法，这里是最直接的排序法'],
    ),
)
