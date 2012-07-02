CREATE TABLE follower_id(
    id INT,
    previous_cursor VARCHAR(50),
    next_cursor VARCHAR(50),
    follower_id blob,

    PRIMARY KEY (id, previous_cursor),
    INDEX (id, next_cursor)
)ENGINE=MyISAM CHARACTER SET=binary;
