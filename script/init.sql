create table chat
(
    serialnum int,
    id        varchar(16),
    seq       int,
    role      int          not null,
    message   varchar(256) not null,
    type      int          not null,
    primary key (serialnum, id, seq)
);

create table dict
(
    key   varchar(256),
    value varchar(256),
    type  int not null,
    constraint dict_pk
        primary key (key, value)
);

create table user
(
	id varchar(16)
		constraint user_pk
			primary key,
	name varchar(16),
	age int
);



insert into user(id, name, age) values ('anonymous','anonymous',0);
