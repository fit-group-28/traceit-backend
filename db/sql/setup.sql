create table "User" (
    id char(50) not null constraint user_pk primary key,
    username char(32),
    email char(320)
);
alter table "User" owner to postgres;
create table if not exists "UserCredentials" (
    id char(50) not null constraint usercredentials_id references "User" on update cascade on delete cascade,
    password char(256),
    salt char(32)
);
alter table "UserCredentials" owner to postgres;
create table if not exists "Supplier" (
    supplier_id serial not null constraint supplier_pk primary key,
    name char(64),
    phone_number int,
    longitude float,
    latitude float
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


INSERT INTO public."Supplier" (
    name, 
    phone_number,
    longitude,
    latitude)
VALUES ('One''s Grocery shop', 12345678, -37.9280453, 145.1182741);

INSERT INTO public."Supplier" (
    name, 
    phone_number,
    longitude,
    latitude)
VALUES ('Two Dollor Shop', 12345678, -37.9263162, 145.1193540);

INSERT INTO public."Supplier" (
    name, 
    phone_number,
    longitude,
    latitude)
VALUES ('Hongkong Supermarket', 12345678, -37.8665312, 145.0936994);

INSERT INTO public."User" (id, username, email)
VALUES ('1', 'admin', 'admin@localhost');
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
