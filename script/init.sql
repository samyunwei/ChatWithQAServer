create table chat
(
	serialnum int,
	id varchar(16),
	seq int,
	role int,
	message varchar(256),
	primary key (serialnum, id, seq)
);

create table dict
(
	key varchar(256)
		constraint dict_pk
			primary key,
	value varchar(256)
);

create table user
(
	id varchar(16)
		constraint user_pk
			primary key,
	name varchar(16),
	age int
);

