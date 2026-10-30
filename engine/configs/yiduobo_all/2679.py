def _color(S, i, j, v):
    jj = S.get('j')
    if jj is None or S.get('_line', 0) < 9 or j != jj:
        return None
    if i <= S.get('i', -1) and v == S.get('v') and S.get('_line', 0) >= 12:
        return 'green'
    return 'yellow'


CONFIG = dict(
    num=2679, title='矩阵中的和', difficulty='Medium', category='模拟',
    author='yiduobo', technique='每行降序 · 逐列取最大',
    tags=[],
    code='''
class Solution(object):
    def matrixSum(self, nums):

        res = 0

        for line in nums:
            line.sort(reverse=True)
        
        for j in range(len(nums[0])):
            v = 0
            for i in range(len(nums)):
                v = max(v, nums[i][j])
            
            res += v
        
        return res
''',
    call='Solution().matrixSum([[7,2,1],[6,4,2],[6,5,3],[3,2,1]])',
    expect=15,
    views=[
        dict(type='grid', var='nums', cursors=[('i', 'j', 'blue', '(i,j)')], color=_color, h=400, label='nums（每行已降序，黄 = 当前列，绿 = 目前这列最大）'),
        dict(type='text', fn=lambda S: f"第 `{S['j']}` 列已看到最大值 `v = {S['v']}`，累计得分 =={S['res']}==" if 'j' in S and 'v' in S else ''),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'pink'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 是总分',
        'line.sort(reverse=True)': '这一行从大到小排：删最大数就是从左往右依次取，第 `j` 轮取第 `j` 列',
        'for j in range': lambda S, B, r: (f'开始第 {S.j} 轮：这一轮每行取走第 {S.j} 个数' if S.j != B.get('j') or 'j' not in B else '三列都处理完了'),
        'v = 0': '`v` 记这一轮取走的数里最大的，先清零',
        'v = max': lambda S, B, r: f'`v = max({B.v}, nums[{S.i}][{S.j}] = {S.nums[S.i][S.j]})` = =={S.v}=='
                                   + ('（新的最大）' if S.v != B.v else '（不变）'),
        'res += v': '这一轮得分 `{v}` 加进总分：`res` = =={res}==',
        'return res': '三轮得分 7 + 5 + 3，总分 =={res}==',
    },
    cards=dict(
        one_liner='每行从大到小排好，第 j 轮就是取每行第 j 个数',
        complexity='时间 `O(mn log n)`，空间 `O(1)`',
        problem=['矩阵每一轮：每行删掉最大数，再把删掉的数里最大的一个加进分数',
                 '重复到矩阵变空，求总分',
                 '示例：`[[7,2,1],[6,4,2],[6,5,3],[3,2,1]]` → `15`'],
        quote='遍历每一行，将每行都从大到小进行排序。接下来遍历每一列，每次选出当前列中的最大值累加到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['降序之后，每行当前最大数永远在最左边',
              '第 `j` 轮各行删掉的正好是第 `j` 列',
              '双层循环：外层列 `j`，内层行 `i` 求这列最大值 `v`'],
        summary=['时间 `O(mn log n)`，空间 `O(1)`',
                 '易错点：必须先对每行排序，否则列上的数并不是各行删掉的数',
                 '`v` 要在每一列开头清零',
                 '对比灵神：灵神升序 + `zip(*nums)` 一行搞定，yiduobo 降序 + 手写双层循环'],
    ),
)
