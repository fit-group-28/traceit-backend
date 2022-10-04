create table "User" (
    id char(50) not null constraint user_pk primary key,
    username char(32),
    email char(320)
);
alter table "User" owner to postgres;
create table if not exists "UserCredentials" (
    id char(50) not null constraint usercredentials_id references "User" on update cascade on delete cascade,
    password char(128),
    salt char(16)
);
alter table "UserCredentials" owner to postgres;
create table if not exists "Supplier" (
    supplier_id serial not null constraint supplier_pk primary key,
    name char(64)
);
alter table "Supplier" owner to postgres;
create table if not exists "Product" (
    product_id serial not null constraint product_pk primary key,
    supplier_id integer constraint supplier_id references "Supplier",
    name char(64),
    price double precision,
    description varchar
);
alter table "Product" owner to postgres;
CREATE TYPE order_status AS ENUM ('placed', 'transit', 'fulfilled', 'cancelled');
create table if not exists "Order" (
    order_id serial not null constraint order_pk primary key,
    user_id char(50) constraint user_fk references "User" on update cascade on delete cascade,
    order_status order_status,
    date_placed date
);
alter table "Order" owner to postgres;
create table if not exists "Orderline" (
    order_id integer constraint order_id references "Order",
    product_id integer constraint product_id references "Product",
    quantity integer,
    subtotal double precision,
    PRIMARY KEY (order_id, product_id)
);
alter table "Orderline" owner to postgres;
INSERT INTO public."User" (id, username, email)
VALUES ('1', 'admin', 'admin@localhost');
INSERT INTO public."Supplier" (supplier_id, name)
VALUES (1, 'One''s Grocery shop');
INSERT INTO public."Supplier" (supplier_id, name)
VALUES (2, 'HongKong Supermarket');
INSERT INTO public."Product" (
        product_id,
        name,
        price,
        description,
        supplier_id
    )
VALUES (1, 'Milk', 4, '2L Milk', 1);
INSERT INTO public."Product" (
        product_id,
        name,
        price,
        description,
        supplier_id
    )
VALUES (2, 'Flour', 10, '10kg Bread Flour', 1);
INSERT INTO public."Product" (
        product_id,
        name,
        price,
        description,
        supplier_id
    )
VALUES (3, 'Rice', 20, '20kg Rice', 2);
INSERT INTO public."Order" (order_id, user_id, order_status, date_placed)
VALUES (1, '1', 'placed', '2020-01-01');
INSERT INTO public."Orderline" (order_id, product_id, quantity, subtotal)
VALUES (1, 1, 1, 4);
INSERT INTO public."Orderline" (order_id, product_id, quantity, subtotal)
VALUES (1, 2, 2, 10);