CONFIG = dict(
    num=566, title='重塑矩阵', difficulty='Easy', category='模拟',
    author='yiduobo', technique='逐个读取 · 满 c 个换行',
    code='''
class Solution(object):
    def matrixReshape(self, nums, r, c):

        m = len(nums)
        n = len(nums[0])
        if m * n != r * c:
            return nums

        res = []
        cnt = 0
        for i in range(m):
            for j in range(n):
                if cnt == 0:
                    res.append([])
                    cnt = 0
                res[-1].append(nums[i][j])
                cnt += 1
                if cnt == c:
                    cnt = 0

        return res
''',
    call='Solution().matrixReshape([[1,2,3],[4,5,6]], 3, 2)',
    expect=[[1, 2], [3, 4], [5, 6]],
    views=[
        dict(type='text', fn=lambda S: f"原矩阵 {S['m']}×{S['n']}，目标 {S['r']}×{S['c']}" if 'm' in S and 'n' in S and 'r' in S else ''),
        dict(type='grid', var='nums', label='nums（原矩阵）', h=200,
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'green' if 'i' in S and 'j' in S and (i, j) < (S['i'], S['j']) else None),
        dict(type='text', fn=lambda S: f"`res` = =={S['res']}==  （当前行已放 `{S['cnt']}` 个，满 `{S['c']}` 个换行）" if 'res' in S and 'cnt' in S else '', h=60),
    ],
    watch=['i', 'j', ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'm * n != r * c': '元素总数 `{m}×{n}={m*n}`，目标 `{r}×{c}={r*c}`：{"不等，无法重塑，返回原矩阵" if m*n != r*c else "相等，可以重塑"}',
        'res.append([])': '`cnt == 0`：当前行是空的（刚好换行）→ 另起一行 `[]`',
        'res[-1].append': '把 `nums[{i}][{j}] = {nums[i][j]}` 放进 `res` 的最后一行：`{res}`',
        'cnt += 1': '这一行已放 `{cnt}` 个',
        'if cnt == c': lambda S, B, r: f'`cnt = {S.cnt}`，目标每行 `c = {S.c}` 个 → ' + ('==满了，下一个另起一行==' if S.cnt == S.c else '还没满，继续放'),
        10: '`cnt = 0`：当前行已放 0 个',
        15: '`cnt = 0`：本来就是 0（新行刚建，原文这句多余但无害）',
        19: '这一行放满了，`cnt` 清零 → 下一个元素另起一行',
        'return res': '重塑完成：`{res}`',
    },
    cards=dict(
        one_liner='按行读原矩阵，每满 c 个就另起一行',
        complexity='时间 `O(m*n)`，空间 `O(m*n)`（输出）',
        problem=['把 `m×n` 的矩阵重塑成 `r×c`，元素仍按行优先顺序排列',
                 '元素总数不同则无法重塑，返回原矩阵',
                 '示例：`[[1,2,3],[4,5,6]]`，`r=3, c=2` → `[[1,2],[3,4],[5,6]]`'],
        quote='首先判断m * n是否等于r * c，若不等于那么就无法reshape，直接返回原矩阵即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先比较元素总数，不等直接返回原矩阵',
              '逐行逐列遍历原矩阵，依次放入答案',
              '用 `cnt` 记录当前行已放几个，达到 `c` 个就另起一行'],
        summary=['时间 `O(m*n)`，空间 `O(m*n)`',
                 '易错：必须先判断 `m*n == r*c`',
                 '`cnt == 0` 时才新建行；达到 `c` 个要清零',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
