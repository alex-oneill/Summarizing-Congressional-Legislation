CREATE TABLE IF NOT EXISTS bills_full_text (
    full_title text not null,
    short_name text not null,
    name text not null,
    section text not null,
    link text not null,
    congress text not null,
    session text null,
    bill_title text null,
    title_sum text null,
    publisher text null,
    date text null,
    header text null,
    words text null,

    PRIMARY KEY (full_title)
);
