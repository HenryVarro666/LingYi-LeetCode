def _expr(S):
    if 'lb' not in S:
        return ''
    left, right = S['left'], S['right']
    lb = S['lb']
    s = f"左括号在 `left[{lb}]` 前"
    if 'rb' in S and S.get('_inner', {}).get('rb') is not None:
        rb = S['rb']
        s += f"，右括号在 `right[{rb-1}]` 后：`{left[:lb]}({left[lb:]}+{right[:rb]}){right[rb:]}`"
    return s


CONFIG = dict(
    num=2232, title='向表达式添加括号后的最小结果', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举括号位置',
    tags=[],
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
        dict(type='string', var='left', pointers={'lb': 'blue'}, h=200, label='left（左括号插在下标 lb 之前）'),
        dict(type='string', var='right', pointers={'rb': 'pink'}, h=200, label='right（右括号插在下标 rb 之前）'),
        dict(type='text', h=70, fn=lambda S: (f"`{S['l1']} × ({S['l2']} + {S['r1']}) × {S['r2']} = ` =={S['l1']*(S['l2']+S['r1'])*S['r2']}==，当前最小 `mi = {S['mi']}`" if all(k in S for k in ('l1', 'l2', 'r1', 'r2')) and S.get('_line') else (f"`mi = {S['mi']}`" if 'mi' in S else ''))),
    ],
    watch=['lb', 'rb', ('mi', 'mi', 'green'), 'res_l', 'res_r'],
    captions={
        'expression.split': '按 `+` 拆开：`left = {left!r}`，`right = {right!r}`',
        'mi = int(left)': '先把「不加括号」的值 `{mi}` 当作初始最小值（括号包住整个数）',
        'res_l = 0': '初始括号位置：左括号在最前，右括号在最后',
        'if lb == 0': '`lb == 0`：左括号前没有数字，乘数 `l1` 取 ==1==' if False else '`lb == 0`？{"是：括号前为空，乘数取 1" if lb == 0 else "否：括号前有数字"}',
        'l1 = 1': '括号前为空，乘数 `l1 = 1`（不能取 0，否则乘积全为 0）',
        'l1 = int(left[:lb])': '括号左侧的数 `l1 = {l1}`',
        'l2 = int(left[lb:])': '括号内左加数 `l2 = {l2}`（至少一位）',
        'if rb == len(right)': '`rb == len(right)`？{"是：括号后为空，乘数取 1" if rb == len(right) else "否：括号后还有数字"}',
        'r2 = 1': '括号后为空，乘数 `r2 = 1`',
        'r2 = int(right[rb:])': '括号右侧的数 `r2 = {r2}`',
        'r1 = int(right[:rb])': '括号内右加数 `r1 = {r1}`（`rb` 从 1 起，保证右加数非空）',
        'if l1 * (l2 + r1) * r2 < mi': '`{l1} × ({l2} + {r1}) × {r2} = {l1*(l2+r1)*r2}`，和 `mi = {mi}` 比：{"更小 → 更新" if l1*(l2+r1)*r2 < mi else "不更小 → 跳过"}',
        'mi = l1': '更新最小值 `mi = {mi}`',
        'res_l = lb': '记下左括号位置 `res_l = {res_l}`',
        'res_r = rb': '记下右括号位置 `res_r = {res_r}`',
        'return left[:res_l]': '按记录的位置把括号插回去：=={ret}==',
    },
    skip=['res_r = len'],
    max_steps=90,
    cards=dict(
        one_liner='表达式最长才 10，直接枚举两个括号的位置',
        complexity='时间 `O(n²)`（再乘上取整数的开销），空间 `O(n)`',
        problem=['`expression` 形如 `"<num1>+<num2>"`，加一对括号使计算结果最小',
                 '左括号必须在 `+` 左侧，右括号在 `+` 右侧',
                 '示例：`"247+38"` → `"2(47+38)"`（值 170）'],
        quote='当确定了括号的位置后，表达式将被分成三个部分，分别是左括号左侧的数l1，左括号右侧的数l2与右括号左侧的数r1的和，以及右括号右侧的数r2。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度不超过 10，两层循环枚举 `lb`、`rb` 就够了',
              '括号内的两个加数不能为空；括号外的 `l1`、`r2` 可以为空，为空时按乘 1 处理',
              '每组位置算 `l1 × (l2 + r1) × r2`，更严格地更小才更新'],
        summary=['时间 `O(n²)`，空间 `O(n)`',
                 '易错点：外侧为空要取 1 而不是 0；`rb` 从 1 开始，`lb` 从 0 开始',
                 '用「不加括号」的值 `int(left)+int(right)` 作初值，括号包住全部时 `res_l=0, res_r=len(right)`',
                 '原文无需改动即可在 Python 3 运行'],
    ),
)
