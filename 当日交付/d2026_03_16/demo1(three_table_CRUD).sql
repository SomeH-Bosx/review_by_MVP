-- 完成时间：2026.03.23
-- 创建数据库demo1【默认属性】
create
    database if not exists
    demo1
    default charset utf8mb4;

use demo1;
show tables;

-- 以基础业务系统为例子：
-- 完成用户表、商品表、订单表的创建，以及完整的正删改查

-- 创建
-- 1. 用户表（user):存储用户基础信息
create table if not exists users (
    id int primary key auto_increment comment '用户ID（主键，自增）',
    username varchar(50) not null unique comment '用户名（唯一',
    password varchar(100) not null comment '密码（建议加密存储）',
    phone varchar(20) comment '手机号',
    create_time datetime default current_timestamp comment '创建时间'
) comment = '用户表';

-- 2. 商品表（products）：存储商品信息
create table if not exists products(
    id int primary key auto_increment comment '商品ID（主键，自增）',
    product_name varchar(100) not null comment '商品名称',
    price decimal(10, 2) not null comment '商品价格（保留2位小数）',
    stock int default 0 comment '商品库存',
    create_time datetime default current_timestamp comment '创建时间'
) comment = '商品表';

-- 3. 订单表（orders）：存储用户下单信息（关联用户和商品）
create table if not exists orders(
    id int primary key auto_increment comment '订单ID（主键，自增）',
    user_id int not null comment '关联用户ID',
    product_id int not null  comment '关联商品表ID',
    order_num varchar(50) not null unique comment '订单编号',
    amount decimal(10, 2) not null comment '订单金额',
    create_time datetime default current_timestamp comment '创建时间',

    -- 外键关联（增强数据完整性）
    foreign key (user_id) references users(id) on delete cascade,
    foreign key (product_id) references products(id) on delete cascade
) comment = '订单表';

-- 数据的增删改查操作（CRUD）
-- 1.新增数据（create）

-- 新增用户
insert into users(username, password, phone)
values('zhangsan', '123456', '13800138000'),
      ('lisi', '654321', '13900139000');

-- 新增商品
insert into products(product_name, price, stock)
values('小米手机', 1999.99, 100),
      ('华为手机', 299.99, 500);

-- 新增订单（关联用户ID=1,商品ID=1）
insert into orders(user_id, product_id, order_num, amount)
values(1, 1, 'order20260323001', 1999.99),
      (2, 2, 'order20260323002', 299.99);


-- 2. 查询数据（read）【涵盖单表、多表以及条件查询】
-- 查询所有用户
select * from users;

-- 查询价格 < 500的商品（条件）
select id, products.product_name, price from products where price < 500;

-- 关联查询：查询订单详情（包含用户名、商品名）
select
    o.id as 订单ID,
    u.username as 用户名,
    p.product_name as 商品名,
    o.order_num as 订单编号,
    o.amount as 订单金额
from orders o
join users u on o.user_id = u.id
join products p on o.product_id = p.id;


-- 3. 修改数据（update）
-- 修改用户手机号（条件：用户名=zhangsan）
update users set phone = '138111138111' where username = 'zhangsan';

-- 修改商品库存（条件：商品ID = 1）
update products set stock = 99 where id = 1;

-- 修改订单金额（条件：订单编号=order20260323002）
update orders set amount = 289.99 where order_num = 'order20260323002';


-- 4. 删除数据（delete）
-- 删除指定用户（条件：ID=2，注意：外键级联删除会同步删除该用户的订单）、
delete from users where id = 2;

-- 删除库存为0的商品（当前无符合条件数据）【可正常运行不报错】
delete from products where stock = 0;

-- 删除指定订单（条件：ID=1)
delete from orders where id = 1;