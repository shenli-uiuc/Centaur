CREATE TABLE users(
    id BIGINT,
    screen_name VARCHAR(50),
    follower_num BIGINT,
    location VARCHAR(50), 

    PRIMARY KEY (id),
    INDEX (screen_name),
    INDEX (location)
)ENGINE=MyISAM CHARACTER SET=binary;
