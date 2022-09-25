create table if not exists "Shop"
(
    shop_id serial not null
        constraint customer_pk
            primary key,
    name char(16),
    address char(64),
    contact char(16)
);

alter table "Shop" owner to postgres;

create table if not exists "Product"
(
    product_id serial not null
        constraint product_pk
            primary key,
    name char(16),
    price double precision,
    description varchar
);

alter table "Product" owner to postgres;

create table if not exists "Supplier"
(
    supplier_id serial not null
        constraint supplier_pk
            primary key,
    name char(64)
);

alter table "Supplier" owner to postgres;

create table if not exists "Supplier_Product"
(
    supplier_id integer
        constraint supplier_id
            references "Supplier"
            on update cascade on delete cascade,
    product_id integer
        constraint product_id
            references "Product"
            on update cascade on delete cascade
);

alter table "Supplier_Product" owner to postgres;

create table if not exists "Order"
(
    order_id serial not null
        constraint order_pk
            primary key,
    shop_id integer
        constraint customer_id
            references "Shop",
    state char(16),
    date date
);

alter table "Order" owner to postgres;

create table if not exists "Orderline"
(
    line_id serial not null
        constraint orderline_pk
            primary key,
    order_id integer
        constraint order_id
            references "Order",
    product_id integer
        constraint product_id
            references "Product",
    quantity integer,
    subtotal double precision
);

alter table "Orderline" owner to postgres;

create table if not exists "Stock"
(
    product_id integer
        constraint stock_product_id
            references "Product",
    shop_id integer
        constraint stock_shop_id
            references "Shop",
    amount double precision
);

alter table "Stock" owner to postgres;

create table "User"
(
    id char(50) not null
        constraint user_pk
            primary key,
    username char(32),
    email char(64)
);

alter table "User" owner to postgres;

create table if not exists "UserCredentials"
(
    id char(50) not null
        constraint usercredentials_id
            references "User"
            on update cascade on delete cascade,
    password char(64),
    salt char(16)
);

alter table "UserCredentials" owner to postgres;


INSERT INTO public."Product" (product_id, name, price, description) VALUES (1, 'Milk', 4, '2L Milk');
INSERT INTO public."Product" (product_id, name, price, description) VALUES (2, 'Flour', 10, '10kg Bread Flour');
INSERT INTO public."Product" (product_id, name, price, description) VALUES (3, 'Rice', 20, '20kg Rice');

INSERT INTO public."Shop" (shop_id, name, address, contact) VALUES (1, 'Nelly''s shop', '1411/868 Blackburn rd Clayton', '0476718121');
INSERT INTO public."Shop" (shop_id, name, address, contact) VALUES (2, 'Douglas''s shop', '13 Renver Road, Clayton', '0476718121');

INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (1, 1, 20);
INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (2, 1, 5);
INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (3, 1, 10);
INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (1, 2, 0);
INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (2, 2, 15);
INSERT INTO public."Stock" (product_id, shop_id, amount) VALUES (3, 2, 0);

INSERT INTO public."Supplier" (supplier_id, name) VALUES (1, 'One''s Grocery shop');
INSERT INTO public."Supplier" (supplier_id, name) VALUES (2, 'HongKong Supermarket');

INSERT INTO public."Supplier_Product" (supplier_id, product_id) VALUES (1, 1);
INSERT INTO public."Supplier_Product" (supplier_id, product_id) VALUES (2, 2);
INSERT INTO public."Supplier_Product" (supplier_id, product_id) VALUES (2, 3);

INSERT INTO public."Order" (order_id, shop_id, state, date) VALUES (1, 1, 'ordered', '2022-08-10');
INSERT INTO public."Order" (order_id, shop_id, state, date) VALUES (2, 2, 'deliveried', '2022-08-08');

INSERT INTO public."Orderline" (line_id, order_id, product_id, quantity, subtotal) VALUES (1, 1, 1, 10, 40);
INSERT INTO public."Orderline" (line_id, order_id, product_id, quantity, subtotal) VALUES (2, 2, 1, 30, 120);
INSERT INTO public."Orderline" (line_id, order_id, product_id, quantity, subtotal) VALUES (3, 2, 3, 30, 400);

INSERT INTO public."User" (id, username, email) VALUES ("test","test","abc@test.com");