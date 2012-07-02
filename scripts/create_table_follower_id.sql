CREATE TABLE follower_id(
    id BIGINT,
    previous_cursor BIGINT,
    next_cursor BIGINT,
    follower_id blob,

    PRIMARY KEY (id, previous_cursor),
    INDEX (previous_cursor),
    INDEX (next_cursor)
)ENGINE=MyISAM CHARACTER SET=binary;
