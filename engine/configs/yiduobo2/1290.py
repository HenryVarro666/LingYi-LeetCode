import tracer

VALS = [1, 1, 0, 1]


def _col(S):
    n = S.get('now')
    return tracer._origin.get(n._uid, (0, None))[1] if n is not None else None


def _horner(S):
    k = _col(S)
    if k is None or 'res' not in S:
        return 'res = a[0]·2^(l-1) + a[1]·2^(l-2) + … + a[l-1]·2^0'
    e = str(VALS[0])
    for j in range(1, k + 1):
        e = f'({e})×2+{VALS[j]}' if j > 1 else f'{e}×2+{VALS[j]}'
    return f'`{e}` = =={S["res"]}=='


CONFIG = dict(
    num=1290, title='二进制链表转整数', difficulty='Easy', category='链表',
    author='yiduobo', technique='秦九韶式展开 · res += res + val',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def getDecimalValue(self, head):

        now = head
        res = now.val
        while now.next:
            now = now.next
            res += res + now.val

        return res
''',
    call=f'Solution().getDecimalValue(L({VALS}))',
    expect=13,
    views=[
        dict(type='text', fn=lambda S: '展开式：`res = (((a[0]×2 + a[1])×2 + a[2])×2 + …)×2 + a[l-1]`', size=26, h=60),
        dict(type='linked', label='链表（青 = now）', h=190, pointers={'now': 'cyan', 'head': 'green'}),
        dict(type='array', var=lambda S: VALS, label='a[k]（绿 = 已累加进 res，青 = now）', h=170, cell=84,
             color=lambda S, i, v: ('cyan' if i == _col(S) else 'green' if _col(S) is not None and i < _col(S) else None)),
        dict(type='text', fn=_horner, size=28, h=70),
    ],
    watch=[('now.val', 'now.val', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = head': '`now` 从链表头部出发',
        'res = now.val': '直接用第一个值初始化：`res = a[0] = {res}`（==链表不为空==，可以这么写）',
        'while now.next': lambda S, B, r: (f'`now.next` 存在（值 `{B.now.next.val}`）→ 继续往后走' if B.now.next
                                           else '`now.next` 为空：已经走到最后一个节点 → 结束'),
        'now = now.next': '`now` 后移到 `{now.val}`',
        'res += res + now.val': '`res += res + {now.val}` 即 `res = 2×{B.res} + {now.val}` = =={res}==：先乘 2 再加当前位',
        'return res': '返回 `res = {res}`：二进制 `1101` = 8+4+1',
    },
    cards=dict(
        one_liner='把 Σ a[k]·2^(l-1-k) 变形成“乘 2 加一位”的嵌套式',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表每个节点是 `0` 或 `1`，整条链表表示一个二进制数，==最高位在头部==',
                 '返回它的十进制值',
                 '示例：`[1,0,1]` → `5`；本视频：`[1,1,0,1]` → `13`'],
        quote='res = a[0]*2^(l-1) + … + a[l-1]*2^0，变形之后可得 res = (((a[0]*2 + a[1])*2 + a[2])*2 + ...)*2 + a[l-1]',
        quote_src='—— yiduobo 题解原文',
        idea=['直接按位权求和需要先知道长度 `l`',
              '变形成嵌套式后：==每一步把 res 乘 2，再加当前值==，不需要长度',
              '`res += res + now.val` 就是 `res = 2·res + now.val` 的紧凑写法'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`res` 初值取 `head.val`，所以循环条件是 `now.next`，==先移动再累加==',
                 '若改成 `res = 0` 起步，循环就要写成 `while now` 并先累加再移动',
                 '原文为 Python 2 写法，仅删去了类型注释的文档字符串'],
    ),
)
