-- we don't know how to generate root <with-no-name> (class Root) :(
create table location
(
	location_id serial not null
		constraint location_pk
			primary key,
	country varchar(128),
	city varchar(128),
	zipcode integer,
	street varchar(128),
	house integer
);

alter table location owner to postgres;

create unique index location_locationid_uindex
	on location (location_id);

create table customer
(
	username varchar(255) not null
		constraint customer_pkey
			primary key,
	email varchar(255) not null,
	name varchar(128) not null,
	surname varchar(128) not null,
	phone varchar(32) not null,
	location_id integer not null
		constraint location
			references location
);

alter table customer owner to postgres;

create unique index customer_username_uindex
	on customer (username);

create unique index customer_email_uindex
	on customer (email);

create unique index customer_phone_uindex
	on customer (phone);

create table workshop
(
	workshop_id serial not null
		constraint workshop_pkey
			primary key,
	open_time time not null,
	close_time time,
	location_id integer not null
		constraint location_fk
			references location
);

alter table workshop owner to postgres;

create unique index workshop_workshopid_uindex
	on workshop (workshop_id);

create table charging_station
(
	station_id serial not null
		constraint charging_station_pkey
			primary key,
	available_sockets integer not null,
	maximum_sockets integer not null,
	location_id integer
		constraint charging_station_location_location_id_fk
			references location
);

alter table charging_station owner to postgres;

create unique index charging_station_station_id_uindex
	on charging_station (station_id);

create table car_provider
(
	provider_id serial not null
		constraint car_provider_pkey
			primary key,
	company_name varchar(128) not null
);

alter table car_provider owner to postgres;

create unique index car_provider_provider_id_uindex
	on car_provider (provider_id);

create table model
(
	model_id serial not null
		constraint model_pk
			primary key,
	class varchar(64),
	max_charge integer not null,
	capacity integer not null,
	provider_id integer
		constraint provider_fk
			references car_provider
				on delete set null,
	price integer not null
);

alter table model owner to postgres;

create unique index model_modelid_uindex
	on model (model_id);

create table car
(
	car_id serial not null
		constraint car_pk
			primary key,
	model_id integer
		constraint model_fk
			references model,
	vin integer not null,
	available boolean default false,
	color text,
	number text
);

alter table car owner to postgres;

create unique index car_carid_uindex
	on car (car_id);

create unique index car_vin_uindex
	on car (vin);

create table request
(
	username varchar(255) not null
		constraint user_fk
			references customer,
	car_id integer not null
		constraint car_fk
			references car,
	payment integer not null,
	start_time timestamp not null,
	end_time timestamp not null,
	start_location_id integer
		constraint request_start_location_id
			references location,
	end_location_id integer
		constraint request_end_location_id
			references location,
	time_for_car_arrival timestamp,
	trip_duration timestamp
);

alter table request owner to postgres;

create table repairment
(
	car_id integer not null
		constraint car_fk
			references car,
	workshop_id integer
		constraint workshop_fk
			references workshop,
	start_date timestamp not null,
	end_date timestamp not null
);

alter table repair owner to postgres;

create table charging
(
	car_id integer not null
		constraint car_fk
			references car,
	station_id integer not null
		constraint station_fk
			references charging_station,
	start_date timestamp not null,
	end_date timestamp not null
);

alter table charging owner to postgres;

