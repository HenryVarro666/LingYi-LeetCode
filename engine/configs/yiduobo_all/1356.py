def _pc(v):
    return bin(v).count('1')


CONFIG = dict(
    num=1356, title='根据数字二进制下 1 的数目排序', difficulty='Easy', category='位运算',
    author='yiduobo', technique='逐个数 1 的个数再排序',
    tags=['灵神题单', '位运算', '难度分 1258'],
    code='''
class Solution(object):
    def sortByBits(self, arr):

        cnt_list = []
        for num in arr:
            tmp = num
            cnt_list.append(0)
            while tmp:
                cnt_list[-1] += tmp % 2
                tmp //= 2

        return [x[0] for x in sorted(zip(arr, cnt_list), key=lambda d:(d[1], d[0]))]
''',
    call='Solution().sortByBits([5, 3, 8, 6])',
    expect=[8, 3, 5, 6],
    views=[
        dict(type='text', size=28, fn=lambda S: '数组 `arr`（当前处理的数标蓝）'),
        dict(type='array', var='arr', h=200, cell=90, pointers={},
             color=lambda S, i, v: 'blue' if 'num' in S and S['num'] == v and S['_line'] < 11 else None),
        dict(type='text', size=28, fn=lambda S: ('`cnt_list`（各数二进制 1 的个数）：' + str(S['cnt_list'])) if 'cnt_list' in S else ''),
        dict(type='text', size=28, fn=lambda S: (f"拆位：`tmp = {S['tmp']}` = `{bin(S['tmp'])[2:]}`，最低位 `{S['tmp'] % 2}`" if 'tmp' in S and S['tmp'] > 0 and S['_line'] < 11
                                                  else ('`tmp = 0`：这个数的位拆完了' if 'tmp' in S and S['_line'] < 11 else ''))),
    ],
    watch=[('num', "num if 'num' in dir() else '-'", 'blue'), ('tmp', "tmp if 'tmp' in dir() else '-'", 'orange'), ('cnt_list', 'cnt_list', 'green')],
    captions={
        'cnt_list = []': '`cnt_list[i]` 将存 `arr[i]` 二进制里 1 的个数',
        'for num in arr': '取出 `num = {num}`（二进制 `{num:b}`）',
        'tmp = num': '拷贝一份 `tmp = {tmp}`，拆位时不破坏 `num`',
        'cnt_list.append(0)': '先给这个数留一个计数位 0：`cnt_list = {cnt_list}`',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}` 不为 0，还有位没数' if S.tmp else '`tmp = 0`：全部位数完了，这个数的计数 =={cnt}==' .replace('{cnt}', str(S.cnt_list[-1]))),
        'cnt_list[-1] +=': '最低位是 `{tmp % 2}`（`tmp % 2`）→ 当前数的 1 的个数累计 `{cnt_list[-1]}`',
        'tmp //= 2': '右移一位（整除 2）：`{B.tmp}` → `{tmp}`',
        'return': '把 `(数, 1的个数)` 配对，按 `(个数, 数值)` 排序，再取出数 → `{ret}`',
    },
    cards=dict(
        one_liner='先逐个数出 1 的个数，再按（个数，数值）排序',
        complexity='时间 `O(n log C + n log n)`，空间 `O(n)`',
        problem=['把数组按二进制里 ==1 的个数== 升序排',
                 '个数相同的，按 ==数值== 升序',
                 '示例：`[0,1,2,3,4,5,6,7,8]` → `[0,1,2,4,8,3,5,6,7]`'],
        quote='比较基础的题目，直接求出每个数二进制表示下1的数目，然后按照题意排序即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`while tmp:` 里每次取 `tmp % 2`（最低位），再 `tmp //= 2`',
              '每个数的结果存进 `cnt_list`，下标和 `arr` 一一对应',
              '`zip(arr, cnt_list)` 配对后，按 `(d[1], d[0])` 排序，最后只取数本身'],
        summary=['时间 `O(n log C + n log n)`，空间 `O(n)`，`C` 是数值上限',
                 '原文为 Python 2 写法，`tmp /= 2` 已改为 `tmp //= 2`（Python 3 的 `/` 是浮点除，会死循环）',
                 '`sorted` 的 key 是 `(个数, 数值)`，先比个数再比数值',
                 '对比灵神：灵神直接用 `bit_count()` 一次算好，不用自己拆位'],
    ),
)
