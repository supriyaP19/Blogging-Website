drop table if exists users;
    CREATE TABLE user(
    name text not null,gender text,
    password text not null,
    username text not null,
    email text not null,
    urlblog text not null,
    urltitle text not null
);