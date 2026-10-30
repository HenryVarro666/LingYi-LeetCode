def _txt(S):
    if 'base' not in S:
        return ''
    n = S['intLength']
    if 'left' not in S or 'q' not in S:
        return f"`base` = 100…0（共 `(n-1)//2` 个 0）= =={S['base']}==，最小的左半边"
    if S['_line'] in (11, 12) or 'left_list' not in S:
        return f"`left = base + q - 1` = `{S['base']} + {S['q']} - 1` = =={S['left']}==" + (f"，`>= base × 10 = {S['base'] * 10}` 越界" if S['left'] >= S['base'] * 10 else '')
    lst = S['left_list']
    half = ''.join(lst)
    return f"左半 `{half}` → 从下标 `{S['start_pos']}` 倒着一位位接到末尾 → 当前 =={S['left']}=="


CONFIG = dict(
    num=2217, title='找到指定长度的回文数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='左半边计数 · 逐位复制',
    tags=['灵神题单·数学算法', '难度分 1822'],
    code='''
class Solution(object):
    def kthPalindrome(self, queries, intLength):

        base = 10 ** ((intLength - 1) // 2)
        res = []
        for q in queries:
            left = base + q - 1
            if left >= base * 10:
                res.append(-1)
                continue
            left_list = list(str(left))
            if intLength % 2 == 0:
                start_pos = len(left_list) - 1
            else:
                start_pos = len(left_list) - 2
            
            for index in range(start_pos, -1, -1):
                left = left * 10 + int(left_list[index])
            res.append(left)
        
        return res
''',
    call='Solution().kthPalindrome([2, 6, 90, 91], 4)',
    expect=[1111, 1551, 9999, -1],
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='queries', label='queries', h=200,
             color=lambda S, i, v: 'blue' if 'q' in S and v == S['q'] else None),
        dict(type='array', var='res', label='res', h=200,
             color=lambda S, i, v: 'green' if v != -1 else 'pink'),
    ],
    watch=[('q', 'q', 'blue'), ('base', 'base', 'orange'), ('left', 'left', 'cyan'), 'start_pos'],
    captions={
        'base = 10': '长度 `{intLength}` 的回文数，左半边有 `(n-1)//2` = {(intLength - 1) // 2} 个 0：最小左半边 `base` = =={base}==',
        'res = []': '`res` 收集每个查询的答案',
        'for q in': lambda S, B, r: (f'开始处理查询：第 `{S.q}` 小' if S.get('q') != B.get('q') else '全部查询处理完'),
        'left = base + q - 1': '第 `{q}` 小的回文数，左半边就是 `100…0 + {q} - 1` = =={left}==',
        'if left >= base * 10': lambda S, B, r: (f'`{S.left} >= {S.base * 10}`：左半边多出一位，回文数不够 → ==越界=='
                                                 if S.left >= S.base * 10 else f'`{S.left} < {S.base * 10}`：没越界，继续构造'),
        'res.append(-1)': '没有第 `{q}` 个回文数 → 追加 `-1`',
        'continue': '直接处理下一个查询',
        'left_list = ': '把左半边拆成数字列表 `{left_list}`，等下逐位复制',
        'start_pos = len(left_list) - 1': '长度为偶数：左半边==每一位都要复制==，从最后一位 `{start_pos}` 开始',
        'start_pos = len(left_list) - 2': '长度为奇数：正中间那一位不复制，从倒数第二位 `{start_pos}` 开始',
        'for index in range': lambda S, B, r: ('`index` 扫完了，左半边已经全部镜像接好' if S.get('index') == B.get('index') and 'index' in B else f'`index = {S.index}`：从 `start_pos` 倒着扫到 0，把左半边==反过来==接在后面'),
        'left = left * 10': '`left` 末尾接上 `left_list[{index}]` = {left_list[index]} → =={left}==',
        'res.append(left)': '回文数构造完成：`{left}`，追加进 `res`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='左半边越小回文数越小：第 k 小 = 100…0 + k − 1，再镜像',
        complexity='时间 `O(n·L)`，空间 `O(L)`（n 个查询，L = 长度）',
        problem=['求长度为 `intLength` 的第 `queries[i]` 小的正回文数，不存在则 `-1`',
                 '示例：`[1,2,3,4,5,90], 3` → `[101,111,121,131,141,999]`',
                 '本视频：`[2,6,90,91], 4` → `[1111,1551,9999,-1]`'],
        quote='由于回文数的左右两个半边是对称的，那么高位越小，也就是左半边越小，整个回文数就越小。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小左半边是 `100…0`，记为 `base`，里面有 `(n-1)/2` 个 0',
              '第 `k` 小的左半边是 `base + k - 1`，若 `>= base * 10` 说明越界 → `-1`',
              '把左半边转成数字列表，倒着一位位接到数字末尾；奇数长度跳过中间那位'],
        summary=['时间 `O(n·L)`，空间 `O(L)`',
                 '原文为 Python 2 写法，整数除法 `(intLength - 1) / 2` 已改为 `//`',
                 '越界判断 `left >= base * 10`：左半边变成 L+1 位说明回文数用完了',
                 '对比灵神：灵神用 `q <= 9 * base` 判断，再用字符串反转拼接；yiduobo 用数值逐位接'],
    ),
)
