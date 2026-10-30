CONFIG = dict(
    num=1386, title='安排电影院座位', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按行聚合 + 分情况讨论',
    code='''
class Solution(object):
    def maxNumberOfFamilies(self, n, reservedSeats):

        res = n * 2
        reserved_dict = {}
        for x, y in reservedSeats:
            if y != 1 and y != 10:
                if x not in reserved_dict:
                    reserved_dict[x] = []
                reserved_dict[x].append(y)
        
        for x in reserved_dict:
            res -= 2
            reserved_list = sorted(reserved_dict[x])
            if len(reserved_list) > 4:
                continue
            
            if len(reserved_list) == 1:
                res += 1
            elif reserved_list[0] > 5:
                res += 1
            elif reserved_list[-1] < 6:
                res += 1
            elif reserved_list[0] < 4 and reserved_list[-1] > 7:
                if len(reserved_list) == 2:
                    res += 1
                elif len(reserved_list) == 3 and (reserved_list[1] < 4 or reserved_list[1] > 7):
                    res += 1
                elif reserved_list[1] == 3 and reserved_list[2] == 8:
                    res += 1
        
        return res
''',
    call='Solution().maxNumberOfFamilies(3, [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]])',
    expect=4,
    views=[
        dict(type='map', var='reserved_dict', fmt=lambda k, v: f'第{k}行 → {v}', h=200, label='reserved_dict：行 → 已预定的 2~9 号座位'),
        dict(type='array', var='reserved_list', label='reserved_list（当前行，已排序）', h=150, cell=80),
        dict(type='text', h=70, fn=lambda S: (f"当前 `res` = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=['x', 'y', ('res', 'res', 'green')],
    captions={
        'res = n * 2': '每行最多 2 组，先假设全空：`res` = {n} × 2 = =={res}==',
        'if y != 1 and y != 10': lambda S, B, r: (f'座位 `{S.y}` 在 2~9 之内，要记录' if S.y not in (1, 10) else f'座位 `{S.y}` 在最左/最右，四连座本来就用不到 → ==跳过=='),
        'reserved_dict[x].append(y)': '第 `{x}` 行记下座位 `{y}` → `{reserved_dict[x]}`',
        'res -= 2': '第 `{x}` 行有预定，先按最坏情况扣掉 2 组：`res` → {res}',
        'reserved_list = sorted': '把这一行预定座位排序：`{reserved_list}`',
        'if len(reserved_list) > 4': lambda S, B, r: (f'已订 `{len(S.reserved_list)}` 个 > 4，2~9 只剩 4 个以下，==放不了== → 下一行' if len(S.reserved_list) > 4 else f'已订 `{len(S.reserved_list)}` 个，不超过 4，继续判断'),
        'if len(reserved_list) == 1': lambda S, B, r: ('只订了 1 个座位，左右总有一块是空的 → 能放 1 组' if len(S.reserved_list) == 1 else '不止 1 个座位，继续判断'),
        'elif reserved_list[0] > 5': lambda S, B, r: f'最左预定 `{S.reserved_list[0]}` ' + ('> 5：座位 2~5 全空 → 能放 1 组' if S.reserved_list[0] > 5 else '≤ 5，2~5 不行'),
        'elif reserved_list[-1] < 6': lambda S, B, r: f'最右预定 `{S.reserved_list[-1]}` ' + ('< 6：座位 6~9 全空 → 能放 1 组' if S.reserved_list[-1] < 6 else '≥ 6，6~9 不行'),
        'elif reserved_list[0] < 4': lambda S, B, r: ('只剩 4~7 可试：要求最左 < 4 且最右 > 7，即预定都在两侧' if (S.reserved_list[0] < 4 and S.reserved_list[-1] > 7) else '最左或最右压住了 4~7 → 这行放不了'),
        'if len(reserved_list) == 2': '只订了两端两个座位，中间 4~7 全空 → 能放 1 组',
        'res += 1': '这一行能放 1 组：`res` → =={res}==',
        'return res': '一共能安排 `{res}` 组',
    },
    cards=dict(
        one_liner='先假设每行 2 组，只对有预定的行扣 2 再看能否补回 1',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['每排 10 座，四人小组必须坐 `2-5`、`4-7`、`6-9` 之一，且全空',
                 '给出已预定的座位，求最多能安排几组',
                 '示例：`n=3`，`[[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]` → `4`'],
        quote='由于这里的行数非常多，因此我们不能考虑每一行。注意到每一行最多安排两组家庭，因此最多只能安排n * 2组家庭，先初始化答案为n * 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['座位 1 和 10 用不上，预定在那里的直接忽略',
              '按行聚合，只枚举有预定的行：先扣 2，再看能否安排 1 组',
              '预定座位排序后分情况：最左 > 5、最右 < 6，或只剩中间 4~7'],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '只订 1 个座位时，两侧至少有一块空，一定能补回 1 组',
                 '中间块要求预定都在 2、3 或 8、9，所以分 2、3、4 个预定讨论',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：他用位掩码一次判断三个四连座，这里是排序后手写分支'],
    ),
)
