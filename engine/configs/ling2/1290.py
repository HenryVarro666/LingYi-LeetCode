import tracer

VALS = [1, 0, 1, 1, 0]


def _col(S, name='head'):
    h = S.get(name)
    if h is None:
        return len(VALS) if 'ans' in S else None
    return tracer._origin.get(h._uid, (0, None))[1]


def _bin(S):
    if 'ans' not in S:
        return ''
    k = _col(S)
    done = VALS[:k] if k is not None else []
    b = ''.join(map(str, done)) or '0'
    return f"已拼好的二进制：`{b}` (2) = 十进制 =={S['ans']}=="


def _cap_while(S, B, ret):
    if B.head is None:
        return '`head` 为空：所有比特都已拼进 `ans` → 结束循环'
    return f'`head` 非空，当前比特 `{B.head.val}`'


CONFIG = dict(
    num=1290, title='二进制链表转整数', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='遍历链表 · 乘 2 再加当前位',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        ans = 0
        while head:
            ans = ans * 2 + head.val
            head = head.next
        return ans
''',
    call=f'Solution().getDecimalValue(L({VALS}))',
    expect=22,
    views=[
        dict(type='text', fn=lambda S: '类比十进制 `[1,2,3]` → `((0×10+1)×10+2)×10+3 = 123`；二进制把 ==10 换成 2==', size=26, h=60),
        dict(type='linked', label='链表（蓝 = head，最高位在头部）', h=190, pointers={'head': 'blue'}),
        dict(type='array', var=lambda S: VALS, label='每个节点的比特（绿 = 已拼进 ans，蓝 = 当前 head）', h=170, cell=84,
             color=lambda S, i, v: ('green' if _col(S) is not None and i < _col(S) else 'blue' if i == _col(S) else None)),
        dict(type='text', fn=_bin, size=28, h=70),
    ],
    watch=[('head.val', 'head.val', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '初始化答案为 `0`：相当于还没有任何二进制位',
        'while head': _cap_while,
        'ans = ans * 2': '`{B.ans} × 2 + {head.val}` = =={ans}==（二进制 `{bin(B.ans)[2:]}` → `{bin(ans)[2:]}`）：乘 2 = 左移一位，新比特补在最低位',
        'head = head.next': lambda S, B, r: f'准备遍历下一个节点：`head` → `{S["head"].val}`' if S.get('head') else '准备遍历下一个节点：`head` → `None`，链表走完了',
        'return ans': '返回 `ans = {ans}`，即二进制 `10110` 的十进制值',
    },
    cards=dict(
        one_liner='像把字符串转整数一样：答案 ×2 再加当前位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['单链表每个节点值是 `0` 或 `1`，整条链表是一个二进制数，==最高位在头部==',
                 '返回它的==十进制值==',
                 '示例：`[1,0,1]` → `5`；本视频：`[1,0,1,1,0]` → `22`'],
        quote='问题相当于给你一串 0 和 1，把它们拼成一个二进制数。类比把字符串转成十进制整数的方式……==乘 2 等价于左移 1==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['十进制：`0×10+1=1`，`1×10+2=12`，`12×10+3=123`',
              '二进制同理：每来一个比特，`ans = ans * 2 + head.val`',
              '用遍历链表的标准框架 `while head: ... head = head.next` 即可'],
        summary=['时间 `O(n)`，空间 `O(1)`，`n ≤ 30` 不会溢出',
                 '易错：不要先求长度再算 `2^(l-1)`，==边走边乘 2== 更简单',
                 '`ans * 2` 也可以写成 `ans << 1 | head.val`（位运算版）',
                 '同类：8 题字符串转整数、把数字串拼成整数的所有场景'],
    ),
)
