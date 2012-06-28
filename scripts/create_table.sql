CREATE TABLE twitter_data(
    id INT,
    screen_name VARCHAR(50),
    follower_id blob,
    location VARCHAR(50),

    PRIMARY KEY (id),
    INDEX (screen_name),
    INDEX (location)
)ENGINE=MyISAM CHARACTER SET=binary;
