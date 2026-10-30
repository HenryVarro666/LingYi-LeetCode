CONFIG = dict(
    num=2844, title='生成特殊数字的最少操作', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举四种结尾 · 从后往前贪心找',
    tags=['贪心算法', '思维题', '难度分 1588'],
    code='''
class Solution(object):
    def minimumOperations(self, num):

        def check(first, second):
            p = len(num_list) - 1
            res = len(num_list)
            while p >= 0 and num_list[p] != first:
                p -= 1

            if p == -1:
                return res
            
            if first == 0:
                res -= 1
            
            p -= 1
            while p >= 0 and num_list[p] != second:
                p -= 1

            if p == -1:
                return res
            
            return len(num_list) - p - 2

        num_list = list([int(x) for x in str(num)])
        res = len(num_list)
        res = min(res, check(0, 0))
        res = min(res, check(5, 2))
        res = min(res, check(0, 5))
        res = min(res, check(5, 7))
        return res
''',
    call='Solution().minimumOperations("2905")',
    expect=2,
    views=[
        dict(type='text', size=32, h=70, fn=lambda S: (f"现在检查结尾 `{S['second']}{S['first']}`（倒数第二位 `{S['second']}`，最后一位 `{S['first']}`）" if 'first' in S else '要让末两位是 `00` `25` `50` `75` 之一')),
        dict(type='array', var='num_list', h=240, label='num_list', pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if 'p' in S and i == S['p'] and (v == S.get('first') or v == S.get('second')) else None,
             dim=lambda S, i, v: 'p' in S and i > S['p']),
        dict(type='text', size=34, h=80, fn=lambda S: f"当前最少操作 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    skip=['p -= 1'],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = len(num_list) - 1': '`p` 从最右边开始，先找最靠后的 `{first}`',
        'while p >= 0 and num_list[p] != first': lambda S, B, ret: f"`num_list[{S.p}] = {S.num_list[S.p]}`" + (f" 就是 {S.first}，停下" if S.p >= 0 and S.num_list[S.p] == S.first else f" 不是 {S.first}，`p` 左移") if S.p >= 0 else f"`p = -1`：整个数里没有 {S.first}",
        'while p >= 0 and num_list[p] != second': lambda S, B, ret: f"`num_list[{S.p}] = {S.num_list[S.p]}`" + (f" 就是 {S.second}，停下" if S.p >= 0 and S.num_list[S.p] == S.second else f" 不是 {S.second}，`p` 左移") if S.p >= 0 else f"`p = -1`：{S.first} 的左边找不到 {S.second}",
        'if p == -1': lambda S, B, ret: ('没找到，这种结尾做不到，只能退回保底的 `res`' if S.p == -1 else '找到了，继续'),
        'if first == 0': lambda S, B, ret: ('最后一位是 0：就算凑不成 00，也可以==留下这单独的 0==，少删一个' if S.first == 0 else '最后一位不是 0，没有保底可留'),
        'return len(num_list) - p - 2': '右边多余的数字全删，保留 `p` 和它右边那位：`{len(num_list)} - {p} - 2` = =={ret}==',
        'num_list = list': '把字符串拆成数字列表 `num_list`',
        'res = len(num_list)': lambda S, B, ret: ('保底：==全删光变成 0==，需要 `%d` 次' % len(S.num_list)) if S['_line'] > 20 else '`res` 先取 `len(num_list)`：这种结尾做不到时的退路，等于全删的次数',
        'res = min(res, check': '`res` 当前 =={res}==；接下来用 check 的结果取更小值',
        'return res': lambda S, B, ret: ('四种结尾和保底取最小，答案 ==%s==' % ret) if S['_line'] > 30 else '这种结尾做不到，返回退路 ==%s==' % ret,
    },
    cards=dict(
        one_liner='100 是 25 的倍数，只看末两位：00、25、50、75',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['删除 `num` 中任意位的数字，使它能被 `25` 整除（删光变成 `0`），求最少删除次数',
                 '示例：`"2905"` → `3`，删成 `"2900"`',
                 '`num` 不含前导零'],
        quote='只需让数字的最后两位是25的倍数就行了，也就是说本题实际上是要求删除最少的数字，使得最后两位变为00、25、50、75这四种情况之一。',
        quote_src='—— yiduobo 题解',
        idea=['对四种结尾分别检查：从后往前找最靠后的最后一位，再往左找倒数第二位',
              '两位都找到就把右边多余的数字删掉，次数是 `len - p - 2`',
              '保底：全删成 `0`；若数里有 `0`，可以留下它，只删 `len - 1` 个'],
        summary=['时间 `O(n)`，空间 `O(n)`（拆成数字列表）',
                 '`check(0, 0)` 找不到第二个 0 时，保底要少算一个：`first == 0` 时 `res -= 1`',
                 '四种结尾是 `(0,0) (5,2) (0,5) (5,7)`，第一个参数是最后一位',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
