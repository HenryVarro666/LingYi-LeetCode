CONFIG = dict(
    num=2295, title='替换数组中的元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记录位置',
    tags=[],
    code='''
class Solution(object):
    def arrayChange(self, nums, operations):

        pos_dict = {}
        for index, num in enumerate(nums):
            pos_dict[num] = index
        
        for x, y in operations:
            if x in pos_dict:
                pos_dict[y] = pos_dict[x]
                pos_dict.pop(x)
        
        res = nums[:]
        for num, index in pos_dict.items():
            res[index] = num
        
        return res
''',
    call='Solution().arrayChange([1,2,4,6], [[1,3],[3,5],[6,1]])',
    expect=[5, 2, 4, 1],
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=200),
        dict(type='map', var='pos_dict', label='pos_dict（数值 → 它在数组里的下标）', fmt=lambda k, v: f'{k} → {v}', h=150, font=34),
        dict(type='array', var='res', label='res（按 pos_dict 还原）', cell=100, h=170, pointers={'index': 'blue'}),
        dict(type='text', h=80, size=30, fn=lambda S: (f"操作 `{S['x']} → {S['y']}`" if 'x' in S and 'y' in S and S['_line'] <= 11 else '')),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('num', 'num', 'orange'), ('index', 'index', 'green')],
    captions={
        'pos_dict = {}': '`pos_dict` 记录每个数当前在数组里的位置',
        'pos_dict[num] = index': '`{num}` 在下标 `{index}`：`pos_dict[{num}] = {index}`',
        'for x, y in operations': lambda S, B, ret: (f'下一个操作：把 `{S.x}` 换成 `{S.y}`' if S.x in S.pos_dict else '操作做完了'),
        'if x in pos_dict': '`{x}` 在表里（题目保证），继续',
        'pos_dict[y] = pos_dict[x]': '`{y}` 接手 `{x}` 的位置：`pos_dict[{y}] = {pos_dict[y]}`',
        'pos_dict.pop(x)': '`{x}` 已被换掉，从表里删除',
        'res = nums[:]': '操作都做完，复制一份 `res` 准备还原',
        'res[index] = num': '`{num}` 放回下标 `{index}`：`res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='用哈希表记位置，替换就是把位置“过户”',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['依次把 `operations[i][0]` 替换成 `operations[i][1]`',
                 '保证被换的数存在、新数不存在；返回最终数组',
                 '示例：`[1,2,4,6]`，操作 `[[1,3],[4,7],[6,1]]` → `[3,2,7,1]`；本视频换成 `[[1,3],[3,5],[6,1]]` → `[5,2,4,1]`'],
        quote='数组在任意时刻都不包含重复的元素。……此时的pos[x]就是x在数组中的下标，替换完成后这个下标的值将变为y，那么就有pos[y] = pos[x]。同时，x被替换掉之后数组中不再有x存在，因此需要将x从哈希表中去除。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组元素互不相同，替换后也不会重复',
              '哈希表 `pos_dict` 记每个数的下标；换 x 为 y：下标过户给 y，删掉 x',
              '最后按 `pos_dict` 把每个数放回下标，得到答案'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '正序模拟依赖“元素互不相同”，这是题目保证的',
                 '易错：必须 `pop(x)`，否则旧值会把新值覆盖回去',
                 '原文已是 Python 3 可运行的写法，无需修改',
                 '对比灵神：他倒着遍历 operations，不用记下标'],
    ),
)
