CONFIG = dict(
    num=2232, title='向表达式添加括号后的最小结果', difficulty='Medium', category='模拟',
    author='yiduobo', technique='枚举左右括号位置', tags=[],
    code='''
class Solution(object):
    def minimizeResult(self, expression):

        left, right = expression.split('+')

        mi = int(left) + int(right)
        res_l = 0
        res_r = len(right)
        for lb in range(0, len(left)):
            if lb == 0:
                l1 = 1
            else:
                l1 = int(left[:lb])
            
            l2 = int(left[lb:])
        
            for rb in range(1, len(right) + 1):
                if rb == len(right):
                    r2 = 1
                else:
                    r2 = int(right[rb:])
                
                r1 = int(right[:rb])

                if l1 * (l2 + r1) * r2 < mi:
                    mi = l1 * (l2 + r1) * r2
                    res_l = lb
                    res_r = rb
        
        return left[:res_l] + '(' + left[res_l:] + '+' + right[:res_r] + ')' + right[res_r:]
''',
    call='Solution().minimizeResult("247+38")',
    expect='2(47+38)',
    views=[
        dict(type='string', var='left', label='left', pointers={'lb': 'blue'}, h=170),
        dict(type='string', var='right', label='right', pointers={'rb': 'pink'}, h=170),
        dict(type='text', fn=lambda S: (f"`l1={S['l1']}` × (`l2={S['l2']}` + `r1={S['r1']}`) × `r2={S['r2']}` = =={S['l1']*(S['l2']+S['r1'])*S['r2']}==") if all(k in S for k in ('l1', 'l2', 'r1', 'r2')) else '', size=34, h=130),
        dict(type='text', fn=lambda S: f"当前最小 ==`{S['mi']}`==" if 'mi' in S else '', size=36, h=70),
    ],
    watch=['lb', 'rb', ('mi', 'mi', 'green'), 'res_l', 'res_r'],
    captions={
        'left, right =': '以 `+` 为界：`left = {left}`，`right = {right}`',
        'mi = int(left)': '先用「不加括号」的和当初始最小值：`mi = {mi}`',
        'res_l = 0': '`res_l`、`res_r` 记最优括号位置',
        'res_r = len': '初始相当于括号包住整个式子',
        'for lb in range': '左括号插在 `left` 的第 `{lb}` 位前',
        'l1 = 1': '括号左边没有数 → `l1 = 1`，乘 1 不影响结果',
        'l1 = int(left[:lb])': '括号左边的数：`l1 = {l1}`',
        'l2 = int': '括号内左加数：`l2 = {l2}`（不能为空）',
        'for rb in range': '右括号插在 `right` 前 `{rb}` 位之后',
        'r2 = 1': '括号右边没有数 → `r2 = 1`',
        'r2 = int(right[rb:])': '括号右边的数：`r2 = {r2}`',
        'r1 = int': '括号内右加数：`r1 = {r1}`（不能为空）',
        'if l1 *': lambda S, B, r: f'`{S.l1}×({S.l2}+{S.r1})×{S.r2} = {S.l1*(S.l2+S.r1)*S.r2}` 比 `mi = {S.mi}` ' + ('更小 → 更新' if S.l1*(S.l2+S.r1)*S.r2 < S.mi else '不小 → 跳过'),
        'mi = l1': '最小值更新为 `{mi}`',
        'res_l = lb': '记下左括号位置 `{res_l}`',
        'res_r = rb': '记下右括号位置 `{res_r}`',
        'return left': '按最优位置插入括号：`{ret}`',
    },
    cards=dict(
        one_liner='长度不超过 10，把括号位置全枚举一遍',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['在 `+` 两侧各加一个括号，使表达式值最小',
                 '括号外没有数字时当作乘 1',
                 '示例：`"247+38"` → `"2(47+38)"`'],
        quote='当确定了括号的位置后，表达式将被分成三个部分，分别是左括号左侧的数l1，左括号右侧的数l2与右括号左侧的数r1的和，以及右括号右侧的数r2。',
        quote_src='—— yiduobo 题解原文',
        idea=['括号内的两个加数 `l2`、`r1` 不能为空，所以 `lb` 可从 0 起、`rb` 从 1 起',
              '`l1`、`r2` 可以为空，空时取 1',
              '用 `l1*(l2+r1)*r2` 更新最小值，同时记下两个括号的位置'],
        summary=['原文为 Python 2 风格，只删去了类型说明文档字符串，本题无需其他改动',
                 '时间 `O(n²)`，空间 `O(n)`',
                 '易错：右括号上界是 `len(right)`，此时 `r2` 为空取 1',
                 '最后用切片重新拼出带括号的字符串'],
    ),
)
