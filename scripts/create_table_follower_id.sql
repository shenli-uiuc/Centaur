CREATE TABLE follower_id(
    id INT,
    previous_cursor INT,
    next_cursor INT,
    follower_id blob,

    PRIMARY KEY (id, previous_cursor),
    INDEX (id, next_cursor)
)ENGINE=MyISAM CHARACTER SET=binary;
