CREATE TABLE follower_id(
    id BIGINT,
    offset BIGINT,
    previous_cursor BIGINT,
    next_cursor BIGINT,
    follower_id blob,

    PRIMARY KEY (id, offset),
    INDEX (id),
    INDEX (offset),
    INDEX (previous_cursor),
    INDEX (next_cursor)
)ENGINE=MyISAM CHARACTER SET=binary;
