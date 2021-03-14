CREATE TABLE IF NOT EXISTS money_hits (
    id text not null,
    hit_type text not null,
    row_number int not null,
    row_text text not null,

    PRIMARY KEY (id)
);