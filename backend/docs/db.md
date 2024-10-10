# Database Design for Virtual Screen Manager

## Entities and Relationships

1. User
   - Represents a registered user of the application
   - Can create and manage multiple virtual screens

2. Virtual Screen
   - Represents a virtual screen created by a user
   - Belongs to one user
   - Can be accessed for read/write by a user via URL or by a chatbot via API

3. Session
   - Represents an active user session
   - Associated with one user

## Relationships

- A User can have many Virtual Screens (one-to-many)
- A Virtual Screen belongs to one User (many-to-one)
- A User can have many Sessions (one-to-many)

## Key Considerations

1. User authentication and authorization
2. Unique identifiers for Virtual Screens (e.g., URL path, API key)
3. Content storage for Virtual Screens
4. Session management and token storage

This simple entity-relationship model provides a foundation for the Virtual Screen Manager application. The next step would be to define the specific attributes for each entity and create the corresponding database schema.


## Database Schema (SQL DDL)

create table users (
    id serial primary key,
    username varchar(255) not null,
    password_hash varchar(255) not null
);

create table virtual_screens (
    id serial primary key,
    user_id int not null,
    name varchar(255) not null,
    url varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

create table sessions (
    id serial primary key, 
    user_id int not null,
    session_token varchar(255) not null,
    created_at timestamp default current_timestamp,
    expires_at timestamp not null
); 

