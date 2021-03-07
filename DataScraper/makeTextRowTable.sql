CREATE TABLE IF NOT EXISTS text_row (
    id text not null,
    short_name text not null,
    name text not null,
    link text not null,
    full_title text not null,
    short_title text not null,
    summary_1 text not null,
    summary_2 text not null,
    summary_3 text not null,
    row_number int not null,
    row_text text not null,

    PRIMARY KEY (id)
);
