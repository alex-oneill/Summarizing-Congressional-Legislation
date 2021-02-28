CREATE TABLE IF NOT EXISTS bill_info (
    full_title text not null,
    name text not null,
    section text not null,
    link text not null,
    congress text not null,
    session text null,
    modified timestamp,

    PRIMARY KEY (full_title)
);

