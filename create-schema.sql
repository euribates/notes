CREATE TABLE note (
    id_note integer primary key,
    title text,
    body text,
    topic text
    );


CREATE VIRTUAL TABLE vnote USING fts5(
    id_note,
    title,
    body,
    topic,
    content=note,
    content_rowid=id_note
);

INSERT INTO vnote SELECT title, body, topic, id_note from note;
