-- users table
create table users (
  id uuid primary key default uuid_generate_v4(),
  email text unique not null,
  password text not null,
  role text not null check (role in ('user', 'admin'))
);

-- vehicles table
create table vehicles (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  type text not null,
  available boolean not null default true
);

-- bookings table
create table bookings (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id),
  vehicle_id uuid references vehicles(id),
  booking_date timestamp default current_timestamp,
  returned boolean not null default false
);