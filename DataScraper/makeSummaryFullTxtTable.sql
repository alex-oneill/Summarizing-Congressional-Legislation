CREATE TABLE IF NOT EXISTS sum_full_text (
    full_title text not null,
    name text not null,
    section text not null,
    congress text not null,
    title_sum text not null,
    sum_text text not null,
    measure_type text not null,
    measure_number text not null,
    origin_chamber text not null,
    orig_publish timestamp not null,

    PRIMARY KEY (full_title)
);
